#!/usr/bin/env python3
"""ExpertPack Ontology Suggest

Suggests a lightweight ontology from an ExpertPack's existing Markdown / AKS
projection. This is review-first: it writes suggestions for maintainers to
accept/reject, not authoritative schema changes.

Usage:
    python tools/ontology-suggest/ep-ontology-suggest.py /path/to/pack
    python tools/ontology-suggest/ep-ontology-suggest.py /path/to/pack --format json
    python tools/ontology-suggest/ep-ontology-suggest.py /path/to/pack --output ontology-suggestions.yaml
    python tools/ontology-suggest/ep-ontology-suggest.py /path/to/pack --init-ontology
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("Error: pyyaml required. pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# Import exporter helpers without requiring installation as a package.
EXPORTER_DIR = Path(__file__).resolve().parents[1] / "micro-record-exporter"
sys.path.insert(0, str(EXPORTER_DIR))
try:
    from ep_micro_record_export import (  # type: ignore[import-not-found]
        build_micro_record,
        load_graph_edges,
    )
except ModuleNotFoundError:
    # Script filename has hyphens; import by path.
    import importlib.util

    exporter_path = EXPORTER_DIR / "ep-micro-record-export.py"
    spec = importlib.util.spec_from_file_location("ep_micro_record_export", exporter_path)
    if spec is None or spec.loader is None:
        raise
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    build_micro_record = mod.build_micro_record
    load_graph_edges = mod.load_graph_edges


STOPWORDS = {
    "the", "and", "for", "with", "from", "that", "this", "into", "when", "where",
    "what", "which", "your", "you", "how", "why", "are", "can", "will", "using",
    "used", "uses", "use", "about", "between", "through", "after", "before",
    "overview", "common", "mistakes", "troubleshooting", "workflow", "concept",
}

ENTITY_PATTERNS = [
    re.compile(r"\b[A-Z][A-Za-z0-9]+(?:\s+[A-Z][A-Za-z0-9]+){0,3}\b"),
    re.compile(r"\b[A-Z]{2,}\b"),
]


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "unknown"


def today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def load_manifest(pack_path: Path) -> dict[str, Any]:
    mp = pack_path / "manifest.yaml"
    if not mp.exists():
        return {}
    try:
        return yaml.safe_load(mp.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}


def load_accepted_ontology(pack_path: Path, ontology_path: Path | None = None) -> dict[str, Any]:
    path = ontology_path or (pack_path / "ontology.yaml")
    if not path.exists():
        return {"schema": "expertpack.ontology.v1", "entities": [], "relations": []}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        return {"schema": "expertpack.ontology.v1", "entities": [], "relations": []}
    data.setdefault("entities", [])
    data.setdefault("relations", [])
    return data


def ontology_indexes(ontology: dict[str, Any]) -> tuple[set[str], set[tuple[str, str, str]], dict[str, str]]:
    entity_ids = {str(e.get("id")) for e in ontology.get("entities", []) if e.get("id")}
    relation_keys = {
        (str(r.get("source")), str(r.get("target")), str(r.get("kind")))
        for r in ontology.get("relations", [])
        if r.get("source") and r.get("target") and r.get("kind")
    }
    alias_to_id: dict[str, str] = {}
    for entity in ontology.get("entities", []):
        eid = entity.get("id")
        if not eid:
            continue
        labels = [entity.get("label", ""), *entity.get("aliases", [])]
        for label in labels:
            if str(label).strip():
                alias_to_id[slugify(str(label))] = str(eid)
    return entity_ids, relation_keys, alias_to_id


def build_records(pack_path: Path, slug: str) -> list[dict[str, Any]]:
    edges_by_file = load_graph_edges(pack_path)
    records: list[dict[str, Any]] = []
    for fp in sorted(pack_path.rglob("*.md")):
        record = build_micro_record(
            pack_path=pack_path,
            file_path=fp,
            pack_slug=slug,
            edges_by_file=edges_by_file,
            compact=True,
        )
        if record:
            records.append(record)
    return sorted(records, key=lambda r: r["id"])


def extract_terms(record: dict[str, Any]) -> set[str]:
    candidates: list[str] = []
    for key in ("title", "canonical_statement"):
        value = str(record.get(key, ""))
        candidates.extend(p.group(0) for pat in ENTITY_PATTERNS for p in pat.finditer(value))
    candidates.extend(str(t) for t in record.get("tags", []) if str(t).strip())

    out: set[str] = set()
    for c in candidates:
        cleaned = re.sub(r"\s+", " ", c.strip())
        if not cleaned or len(cleaned) < 3:
            continue
        if cleaned.lower() in STOPWORDS:
            continue
        if cleaned.isdigit():
            continue
        out.add(cleaned)
    return out


def infer_category(record: dict[str, Any]) -> str:
    rtype = str(record.get("type", "reference") or "reference")
    tags = {str(t).lower() for t in record.get("tags", [])}
    path = str(record.get("canonical_path", ""))
    title = str(record.get("title", "")).lower()

    if rtype == "workflow" or "workflow" in path:
        return "workflow"
    if rtype in {"troubleshooting", "faq"} or "error" in tags or "mistake" in title:
        return "failure-mode"
    if rtype in {"commercial", "customer"}:
        return "commercial"
    if rtype in {"interface", "screen", "ui"} or "interface" in tags or "screen" in path:
        return "interface"
    if "api" in tags or "code" in tags or "class" in tags:
        return "artifact"
    return rtype or "concept"


def suggest_ontology(pack_path: Path, ontology_path: Path | None = None) -> dict[str, Any]:
    manifest = load_manifest(pack_path)
    slug = manifest.get("slug") or pack_path.name
    records = build_records(pack_path, slug)
    accepted = load_accepted_ontology(pack_path, ontology_path)
    accepted_entity_ids, accepted_relation_keys, alias_to_id = ontology_indexes(accepted)

    categories: dict[str, list[str]] = defaultdict(list)
    term_records: dict[str, set[str]] = defaultdict(set)
    explicit_edges: list[dict[str, str]] = []

    for r in records:
        rid = r["id"]
        categories[infer_category(r)].append(rid)
        for term in extract_terms(r):
            term_records[term].add(rid)
        for req in r.get("requires", []):
            explicit_edges.append({"source": rid, "target": str(req), "kind": "requires"})
        for edge in r.get("related", []):
            explicit_edges.append({
                "source": rid,
                "target": str(edge.get("id")),
                "kind": str(edge.get("kind", "related")),
            })

    # Candidate entities are terms that appear in multiple records or are tags on at least one record.
    entities = []
    for term, refs in sorted(term_records.items(), key=lambda x: (-len(x[1]), x[0].lower())):
        if len(refs) < 2:
            continue
        eid = alias_to_id.get(slugify(term), f"entity:{slugify(term)}")
        status = "existing" if eid in accepted_entity_ids else "suggested"
        entities.append({
            "id": eid,
            "label": term,
            "kind": "term",
            "evidence_count": len(refs),
            "evidence": sorted(refs)[:10],
            "status": status,
        })

    category_nodes = [
        {
            "id": f"category:{slugify(cat)}",
            "label": cat,
            "kind": "category",
            "member_count": len(ids),
            "members": sorted(ids)[:20],
            "status": "suggested",
        }
        for cat, ids in sorted(categories.items())
    ]

    for edge in explicit_edges:
        key = (edge.get("source", ""), edge.get("target", ""), edge.get("kind", ""))
        edge["status"] = "existing" if key in accepted_relation_keys else "suggested"

    relation_counts = Counter(edge["kind"] for edge in explicit_edges)

    return {
        "meta": {
            "pack": manifest.get("name", slug),
            "slug": slug,
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "record_count": len(records),
            "entity_suggestion_count": len(entities),
            "category_count": len(category_nodes),
            "explicit_edge_count": len(explicit_edges),
            "relation_kinds": dict(sorted(relation_counts.items())),
            "review_required": True,
            "accepted_ontology_entities": len(accepted_entity_ids),
            "accepted_ontology_relations": len(accepted_relation_keys),
        },
        "review_instructions": [
            "This file is suggestions only. Do not treat entities/categories as authoritative until reviewed.",
            "Accept useful entities by moving them into a maintained ontology/graph file or pack-specific entity registry.",
            "Reject generic tags or accidental capitalized phrases that do not represent domain entities.",
        ],
        "categories": category_nodes,
        "entities": entities,
        "edges": explicit_edges,
    }


def init_ontology(pack_path: Path, output: Path | None = None, force: bool = False) -> Path:
    manifest = load_manifest(pack_path)
    slug = manifest.get("slug") or pack_path.name
    out_path = output or (pack_path / "ontology.yaml")
    if out_path.exists() and not force:
        print(f"Error: {out_path} already exists (use --force to overwrite)", file=sys.stderr)
        sys.exit(2)
    ontology = {
        "schema": "expertpack.ontology.v1",
        "pack": slug,
        "updated_at": today(),
        "entities": [],
        "relations": [],
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(yaml.safe_dump(ontology, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="ExpertPack ontology suggestion generator")
    parser.add_argument("pack", help="Path to pack directory")
    parser.add_argument("--output", default="ontology-suggestions.yaml", help="Output path (default: pack/ontology-suggestions.yaml)")
    parser.add_argument("--format", choices=["yaml", "json"], default="yaml", help="Output format")
    parser.add_argument("--ontology", default=None, help="Accepted ontology path (default: pack/ontology.yaml)")
    parser.add_argument("--init-ontology", action="store_true", help="Create an empty accepted ontology.yaml and exit")
    parser.add_argument("--force", action="store_true", help="Allow --init-ontology to overwrite existing ontology file")
    args = parser.parse_args()

    pack_path = Path(args.pack).resolve()
    if not pack_path.is_dir():
        print(f"Error: {pack_path} is not a directory", file=sys.stderr)
        sys.exit(1)

    ontology_path = Path(args.ontology).resolve() if args.ontology else None
    if args.init_ontology:
        out = Path(args.output).resolve() if args.output != "ontology-suggestions.yaml" else None
        written = init_ontology(pack_path, output=out, force=args.force)
        print(f"Written: {written}", file=sys.stderr)
        return

    suggestions = suggest_ontology(pack_path, ontology_path=ontology_path)
    out_path = Path(args.output)
    if not out_path.is_absolute():
        out_path = pack_path / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if args.format == "json":
        out_path.write_text(json.dumps(suggestions, indent=2, ensure_ascii=False), encoding="utf-8")
    else:
        out_path.write_text(yaml.safe_dump(suggestions, sort_keys=False, allow_unicode=True), encoding="utf-8")

    meta = suggestions["meta"]
    print(f"Records: {meta['record_count']}", file=sys.stderr)
    print(f"Categories: {meta['category_count']}", file=sys.stderr)
    print(f"Entity suggestions: {meta['entity_suggestion_count']}", file=sys.stderr)
    print(f"Explicit edges: {meta['explicit_edge_count']}", file=sys.stderr)
    print(f"Written: {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
