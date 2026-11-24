#!/usr/bin/env python3
"""Packaging helper so `expertpack-cli` builds a self-contained wheel (bundling tools/ and template/)."""

from pathlib import Path
from setuptools import setup


def _collect_data_files(base_dirs: list[str]) -> list[tuple[str, list[str]]]:
    root = Path(__file__).resolve().parent
    skip = {"__pycache__", ".git", ".ep-mcp", "node_modules"}
    grouped: dict[str, list[str]] = {}
    for top in base_dirs:
        base = root / top
        if not base.exists():
            continue
        for fp in sorted(base.rglob("*")):
            if not fp.is_file():
                continue
            rel = fp.relative_to(root)
            if any(part in skip for part in rel.parts) or fp.suffix == ".pyc":
                continue
            target_dir = (Path("share") / "expertpack" / rel.parent).as_posix()
            grouped.setdefault(target_dir, []).append(rel.as_posix())
    return sorted(grouped.items())


setup(
    data_files=_collect_data_files(["tools", "template", "schemas/registry"]),
)
