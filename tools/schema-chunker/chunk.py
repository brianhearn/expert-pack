#!/usr/bin/env python3
"""
ExpertPack Schema-Aware Chunker

Pre-processes ExpertPack .md files into optimally-sized chunk files for
OpenClaw's RAG indexer. Each output file is sized to fit within one chunk
of OpenClaw's token budget, so its dumb line-accumulator chunker passes
them through 1:1.

Usage:
    python3 chunk.py --pack ./path/to/pack --output ./path/to/pack/.chunks
    python3 chunk.py --pack ./pack --output ./pack/.chunks --max-chars 2000
    python3 chunk.py --pack ./pack --output ./pack/.chunks --config /path/to/openclaw.json

The tool respects ExpertPack schema conventions:
- Splits on ## headers (semantic boundaries)
- Keeps lead summaries with their titles
- Keeps proposition groups intact
- Attaches <!-- refresh --> metadata to preceding content
- Preserves YAML frontmatter with first chunk
- Tags each chunk with source file and tier metadata
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# YAML helpers (avoid PyYAML dependency)
# ---------------------------------------------------------------------------

def parse_simple_yaml(text: str) -> dict:
    """Parse simple YAML (key: value, lists) without PyYAML dependency.
    Handles the subset of YAML used in manifest.yaml: scalar values,
    simple lists, and one level of nested mappings."""
    result = {}
    current_key = None
    current_list = None
    indent_stack = []

    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # List item under current key
        if stripped.startswith("- ") and current_key:
            if current_list is None:
                current_list = []
                result[current_key] = current_list
            val = stripped[2:].strip().strip('"').strip("'")
            current_list.append(val)
            continue

        # Key: value pair
        match = re.match(r'^(\w[\w.]*)\s*:\s*(.*)', stripped)
        if match:
            key = match.group(1)
            val = match.group(2).strip().strip('"').strip("'")
            current_key = key
            current_list = None
            if val:
                result[key] = val
            # If no value, it might be a list or nested map — handled on next lines
            continue

    return result


def parse_retrieval_strategy(frontmatter: str) -> str:
    """Extract retrieval.strategy from YAML frontmatter block.
    Returns 'atomic' or 'sectioned' or None if not specified."""
    # Simple regex-based parser for nested yaml key (good enough for our use)
    match = re.search(r'retrieval\s*:\s*.*?strategy\s*:\s*(\w+)', frontmatter, re.DOTALL | re.IGNORECASE)
    if match:
        strategy = match.group(1).lower().strip()
        if strategy in ('atomic', 'sectioned'):
            return strategy
    return None


def get_directory_default_strategy(rel_path: str) -> str:
    """Return default chunking strategy based on directory convention."""
    path = Path(rel_path).as_posix()
    if 'workflows/' in path:
        return 'atomic'
    elif any(d in path for d in ('troubleshooting/errors/', 'troubleshooting/diagnostics/', 'troubleshooting/common-mistakes/')):
        return 'atomic'
    elif any(d in path for d in ('interfaces/', 'concepts/', 'faq/', 'propositions/', 'summaries/', 'commercial/')):
        return 'sectioned'
    return 'sectioned'


def parse_manifest(pack_dir: Path) -> dict:
    """Read and parse manifest.yaml from pack directory."""
    manifest_path = pack_dir / "manifest.yaml"
    if not manifest_path.exists():
        return {}
    try:
        import yaml
        with open(manifest_path) as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        with open(manifest_path) as f:
            return parse_simple_yaml(f.read())


def parse_context_tiers(manifest: dict) -> dict:
    """Extract context tier assignments from manifest.
    Returns {relative_path: tier_number} mapping."""
    tiers = {}
    context = manifest.get("context", {})
    if not isinstance(context, dict):
        return tiers

    for tier_name, tier_num in [("always", 1), ("searchable", 2), ("on_demand", 3)]:
        paths = context.get(tier_name, [])
        if isinstance(paths, list):
            for p in paths:
                tiers[str(p)] = tier_num
    return tiers


def resolve_tier(rel_path: str, tier_map: dict) -> int:
    """Resolve the context tier for a file path. Default is 2 (searchable)."""
    # Check exact match first
    if rel_path in tier_map:
        return tier_map[rel_path]

    # Check directory matches (paths ending with /)
    parts = Path(rel_path).parts
    for i in range(len(parts)):
        dir_path = "/".join(parts[:i + 1]) + "/"
        if dir_path in tier_map:
            return tier_map[dir_path]

    return 2  # Default: searchable


# ---------------------------------------------------------------------------
# OpenClaw config reader
# ---------------------------------------------------------------------------

def read_openclaw_config(config_path: str) -> int | None:
    """Read chunking.tokens from openclaw.json (JSON5 format).
    Returns max_chars (tokens * 4) or None if not found."""
    try:
        with open(config_path) as f:
            text = f.read()
        # Strip // line comments for JSON5 compatibility
        lines = []
        for line in text.split("\n"):
            # Remove // comments (but not inside strings — best effort)
            stripped = re.sub(r'(?<!["\':])//.*$', '', line)
            lines.append(stripped)
        text = "\n".join(lines)
        # Remove trailing commas before } or ]
        text = re.sub(r',\s*([}\]])', r'\1', text)

        config = json.loads(text)

        # Navigate to chunking.tokens — could be nested under agents.defaults
        tokens = None
        # Try agents.defaults.memorySearch.chunking.tokens
        try:
            tokens = config["agents"]["defaults"]["memorySearch"]["chunking"]["tokens"]
        except (KeyError, TypeError):
            pass
        # Try memorySearch.chunking.tokens
        if tokens is None:
            try:
                tokens = config["memorySearch"]["chunking"]["tokens"]
            except (KeyError, TypeError):
                pass

        if tokens and isinstance(tokens, (int, float)):
            return int(tokens) * 4
    except Exception as e:
        print(f"Warning: Could not read OpenClaw config: {e}", file=sys.stderr)
    return None


# ---------------------------------------------------------------------------
# Markdown parsing and chunking
# ---------------------------------------------------------------------------

# Directories and files to skip
SKIP_DIRS = {".chunks", ".git", "eval", "meta", "node_modules", "__pycache__"}
SKIP_FILES = {"manifest.yaml", "manifest.yml"}

# Regex patterns
FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?\n)---\s*\n', re.DOTALL)
LEAD_SUMMARY_RE = re.compile(r'^(>\s*\*\*Lead summary:?\*\*.*?)(?=\n[^>]|\n\n|\Z)', re.DOTALL | re.MULTILINE)
REFRESH_BLOCK_RE = re.compile(r'(<!--\s*refresh\b.*?-->)', re.DOTALL)
H1_RE = re.compile(r'^# (.+)$', re.MULTILINE)
H2_RE = re.compile(r'^## (.+)$', re.MULTILINE)
H3_RE = re.compile(r'^### (.+)$', re.MULTILINE)


def slugify(text: str) -> str:
    """Convert text to a URL/filename-safe slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')[:60]


def extract_frontmatter(content: str) -> tuple[str, str]:
    """Split YAML frontmatter from content. Returns (frontmatter, body)."""
    match = FRONTMATTER_RE.match(content)
    if match:
        fm = content[:match.end()]
        body = content[match.end():]
        return fm, body
    return "", content


def split_by_headers(content: str, header_re: re.Pattern) -> list[dict]:
    """Split content by header pattern into sections.
    Returns list of {title, content, header_line} dicts."""
    sections = []
    matches = list(header_re.finditer(content))

    if not matches:
        return [{"title": "", "content": content, "header_line": ""}]

    # Content before first header
    pre = content[:matches[0].start()].strip()
    if pre:
        sections.append({"title": "_preamble", "content": pre, "header_line": ""})

    for i, match in enumerate(matches):
        title = match.group(1).strip()
        header_line = match.group(0)
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        section_content = content[start:end].strip()
        sections.append({
            "title": title,
            "content": section_content,
            "header_line": header_line
        })

    return sections


def attach_refresh_blocks(text: str) -> str:
    """Ensure <!-- refresh --> blocks stay attached to preceding content.
    This is mostly a no-op when we split on headers correctly, but handles
    edge cases where a refresh block is at the boundary."""
    return text  # Handled naturally by section-based splitting


def split_oversized_section(text: str, max_chars: int) -> list[str]:
    """Split a section that's too large. Tries ### headers, then paragraphs,
    then line boundaries. Never splits mid-line."""

    if len(text) <= max_chars:
        return [text]

    # Try splitting on ### headers
    h3_sections = split_by_headers(text, H3_RE)
    if len(h3_sections) > 1:
        chunks = []
        for section in h3_sections:
            if len(section["content"]) <= max_chars:
                chunks.append(section["content"])
            else:
                chunks.extend(split_by_paragraphs(section["content"], max_chars))
        return chunks

    return split_by_paragraphs(text, max_chars)


def split_by_paragraphs(text: str, max_chars: int) -> list[str]:
    """Split text by paragraph boundaries (double newline).
    Falls back to line-by-line if paragraphs are too large."""
    paragraphs = re.split(r'\n\n+', text)

    if len(paragraphs) <= 1:
        return split_by_lines(text, max_chars)

    chunks = []
    current = ""

    for para in paragraphs:
        candidate = (current + "\n\n" + para).strip() if current else para
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                chunks.append(current)
            if len(para) <= max_chars:
                current = para
            else:
                # Paragraph itself is too large — split by lines
                line_chunks = split_by_lines(para, max_chars)
                chunks.extend(line_chunks[:-1])
                current = line_chunks[-1] if line_chunks else ""

    if current:
        chunks.append(current)

    return chunks


def split_by_lines(text: str, max_chars: int) -> list[str]:
    """Last resort: split on line boundaries."""
    lines = text.split("\n")
    chunks = []
    current = ""

    for line in lines:
        candidate = (current + "\n" + line) if current else line
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                chunks.append(current)
            current = line
            # If a single line exceeds max_chars, include it anyway
            # (we never split mid-line)

    if current:
        chunks.append(current)

    return chunks


def resolve_strategy(frontmatter: str, rel_path: str) -> str:
    """Resolve chunking strategy: frontmatter override → directory default → sectioned."""
    fm_strategy = parse_retrieval_strategy(frontmatter)
    if fm_strategy:
        return fm_strategy
    return get_directory_default_strategy(rel_path)


def chunk_file(content: str, max_chars: int, rel_path: str = "") -> list[dict]:
    """Chunk a single markdown file respecting schema conventions and retrieval strategy.

    Returns list of {text, section_title, is_atomic: bool, strategy: str} dicts."""

    # Extract frontmatter
    frontmatter, body = extract_frontmatter(content)

    strategy = resolve_strategy(frontmatter, rel_path)

    # If atomic strategy, emit as one chunk (even if huge)
    if strategy == 'atomic':
        h1_match = H1_RE.search(body)
        h1_title = h1_match.group(1).strip() if h1_match else "content"
        full_text = frontmatter + body if frontmatter else body
        return [{
            "text": full_text,
            "section_title": h1_title,
            "is_atomic": True,
            "strategy": strategy
        }]

    # Get the H1 title and any lead summary (for sectioned)
    h1_match = H1_RE.search(body)
    h1_title = h1_match.group(1).strip() if h1_match else ""

    # Split body by ## headers
    sections = split_by_headers(body, H2_RE)

    chunks = []

    for section in sections:
        title = section["title"]
        text = section["content"]

        # For preamble section (before first ##), attach frontmatter
        if title == "_preamble" and frontmatter:
            text = frontmatter + text
            title = h1_title or "_preamble"

        # Check if it fits in one chunk
        if len(text) <= max_chars:
            chunks.append({"text": text, "section_title": title, "is_atomic": False, "strategy": strategy})
        else:
            # Split oversized section
            sub_chunks = split_oversized_section(text, max_chars)
            for i, sub in enumerate(sub_chunks):
                suffix = f" (part {i + 1})" if len(sub_chunks) > 1 else ""
                chunks.append({
                    "text": sub,
                    "section_title": f"{title}{suffix}",
                    "is_atomic": False,
                    "strategy": strategy
                })

    # If no chunks produced (empty file), return empty
    if not chunks:
        return []

    # If frontmatter wasn't part of preamble (no preamble text), prepend to first chunk
    if frontmatter and sections and sections[0]["title"] != "_preamble":
        first = chunks[0]
        combined = frontmatter + first["text"]
        if len(combined) <= max_chars:
            first["text"] = combined

    return chunks


# ---------------------------------------------------------------------------
# File naming
# ---------------------------------------------------------------------------

def make_chunk_filename(rel_path: str, section_title: str, chunk_index: int,
                        total_chunks: int, is_atomic: bool = False) -> str:
    """Generate chunk filename from source path and section.

    For atomic files that exceed size: produces {name}--summary.md and {name}--full.md
    Otherwise follows standard convention.
    """
    path = Path(rel_path)
    stem = path.stem  # filename without .md
    parent = str(path.parent) if str(path.parent) != "." else ""

    parts = []
    if parent:
        parts.append(parent.replace("/", "--").replace("\\", "--"))
    parts.append(stem)

    if is_atomic and total_chunks > 1:
        # Special case for oversized atomic → summary + full
        if "summary" in section_title.lower() or chunk_index == 0:
            parts.append("summary")
        else:
            parts.append("full")
    elif total_chunks > 1 and section_title and section_title != "_preamble" and not is_atomic:
        slug = slugify(section_title)
        if slug:
            parts.append(slug)
    elif total_chunks > 1:
        parts.append(f"part-{chunk_index + 1}")

    filename = "--".join(parts) + ".md"

    # Ensure no duplicate -- from empty parts
    filename = re.sub(r'-{3,}', '--', filename)

    return filename


# ---------------------------------------------------------------------------
# Main processing
# ---------------------------------------------------------------------------

def should_skip(rel_path: str) -> str | None:
    """Check if a file should be skipped. Returns reason string or None."""
    parts = Path(rel_path).parts

    # Skip hidden dirs/files
    for part in parts:
        if part.startswith("."):
            return "hidden file/directory"

    # Skip specific directories
    if parts[0] in SKIP_DIRS:
        return f"excluded directory: {parts[0]}"

    # Skip specific files
    filename = parts[-1]
    if filename in SKIP_FILES:
        return "excluded file"

    # Skip non-markdown
    if not filename.endswith(".md"):
        return "non-markdown file"

    return None


def collect_source_files(pack_dir: Path) -> list[str]:
    """Collect all processable .md files from the pack directory.
    Returns relative paths sorted alphabetically."""
    files = []
    for root, dirs, filenames in os.walk(pack_dir):
        # Prune skipped directories in-place
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        dirs.sort()

        for fname in sorted(filenames):
            abs_path = Path(root) / fname
            rel_path = str(abs_path.relative_to(pack_dir))

            skip_reason = should_skip(rel_path)
            if skip_reason:
                continue

            files.append(rel_path)

    return files


def process_pack(pack_dir: Path, output_dir: Path, max_chars: int,
                 verbose: bool = False) -> dict:
    """Process an entire ExpertPack into chunked output files.

    Returns a summary dict with statistics."""

    # Read manifest
    manifest = parse_manifest(pack_dir)
    pack_name = manifest.get("name", pack_dir.name)
    pack_slug = manifest.get("slug", pack_dir.name)
    tier_map = parse_context_tiers(manifest)

    # Collect source files
    source_files = collect_source_files(pack_dir)

    # Clear and create output directory
    if output_dir.exists():
        for f in output_dir.iterdir():
            if f.is_file():
                f.unlink()
    output_dir.mkdir(parents=True, exist_ok=True)

    # Track statistics
    stats = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "pack": pack_slug,
        "source_files": len(source_files),
        "chunks_produced": 0,
        "max_chars": max_chars,
        "total_chars": 0,
        "skipped": [],
        "included": [],
        "warnings": [],
        "oversized": [],
    }

    # Track used filenames to avoid collisions
    used_names: dict[str, int] = {}

    for rel_path in source_files:
        abs_path = pack_dir / rel_path
        content = abs_path.read_text(encoding="utf-8", errors="replace")

        if not content.strip():
            stats["warnings"].append(f"{rel_path}: empty file, skipped")
            continue

        tier = resolve_tier(rel_path, tier_map)

        # Reserve chars for source comment (added to each chunk)
        # <!-- source: {path} | section: {title} | tier: {n} -->
        # Use generous overhead to account for long paths and section titles
        comment_overhead = 20 + len(rel_path) + 50  # base + path + section/tier
        effective_max = max_chars - max(comment_overhead, 120)

        # Chunk the file
        chunks = chunk_file(content, effective_max, rel_path=rel_path)

        if not chunks:
            stats["warnings"].append(f"{rel_path}: no chunks produced")
            continue

        stats["included"].append(rel_path)

        total_for_file = len(chunks)
        atomic_strategy = chunks[0].get("strategy", "sectioned") if chunks else "sectioned"

        for i, chunk in enumerate(chunks):
            is_atomic_chunk = chunk.get("is_atomic", False)

            # Build source comment with sequence metadata for sectioned splits
            section_title = chunk["section_title"]
            section_part = f" | section: {section_title}" if section_title and section_title != "_preamble" else ""
            if not is_atomic_chunk and total_for_file > 1:
                of_n = f" of {total_for_file}"
                seq_glob = rel_path.replace('.md', '--*.md').replace('/', '--')
                section_part = f" | section: {section_title} (part {i+1}{of_n}) | sequence: {seq_glob}"
            source_comment = f"<!-- source: {rel_path}{section_part} | tier: {tier} -->\n"

            chunk_text = source_comment + chunk["text"]

            # Generate filename (pass atomic flag)
            filename = make_chunk_filename(rel_path, section_title, i, total_for_file, is_atomic=is_atomic_chunk)

            # Handle collisions
            if filename in used_names:
                used_names[filename] += 1
                base, ext = os.path.splitext(filename)
                filename = f"{base}--{used_names[filename]}{ext}"
            else:
                used_names[filename] = 1

            # Write chunk file
            chunk_path = output_dir / filename
            chunk_path.write_text(chunk_text, encoding="utf-8")

            stats["chunks_produced"] += 1
            stats["total_chars"] += len(chunk_text)

            # Check for oversized chunks
            if len(chunk_text) > max_chars:
                stats["oversized"].append({
                    "file": filename,
                    "chars": len(chunk_text),
                    "source": rel_path
                })

            if verbose:
                print(f"  {rel_path} → {filename} ({len(chunk_text)} chars, strategy={atomic_strategy})")

    # Calculate average
    avg_chars = (stats["total_chars"] // stats["chunks_produced"]
                 if stats["chunks_produced"] > 0 else 0)
    stats["avg_chunk_chars"] = avg_chars

    # Collect skipped files info
    for root, dirs, filenames in os.walk(pack_dir):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fname in filenames:
            abs_path = Path(root) / fname
            rel_path = str(abs_path.relative_to(pack_dir))
            skip_reason = should_skip(rel_path)
            if skip_reason:
                stats["skipped"].append({"file": rel_path, "reason": skip_reason})

    # Write chunk manifest
    atomic_count = sum(1 for p in stats.get("included", []) if "workflows/" in p or "troubleshooting/" in p)  # rough
    manifest_out = {
        "generated": stats["generated"],
        "pack": stats["pack"],
        "source_files": stats["source_files"],
        "chunks_produced": stats["chunks_produced"],
        "max_chars": stats["max_chars"],
        "avg_chunk_chars": stats["avg_chunk_chars"],
        "strategy_stats": {
            "atomic_files_approx": atomic_count,
            "sectioned_files_approx": len(stats["included"]) - atomic_count
        },
        "coverage": {
            "included": stats["included"],
            "skipped": [s["file"] for s in stats["skipped"]]
        }
    }
    manifest_path = output_dir / "_manifest.json"
    manifest_path.write_text(json.dumps(manifest_out, indent=2) + "\n", encoding="utf-8")

    return stats


def print_summary(stats: dict, output_dir: Path):
    """Print a human-readable summary of chunking results."""
    print(f"\nSchema Chunker — {stats['pack']}")
    print(f"{'─' * 40}")
    print(f"Source files:    {stats['source_files']}")
    print(f"Chunks produced: {stats['chunks_produced']}")
    print(f"Avg chunk size:  {stats['avg_chunk_chars']:,} chars")
    print(f"Max chunk budget: {stats['max_chars']:,} chars")
    print(f"Files skipped:   {len(stats['skipped'])}")

    strat = stats.get("strategy_stats", {})
    print(f"Atomic (approx): {strat.get('atomic_files_approx', 0)}")
    print(f"Sectioned (approx): {strat.get('sectioned_files_approx', 0)}")

    if stats["oversized"]:
        print(f"\n⚠️  Oversized chunks ({len(stats['oversized'])}):")
        for item in stats["oversized"]:
            print(f"  {item['file']}: {item['chars']:,} chars (from {item['source']})")

    if stats["warnings"]:
        print(f"\n⚠️  Warnings ({len(stats['warnings'])}):")
        for w in stats["warnings"]:
            print(f"  {w}")

    pct = (len(stats["included"]) / stats["source_files"] * 100
           if stats["source_files"] > 0 else 0)
    print(f"\nCoverage: {pct:.0f}% of content files")
    print(f"Output:   {output_dir}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="ExpertPack Schema-Aware Chunker — pre-process pack files for OpenClaw RAG"
    )
    parser.add_argument("--pack", required=True,
                        help="Path to ExpertPack directory")
    parser.add_argument("--output", required=True,
                        help="Output directory for chunk files")
    parser.add_argument("--max-chars", type=int, default=2000,
                        help="Max characters per chunk file (default: 2000)")
    parser.add_argument("--config", default=None,
                        help="Path to openclaw.json — reads chunking.tokens to compute max-chars")
    parser.add_argument("--verbose", action="store_true",
                        help="Print per-file chunking details")

    args = parser.parse_args()

    pack_dir = Path(args.pack).resolve()
    output_dir = Path(args.output).resolve()

    if not pack_dir.is_dir():
        print(f"Error: Pack directory not found: {pack_dir}", file=sys.stderr)
        sys.exit(1)

    # Resolve max_chars from config if provided
    max_chars = args.max_chars
    if args.config:
        config_max = read_openclaw_config(args.config)
        if config_max:
            max_chars = config_max
            print(f"Using max-chars {max_chars} from OpenClaw config "
                  f"(chunking.tokens={max_chars // 4})")
        else:
            print(f"Could not read chunking.tokens from config, "
                  f"using default: {max_chars}")

    # Process
    stats = process_pack(pack_dir, output_dir, max_chars, verbose=args.verbose)
    print_summary(stats, output_dir)


if __name__ == "__main__":
    main()
