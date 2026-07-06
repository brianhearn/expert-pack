#!/usr/bin/env python3
"""Validate every pack in the repository against the --strict contract.

Runs `ep-validate --strict` on the template (which must be pristine) and on each
pack under packs/. Used by CI and the pre-commit hook so a single command gates
the whole repo on Windows and Linux alike.

Usage:
    python tools/validate-all.py
    python tools/validate-all.py --ignore W-V41-01      # tolerate a tracked backlog
    python tools/validate-all.py --fail-on-warn         # also fail on warnings

The template is always validated with no --ignore codes; --ignore applies to the
packs/ demo packs, which carry an oversized-concept backlog awaiting the
atomic-split sprint.
"""

import argparse
import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VALIDATOR = os.path.join(REPO_ROOT, 'tools', 'validator', 'ep-validate.py')


def discover_packs():
    packs_dir = os.path.join(REPO_ROOT, 'packs')
    if not os.path.isdir(packs_dir):
        return []
    out = []
    for name in sorted(os.listdir(packs_dir)):
        pack = os.path.join(packs_dir, name)
        if os.path.isdir(pack) and os.path.exists(os.path.join(pack, 'manifest.yaml')):
            out.append(pack)
    return out


def run(target, extra):
    cmd = [sys.executable, VALIDATOR, target, '--strict'] + extra
    print(f"\n>>> {' '.join(os.path.relpath(c, REPO_ROOT) if os.path.exists(c) else c for c in cmd[1:])}")
    return subprocess.run(cmd).returncode


def main():
    parser = argparse.ArgumentParser(description='Validate all ExpertPacks (--strict)')
    parser.add_argument('--ignore', action='append', metavar='CODE', default=[],
                        help='Check codes to tolerate on packs/ (repeatable)')
    parser.add_argument('--fail-on-warn', action='store_true',
                        help='Also fail if any warning remains')
    args = parser.parse_args()

    common = []
    if args.fail_on_warn:
        common.append('--fail-on-warn')

    targets = []
    template = os.path.join(REPO_ROOT, 'template')
    if os.path.exists(os.path.join(template, 'manifest.yaml')):
        targets.append((template, common))  # template: no --ignore, must be clean
    pack_extra = common + [f'--ignore={c}' for c in args.ignore]
    for pack in discover_packs():
        targets.append((pack, pack_extra))

    if not targets:
        print("No packs or template found to validate.")
        return 1

    failures = []
    for target, extra in targets:
        if run(target, extra) != 0:
            failures.append(os.path.relpath(target, REPO_ROOT))

    print("\n" + "=" * 60)
    if failures:
        print(f"FAILED: {len(failures)} target(s) did not pass --strict:")
        for f in failures:
            print(f"  - {f}")
        print("=" * 60)
        return 1
    print(f"OK: all {len(targets)} target(s) pass --strict")
    print("=" * 60)
    return 0


if __name__ == '__main__':
    sys.exit(main())
