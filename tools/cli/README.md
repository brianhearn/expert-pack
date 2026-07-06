# expertpack — unified CLI

One entrypoint for the ExpertPack authoring tools. Each subcommand shells out to
the underlying script (`ep-validate`, `ep-doctor`, `ep-chunk-annotate`,
`convert.py`, `ep-migrate-3-to-4`), so behavior is identical to calling them
directly — you just don't have to remember where each one lives.

## Run it

```bash
python tools/cli/expertpack.py <command> [options]
```

Or install it as an `expertpack` command (editable, so it keeps calling the
in-repo tools):

```bash
pip install -e .        # from the repo root; requires pip >= 21.3
expertpack --help
```

## Commands

| Command | Wraps | Notes |
|---------|-------|-------|
| `expertpack init <slug> --type product\|person\|process` | `template/` copy + `ep-doctor` | Scaffolds a new pack, substitutes the manifest, backfills provenance, and validates. |
| `expertpack validate [path]` | `ep-validate` | Strict by default; `--no-strict`, `--ignore CODE`, `--fail-on-warn`, `--json`. |
| `expertpack doctor [path] --fix <scope> [--apply]` | `ep-doctor` | Dry-run unless `--apply`. |
| `expertpack checksum [path] [--apply]` | `ep-doctor --fix hash` | Backfills `content_hash` + provenance fields. |
| `expertpack chunk-annotate [path] [--apply\|--check]` | `ep-chunk-annotate` | Generates/verifies `.chunks.yaml` sidecars (RFC-004). |
| `expertpack migrate obsidian <vault> --output <dir>` | `convert.py` | Obsidian vault → pack. |
| `expertpack migrate v3-to-v4 <pack> --plan` | `ep-migrate-3-to-4` | Read-only migration plan. |

## Example: scaffold, author, ship

```bash
expertpack init acme-widgets --type product --name "Acme Widgets"
# ...author concepts/ ...
expertpack checksum acme-widgets --apply
expertpack validate acme-widgets
```
