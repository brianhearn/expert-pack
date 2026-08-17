---
name: expertpack-intelligence
description: "Periodically refine the ExpertPack framework as frontier LLMs improve. Use when: (1) Running an intelligence refinement cycle, (2) Doing a bounded web research sweep on agent knowledge / retrieval approaches, (3) Reviewing EP schemas against axioms and architecture, (4) Checking context-loaded schema projections for drift or bloat, (5) Syncing schemas with SDLC docs. Triggers on: 'intelligence refinement', 'EP research sweep', 'schema review cadence', 'frontier EK scan', 'refine expertpack', 'expertpack intelligence'."
metadata:
  openclaw:
    homepage: https://expertpack.ai
---

# ExpertPack Intelligence

Keep the ExpertPack *framework* current as frontier models improve. This is not pack hydration.

**Learn more:** [expertpack.ai](https://expertpack.ai) · [GitHub](https://github.com/brianhearn/expert-pack) · [Guide](https://github.com/brianhearn/expert-pack/blob/main/guides/intelligence-refinement.md)

> **Companion skills:** For pack consume/hydrate/validate use `expertpack`. For EK measurement and quality evals use `expertpack-eval`. For exporting an OpenClaw agent as an ExpertPack use `expertpack-export`.

**Human entry:** `guides/intelligence-refinement.md` in the ExpertPack repo.

## Modes

| Mode | Runs | Default cadence |
|------|------|-----------------|
| **`sweep`** | Step 1 only | Optional; after a paper or model drop |
| **`refine`** | Steps 1, 2, 3, 5, then human gate | Monthly, or after a major frontier model release |

If the operator does not name a mode, run **`refine`**.

## Actions

### 1. Research sweep (step 1)

1. Read `{skill_dir}/references/research-protocol.md`.
2. Execute the query set. Hard stop at 30 minutes.
3. Score candidates against the rubric. Emit exactly 3 suggestions.
4. If mode is `sweep`, write `logs/intelligence/YYYY-MM-DD.md` from `{skill_dir}/references/run-template.md` (step 1 section only) and stop.

### 2. Schema review (step 2)

1. Read `{skill_dir}/references/schema-review-protocol.md`.
2. Read in the listed order (objectives → canonical schemas → context-loaded projections).
3. Emit exactly 3 schema-level suggestions (not pack content).

### 3. Context-schema footprint (step 3, standing)

1. Read `{skill_dir}/references/context-schema-protocol.md`.
2. Rebuild or patch skill schema *projections* only. Do not compact `schemas/*.md`.
3. Run `python tools/check-schema-projections.py` and fix any hits.

### 4. SDLC sync (step 5, standing)

1. Read `{skill_dir}/references/sync-checklist.md`.
2. Fix derived-doc drift. Prefer aligning ROADMAP / eval / skill copy to axioms.
3. If schema versions changed: `python tools/update-schema-readme.py`.

### 5. Human gate, then apply

1. Present both top-3 lists. Do not apply judgment items yet.
2. After the operator picks 0–3 from each list, apply only those.
3. Write or update `logs/intelligence/YYYY-MM-DD.md` from `{skill_dir}/references/run-template.md`.
4. Append a dated entry to `ROADMAP.md` status log. Update Vector 6 checkboxes if a planned item shipped.

## Rules

- Framework-first, pack-type agnostic, measurable. No vibes-based “improvement.”
- Do not propose standalone summary / aggregator layers (axioms 11–13).
- Do not densify prose to save tokens (consumption-guide anti-compaction result).
- Do not rewrite canonical `schemas/core.md` to be shorter.
- Do not hydrate or re-measure demo packs in this cycle.
- Already-integrated unless something material changed: bi-temporal provenance, AKS micro-records, Reconstruct Mode, TAC.
