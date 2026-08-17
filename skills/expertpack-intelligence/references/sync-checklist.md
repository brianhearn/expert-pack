# SDLC Sync Checklist (Step 5)

Align derived docs with axioms and the schema index. Prefer fixing the derived doc. Do not change `AXIOMS.md` unless the review found a real contradiction.

## Source of truth

| Topic | Source |
|-------|--------|
| Schema family + versions | `schemas/schema-index.yaml` |
| Filing rules | `schemas/core.md` + type schemas |
| Axioms | `AXIOMS.md` |
| Framework shape | `ARCHITECTURE.md` |
| Improvement backlog | `ROADMAP.md` |
| README schema table | Generated from the index via `python tools/update-schema-readme.py` |

## Checks

- [ ] `python tools/update-schema-readme.py --check` — README table matches the index
- [ ] `python tools/check-schema-projections.py` — skill projections do not teach retired patterns
- [ ] ROADMAP Vector 2 / eval examples do not recommend standalone summary layers (axiom 12)
- [ ] ROADMAP status log does not claim demo packs are still v3.x if manifests say `4.1`
- [ ] ROADMAP Vector 6 points at this skill + `logs/intelligence/` (not the retired weekly GPT-5 Mini cron as SoT)
- [ ] `ARCHITECTURE.md` tree lists current `guides/`, `tools/`, and `skills/`
- [ ] `README.md` repo tree lists `guides/intelligence-refinement.md` and `logs/intelligence/`
- [ ] Composite *pack* examples use `schema_version: "1.2"` (composite type version). `_graph.yaml` `schema_version` is the graph-export format version — do not silently retitle it as the EP family version
- [ ] Skill `SKILL.md` files point at current projections and do not name retired dirs as required
- [ ] CHANGELOG `[Unreleased]` mentions intelligence-refinement + projection guard if this cycle shipped them

## After fixes

Append what you changed to the run log under **Step 5**. If a checkbox on ROADMAP shipped or was retired, update it in the same commit.
