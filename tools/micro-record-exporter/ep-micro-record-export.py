#!/usr/bin/env python3
"""
ExpertPack Micro-Record Exporter

Generates canonical micro-records from pack content files. Default output is
full JSONL micro-records; --compact emits Agent Knowledge Schema (AKS) JSONL
(schemas/registry/agent-knowledge.schema.yaml). Reads frontmatter + _graph.yaml;
optionally uses an LLM to generate canonical_statement for files that don't have one.

Usage:
    # Export all files in a pack to micro-records:
    python tools/micro-record-exporter/ep-micro-record-export.py \
        --pack ExpertPacks/ezt-designer \
        --output exports/ezt-designer-micro-records.jsonl

    # Export a single file:
    python tools/micro-record-exporter/ep-micro-record-export.py \
        --pack ExpertPacks/ezt-designer \
        --file concepts/con-scheduling-algorithm.md \
        --output exports/single.json

    # Generate canonical_statement via LLM (requires OPENROUTER_API_KEY):
    python tools/micro-record-exporter/ep-micro-record-export.py \
        --pack ExpertPacks/ezt-designer \
        --output exports/ezt-designer-micro-records.jsonl \
        --generate-statements

    # Compact AKS export for token-efficient retrieval pipelines:
    python tools/micro-record-exporter/ep-micro-record-export.py \
        --pack ExpertPacks/ezt-designer \
        --compact \
        --output exports/ezt-designer.aks.jsonl

    # Strict CI mode — fail if exportable content files are skipped:
    python tools/micro-record-exporter/ep-micro-record-export.py \
        --pack ExpertPacks/ezt-designer \
        --compact \
        --strict \
        --report-json exports/ezt-designer.aks-report.json \
        --output exports/ezt-designer.aks.jsonl

    # Dry run — show what would be exported without writing:
    python tools/micro-record-exporter/ep-micro-record-export.py \
        --pack ExpertPacks/ezt-designer \
        --dry-run

Output:
    JSONL file (one micro-record per line) or single JSON for --file.
    Default records are full micro-records. --compact records conform to
    schemas/registry/agent-knowledge.schema.yaml.

Notes:
    - canonical_statement is the one field that can't be derived from frontmatter alone.
      Without --generate-statements, it's set to the first non-empty paragraph of the file.
    - Files without frontmatter `id` are skipped with a warning (run ep-validate --provenance first).
    - _graph.yaml edges are used to populate the `related` field.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("Error: pyyaml required. pip install pyyaml")
    sys.exit(1)

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_STATEMENT_MODEL = "openrouter/openai/gpt-4o-mini"

# Files to skip
SKIP_FILES = {"_graph.yaml", "_index.json", "_access.json", "manifest.yaml"}
SKIP_PREFIXES = {".obsidian", ".git"}


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from a markdown file.

    Returns (frontmatter_dict, body_text).
    """
    if not text.startswith("---"):
        return {}, text

    end = text.find("\n---", 3)
    if end == -1:
        return {}, text

    fm_text = text[3:end].strip()
    body = text[end + 4:].strip()

    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        fm = {}

    return fm, body


def clean_md(text: str) -> str:
    """Strip common markdown inline formatting."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    text = re.sub(r"\[\[(.+?)\]\]", r"\1", text)
    text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
    return text.strip()


def first_paragraph(body: str) -> str:
    """Extract the best canonical statement from markdown body.

    Priority:
    1. Lead summary blockquote (> **Lead summary:** ...)
    2. First non-empty, non-heading prose paragraph
    """
    lines = body.splitlines()

    # Pass 1: look for lead summary blockquote
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(">") and "lead summary" in stripped.lower():
            text = re.sub(r"^>\s*", "", stripped)
            text = re.sub(r"\*\*Lead [Ss]ummary:\*\*\s*", "", text)
            text = re.sub(r"Lead [Ss]ummary:\s*", "", text)
            text = clean_md(text)
            if len(text) > 20:
                return text[:400]

    # Pass 2: first non-empty prose paragraph
    paragraph_lines = []
    in_para = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_para:
                break
            continue
        # Skip headings, horizontal rules, code fences, HTML comments, blockquotes, tables
        if stripped.startswith(("#", "---", "```", "|", ">", "<!--", "!")):
            if in_para:
                break
            continue
        if stripped.endswith("-->"):
            if in_para:
                break
            continue
        in_para = True
        paragraph_lines.append(stripped)

    return clean_md(" ".join(paragraph_lines))[:400]


def compute_hash(body: str) -> str:
    """Compute SHA-256 of file body."""
    return "sha256:" + hashlib.sha256(body.encode("utf-8")).hexdigest()


def is_exportable_markdown(pack_path: Path, file_path: Path) -> bool:
    """Return True for content Markdown files the exporter should consider."""
    try:
        rel_path = file_path.relative_to(pack_path)
    except ValueError:
        return False
    if file_path.suffix != ".md":
        return False
    if file_path.name.startswith("_") or file_path.name in SKIP_FILES:
        return False
    return not any(part.startswith(".") for part in rel_path.parts[:-1])


# ---------------------------------------------------------------------------
# Graph loading
# ---------------------------------------------------------------------------

def load_graph_edges(pack_path: Path) -> dict[str, list[dict]]:
    """Load _graph.yaml and return a dict of node_id → list of {id, kind} dicts."""
    graph_path = pack_path / "_graph.yaml"
    if not graph_path.exists():
        return {}

    try:
        raw = yaml.safe_load(graph_path.read_text(encoding="utf-8"))
    except (yaml.YAMLError, OSError):
        return {}

    if not isinstance(raw, dict):
        return {}

    # Build node_id → file mapping
    nodes = raw.get("nodes", [])
    node_file_map = {}
    for n in nodes:
        nid = n.get("id")
        fp = n.get("file")
        if nid and fp:
            node_file_map[nid] = fp

    # Build file → related list
    edges_by_file: dict[str, list[dict]] = {}
    for edge in raw.get("edges", []):
        src = edge.get("source")
        tgt = edge.get("target")
        kind = edge.get("kind", "wikilink")
        if not src or not tgt:
            continue

        src_file = node_file_map.get(src)
        if not src_file:
            continue

        if src_file not in edges_by_file:
            edges_by_file[src_file] = []

        edges_by_file[src_file].append({"id": tgt, "kind": kind})

    return edges_by_file


# ---------------------------------------------------------------------------
# LLM canonical statement generation
# ---------------------------------------------------------------------------

def load_api_key() -> str:
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if key:
        return key
    for env_path in ["/root/.openclaw/.env", os.path.expanduser("~/.openclaw/.env"), ".env"]:
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("OPENROUTER_API_KEY="):
                        key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if key:
                            return key
    return ""


STATEMENT_PROMPT = """\
Read the following ExpertPack content file and write a single canonical statement — \
the most important assertable fact from this file in one sentence (max 400 characters). \
It should be self-contained: readable without the source file. No hedging, no "This document describes".

FILE: {file_path}
TYPE: {content_type}

CONTENT:
{content}

Return ONLY the canonical statement. No preamble, no quotes."""


def generate_statement(
    file_path: str,
    content_type: str,
    body: str,
    model: str,
    api_key: str,
) -> str:
    """Use LLM to generate a canonical statement for a file."""
    prompt = STATEMENT_PROMPT.format(
        file_path=file_path,
        content_type=content_type,
        content=body[:3000],
    )
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
    }
    try:
        resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()[:400]
    except Exception as e:
        return ""  # Fall back to first paragraph


# ---------------------------------------------------------------------------
# Record building
# ---------------------------------------------------------------------------

def build_micro_record(
    pack_path: Path,
    file_path: Path,
    pack_slug: str,
    edges_by_file: dict[str, list[dict]],
    generate_statements: bool = False,
    api_key: str = "",
    model: str = DEFAULT_STATEMENT_MODEL,
    delay: float = 0.3,
    compact: bool = False,
) -> dict | None:
    """Build a micro-record for a single file. Returns None if file should be skipped."""
    rel_path = file_path.relative_to(pack_path)
    rel_str = str(rel_path)

    if not is_exportable_markdown(pack_path, file_path):
        return None

    try:
        raw = file_path.read_text(encoding="utf-8")
    except OSError:
        return None

    fm, body = parse_frontmatter(raw)

    # Must have an id in frontmatter
    record_id = fm.get("id")
    if not record_id:
        return None

    # Content type
    content_type = fm.get("type", "reference")

    # Label — frontmatter title or H1
    label = fm.get("title", "")
    if not label:
        for line in body.splitlines():
            if line.startswith("# "):
                label = line[2:].strip()
                break
    if not label:
        label = file_path.stem

    # Canonical statement
    canonical_statement = ""
    if generate_statements and api_key and REQUESTS_AVAILABLE:
        canonical_statement = generate_statement(rel_str, content_type, body, model, api_key)
        time.sleep(delay)
    if not canonical_statement:
        canonical_statement = first_paragraph(body)

    if not canonical_statement:
        canonical_statement = f"{label} — {content_type} in {pack_slug}."

    # Tags
    tags = fm.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]

    # Provenance — first-class fields in the record, with a nested block kept
    # for JSON-LD/registry compatibility.
    content_hash = str(fm.get("content_hash") or compute_hash(body))
    verified_at = str(fm["verified_at"]) if "verified_at" in fm else None
    verified_by = str(fm["verified_by"]) if "verified_by" in fm else None
    source = str(fm["source"]) if "source" in fm else None
    recorded_at = str(fm.get("recorded_at") or fm.get("created")) if (fm.get("recorded_at") or fm.get("created")) else None
    valid_from = str(fm["valid_from"]) if "valid_from" in fm else None

    provenance: dict[str, Any] = {
        "id": record_id,
        "source_span_uri": f"{pack_slug}/{rel_str}",
        "content_hash": content_hash,
    }
    if verified_at:
        provenance["verified_at"] = verified_at
    if verified_by:
        provenance["verified_by"] = verified_by
    if source:
        provenance["source"] = source
    if recorded_at:
        provenance["recorded_at"] = recorded_at
    if valid_from:
        provenance["valid_from"] = valid_from

    # Related edges from _graph.yaml plus explicit frontmatter edges.
    related = edges_by_file.get(rel_str, [])
    fm_related = fm.get("related", [])
    if isinstance(fm_related, str):
        fm_related = [fm_related]
    related.extend({"id": str(r), "kind": "related"} for r in fm_related if str(r).strip())

    requires = fm.get("requires", [])
    if isinstance(requires, str):
        requires = [requires]
    requires = [str(r) for r in requires if str(r).strip()]

    supersedes = fm.get("supersedes", [])
    if isinstance(supersedes, str):
        supersedes = [supersedes]
    supersedes = [str(s) for s in supersedes if str(s).strip()]

    # Lifecycle
    lifecycle: dict[str, Any] = {"status": fm.get("lifecycle_status", "active")}
    superseded_by = fm.get("superseded_by")
    if superseded_by:
        lifecycle["superseded_by"] = str(superseded_by)
        lifecycle["status"] = "superseded"
    valid_until = fm.get("expires_at")
    if valid_until:
        lifecycle["valid_until"] = str(valid_until)

    if compact:
        record = {
            "schema": "expertpack.agent_knowledge.v1",
            "id": record_id,
            "canonical_statement": canonical_statement,
            "title": label,
            "type": content_type,
            "pack": pack_slug,
            "canonical_path": rel_str,
            "source_span_uri": f"{pack_slug}/{rel_str}",
            "content_hash": content_hash,
            "source_checksum": content_hash,
        }
        if verified_at:
            record["verified_at"] = verified_at
        if verified_by:
            record["verified_by"] = verified_by
        if recorded_at:
            record["recorded_at"] = recorded_at
        if valid_from:
            record["valid_from"] = valid_from
        if tags:
            record["tags"] = tags
        if requires:
            record["requires"] = requires
        if related:
            record["related"] = related
        if supersedes:
            record["supersedes"] = supersedes
        return record

    record = {
        "@context": "https://expertpack.ai/schema/1.0/context.jsonld",
        "schema": "expertpack.micro_record.v1",
        "id": record_id,
        "source_span_uri": f"{pack_slug}/{rel_str}",
        "label": label,
        "canonical_statement": canonical_statement,
        "type": content_type,
        "pack": pack_slug,
        "content_hash": content_hash,
    }

    if verified_at:
        record["verified_at"] = verified_at
    if recorded_at:
        record["recorded_at"] = recorded_at
    if valid_from:
        record["valid_from"] = valid_from
    if tags:
        record["tags"] = tags
    record["provenance"] = provenance
    if related:
        record["related"] = related
    if requires:
        record["requires"] = requires
    if supersedes:
        record["supersedes"] = supersedes
    if lifecycle["status"] != "active" or len(lifecycle) > 1:
        record["lifecycle"] = lifecycle

    return record


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(args):
    pack_path = Path(args.pack)
    if not pack_path.exists():
        print(f"Error: pack path not found: {pack_path}")
        sys.exit(1)

    # Load pack slug from manifest
    manifest_path = pack_path / "manifest.yaml"
    pack_slug = args.slug
    if not pack_slug and manifest_path.exists():
        try:
            mf = yaml.safe_load(manifest_path.read_text())
            pack_slug = mf.get("slug", pack_path.name)
        except Exception:
            pack_slug = pack_path.name
    if not pack_slug:
        pack_slug = pack_path.name

    generate_statements = args.generate_statements
    api_key = ""
    model = args.model or DEFAULT_STATEMENT_MODEL

    if generate_statements:
        if not REQUESTS_AVAILABLE:
            print("Error: --generate-statements requires requests. pip install requests")
            sys.exit(1)
        api_key = load_api_key()
        if not api_key:
            print("Error: --generate-statements requires OPENROUTER_API_KEY")
            sys.exit(1)

    # Load graph edges
    edges_by_file = load_graph_edges(pack_path)

    # Collect files to process
    if args.file:
        files = [pack_path / args.file]
    else:
        files = sorted(pack_path.rglob("*.md"))

    if args.dry_run:
        print(f"Pack:  {pack_path}")
        print(f"Slug:  {pack_slug}")
        print(f"Files: {len(files)} markdown files")
        print(f"Graph: {sum(len(v) for v in edges_by_file.values())} edges loaded")
        skipped = 0
        processable = 0
        missing_id = 0
        for fp in files:
            try:
                raw = fp.read_text(encoding="utf-8")
                fm, _ = parse_frontmatter(raw)
                if fm.get("id"):
                    processable += 1
                else:
                    missing_id += 1
            except Exception:
                skipped += 1
        print(f"Would export: {processable} records")
        print(f"Would skip (no id): {missing_id} files")
        print(f"Would skip (error): {skipped} files")
        print("\nDry run complete.")
        return

    # Process files
    records = []
    skipped_no_id = []
    errors = []

    for fp in files:
        record = build_micro_record(
            pack_path=pack_path,
            file_path=fp,
            pack_slug=pack_slug,
            edges_by_file=edges_by_file,
            generate_statements=generate_statements,
            api_key=api_key,
            model=model,
            delay=args.delay,
            compact=args.compact,
        )
        if record is None:
            rel = str(fp.relative_to(pack_path))
            # Check if it's skipped due to missing id
            try:
                raw = fp.read_text(encoding="utf-8")
                fm, _ = parse_frontmatter(raw)
                if is_exportable_markdown(pack_path, fp) and not fm.get("id"):
                    skipped_no_id.append(rel)
            except Exception:
                pass
        else:
            records.append(record)

    report = {
        "pack": pack_slug,
        "mode": "aks" if args.compact else "micro_record",
        "records": len(records),
        "skipped_no_id": skipped_no_id,
        "skipped_no_id_count": len(skipped_no_id),
    }

    print(f"Exported: {len(records)} records")
    if skipped_no_id:
        print(f"Skipped (no frontmatter id): {len(skipped_no_id)}")
        if args.verbose:
            for f in skipped_no_id[:20]:
                print(f"  {f}")

    if args.report_json:
        report_path = Path(args.report_json)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))
        print(f"Report → {report_path}")

    if args.strict and skipped_no_id:
        print("Error: --strict set and one or more exportable files are missing frontmatter id.")
        sys.exit(2)

    if not records:
        print("No records to write.")
        return

    # Write output
    if args.file:
        # Single file → pretty JSON
        output_path = Path(args.output) if args.output else Path(
            pack_path / f"_micro-{Path(args.file).stem}.json"
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(records[0], indent=2, ensure_ascii=False))
        print(f"Written → {output_path}")
    else:
        # Multi-file → JSONL
        output_path = Path(args.output) if args.output else Path(
            f"exports/{pack_slug}-micro-records.jsonl"
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        print(f"Written → {output_path}  ({len(records)} records, {output_path.stat().st_size:,} bytes)")


def main():
    parser = argparse.ArgumentParser(
        description="ExpertPack Micro-Record Exporter — generate canonical micro-records from pack files"
    )
    parser.add_argument("--pack", required=True,
                        help="Path to pack directory")
    parser.add_argument("--output", default=None,
                        help="Output path (.jsonl for full pack, .json for single file)")
    parser.add_argument("--file", default=None,
                        help="Export a single file (relative to pack root)")
    parser.add_argument("--slug", default=None,
                        help="Override pack slug (default: read from manifest.yaml)")
    parser.add_argument("--generate-statements", action="store_true",
                        help="Use LLM to generate canonical_statement (requires OPENROUTER_API_KEY)")
    parser.add_argument("--model", default=None,
                        help=f"LLM model for statement generation (default: {DEFAULT_STATEMENT_MODEL})")
    parser.add_argument("--delay", type=float, default=0.3,
                        help="Seconds between LLM calls when --generate-statements (default: 0.3)")
    parser.add_argument("--compact", action="store_true",
                        help="Emit lean JSONL with first-class provenance fields for token-efficient pipelines")
    parser.add_argument("--strict", action="store_true",
                        help="Exit nonzero if exportable content files are skipped (for CI/export readiness gates)")
    parser.add_argument("--report-json", default=None,
                        help="Write machine-readable export report JSON")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be exported without writing files")
    parser.add_argument("--verbose", action="store_true",
                        help="Show skipped file details")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
