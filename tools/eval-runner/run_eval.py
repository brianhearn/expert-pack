#!/usr/bin/env python3
"""
ExpertPack Pack-Agnostic Eval Runner

Supports four evaluation modes:
  - full         : loads up to 80K chars of pack Markdown as context (default)
  - rag          : retrieves top-K atoms per question via local SQLite FTS5/BM25
                   or a running ep-mcp HTTP endpoint (--mcp-url)
  - without-pack : blind baseline with NO pack context (proves what model knows alone)
  - compare      : runs both without-pack and rag (or full) and computes the delta,
                   tagging confirmed model misses as knowledge_gap_verified

Also enforces optional pack_version pinning (P36): if an eval file or question
declares `pack_version`, run_eval checks it against manifest.yaml and fails on
drift unless --allow-version-drift is passed.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: pyyaml required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "openrouter/openai/gpt-4o-mini"
DEFAULT_JUDGE_MODEL = "openrouter/openai/gpt-4o-mini"
MAX_CONTEXT_CHARS = 80_000

PRIORITY_FILES = ["overview.md", "glossary.md", "manifest.yaml"]
PRIORITY_DIRS = ["concepts", "workflows", "troubleshooting", "faq", "phases", "decisions", "gotchas"]
SKIP_DIRS = {".git", ".obsidian", ".ep-mcp", "node_modules", "__pycache__", ".venv", "eval"}

_STOPWORDS = frozenset({
    "the", "and", "for", "with", "that", "this", "from", "what", "when", "how",
    "why", "does", "are", "was", "were", "can", "you", "your", "should", "into",
    "about", "have", "has", "not", "use", "using", "between", "difference",
})


# ---------------------------------------------------------------------------
# Manifest + version pinning (P36)
# ---------------------------------------------------------------------------

def load_pack_manifest(pack_path: Path) -> dict:
    mf = pack_path / "manifest.yaml"
    if not mf.is_file():
        return {}
    data = yaml.safe_load(mf.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def check_version_pinning(pack_manifest: dict, eval_data: dict) -> list[str]:
    """Return list of version-drift messages if pinned pack_version != manifest.version."""
    actual = str(pack_manifest.get("version") or "").strip()
    if not actual:
        return []
    mismatches: list[str] = []
    suite_pin = eval_data.get("pack_version")
    if suite_pin is not None and str(suite_pin).strip() != actual:
        mismatches.append(
            f"Eval suite pinned to pack_version={suite_pin!r}, but pack manifest.version is {actual!r}"
        )
    for q in eval_data.get("questions", []):
        qpin = q.get("pack_version")
        if qpin is not None and str(qpin).strip() != actual:
            mismatches.append(
                f"Question {q.get('id', '?')} pinned to pack_version={qpin!r}, "
                f"but pack manifest.version is {actual!r}"
            )
    return mismatches


# ---------------------------------------------------------------------------
# Pack context loading (full-context mode)
# ---------------------------------------------------------------------------

def load_pack_context(pack_path: Path) -> str:
    """Load pack markdown files as a single context string up to MAX_CONTEXT_CHARS."""
    if not pack_path.exists():
        print(f"Error: Pack path does not exist: {pack_path}", file=sys.stderr)
        sys.exit(1)

    chunks: list[str] = []
    total_chars = 0
    seen: set[Path] = set()

    def add_file(fp: Path):
        nonlocal total_chars
        if fp in seen or total_chars >= MAX_CONTEXT_CHARS:
            return
        if fp.name in {"_index.md", "source-coverage.md"}:
            return
        rel_parts = fp.relative_to(pack_path).parts
        if any(part in SKIP_DIRS for part in rel_parts):
            return
        seen.add(fp)
        try:
            content = fp.read_text(encoding="utf-8")
            if len(content.strip()) < 10:
                return
            header = f"\n\n--- FILE: {fp.relative_to(pack_path).as_posix()} ---\n"
            chunk = header + content
            remaining = MAX_CONTEXT_CHARS - total_chars
            if len(chunk) > remaining:
                chunk = chunk[:remaining] + "\n[...truncated]"
            chunks.append(chunk)
            total_chars += len(chunk)
        except OSError:
            pass

    for fname in PRIORITY_FILES:
        fp = pack_path / fname
        if fp.exists():
            add_file(fp)
    for dname in PRIORITY_DIRS:
        for fp in sorted(pack_path.rglob(f"{dname}/**/*.md")):
            if total_chars < MAX_CONTEXT_CHARS:
                add_file(fp)
    for fp in sorted(pack_path.rglob("*.md")):
        if total_chars >= MAX_CONTEXT_CHARS:
            break
        add_file(fp)

    context = "".join(chunks)
    print(f"Loaded pack context: {len(chunks)} files, {total_chars:,} chars")
    return context


# ---------------------------------------------------------------------------
# Local SQLite FTS5/BM25 Retriever (for --mode rag / compare without API keys)
# ---------------------------------------------------------------------------

class LocalBM25Retriever:
    """Zero-dependency in-memory SQLite FTS5/BM25 retriever over a pack's Markdown atoms."""

    def __init__(self, pack_path: Path):
        self.pack_path = pack_path
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.conn.execute(
            "CREATE VIRTUAL TABLE docs USING fts5(rel_path, title, content, tokenize='porter unicode61')"
        )
        self.doc_count = 0
        self._index_pack()

    def _index_pack(self) -> None:
        for fp in sorted(self.pack_path.rglob("*.md")):
            rel_parts = fp.relative_to(self.pack_path).parts
            if any(part in SKIP_DIRS for part in rel_parts):
                continue
            if fp.name in {"_index.md", "source-coverage.md", "meta-source-coverage.md"}:
                continue
            raw = fp.read_text(encoding="utf-8", errors="replace")
            title = fp.stem.replace("-", " ")
            body = raw
            if raw.startswith("---\n") or raw.startswith("---\r\n"):
                end = raw.find("\n---", 3)
                if end != -1:
                    fm_raw = raw[4:end]
                    body = raw[end + 4:].lstrip("\r\n")
                    try:
                        fm = yaml.safe_load(fm_raw) or {}
                        if isinstance(fm, dict):
                            if fm.get("retrieval_strategy") in {"navigation", "on_demand"}:
                                continue
                            if fm.get("title"):
                                title = str(fm["title"])
                    except yaml.YAMLError:
                        pass
            rel = fp.relative_to(self.pack_path).as_posix()
            self.conn.execute(
                "INSERT INTO docs (rel_path, title, content) VALUES (?, ?, ?)",
                (rel, title, body),
            )
            self.doc_count += 1
        self.conn.commit()

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        tokens = [
            t for t in re.sub(r"[^\w\s]", " ", query).lower().split()
            if len(t) >= 3 and t not in _STOPWORDS
        ]
        if not tokens:
            tokens = re.sub(r"[^\w\s]", " ", query).lower().split()[:5]
        if not tokens:
            return []
        fts_query = " OR ".join(f'"{t}"' for t in tokens[:12])
        rows = self.conn.execute(
            "SELECT rel_path, title, content, bm25(docs, 0.5, 2.0, 1.0) AS rank "
            "FROM docs WHERE docs MATCH ? ORDER BY rank LIMIT ?",
            (fts_query, top_k),
        ).fetchall()
        return [
            {
                "source_file": r["rel_path"],
                "title": r["title"],
                "text": r["content"],
                "score": round(-float(r["rank"]), 4),
            }
            for r in rows
        ]

    def close(self) -> None:
        self.conn.close()


def retrieve_via_mcp(mcp_url: str, pack_slug: str, query: str, top_k: int = 5, token: str = "") -> list[dict]:
    """Query a running ep-mcp HTTP /search endpoint."""
    import requests

    headers = {"Authorization": f"Bearer {token}"} if token else {}
    resp = requests.get(
        mcp_url,
        params={"q": query, "pack": pack_slug, "n": top_k},
        headers=headers,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    hits = data.get("results", data) if isinstance(data, dict) else data
    return hits if isinstance(hits, list) else []


def format_rag_context(hits: list[dict], max_chars: int = 24_000) -> str:
    parts: list[str] = []
    total = 0
    for h in hits:
        src = h.get("source_file", "unknown")
        tok = h.get("provenance_token") or src
        body = str(h.get("text") or "")
        block = f"\n\n--- SOURCE: {tok} ({src}) ---\n{body}"
        if total + len(block) > max_chars:
            block = block[: max(0, max_chars - total)] + "\n[...truncated]"
        parts.append(block)
        total += len(block)
        if total >= max_chars:
            break
    return "".join(parts)


# ---------------------------------------------------------------------------
# Eval YAML loading
# ---------------------------------------------------------------------------

def load_eval_set(path: Path) -> dict:
    """Load and validate eval YAML following schemas/eval.md."""
    if not path.exists():
        print(f"Error: Eval file not found: {path}", file=sys.stderr)
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    questions = data.get("questions", [])
    if not questions:
        print(f"Error: No questions found in {path}", file=sys.stderr)
        sys.exit(1)

    required_fields = ("id", "question", "expected_answer", "category", "ek_dependent")
    for i, q in enumerate(questions):
        for field in required_fields:
            if field not in q:
                print(f"Error: Question {i+1} (id={q.get('id','?')}) missing required field '{field}'", file=sys.stderr)
                sys.exit(1)

    print(f"Loaded {len(questions)} questions from {path}")
    return data


# ---------------------------------------------------------------------------
# OpenRouter API
# ---------------------------------------------------------------------------

def load_api_key() -> str:
    """Load OpenRouter API key from environment or .env file."""
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if key:
        return key

    for env_path in ["/root/.openclaw/.env", os.path.expanduser("~/.openclaw/.env"), ".env"]:
        if os.path.exists(env_path):
            with open(env_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("OPENROUTER_API_KEY="):
                        key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if key:
                            return key
    return ""


def call_llm(prompt: str, model: str, api_key: str, temperature: float = 0.3) -> dict:
    """Call OpenRouter and return response text + token usage."""
    import requests

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
    }

    try:
        resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"].strip()
        usage = data.get("usage", {})
        return {
            "text": content,
            "input_tokens": usage.get("prompt_tokens", 0),
            "output_tokens": usage.get("completion_tokens", 0),
        }
    except Exception as e:
        return {"text": f"[ERROR] {e}", "input_tokens": 0, "output_tokens": 0}


# ---------------------------------------------------------------------------
# Prompt building
# ---------------------------------------------------------------------------

def build_question_prompt(context: str | None, question: str, authority_in_scope: str = "") -> str:
    if context is None:
        return (
            f"QUESTION: {question}\n\n"
            "Answer concisely and factually from your own knowledge. "
            "If you are unsure or the topic is outside scope, say so clearly."
        )
    scope_line = f"Scope of this knowledge base: {authority_in_scope}\n" if authority_in_scope else ""
    return (
        f"KNOWLEDGE BASE:\n{context}\n\n---\n\n{scope_line}"
        f"QUESTION: {question}\n\n"
        "Answer based on the knowledge base above. If this question is outside the scope of this "
        'knowledge base, say: "This question is outside the scope of this knowledge base."'
    )


def build_judge_prompt(question: dict, response: str) -> str:
    category = question.get("category", "")
    expected = question["expected_answer"]
    required_facts = question.get("required_facts", [])
    anti_hallucination = question.get("anti_hallucination", [])
    is_refusal = category in ("refusal", "out-of-scope")

    facts_section = ""
    if required_facts:
        facts_section = "\nREQUIRED FACTS (must be present for full correctness):\n"
        facts_section += "\n".join(f"- {f}" for f in required_facts)

    anti_section = ""
    if anti_hallucination:
        anti_section = "\nANTI-HALLUCINATION CHECKS (response must NOT contain these):\n"
        anti_section += "\n".join(f"- {f}" for f in anti_hallucination)

    refusal_note = ""
    if is_refusal:
        refusal_note = "\nNOTE: This is an OUT-OF-SCOPE question. The correct behavior is to decline or state it is outside scope."

    return f"""You are an evaluation judge scoring an AI assistant's response.

QUESTION: {question['question']}

EXPECTED ANSWER: {expected}
{facts_section}{anti_section}{refusal_note}

ACTUAL RESPONSE:
{response}

Score the response. Return ONLY valid JSON (no markdown fences):
{{
  "correctness": <float 0.0-1.0, fraction of key facts from expected_answer present in response>,
  "groundedness": <float 0.0-1.0, how well the response sticks to facts vs fabricating>,
  "hallucinations": [<list of specific wrong claims found, or empty list>],
  "refusal_correct": <true if out-of-scope question was properly declined, false if not, null if not out-of-scope>,
  "notes": "<brief explanation>"
}}

Be strict but fair. A fact counts as present if the response conveys the same meaning even if phrased differently."""


def _aggregate(results: list[dict]) -> dict:
    n = len(results)
    avg_correctness = sum(r["correctness"] for r in results) / n if n else 0.0
    avg_groundedness = sum(r["groundedness"] for r in results) / n if n else 0.0
    hallucination_count = sum(1 for r in results if r["hallucinations"])
    hallucination_rate = hallucination_count / n if n else 0.0

    refusal_qs = [r for r in results if r["category"] in ("refusal", "out-of-scope")]
    refusal_correct = sum(1 for r in refusal_qs if r.get("refusal_correct") is True)
    refusal_accuracy = refusal_correct / len(refusal_qs) if refusal_qs else None

    ek_qs = [r for r in results if r.get("ek_dependent")]
    ek_correctness = sum(r["correctness"] for r in ek_qs) / len(ek_qs) if ek_qs else None
    avg_latency = sum(r["latency_ms"] for r in results) / n if n else 0

    return {
        "correctness": round(avg_correctness, 3),
        "groundedness": round(avg_groundedness, 3),
        "hallucination_rate": round(hallucination_rate, 3),
        "hallucination_count": hallucination_count,
        "refusal_accuracy": round(refusal_accuracy, 3) if refusal_accuracy is not None else None,
        "ek_correctness": round(ek_correctness, 3) if ek_correctness is not None else None,
        "avg_latency_ms": int(avg_latency),
    }


def _execute_pass(
    *,
    mode: str,
    questions: list[dict],
    pack_path: Path,
    pack_manifest: dict,
    model: str,
    judge_model: str,
    api_key: str,
    delay: float,
    top_k: int,
    mcp_url: str | None,
    mcp_token: str,
) -> tuple[list[dict], dict]:
    full_context = load_pack_context(pack_path) if mode == "full" else None
    retriever = LocalBM25Retriever(pack_path) if (mode == "rag" and not mcp_url) else None
    ab = pack_manifest.get("authority_boundary") or {}
    in_scope = str(ab.get("in_scope") or "") if isinstance(ab, dict) else ""
    pack_slug = str(pack_manifest.get("slug") or pack_path.name)

    results: list[dict] = []
    tokens = {"model_input": 0, "model_output": 0, "judge_input": 0, "judge_output": 0}

    try:
        for i, q in enumerate(questions):
            qid = q["id"]
            print(f"[{mode}] [{i+1}/{len(questions)}] {qid} ({q.get('category','?')}): {q['question'][:50]}...", end=" ", flush=True)
            retrieved_files: list[str] = []
            if mode == "without-pack":
                ctx = None
            elif mode == "rag":
                if mcp_url:
                    hits = retrieve_via_mcp(mcp_url, pack_slug, q["question"], top_k=top_k, token=mcp_token)
                else:
                    assert retriever is not None
                    hits = retriever.retrieve(q["question"], top_k=top_k)
                retrieved_files = [h.get("source_file", "") for h in hits if h.get("source_file")]
                ctx = format_rag_context(hits)
            else:
                ctx = full_context

            t0 = time.time()
            prompt = build_question_prompt(ctx, q["question"], authority_in_scope=in_scope)
            answer_result = call_llm(prompt, model, api_key, temperature=0.3)
            latency_ms = int((time.time() - t0) * 1000)

            response = answer_result["text"]
            tokens["model_input"] += answer_result["input_tokens"]
            tokens["model_output"] += answer_result["output_tokens"]

            if response.startswith("[ERROR]") or response.startswith("[HTTP_ERROR]"):
                print("ERROR")
                score = {
                    "correctness": 0.0, "groundedness": 0.0,
                    "hallucinations": [], "refusal_correct": None,
                    "notes": response,
                }
            else:
                judge_prompt = build_judge_prompt(q, response)
                judge_result = call_llm(judge_prompt, judge_model, api_key, temperature=0.0)
                tokens["judge_input"] += judge_result["input_tokens"]
                tokens["judge_output"] += judge_result["output_tokens"]

                raw = judge_result["text"]
                if raw.startswith("```"):
                    lines = raw.split("\n")
                    raw = "\n".join(lines[1:])
                    if raw.endswith("```"):
                        raw = raw[:-3]
                    raw = raw.strip()
                try:
                    score = json.loads(raw)
                except json.JSONDecodeError:
                    score = {
                        "correctness": 0.0, "groundedness": 0.0,
                        "hallucinations": [], "refusal_correct": None,
                        "notes": f"Judge returned invalid JSON: {raw[:100]}",
                    }

            print(f"correctness={float(score.get('correctness', 0)):.2f} ({latency_ms}ms)")
            entry = {
                "id": qid,
                "category": q.get("category", ""),
                "ek_dependent": q.get("ek_dependent", False),
                "correctness": round(float(score.get("correctness", 0)), 3),
                "groundedness": round(float(score.get("groundedness", 0)), 3),
                "hallucinations": score.get("hallucinations", []),
                "refusal_correct": score.get("refusal_correct"),
                "latency_ms": latency_ms,
                "response_preview": response[:300],
                "notes": score.get("notes", ""),
            }
            if retrieved_files:
                entry["retrieved_files"] = retrieved_files
            results.append(entry)

            if delay > 0 and i < len(questions) - 1:
                time.sleep(delay)
    finally:
        if retriever is not None:
            retriever.close()

    tokens["total"] = sum(tokens.values())
    return results, tokens


# ---------------------------------------------------------------------------
# Main eval loop
# ---------------------------------------------------------------------------

def run_eval(args):
    pack_path = Path(args.pack)
    eval_path = Path(args.eval)
    output_path = Path(args.output) if args.output else Path(
        f"results/{pack_path.name}-{args.mode}-{datetime.now(timezone.utc).strftime('%Y-%m-%d-%H%M')}.yaml"
    )

    pack_manifest = load_pack_manifest(pack_path)
    eval_data = load_eval_set(eval_path)
    questions = eval_data["questions"]

    # P36: Enforce pack_version pinning
    drift = check_version_pinning(pack_manifest, eval_data)
    if drift:
        for msg in drift:
            print(f"{'WARNING' if args.allow_version_drift else 'ERROR'} [pack_version]: {msg}", file=sys.stderr)
        if not args.allow_version_drift:
            sys.exit(2)

    categories: dict[str, int] = {}
    for q in questions:
        cat = q.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1

    pack_version = str(pack_manifest.get("version") or "unknown")
    integrity = pack_manifest.get("integrity") or {}
    pack_digest = integrity.get("pack_digest") if isinstance(integrity, dict) else None

    if args.dry_run:
        print("\n=== DRY RUN — validation only, no API calls ===")
        print(f"Pack:         {pack_path} (v{pack_version})")
        print(f"Mode:         {args.mode}")
        print(f"Eval:         {eval_path}")
        print(f"Questions:    {len(questions)}")
        for cat, count in sorted(categories.items()):
            print(f"  {cat}: {count}")
        ek_count = sum(1 for q in questions if q.get("ek_dependent"))
        print(f"EK-dependent: {ek_count}")
        if args.mode in ("rag", "compare") and not args.mcp_url:
            ret = LocalBM25Retriever(pack_path)
            sample_hits = ret.retrieve(questions[0]["question"], top_k=args.top_k)
            print(f"Local BM25 index: {ret.doc_count} atoms; sample top hit for {questions[0]['id']}: "
                  f"{sample_hits[0]['source_file'] if sample_hits else 'none'}")
            ret.close()
        print("\nValidation passed.")
        return

    if args.mode == "retrieval-only":
        ret = LocalBM25Retriever(pack_path)
        try:
            rows = []
            in_scope_total = 0
            in_scope_hits = 0
            for q in questions:
                hits = ret.retrieve(q["question"], top_k=args.top_k)
                is_ref = q.get("category") in ("refusal", "out-of-scope")
                if not is_ref:
                    in_scope_total += 1
                    if hits:
                        in_scope_hits += 1
                rows.append({
                    "id": q["id"],
                    "category": q.get("category", ""),
                    "ek_dependent": bool(q.get("ek_dependent")),
                    "hits_count": len(hits),
                    "top_hit": hits[0]["source_file"] if hits else None,
                    "top_score": hits[0]["score"] if hits else 0.0,
                    "retrieved_files": [h["source_file"] for h in hits],
                })
            output = {
                "run_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "pack": str(pack_path),
                "pack_slug": pack_manifest.get("slug", pack_path.name),
                "pack_version": pack_version,
                "pack_digest": pack_digest,
                "mode": "retrieval-only (local SQLite FTS5 BM25, zero LLM calls)",
                "eval_set": str(eval_path),
                "eval_set_version": eval_data.get("version", "1.0"),
                "indexed_atoms": ret.doc_count,
                "questions_total": len(questions),
                "in_scope_questions": in_scope_total,
                "in_scope_retrieval_coverage": round(in_scope_hits / in_scope_total, 3) if in_scope_total else 0.0,
                "note": (
                    "Deterministic zero-key BM25 retrieval coverage only — not an LLM correctness "
                    "or with-vs-without accuracy claim. Run --mode compare with OPENROUTER_API_KEY "
                    "for full LLM with-vs-without delta."
                ),
                "details": rows,
            }
        finally:
            ret.close()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(output, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        print(
            f"Retrieval-only baseline -> {output_path} "
            f"(in-scope coverage: {in_scope_hits}/{in_scope_total}, indexed atoms: {output['indexed_atoms']})"
        )
        return

    api_key = load_api_key()
    if not api_key:
        print("Error: OPENROUTER_API_KEY not found. Set it in the environment or ~/.openclaw/.env", file=sys.stderr)
        sys.exit(1)

    model = args.model or DEFAULT_MODEL
    judge_model = args.judge_model or DEFAULT_JUDGE_MODEL

    if args.mode == "compare":
        with_mode = "rag" if args.compare_with == "rag" else "full"
        base_results, base_tokens = _execute_pass(
            mode="without-pack", questions=questions, pack_path=pack_path, pack_manifest=pack_manifest,
            model=model, judge_model=judge_model, api_key=api_key, delay=args.delay,
            top_k=args.top_k, mcp_url=args.mcp_url, mcp_token=args.mcp_token,
        )
        with_results, with_tokens = _execute_pass(
            mode=with_mode, questions=questions, pack_path=pack_path, pack_manifest=pack_manifest,
            model=model, judge_model=judge_model, api_key=api_key, delay=args.delay,
            top_k=args.top_k, mcp_url=args.mcp_url, mcp_token=args.mcp_token,
        )
        base_scores = _aggregate(base_results)
        with_scores = _aggregate(with_results)

        # Tag questions where blind baseline missed (<0.6) and pack-backed improved (>=0.8)
        verified_gaps = [
            w["id"]
            for b, w in zip(base_results, with_results)
            if b["correctness"] < 0.6 and w["correctness"] >= 0.8 and w["category"] not in ("refusal", "out-of-scope")
        ]
        output = {
            "run_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "pack": str(pack_path),
            "pack_slug": pack_manifest.get("slug", pack_path.name),
            "pack_version": pack_version,
            "pack_digest": pack_digest,
            "mode": f"compare (without-pack vs {with_mode})",
            "eval_set": str(eval_path),
            "eval_set_version": eval_data.get("version", "1.0"),
            "model": model,
            "judge_model": judge_model,
            "questions_total": len(questions),
            "without_pack_scores": base_scores,
            "with_pack_scores": with_scores,
            "delta": {
                "correctness": round(with_scores["correctness"] - base_scores["correctness"], 3),
                "groundedness": round(with_scores["groundedness"] - base_scores["groundedness"], 3),
                "hallucination_rate": round(with_scores["hallucination_rate"] - base_scores["hallucination_rate"], 3),
            },
            "knowledge_gap_verified": verified_gaps,
            "tokens": {
                "without_pack": base_tokens,
                "with_pack": with_tokens,
            },
            "without_pack_details": base_results,
            "with_pack_details": with_results,
        }
    else:
        results, tokens = _execute_pass(
            mode=args.mode, questions=questions, pack_path=pack_path, pack_manifest=pack_manifest,
            model=model, judge_model=judge_model, api_key=api_key, delay=args.delay,
            top_k=args.top_k, mcp_url=args.mcp_url, mcp_token=args.mcp_token,
        )
        scores = _aggregate(results)
        output = {
            "run_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "pack": str(pack_path),
            "pack_slug": pack_manifest.get("slug", pack_path.name),
            "pack_version": pack_version,
            "pack_digest": pack_digest,
            "mode": args.mode,
            "eval_set": str(eval_path),
            "eval_set_version": eval_data.get("version", "1.0"),
            "model": model,
            "judge_model": judge_model,
            "questions_total": len(questions),
            "scores": scores,
            "tokens": tokens,
            "details": results,
        }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(output, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"\nResults -> {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="ExpertPack Eval Runner — measure pack quality (full, RAG, without-pack, or compare)"
    )
    parser.add_argument("--pack", required=True, help="Path to pack directory (e.g. packs/blender-3d)")
    parser.add_argument("--eval", required=True, help="Path to eval YAML file")
    parser.add_argument(
        "--mode", choices=["full", "rag", "without-pack", "compare", "retrieval-only"], default="full",
        help="Evaluation mode (default: full; 'compare' for with-vs-without delta; 'retrieval-only' for zero-key BM25 coverage)",
    )
    parser.add_argument(
        "--compare-with", choices=["rag", "full"], default="rag",
        help="With-pack arm when --mode compare is used (default: rag)",
    )
    parser.add_argument("--top-k", type=int, default=5, help="Top-K atoms retrieved per question in rag mode (default: 5)")
    parser.add_argument("--mcp-url", default=None, help="Optional ep-mcp HTTP /search URL (otherwise uses local SQLite FTS5 BM25)")
    parser.add_argument("--mcp-token", default="", help="Optional Bearer token for --mcp-url")
    parser.add_argument("--model", default=None, help=f"Model for answering questions (default: {DEFAULT_MODEL})")
    parser.add_argument("--judge-model", default=None, help=f"Model for LLM-as-judge scoring (default: {DEFAULT_JUDGE_MODEL})")
    parser.add_argument("--output", default=None, help="Output YAML path")
    parser.add_argument("--delay", type=float, default=1.0, help="Seconds to wait between questions (default: 1.0)")
    parser.add_argument("--allow-version-drift", action="store_true", help="Warn instead of failing on pack_version mismatch")
    parser.add_argument("--dry-run", action="store_true", help="Validate eval YAML, version pinning, and retrieval without API calls")

    args = parser.parse_args()
    run_eval(args)


if __name__ == "__main__":
    main()
