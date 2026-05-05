#!/usr/bin/env python3
"""
ExpertPack SQLite Triple Store Loader

Loads a micro-records JSONL file (from ep-micro-record-export.py) into a
SQLite database for deterministic ID lookups alongside vector search.

Schema:
  records   — one row per micro-record or compact AKS record (id, label, canonical_statement, type, pack, ...)
  provenance — provenance fields per record (recorded_at, valid_from, verified_at, ...)
  edges      — graph edges between records (source_id, target_id, kind)
  tags       — many-to-many tag associations

Usage:
    python tools/micro-record-exporter/ep-sqlite-loader.py \
        --input exports/ezt-designer-micro-records.jsonl \
        --db exports/ezt-designer.db

    # Query examples (after loading):
    python tools/micro-record-exporter/ep-sqlite-loader.py \
        --db exports/ezt-designer.db \
        --lookup "ezt-designer/concepts/con-scheduling-algorithm"

    python tools/micro-record-exporter/ep-sqlite-loader.py \
        --db exports/ezt-designer.db \
        --neighbors "ezt-designer/concepts/con-scheduling-algorithm"

    python tools/micro-record-exporter/ep-sqlite-loader.py \
        --db exports/ezt-designer.db \
        --stats
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

DDL = """
CREATE TABLE IF NOT EXISTS records (
    id                  TEXT PRIMARY KEY,
    source_span_uri     TEXT NOT NULL,
    label               TEXT,
    canonical_statement TEXT,
    type                TEXT,
    pack                TEXT,
    lifecycle_status    TEXT DEFAULT 'active',
    superseded_by       TEXT,
    valid_until         TEXT
);

CREATE TABLE IF NOT EXISTS provenance (
    id              TEXT PRIMARY KEY REFERENCES records(id),
    recorded_at     TEXT,
    valid_from      TEXT,
    verified_at     TEXT,
    verified_by     TEXT,
    source          TEXT,
    content_hash    TEXT
);

CREATE TABLE IF NOT EXISTS edges (
    source_id   TEXT NOT NULL,
    target_id   TEXT NOT NULL,
    kind        TEXT NOT NULL,
    PRIMARY KEY (source_id, target_id, kind)
);

CREATE TABLE IF NOT EXISTS tags (
    record_id   TEXT NOT NULL REFERENCES records(id),
    tag         TEXT NOT NULL,
    PRIMARY KEY (record_id, tag)
);

CREATE INDEX IF NOT EXISTS idx_records_type ON records(type);
CREATE INDEX IF NOT EXISTS idx_records_pack ON records(pack);
CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source_id);
CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target_id);
CREATE INDEX IF NOT EXISTS idx_tags_tag ON tags(tag);
CREATE INDEX IF NOT EXISTS idx_provenance_valid_from ON provenance(valid_from);
CREATE INDEX IF NOT EXISTS idx_provenance_verified_at ON provenance(verified_at);

-- Full-text search on label + canonical_statement
CREATE VIRTUAL TABLE IF NOT EXISTS records_fts USING fts5(
    id UNINDEXED,
    label,
    canonical_statement,
    content=records,
    content_rowid=rowid
);

CREATE TRIGGER IF NOT EXISTS records_ai AFTER INSERT ON records BEGIN
    INSERT INTO records_fts(rowid, id, label, canonical_statement)
    VALUES (new.rowid, new.id, new.label, new.canonical_statement);
END;

CREATE TRIGGER IF NOT EXISTS records_ad AFTER DELETE ON records BEGIN
    INSERT INTO records_fts(records_fts, rowid, id, label, canonical_statement)
    VALUES ('delete', old.rowid, old.id, old.label, old.canonical_statement);
END;
"""


# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------

def load_jsonl(path: Path, db_path: Path) -> dict:
    """Load a micro-records JSONL into SQLite. Returns stats dict."""
    conn = sqlite3.connect(str(db_path))
    conn.executescript(DDL)

    records_inserted = 0
    edges_inserted = 0
    tags_inserted = 0
    skipped = 0

    with conn:
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"  Warning: line {line_no} invalid JSON — {e}")
                skipped += 1
                continue

            rid = r.get("id")
            if not rid:
                skipped += 1
                continue

            # records
            lc = r.get("lifecycle", {})
            conn.execute(
                """INSERT OR REPLACE INTO records
                   (id, source_span_uri, label, canonical_statement, type, pack,
                    lifecycle_status, superseded_by, valid_until)
                   VALUES (?,?,?,?,?,?,?,?,?)""",
                (
                    rid,
                    r.get("source_span_uri", ""),
                    r.get("label") or r.get("title", ""),
                    r.get("canonical_statement", ""),
                    r.get("type", ""),
                    r.get("pack", ""),
                    lc.get("status", "active"),
                    lc.get("superseded_by"),
                    lc.get("valid_until"),
                ),
            )
            records_inserted += 1

            # provenance. Full records use nested provenance; compact AKS
            # records promote these fields to the top level.
            prov = r.get("provenance", {}) or {}
            content_hash = prov.get("content_hash") or r.get("content_hash") or r.get("source_checksum")
            if prov or any(k in r for k in ("recorded_at", "valid_from", "verified_at", "verified_by", "source", "content_hash", "source_checksum")):
                conn.execute(
                    """INSERT OR REPLACE INTO provenance
                       (id, recorded_at, valid_from, verified_at, verified_by, source, content_hash)
                       VALUES (?,?,?,?,?,?,?)""",
                    (
                        rid,
                        prov.get("recorded_at") or r.get("recorded_at"),
                        prov.get("valid_from") or r.get("valid_from"),
                        prov.get("verified_at") or r.get("verified_at"),
                        prov.get("verified_by") or r.get("verified_by"),
                        prov.get("source") or r.get("source"),
                        content_hash,
                    ),
                )

            # edges
            for req in r.get("requires", []):
                if req:
                    conn.execute(
                        "INSERT OR IGNORE INTO edges (source_id, target_id, kind) VALUES (?,?,?)",
                        (rid, str(req), "requires"),
                    )
                    edges_inserted += 1
            for sup in r.get("supersedes", []):
                if sup:
                    conn.execute(
                        "INSERT OR IGNORE INTO edges (source_id, target_id, kind) VALUES (?,?,?)",
                        (rid, str(sup), "supersedes"),
                    )
                    edges_inserted += 1
            for edge in r.get("related", []):
                target = edge.get("id")
                kind = edge.get("kind", "wikilink")
                if target:
                    conn.execute(
                        "INSERT OR IGNORE INTO edges (source_id, target_id, kind) VALUES (?,?,?)",
                        (rid, target, kind),
                    )
                    edges_inserted += 1

            # tags
            for tag in r.get("tags", []):
                conn.execute(
                    "INSERT OR IGNORE INTO tags (record_id, tag) VALUES (?,?)",
                    (rid, tag),
                )
                tags_inserted += 1

    conn.close()
    return {
        "records": records_inserted,
        "edges": edges_inserted,
        "tags": tags_inserted,
        "skipped": skipped,
        "db_bytes": db_path.stat().st_size,
    }


# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------

def lookup(db_path: Path, record_id: str):
    """Fetch a single record by ID with provenance and tags."""
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    row = conn.execute("SELECT * FROM records WHERE id=?", (record_id,)).fetchone()
    if not row:
        print(f"Not found: {record_id}")
        conn.close()
        return

    prov = conn.execute("SELECT * FROM provenance WHERE id=?", (record_id,)).fetchone()
    tags = [r["tag"] for r in conn.execute("SELECT tag FROM tags WHERE record_id=?", (record_id,))]
    edges_out = conn.execute(
        "SELECT target_id, kind FROM edges WHERE source_id=?", (record_id,)
    ).fetchall()
    edges_in = conn.execute(
        "SELECT source_id, kind FROM edges WHERE target_id=?", (record_id,)
    ).fetchall()
    conn.close()

    result = dict(row)
    result["tags"] = tags
    result["provenance"] = dict(prov) if prov else {}
    result["related_out"] = [{"id": e["target_id"], "kind": e["kind"]} for e in edges_out]
    result["related_in"] = [{"id": e["source_id"], "kind": e["kind"]} for e in edges_in]
    print(json.dumps(result, indent=2, default=str))


def neighbors(db_path: Path, record_id: str, depth: int = 2):
    """BFS neighborhood of a record — mirrors ep_graph_traverse."""
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    visited = {record_id}
    queue = [(record_id, 0)]
    results = []

    while queue:
        current, d = queue.pop(0)
        if d >= depth:
            continue
        for edge in conn.execute(
            "SELECT target_id, kind FROM edges WHERE source_id=?", (current,)
        ).fetchall():
            nid = edge["target_id"]
            if nid not in visited:
                visited.add(nid)
                row = conn.execute(
                    "SELECT label, type FROM records WHERE id=?", (nid,)
                ).fetchone()
                results.append({
                    "id": nid,
                    "label": row["label"] if row else None,
                    "type": row["type"] if row else None,
                    "kind": edge["kind"],
                    "depth": d + 1,
                })
                queue.append((nid, d + 1))

    conn.close()
    print(json.dumps({"start": record_id, "neighbors": results}, indent=2))


def fts_search(db_path: Path, query: str, limit: int = 10):
    """Full-text search over label + canonical_statement."""
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """SELECT r.id, r.label, r.type, r.canonical_statement,
                  snippet(records_fts, 2, '[', ']', '...', 20) AS snippet
           FROM records_fts
           JOIN records r ON r.id = records_fts.id
           WHERE records_fts MATCH ?
           ORDER BY rank
           LIMIT ?""",
        (query, limit),
    ).fetchall()
    conn.close()
    print(json.dumps([dict(r) for r in rows], indent=2))


def stats(db_path: Path):
    """Print database statistics."""
    conn = sqlite3.connect(str(db_path))
    n_records = conn.execute("SELECT COUNT(*) FROM records").fetchone()[0]
    n_edges = conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
    n_tags = conn.execute("SELECT COUNT(*) FROM tags").fetchone()[0]
    n_prov = conn.execute("SELECT COUNT(*) FROM provenance").fetchone()[0]
    n_with_valid_from = conn.execute(
        "SELECT COUNT(*) FROM provenance WHERE valid_from IS NOT NULL"
    ).fetchone()[0]
    by_type = conn.execute(
        "SELECT type, COUNT(*) as n FROM records GROUP BY type ORDER BY n DESC"
    ).fetchall()
    by_pack = conn.execute(
        "SELECT pack, COUNT(*) as n FROM records GROUP BY pack ORDER BY n DESC"
    ).fetchall()
    by_status = conn.execute(
        "SELECT lifecycle_status, COUNT(*) as n FROM records GROUP BY lifecycle_status"
    ).fetchall()
    conn.close()

    print(f"Database: {db_path}  ({db_path.stat().st_size:,} bytes)")
    print(f"Records:  {n_records}")
    print(f"Edges:    {n_edges}")
    print(f"Tags:     {n_tags}")
    print(f"Provenance rows: {n_prov}  (with valid_from: {n_with_valid_from})")
    print(f"\nBy type:")
    for row in by_type:
        print(f"  {row[0]:20s}  {row[1]}")
    print(f"\nBy pack:")
    for row in by_pack:
        print(f"  {row[0]:30s}  {row[1]}")
    print(f"\nBy lifecycle status:")
    for row in by_status:
        print(f"  {row[0]:15s}  {row[1]}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="ExpertPack SQLite triple store loader and query tool"
    )
    parser.add_argument("--input", default=None,
                        help="JSONL file to load (from ep-micro-record-export.py)")
    parser.add_argument("--db", required=True,
                        help="SQLite database path (created if not exists)")
    parser.add_argument("--lookup", default=None, metavar="ID",
                        help="Look up a single record by id")
    parser.add_argument("--neighbors", default=None, metavar="ID",
                        help="BFS neighbors of a record (depth 2)")
    parser.add_argument("--search", default=None, metavar="QUERY",
                        help="Full-text search over label + canonical_statement")
    parser.add_argument("--stats", action="store_true",
                        help="Print database statistics")
    parser.add_argument("--depth", type=int, default=2,
                        help="BFS depth for --neighbors (default 2)")
    parser.add_argument("--limit", type=int, default=10,
                        help="Result limit for --search (default 10)")
    args = parser.parse_args()

    db_path = Path(args.db)

    if args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: input file not found: {input_path}")
            sys.exit(1)
        print(f"Loading {input_path} → {db_path}...")
        s = load_jsonl(input_path, db_path)
        print(f"Loaded: {s['records']} records, {s['edges']} edges, {s['tags']} tags")
        if s['skipped']:
            print(f"Skipped: {s['skipped']}")
        print(f"DB size: {s['db_bytes']:,} bytes")

    if not db_path.exists():
        print(f"Error: database not found: {db_path}")
        sys.exit(1)

    if args.lookup:
        lookup(db_path, args.lookup)
    if args.neighbors:
        neighbors(db_path, args.neighbors, depth=args.depth)
    if args.search:
        fts_search(db_path, args.search, limit=args.limit)
    if args.stats:
        stats(db_path)


if __name__ == "__main__":
    main()
