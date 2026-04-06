---
name: expertpack
description: "Work with ExpertPacks — structured knowledge packs for AI agents. Obsidian-compatible: every pack is a valid Obsidian vault with Dataview support. Use when: (1) Loading/consuming an ExpertPack as agent context, (2) Creating or hydrating a new ExpertPack from scratch, (3) Configuring RAG for a pack, (4) Opening or authoring a pack in Obsidian. Triggers on: 'expertpack', 'expert pack', 'esoteric knowledge', 'knowledge pack', 'pack hydration', 'obsidian vault', 'obsidian pack'. For EK ratio measurement and quality evals install expertpack-eval. For exporting an OpenClaw agent as an ExpertPack install expertpack-export."
metadata:
  openclaw:
    homepage: https://expertpack.ai
    requires:
      bins:
        - python3
    data_access:
      - label: OpenClaw config (RAG setup)
        description: "The RAG configuration snippet modifies openclaw.json to point the memory search engine at pack directories. This is optional and user-initiated."
        scope: local
    external_services:
      - label: OpenRouter (via expertpack-eval companion)
        description: "EK ratio measurement and quality evals (in the separate expertpack-eval skill) send pack-derived content to LLM APIs via OpenRouter for blind probing. This skill itself makes NO external API calls."
        optional: true
        skill: expertpack-eval
---

# ExpertPack

Structured knowledge packs for AI agents. Maximize the knowledge your AI is missing.

**Learn more:** [expertpack.ai](https://expertpack.ai) · [GitHub](https://github.com/brianhearn/ExpertPack) · [Schema docs](https://expertpack.ai/#schemas) · [Obsidian compatible](https://expertpack.ai/#obsidian)

> **💎 Obsidian compatible:** Every ExpertPack is a valid Obsidian vault. Copy the `.obsidian/` folder from the repo root into any pack directory, open it in Obsidian, and install Dataview + Templater. You get live queries by content type, EK score, and tags; graph view; and full-text search. Standard relative Markdown links — packs render correctly on GitHub and in Obsidian simultaneously.

> **Companion skills:** This skill covers consumption, hydration, and RAG setup only. For EK measurement and quality evals use `expertpack-eval`. For exporting an OpenClaw agent's workspace as an ExpertPack use `expertpack-export`.

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

Install the companion skill:

```
clawhub install expertpack-eval
```

### 5. Export an OpenClaw Agent as an ExpertPack

Install the companion skill:

```
clawhub install expertpack-export
```
