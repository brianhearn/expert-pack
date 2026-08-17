# Session Handoff — 2026-08-17

*Context for the next agent. Two arcs landed since the 2026-07-07 handoff: Intelligence Refinement cycle 1 (2026-08-16) and EasyBot-brief leftovers (2026-08-17). Do not edit `.cursor/plans/intelligence_refinement_52705987.plan.md`.*

---

## Git state (after this wrap-up)

| Item | Value |
|------|--------|
| **Branch** | `main` |
| **What this commit covers** | Intelligence Refinement process + cycle 1 applications + authority boundary + composite 1.2 conflict resolver |
| **Do not commit** | `expert-pack.code-workspace` (local IDE only) |
| **Deploy** | **Not done** — do not deploy ep-mcp or reindex without an explicit user request |

---

## What landed

### A. Intelligence Refinement (2026-08-16)

Repeatable process (user chose **repo skill + guide**, not a process pack):

- [`guides/intelligence-refinement.md`](../guides/intelligence-refinement.md)
- [`skills/expertpack-intelligence/`](../skills/expertpack-intelligence/) — `sweep` (step 1 only) vs `refine` (full cycle)
- Run log: [`logs/intelligence/2026-08-16.md`](../logs/intelligence/2026-08-16.md)
- ROADMAP Vector 6 points here. The old Wednesday GPT-5 Mini sweep and the **X daily scan** are retired (scan campaign ended 2026-08-16).

Standing work (no extra approval):

- Context-loaded schema **projections** — do **not** compact canonical `schemas/*.md`
  - [`skills/expertpack/references/schemas.md`](../skills/expertpack/references/schemas.md) — filing rules only
  - Type-gated: `schemas-product.md`, `schemas-person.md`, `schemas-process.md`, `schemas-agent.md`, `schemas-composite.md`
  - Export summary brought to v4.1
  - `expertpack` SKILL.md loads the type file only after type is known
- [`tools/check-schema-projections.py`](../tools/check-schema-projections.py) — fails if projections teach retired patterns (`relations.yaml`, nested `retrieval.strategy`, `summaries/`/`propositions/`, `sectioned`)
- Wired in `.github/workflows/validate.yml` (docs job) and `.pre-commit-config.yaml`

Cycle 1 human gate: user applied **all six** top-3 items.

| ID | Landed in this repo | Still in ep-mcp / elsewhere |
|----|---------------------|-----------------------------|
| R1 | Sidecar `context_prefix` (deterministic title+section) in `ep-chunk-annotate.py`, spec, RFC-004; demo sidecars regenerated | EP MCP must prepend at index time |
| R2 | Hierarchical consume loop in `guides/consumption.md` + skill copy: search → read atom → `requires:` → stop (budget 3 / cap 7) | EP MCP/host tool loop |
| R3 | Optional `activation:` frontmatter (`tools`, `constraints`, `next`) on workflow/decision/gotcha/phase | Adoption on real atoms |
| S1 | [RFC-002](../schemas/rfcs/RFC-002-person-pack-atomic-conceptual.md); person stories/reflections/opinions/conversations default **`atomic`**; no overview/detail summary pair | Person-pack eval fixture |
| S2 | Validator `W-TIER-01..03`; template `_index.md` set to `navigation` | Demo-pack `_index.md` still `standard` (W-TIER-02); demo always-tier over 5KB (W-TIER-01) |
| S3 | Converters no longer write `relations.yaml`; `W-GRAPH-01`; elite/self-improving map `lessons/` not `summaries/` | External packs that still have the file |

### B. EasyBot brief leftovers (2026-08-17)

Source: `C:\Users\BrianHearn\OneDrive - Easy Territory, Inc\Desktop\ep-improvement-brief-2026-08-16.md`. Thesis still holds: find the canonical block, prove it, inject that.

**Already done before this session — do not re-sprint:** `expertpack init`; aggregator exclusion; Reconstruct/TAC; ontology-suggest + `_graph.yaml`; AKS compact export; definitional leads; RFC-002; don’t default a cross-encoder; don’t drop to 768-d.

**Stale in that brief:** “init does not exist” (it does); 1,500-token ceiling (now **1,000**); “EP MCP is gone” (this repo still treats ep-mcp as runtime — prefer **pack + consumer contract** over standing the server back up).

User said **do both** leftovers. Both shipped:

1. **Authority boundary + refusal evals**
   - `authority_boundary` on `manifest.yaml` (`in_scope`, `out_of_scope`, `refuse_when`, `no_source_no_claim`)
   - Documented in `schemas/core.md`; template + `template/TOOLS.md` Authority section
   - `expertpack init` substitutes type-specific defaults (product / person / process / composite)
   - Template eval has **3** `refusal` questions (`q004`–`q006`)
   - Validator: `W-AUTH-01` (missing), `W-AUTH-02` (incomplete), `W-EVAL-01` (<3 refusal/out-of-scope questions if an eval file exists)
   - **Not in `STRICT_PROMOTE`** — demo packs stay `--strict` green
   - Eval schema **1.4**; `skills/expertpack-eval` scores `refusal` and `out-of-scope` as the same category

2. **Composite conflict rules with tests**
   - Composite schema **1.2**: isolation → authority → `fail_closed` / `flag` / `priority` + `tie_break`
   - Default strategy remains **`flag`** (backward compatible). Production help-bots should prefer `fail_closed`.
   - Executable: [`tools/composite/conflict.py`](../tools/composite/conflict.py) — 13 tests in `test_conflict.py`
   - Worked examples: person vs product deprecation (flag); two products disagree on a term (fail_closed); family-tier fact in a public composite (isolation drop before priority)
   - Wired in docs CI and pre-commit

---

## Key design decisions (carry forward)

1. **Schema family stays 4.1** unless the user explicitly asks for 4.2. Authority boundary is additive on core. Composite 1.1 → 1.2 and eval 1.3 → 1.4 are type-schema bumps only.
2. **Do not compact canonical `schemas/*.md`.** Prose densification hurt correctness. Shrink context via type-gated projections + `check-schema-projections.py`.
3. **Axioms 11–13 are load-bearing.** One topic = one file. No standalone summary/aggregator files. Content strategy must match retrieval-first vs LLM-reads-all. ROADMAP “Summary layers” is **rejected**.
4. **Pack + consumer contract over reviving EP MCP as the destination.** Specs and tests live here; runtime wiring stays in [ep-mcp](https://github.com/brianhearn/ep-mcp).
5. **Token ceiling is 1,000** for concepts (not 1,500).
6. **New validator codes are WARN, not `--strict` ERROR**, unless they are the frontmatter/provenance contract. Do not add `W-AUTH-*`, `W-EVAL-01`, `W-TIER-*`, or `W-GRAPH-01` to `STRICT_PROMOTE`.
7. **Do not hydrate blender / HA / solar content** to clear advisory warnings unless the user asks. `W-AUTH-01` on demo manifests is expected.
8. **Do not edit the Intelligence Refinement plan file.**
9. **Do not deploy without an explicit user request.**
10. **`init --type person|process|composite` still copies the product-shaped `template/`** (pre-existing). Only `authority_boundary` text is type-specific. Person init can fail `--strict` on `meta/source-coverage.md` (person prefix `meta-`).
11. **PowerShell:** `&&` is not a statement separator on older Windows PowerShell. Use `;` and check `$LASTEXITCODE`.
12. **`refusal` and `out-of-scope` are the same eval category.** Template uses `refusal`; blender uses `"refusal"`; schema table lists both.

---

## Verification (Windows / PowerShell)

```powershell
cd C:\Users\BrianHearn\source\repos\expert-pack
python tools/validate-all.py --ignore W-V41-01
python tools/validator/ep-validate.py template --strict
python tools/check-schema-projections.py
python tools/update-schema-readme.py --check
python tools/composite/test_conflict.py
python tools/chunker/ep-chunk-annotate.py packs/blender-3d --check --embedding-version gemini-embedding-001
```

Expected: template **0 errors** (no `W-AUTH` / `W-EVAL-01`). Demo packs **0 errors** under `--strict --ignore W-V41-01`, with advisory `W-AUTH-01` (and blender `W-EVAL-01` — only 2 refusal questions). Conflict tests: **13 OK**.

---

## Known backlog (do not treat as regressions)

| Item | Notes |
|------|--------|
| **W-V41-01** | Oversized `standard` concepts in demo packs; CI/pre-commit `--ignore W-V41-01` |
| **W-TIER-01** | Demo `context.always` over 5KB |
| **W-TIER-02** | Demo `_index.md` still `retrieval_strategy: standard` |
| **W-AUTH-01** | Demo manifests have no `authority_boundary` (intentional) |
| **W-EVAL-01** | blender-3d eval has 2 refusal questions; floor is 3 |
| **Person-pack eval fixture** | RFC-002 landed; no in-repo person demo to score |
| **EP MCP runtime** | `context_prefix` prepend; consume-loop tools; navigation/tier index filter; chunk-level contradiction |
| **Production reindex** | Still deferred; needed for accurate `fragment_id` after sidecar/`context_prefix` |
| **`init` template shape** | Product tree for all `--type` values |
| **ROADMAP “Confidence tagging”** | Field exists in core; not widely adopted on atoms |
| **`site/`** | Listed in README; not in this checkout |
| **Windows ep-mcp loader tests** | 8 pre-existing unit failures on Windows |
| **`pip install -e .`** | May need modern pip/setuptools on Windows; `python tools/cli/expertpack.py` works |

---

## Likely next-session work (pick with the user)

1. **ep-mcp:** prepend `context_prefix` at index time; honor consume loop (search → read atom → `requires:` → stop); optional navigation/tier index filter.
2. **Demo-pack hygiene:** `_index.md` → `navigation`; trim always-tier; optional `authority_boundary` + third blender refusal question (only if asked to hydrate demos).
3. **Person-pack eval fixture** to close RFC-002 measurement.
4. **Atomic-split sprint** to drop `W-V41-01` ignore.
5. **Version tag** + `[Unreleased]` → versioned CHANGELOG (both repos) — only if asked.
6. **Core 4.2** — only if the user explicitly requests a family bump.
7. Next Intelligence Refinement `sweep` or `refine` when the user wants another research cycle.

---

## Key file index

```
guides/intelligence-refinement.md
guides/consumption.md
logs/intelligence/2026-08-16.md
logs/intelligence/2026-08-17.md
skills/expertpack-intelligence/
skills/expertpack/references/schemas.md          # filing rules only
skills/expertpack/references/schemas-*.md        # type-gated projections
tools/check-schema-projections.py
tools/composite/conflict.py
tools/composite/test_conflict.py
tools/cli/expertpack.py                          # init authority defaults
tools/validator/ep-validate.py                   # W-AUTH, W-EVAL, W-TIER, W-GRAPH
tools/chunker/ep-chunk-annotate.py               # context_prefix
schemas/core.md                                  # authority_boundary
schemas/composite.md                             # 1.2 fail-closed contract
schemas/eval.md                                  # 1.4
schemas/rfcs/RFC-002-person-pack-atomic-conceptual.md
schemas/schema-index.yaml
template/manifest.yaml
template/eval/benchmark.yaml
template/TOOLS.md
AXIOMS.md
ARCHITECTURE.md
ROADMAP.md
CHANGELOG.md
```

---

## Related repos

| Repo | Path | Role |
|------|------|------|
| expert-pack | `C:\Users\BrianHearn\source\repos\expert-pack` | Authoring framework, specs, validation, consumer contracts |
| ep-mcp | `C:\Users\BrianHearn\source\repos\ep-mcp` | MCP runtime — hybrid retrieval, sidecars, reconstruct. Index-side `context_prefix` + consume loop still open. |

---

## Conversation pointers

- Intelligence Refinement + cycle 1 + EasyBot leftovers: [Intelligence and leftovers](ec71ad04-55d7-4623-8bf6-14929bb44199)

---

*End handoff.*
