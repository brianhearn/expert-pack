#!/usr/bin/env python3
"""Fail if context-loaded schema projections teach retired patterns as current.

Canonical schemas may document history. These skill projections are what agents
load first — they must teach v4.1 only.

Usage:
    python tools/check-schema-projections.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PROJECTIONS = [
    ROOT / "skills" / "expertpack" / "references" / "schemas.md",
    ROOT / "skills" / "expertpack" / "references" / "schemas-product.md",
    ROOT / "skills" / "expertpack" / "references" / "schemas-person.md",
    ROOT / "skills" / "expertpack" / "references" / "schemas-process.md",
    ROOT / "skills" / "expertpack" / "references" / "schemas-agent.md",
    ROOT / "skills" / "expertpack" / "references" / "schemas-composite.md",
    ROOT / "skills" / "expertpack-export" / "references" / "schemas-summary.md",
]

# Patterns that mean "this is the current contract" when they appear in a projection.
RULES = [
    (
        "relations.yaml",
        re.compile(r"relations\.yaml"),
        "graph projection is _graph.yaml + ontology.yaml, not relations.yaml",
    ),
    (
        "retrieval.strategy",
        re.compile(r"(?<![A-Za-z_])retrieval\.strategy"),
        "use flat retrieval_strategy, not nested retrieval.strategy",
    ),
    (
        "summaries/",
        re.compile(r"summaries/"),
        "summaries/ is not a live v4.1 directory",
    ),
    (
        "propositions/",
        re.compile(r"propositions/"),
        "propositions/ is not a live v4.1 directory",
    ),
    (
        "sectioned",
        re.compile(r"\bsectioned\b"),
        "v4.1 strategies are standard | atomic | navigation, not sectioned",
    ),
]


def main() -> int:
    errors: list[str] = []
    missing = [p for p in PROJECTIONS if not p.is_file()]
    for path in missing:
        errors.append(f"missing projection: {path.relative_to(ROOT)}")

    for path in PROJECTIONS:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()
        for label, pattern, why in RULES:
            if pattern.search(text):
                errors.append(f"{rel}: teaches retired pattern {label!r} ({why})")

    if errors:
        print("Schema projection check failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"OK: {len(PROJECTIONS)} schema projections teach current v4.1 patterns")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
