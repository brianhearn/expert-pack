# CHANGELOG

All notable changes to the ExpertPack framework. Follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) conventions.

Schema versions use the format `core.X.Y` for core schema and `type.X.Y` for type-specific schemas.

---

## [Unreleased]

### Added
- **Ontology suggestion CLI** — added `tools/ontology-suggest/ep-ontology-suggest.py`. It builds on the compact AKS projection plus existing `requires:` / `related` edges to propose review-first category nodes, repeated domain entities/terms, and explicit graph edges. Output is suggestions only (`ontology-suggestions.yaml` by default); maintainers accept/reject into `ontology.yaml`, the new accepted ontology registry (`schemas/registry/ontology.schema.yaml`).
- **AKS export-readiness gates** — `ep-validate.py --aks` now checks whether content files can produce complete compact Agent Knowledge Schema rows (stable IDs, freshness metadata, stored content hashes, and canonical-statement surfaces). `ep-micro-record-export.py` now supports `--strict` and `--report-json` for CI/export gates; `--strict` exits nonzero when exportable content would be skipped.
- **Agent Knowledge Schema (AKS) v1** — added `schemas/registry/agent-knowledge.schema.yaml` and `schemas/registry/README.md`. AKS formalizes the compact provenance-first JSONL shape for grounded agent retrieval pipelines: stable `id`, `canonical_statement`, `title`, `type`, `pack`, `canonical_path`, `source_span_uri`, `content_hash`, `source_checksum`, plus optional verification and graph fields.
- **Compact provenance-first micro-record export** — `tools/micro-record-exporter/ep-micro-record-export.py --compact` now emits lean JSONL for token-efficient agent pipelines. Compact records keep the fields agents need for deterministic grounding (`id`, `canonical_statement`, `type`, `pack`, `source_span_uri`, `content_hash`, `verified_at`, `requires`, `related`) without the full JSON-LD envelope. Full exports also promote provenance fields (`content_hash`, `verified_at`, `recorded_at`, `valid_from`) to top-level while preserving the nested `provenance` block for registry compatibility.

---

## [Core 4.1] — 2026-04-19 — Atomic-Conceptual Refinement (`requires:` dependencies)

**Minor version bump.** Refines the v4.0 atomic-conceptual model after the first real post-territory migration surfaced that the composite parent-child pattern added ceremony without retrieval gain. Schema v4.1 keeps every v4.0 deprecation (summaries, propositions directories, per-domain glossary, standalone faq) and strengthens the single-atom principle.

### Added
- **`requires:` frontmatter field** — directional dependencies between atoms. `A requires B` means B's content is needed to understand A; asymmetric. EP MCP expands a matched atom's context to include its `requires:` chain at retrieval time (depth cap 2, count cap 3 atoms total per expansion, token-budget cap).
- `schemas/rfcs/RFC-001-atomic-conceptual-chunks.md` — appended "v4.1 refinement" section documenting why composite hierarchy was retired.
- `schemas/references/granularity-guide.md` — new "Splitting oversized concepts" section with v4.1 decision procedure and an Authentication worked example.

### Changed
- **Size ceiling tightened: 1,500 → 1,000 tokens** for concept files. Concepts exceeding the ceiling split into independent atoms (not parent-child file groups).
- Soft target tightened to 500–800 tokens per concept file.
- Lower bound raised: ~250 tokens (from ~200).
- `schemas/core.md` § Atomic-Conceptual Content Files rewritten for v4.1 model.
- `schemas/product.md` and `schemas/process.md` atomic-conceptual pointers updated to reference v4.1 semantics.
- Granularity guide Example 7 ("Simple Partitioning") rewritten from composite-embed to promote-with-`requires:`.
- All `1,500`-token references in core.md and granularity-guide.md updated to `1,000`.

### Deprecated
- **`concept_scope: composite`** — removed from schema. Concepts that used composite hierarchy split into independent atoms with `requires:` dependencies.
- **`parent_concept:`** frontmatter field — removed.
- **`## Key Propositions`** section — deprecated. Body prose carries propositions; the separate section was a retrieval hack for the aggregator era. Existing atoms may keep it until next revision.

### Migration notes
- Packs already at v4.0 with no composite atoms and no `## Key Propositions` sections: bump manifest `schema_version: 4.1` after validator clears. No content changes needed.
- Packs with composite atoms: split the composite parent and its children into independent atoms. Add `requires:` links where a child was truly unintelligible without the parent.
- The ezt-designer pack had one v4.0 atom (`territory.md`) at the time of this bump; it's already v4.1-compatible.

### Tools
- `tools/validator/ep-validate.py` — new check `W-V41-01` flags concept files exceeding 1,000 tokens; `W-V41-02` flags `concept_scope: composite` and `parent_concept:` as removed fields; `W-V41-03` notes `## Key Propositions` as deprecated (warning, not error).
- `tools/migrate/ep-migrate-3-to-4.py` — renamed to `ep-migrate-3-to-4.py` still; plan output now targets v4.1 shape by default.

---

## [Core 4.0] — 2026-04-18 — Atomic-Conceptual Chunks (RFC-001)

**Breaking change** — MAJOR version bump. Product and process packs adopt a single self-contained content model; v3.x aggregator directories are deprecated. Person packs retain their verbatim↔summary model pending a follow-up RFC.

### Added
- `schemas/rfcs/RFC-001-atomic-conceptual-chunks.md` — Accepted RFC documenting the atomic-conceptual content model: one concept = one self-contained file carrying definition, body, FAQs, related terms, and key propositions. Records motivation, resolved design decisions, migration plan, and validation findings.
- `schemas/references/granularity-guide.md` — Companion reference for the hardest authoring decision: embed a term vs. promote it to its own concept file. 5-test decision procedure, 8 worked examples from the ezt-designer validation refactor, plus boundary tables for concept-vs-workflow, concept-vs-term, and concept-vs-FAQ.
- `schemas/core.md` — New `## Atomic-Conceptual Content Files` section documenting concept file structure, required/optional sections (`## Frequently Asked`, `## Related Terms`, `## Key Propositions`, `## Related Concepts`), size targets (500-900 soft / 1,500 hard), granularity, composite concepts (`concept_scope: composite` + `parent_concept:`), workflow-vs-concept boundary, deprecation tracking (`supersedes:`), and optional lean root-level `glossary.md`.
- `schemas/core.md` — New frontmatter fields: `concept_scope`, `parent_concept`, `schema_version`, `supersedes`.
- `tools/migrate/ep-migrate-3-to-4.py` — Migration planner. Scans a v3.x pack and emits `_migration-plan.md` covering deprecated-directory inventory, FAQ relocations (heuristic), glossary term embed-vs-promote suggestions, lead-blockquote removals, concept-file renames (drop `con-` prefix), and oversized-file warnings. Plan mode only; `--scaffold` and `--apply` stubbed pending first real migration to validate the plan format.

### Changed
- `schemas/core.md` — Replaced v3.x `## Retrieval Optimization` section (which contained Summaries Directory, Lead Summaries, Glossary, Propositions Directory, and File Splitting subsections) with the new `## Atomic-Conceptual Content Files` section. Net -44 lines.
- `schemas/core.md` — Updated scaffolding sequence, type registry (dropped `faq`/`proposition`/`summary` types for non-person packs), EK ratio measurement (now pulls propositions from concept-file `## Key Propositions` sections and body prose).
- `schemas/product.md` — Removed `summaries/`, `propositions/`, and `sources/` directory blocks. Rewrote `## Retrieval Layers` section as pointer to core.md. Reframed `## Sources Directory` as DEPRECATED. Converted `### FAQ File` template into v4.0 embedded-in-concepts guidance. Updated directory tree and customer-flow description.

### Deprecated
- `summaries/` directory (product/process packs) — content absorbed into concept-file opening paragraphs.
- `propositions/` directory — content absorbed into concept-file body prose and optional `## Key Propositions` sections.
- `sources/` ingestion-artifacts directory — source-provenance tracking lives in per-file `verified_at`/`source:` frontmatter and pack-level `sources/_coverage.md`.
- Per-domain `glossary-{domain}.md` files — terms either earn standalone concept files or embed as `## Related Terms`. A lean, optional `glossary.md` at pack root remains for cross-cutting terms only.
- Standalone `faq/` directory for per-concept FAQs — FAQs move into primary concept files' `## Frequently Asked` sections. Cross-cutting FAQs may remain in `faq/` sparingly.
- Lead-summary blockquote pattern — opening paragraph of concept file is the summary.

### Validation
- Validation refactor completed against `ezt-designer` pack: 3 concepts (`territory`, `workload-partitioning`, `capacity-planning`) refactored into atomic-conceptual format and stored at `ExpertPacks/ezt-designer/_schema-refactor/` (now superseded by real migration).
- First production migration: `ezt-designer/concepts/territory.md` deployed to GitHub main, superseding `con-territories-overview.md`, `con-territories-geometry.md`, `faq/faq-territory-overlaps.md`, `faq/faq-stuck-zip-codes.md`, and `glossary-territory-markup.md`. Pack file count 296 → 292. Eval pipeline will measure retrieval impact on next scheduled run.

### Deferred
- `schemas/person.md` v4.0 migration — person packs use a verbatim↔summary mirroring pattern that interacts non-trivially with the atomic-conceptual model. RFC-002 will address person-pack consequences after product-pack migration proves out.
- `schemas/process.md` v4.0 migration — same atomic-conceptual model applies; schema updated in-place but broader process-pack migration deferred until a real process pack proves the pattern.
- `entities.json` and lookup-table reconsideration.
- `_graph.yaml` tooling updates — will revisit once a real Schema 4.0 pack exists to observe graph topology.
- Example packs under `packs/` (`blender-3d`, `home-assistant`, `solar-diy`) remain in v3.x format as legacy demonstrations. A separate migration pass will modernize them.

---

## [Core 3.3] — 2026-04-14 — MCP Configuration

### Added
- `schemas/core.md` — New `mcp` block in `manifest.yaml` spec: `mcp.instructions`, `mcp.prompts`, and `mcp.resources` fields. Enables EP MCP to serve packs as full expertise injection layers (orientation via `instructions=`, foundational context via Resources, workflow guidance via Prompts).
- `schemas/core.md` — New `## MCP Configuration` section documenting the three MCP primitives, their EP source mapping, per-field guidance, pack-type applicability (product/process/person/composite), auto-discovery fallback for prompts, validator rules (W-MCP-01/02/03, E-MCP-01), and a full example.
- `schemas/core.md` — Validator rules table for MCP block: source file type/atomic checks, instructions length warning.

### Design Rationale
- The `mcp` block is universal — defined in `core.md`, applies to all pack types. Product, process, person, and composite packs all expose the same three MCP primitives; content varies by type.
- `mcp.prompts` maps to `type: workflow` + `retrieval_strategy: atomic` files — the schema already marked these as the right candidates. The prompts block is the explicit name mapping; EP MCP auto-discovers when omitted.
- `context.always` tier is the natural source for MCP Resources — same files the pack author already said load every session.

---

## [Core 3.1.1] — 2026-04-10 — Schema REFINE/OPTIMIZE Pass

### Changed
- `schemas/core.md` — Retired `relations.yaml` section (superseded by `_graph.yaml`); trimmed Chunking Strategy ~60%; consolidated duplicate Provenance sections under single `## Provenance` header; removed inline OpenClaw config JSON (replaced with pointer to guides); collapsed `_access.json` to pointer; replaced Eval-Driven Improvement section with pointer; updated Shared Principles Summary table
- `schemas/person.md` — Collapsed Story Intake Workflow to 3 lines + pointer; replaced 14-step playbook with key principles + pointer; added full `_access.json` docs + expanded Tags Taxonomy stubs
- `schemas/product.md` — Extracted Interface Reference Tables to new `schemas/references/interface-vocabulary.md`; replaced 50-line "Creating a New Product Pack" playbook with compact pointer; version bumped to 3.1
- `schemas/process.md` — Version/date update only (already cleanest schema)

### Added
- `schemas/agent.md` — New standalone Agent Extension schema (split from person.md)
- `schemas/references/interface-vocabulary.md` — Extracted interface reference tables from product.md

### Removed
- ~253 lines of operational/guide content that had accumulated in schema files — playbooks, inline config, and duplicated sections moved to appropriate guides or replaced with pointers

---

## [Core 3.1] — 2026-04-10 — Graph Export

### Added
- **Graph Export section** in `schemas/core.md` — `_graph.yaml` adjacency file spec
  - Format: nodes (file path + title + type) and edges (source → target + kind)
  - Edge kinds: `wikilink`, `related`, `context_hint`
  - Generation rules: derive from wikilinks, `related:` frontmatter, and `<!-- context: -->` comments
  - GraphRAG compatibility notes
- `tools/graph-export/ep-graph-export.py` — generates `_graph.yaml` from pack files
  - Parses wikilinks, `related:` frontmatter arrays, context hint comments
  - Outputs adjacency file with node metadata and typed edges

### Changed
- `guides/consumption.md` — v2.2: added "Deploy Prep: Strip Frontmatter Before Indexing" section and "Eval Discipline" section; strip-frontmatter step added to quick-start checklist
- Version bump: 3.0 → 3.1

---

## [Core 3.0] — 2026-04-10 — Provenance Metadata

### Added
- **Provenance Metadata section** in `schemas/core.md` — per-file frontmatter fields:
  - `id` — stable pack-relative path identifier (e.g. `pack-name/dir/filename`)
  - `content_hash` — SHA-256 of file body for change detection
  - `verified_at` — ISO 8601 date of last human or agent verification
  - `verified_by` — `human` or `agent`
- **Freshness block** in `manifest.yaml` spec — `refresh_cycle`, `coverage_pct`, `last_sweep`
- **Citation Response Contract** — retrieval responses should include `(file, id, hash, excerpt)` for auditable citations
- `tools/validator/ep-validate.py` — 4 new provenance checks behind `--provenance` flag:
  - `W-PROV-01` missing `id`, `W-PROV-02` missing `content_hash`, `W-PROV-03` missing `verified_at`, `W-PROV-04` missing `verified_by`
- `tools/deploy-prep/ep-strip-frontmatter.py` — strips YAML frontmatter from `.md` files before deploying to RAG platforms
  - Provenance metadata serves tooling, not retrieval; embedding it dilutes semantic similarity
  - Source files unchanged; deploy artifacts are ephemeral
  - Supports `--dry-run`, `--force`; prints per-file summary
- `tools/deploy-prep/README.md` — usage and recommended deploy pattern

### Changed
- `guides/consumption.md` — added full tuned RAG config block (`vectorWeight`, `textWeight`, `candidateMultiplier`, `minScore`) alongside minimal config
- `guides/hydration.md` — same full tuned RAG config block added
- Version bump: 2.9 → 3.0

### Design Notes
- Provenance is opt-in via `--provenance` validator flag; no regressions on existing packs
- `id` is the stable identifier for graph edges and citation references — stable across renames when updated consistently
- Strip frontmatter at deploy time (not authoring time) to keep source files as the single source of truth

---

## [Core 2.9] — 2026-04-06 — Graph View: Clean Topology

### Added
- `.obsidian/graph.json` — pre-configured graph view settings:
  - `_index.md` files excluded by default (`-_index` filter) — removes hub-spoke noise, reveals true concept topology
  - Color groups: blue=concept, green=workflow, orange=faq, red=troubleshooting
- `schemas/core.md` — `related:` frontmatter field documented as optional; enables explicit cross-links between content files for richer graph edges and agent context traversal

### Changed
- `schemas/core.md` — `_index.md` section clarified: "orientation only" role, explicit guidance that cross-section relationships belong on content files, not on index hubs
- `schemas/core.md` — `OBSIDIAN-SETUP.md` references updated; new "Graph View Configuration" and "Content Cross-Linking" sections added
- `.obsidian/OBSIDIAN-SETUP.md` — updated with graph filter notes and `related:` frontmatter guidance
- Version bump: 2.8 → 2.9

---

## [2026-04-06] — Scaffolding: .obsidian/ Required Step

### Changed
- `schemas/core.md` — added "Scaffolding a New Pack" section with explicit 10-step sequence; `.obsidian/` copy is step 2 and marked as non-optional
- `skills/expertpack/SKILL.md` — hydration steps updated to include `.obsidian/` copy as step 4
- Local `expertpack` skill also updated

---

## [2026-04-06] — ExpertPack Skill Cleanup

### Changed
- `skills/expertpack/SKILL.md` — stripped `requires`, `data_access`, and `external_services` metadata; skill is now pure instructions with no scripts, no file access, no external calls
- `skills/expertpack/scripts/` — removed `scan.py`, `distill.py`, `compose.py`, `validate.py`; these belong in `expertpack-export` (where they already exist)
- Published `expertpack@1.6.0` to ClawHub with clean security scan

---

## [2026-04-06] — Community Packs: Obsidian Ready Out of the Box

### Added
- `.obsidian/` config folder copied into each community pack directory:
  - `packs/blender-3d/.obsidian/`
  - `packs/home-assistant/.obsidian/`
  - `packs/solar-diy/.obsidian/`
- Packs are now fully self-contained Obsidian vaults — download any pack folder and open directly in Obsidian without any manual setup step

---

## [2026-04-06] — Obsidian Vault Template

### Added
- `template/` — complete Obsidian vault template for building ExpertPacks inside Obsidian
  - Full EP directory structure with stubs for every content type
  - `manifest.yaml`, `overview.md`, `glossary.md`, `Dashboard.md` pre-filled
  - Example content files for `concepts/`, `workflows/`, `troubleshooting/`, `faq/`
  - `sources/_coverage.md`, `volatile/README.md`, `eval/benchmark.yaml` stubs
  - `.obsidian/` pre-configured: Dataview + Templater enabled, relative link format
  - 5 Templater templates (concept, workflow, FAQ, troubleshooting, volatile) — frontmatter auto-populates on note creation
  - `Dashboard.md` with 7 live Dataview queries: content by type, missing frontmatter, expiring volatile, atomic files, tag browser, EK scores, file count by directory
  - `template/README.md` — quick start guide for Obsidian users covering EK ratio concept, content types, file size targets, AI agent integration
- `README.md` — added Vault Template nav link and callout in Obsidian Compatibility section

---

## [Core 2.8] — 2026-04-06 — Obsidian Compatibility

### Added
- **Per-file YAML frontmatter standard** — all content files now require `title`, `type`, `tags`, `pack` fields; `retrieval_strategy` and `ek_score` recommended
- **Type taxonomy** — 25 defined `type` values mapped to directory conventions with default `retrieval_strategy` per type
- **`.obsidian/` reference folder** — pre-configured Obsidian vault settings in repo root; includes Dataview + Templater plugin config and setup guide with example queries
- **Obsidian Compatibility section** in `schemas/core.md` — full spec for frontmatter fields, type reference table, link format policy, and what Obsidian adds
- Migrated all content files in community packs (blender-3d, home-assistant, solar-diy) and private packs (brian-gpt, ezt-designer) to include frontmatter

### Changed
- `retrieval_strategy` frontmatter key (flat) replaces legacy `retrieval.strategy` (nested); both accepted by current tooling
- Core Principles table in `ARCHITECTURE.md` — added **Obsidian-Native** principle

### Design Notes
- Link format remains standard relative Markdown (`[text](file.md)`) — not wikilinks — preserving GitHub rendering and all existing tooling
- The `.obsidian/` folder is a *reference config*: copy it into any pack directory to make that pack an Obsidian-ready vault
- Frontmatter is additive and backwards-compatible; existing consumers (RAG chunker, eval runner) are unaffected
- Obsidian adoption is zero-friction: open any EP pack folder as an Obsidian vault

---

## [2026-04-02] — Tooling: Public Eval Runner + Benchmark Pack

### Added
- `tools/eval-runner/run_eval.py` — fully rewritten as a pack-agnostic eval runner
  - `--pack` + `--eval` flags; no agent endpoint required
  - Loads pack `.md` files directly as LLM context and queries OpenRouter
  - LLM-as-judge scoring: correctness, groundedness, hallucination rate, refusal accuracy
  - Separate EK correctness metric tracking `ek_dependent` questions
  - `--dry-run` flag for YAML validation without API calls
  - Dependencies: `requests` + `pyyaml` only
- `packs/blender-3d/eval/benchmark.yaml` — 24-question benchmark eval set
  - Categories: concept, workflow, troubleshooting, gotcha, refusal
  - 5 EK-dependent questions grounded in actual pack content
- `tools/eval-runner/README.md` — updated with usage, metrics explanation, YAML authoring guide

### Changed
- `ARCHITECTURE.md` — synced all schema version references to current (core 2.7, person 1.6, composite 1.1, eval 1.2); updated repo structure diagram with real community packs; added revision history entries for Schema 2.5–2.7

---

## [Core 2.7] — 2026-04-01 — Volatile Data Isolation

### Added
- `volatile/` directory convention for time-bound EK (pricing, API specs, leaderboards, anything with a shelf life)
- Frontmatter TTL fields: `refresh` (ISO 8601 duration), `source`, `fetched_at`, `expires_at`
- Passive staleness detection: agents check freshness at session start, not via cron
- AXIOMS.md updated: Axiom 6d reworded to permit volatile files with declared refresh paths (was too restrictive)

### Design Notes
- Volatile content is excluded from EK ratio measurement
- Static and volatile content must not coexist in the same file
- The passive approach avoids adding infrastructure; files + frontmatter TTL is the interface

---

## [Core 2.6] — 2026-03-31 — Pack–Consumer Coordination Contract

### Added
- Pack–Consumer Coordination Contract section in `schemas/core.md`
- Defines what packs must provide vs. what consuming agents are responsible for
- Clarifies authority boundaries: pack content is authoritative within its declared scope

---

## [Core 2.5] — 2026-03-27 — Schema IS the Chunker

### Changed
- Core insight: files authored as self-contained 400–800 token retrieval units require no preprocessing — the schema itself became the chunking strategy
- Hard ceiling raised to 1,500 tokens per file
- Any RAG chunker passes these files through intact, preserving structure, lead summaries, propositions, and metadata

### Removed
- `tools/schema-chunker/` — zero adoption, no deprecation burden; deleted entirely

### Validation
- Schema-aware chunker experiment: +9.4% correctness, -52% tokens on EZT Designer eval (2026-03-13)
- Led directly to this schema change

---

## [Core 2.4] — 2026-03-24 — Chunking Strategy

### Added
- Chunking Strategy section to `schemas/core.md`
- Two authoring modes: atomic (one concept per file) and sectioned (multiple `##` headers)
- Guidance on when to split vs. consolidate files

---

## [Core 2.3] — 2026-03-16 — Entity Relation Graph

### Added
- Optional `relations.yaml` for entity relation graphs
- Enables cross-referencing entities within a pack with typed relationships

### Added (Skills)
- `skills/expertpack/` — unified OpenClaw skill for ClawHub
- `skills/expertpack-eval/` — eval API scripts split from main skill
- `skills/elite-to-expertpack/` — converter for Elite Longterm Memory format
- `skills/ontology-to-expertpack/` — converter for Ontology graph format
- `skills/self-improving-to-expertpack/` — converter for Self-Improving format

---

## [Eval 1.2] — 2026-03-12 — EK Ratio as First-Class Metric

### Added
- EK ratio metric to eval schema: proportion of propositions frontier models can't answer without the pack
- Per-section EK ratio tracking
- GK bloat measurement (general knowledge that could be cut)
- `tools/eval-ek.py` — EK ratio measurement via blind probing across multiple frontier models

### Changed
- Eval schema: `v1.0 → v1.1 → v1.2` during this session

---

## [Core 2.2 and earlier] — 2026-02 through 2026-03-11

### Foundation (2026-02-13 to 2026-03-11)
- Initial ExpertPack framework: three pack types (person, product, process)
- Core principles: MD-canonical, one source of truth, small files, RAG-optimized
- Multi-layer retrieval system: summaries, propositions, lead summaries, glossary
- Three-tier context loading: always → searchable → on-demand
- Source provenance tracking with frontmatter
- Schema versioning system
- Eval framework schema (`schemas/eval.md`)
- Guides: `guides/hydration.md`, `guides/consumption.md`
- Community packs: Home Assistant (composite, EK 54%), Blender 3D (product, EK 42%), Solar DIY (composite, EK 52%)
- Apache 2.0 license
- EK ratio introduced as primary quality metric (Axioms 9–10)
- EK-first messaging and hydration triage pipeline

### Schema versions at end of this period
- `core.md`: 2.2
- `person.md`: 1.6
- `product.md`: 1.8
- `process.md`: 1.4
- `composite.md`: 1.1
- `eval.md`: 1.2

---

*This changelog tracks framework-level changes. For pack-level changes, see individual pack `manifest.yaml` files.*
