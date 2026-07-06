#!/usr/bin/env python3
"""Pack ingestion gate: validate -> strip -> export, aborting on any failure.

Nothing should enter a retrieval index or AKS pipeline unless it first passes
the --strict frontmatter contract. This script enforces that ordering:

  1. ep-validate --strict   (abort if the pack does not conform)
  2. ep-strip-frontmatter   (produce a clean, index-ready copy)
  3. ep-micro-record-export (compact AKS JSONL, also --strict)

Usage:
    python tools/ingest-gate.py packs/blender-3d
    python tools/ingest-gate.py packs/blender-3d --ignore W-V41-01
    python tools/ingest-gate.py packs/blender-3d --out build/blender-3d --export build/blender-3d.jsonl
"""

import argparse
import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VALIDATOR = os.path.join(REPO_ROOT, 'tools', 'validator', 'ep-validate.py')
STRIPPER = os.path.join(REPO_ROOT, 'tools', 'deploy-prep', 'ep-strip-frontmatter.py')
EXPORTER = os.path.join(REPO_ROOT, 'tools', 'micro-record-exporter', 'ep-micro-record-export.py')


def step(title, cmd):
    print(f"\n=== {title} ===")
    print("    " + " ".join(cmd))
    return subprocess.run(cmd).returncode


def main():
    parser = argparse.ArgumentParser(description='ExpertPack ingestion gate')
    parser.add_argument('pack', help='Path to the pack directory')
    parser.add_argument('--out', default=None,
                        help='Deploy output dir for the frontmatter-stripped copy '
                             '(default: build/<pack-name>-deploy)')
    parser.add_argument('--export', default=None,
                        help='AKS JSONL output path (default: build/<pack-name>.aks.jsonl)')
    parser.add_argument('--ignore', action='append', metavar='CODE', default=[],
                        help='Check codes to tolerate during validation (repeatable)')
    parser.add_argument('--skip-export', action='store_true',
                        help='Stop after validate + strip (do not run AKS export)')
    args = parser.parse_args()

    pack = os.path.abspath(args.pack)
    if not os.path.isdir(pack):
        print(f"ERROR: not a directory: {pack}", file=sys.stderr)
        return 1
    name = os.path.basename(pack.rstrip(os.sep))
    out = os.path.abspath(args.out or os.path.join(REPO_ROOT, 'build', f'{name}-deploy'))
    export = os.path.abspath(args.export or os.path.join(REPO_ROOT, 'build', f'{name}.aks.jsonl'))

    validate_cmd = [sys.executable, VALIDATOR, pack, '--strict']
    for code in args.ignore:
        validate_cmd += ['--ignore', code]
    if step('1/3 validate (--strict)', validate_cmd) != 0:
        print("\nGATE FAILED at validation. Pack not stripped or exported.", file=sys.stderr)
        return 1

    strip_cmd = [sys.executable, STRIPPER, '--src', pack, '--out', out, '--force']
    if step('2/3 strip frontmatter', strip_cmd) != 0:
        print("\nGATE FAILED at strip step.", file=sys.stderr)
        return 1

    if args.skip_export:
        print("\nGATE PASSED (export skipped).")
        return 0

    os.makedirs(os.path.dirname(export), exist_ok=True)
    export_cmd = [sys.executable, EXPORTER, '--pack', pack, '--compact', '--strict',
                  '--output', export]
    if step('3/3 AKS micro-record export (--strict)', export_cmd) != 0:
        print("\nGATE FAILED at export step.", file=sys.stderr)
        return 1

    print(f"\nGATE PASSED. Deploy copy: {out}\n            AKS JSONL:   {export}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
