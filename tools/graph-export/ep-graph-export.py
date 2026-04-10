#!/usr/bin/env python3
"""ExpertPack Graph Export — generates _graph.yaml adjacency file for a pack.

Usage:
    python3 ep-graph-export.py /path/to/pack [--output _graph.yaml] [--format yaml|json]

Output (_graph.yaml by default at pack root):
    nodes:    list of {id, title, type, file, verified_at}
    edges:    list of {source, target, kind}
    meta:     {pack, slug, generated_at, node_count, edge_count}

Edge kinds:
    wikilink  -- [[target.md]] body reference
    related   -- frontmatter related: list
    context   -- context comment related= hint

Nodes without an id frontmatter field are excluded (use ep-validate --provenance first).
"""

import os, re, sys, yaml, json
from datetime import datetime, timezone
from collections import defaultdict

SKIP_DIRS  = {'.obsidian', '.git', 'node_modules', '__pycache__', '.venv', 'eval'}
SKIP_FILES = {'_index.md', 'overview.md', 'glossary.md', 'README.md',
              'SCHEMA.md', 'STATUS.md', 'Dashboard.md'}
SKIP_TYPES = {'index', 'source', 'proposition', 'summary', 'training'}

RE_FM      = re.compile(r'^---\n(.*?)\n---', re.DOTALL)
RE_WIKI    = re.compile(r'\[\[([^\]|#\n]+?)(?:\|[^\]\n]+?)?\]\]')
RE_CTX_REL = re.compile(r'<!--\s*context:[^>]*?related=([^\s,>]+)')


def parse_fm(content):
    m = RE_FM.match(content)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}


def strip_fm(content):
    return RE_FM.sub('', content, count=1).lstrip('\n')


def build_graph(pack_path):
    pack_path = os.path.abspath(pack_path)

    manifest = {}
    mp = os.path.join(pack_path, 'manifest.yaml')
    if os.path.exists(mp):
        try:
            manifest = yaml.safe_load(open(mp).read()) or {}
        except Exception:
            pass
    slug = manifest.get('slug', os.path.basename(pack_path))

    nodes = {}
    basename_to_ids = defaultdict(list)
    file_to_id = {}

    for root, dirs, files in os.walk(pack_path):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for f in sorted(files):
            if not f.endswith('.md') or f in SKIP_FILES:
                continue
            full = os.path.join(root, f)
            rel  = os.path.relpath(full, pack_path).replace(os.sep, '/')
            try:
                content = open(full, encoding='utf-8', errors='replace').read()
            except Exception:
                continue
            fm = parse_fm(content)
            nid = fm.get('id', '')
            if not nid:
                continue
            ftype = fm.get('type', '')
            if ftype in SKIP_TYPES:
                continue

            nodes[nid] = {
                'id':          nid,
                'title':       fm.get('title', ''),
                'type':        ftype,
                'file':        rel,
                'verified_at': str(fm.get('verified_at', '')) or None,
            }
            file_to_id[rel] = nid
            bn_noext = os.path.splitext(f)[0]
            basename_to_ids[bn_noext].append(nid)
            basename_to_ids[f].append(nid)

    def resolve(ref, source_dir):
        ref = ref.strip()
        ref_noext = ref[:-3] if ref.endswith('.md') else ref
        candidates = basename_to_ids.get(ref_noext) or basename_to_ids.get(ref, [])
        if len(candidates) == 1:
            return candidates[0]
        if len(candidates) > 1:
            for c in candidates:
                if nodes[c]['file'].startswith(source_dir):
                    return c
            return candidates[0]
        rel_try = os.path.normpath(os.path.join(source_dir, ref_noext + '.md')).replace(os.sep, '/')
        if rel_try in file_to_id:
            return file_to_id[rel_try]
        return None

    edges = []
    seen_edges = set()

    def add_edge(src, tgt, kind):
        if not src or not tgt or src == tgt:
            return
        key = (src, tgt, kind)
        if key not in seen_edges:
            seen_edges.add(key)
            edges.append({'source': src, 'target': tgt, 'kind': kind})

    for root, dirs, files in os.walk(pack_path):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for f in sorted(files):
            if not f.endswith('.md') or f in SKIP_FILES:
                continue
            full = os.path.join(root, f)
            rel  = os.path.relpath(full, pack_path).replace(os.sep, '/')
            src_id = file_to_id.get(rel)
            if not src_id:
                continue
            src_dir = os.path.dirname(rel)
            try:
                content = open(full, encoding='utf-8', errors='replace').read()
            except Exception:
                continue
            fm   = parse_fm(content)
            body = strip_fm(content)

            related = fm.get('related', [])
            if isinstance(related, str):
                related = [related]
            for r in (related or []):
                tgt = resolve(str(r), src_dir)
                if tgt:
                    add_edge(src_id, tgt, 'related')

            for wl in RE_WIKI.findall(body):
                tgt = resolve(wl.strip(), src_dir)
                if tgt:
                    add_edge(src_id, tgt, 'wikilink')

            for ctx_rel in RE_CTX_REL.findall(body):
                for r in ctx_rel.split(','):
                    r = r.strip()
                    if r:
                        tgt = resolve(r, src_dir)
                        if tgt:
                            add_edge(src_id, tgt, 'context')

    return {
        'meta': {
            'pack':           manifest.get('name', slug),
            'slug':           slug,
            'generated_at':   datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'node_count':     len(nodes),
            'edge_count':     len(edges),
            'schema_version': '1.0',
        },
        'nodes': list(nodes.values()),
        'edges': edges,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description='ExpertPack Graph Export v1.0')
    parser.add_argument('pack',   help='Path to pack directory')
    parser.add_argument('--output', default='_graph.yaml',
                        help='Output filename (default: _graph.yaml at pack root)')
    parser.add_argument('--format', choices=['yaml', 'json'], default='yaml',
                        help='Output format (default: yaml)')
    args = parser.parse_args()

    if not os.path.isdir(args.pack):
        print(f"Error: {args.pack} is not a directory", file=sys.stderr)
        sys.exit(1)

    print(f"Building graph for {os.path.basename(args.pack)}...", file=sys.stderr)
    graph = build_graph(args.pack)

    out_path = os.path.join(os.path.abspath(args.pack), args.output)
    with open(out_path, 'w', encoding='utf-8') as fh:
        if args.format == 'json':
            json.dump(graph, fh, indent=2, ensure_ascii=False)
        else:
            yaml.dump(graph, fh, allow_unicode=True, sort_keys=False,
                      default_flow_style=False)

    m = graph['meta']
    print(f"  Nodes: {m['node_count']}", file=sys.stderr)
    print(f"  Edges: {m['edge_count']}", file=sys.stderr)
    print(f"  Written: {out_path}", file=sys.stderr)


if __name__ == '__main__':
    main()
