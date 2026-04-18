# ExpertPack Concept Granularity Guide

*Reference companion to [core.md](../core.md) and [RFC-001](../rfcs/RFC-001-atomic-conceptual-chunks.md). Answers the single hardest question when authoring an atomic-conceptual pack: "does this deserve its own concept file, or does it live inside another concept?"*

---

## The question in plain language

You're writing (or reviewing) a concept file. A related term, sub-topic, or idea comes up. You have three options:

1. **Embed** it — as a paragraph in the body, an entry under `## Related Terms`, or an FAQ under `## Frequently Asked`.
2. **Promote** it to its own concept file, linked via `## Related Concepts` and wikilinks.
3. **Cross-cut** it — keep it as a shared term referenced from multiple concept files.

The wrong choice on either side has real costs:

- **Over-embedding** — concept files become bloated, drift over the 1,500-token ceiling, and retrieve broadly like the old aggregator files.
- **Over-promoting** — the pack explodes into hundreds of tiny files, graph expansion becomes noisy, and users have to stitch multiple retrievals for any meaningful answer.

This guide gives you a decision procedure and worked examples to make the call.

---

## Decision procedure

Run through these checks **in order**. The first check that gives a clear signal wins.

### 1. The atomic-coherence test (primary)

Ask: **does this thing have its own definition, properties, and relationships — or is it only meaningful relative to another concept?**

- If it can be defined without saying "X in the context of Y," it passes the test. **Promote.**
- If its definition requires reference to a parent concept, it fails the test. **Embed.**

**Example — passes:** "Drive-time polygon" has its own definition (a polygon enclosing all points reachable within N minutes by road), its own properties (origin point, travel mode, time budget), and its own relationships (used in territory building, affected by traffic model). → Promote.

**Example — fails:** "Locked territory" is defined as "a territory whose components cannot be moved during realignment." It has no meaning without the Territory concept. → Embed under Territory's `## Related Terms`.

### 2. The size test

Ask: **how much content does this idea carry on its own?**

- If a full treatment (definition + mechanics + 1-2 examples + edge cases) would exceed ~300 tokens, it's already its own concept. **Promote.**
- If a complete treatment fits in a sentence or two, it's a term. **Embed.**

Files smaller than ~200 tokens are almost always better embedded — they don't carry enough signal to justify their own retrieval slot, and they fragment the graph.

### 3. The cross-reference test

Ask: **do other concepts in the pack need to link to this thing?**

- If 3+ other concept files would naturally want to link to it, it's a shared anchor. **Promote.**
- If only the parent concept references it, it's private to that concept. **Embed.**

A wikilink target that multiple concepts point at is doing real work in the graph. A term referenced only by its parent is just scaffolding.

### 4. The retrievability test

Ask: **will users ask about this thing directly, independent of the parent concept?**

- If "What is X?" is a natural standalone query, it needs its own file to be found directly. **Promote.**
- If it only ever comes up as "What's X in the context of Y?", it lives with Y. **Embed.**

This is a judgment call — you don't need eval data to answer it. Ask yourself: would a domain expert introduce this term in a vacuum, or only while explaining something else?

### 5. The tiebreaker: prefer embed

When tests 1-4 don't produce a clear signal, **embed** by default.

Embedded terms can always be promoted later when they earn it. Promoted concepts that turn out not to earn it cause orphan files, broken wikilinks, and graph noise that's harder to clean up.

---

## Worked examples

The following examples are drawn from the ezt-designer pack's 2026-04-18 validation refactor. Each shows a real embed-vs-promote decision and why it went the way it did.

### Example 1: "Dissolve" → EMBED

**Context:** In the Territory concept, we mention that components get combined via a "dissolve" process involving deduplication, nearest-neighbor union, hole management, sliver removal.

**Decision:** Embedded in Territory's `## Related Terms` and referenced inline in the `## How It Works → Geometry & Dissolve` section.

**Why:**
- **Atomic-coherence:** Fails. Dissolve is defined as "the process of merging territory components into a unified polygon." You cannot define it without Territory.
- **Size:** A full treatment fits in ~100 tokens.
- **Cross-reference:** Only Territory references it (no other pack concepts care how the polygon was produced).

### Example 2: "Drive-time polygon" → PROMOTE

**Context:** Referenced from Territory (as one of several shapes that can bound a territory), from Routing (as an input to optimization), and from Service Area Planning (as the primary geometric unit).

**Decision:** Own concept file.

**Why:**
- **Atomic-coherence:** Passes. Has its own definition independent of any single parent.
- **Size:** Full treatment (origin, travel modes, time budgets, traffic model, computational cost, rendering) easily exceeds 500 tokens.
- **Cross-reference:** 3+ concepts would naturally link to it.
- **Retrievability:** "How do drive-time polygons work?" is a natural standalone query.

### Example 3: "Realignment" → EMBED (in Territory)

**Context:** The act of moving territory components (e.g. ZIP codes) between territories.

**Decision:** Embedded as a section inside Territory (`## How It Works → Realignment`) and listed under `## Related Terms`.

**Why:**
- **Atomic-coherence:** Fails. Realignment has no meaning outside the Territory concept — it *is* the operation you perform on territories.
- **Size:** A complete explanation (data grid workflow, locked/hidden behavior, conflict prompts) fits in ~150-200 tokens.
- **Cross-reference:** Only Territory and its related workflow files reference it.
- **Tension:** This one was close — the workflow has enough procedure to feel like it wants its own file. **Resolved by splitting:** the definitional content stays embedded in Territory; the step-by-step "how to realign a territory" lives in `workflows/wf-realign-territory.md`. See also §"Concept vs. workflow boundary" below.

### Example 4: "Coefficient of Variation (CoV)" → EMBED

**Context:** A statistical measure used by the workload partitioning algorithm to assess balance across partitions.

**Decision:** Embedded in Workload Partitioning's `## Related Terms`.

**Why:**
- **Atomic-coherence:** Passes (it's a standalone math concept) but only barely — in this pack, CoV is only meaningful as an output of the partitioning algorithm.
- **Size:** The EP-relevant treatment fits in 2 sentences.
- **Cross-reference:** Only Workload Partitioning references it. (General statistical context is outside the pack's scope.)
- **Tiebreaker:** Prefer embed. If a future concept (e.g. "Capacity Planning Metrics") also needs CoV, promote it then.

### Example 5: "Capacity Planning" → PROMOTE

**Context:** A modeling workflow that uses workload partitioning to project territory viability given rep capacity and call frequency.

**Decision:** Own concept file (`capacity-planning.md`), linked from Workload Partitioning.

**Why:**
- **Atomic-coherence:** Passes. Has its own framing (it's about modeling future capacity, not current partitioning), its own inputs (capacity parameters, call frequencies), its own outputs (statistical projections, not drawn territories).
- **Size:** Complete treatment with examples reaches ~500 tokens.
- **Cross-reference:** Referenced from Workload Partitioning, Scheduling, and future Territory Planning content.
- **Retrievability:** "How does capacity planning work?" is a natural query.

### Example 6: "Stuck ZIP codes" → EMBED (as an FAQ)

**Context:** A common user complaint: they try to move ZIP codes during realignment and the ZIPs don't move.

**Decision:** Embedded as an H3 under Territory's `## Frequently Asked`.

**Why:**
- **Atomic-coherence:** Fails. It's a symptom that's only meaningful in context of Territory's realignment behavior.
- **Retrievability:** Users do ask this directly — but the answer is tightly coupled to understanding locked/hidden territories. Embedding in Territory keeps the answer adjacent to the conceptual context.
- **Note:** The old `faq/faq-stuck-zip-codes.md` file was absorbed. Its content lives in the Territory concept's FAQ section, and any `troubleshooting/` entry for this symptom can link to the Territory concept for canonical context.

### Example 7: "Simple Partitioning" → EMBED (with sibling link)

**Context:** A distinct partitioning mode, contrasted with Workload Partitioning.

**Decision:** Embedded in Workload Partitioning's `## Related Terms` with a brief contrast. A separate `partitioning.md` parent concept may exist covering both modes.

**Why:**
- **Atomic-coherence:** Passes weakly — Simple Partitioning *is* its own mode with its own mechanics. But its utility is almost entirely in contrast to Workload Partitioning.
- **Size:** A couple of paragraphs suffice; no need for its own file.
- **Composite handling:** This is a candidate for the `concept_scope: composite` pattern — where Partitioning (the parent) covers both modes in a single concept file, rather than splitting into one file per mode.

### Example 8: "EasyTerritory" → EMBED (in overview.md, mention in glossary if needed)

**Context:** The product's own name.

**Decision:** Defined in `overview.md`. Not its own concept file. If a lightweight `glossary.md` exists for cross-cutting terms, it may be listed there.

**Why:**
- **Retrievability:** Users rarely ask "what is EasyTerritory?" directly; the overview handles this.
- **Cross-reference:** Every concept technically references it, but that's framing, not a substantive link.
- **Anti-pattern avoidance:** A standalone "EasyTerritory.md" concept would score broadly on every query (like the old aggregator files). Keep it in the entry point.

---

## Concept vs. workflow boundary

A persistent source of friction: procedural "how to do X" material wants to live in `workflows/`, while definitional material lives in `concepts/`. Applying the rule:

| If the content is… | It belongs in… |
|---|---|
| Numbered steps the user follows | `workflows/` |
| A decision tree / "if X then Y" | `workflows/` or `troubleshooting/` |
| "What X is and why it matters" | `concepts/` |
| Tradeoffs, constraints, mechanics | `concepts/` |
| Mental models, definitions, relationships | `concepts/` |

A concept file may reference its workflow(s) via wikilinks. A workflow file may reference the concept(s) it operates on via wikilinks. They're peers, not duplicates.

**When in doubt:** if you'd teach it by saying "do this, then this, then this" → workflow. If you'd teach it by saying "imagine a map where…" → concept.

---

## Concept vs. related term

A concept has a `concepts/{slug}.md` file. A related term is an entry in another concept's `## Related Terms` section.

| Concept | Related Term |
|---|---|
| Has its own definition | Defined relative to a parent |
| Has its own properties | Is a property / modifier of a parent |
| Gets linked from 3+ places | Only referenced by one parent |
| Users ask about it directly | Users ask about it only in context |
| Earns 300+ tokens of treatment | Defined in 1-3 sentences |

---

## Concept vs. FAQ

An FAQ entry lives under a concept's `## Frequently Asked` section as an H3 question.

| Concept | FAQ |
|---|---|
| Defines a "what" or "how it works" | Answers a "why" or "how do I" in user language |
| Stable, definitional | Reactive to common user confusion |
| Reads like documentation | Reads like a conversation |

If an FAQ answer grows past ~200 tokens and starts introducing new mechanics, that's a signal the underlying concept needs better coverage in its body — not that the FAQ should become a concept file.

---

## Composite concepts (`concept_scope: composite`)

Some concepts span multiple files by design. Example: `partitioning.md` as a parent covering `simple-partitioning.md` and `workload-partitioning.md` as children. When you use composite scope:

- The parent file has `concept_scope: composite` in frontmatter.
- Children have `concept_scope: single` and `parent_concept: partitioning` (or `part_of: partitioning.md`).
- The parent file's body introduces both variants and links out to children.
- Children cover their own mechanics without repeating the parent's framing.

Use composite scope when the parent-child split is a **natural hierarchy**, not when it's just "this concept got too big." If a concept exceeds the size ceiling, first try to tighten the writing; only split when there are genuinely distinct sub-concepts.

---

## Red flags

Signals that you've made the wrong granularity call:

### Over-embedded (concept file is doing too much)

- File exceeds 1,500 tokens
- `## Related Terms` section has 10+ entries
- `## Frequently Asked` section has 8+ questions
- Body has 5+ top-level `##` sections covering distinct topics
- You find yourself wanting to write a table of contents at the top

**Fix:** Identify the densest sub-topic, promote it to its own concept file, link from the parent.

### Over-promoted (too many tiny concept files)

- Multiple concept files under 200 tokens each
- `## Related Concepts` lists always link the same 2-3 files
- A user question routinely requires 4+ concept-file hits to answer
- Graph view shows a tight cluster of small files that only link to each other

**Fix:** Identify the cluster, merge into a single parent concept with the smaller ones as `## Related Terms` or body sections.

### Aggregator regression (the schema's original sin)

- A file that's basically a catalog: "Here are all the X in our pack"
- A file whose name is a category, not a concept (`workflows.md`, `errors.md`, `all-features.md`)
- A file that retrieves well for broad queries but poorly for specific ones

**Fix:** Delete it. Use `_index.md` for navigation. Let atomic concept files compete on their own merit.

---

## When to revisit

Granularity decisions aren't permanent. Revisit when:

- A "related term" keeps getting linked from new concepts → it's earning its own file
- A concept file grows past 1,500 tokens → it needs splitting
- A concept file shrinks (because material got refactored elsewhere) below ~300 tokens → consider merging it into its parent
- Users consistently ask about something you embedded → promote it

Keep the decision log in the pack's `meta/changelog.md` so the reasoning is preserved.

---

*See also: [core.md](../core.md) Retrieval Optimization section; [RFC-001](../rfcs/RFC-001-atomic-conceptual-chunks.md) atomic-conceptual chunks proposal; `_schema-refactor/NOTES.md` in the ezt-designer pack for real-world friction data.*
