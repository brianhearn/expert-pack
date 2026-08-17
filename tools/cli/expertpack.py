#!/usr/bin/env python3
"""expertpack — one entrypoint for authoring, validating, and migrating packs.

Thin wrapper over the existing tools so a new user never has to remember which
script lives where. Each subcommand shells out to the underlying tool with
sys.executable, so behavior stays identical to calling the tool directly.

    expertpack init my-pack --type product
    expertpack validate packs/blender-3d --strict
    expertpack doctor packs/blender-3d --fix hash --apply
    expertpack checksum packs/blender-3d --apply
    expertpack chunk-annotate packs/blender-3d --check
    expertpack migrate obsidian ./vault --output ./my-pack
    expertpack migrate v3-to-v4 packs/blender-3d --plan

Run `python tools/cli/expertpack.py <command> --help` for per-command options.
Install as an `expertpack` command with `pip install -e .` from the repo root.
"""

import argparse
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

__version__ = "0.1.0"

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
AUTH_BLOCK_RE = re.compile(
    r"^authority_boundary:.*?^  no_source_no_claim: .+$",
    re.M | re.S,
)
AUTH_SCOPE = {
    "product": (
        "This product's documented concepts, workflows, interfaces, and troubleshooting.",
        [
            "Legal, medical, or financial advice",
            "Other products or vendors not covered by this pack",
        ],
    ),
    "person": (
        "This person's documented stories, opinions, relationships, and voice.",
        [
            "Medical, legal, or financial advice on their behalf",
            "Private facts not present in the pack",
            "Other people not covered by this pack",
        ],
    ),
    "process": (
        "This process's documented phases, decisions, checklists, and exceptions.",
        [
            "Legal or regulatory advice beyond the pack's regulations/",
            "Other processes not covered by this pack",
        ],
    ),
    "composite": (
        "Topics covered by the constituent packs listed in this composite.",
        [
            "Topics outside every constituent pack's authority_boundary",
            "Private or role-isolated facts the composite must not leak",
        ],
    ),
}


def render_authority_boundary(pack_type: str) -> str:
    in_scope, out_of_scope = AUTH_SCOPE[pack_type]
    lines = [
        "authority_boundary:",
        f'  in_scope: "{in_scope}"',
        "  out_of_scope:",
    ]
    for item in out_of_scope:
        lines.append(f'    - "{item}"')
    lines += [
        "  refuse_when:",
        '    - "No supporting atom in the pack"',
        '    - "Question is outside in_scope"',
        "  no_source_no_claim: false",
    ]
    return "\n".join(lines)


def find_repo_root(start: Path) -> Path:
    """Walk up until we find the tools/ layout, so the CLI works from anywhere."""
    p = start
    for _ in range(6):
        if (p / "tools" / "validator" / "ep-validate.py").exists():
            return p
        p = p.parent
    return start


REPO_ROOT = find_repo_root(Path(__file__).resolve().parent)
TOOLS = REPO_ROOT / "tools"
VALIDATE = TOOLS / "validator" / "ep-validate.py"
DOCTOR = TOOLS / "validator" / "ep-doctor.py"
CHUNK = TOOLS / "chunker" / "ep-chunk-annotate.py"
MIGRATE_V4 = TOOLS / "migrate" / "ep-migrate-3-to-4.py"
CONVERT = REPO_ROOT / "skills" / "obsidian-to-expertpack" / "scripts" / "convert.py"
TEMPLATE = REPO_ROOT / "template"


def run(script: Path, *args) -> int:
    """Invoke a sibling tool with the current interpreter; return its exit code."""
    if not script.exists():
        print(f"error: tool not found: {script}", file=sys.stderr)
        return 2
    return subprocess.call([sys.executable, str(script), *(str(a) for a in args)])


# ---------------------------------------------------------------------------
# init
# ---------------------------------------------------------------------------

def cmd_init(args) -> int:
    slug = args.slug
    if not SLUG_RE.match(slug):
        print(f"error: slug must be kebab-case (got '{slug}')", file=sys.stderr)
        return 2

    dest = Path(args.output).resolve() / slug
    if dest.exists() and not args.force:
        print(f"error: {dest} already exists (use --force to overwrite)", file=sys.stderr)
        return 2
    if not TEMPLATE.exists():
        print(f"error: template not found at {TEMPLATE}", file=sys.stderr)
        return 2

    shutil.copytree(TEMPLATE, dest, dirs_exist_ok=args.force)

    name = args.name or slug.replace("-", " ").title()
    today = date.today().isoformat()
    for fp in dest.rglob("*"):
        if not fp.is_file() or fp.suffix.lower() not in {".md", ".yaml", ".yml"}:
            continue
        text = fp.read_text(encoding="utf-8")
        new = text.replace("your-pack-slug", slug)
        if fp.name == "manifest.yaml":
            new = new.replace('name: "Your Pack Name"', f'name: "{name}"')
            new = new.replace('type: "product"', f'type: "{args.type}"')
            new = new.replace("YYYY-MM-DD", today)
            new = AUTH_BLOCK_RE.sub(render_authority_boundary(args.type), new, count=1)
        if new != text:
            with open(fp, "w", encoding="utf-8", newline="\n") as f:
                f.write(new)

    print(f"Scaffolded {name} → {dest}")
    # Backfill provenance so the fresh pack passes --strict out of the box.
    run(DOCTOR, dest, "--fix", "hash", "--apply")
    print("\nValidating scaffold...")
    rc = run(VALIDATE, dest, "--strict")
    if rc == 0:
        print(f"\nReady. Next: edit manifest.yaml + overview.md, then author concepts/ in {dest}")
    return rc


# ---------------------------------------------------------------------------
# validate / doctor / checksum / chunk-annotate
# ---------------------------------------------------------------------------

def cmd_validate(args) -> int:
    passthru = []
    if args.strict:
        passthru.append("--strict")
    if args.fail_on_warn:
        passthru.append("--fail-on-warn")
    if args.json:
        passthru.append("--json")
    if args.verbose:
        passthru.append("--verbose")
    for code in args.ignore or []:
        passthru += ["--ignore", code]
    return run(VALIDATE, args.path, *passthru)


def cmd_doctor(args) -> int:
    passthru = ["--fix", args.fix]
    if args.apply:
        passthru.append("--apply")
    return run(DOCTOR, args.path, *passthru)


def cmd_checksum(args) -> int:
    # content_hash + provenance backfill lives in ep-doctor's hash fixer.
    passthru = ["--fix", "hash"]
    if args.apply:
        passthru.append("--apply")
    return run(DOCTOR, args.path, *passthru)


def cmd_chunk_annotate(args) -> int:
    passthru = []
    if args.apply:
        passthru.append("--apply")
    if args.check:
        passthru.append("--check")
    if args.all:
        passthru.append("--all")
    if args.min_tokens is not None:
        passthru += ["--min-tokens", str(args.min_tokens)]
    return run(CHUNK, args.path, *passthru)


# ---------------------------------------------------------------------------
# migrate
# ---------------------------------------------------------------------------

def cmd_migrate_obsidian(args) -> int:
    passthru = [args.vault, "--output", args.output]
    if args.name:
        passthru += ["--name", args.name]
    if args.type:
        passthru += ["--type", args.type]
    if args.dry_run:
        passthru.append("--dry-run")
    return run(CONVERT, *passthru)


def cmd_migrate_v3(args) -> int:
    passthru = [args.pack, "--plan"]
    if args.verbose:
        passthru.append("--verbose")
    return run(MIGRATE_V4, *passthru)


# ---------------------------------------------------------------------------
# CLI wiring
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="expertpack", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--version", action="version", version=f"expertpack {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Scaffold a new pack from template/")
    p_init.add_argument("slug", help="Pack slug (kebab-case)")
    p_init.add_argument("--type", choices=["product", "person", "process", "composite"],
                        default="product", help="Pack type (default: product)")
    p_init.add_argument("--name", help="Human-readable pack name (default: title-cased slug)")
    p_init.add_argument("--output", default=".", help="Parent directory for the new pack (default: .)")
    p_init.add_argument("--force", action="store_true", help="Overwrite if the target exists")
    p_init.set_defaults(func=cmd_init)

    p_val = sub.add_parser("validate", help="Run ep-validate (strict by default)")
    p_val.add_argument("path", nargs="?", default=".", help="Pack path (default: .)")
    p_val.add_argument("--strict", action=argparse.BooleanOptionalAction, default=True,
                       help="Enforce the hard frontmatter gate (default: on)")
    p_val.add_argument("--fail-on-warn", action="store_true", help="Any warning fails the run")
    p_val.add_argument("--ignore", action="append", metavar="CODE",
                       help="Demote a check code to warning (repeatable, e.g. W-V41-01)")
    p_val.add_argument("--json", action="store_true", help="Emit JSON report")
    p_val.add_argument("--verbose", action="store_true")
    p_val.set_defaults(func=cmd_validate)

    p_doc = sub.add_parser("doctor", help="Run ep-doctor auto-fixer (dry-run by default)")
    p_doc.add_argument("path", nargs="?", default=".", help="Pack path (default: .)")
    p_doc.add_argument("--fix", choices=["links", "fm", "hash", "prefix", "size", "all"],
                       default="all", help="Fix scope (default: all)")
    p_doc.add_argument("--apply", action="store_true", help="Write changes (omit for dry-run)")
    p_doc.set_defaults(func=cmd_doctor)

    p_sum = sub.add_parser("checksum", help="Backfill content_hash + provenance (dry-run by default)")
    p_sum.add_argument("path", nargs="?", default=".", help="Pack path (default: .)")
    p_sum.add_argument("--apply", action="store_true", help="Write changes (omit for dry-run)")
    p_sum.set_defaults(func=cmd_checksum)

    p_chunk = sub.add_parser("chunk-annotate", help="Generate/check chunk sidecars (RFC-004)")
    p_chunk.add_argument("path", nargs="?", default=".", help="File or pack path (default: .)")
    p_chunk.add_argument("--apply", action="store_true", help="Write sidecars")
    p_chunk.add_argument("--check", action="store_true", help="CI mode: fail on drift")
    p_chunk.add_argument("--all", action="store_true", help="Annotate all eligible files, not just oversized")
    p_chunk.add_argument("--min-tokens", type=int, default=None, help="Minimum tokens to chunk")
    p_chunk.set_defaults(func=cmd_chunk_annotate)

    p_mig = sub.add_parser("migrate", help="Migrate content into ExpertPack format")
    mig_sub = p_mig.add_subparsers(dest="migrate_kind", required=True)

    p_obs = mig_sub.add_parser("obsidian", help="Convert an Obsidian vault to a pack")
    p_obs.add_argument("vault", help="Path to the source Obsidian vault")
    p_obs.add_argument("--output", required=True, help="Output directory for the pack")
    p_obs.add_argument("--name", help="Pack name (default: vault folder name)")
    p_obs.add_argument("--type", choices=["auto", "person", "product", "process", "composite"],
                       help="Pack type (default: auto-detect)")
    p_obs.add_argument("--dry-run", action="store_true", help="Preview without writing")
    p_obs.set_defaults(func=cmd_migrate_obsidian)

    p_v3 = mig_sub.add_parser("v3-to-v4", help="Plan a Schema v3 → v4 migration")
    p_v3.add_argument("pack", help="Path to the pack root")
    p_v3.add_argument("--plan", action="store_true", default=True, help="Read-only plan (default)")
    p_v3.add_argument("--verbose", action="store_true")
    p_v3.set_defaults(func=cmd_migrate_v3)

    return parser


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
