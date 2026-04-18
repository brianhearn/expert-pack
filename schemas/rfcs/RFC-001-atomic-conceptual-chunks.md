# RFC-001: Atomic-Conceptual Chunks

- **Status:** Accepted (pending migration tooling + eval validation)
- **Author:** Brian Hearn (with EasyBot)
- **Created:** 2026-04-18
- **Accepted:** 2026-04-18
- **Target:** Schema 4.0 (MAJOR bump)
- **Supersedes:** Portions of Retrieval Optimization section in `schemas/core.md` (summaries directory, propositions directory, separate FAQ directory, lead summary pattern)
- **Companion:** [`schemas/references/granularity-guide.md`](../references/granularity-guide.md)

---

## Summary

Replace the current "aggregator-by-type" retrieval architecture (separate `summaries/`, `propositions/`, `faq/`, and root-level `glossary-*.md` files) with an **atomic-conceptual chunk** model: one concept = one file, with related glossary terms, FAQs, and propositions **co-located** in that file.

A concept file becomes a self-contained retrieval unit carrying:
- A retriever-friendly opening paragraph that functions as the summary
- The full conceptual body
- FAQs as a structured `## Frequently Asked` section (H3 per question)
- Related terms that don't stand alone, as a `## Related Terms` section
- Wikilinks to sibling concept files for graph expansion

This eliminates three categories of files (`summaries/`, `propositions/`, standalone FAQ files) and reframes glossaries as either embedded subsections or promoted concepts.

---

## Motivation

### The aggregator antipattern

The current schema recommends generating three derived retrieval layers — `summaries/`, `propositions/`, and a root `glossary.md` — alongside canonical content files. This was justified by hierarchical retrieval theory (RAPTOR-style), but empirical results in the ezt-designer pack have consistently shown the opposite:

- **2026-04-17:** Deleting `summaries/`, `propositions/`, and `sources/` directories from ezt-designer produced a measurable retrieval boost. Aggregator files were scoring broadly on every query and displacing specific atomic files.
- This has been promoted to a standing rule in `MEMORY.md`: *"Aggregator files are an antipattern for retrieval-first packs. `propositions/`, `summaries/`, `sources/` directories score broadly on every query and displace specific atomic files."*

The root cause: each aggregator file is keyword-dense and topic-agnostic. Its embedding lands in a centroid of many concepts, so it ranks modestly for everything and well for nothing — displacing the specific files that would give a focused answer.

### The knowledge spreading problem

Even without aggregator directories, the schema currently encourages **spreading knowledge about a single concept across multiple files**:

- The concept's definition lives in `concepts/{topic}.md`
- Its technical terms live in a root-level `glossary-{domain}.md`
- Its common questions live in `faq/{category}.md`
- Its atomic facts live in `propositions/{section}.md`

For a retriever to answer a nuanced question about one concept, it must stitch together hits from three or four files. That's a tax on the retriever (more hits needed, more displacement risk), on the chunker (more boilerplate per file), and on the generator (more context to reason over).

### The summary redundancy question

The current schema recommends a "lead summary" blockquote at the top of every high-traffic file, AND a separate `summaries/{section}.md` file covering the same material. In practice:

- The lead summary and the file's first paragraph carry nearly identical signal.
- The separate summaries file competes with (and usually outscores) the canonical file it summarizes.
- LLMs can generate a summary on demand from well-written source text; pre-generated summaries are retrieval bait, not knowledge.

A well-written opening paragraph with a clear concept definition does everything a separate summary does, without the retrieval penalty.

---

## Proposal

### Core principle

**One concept = one retrievable unit.** All knowledge about a concept — definition, mechanics, examples, relative terminology, common questions — lives in a single markdown file. The file's structure is designed for both retrieval (via section-boundary chunking) and LLM reasoning (via natural narrative flow).

### File structure

```markdown
---
id: {pack-slug}/concepts/{concept-slug}
title: "Concept Name"
type: concept
tags: [concept-slug, related-domain-tags]
pack: {pack-slug}
retrieval_strategy: standard
concept_scope: single          # or "composite" for parent concepts spanning children
parent_concept: parent-slug    # optional — set when this is a child in a composite hierarchy
supersedes:                    # optional — files replaced by this one (for migration tracking)
  - old-filename.md
related:
  - sibling-concept.md
  - related-workflow.md
---

# Concept Name

Opening paragraph (1-3 sentences) that defines the concept in retriever-friendly terms. No "this document describes" preamble. This paragraph IS the summary — retrieval-anchored and reader-useful.

## [Body sections as needed]

Full EK body: mechanics, behavior, usage, examples, constraints. Use `##` section headers at natural topic breaks so the chunker aligns to semantic boundaries.

## Frequently Asked

### How does X differ from Y?
Answer phrased to match likely user queries.

### When should I use X?
Answer.

## Related Terms

- **Relative term:** Definition that only makes sense in context of this concept.
- **Another term:** Definition.

## Related Concepts
- [[sibling-concept]]
- [[related-workflow]]
```

### Mandatory elements

1. **Opening paragraph defines the concept.** No throat-clearing. First 1-3 sentences must be retriever-anchored: the concept named explicitly, the category it belongs to, its distinguishing characteristic. Replaces both the old `## What It Is` section and the old lead-summary blockquote.

2. **Section headers at topic breaks.** Every `##` section is one coherent sub-topic that produces a clean chunk.

3. **Wikilinks for graph expansion.** `related:` frontmatter + `## Related Concepts` section with `[[bare-filename]]` wikilinks. EP MCP's graph expansion layer pulls in siblings when relevant, so we don't duplicate content across files.

### Optional sections

4. **`## Frequently Asked`.** Include when the concept has documented questions that users actually ask. Each question as an H3 heading. The chunker splits on headings, so each Q/A becomes its own sub-chunk with strong query-matching surface. Canonical ownership: each Q/A lives in the primary concept it answers for; other concepts cross-link to it via `## Related Concepts` rather than duplicating the Q/A.

5. **`## Related Terms`.** Include when the concept has relative terminology that doesn't stand alone. If a term has its own definition, properties, and relationships, it earns its own concept file instead. See [granularity-guide.md](../references/granularity-guide.md) for the embed-vs-promote decision procedure.

6. **`## Key Propositions`** (optional). Include when the concept has genuinely axiomatic statements worth surfacing for logical extraction — invariants, hard rules, or formal properties. Each proposition as a concise bullet. Omit when the concept's truth is adequately carried by body prose. This is the schema-supported path for the declarative style that `propositions/` files used to carry, without the aggregator regression.

### Removed / deprecated

- **`summaries/` directory** — deprecated. The opening paragraph of each concept file replaces this.
- **`propositions/` directory** — deprecated as a standalone directory. When a concept has axiomatic statements worth surfacing, use the optional `## Key Propositions` section inside the concept file.
- **Standalone `faq/` directory** — deprecated for concept-specific FAQs. Questions move into the primary concept file's `## Frequently Asked` section. A root `faq/` may persist for truly cross-cutting questions that don't belong to any single concept (e.g., "What does 'EasyTerritory' mean?"), but should be used sparingly.
- **Root-level `glossary-{domain}.md` files** — deprecated. Terms either:
  - Get promoted to their own concept file (if they stand alone), OR
  - Get embedded in the `## Related Terms` section of the parent concept (if relative)
  - A lean, optional `glossary.md` at the pack root may exist for genuinely cross-cutting terms (product name, industry vocabulary) as an author/agent navigation aid — not as a retrieval layer.
- **Lead summary blockquote pattern** — deprecated. The opening paragraph IS the lead summary; no separate blockquote needed.

### Preserved

- `workflows/` — unchanged. Atomic retrieval strategy, step-by-step procedures.
- `troubleshooting/` — unchanged. Atomic retrieval strategy, symptom → cause → fix.
- `volatile/` — unchanged. Frontmatter TTL, time-bound content.
- `decisions/`, `specifications/`, `customers/`, `commercial/`, `interfaces/` — unchanged.
- `meta/` — unchanged. Changelog, provenance tracking.
- `overview.md`, `manifest.yaml` — unchanged structure.

### Granularity rule

**Author discretion, no frequency threshold.** A term or sub-topic earns its own concept file when it has its own definition (not just "X in the context of Y"), its own properties or sub-concepts, its own relationships to other concepts, or enough content to justify standalone treatment. Otherwise, it lives embedded in the parent concept. When tests are inconclusive, **prefer embed** — promotion is cheap later; demotion creates broken wikilinks and orphan files.

The full decision procedure, boundary tables (concept-vs-term, concept-vs-workflow, concept-vs-FAQ), and 8 worked examples from the validation refactor live in [`schemas/references/granularity-guide.md`](../references/granularity-guide.md). Authors and review agents should consult it whenever an embed-vs-promote call is non-obvious.

### Workflow vs. concept boundary

A concept file is definitional: what something is, why it matters, how it behaves, what tradeoffs it carries. A workflow file is procedural: numbered steps the user executes to accomplish a task. When content has both, split it:

- Definitional content → `concepts/{concept}.md`
- Procedural content → `workflows/{workflow}.md`
- Wikilink the two together

Rule of thumb: if you'd teach it by saying "do this, then this, then this," it's a workflow. If you'd teach it by saying "imagine a map where…", it's a concept.

### Size targets

- **Soft target:** 500–900 tokens per concept file. This is the natural range observed in the validation refactor and leaves room for the opening definition, body, FAQ section, and related terms without crowding.
- **Hard ceiling:** 1,500 tokens. Files above this must be split at `##` boundaries or decomposed into parent+child concepts via `concept_scope: composite`.
- **Lower bound:** files under ~200 tokens are almost always better embedded as related terms in a parent concept; they don't carry enough signal to justify their own retrieval slot.

### Wikilink convention

Related concept files are linked via bare-filename wikilinks (`[[concept-slug]]`, no path, no `.md` extension required but allowed). Filename uniqueness across the pack is already enforced by the existing directory-prefix convention. EP MCP's graph expansion picks up wikilinked neighbors during retrieval, reducing the need to duplicate content.

### Deprecation tracking (`supersedes:`)

When a new atomic-conceptual file replaces one or more legacy files, list the legacy filenames in the new file's `supersedes:` frontmatter field. This lets `ep-validate` detect orphans (a `supersedes:` target that still exists in the pack), lets migration tooling prune replaced files once the new file is validated, and preserves the audit trail without baking stale paths into the content body.

---

## Migration

### For new packs

Start directly in the atomic-conceptual model. No `summaries/`, `propositions/`, or glossary files at the root. Concepts are self-contained.

### For existing packs

Schema 4.0 is a MAJOR bump; migration is required for conformance but can be phased:

1. **Phase 1 (immediate):** Delete `summaries/` and `propositions/` directories. These are derived — regenerating from canonical content recovers anything lost.
2. **Phase 2 (per-concept):** For each concept file, consolidate its related FAQs and glossary entries from other files into the concept file. Move or merge in the following order:
   - FAQs from `faq/` → `## Frequently Asked` section
   - Relative glossary terms from root-level glossaries → `## Related Terms` section
   - Cross-referenced propositions from deleted `propositions/` → absorbed into body prose
3. **Phase 3 (cleanup):** Delete the emptied source directories and glossary files. Add/verify wikilinks in `## Related Concepts`. Regenerate `_graph.yaml`.

Packs on Schema 3.x remain readable by EP MCP — this RFC does not break the loader. It reorganizes where content lives but keeps the markdown-canonical principle intact.

### Migration tooling

The `tools/` directory should gain:

- `ep-migrate-3-to-4.py` — scans a pack for `summaries/`, `propositions/`, `faq/`, `glossary-*.md` and produces a migration plan (which content goes where). Interactive or plan-file driven — asks the author about ambiguous cases (e.g., "this term could be promoted or embedded — your call"). Emits a `_migration-plan.md` for review before applying changes.
- `ep-validate` updated to:
  - Flag deprecated directories (`summaries/`, `propositions/`) in Schema 4.0+ packs
  - Verify `supersedes:` targets no longer exist (or warn when they still do)
  - Verify `parent_concept:` references resolve to a file with `concept_scope: composite`
  - Warn on concept files above the 1,500-token hard ceiling

---

## Expected impact

### Retrieval quality

- **Higher precision top-K:** One hit on an atomic-conceptual file surfaces the full conceptual neighborhood. Fewer hits needed per answer. Less displacement risk from keyword-dense aggregator files.
- **Better chunk semantics:** Each `##`-bounded chunk is a meaningful sub-unit of a single concept, not a fragment of an aggregator.
- **Improved FAQ retrieval:** Literal question text at H3 boundaries gives strong query-match surfaces for natural-language queries.

### EK density

- Removing aggregator boilerplate (index prose, "see also" scaffolding, repeated framing) increases EK-per-token in each chunk.
- Measurement via `expertpack-eval` EK ratio tooling should confirm this — expected improvement in product-domain packs.

### Author experience

- Fewer files to maintain. A concept that previously spanned 4 files (concept + summary + proposition + FAQ) becomes 1 file.
- Natural authoring flow: explain the concept, document its terms, capture common questions — all in one place.
- Graph view becomes cleaner: the knowledge topology is visible without aggregator hubs cluttering the layout.

### Risks

- **Larger individual files.** Consolidation pushes file size up. The 1,500-token ceiling may need revisiting; verify the chunker splits on `##` boundaries sensibly.
- **Loss of hierarchical retrieval fallback.** Broad queries previously hit summaries first. Empirically, this wasn't helping — but we should monitor recall on genuinely broad queries after migration.
- **Over-consolidation.** Authors may be tempted to stuff everything into one file. The granularity rule (author discretion, guided by atomic coherence) combats this, but needs clear guidance and examples.
- **Migration churn.** Existing packs need manual review. Tooling helps but cannot replace author judgment on embed-vs-promote decisions.

---

## Validation plan

1. **Manual refactor (this RFC):** Refactor 3-5 ezt-designer concepts into the new format. Document friction points. Feed back into RFC before merging.
2. **A/B eval:** Run existing eval suite against ezt-designer pack in current form vs. with refactored subset swapped in. Measure hit rate delta and token efficiency.
3. **EK ratio measurement:** Compare EK ratio of refactored subset vs. original. Expected: equal or higher density.
4. **Production trial:** If evals pass, migrate full ezt-designer pack. Monitor EP MCP retrieval quality over subsequent eval runs.
5. **Cross-pack validation:** Apply same refactor pattern to a person pack (e.g., brian-gpt) to verify the pattern generalizes beyond product packs.

---

## Resolved design decisions

Original open questions, resolved and folded into the spec above:

1. **Chunker tuning** — RESOLVED. Verified against `ExpertPack_MCP/ep_mcp/index/chunker.py`: chunker splits consistently at `##` and `###` boundaries when a file exceeds `max_tokens`, with file-title prefixes preserved on each split. The atomic-conceptual format aligns with this behavior by design; no chunker changes required.
2. **Cross-cutting FAQ ownership** — RESOLVED. Each Q/A lives in the primary concept it answers for; other concepts cross-link via `## Related Concepts`. Duplication is forbidden (would re-introduce aggregator-style displacement). Codified in the §Optional sections spec above.
6. **Concept hierarchy / composition** — RESOLVED. Optional `parent_concept:` frontmatter field. `concept_scope: single | composite` distinguishes atomic concepts from parents spanning children. Codified in §File structure and in the granularity guide.
7. **Declarative knowledge section** — RESOLVED. Optional `## Key Propositions` section preserved for concepts with genuinely axiomatic statements. Codified in §Optional sections.
8. **Workflow vs. concept boundary** — RESOLVED. Explicit boundary rule in §Workflow vs. concept boundary above and detailed table in the granularity guide.
9. **Size targets** — RESOLVED. Soft target 500–900 tokens; hard ceiling 1,500 tokens; lower bound ~200 tokens (below which prefer embedding). Codified in §Size targets.
10. **Deprecation / supersedes tracking** — RESOLVED. Optional `supersedes:` frontmatter field. `ep-validate` warns when both new and deprecated files coexist. Codified in §Deprecation tracking.
11. **Granularity decision tree** — RESOLVED. Full decision procedure + 8 worked examples shipped in [`schemas/references/granularity-guide.md`](../references/granularity-guide.md).
12. **Residual glossary** — RESOLVED. A lean, optional `glossary.md` is permitted at the pack root for genuinely cross-cutting terms, explicitly scoped as an author/agent navigation aid rather than a retrieval layer. Codified in §Removed / deprecated.

## Deferred (follow-up work)

3. **Entity/reference files** (`entities.json`, lookup tables). DEFERRED to a follow-up RFC. This RFC is scoped to markdown concept organization; JSON navigation/index files serve a different purpose and remain unchanged.
4. **Person pack verbatim/summary pattern.** DEFERRED to a follow-up RFC (RFC-002, prospective). Person packs use a verbatim↔summary mirroring pattern that interacts non-trivially with the atomic-conceptual model. Product packs migrate first; person-pack schema v4 consequences will be addressed separately after product-pack migration proves out.
5. **`_graph.yaml` changes** and `ep-graph-export.py` tooling. DEFERRED pending first product-pack migration. Will revisit once a real Schema 4.0 pack exists to observe the graph topology it produces.

---

## Decision log

- **2026-04-17:** Deleted `summaries/`, `propositions/`, `sources/` from ezt-designer v2.1.0 — measurable retrieval improvement. Promoted to standing rule in MEMORY.md.
- **2026-04-18:** This RFC drafted. Scope: schema-level formalization of the atomic-conceptual pattern for product packs.
- **2026-04-18:** Validation refactor completed — 3 concepts (`territory`, `workload-partitioning`, `capacity-planning`) refactored into the proposed format. Artifacts in `ExpertPacks/ezt-designer/_schema-refactor/`. Findings folded into Open Questions (§6–§12). Core pattern validated; remaining work is schema-level guidance for granularity, hierarchy, and workflow/concept boundaries.

---

## Validation findings (2026-04-18 refactor)

Three concepts refactored into `ExpertPacks/ezt-designer/_schema-refactor/concepts/`:

- `territory.md` (~720 tokens) — high-interconnection stress test; pulled from 5 source files
- `workload-partitioning.md` (~680 tokens) — algorithm/tradeoff content with sibling-concept overlap
- `capacity-planning.md` (~520 tokens) — modeling-focused, tightest scope

**Confirmed working:**
- Retriever-friendly opening paragraphs produce clean definitional anchors
- `## Frequently Asked` with H3 per question creates strong query-match chunks
- Co-locating related terms + wikilinks feels natural and removes the cross-file stitch tax
- Files comfortably stay under 1,500 token ceiling; 500-800 is the natural range

**Confirmed friction points (now reflected in Open Questions):**
- Granularity judgment is the hardest part of authoring (→ §11 granularity guide needed)
- Concept hierarchies want explicit frontmatter (→ §6 `parent_concept` field)
- Propositions-as-prose loses crispness for logical extraction (→ §7 optional `## Key Propositions`)
- Workflow-vs-concept tension is real and persistent (→ §8 explicit boundary rule)
- Old aggregator files need formal deprecation markers (→ §10 `supersedes:` field)

Full source mapping and friction analysis in `ExpertPacks/ezt-designer/_schema-refactor/NOTES.md`.

---

*Schema target: 4.0 (MAJOR bump — breaking structural change to directory layout)*
