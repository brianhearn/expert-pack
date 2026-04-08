---
name: expertpack
description: "Work with ExpertPacks — structured knowledge packs for AI agents. Obsidian-compatible: every pack is a valid Obsidian vault with Dataview support. Use when: (1) Loading/consuming an ExpertPack as agent context, (2) Creating or hydrating a new ExpertPack from scratch, (3) Configuring RAG for a pack, (4) Validating or fixing a pack with the CLI tools, (5) Opening or authoring a pack in Obsidian. Triggers on: 'expertpack', 'expert pack', 'esoteric knowledge', 'knowledge pack', 'pack hydration', 'validate pack', 'ep-validate', 'ep-doctor', 'obsidian vault', 'obsidian pack'. For EK ratio measurement and quality evals install expertpack-eval. For exporting an OpenClaw agent as an ExpertPack install expertpack-export. For converting an existing Obsidian Vault into an ExpertPack install obsidian-to-expertpack."
metadata:
  openclaw:
    homepage: https://expertpack.ai
---

# ExpertPack

Structured knowledge packs for AI agents. Maximize the knowledge your AI is missing.

**Learn more:** [expertpack.ai](https://expertpack.ai) · [GitHub](https://github.com/brianhearn/ExpertPack) · [Schema docs](https://expertpack.ai/#schemas) · [Obsidian compatible](https://expertpack.ai/#obsidian)

> **💎 Obsidian compatible:** Every ExpertPack is a valid Obsidian vault. Copy the `.obsidian/` folder from the repo root into any pack directory, open it in Obsidian, and install Dataview + Templater. You get live queries by content type, EK score, and tags; graph view; and full-text search. Standard relative Markdown links — packs render correctly on GitHub and in Obsidian simultaneously.

> **Companion skills:** This skill covers consumption and hydration guidance only. For EK measurement and quality evals use `expertpack-eval`. For exporting an OpenClaw agent's workspace as an ExpertPack use `expertpack-export`. For converting an existing Obsidian Vault into an agent-ready ExpertPack use `obsidian-to-expertpack`.

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

**OpenClaw RAG config** — add to `openclaw.json` to point the memory search engine at the pack directory:

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
3. Create root directory using the pack slug (kebab-case)
4. **Copy `.obsidian/` config into the pack root** — from the ExpertPack repo `template/` folder. This makes the pack immediately usable in Obsidian with Dataview and Templater pre-configured.
   ```bash
   cp -r /path/to/ExpertPack/template/.obsidian ./your-pack-slug/.obsidian
   ```
5. Create `manifest.yaml` and `overview.md` (both required)
6. Scaffold content directories per the type schema with `_index.md` in each
7. Populate content using EK-aware hydration:
   - Focus on esoteric knowledge — content the model cannot produce on its own
   - Full treatment for EK content; compressed scaffolding for general knowledge
   - Skip content with zero EK value
8. Add retrieval layers: `summaries/`, `propositions/`, `glossary.md`, lead summaries in content files
9. Add `sources/_coverage.md` documenting what was researched

For full hydration methodology and source prioritization: read `{skill_dir}/references/hydration.md`.

### 3. Configure RAG

Point OpenClaw RAG at the pack directory using the config snippet above. Files are authored at 400–800 tokens each — retrieval-ready by design, no external chunking tool needed.

### 4. Measure EK Ratio & Run Quality Evals

Install the companion skill — it handles all LLM API calls for blind probing and eval scoring:

```
clawhub install expertpack-eval
```

### 5. Validate & Fix a Pack

Run the CLI validator to check compliance (16 checks covering manifest, frontmatter, wikilinks, cross-links, file prefixes, orphans, and file size):

```bash
python3 /path/to/ExpertPack/tools/validator/ep-validate.py /path/to/pack [--verbose] [--json]
```

**Must pass with 0 errors before committing.** Warnings are advisory.

Auto-fix common issues with the doctor (dry-run by default):

```bash
# Dry-run — see what would change
python3 /path/to/ExpertPack/tools/validator/ep-doctor.py /path/to/pack

# Apply all fixes
python3 /path/to/ExpertPack/tools/validator/ep-doctor.py /path/to/pack --apply

# Apply specific fix category: links | fm | prefix
python3 /path/to/ExpertPack/tools/validator/ep-doctor.py /path/to/pack --fix links --apply
```

Fix operations:
- **links** — convert path-based `related:` to bare filenames, markdown links → wikilinks, add missing verbatim↔summary cross-links, enforce bidirectional `related:`
- **fm** — add missing frontmatter fields (title, type, tags, pack), fix `canonical_verbatim` paths
- **prefix** — rename files to content-type prefixes for vault-wide uniqueness (`sum-`, `vbt-`, `facts-`, `meta-`, `mind-`, `prop-`, `rel-`, `pres-`)

Remove broken wikilinks pointing to non-existent files (safe for cross-sub-pack references in composites):

```bash
python3 /path/to/ExpertPack/tools/validator/ep-fix-broken-wikilinks.py /path/to/pack [--apply]
```

**Recommended workflow:** `ep-doctor --apply` → `ep-validate` → commit.

All tools are in `ExpertPack/tools/validator/` in the public repo.

### 6. Export an OpenClaw Agent as an ExpertPack

Install the companion skill — it handles workspace scanning, distillation, and packaging:

```
clawhub install expertpack-export
```
