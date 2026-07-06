#!/usr/bin/env python3
"""Regenerate README.md's schema table from schemas/schema-index.yaml."""
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "schemas" / "schema-index.yaml"
README = ROOT / "README.md"
ORDER = [
    "core", "product", "person", "agent", "process", "composite", "eval",
    "registry_agent_knowledge", "registry_frontmatter", "registry_chunk_sidecar",
    "registry_typed_answer", "registry_ontology",
]


def label_for(key: str, file_path: str) -> str:
    path = Path(file_path)
    if key.startswith("registry_"):
        return f"registry/{path.name}"
    return path.name


def main() -> int:
    index = yaml.safe_load(INDEX.read_text(encoding="utf-8"))
    schemas = index["schemas"]
    rows = []
    for key in ORDER:
        item = schemas[key]
        file_path = item["file"]
        label = label_for(key, file_path)
        rows.append(f"| [{label}]({file_path}) | {item['version']} | {item['description']} |")

    table = "\n".join([
        "The canonical compatibility matrix lives in [`schemas/schema-index.yaml`](schemas/schema-index.yaml). Regenerate this table with `python3 tools/update-schema-readme.py` when schema versions change.",
        "",
        "| Schema | Version | What It Covers |",
        "|--------|---------|---------------|",
        *rows,
    ])

    text = README.read_text(encoding="utf-8")
    pattern = re.compile(r"(## Schemas\n\n).*?(\n\n---\n\n## Axioms)", re.S)
    new_text, count = pattern.subn(r"\1" + table + r"\2", text)
    if count != 1:
        raise SystemExit("Could not find README Schemas section")

    check = "--check" in sys.argv[1:]
    if check:
        if new_text != text:
            raise SystemExit("README schema table is out of sync; run tools/update-schema-readme.py")
        return 0

    README.write_text(new_text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
