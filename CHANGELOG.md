# CHANGELOG

All notable changes to the ExpertPack framework. Follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) conventions.

Schema versions use the format `core.X.Y` for core schema and `type.X.Y` for type-specific schemas.

---

## [Unreleased]

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
