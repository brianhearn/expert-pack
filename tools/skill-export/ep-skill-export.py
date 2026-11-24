#!/usr/bin/env python3
"""Export an ExpertPack as a portable, self-contained Agent Skill folder (SKILL.md).

Produces a plain folder compatible with the strict shared Agent Skills profile
(Claude Code, Cursor, Gemini in Chrome, Google Workspace, Cloudflare Agents SDK):

    <outdir>/<slug>/
      SKILL.md          (strict frontmatter, <=10,000-char body, front-loaded summary + gotchas)
      references/       (non-on_demand pack Markdown files, preserving relative structure)
      assets/           (local non-script assets, if present)
      evals/evals.json  (converted from eval/benchmark.yaml or eval/questions.yaml, if present)

Usage:
    python tools/skill-export/ep-skill-export.py packs/solar-diy ./dist/skills
    python tools/skill-export/ep-skill-export.py --validate ./dist/skills/solar-diy
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any

import yaml

# Strict shared profile limits (intersection across major Agent Skills hosts)
MAX_NAME_LEN = 64
MAX_DESCRIPTION_LEN = 1024
MAX_BODY_CHARS = 10_000
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

SKIP_DIRS = frozenset({
    ".git", ".obsidian", ".ep-mcp", "node_modules", "__pycache__", ".venv",
})
SCRIPT_EXTS = frozenset({
    ".py", ".sh", ".bash", ".zsh", ".ps1", ".bat", ".cmd", ".js", ".mjs", ".cjs", ".ts", ".rb", ".pl", ".exe",
})
ASSET_EXTS = frozenset({
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".pdf", ".csv", ".json", ".txt", ".mermaid", ".mmd",
})

_FM_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)
_MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")


def _slugify(value: str) -> str:
    s = re.sub(r"[^a-z0-9-]+", "-", value.lower()).strip("-")
    s = re.sub(r"-{2,}", "-", s)[:MAX_NAME_LEN].strip("-")
    return s or "expertpack"


def _split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    m = _FM_RE.match(text)
    if not m:
        return {}, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        fm = {}
    if not isinstance(fm, dict):
        fm = {}
    return fm, text[m.end():]


def _load_manifest(pack_dir: Path) -> dict[str, Any]:
    mf = pack_dir / "manifest.yaml"
    if not mf.is_file():
        raise FileNotFoundError(f"manifest.yaml not found in {pack_dir}")
    data = yaml.safe_load(mf.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Invalid manifest.yaml in {pack_dir}")
    return data


def _collect_pack_files(pack_dir: Path, manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], list[Path]]:
    """Collect non-on_demand Markdown files and local non-script asset files."""
    context = manifest.get("context") or {}
    on_demand_raw = context.get("on_demand") or [] if isinstance(context, dict) else []
    on_demand_prefixes = tuple(str(x).replace("\\", "/").lstrip("./") for x in on_demand_raw)

    md_entries: list[dict[str, Any]] = []
    asset_files: list[Path] = []

    for root, dirs, files in os.walk(pack_dir):
        rel_root = Path(root).relative_to(pack_dir).as_posix()
        if rel_root == ".":
            rel_root = ""
        dirs[:] = sorted(
            d for d in dirs
            if d not in SKIP_DIRS
            and not (rel_root == "eval" and d == "results")
        )
        for fname in sorted(files):
            full = Path(root) / fname
            rel = full.relative_to(pack_dir).as_posix()

            # Skip infrastructure / meta / eval / sidecars
            if fname in {"manifest.yaml", "_graph.yaml", "SKILL.md", ".DS_Store", "Thumbs.db"}:
                continue
            if rel.startswith("eval/") or rel.endswith(".chunks.yaml"):
                continue
            if any(rel == p or (p.endswith("/") and rel.startswith(p)) for p in on_demand_prefixes):
                continue

            ext = full.suffix.lower()
            if ext == ".md":
                raw = full.read_text(encoding="utf-8", errors="replace")
                fm, body = _split_frontmatter(raw)
                strat = str(fm.get("retrieval_strategy") or "standard").strip().lower()
                if strat == "on_demand":
                    continue
                if fname in {"_index.md", "source-coverage.md"}:
                    continue
                title = str(fm.get("title") or full.stem.replace("-", " ").title()).strip()
                ftype = str(fm.get("type") or "").strip().lower()
                md_entries.append({
                    "rel": rel,
                    "full": full,
                    "title": title,
                    "type": ftype,
                    "fm": fm,
                    "body": body,
                })
            elif ext in ASSET_EXTS:
                asset_files.append(full)

    return md_entries, asset_files


def _extract_gotchas(md_entries: list[dict[str, Any]], max_items: int = 8) -> list[str]:
    """Pull concise bullet gotchas from gotcha/troubleshooting/common-mistakes atoms."""
    bullets: list[str] = []
    gotcha_files = [
        e for e in md_entries
        if e["type"] == "gotcha"
        or "gotcha" in e["rel"].lower()
        or "mistake" in e["rel"].lower()
    ]
    for entry in gotcha_files:
        for line in entry["body"].splitlines():
            s = line.strip()
            if s.startswith("## ") or s.startswith("### "):
                heading = s.lstrip("#").strip()
                if heading and len(heading) <= 120 and heading.lower() not in {"related concepts", "related terms", "frequently asked"}:
                    bullets.append(f"{heading} (see `references/{entry['rel']}`)")
            elif s.startswith("- **") and len(s) <= 160:
                bullets.append(s[2:].strip())
            if len(bullets) >= max_items:
                return bullets
    return bullets


def _extract_overview_summary(md_entries: list[dict[str, Any]], manifest: dict[str, Any]) -> str:
    """Build a short front-loaded routing summary from overview.md or manifest description."""
    for entry in md_entries:
        if entry["rel"] == "overview.md":
            paras = [
                p.strip() for p in re.split(r"\n\s*\n", entry["body"])
                if p.strip() and not p.strip().startswith(("#", ">", "|", "-", "*"))
            ]
            if paras:
                summary = " ".join(paras[0].split())
                return summary[:450] + ("..." if len(summary) > 450 else "")
    desc = " ".join(str(manifest.get("description") or "").split())
    return desc[:450] + ("..." if len(desc) > 450 else "")


def _build_description(manifest: dict[str, Any]) -> str:
    parts: list[str] = []
    desc = " ".join(str(manifest.get("description") or "").split())
    if desc:
        parts.append(desc)
    else:
        parts.append(f"{manifest.get('name', manifest.get('slug', 'ExpertPack'))} domain knowledge skill.")
    ab = manifest.get("authority_boundary")
    if isinstance(ab, dict) and ab.get("in_scope"):
        in_scope = " ".join(str(ab["in_scope"]).split())
        if in_scope and in_scope.lower() not in desc.lower():
            parts.append(f"Use for: {in_scope}")
    full = " ".join(parts)
    if len(full) > MAX_DESCRIPTION_LEN:
        full = full[: MAX_DESCRIPTION_LEN - 3].rstrip() + "..."
    return full


def _build_skill_md(
    manifest: dict[str, Any],
    slug: str,
    md_entries: list[dict[str, Any]],
    asset_rels: list[str],
    default_license: str | None = None,
) -> str:
    name = _slugify(slug)
    description = _build_description(manifest)

    metadata: dict[str, str] = {
        "pack_version": str(manifest.get("version") or "1.0.0"),
        "pack_type": str(manifest.get("type") or "product"),
        "exported_by": "expertpack",
    }
    if manifest.get("schema_version"):
        metadata["schema_version"] = str(manifest["schema_version"])
    if manifest.get("canonical_url"):
        metadata["canonical_url"] = str(manifest["canonical_url"])
    if manifest.get("applies_to"):
        metadata["applies_to"] = str(manifest["applies_to"])
    integrity = manifest.get("integrity")
    if isinstance(integrity, dict) and integrity.get("pack_digest"):
        metadata["pack_digest"] = str(integrity["pack_digest"])

    fm: dict[str, Any] = {
        "name": name,
        "description": description,
    }
    lic = manifest.get("license") or default_license
    if lic:
        fm["license"] = str(lic)
    fm["metadata"] = metadata

    fm_yaml = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=10_000).strip()

    # Build body, front-loading routing summary, usage rules, authority boundary, and gotchas
    pack_name = str(manifest.get("name") or slug).strip()
    summary = _extract_overview_summary(md_entries, manifest)

    header_lines: list[str] = [
        f"# {pack_name}",
        "",
        summary,
        "",
        "## How to Use This Skill",
        "",
        "1. Read the relevant topic file(s) under `references/` before answering — do not rely on memory for domain-specific rules or numbers.",
        "2. Follow any `requires:` frontmatter links in an atom when the topic depends on another atom.",
        "3. Stay within the authority boundary below; decline out-of-scope requests explicitly.",
        "4. Caveat or verify answers drawn from `volatile/` files or atoms past their refresh date.",
        "",
    ]

    ab = manifest.get("authority_boundary")
    if isinstance(ab, dict):
        header_lines += ["## Authority & Scope", ""]
        if ab.get("in_scope"):
            header_lines.append(f"- **In scope:** {' '.join(str(ab['in_scope']).split())}")
        for item in (ab.get("out_of_scope") or [])[:5]:
            header_lines.append(f"- **Refuse:** {' '.join(str(item).split())}")
        for item in (ab.get("refuse_when") or [])[:3]:
            header_lines.append(f"- **Refuse when:** {' '.join(str(item).split())}")
        header_lines.append("")

    gotchas = _extract_gotchas(md_entries, max_items=6)
    if gotchas:
        header_lines += ["## Common Gotchas & Mistakes", ""]
        for g in gotchas:
            header_lines.append(f"- {g}")
        header_lines.append("")

    header_lines += ["## References", ""]
    body_prefix = "\n".join(header_lines)

    footer_lines: list[str] = []
    if asset_rels:
        footer_lines += ["", "## Assets", ""]
        for ar in asset_rels[:20]:
            footer_lines.append(f"- [{ar}](assets/{ar})")
    footer = ("\n".join(footer_lines) + "\n") if footer_lines else ""

    # Budget remaining characters strictly under MAX_BODY_CHARS (10,000)
    max_ref_budget = MAX_BODY_CHARS - len(body_prefix) - len(footer) - 120
    ref_lines: list[str] = []
    used = 0
    omitted = 0

    # Group by top-level directory for clean scannability while staying under budget
    for entry in md_entries:
        title = entry["title"].replace("\n", " ").replace("]", "")
        typ = f" ({entry['type']})" if entry["type"] else ""
        line = f"- [{title}](references/{entry['rel']}){typ}\n"
        if used + len(line) > max_ref_budget:
            omitted += 1
            continue
        ref_lines.append(line)
        used += len(line)

    if omitted > 0:
        ref_lines.append(
            f"\n*({omitted} additional reference files are included under `references/` — list `references/` to browse all files.)*\n"
        )

    body = body_prefix + "".join(ref_lines) + footer
    if len(body) > MAX_BODY_CHARS:
        body = body[: MAX_BODY_CHARS - 20].rstrip() + "\n"

    return f"---\n{fm_yaml}\n---\n\n{body}"


def _export_evals(pack_dir: Path, out_dir: Path, pack_version: str) -> bool:
    """Convert pack eval YAML (if present) into evals/evals.json."""
    candidates = [
        pack_dir / "eval" / "benchmark.yaml",
        pack_dir / "eval" / "questions.yaml",
    ]
    eval_src = next((c for c in candidates if c.is_file()), None)
    if eval_src is None:
        return False
    try:
        data = yaml.safe_load(eval_src.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        return False
    if not isinstance(data, dict):
        return False
    questions = data.get("questions") or data.get("cases") or []
    if not isinstance(questions, list) or not questions:
        return False

    payload = {
        "pack_version": pack_version,
        "source": eval_src.relative_to(pack_dir).as_posix(),
        "question_count": len(questions),
        "questions": questions,
    }
    evals_dir = out_dir / "evals"
    evals_dir.mkdir(parents=True, exist_ok=True)
    (evals_dir / "evals.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return True


def export_skill(
    pack_dir: str | Path,
    out_root: str | Path,
    *,
    exact_dir: bool = False,
    include_scripts: bool = False,
    default_license: str | None = None,
    force: bool = False,
) -> Path:
    """Export an ExpertPack directory into a validated plain Agent Skill folder."""
    pack_path = Path(pack_dir).resolve()
    manifest = _load_manifest(pack_path)
    slug = _slugify(str(manifest.get("slug") or pack_path.name))

    out_dir = Path(out_root).resolve() if exact_dir else (Path(out_root).resolve() / slug)
    if out_dir.exists():
        if not force:
            raise FileExistsError(f"Output directory already exists: {out_dir} (pass --force to overwrite)")
        shutil.rmtree(out_dir)

    md_entries, asset_files = _collect_pack_files(pack_path, manifest)

    refs_dir = out_dir / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)
    for entry in md_entries:
        dest = refs_dir / entry["rel"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(entry["full"], dest)

    asset_rels: list[str] = []
    if asset_files:
        assets_dir = out_dir / "assets"
        for src in asset_files:
            if not include_scripts and src.suffix.lower() in SCRIPT_EXTS:
                continue
            rel = src.relative_to(pack_path).as_posix()
            dest = assets_dir / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            asset_rels.append(rel)

    skill_md = _build_skill_md(
        manifest, slug, md_entries, asset_rels, default_license=default_license,
    )
    (out_dir / "SKILL.md").write_text(skill_md, encoding="utf-8", newline="\n")

    _export_evals(pack_path, out_dir, str(manifest.get("version") or "1.0.0"))

    errors = validate_skill_folder(
        out_dir,
        check_folder_name=not exact_dir,
        forbid_scripts=not include_scripts,
    )
    if errors:
        raise ValueError(
            "Exported SKILL.md failed strict profile validation:\n  - " + "\n  - ".join(errors)
        )
    return out_dir


def validate_skill_folder(
    skill_dir: str | Path,
    *,
    check_folder_name: bool = True,
    forbid_scripts: bool = True,
) -> list[str]:
    """Validate a SKILL.md folder against the strict shared Agent Skills profile.

    Returns a list of error strings (empty list = valid).
    """
    errors: list[str] = []
    root = Path(skill_dir).resolve()
    skill_path = root / "SKILL.md"
    if not skill_path.is_file():
        return [f"Missing SKILL.md in {root}"]

    raw = skill_path.read_text(encoding="utf-8")

    # 1. Nothing above opening frontmatter ---
    if not (raw.startswith("---\n") or raw.startswith("---\r\n")):
        errors.append("SKILL.md must start immediately with '---' frontmatter (no content or comments above)")
        return errors

    m = _FM_RE.match(raw)
    if not m:
        errors.append("SKILL.md frontmatter is missing a closing '---' delimiter")
        return errors

    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as exc:
        return [f"SKILL.md frontmatter is invalid YAML: {exc}"]

    if not isinstance(fm, dict):
        return ["SKILL.md frontmatter must be a YAML mapping"]

    body = raw[m.end():].lstrip("\r\n")

    # 2. name checks
    name = fm.get("name")
    if not isinstance(name, str) or not name:
        errors.append("Frontmatter 'name' is required and must be a non-empty string")
    else:
        if len(name) > MAX_NAME_LEN:
            errors.append(f"Frontmatter 'name' exceeds {MAX_NAME_LEN} chars ({len(name)})")
        if not NAME_RE.match(name):
            errors.append(f"Frontmatter 'name' must be lowercase kebab-case (got {name!r})")
        if check_folder_name and name != root.name:
            errors.append(f"Frontmatter 'name' ({name!r}) must match folder name ({root.name!r})")

    # 3. description checks
    desc = fm.get("description")
    if not isinstance(desc, str) or not desc.strip():
        errors.append("Frontmatter 'description' is required and must be a non-empty string")
    elif len(desc) > MAX_DESCRIPTION_LEN:
        errors.append(f"Frontmatter 'description' exceeds {MAX_DESCRIPTION_LEN} chars ({len(desc)})")

    # 4. metadata must be flat string -> string
    meta = fm.get("metadata")
    if meta is not None:
        if not isinstance(meta, dict):
            errors.append("Frontmatter 'metadata' must be a string->string mapping")
        else:
            for k, v in meta.items():
                if not isinstance(k, str) or not isinstance(v, str):
                    errors.append(
                        f"Frontmatter metadata[{k!r}] must be a string (got {type(v).__name__})"
                    )

    # 5. body length <= 10,000 chars
    if len(body) > MAX_BODY_CHARS:
        errors.append(f"SKILL.md body exceeds {MAX_BODY_CHARS} chars ({len(body)})")

    # 6. Check relative markdown links in SKILL.md resolve locally
    for match in _MD_LINK_RE.finditer(body):
        target = match.group(1).strip()
        if target.startswith(("http://", "https://", "mailto:", "skill://", "ep://")):
            continue
        if not (root / target).exists():
            errors.append(f"Broken relative link in SKILL.md: {target}")

    # 7. Script-free check
    if forbid_scripts:
        for fp in root.rglob("*"):
            if fp.is_file() and fp.suffix.lower() in SCRIPT_EXTS:
                rel = fp.relative_to(root).as_posix()
                errors.append(f"Executable script found in script-free skill export: {rel}")

    return errors


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    parser = argparse.ArgumentParser(
        description="Export an ExpertPack as a portable Agent Skill folder (SKILL.md) or validate an existing folder."
    )
    parser.add_argument("pack_or_skill", help="Path to ExpertPack directory (or Skill folder with --validate)")
    parser.add_argument("outdir", nargs="?", help="Output directory for the exported skill folder")
    parser.add_argument("--validate", action="store_true", help="Validate an existing SKILL.md folder instead of exporting")
    parser.add_argument("--exact-dir", action="store_true", help="Write directly into outdir instead of outdir/<slug>")
    parser.add_argument("--include-scripts", action="store_true", help="Allow copying executable scripts into assets/")
    parser.add_argument("--license", dest="default_license", default=None, help="Fallback SPDX license if manifest lacks one")
    parser.add_argument("--force", action="store_true", help="Overwrite existing output directory")
    args = parser.parse_args()

    if args.validate:
        errors = validate_skill_folder(args.pack_or_skill, forbid_scripts=not args.include_scripts)
        if errors:
            print(f"FAIL: {args.pack_or_skill}", file=sys.stderr)
            for e in errors:
                print(f"  - {e}", file=sys.stderr)
            return 1
        print(f"OK: {args.pack_or_skill} passes strict Agent Skills profile")
        return 0

    if not args.outdir:
        parser.error("outdir is required unless --validate is set")

    try:
        out_dir = export_skill(
            args.pack_or_skill,
            args.outdir,
            exact_dir=args.exact_dir,
            include_scripts=args.include_scripts,
            default_license=args.default_license,
            force=args.force,
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    ref_count = sum(1 for _ in (out_dir / "references").rglob("*.md"))
    skill_size = len((out_dir / "SKILL.md").read_text(encoding="utf-8"))
    print(f"Exported skill -> {out_dir}")
    print(f"  SKILL.md:   {skill_size:,} chars (strict profile PASS)")
    print(f"  references: {ref_count} files")
    if (out_dir / "evals" / "evals.json").is_file():
        print("  evals:      evals/evals.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
