# ExpertPack Schemas — filing rules

Projection of `schemas/core.md` (family 4.1). Canonical text wins if this file disagrees.

When the pack type is known, also read the matching file in this folder: `schemas-product.md`, `schemas-person.md`, `schemas-process.md`, `schemas-agent.md`, or `schemas-composite.md`. Full depth: repo `schemas/{type}.md`.

## Pack types

| Type | Use |
|------|-----|
| person | Human: stories, mind, relationships, voice |
| person + subtype agent | AI agent: operational identity, prescriptive mind |
| product | Concepts, workflows, interfaces, troubleshooting |
| process | Phases, decisions, checklists, gotchas |
| composite | Wires packs together with roles and conflict rules |

## Required root files

- `manifest.yaml` — type, version, `schema_version`, context tiers, recommended `authority_boundary` (`in_scope` / `out_of_scope` / `refuse_when`), optional `ek_ratio` / `mcp`
- `overview.md` — entry point; retriever-anchored opening paragraph

## Context tiers (`manifest.yaml`)

- **always** — every session. Keep total **<5KB** (identity, voice, navigation).
- **searchable** — RAG / `_index.md` (default for unlisted files).
- **on_demand** — verbatim, training, archives; explicit request only.

## File rules (retrieval-critical)

- **One topic = one file.** The retrieval unit is the file.
- Concept atoms: **400–800 tokens** target, **1,000-token hard ceiling**.
- Procedural files (workflows, phases) may be longer; retrieve them whole (`atomic`) or add a `.chunks.yaml` sidecar (RFC-004).
- kebab-case filenames; unique basenames vault-wide.
- Markdown is canonical. `_graph.yaml` + `ontology.yaml` are graph projections — not a second source of truth.
- Opening paragraph (1–3 sentences) **is** the summary and the embed anchor. No “this document describes.”
- `##` headers at natural breaks. Optional `## Frequently Asked` (each Q as `###`), `## Related Terms`, `## Related Concepts`.
- **Do not compact prose** to save tokens. Examples are reasoning scaffolding.
- **Do not create aggregator directories.** Per-concept FAQs live inside the atom. Optional `faq/` is cross-cutting questions only.

## Frontmatter (strict)

Required under `ep-validate --strict`: `title`, `type`, `tags`, `pack`, `id`, `schema_version`, `retrieval_strategy`, `verified_at`, `content_hash`.

```yaml
---
id: {pack-slug}/concepts/{slug}
title: "Concept Name"
type: concept
tags: [slug]
pack: {pack-slug}
retrieval_strategy: standard   # standard | atomic | navigation
schema_version: "4.1"
verified_at: "YYYY-MM-DD"
content_hash: ""
requires:                      # optional — auto-expanded at retrieval (depth 2, count 3)
  - prerequisite.md
related:                       # optional — soft; not auto-retrieved
  - sibling.md
---
```

`retrieval_strategy`:

| Value | Behavior |
|-------|----------|
| `standard` | Default. File is an indexable atom (concept-sized). |
| `atomic` | Retrieve the whole file. Workflows, phases, troubleshooting. |
| `navigation` | Excluded from the RAG pool (`_index.md`, coverage maps, hubs). |

## Volatile data

Time-bound EK lives in `volatile/` with frontmatter `refresh` / `source` / `fetched_at` / `expires_at`. Always searchable, never always-tier. Excluded from EK ratio (`ek_ratio.volatile_excluded: true`). Refresh is user-initiated.

## Key rules

- No secrets.
- Distill knowledge; do not copy raw state.
- Humans adjudicate contradictions (never overwrite).
- Reconstruct Mode (RFC-003) + TAC when `retrieval_mode: reconstruct`.

Full schemas: repo `schemas/` · https://github.com/brianhearn/expert-pack/tree/main/schemas
