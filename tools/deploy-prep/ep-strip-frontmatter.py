#!/usr/bin/env python3
"""
ep-strip-frontmatter.py — ExpertPack Deploy Prep Tool

Copies a pack directory to an output directory, stripping YAML frontmatter
(---...--- blocks) from all .md files. Non-.md files are copied as-is.
Source files are never modified.

Usage:
    python3 ep-strip-frontmatter.py --src <pack-dir> --out <output-dir> [--force]

Options:
    --src   Source pack directory (required)
    --out   Output directory for deploy-ready files (required)
    --force Overwrite output directory if it exists (default: warn and overwrite)
    --dry-run  Report what would be stripped without writing anything

Purpose:
    Provenance frontmatter (id, content_hash, verified_at, verified_by) is
    management metadata — it serves tooling and freshness tracking, not
    retrieval. Embedding it dilutes semantic similarity scores. This tool
    produces a clean copy for indexing/deployment while the source retains
    full provenance.

Part of the ExpertPack toolchain. See ExpertPack/tools/ for related tools.
"""

import argparse
import re
import shutil
import sys
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\s*\n.*?\n---\s*\n?", re.DOTALL)


def strip_frontmatter(text: str) -> tuple[str, bool]:
    """Strip YAML frontmatter from markdown text. Returns (stripped_text, was_stripped)."""
    match = FRONTMATTER_RE.match(text)
    if match:
        stripped = text[match.end():]
        # Remove leading blank lines left after stripping
        stripped = stripped.lstrip("\n")
        return stripped, True
    return text, False


def process_pack(src: Path, out: Path, dry_run: bool = False) -> dict:
    stats = {"md_total": 0, "md_stripped": 0, "md_no_frontmatter": 0, "other": 0, "errors": 0}

    for src_file in sorted(src.rglob("*")):
        if src_file.is_dir():
            continue

        rel = src_file.relative_to(src)
        dst_file = out / rel

        if not dry_run:
            dst_file.parent.mkdir(parents=True, exist_ok=True)

        if src_file.suffix.lower() == ".md":
            stats["md_total"] += 1
            try:
                text = src_file.read_text(encoding="utf-8")
                stripped, was_stripped = strip_frontmatter(text)
                if was_stripped:
                    stats["md_stripped"] += 1
                    action = "STRIP"
                else:
                    stats["md_no_frontmatter"] += 1
                    stripped = text
                    action = "COPY "
                if not dry_run:
                    dst_file.write_text(stripped, encoding="utf-8")
                if dry_run:
                    print(f"  [{action}] {rel}")
            except Exception as e:
                stats["errors"] += 1
                print(f"  [ERROR] {rel}: {e}", file=sys.stderr)
        else:
            stats["other"] += 1
            if not dry_run:
                try:
                    shutil.copy2(src_file, dst_file)
                except Exception as e:
                    stats["errors"] += 1
                    print(f"  [ERROR] {rel}: {e}", file=sys.stderr)

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Strip YAML frontmatter from ExpertPack .md files for deploy."
    )
    parser.add_argument("--src", required=True, help="Source pack directory")
    parser.add_argument("--out", required=True, help="Output directory for deploy-ready files")
    parser.add_argument("--force", action="store_true", help="Overwrite output directory without prompting")
    parser.add_argument("--dry-run", action="store_true", help="Report what would be stripped, no files written")
    args = parser.parse_args()

    src = Path(args.src).resolve()
    out = Path(args.out).resolve()

    if not src.exists() or not src.is_dir():
        print(f"ERROR: Source directory not found: {src}", file=sys.stderr)
        sys.exit(1)

    if src == out:
        print("ERROR: --src and --out must be different directories.", file=sys.stderr)
        sys.exit(1)

    if out.exists() and not args.dry_run:
        if not args.force:
            print(f"WARNING: Output directory exists: {out}")
            print("         It will be removed and recreated. Pass --force to suppress this warning.")
        shutil.rmtree(out)
    
    if not args.dry_run:
        out.mkdir(parents=True, exist_ok=True)

    mode = "DRY RUN — " if args.dry_run else ""
    print(f"\nep-strip-frontmatter  {mode}{src.name} → {out}")
    print("─" * 60)

    stats = process_pack(src, out, dry_run=args.dry_run)

    print("─" * 60)
    print(f"  Markdown files:      {stats['md_total']}")
    print(f"  Frontmatter stripped:{stats['md_stripped']}")
    print(f"  No frontmatter:      {stats['md_no_frontmatter']}")
    print(f"  Other files copied:  {stats['other']}")
    if stats["errors"]:
        print(f"  Errors:              {stats['errors']}  ⚠️")
        sys.exit(1)
    else:
        print(f"  Errors:              0  ✅")

    if not args.dry_run:
        print(f"\n✅ Deploy-ready pack written to: {out}")
        print("   Source files unchanged.")
    print()


if __name__ == "__main__":
    main()
