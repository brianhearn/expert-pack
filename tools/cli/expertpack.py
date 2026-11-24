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
    """Locate the directory containing tools/ and template/ (repo checkout or wheel install)."""
    p = start
    for _ in range(6):
        if (p / "tools" / "validator" / "ep-validate.py").exists():
            return p
        p = p.parent
    # Wheel / site-packages install via share/expertpack
    for prefix in (Path(sys.prefix), Path(sys.base_prefix)):
        candidate = prefix / "share" / "expertpack"
        if (candidate / "tools" / "validator" / "ep-validate.py").exists():
            return candidate
    return start


REPO_ROOT = find_repo_root(Path(__file__).resolve().parent)
TOOLS = REPO_ROOT / "tools"
VALIDATE = TOOLS / "validator" / "ep-validate.py"
DOCTOR = TOOLS / "validator" / "ep-doctor.py"
CHUNK = TOOLS / "chunker" / "ep-chunk-annotate.py"
MIGRATE_V4 = TOOLS / "migrate" / "ep-migrate-3-to-4.py"
SKILL_EXPORT = TOOLS / "skill-export" / "ep-skill-export.py"
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

def _write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def _copy_shared_root(dest: Path, slug: str, name: str, today: str) -> None:
    """Copy shared root scaffolding (.obsidian, overview, DESIGN, TOOLS, eval) from template/."""
    dest.mkdir(parents=True, exist_ok=True)
    obs = TEMPLATE / ".obsidian"
    if obs.is_dir():
        shutil.copytree(obs, dest / ".obsidian", dirs_exist_ok=True)
    for rel in ("overview.md", "DESIGN.md", "TOOLS.md", "eval/benchmark.yaml"):
        src = TEMPLATE / rel
        if src.is_file():
            dst = dest / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            txt = src.read_text(encoding="utf-8")
            txt = txt.replace("your-pack-slug", slug).replace("Your Pack Name", name).replace("YYYY-MM-DD", today)
            _write_md(dst, txt)


def _scaffold_person(dest: Path, slug: str, name: str, today: str) -> None:
    _copy_shared_root(dest, slug, name, today)
    manifest = f"""name: "{name}"
slug: "{slug}"
type: "person"
version: "1.0.0"
schema_version: "4.1"
description: "Person ExpertPack capturing {name}'s stories, perspectives, relationships, and voice."
entry_point: "overview.md"
author: "Your Name"
created: "{today}"
updated: "{today}"
license: "CC-BY-4.0"

freshness:
  refresh_cycle: "P180D"
  last_full_review: "{today}"
  verified_file_count: 2
  total_file_count: 2
  coverage_pct: 100

{render_authority_boundary("person")}

context:
  always:
    - overview.md
  searchable:
    - stories/
    - opinions/
    - relationships/
    - mind/
  on_demand:
    - meta/
"""
    _write_md(dest / "manifest.yaml", manifest)
    for d, title in (
        ("stories", "Stories"),
        ("opinions", "Opinions"),
        ("relationships", "Relationships"),
        ("mind", "Mind & Mental Models"),
        ("meta", "Meta & Coverage"),
    ):
        _write_md(
            dest / d / "_index.md",
            f"---\ntitle: \"{title}\"\ntype: index\ntags: [index, {d}]\npack: {slug}\n"
            f"retrieval_strategy: navigation\nschema_version: \"4.1\"\nverified_at: \"{today}\"\n---\n\n"
            f"# {title}\n\nDirectory index for `{d}/`.\n",
        )
    _write_md(
        dest / "stories" / "story-example.md",
        f"---\ntitle: \"Example Story\"\ntype: story\ntags: [story, example]\npack: {slug}\n"
        f"retrieval_strategy: atomic\nschema_version: \"4.1\"\nverified_at: \"{today}\"\n---\n\n"
        "# Example Story\n\nReplace this starter atom with a real first-person story or formative experience.\n",
    )
    _write_md(
        dest / "meta" / "meta-source-coverage.md",
        f"---\ntitle: \"Source Coverage\"\ntype: reference\ntags: [meta, coverage]\npack: {slug}\n"
        f"retrieval_strategy: navigation\nschema_version: \"4.1\"\nverified_at: \"{today}\"\n---\n\n"
        "# Source Coverage\n\nTrack interviews, journals, and notes hydrated into this person pack.\n",
    )


def _scaffold_process(dest: Path, slug: str, name: str, today: str) -> None:
    _copy_shared_root(dest, slug, name, today)
    manifest = f"""name: "{name}"
slug: "{slug}"
type: "process"
version: "1.0.0"
schema_version: "4.1"
description: "Process ExpertPack documenting phases, decision frameworks, and practitioner gotchas for {name}."
entry_point: "overview.md"
author: "Your Name"
created: "{today}"
updated: "{today}"
license: "CC-BY-4.0"

domain: "general"
typical_duration: "TBD"
complexity: "medium"

freshness:
  refresh_cycle: "P90D"
  last_full_review: "{today}"
  verified_file_count: 2
  total_file_count: 2
  coverage_pct: 100

{render_authority_boundary("process")}

context:
  always:
    - overview.md
  searchable:
    - phases/
    - decisions/
    - gotchas/
  on_demand:
    - meta/
"""
    _write_md(dest / "manifest.yaml", manifest)
    for d, title in (
        ("phases", "Phases"),
        ("decisions", "Decisions"),
        ("gotchas", "Gotchas"),
        ("meta", "Meta & Coverage"),
    ):
        _write_md(
            dest / d / "_index.md",
            f"---\ntitle: \"{title}\"\ntype: index\ntags: [index, {d}]\npack: {slug}\n"
            f"retrieval_strategy: navigation\nschema_version: \"4.1\"\nverified_at: \"{today}\"\n---\n\n"
            f"# {title}\n\nDirectory index for `{d}/`.\n",
        )
    _write_md(
        dest / "phases" / "01-getting-started.md",
        f"---\ntitle: \"Phase 1: Getting Started\"\ntype: phase\ntags: [phase, planning]\npack: {slug}\n"
        f"retrieval_strategy: standard\nschema_version: \"4.1\"\nverified_at: \"{today}\"\n---\n\n"
        "# Phase 1: Getting Started\n\nDefine the goals, entry criteria, decision gates, and common pitfalls for Phase 1.\n",
    )
    _write_md(
        dest / "meta" / "source-coverage.md",
        f"---\ntitle: \"Source Coverage\"\ntype: reference\ntags: [meta, coverage]\npack: {slug}\n"
        f"retrieval_strategy: navigation\nschema_version: \"4.1\"\nverified_at: \"{today}\"\n---\n\n"
        "# Source Coverage\n\nTrack SOPs, practitioner interviews, and lessons learned hydrated into this pack.\n",
    )


def _scaffold_product(dest: Path, slug: str, name: str, today: str, force: bool) -> None:
    shutil.copytree(TEMPLATE, dest, dirs_exist_ok=force)
    for fp in dest.rglob("*"):
        if not fp.is_file() or fp.suffix.lower() not in {".md", ".yaml", ".yml"}:
            continue
        text = fp.read_text(encoding="utf-8")
        new = text.replace("your-pack-slug", slug)
        if fp.name == "manifest.yaml":
            new = new.replace('name: "Your Pack Name"', f'name: "{name}"')
            new = new.replace('type: "product"', 'type: "product"')
            new = new.replace("YYYY-MM-DD", today)
            new = AUTH_BLOCK_RE.sub(render_authority_boundary("product"), new, count=1)
        elif fp.suffix.lower() == ".md":
            new = re.sub(r'^verified_at:\s*["\']?\d{4}-\d{2}-\d{2}["\']?', f'verified_at: "{today}"', new, flags=re.M)
        if new != text:
            _write_md(fp, new)


def _scaffold_composite(dest: Path, slug: str, name: str, today: str, force: bool) -> None:
    _copy_shared_root(dest, slug, name, today)
    manifest = f"""name: "{name}"
slug: "{slug}"
type: "composite"
version: "1.0.0"
schema_version: "1.2"
description: "Composite ExpertPack combining constituent product and process packs for {name}."
entry_point: "overview.md"
author: "Your Name"
created: "{today}"
updated: "{today}"
license: "CC-BY-4.0"

packs:
  - path: "product"
    role: knowledge
  - path: "process"
    role: knowledge

{render_authority_boundary("composite")}

conflicts:
  priority: [product, process]
  strategy: "fail_closed"
  isolation:
    voice_must_not_assert_knowledge: true
    knowledge_must_not_override_voice: true
    respect_access_tiers: true
  tie_break: [authority_boundary, confidence, verified_at]

context:
  overrides:
    "product":
      always:
        - overview.md
    "process":
      always:
        - overview.md
"""
    _write_md(dest / "manifest.yaml", manifest)
    _scaffold_product(dest / "product", f"{slug}-product", f"{name} Reference", today, force)
    _scaffold_process(dest / "process", f"{slug}-process", f"{name} Process", today)


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

    name = args.name or slug.replace("-", " ").title()
    today = date.today().isoformat()

    if args.type == "product":
        _scaffold_product(dest, slug, name, today, args.force)
        doctor_targets = [dest]
    elif args.type == "person":
        _scaffold_person(dest, slug, name, today)
        doctor_targets = [dest]
    elif args.type == "process":
        _scaffold_process(dest, slug, name, today)
        doctor_targets = [dest]
    else:
        _scaffold_composite(dest, slug, name, today, args.force)
        doctor_targets = [dest / "product", dest / "process"]

    print(f"Scaffolded {name} ({args.type}) → {dest}")
    # Backfill provenance so the fresh pack passes --strict out of the box.
    for target in doctor_targets:
        run(DOCTOR, target, "--fix", "hash", "--apply")
    print("\nValidating scaffold...")
    rc = run(VALIDATE, dest, "--strict")
    if rc == 0:
        print(f"\nReady. Next: edit manifest.yaml + overview.md, then author content in {dest}")
    return rc


# ---------------------------------------------------------------------------
# validate / doctor / checksum / chunk-annotate
# ---------------------------------------------------------------------------

def cmd_validate(args) -> int:
    passthru = []
    if args.strict:
        passthru.append("--strict")
    if args.security:
        passthru.append("--security")
    if args.skillspector:
        passthru.append("--skillspector")
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
    if args.seal:
        passthru.append("--seal")
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


def cmd_export_skill(args) -> int:
    passthru = [args.pack]
    if args.outdir:
        passthru.append(args.outdir)
    if args.validate:
        passthru.append("--validate")
    if args.exact_dir:
        passthru.append("--exact-dir")
    if args.include_scripts:
        passthru.append("--include-scripts")
    if args.default_license:
        passthru += ["--license", args.default_license]
    if args.force:
        passthru.append("--force")
    return run(SKILL_EXPORT, *passthru)


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
    p_val.add_argument("--security", action="store_true",
                       help="Promote all security and signature warnings (W-SEC-01..04, W-INT-01..02) to ERROR")
    p_val.add_argument("--skillspector", action="store_true",
                       help="Run external NVIDIA SkillSpector scan if installed on PATH")
    p_val.add_argument("--fail-on-warn", action="store_true", help="Any warning fails the run")
    p_val.add_argument("--ignore", action="append", metavar="CODE",
                       help="Demote a check code to warning (repeatable, e.g. W-V41-01)")
    p_val.add_argument("--json", action="store_true", help="Emit JSON report")
    p_val.add_argument("--verbose", action="store_true")
    p_val.set_defaults(func=cmd_validate)

    p_doc = sub.add_parser("doctor", help="Run ep-doctor auto-fixer (dry-run by default)")
    p_doc.add_argument("path", nargs="?", default=".", help="Pack path (default: .)")
    p_doc.add_argument("--fix", choices=["links", "fm", "hash", "integrity", "prefix", "size", "all"],
                       default="all", help="Fix scope (default: all)")
    p_doc.add_argument("--seal", action="store_true",
                       help="Compute and write/update manifest.yaml integrity block")
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

    p_exp = sub.add_parser("export", help="Export an ExpertPack to external agent formats")
    exp_sub = p_exp.add_subparsers(dest="export_kind", required=True)
    p_skill = exp_sub.add_parser("skill", help="Export as a portable Agent Skill folder (SKILL.md)")
    p_skill.add_argument("pack", help="Path to ExpertPack (or skill folder with --validate)")
    p_skill.add_argument("outdir", nargs="?", help="Output directory (creates <outdir>/<slug>/)")
    p_skill.add_argument("--validate", action="store_true", help="Validate an existing SKILL.md folder")
    p_skill.add_argument("--exact-dir", action="store_true", help="Write directly into outdir")
    p_skill.add_argument("--include-scripts", action="store_true", help="Allow executable scripts in assets/")
    p_skill.add_argument("--license", dest="default_license", default=None, help="Fallback SPDX license")
    p_skill.add_argument("--force", action="store_true", help="Overwrite existing output directory")
    p_skill.set_defaults(func=cmd_export_skill)

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
