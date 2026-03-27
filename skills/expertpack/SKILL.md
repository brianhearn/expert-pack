---
name: expertpack
description: "Work with ExpertPacks — structured knowledge packs for AI agents. Use when: (1) Loading/consuming an ExpertPack as agent context, (2) Creating or hydrating a new ExpertPack from scratch, (3) Chunking a pack for RAG deployment, (4) Backing up/exporting an OpenClaw agent's workspace into an ExpertPack. Triggers on: 'expertpack', 'expert pack', 'esoteric knowledge', 'knowledge pack', 'pack hydration', 'backup to expertpack', 'export agent knowledge'. For EK ratio measurement and quality evals, install the separate expertpack-eval skill."
metadata:
  openclaw:
    homepage: https://expertpack.ai
    requires:
      bins:
        - python3
---

# ExpertPack

Structured knowledge packs for AI agents. Maximize the knowledge your AI is missing.

**Learn more:** [expertpack.ai](https://expertpack.ai) · [GitHub](https://github.com/brianhearn/ExpertPack) · [Schema docs](https://expertpack.ai/#schemas)

**Full schemas:** `/path/to/ExpertPack/schemas/` in the repo (core.md, person.md, product.md, process.md, composite.md, eval.md)

## Pack Location

Default directory: `~/expertpacks/`. Check there first, fall back to current workspace. Users can override by specifying a path.

## Actions

### 1. Load / Consume a Pack

1. Read `manifest.yaml` — identify type, version, context tiers
2. Read `overview.md` — understand what the pack covers
3. Load all Tier 1 (always) files into session context
4. For queries: search Tier 2 (searchable) files via RAG or `_index.md` navigation
5. Load Tier 3 (on-demand) only on explicit request (verbatim transcripts, training data)

**OpenClaw RAG config** — add to `openclaw.json`:

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "extraPaths": ["path/to/pack"],
        "chunking": { "tokens": 500, "overlap": 0 },
        "query": {
          "hybrid": {
            "enabled": true,
            "mmr": { "enabled": true, "lambda": 0.7 },
            "temporalDecay": { "enabled": false }
          }
        }
      }
    }
  }
}
```

For detailed platform integration (Cursor, Claude Code, custom APIs, direct context window): read `{skill_dir}/references/consumption.md`.

### 2. Create / Hydrate a Pack

1. Determine pack type: person, product, process, or composite
2. Read `{skill_dir}/references/schemas.md` for structural requirements
3. Scaffold the directory structure per the type schema
4. Create `manifest.yaml` and `overview.md` (both required)
5. Populate content using EK-aware hydration:
   - Blind-probe each extracted fact before filing
   - Full treatment for EK content (the model can't produce it)
   - Compressed scaffolding for GK content (the model already knows it)
   - Skip content with zero EK value
6. Add retrieval layers: `_index.md` per directory, `summaries/`, `propositions/`, `glossary.md`
7. Add `sources/_coverage.md` documenting what was researched

For full hydration methodology, EK triage process, and source prioritization: read `{skill_dir}/references/hydration.md`.

### 3. Configure RAG

Point OpenClaw RAG at the pack directly. The 400–800 token file-size constraint makes files retrieval-ready by design — no external chunking tool needed.

### 4. Measure EK Ratio & Run Quality Evals

For EK ratio measurement (blind probing) and automated quality evals, install the companion skill:

```
clawhub install expertpack-eval
```

See `expertpack-eval` for full details on EK measurement, eval runner, and the improvement loop.

### 5. Backup / Export OpenClaw → ExpertPack

Export an OpenClaw agent's accumulated knowledge into a structured ExpertPack composite.

**Step 1 — Scan:**

```bash
python3 {skill_dir}/scripts/scan.py --workspace <workspace-path> --output /tmp/ep-scan.json
```

Review the scan output with the user. It proposes pack assignments (agent, person, product, process) with confidence scores. Flag ambiguous classifications for user decision.

**Step 2 — Distill** (repeat per pack):

```bash
python3 {skill_dir}/scripts/distill.py \
  --scan /tmp/ep-scan.json \
  --pack <type:slug> \
  --output <export-dir>/packs/<slug>/
```

- Distill, don't copy — target 10-20% volume of raw state
- Strips secrets automatically (API keys, tokens, passwords)
- Deduplicates, prefers newest for conflicts

**Step 3 — Compose:**

```bash
python3 {skill_dir}/scripts/compose.py \
  --scan /tmp/ep-scan.json \
  --export-dir <export-dir>/
```

Generates composite manifest and overview.

**Step 4 — Validate:**

```bash
python3 {skill_dir}/scripts/validate.py --export-dir <export-dir>/
```

Checks: required files exist, manifest fields valid, no secrets leaked, file sizes within guidelines, cross-references resolve.

**Step 5 — Review & ship.** Present validation report to user. They decide whether to commit/push.

**Critical rules:**
- Never include secrets in the export
- Never modify the live workspace — all output goes to the export directory
- Flag personal information for access tier review
- Default user-specific content to `private` access
