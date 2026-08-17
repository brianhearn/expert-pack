# Session Handoff — 2026-08-17 (afternoon)

*Context for the next agent. Do not edit `.cursor/plans/intelligence_refinement_52705987.plan.md`.*

---

## Git state (after this wrap-up)

| Item | Value |
|------|--------|
| **Branch** | `main` |
| **Prior commit** | `8c5c627` — intelligence refinement + authority + composite 1.2 |
| **This commit** | Public-pack contract + concept-split sprint; CI drops `--ignore W-V41-01` |
| **Do not commit** | `expert-pack.code-workspace` (local IDE only) |
| **Deploy** | **Not done** — do not deploy ep-mcp or reindex without an explicit user request |

---

## What landed this session (after `8c5c627`)

### C. Public demo packs to current contract

User: “check the three public EPs and bring them up to the latest.”

- `authority_boundary` on all seven manifests (blender + HA/solar composites and product/process packs).
- HA/solar composites: `schema_version: "1.2"`, `fail_closed`, isolation, `tie_break`. Glossaries removed from `context.always` (and from composite overrides).
- All 20 `_index.md` files: `retrieval_strategy: navigation`.
- Blender eval: 5 refusal questions. HA/solar: composite `eval/benchmark.yaml` stubs.
- `TOOLS.md` on each public pack root.
- `common-mistakes` atoms typed `gotcha`.
- Validator: `_index.md` and type-dir checks normalize to `/` so Windows stops false `missing-index`.

### D. Concept-split sprint

User: “concept-split sprint next.”

W-V41-01 uses **full file size ÷ 4** (frontmatter counts). Keep concept files **< ~3900 bytes**.

| Pack | Before | After |
|------|--------|-------|
| blender-3d concepts | 22 oversized hubs | 56 atoms (~330–975 tok) |
| HA product concepts | 12 hubs (some ~5k tok) | 78 atoms (~410–991 tok) |
| solar-diy product concepts | 3 hubs | 7 atoms |

Rules used: move sections, do not compact EK; no `*-part-2.md`; no aggregator leftovers; opening paragraph is the definition; `requires:` only when unintelligible without the other atom; `related:` for siblings. Old hub filenames deleted (`inverter-types.md`, `voice-assistant.md`, `python-bpy-api.md`, …).

`python tools/validate-all.py` (no ignore) is **0 errors** on template + three public packs. CI and pre-commit no longer pass `--ignore W-V41-01`.

---

## Earlier this calendar day (already on `origin/main` as `8c5c627`)

Intelligence Refinement cycle 1 (2026-08-16) + EasyBot leftovers (authority boundary, composite conflict resolver). See that commit and `logs/intelligence/2026-08-16.md` / `2026-08-17.md`.

Cycle 1 applied all six top-3s (R1–R3, S1–S3). EP MCP still must prepend `context_prefix` and honor the consume loop.

---

## Key design decisions (carry forward)

1. **Schema family stays 4.1** unless the user asks for 4.2.
2. **Do not compact canonical `schemas/*.md`.** Shrink context via type-gated projections.
3. **Axioms 11–13.** One topic = one file. No standalone summaries. Retrieval-first vs LLM-reads-all must match.
4. **Pack + consumer contract** over standing EP MCP back up as the destination. Runtime stays in [ep-mcp](https://github.com/brianhearn/ep-mcp).
5. **Concept ceiling is 1,000 tokens** measured as `filesize/4`. Do not dodge with `retrieval_strategy: atomic` on concepts that should split.
6. **`W-AUTH-*`, `W-EVAL-01`, `W-TIER-*`, `W-GRAPH-01` stay WARN** — not in `STRICT_PROMOTE`.
7. **Public packs are now hydrated** to the current contract. Further demo edits are fine when the user asks (related: backlinks, glossary/FAQ size).
8. **Do not edit the Intelligence Refinement plan file.**
9. **Do not deploy without an explicit user request.**
10. **`init --type person|process|composite` still copies the product-shaped `template/`.** Person init can fail `--strict` on `meta/source-coverage.md`.
11. **PowerShell:** `&&` is not a statement separator on older Windows PowerShell. Use `;`.
12. **`refusal` ≡ `out-of-scope`** for eval scoring.
13. **Cyclic `requires:` (W-V41-05)** means the boundary is wrong — drop one direction (solar string inverter vs string-sizing: only sizing `requires` the inverter atom).

---

## Verification (Windows / PowerShell)

```powershell
cd C:\Users\BrianHearn\source\repos\expert-pack
python tools/validate-all.py
python tools/check-schema-projections.py
python tools/update-schema-readme.py --check
python tools/composite/test_conflict.py
python tools/chunker/ep-chunk-annotate.py packs/blender-3d --check --embedding-version gemini-embedding-001
```

Expected: all four targets **0 errors** under `--strict` with no ignore.

---

## Known backlog (not regressions)

| Item | Notes |
|------|--------|
| **unidirectional-related** | HA ~64, blender ~27 after the split. Next hygiene pass. |
| **file-too-large** | Glossaries, HA `faq/common-questions.md`, process decisions/patterns. Not concepts. |
| **W-HUB-01** | `packs/blender-3d/concepts/geometry-nodes-flow-creation.md` |
| **orphaned** | FAQs/workflows without `related:` |
| **Person-pack eval fixture** | RFC-002 landed; no in-repo person demo |
| **EP MCP** | `context_prefix` at index; consume-loop tools; tier/navigation filter; chunk contradiction |
| **Production reindex** | Deferred |
| **`init` template shape** | Product tree for all `--type` values |
| **`site/`** | Listed in README; not in this checkout |

---

## Likely next-session work (pick with the user)

1. **Bidirectional `related:`** on the new concept atoms.
2. **ep-mcp:** `context_prefix` prepend + consume loop.
3. **Person-pack eval fixture.**
4. Split oversized **process decisions / patterns / FAQs** (not W-V41-01; those are not `type: concept`).
5. Version tag / `[Unreleased]` — only if asked.
6. Core **4.2** — only if asked.
7. Next Intelligence Refinement `sweep` or `refine`.

---

## Conversation pointers

- Prior wrap-up (intelligence + leftovers): [Intelligence and leftovers](ec71ad04-55d7-4623-8bf6-14929bb44199)
- This session (public packs + concept split): continue from the current transcript after `8c5c627`

---

*End handoff.*
