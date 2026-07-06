---
name: expertpack
description: "Work with ExpertPacks — structured knowledge packs for AI agents. Obsidian-compatible: every pack is a valid Obsidian vault with Dataview support. Use when: (1) Loading/consuming an ExpertPack as agent context, (2) Creating or hydrating a new ExpertPack from scratch, (3) Configuring RAG for a pack, (4) Validating or fixing a pack with the CLI tools, (5) Opening or authoring a pack in Obsidian. Triggers on: 'expertpack', 'expert pack', 'esoteric knowledge', 'knowledge pack', 'pack hydration', 'validate pack', 'ep-validate', 'ep-doctor', 'obsidian vault', 'obsidian pack'. For EK ratio measurement and quality evals install expertpack-eval. For exporting an OpenClaw agent as an ExpertPack install expertpack-export. For converting an existing Obsidian Vault into an ExpertPack install obsidian-to-expertpack."
metadata:
  openclaw:
    homepage: https://expertpack.ai
---

# ExpertPack

Structured knowledge packs for AI agents. Maximize the knowledge your AI is missing.

**Learn more:** [expertpack.ai](https://expertpack.ai) · [GitHub](https://github.com/brianhearn/expert-pack) · [Schema docs](https://expertpack.ai/#schemas) · [Obsidian compatible](https://expertpack.ai/#obsidian)

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

To configure OpenClaw RAG, point `memorySearch.extraPaths` in `openclaw.json` at the pack directory. Files are authored at 400–800 tokens each — retrieval-ready by design. See `{skill_dir}/references/cli-commands.md` for the exact config snippet.

For detailed platform integration (Cursor, Claude Code, custom APIs, direct context window): read `{skill_dir}/references/consumption.md`.

> **Volatile files:** If a pack uses `volatile/` files with a `source` URL, staleness is checked at session start and the agent alerts you. Refresh is always **user-initiated** — no automatic background network fetches occur.

### 2. Create / Hydrate a Pack

1. Determine pack type: person, product, process, or composite
2. Read `{skill_dir}/references/schemas.md` for structural requirements
3. Create root directory using the pack slug (kebab-case)
4. **Copy `.obsidian/` config into the pack root** — from the `template/` folder in the public ExpertPack repo (github.com/brianhearn/expert-pack). This makes the pack immediately usable in Obsidian with Dataview and Templater pre-configured. See `{skill_dir}/references/cli-commands.md` for the copy command.
5. Create `manifest.yaml` and `overview.md` (both required)
6. Scaffold content directories per the type schema with `_index.md` in each
7. Populate content using EK-aware hydration:
   - Focus on esoteric knowledge — content the model cannot produce on its own
   - Full treatment for EK content; compressed scaffolding for general knowledge
   - Skip content with zero EK value
8. Structure each concept file as an atomic-conceptual unit (v4.1): retriever-anchored opening paragraph, body sections, optional `## Frequently Asked`, `## Related Terms`, `## Related Concepts`, and `requires:` dependencies where needed. Avoid `summaries/`/`propositions/`/per-domain `glossary-*.md` aggregator directories.
9. Add `meta/source-coverage.md` documenting what was researched

For full hydration methodology and source prioritization: read `{skill_dir}/references/hydration.md`.

### 3. Configure RAG

Point OpenClaw RAG at the pack directory via `openclaw.json`. See `{skill_dir}/references/cli-commands.md` for the exact config snippet. No external chunking tool needed — files are authored at 400–800 tokens by design.

### 4. Measure EK Ratio & Run Quality Evals

Install the companion skill `expertpack-eval` via clawhub — it handles all LLM API calls for blind probing and eval scoring.

### 5. Validate & Fix a Pack

The ExpertPack repo (`tools/validator/` at github.com/brianhearn/expert-pack) includes local Python scripts for validation and auto-fix. They operate on local pack files only — no network calls, no external dependencies beyond Python stdlib.

- **ep-validate.py** — compliance validator (manifest, frontmatter, wikilinks, cross-links, file prefixes, orphans, file size, provenance, chunk sidecars). Add `--strict` to turn the frontmatter contract into a hard gate; must pass with 0 errors before committing.
- **ep-doctor.py** — auto-fixes common issues. Always run in dry-run mode first (default behavior); only add the apply flag after reviewing proposed changes. Fix categories: links (includes broken-wikilink removal, composite-safe), fm, hash (provenance backfill), prefix.

Recommended workflow: ep-doctor dry-run → ep-doctor apply → ep-validate → commit.

See `{skill_dir}/references/cli-commands.md` for exact command syntax.

### 6. Export an OpenClaw Agent as an ExpertPack

Install the companion skill `expertpack-export` via clawhub — it handles workspace scanning, distillation, and packaging.

### 7. Emit Typed Answers (TAC)

When retrieval runs in Reconstruct Mode (`retrieval_mode: reconstruct`, see RFC-003), agents MUST return a Typed Answer Contract (TAC) envelope instead of free prose. TAC forces every claim in an answer to map to a retrieved source fragment, so answers can be machine-verified rather than trusted blindly.

- Copy the prompt contract from `templates/TAC-PROMPT.md` into the agent's system prompt.
- The envelope schema lives in `schemas/registry/typed-answer.schema.json` (spec: `schemas/registry/typed-answer.spec.yaml`).
- Validate output structurally with `python tools/tac/validate_tac.py answer.json`; the eval `claim_verifier.py --tac` scores TAC envelopes against the pack.

In `standard` retrieval mode file-level citations suffice and TAC is optional; in `reconstruct` mode each source must carry a `fragment_id`.
