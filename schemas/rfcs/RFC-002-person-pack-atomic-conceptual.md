# RFC-002: Person-pack atomic-conceptual adaptation

- **Status:** Accepted (authoring contract; person-pack eval fixture still pending)
- **Author:** Intelligence Refinement cycle 1 (2026-08-16)
- **Created:** 2026-08-16
- **Target:** Schema 4.1 (additive clarification of `person.md`)
- **Depends on:** RFC-001 (atomic-conceptual files), RFC-004 (chunk sidecars)
- **Resolves:** ROADMAP Vector 5 “RFC-002: person-pack atomic-conceptual adaptation”

---

## Summary

Person packs keep **one story / reflection / opinion / conversation = one file**. Verbatim voice lives in that atom. The 1,000-token *concept* ceiling does **not** force a parallel summary file.

When a narrative atom is too long to embed as one chunk:

1. Prefer **RFC-004 sidecar** (`retrieval_strategy: atomic`) so the file stays whole for the reader and splits only at `##`/`###` for the indexer.
2. **Split** only when each resulting file is an independently retrievable episode (different query, different answer).
3. **Never** create `story-overview.md` + `story-detail.md` where the first file exists only to summarize the second. That is axiom 12.

Stories, reflections, opinions, and conversations default to `retrieval_strategy: atomic`.

---

## Motivation

RFC-001 proved aggregator layers harm retrieval-first packs. Person packs were deferred because verbatim voice collides with the concept size ceiling: a story that is the person’s actual words is often longer than 1,000 tokens, and splitting it the way a product concept splits loses the voice (axiom 5 / 11).

`person.md` previously recommended `story-overview.md` (summary + key beats) requiring `story-detail.md` (full verbatim). That pattern is a standalone summary file with extra steps. It will score broadly, displace the voice atom, and teach authors the antipattern RFC-001 retired.

---

## Decision

| Case | Action |
|------|--------|
| Narrative fits in ~1,000 tokens | One file. `retrieval_strategy: atomic` still (retrieve whole; do not FAQ-split a story). |
| Narrative exceeds ~1,000 tokens but is one episode | Keep one file. `retrieval_strategy: atomic`. Add `.chunks.yaml` (RFC-004). Opening paragraph remains the embed anchor. |
| Narrative is several independently askable episodes | Split into one file per episode. Link with `related:` (soft) or `requires:` only if one episode is unintelligible without another. |
| Product-style concept inside a person pack (`facts/`, `mind/`) | RFC-001 rules unchanged: 400–800 / 1,000 ceiling, `standard`, split if not one topic. |

### Rejected alternatives

- **Overview + detail pair.** Violates axiom 12. `requires:` expansion does not make a summary file legitimate.
- **Unbounded `standard` stories.** Indexers will split mid-sentence and retrieve a fragment of voice without the beat that makes it true.
- **Person-pack exemption from atomic-conceptual.** Filing-guide drift; agents would learn two schemas.

---

## Schema changes

- `schemas/person.md` — replace the overview/detail split pattern with this decision table; keep story-card frontmatter.
- `schemas/core.md` — directory default for `stories/` (and sibling narrative dirs) is `atomic`, not `standard`.
- Validator: existing W-V41-01 already exempts `atomic` / `navigation`. No new error code. Oversized *concept-like* person files (`facts/`, `mind/`) still warn.

---

## Eval

No person demo pack ships in this repo. When a fixture exists, measure:

- retrieval hit rate on “tell the X story” vs “what happened after X”
- correctness / voice fidelity (human or LLM-as-judge against the verbatim atom)
- W-V41-01 count on `facts/` + `mind/` only (stories should be 0 if marked `atomic`)

Until that fixture exists, treat this RFC as the authoring contract, not a measured retrieval win.

---

## Migration

Existing overview/detail pairs: merge the overview’s unique beats into the detail atom’s opening paragraph, delete the overview file, set `retrieval_strategy: atomic`, run `ep-chunk-annotate --apply` if still oversized, add `supersedes:` on the survivor.
