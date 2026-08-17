# Intelligence Refinement Guide

*How ExpertPack stays current as frontier LLMs improve. This is a framework-maintenance cycle — not pack-content hydration. Read this before running a sweep or a full refine.*

---

## Philosophy

ExpertPack's value is **esoteric knowledge (EK)** — knowledge that does not exist in the weights of frontier-lab LLMs ([AXIOMS.md](../AXIOMS.md) 1–3, 9–10). As those models improve, two things happen at once:

1. **Pack EK decays.** Some content that used to be esoteric becomes general knowledge. Re-measure with the existing quarterly / post-release path in [guides/hydration.md](hydration.md). That is *not* this cycle.
2. **New techniques appear.** Agent memory, retrieval, grounding, and skill-loading approaches can raise axiom 6 quality (compactness × EK volume × retrieval × low decay) if they are adapted in a **framework-first, measurable, pack-type-agnostic** way ([ROADMAP.md](../ROADMAP.md) principles).

This cycle is the mechanism for (2). It does not hydrate packs, rewrite pack atoms, or compact canonical `schemas/*.md` prose.

Documented anti-patterns this cycle must not repeat:

- **Prose densification** dropped correctness (~76.8%, −2.2%).
- **Schema-aware chunking** raised it (~88.4%, +9.4%). See [guides/consumption.md](consumption.md).
- **Standalone summary / aggregator layers** violate axioms 11–13 and harm retrieval.

---

## Cadence

| Mode | What it runs | When |
|------|----------------|------|
| **`sweep`** | Step 1 only (30-minute research → top 3) | Optional light pass; after an interesting paper or model drop |
| **`refine`** | Full cycle (steps 1, 2, 3, 5, then a human gate) | Default: monthly, or after a major frontier model release |

Operator-triggered via the `expertpack-intelligence` skill. There is no required cron. The old Wednesday GPT-5 Mini sweep is retired as the source of truth.

---

## What each cycle does

```
Start
  ├─ Step 1  30-min research          → Top 3 from the field
  ├─ Step 2  Schema vs objectives     → Top 3 from schemas
  ├─ Step 3  Context-schema footprint → standing apply (no extra approval)
  └─ Step 5  SDLC sync                → standing apply (no extra approval)
                    │
                    ▼
              Human gate (0–3 from each top-3 list)
                    │
                    ▼
              Apply approved items → write run log → update ROADMAP
```

There is no step 4.

**Standing work** (applied every `refine`, no extra approval): step 3 + step 5.

**Judgment work** (human picks 0–3 items from each list before apply): steps 1 and 2.

---

## Artifacts

| Artifact | Role |
|----------|------|
| This guide | Human entry: purpose, cadence, gates |
| [`skills/expertpack-intelligence/SKILL.md`](../skills/expertpack-intelligence/SKILL.md) | Agent executor |
| Skill `references/` | Protocols loaded on demand (not dumped into every turn) |
| [`logs/intelligence/YYYY-MM-DD.md`](../logs/intelligence/) | Dated run log (copy from the skill run template) |
| [`ROADMAP.md`](../ROADMAP.md) Vector 6 + status log | Framework backlog and cycle outcomes |

Canonical schemas stay in [`schemas/`](../schemas/). Skill schema projections are *projections* of that contract, not a second authoring surface.

---

## Phases

### Step 1 — Bounded research (30 min)

Hard stop at 30 minutes. Goal is transferable approaches, not a literature review.

Load `{skill_dir}/references/research-protocol.md` and follow it. Output exactly 3 suggestions, each with: approach, source, EP mapping, metric, risk, recommended next action (`consider` / `pilot` / `reject`).

Already-integrated (do not re-propose unless something material changed): Graphiti-style bi-temporal facts, AKS micro-records, Reconstruct Mode / TAC.

### Step 2 — Schema review vs objectives

Load `{skill_dir}/references/schema-review-protocol.md`. Read axioms and architecture first, then canonical schemas, then the context-loaded projections. Score gaps against EK maximization, retrievability, compactness-without-EK-loss, decay control, and filing-guide quality.

Output exactly 3 schema-level suggestions in the same shape as step 1. Do not propose pack-content edits.

### Step 3 — Context-loaded schema footprint

Load `{skill_dir}/references/context-schema-protocol.md`.

This is **not** “rewrite `schemas/core.md` with fewer words.” Canonical schemas stay the complete filing guide. The failure mode is stale, hand-maintained projections that agents load first.

Method: progressive disclosure, not compression. Keep the words that retrieve (opening-paragraph rules, `requires:`, `## Frequently Asked`, anti-compaction, anti-aggregator). After editing projections, run `python tools/check-schema-projections.py`.

### Step 5 — SDLC sync

Load `{skill_dir}/references/sync-checklist.md`. Align ROADMAP, ARCHITECTURE, README, eval examples, and skill copy with axioms and `schemas/schema-index.yaml`. Prefer fixing the derived docs. Do not change axiom text unless the review found a real contradiction.

Regenerate the README schema table when versions change:

```bash
python tools/update-schema-readme.py
```

---

## Human gate

After steps 1–2 (and after standing 3 + 5 on a `refine`), stop. Present both top-3 lists. The operator picks 0–3 items from each list. Apply only those. Append decisions to the run log and a ROADMAP status-log entry.

Never apply unapproved top-3 items. Never treat a top-3 as a commit license.

---

## Companion skills

- `expertpack` — consume / hydrate / validate packs
- `expertpack-eval` — EK ratio and quality evals (use when a pilot needs a before/after metric)
- `expertpack-export` — OpenClaw workspace → EP (its schema summary is a projection; keep it in sync via step 3)
