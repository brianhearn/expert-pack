# ExpertPack Validator & Doctor

Two companion tools for validating and auto-fixing ExpertPack files.

## ep-validate.py

Runs structural, retrieval, provenance, and optional AKS export-readiness checks across a pack and reports errors and warnings.

```bash
python3 ep-validate.py /path/to/your-pack
python3 ep-validate.py /path/to/your-pack --verbose
python3 ep-validate.py /path/to/your-pack --json
python3 ep-validate.py /path/to/your-pack --provenance
python3 ep-validate.py /path/to/your-pack --aks
```

### Checks

| # | Check | Level |
|---|-------|-------|
| 1 | `manifest.yaml` exists and has required fields | ERROR |
| 2 | `manifest.yaml` slug format | WARN |
| 3 | Entry point file exists | ERROR |
| 4 | `_index.md` present in each content directory | WARN |
| 5 | File size (default: warn >50KB) | WARN |
| 6 | Frontmatter present | WARN |
| 7 | Required frontmatter fields (`type`, `pack`, `tags`) | WARN |
| 8 | `type` matches directory convention | ERROR |
| 9 | Duplicate basenames (vault-wide uniqueness) | ERROR |
| 10 | Verbatim↔summary cross-links (bidirectionality) | ERROR/WARN |
| 11 | Broken `[[wikilinks]]` | ERROR |
| 12 | Markdown links that should be wikilinks | WARN |
| 13 | Orphaned files (no related: and no incoming links) | WARN |
| 14 | Composite sub-pack references | ERROR |
| 15 | Missing frontmatter fields (title, retrieval_strategy) | WARN |
| 16 | Stale paths in related: frontmatter | ERROR |

**Standing rule:** A pack must pass with **0 errors** before committing.

### Provenance and AKS readiness

Use `--provenance` to check stable citation/freshness fields (`id`, `verified_at`, `content_hash`). Use `--aks` when a pack needs to produce complete compact Agent Knowledge Schema JSONL for retrieval pipelines. `--aks` implies provenance checks and adds:

| Check | Meaning |
|-------|---------|
| `W-AKS-01` | File will be skipped by AKS export because it lacks stable `id` |
| `W-AKS-02` | AKS row will lack `verified_at` freshness metadata |
| `W-AKS-03` | Exporter can compute `content_hash`, but no stored frontmatter hash exists for drift detection |
| `W-AKS-04` | Exporter has weak `canonical_statement` fallback; add lead summary or opening prose |

## ep-doctor.py

Auto-fixes mechanical issues found by the validator.

```bash
# Dry run (safe — shows what would change)
python3 ep-doctor.py /path/to/your-pack

# Apply fixes
python3 ep-doctor.py /path/to/your-pack --apply

# Scope to specific fix types
python3 ep-doctor.py /path/to/your-pack --fix wikilinks
python3 ep-doctor.py /path/to/your-pack --fix reverse-related --apply
```

### Fix Operations

| Fix | What it does |
|-----|-------------|
| `wikilinks` | Converts `[text](file.md)` → `[[file\|text]]` |
| `reverse-related` | Adds missing bidirectional `related:` frontmatter entries |
| `frontmatter` | Adds missing required frontmatter fields |
| `orphan-links` | Removes stale paths from `related:` |
| `index` | Creates missing `_index.md` stubs |
| `prefixes` | Renames files to match content-type prefix convention |

## Workflow

```bash
# 1. Validate first
python3 ep-validate.py /path/to/pack

# 2. Dry-run doctor to preview fixes
python3 ep-doctor.py /path/to/pack

# 3. Apply
python3 ep-doctor.py /path/to/pack --apply

# 4. Validate again — must be 0 errors before committing
python3 ep-validate.py /path/to/pack
```

## Requirements

- Python 3.8+
- `pyyaml` (`pip install pyyaml`)
