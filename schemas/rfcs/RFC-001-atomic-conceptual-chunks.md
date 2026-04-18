# RFC-001: Atomic-Conceptual Chunks

- **Status:** Draft
- **Author:** Brian Hearn (with EasyBot)
- **Created:** 2026-04-18
- **Target:** Schema 4.0 (MAJOR bump)
- **Supersedes:** Portions of Retrieval Optimization section in `schemas/core.md` (summaries directory, propositions directory, separate FAQ directory, lead summary pattern)

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
concept_scope: single
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

4. **`## Frequently Asked`.** Include when the concept has documented questions that users actually ask. Each question as an H3 heading. The chunker splits on headings, so each Q/A becomes its own sub-chunk with strong query-matching surface.

5. **`## Related Terms`.** Include when the concept has relative terminology that doesn't stand alone. If a term has its own definition, properties, and relationships, it earns its own concept file instead.

### Removed / deprecated

- **`summaries/` directory** — deprecated. The opening paragraph of each concept file replaces this.
- **`propositions/` directory** — deprecated. Propositions are absorbed into body prose and FAQ answers.
- **Standalone `faq/` directory** — deprecated for concept-specific FAQs. Questions move into the concept file's `## Frequently Asked` section. A root `faq/` may persist for cross-cutting questions that don't belong to any single concept (e.g., "What does 'EasyTerritory' mean?"), but should be used sparingly.
- **Root-level `glossary-{domain}.md` files** — deprecated. Terms either:
  - Get promoted to their own concept file (if they stand alone), OR
  - Get embedded in the `## Related Terms` section of the parent concept (if relative)
- **Lead summary blockquote pattern** — deprecated. The opening paragraph IS the lead summary; no separate blockquote needed.

### Preserved

- `workflows/` — unchanged. Atomic retrieval strategy, step-by-step procedures.
- `troubleshooting/` — unchanged. Atomic retrieval strategy, symptom → cause → fix.
- `volatile/` — unchanged. Frontmatter TTL, time-bound content.
- `decisions/`, `specifications/`, `customers/`, `commercial/`, `interfaces/` — unchanged.
- `meta/` — unchanged. Changelog, provenance tracking.
- `overview.md`, `manifest.yaml` — unchanged structure.

### Granularity rule

**Author discretion, no frequency threshold.** A term or sub-topic earns its own concept file when it has:
- Its own definition (not just "X in the context of Y")
- Its own properties or sub-concepts
- Its own relationships to other concepts
- Content that would exceed the target size (400-800 tokens) if embedded

Otherwise, it lives embedded in the parent concept. This is a judgment call by the pack author, informed by how the domain naturally decomposes — not by eval hit frequency (which is circular and doesn't generalize to real-world usage).

### Wikilink convention

Related concept files are linked via bare-filename wikilinks (`[[concept-slug]]`, no path, no `.md` extension required but allowed). Filename uniqueness across the pack is already enforced by the existing directory-prefix convention. EP MCP's graph expansion picks up wikilinked neighbors during retrieval, reducing the need to duplicate content.

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

- `ep-migrate-3-to-4.py` — scans a pack for `summaries/`, `propositions/`, `faq/`, `glossary-*.md` and produces a migration plan (which content goes where). Interactive — asks the author about ambiguous cases (e.g., "this term could be promoted or embedded — your call").
- `ep-validate` updated to flag deprecated directories in Schema 4.0+ packs.

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

## Open questions

1. **Chunker tuning.** Does the current EP MCP chunker split consistently at `##` boundaries, or does it fall back to token windows? If the latter, larger consolidated files may re-fragment at arbitrary points. Needs verification before migration.
2. **Cross-cutting FAQs / canonical ownership.** Some questions genuinely span multiple concepts ("What's the difference between territory alignment and rebalancing?"). **Proposed resolution:** pick the primary concept and cross-link via `## Related Concepts`. Validation refactor confirmed this works — duplicating Q/A across concept files would re-introduce the aggregator problem in miniature. Schema should state this explicitly.
3. **Entity/reference files.** `entities.json`, lookup tables — unaffected by this RFC, or should they also be reconsidered?
4. **Person pack verbatim/summary pattern.** Person packs mirror verbatim files to summary files in paired directories. This RFC is scoped to product packs; person-pack consequences need a follow-up RFC.
5. **`_graph.yaml` changes.** Will the new structure produce a cleaner graph? Should `ep-graph-export.py` be updated to reflect the richer wikilink density inside concept files?
6. **Concept hierarchy / composition.** Validation surfaced the need for explicit parent-child concept relationships (e.g. `Workload Partitioning` is a sub-concept of `Partitioning`, which is a sub-concept of `Scheduling`). **Proposed:** add optional `parent_concept:` and/or `part_of:` fields to concept frontmatter. Add optional `concept_scope: composite` to flag concepts that intentionally span multiple files. Needs a dedicated section in the final schema.
7. **Declarative knowledge section.** Absorbing propositions into body prose sacrifices the crisp declarative style that was useful for logical extraction and some downstream tool uses. **Proposed:** allow an optional `## Key Propositions` or `## Principles` section in concept files when the concept has genuinely axiomatic statements worth surfacing. Keep it optional — not every concept has them.
8. **Workflow vs. concept boundary.** Validation consistently surfaced a tension: procedural "how to do X" material wants to live in `workflows/`, while concept files should stay definitional ("what it is, why it matters, key tradeoffs"). The schema should state this boundary explicitly. Rule of thumb: if it has numbered steps, it's a workflow; if it describes behavior, tradeoffs, or mental models, it's a concept.
9. **Soft vs. hard size targets.** Validation files came in at 520-720 tokens naturally. The current 1,500 hard ceiling is correct, but the 400-800 target may be too tight — richer concepts comfortably reach 900. **Proposed:** soft target 500-900 tokens; hard ceiling 1,500.
10. **Deprecation / supersedes tracking.** When `con-territories-overview.md` is replaced by `territory.md`, how do we signal this to the loader and to readers? **Proposed:** add optional `supersedes:` frontmatter field listing deprecated filenames. `ep-validate` can warn if both the new and deprecated files coexist.
11. **Granularity decision tree.** Validation showed author granularity judgment is the single hardest part of applying this schema. "Territory" wanted to swallow half the pack. The schema needs a concrete decision tree with worked examples of embed-vs-promote calls. **Proposed:** add a `schemas/references/granularity-guide.md` reference document with 10-20 worked examples.
12. **Residual glossary.** Even with concept-level `## Related Terms`, some high-frequency cross-cutting terms (e.g. "EasyTerritory" itself, industry vocabulary) may benefit from a lightweight `glossary.md` index. **Proposed:** allow an optional, lean `glossary.md` for truly cross-cutting terms only — not as a retrieval layer, but as a navigation aid for authors and agents.

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
