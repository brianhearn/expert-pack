#!/usr/bin/env python3
"""ep-chunk-annotate.py — generate semantic chunk sidecars for ExpertPack files.

For files that exceed the one-atom size ceiling, this records header-aware chunk
boundaries in a git-tracked YAML sidecar (`<name>.chunks.yaml`) next to the
Markdown file. See schemas/rfcs/RFC-004-chunk-metadata-sidecars.md.

The sidecar keeps chunk metadata out of the embeddable body (no frontmatter
dilution) while giving the indexer deterministic boundaries to split on and
reassemble from by chunk_order.

Usage (Windows: use `python`):
    python ep-chunk-annotate.py <pack-dir|file.md>              # dry-run plan
    python ep-chunk-annotate.py <pack-dir|file.md> --apply      # write sidecars
    python ep-chunk-annotate.py <pack-dir|file.md> --check      # CI drift check
    python ep-chunk-annotate.py <file.md> --all                 # ignore size gate

Options:
    --min-tokens N          Only annotate files over N estimated tokens (default 1000)
    --all                   Annotate regardless of size (a single file, or a whole pack)
    --embedding-version STR Record this embedding_version in each chunk (default: unset)
"""

import argparse
import hashlib
import os
import re
import sys

import yaml

RE_FM = re.compile(r'^---\n(.*?)\n---', re.DOTALL)
RE_HEADING = re.compile(r'^(#{2,3})\s+(.+?)\s*$')
RE_FENCE = re.compile(r'^\s*```')
SKIP_DIRS = {'.obsidian', '.git', 'node_modules', 'eval', '__pycache__', '.venv'}
SKIP_BASENAMES = {'_index.md', '_access.json', '_index.json'}
ROOT_EXEMPT = {
    'README.md', 'SCHEMA.md', 'STATUS.md', 'LEGACY.md',
    'glossary.md', 'overview.md', 'freshness.md',
}
SIDECAR_SUFFIX = '.chunks.yaml'
CHARS_PER_TOKEN = 4


class FlowList(list):
    """A list rendered inline (flow style) by yaml.dump, e.g. [23, 45]."""


def _represent_flow_list(dumper, data):
    return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)


yaml.add_representer(FlowList, _represent_flow_list)


def parse_fm(content):
    m = RE_FM.match(content)
    if not m:
        return {}, 0
    fm = yaml.safe_load(m.group(1)) or {}
    # 1-indexed line number where the body starts (after the closing '---').
    body_start = content[:m.end()].count('\n') + 2
    return fm, body_start


def strip_fm_body(content):
    m = RE_FM.match(content)
    if m:
        return content[m.end():].lstrip('\n')
    return content


def slugify(text):
    slug = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    return slug or 'section'


def estimate_tokens(text):
    return int(len(text) / CHARS_PER_TOKEN)


def first_summary_line(lines):
    for line in lines:
        s = line.strip()
        if not s or s.startswith(('#', '```', '|', '>', '<!--', '---', '!')):
            continue
        return (s[:157] + '...') if len(s) > 160 else s
    return ''


def compute_chunks(content, stem):
    """Split the body at ##/### headings (ignoring fenced code). Returns a list
    of chunk dicts. Chunk 0 is the opening (H1 + lead paragraph)."""
    fm, body_start = parse_fm(content)
    lines = content.split('\n')

    # Collect heading boundaries in the body region, skipping code fences.
    boundaries = []  # (line_no_1indexed, heading_text)
    in_fence = False
    for idx in range(body_start - 1, len(lines)):
        line = lines[idx]
        if RE_FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = RE_HEADING.match(line)
        if m:
            boundaries.append((idx + 1, m.group(2).strip()))

    last_line = len(lines)
    # Trim a trailing empty final line from the split.
    if lines and lines[-1] == '':
        last_line -= 1

    segments = []  # (section_or_None, start_line, end_line)
    first_heading = boundaries[0][0] if boundaries else last_line + 1
    opening_end = first_heading - 1
    if opening_end >= body_start:
        segments.append((None, body_start, opening_end))
    for i, (hline, htext) in enumerate(boundaries):
        end = (boundaries[i + 1][0] - 1) if i + 1 < len(boundaries) else last_line
        segments.append((htext, hline, end))

    chunks = []
    seen = {}
    for order, (section, start, end) in enumerate(segments):
        seg_lines = lines[start - 1:end]
        text = '\n'.join(seg_lines)
        slug = 'opening' if section is None else slugify(section)
        if slug in seen:
            seen[slug] += 1
            slug = f"{slug}-{seen[slug]}"
        else:
            seen[slug] = 1
        chunk = {
            'chunk_id': f"{stem}--{slug}",
            'chunk_order': order,
            'section': section,
            'line_range': FlowList([start, end]),
            'tokenizer_tokens': estimate_tokens(text),
            'chunk_summary': first_summary_line(seg_lines),
        }
        chunks.append(chunk)
    return chunks


def build_sidecar(content, source_id, stem, embedding_version):
    body = strip_fm_body(content)
    content_hash = 'sha256:' + hashlib.sha256(body.encode('utf-8')).hexdigest()
    chunks = compute_chunks(content, stem)
    if embedding_version:
        for c in chunks:
            c['embedding_version'] = embedding_version
    return {
        'schema_version': '1.0',
        'source_id': source_id or stem,
        'content_hash': content_hash,
        'generated_by': 'ep-chunk-annotate',
        'chunks': chunks,
    }


def dump_sidecar(data):
    return yaml.dump(data, sort_keys=False, allow_unicode=True, width=200,
                     default_flow_style=False)


def is_content_file(rel):
    bn = os.path.basename(rel)
    if bn in SKIP_BASENAMES or bn in ROOT_EXEMPT or not bn.endswith('.md'):
        return False
    if bn.endswith(SIDECAR_SUFFIX):
        return False
    return os.path.dirname(rel) != ''  # skip root-level docs


def discover_targets(root):
    if os.path.isfile(root):
        return [root]
    out = []
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in sorted(files):
            full = os.path.join(dirpath, f)
            rel = os.path.relpath(full, root)
            if is_content_file(rel):
                out.append(full)
    return out


def process_file(path, args, explicit=False):
    """Returns (status, message). status in {written, ok, drift, missing, skipped}.

    A directory scan only treats oversized atomic/reference files as needing a
    sidecar — the same population ep-validate's W-CHUNK-01 targets (standard
    oversized concepts should split into atoms instead). An explicitly named
    file is always annotated so a maintainer can override that policy.
    """
    content = open(path, encoding='utf-8').read()
    fm, _ = parse_fm(content)
    body = strip_fm_body(content)
    tokens = estimate_tokens(body)
    stem = os.path.splitext(os.path.basename(path))[0]
    sidecar_path = os.path.splitext(path)[0] + SIDECAR_SUFFIX
    is_reference = (fm.get('concept_scope') == 'reference'
                    or fm.get('retrieval_strategy') == 'atomic')
    needs = explicit or args.all or (tokens > args.min_tokens and is_reference)

    if not needs and not os.path.exists(sidecar_path):
        return ('skipped', f"{tokens} tokens; no sidecar needed")

    expected = build_sidecar(content, fm.get('id'), stem, args.embedding_version)
    expected_text = dump_sidecar(expected)

    if args.check:
        if not os.path.exists(sidecar_path):
            return ('missing', f"needs sidecar ({tokens} tokens) but none present")
        current = open(sidecar_path, encoding='utf-8').read()
        if current.strip() != expected_text.strip():
            return ('drift', "sidecar is stale — rerun with --apply")
        return ('ok', f"{len(expected['chunks'])} chunks, up to date")

    if args.apply:
        with open(sidecar_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(expected_text)
        return ('written', f"{len(expected['chunks'])} chunks -> {os.path.basename(sidecar_path)}")

    return ('ok', f"would write {len(expected['chunks'])} chunks -> {os.path.basename(sidecar_path)}")


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    parser = argparse.ArgumentParser(description='ExpertPack chunk sidecar annotator')
    parser.add_argument('path', help='Pack directory or a single .md file')
    parser.add_argument('--apply', action='store_true', help='Write sidecars')
    parser.add_argument('--check', action='store_true',
                        help='Verify sidecars are up to date (CI); nonzero on drift/missing')
    parser.add_argument('--min-tokens', type=int, default=1000,
                        help='Only annotate files over this token estimate (default 1000)')
    parser.add_argument('--all', action='store_true',
                        help='Annotate regardless of size')
    parser.add_argument('--embedding-version', default=None,
                        help='Record this embedding_version in each chunk')
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Error: {args.path} not found")
        return 1

    targets = discover_targets(os.path.abspath(args.path))
    if not targets:
        print("No content files found.")
        return 1

    explicit = os.path.isfile(os.path.abspath(args.path))
    counts = {}
    problems = []
    for path in targets:
        status, msg = process_file(path, args, explicit=explicit)
        counts[status] = counts.get(status, 0) + 1
        if status in ('written', 'drift', 'missing') or (status == 'ok' and not args.check and args.apply is False and args.all):
            rel = os.path.relpath(path, os.path.abspath(args.path)) if os.path.isdir(args.path) else os.path.basename(path)
            print(f"  [{status}] {rel}: {msg}")
        if status in ('drift', 'missing'):
            problems.append(path)

    print("\n" + "=" * 60)
    summary = ', '.join(f"{k}={v}" for k, v in sorted(counts.items()))
    print(f"chunk-annotate: {summary}")
    print("=" * 60)

    if args.check and problems:
        print(f"CHECK FAILED: {len(problems)} sidecar(s) missing or stale")
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
