# Context-Schema Protocol (Step 3)

Improve schemas that are **loaded into AI context**. Do not compact canonical `schemas/*.md`.

## Inventory

| Surface | Role | Rule |
|---------|------|------|
| `skills/expertpack/SKILL.md` | Points at projections | Keep the pointer thin |
| `skills/expertpack/references/schemas.md` | Always-loaded filing rules | Retrieval-critical rules only |
| `skills/expertpack/references/schemas-*.md` | Type trees | Load only when pack type is known |
| `skills/expertpack-export/references/schemas-summary.md` | Export filing rules | Current v4.1; no retired dirs |
| `schemas/*.md` | On-demand filing guide | Canonical; do not shorten |

## Method

1. **Progressive disclosure, not compression.** Always-loaded layer = filing rules that protect retrieval. Type trees and examples load when the pack type is known.
2. **Single source of truth.** Canonical text stays in `schemas/`. Skill files are projections. When they disagree, fix the projection.
3. **Keep the words that retrieve.** Do not densify: opening-paragraph rules, `## Frequently Asked`, `requires:` semantics, anti-compaction, anti-aggregator, size ceilings, `retrieval_strategy` enum.
4. **Guardrail.** After edits, run:

```bash
python tools/check-schema-projections.py
```

The checker fails if designated projections teach retired patterns as current: `relations.yaml` as the graph, nested `retrieval.strategy` as the primary key, `summaries/` / `propositions/` as live dirs, `sectioned` as a v4.1 strategy.

## Always-loaded contract (must remain in `schemas.md`)

- One topic = one file; 400–800 token target; 1,000-token concept ceiling
- Opening paragraph is the embed anchor (no “this document describes”)
- `retrieval_strategy`: `standard` \| `atomic` \| `navigation`
- `requires:` (auto-expand) vs `related:` (soft)
- No aggregator dirs; no prose compaction
- Strict required frontmatter: `title`, `type`, `tags`, `pack`, `id`, `schema_version`, `retrieval_strategy`, `verified_at`, `content_hash`
- Context tiers: always / searchable / on_demand; Tier 1 budget <5KB
- Markdown canonical; `_graph.yaml` + `ontology.yaml` for graph (not `relations.yaml`)

## Do not

- Rewrite `schemas/core.md` (or other canonical type schemas) to use fewer words
- Split atoms that are not independently retrievable
- Reintroduce `summaries/`, `propositions/`, per-domain `glossary-*.md`, or standalone FAQ hubs as required structure
- Leave a second authoring surface that can drift (if you teach a rule in a projection, it must match core)
