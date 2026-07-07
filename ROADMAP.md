# ExpertPack Improvement Roadmap

*Ongoing project to improve performance, accuracy, efficiency, and usability of the ExpertPack framework. Started 2026-03-05.*

---

## Vision

Make ExpertPacks measurably better across all pack types (person, product, process) — faster retrieval, fewer tokens, less hallucination, easier to build, and continuously improving as LLMs advance.

## Principles

- **Framework-first** — improvements live in the schema/framework, not buried in one pack
- **Pack-type agnostic** — everything should work for person, product, and process packs equally
- **Measurable** — no vibes-based "improvement"; every change needs a before/after metric
- **Test with real packs** — validate improvements against actual deployed packs, not just theory

---

## Improvement Vectors

### 1. Evaluation & Metrics
Define how any pack measures quality. Without this, everything else is guessing.
- [x] **Eval framework schema** — standard format for Q&A eval sets, quality scoring
- [ ] **Pack health metrics** — schema conformance, coverage, freshness, cross-ref integrity
- [ ] **Runtime metrics** — tokens/query, latency, cost, retrieval precision
- [x] **Eval runner** — tool/script that executes eval sets and produces scorecards
- [x] **First pack baseline** — run eval against a real deployed pack to establish baseline numbers

### 2. Performance & Token Efficiency
Reduce latency and token consumption for pack-powered interactions.
- [ ] **Split oversized files** — enforce 1-3KB guideline across all packs
- [ ] **Query routing** — classify questions and scope retrieval to relevant directories
- [ ] **Summary layers** — lightweight summary files for dense reference content
- [ ] **Context tier enforcement** — runtime should respect always/searchable/on-demand tiers
- [ ] **Semantic caching** — cache frequent query patterns to avoid redundant RAG + LLM
- [ ] **Conversation-aware retrieval** — don't re-retrieve files already in context

### 3. Response Quality & Accuracy
Reduce hallucinations and improve answer completeness.
- [x] **Grounding citations** — Citation Response Contract (schema v3.0); provenance `id` + `verified_at` fields enable auditable citations
- [ ] **Confidence tagging** — content-level confidence (expert-verified, crawled, inferred)
- [ ] **Contradiction detection** — surface conflicting chunks at runtime instead of guessing
- [x] **Hallucination measurement** — automated detection via LLM-as-judge against pack content
- [x] **Claim-to-span verification** *(shipped 2026-04-15)* — `tools/eval-runner/claim_verifier.py`: post-processor that extracts claims from any completed eval result, verifies each against pack spans, and appends `claim_coverage` + `citation_f1` to both per-question details and aggregate scores. Run after `run_eval.py` to get grounding metrics on any result file.
- [x] **Schema registry** *(shipped 2026-04-15)* — `schemas/registry/`: descriptive registry specs for compact AKS export and accepted ontology (`agent-knowledge.spec.yaml`, `ontology.spec.yaml`) plus usage guide. Markdown remains canonical; `.spec.yaml` files are ExpertPack-native specs rather than JSON Schema/OpenAPI.

### 4. Pack Creation & Training
Make it easier to build and maintain packs.
- [x] **Pack scaffolding CLI** — `expertpack init <slug> --type product` scaffolds from `template/`, substitutes the manifest, backfills provenance, and validates. Unified `tools/cli/expertpack.py` also wraps validate/doctor/checksum/chunk-annotate/migrate.
- [x] **Validation tool** — `ep-validate.py` (strict frontmatter gate + provenance + chunk checks) + `ep-doctor.py` (auto-fix: links incl. broken-wikilink removal, fm, hash backfill, prefix). Ships in `tools/validator/`.
- [ ] **Guided interview mode** — agent-driven structured knowledge capture
- [ ] **Population playbooks** — interactive recipes per source type

### 5. Schema Evolution
Keep the framework current as LLMs advance.
- [x] **Atomic-conceptual chunks** *(shipped Core 4.0, 2026-04-18; refined Core 4.1, 2026-04-19)* — RFC-001: concept files are self-contained retrieval units carrying definition, body, FAQs, related terms in one file. Deprecated `summaries/`, `propositions/`, per-domain `glossary-{domain}.md`, standalone `faq/` directory, and lead-summary blockquote pattern for product/process packs.
  - **v4.1 refinement (2026-04-19):** Retired the composite parent-child pattern (`concept_scope: composite` + `parent_concept:`) in favor of strict single-file atoms linked by directional `requires:` dependencies. Tightened size ceiling from 1,500 to 1,000 tokens. Deprecated `## Key Propositions` section (body prose already carries them). Validator checks added: W-V41-01..05. EP MCP retrieval expansion (depth 2, count 3, token-budget capped) to be implemented as the next milestone. Person-pack consequences deferred to RFC-002.
- [x] **EP MCP `requires:` expansion** — implemented in EP MCP 0.4. Top-K atoms expand their directional `requires:` chain after slicing (depth 2, count 3, token-budget capped), so v4.1 atomic semantics land end-to-end.
- [ ] **RFC-002: person-pack atomic-conceptual adaptation** — verbatim↔summary mirroring in person packs interacts non-trivially with the RFC-001 model. Needs dedicated RFC after product-pack migration proves out.
- [ ] **Context-tier compaction** — ruthlessly compress Tier 1 to identity+voice+navigation only (<5KB); push everything else to Tier 2/3. Audit current packs for tier discipline.
- [ ] **Structured fact tables** — replace narrative repetition with key/value facts, decision tables, canonicalized terms/glossaries for deduplication and retrieval precision
- [ ] **Entity cross-reference indexes** — use entities.json as canonical registry with aliases for term normalization (evaluate whether current RAG actually benefits)
- [ ] **File size flexibility** — revisit 1-3KB for large-context models; maybe a "dense mode"
- [x] **Chunking strategy review** — We built and validated a schema-aware chunker that respected structural elements like headers, lead summaries, proposition groups, and glossary tables. This produced +9.4% correctness and -52% tokens on EZT Designer eval (2026-03-13). The core insight led directly to Schema 2.5: files authored as self-contained 400–800 token retrieval units require no preprocessing — the schema itself became the chunking strategy.
- [x] **Volatile data isolation** — Schema 2.7 (2026-04-01): `volatile/` subdirectory with TTL frontmatter fields (`refresh`, `source`, `fetched_at`, `expires_at`); excluded from EK ratio measurement.
- [x] **Obsidian compatibility** — Schema 2.8 (2026-04-06): per-file YAML frontmatter standard, 25-type taxonomy, `.obsidian/` vault config, Dataview + Templater templates. Every pack is a valid Obsidian vault.
- [x] **Provenance metadata** — Schema 3.0 (2026-04-10): per-file `id`, `content_hash`, `verified_at`, `verified_by`; manifest `freshness` block; Citation Response Contract; `--provenance` validator flag (W-PROV-01..04). All 7 packs backfilled (537 files total).
- [x] **Graph export** — Schema 3.1 (2026-04-10): `_graph.yaml` adjacency file; `ep-graph-export.py` parses wikilinks + `related:` frontmatter + context hints into typed edges. GraphRAG-compatible.
- [x] **Deploy-prep tooling** — `ep-strip-frontmatter.py` (2026-04-10): strips frontmatter before RAG deploy to prevent provenance metadata diluting embeddings. Source files unchanged.
- [ ] **Shared entities across packs** — canonical entity IDs (`entity:<slug>`) declared in `manifest.yaml` or `entities.json` so `ep-graph-export` can emit cross-pack edges for people, organizations, products, and locations that appear in multiple packs. Enables multi-pack GraphRAG traversal and cross-vault Obsidian linking. Initial review-first `ep-ontology-suggest.py` now proposes candidate entities/categories from AKS + graph edges; accepted registry format now exists as `ontology.yaml`, and graph export now consumes it into `_graph.yaml` as ontology/entity edges.
- [ ] **OpenClaw EP retrieval plugin** — a pluggable retrieval interface (when OC supports it) that uses EP frontmatter (provenance `id`, `related:`, `type:`, graph edges) for retrieval scoring and graph traversal, but strips frontmatter from chunks before injecting into context. EP MCP now covers the generic runtime side, including reconstruct mode; OpenClaw-native integration remains a separate future plugin.
- [x] **Bi-temporal provenance model** *(shipped Schema 3.4, 2026-04-15)* — `valid_from` (world truth date) + `recorded_at` (ingestion date) added to frontmatter spec and micro-record schema. W-PROV-05 validator rule added. Both fields optional; most valuable for product feature / policy files with a clear real-world effective date.
- [x] **Hybrid KG + vector micro-records export** *(shipped 2026-04-15; AKS compact provenance-first mode 2026-05-05)* — `tools/micro-record-exporter/ep-micro-record-export.py`: generates JSONL of micro-records from any pack. Reads frontmatter + `_graph.yaml`; prefers lead summary blockquote for `canonical_statement`, falls back to first prose paragraph, optionally uses LLM via `--generate-statements`. `--compact` emits a formal Agent Knowledge Schema (AKS v1) row with first-class provenance fields for token-efficient pipelines. Pilot run: EZT Designer 295 records, 153 edges, 226KB. Optional next step: load JSONL into SQLite/FalkorDB triple store for deterministic ID lookups alongside vector search.
- [x] **EP MCP: graph traversal queries** *(verified 2026-04-15)* — `ep_graph_traverse_tool` already fully implemented and deployed. BFS up to depth 3, all edge kinds (wikilink, related, context), returns connected nodes with title/type/depth/edge_kind. Smoke tested: `wf-capacity-planning-overview` depth-2 traversal surfaces 7 connected nodes (scheduling algorithms, workload partitioning concepts, 2 related workflows) via 8 edge traversals. No code work needed — this item was already done.
- [x] **Ontology suggestion assist** *(initial shipped 2026-05-05)* — `tools/ontology-suggest/ep-ontology-suggest.py` proposes review-first category/entity suggestions from AKS records and existing graph edges. Maintainers accept/reject suggestions; accepted entries live in `ontology.yaml`; no automatic ontology mutation.
- [ ] **Agentic RAG patterns** — multi-step retrieval, query refinement *(two-pass retrieve→focus flow from intelligence sweep #3, 2026-04-15)*
- [ ] **Minimum capability declarations** — manifest field for required model capabilities
- [ ] **Regular schema review cadence** — triggered by major model releases

### 6. Continuous Intelligence
Stay current with developments that could improve the framework.
- [x] **X daily scan** — Already running (captures design learnings)
- [x] **Weekly web intelligence sweep** — Wednesdays 14:00 UTC, GPT-5 Mini, logs to logs/expertpack-intelligence.md
- [ ] **Schema review triggers** — flag when new model capabilities make assumptions revisitable

---

## Status Log

### 2026-07-06 — Top-5 improvements: enforcement, provenance, chunking, typed answers, onboarding
- **Strict validator (`ep-validate --strict`):** turns the frontmatter contract into a hard gate. Implies `--provenance` and promotes required-field, hash, size, and provenance rules from WARN to ERROR (`title`/`type`/`tags`/`pack`/`id`/`schema_version`/`retrieval_strategy`/`verified_at`/`content_hash`, W-PROV-02/05, W-V41-01, manifest `schema_version`). Added `--fail-on-warn` and `--ignore CODE` (demote a tracked backlog). Implemented the previously-documented W-PROV-05. Fixed cross-platform UTF-8 file/stdout handling so the tools run on Windows.
- **Doctor backfill (`ep-doctor --fix hash`):** minimal textual insertion of `id`/`schema_version`/`retrieval_strategy`/`verified_at`/`content_hash`. Backfilled all three demo packs and the template; every target now passes `--strict` (`packs/*` with `--ignore W-V41-01` for the oversized-concept backlog awaiting the atomic-split sprint).
- **Hard gates:** `.github/workflows/validate.yml` (template + per-pack matrix), `.pre-commit-config.yaml`, `tools/validate-all.py`, and `tools/ingest-gate.py` (validate → strip → export). No pack enters the index without passing `--strict`.
- **Machine-readable schema:** `schemas/registry/frontmatter.spec.yaml` + `frontmatter.schema.json` (JSON Schema 2020-12) — validated against all 94 content files.
- **Reconstruct Mode (RFC-003):** fragment provenance contract added to `schemas/core.md` and `schemas/rfcs/RFC-003-fragment-provenance-reconstruct-mode.md` (content-addressed `fragment_id`, `line_range`, span hash, `stale`). AKS spec extended with `fragment_id`/`line_range`/`span_hash`. The OpenClaw plugin sends `reconstruct` and surfaces the returned provenance; EP MCP ships the runtime envelope (`ep-mcp` commit `a9d1639`, 2026-07-06). Production packs require reindex after deploy for accurate `fragment_id` / `stale`.
- **Semantic chunk sidecars (RFC-004):** `tools/chunker/ep-chunk-annotate.py` generates header-aware `<name>.chunks.yaml` sidecars (git-tracked, out of the embeddable body). Format spec in `schemas/registry/chunk-sidecar.spec.yaml`; validator adds `W-CHUNK-01..03`; CI runs `--check` for drift. Sidecars generated for the oversized atomic/reference files across all three demo packs. EP MCP consumes sidecars at index time for deterministic boundaries (`ep-mcp` commit `a9d1639`, 2026-07-06).
- **Typed Answer Contract (TAC v1):** machine-verifiable response envelope where every claim maps to a retrieved source fragment (`supported`/`partial`/`unsupported`). Spec in `schemas/registry/typed-answer.spec.yaml` + `typed-answer.schema.json` (JSON Schema 2020-12); agent prompt in `templates/TAC-PROMPT.md`; TypeScript types in `tools/openclaw-memory-plugin/src/tac-types.ts`. `tools/tac/validate_tac.py` enforces the structural + semantic contract (every claim grounded, `reconstruct` requires `fragment_id`); `claim_verifier.py --tac` scores envelopes in the eval pipeline. TAC is the response layer on top of RFC-003 retrieval.
- **Guided onboarding CLI:** `tools/cli/expertpack.py` is one entrypoint over the existing tools — `init` (scaffold + provenance backfill + validate), `validate`, `doctor`, `checksum`, `chunk-annotate`, and `migrate obsidian|v3-to-v4`. Optional `pip install -e .` exposes it as `expertpack`. Added `template/DESIGN.md` (scope/audience/non-goals/decisions) and `template/TOOLS.md` (retrieval, MCP tools, workflows) starter docs. The Obsidian converter now emits `_migration-report.md` (ambiguous types, oversized files + split suggestions, provenance backfill). Consolidated the never-shipped `ep-fix-broken-wikilinks.py` into `ep-doctor --fix links` (composite-safe broken-wikilink removal; also stopped mis-converting `.md` URLs) and fixed the dangling references across the skills docs.

### 2026-04-18 — Schema v4.0 shipped (RFC-001 atomic-conceptual chunks)
- **RFC-001 accepted:** `schemas/rfcs/RFC-001-atomic-conceptual-chunks.md`. Concept files become self-contained retrieval units; aggregator directories (`summaries/`, `propositions/`, `sources/`, per-domain `glossary-*.md`) deprecated for product/process packs.
- **Schemas bumped to 4.0:** `core.md` and `product.md` updated in-place. Replaced 180+ lines of v3.x Retrieval Optimization guidance with a single `## Atomic-Conceptual Content Files` section. New frontmatter fields: `concept_scope`, `parent_concept`, `schema_version`, `supersedes`.
- **Granularity guide:** `schemas/references/granularity-guide.md` — 8 worked examples from ezt-designer validation refactor, 5-test decision procedure, boundary tables for the three hardest authoring decisions (concept-vs-workflow, concept-vs-term, concept-vs-FAQ).
- **Migration tool:** `tools/migrate/ep-migrate-3-to-4.py` (plan mode). Tested against ezt-designer: 60 rename candidates, 33 glossary term decisions, 42 FAQ Q/A relocations, 2 oversized files flagged.
- **First production migration:** `ezt-designer/concepts/territory.md` live on `ExpertPacks/main`. Supersedes 5 legacy files (territories-overview, territories-geometry, territory-overlaps FAQ, stuck-zip-codes FAQ, glossary-territory-markup). Pack 296 → 292 files. Eval pipeline will measure retrieval impact on next scheduled run.
- **Deferred:** person-pack adaptation (RFC-002), example-pack migrations under `packs/` (blender-3d, home-assistant, solar-diy remain v3.x demos), `--scaffold`/`--apply` modes in the migration tool.

### 2026-03-05 — Project Kickoff + Baseline Captured
- Defined the six improvement vectors
- Decision: start with eval framework (Vector 1) as foundation for everything else
- Decision: framework-first, pack-type agnostic approach
- Completed eval framework schema (`schemas/eval.md`) with eval dimensions concept
- Built eval runner + scorer scripts (`ExpertPacks/ezt-designer/eval/run-eval.py`, `score-eval.py`)
- First eval set built (50 questions, 8 categories) for EZT Designer product pack
- Set up weekly web intelligence sweep cron (Wednesdays 14:00 UTC)
- **BASELINE CAPTURED:** 50/50 questions, 0 errors
  - Correctness: 79% | Completeness: 3.8/5 | Hallucination: 10% (5/50) | Refusal: 0% (0/8)
  - Tokens: avg 4,372 in / 840 out / 9,348 total per question | 467K total
  - Model: GPT-5 Mini via OpenRouter | Avg latency: 21.8s
  - Results: `ExpertPacks/ezt-designer/eval/baselines/2026-03-05-baseline.yaml`
- **Key findings:**
  - Concept (94%) and Comparison (94%) categories are strong
  - Refusal accuracy is 0% — bot never declines out-of-scope questions
  - 5 hallucinations: q028 (invented flag names), q037 (oversold), q041 (false export guarantee), q047 (AAD details), q048 (fabricated tech stack)
  - Weak retrieval for q009, q014, q019 — right content exists but wasn't found
- **Improvement plan (in order):**
  1. Agent training (SOUL.md refusal + grounding rules) → re-eval
  2. Pack structure (split oversized files) → re-eval
  3. Content gaps (missing docs, disambiguation layer) → re-eval
  - Each step = one dimension change for clean attribution

### 2026-04-02 — Public eval runner + blender-3d benchmark pack
- Refactored `tools/eval-runner/run_eval.py` to be fully pack-agnostic (accepts --pack + --eval flags, loads pack files as context)
- Created `packs/blender-3d/eval/benchmark.yaml` with 24 questions across concept/workflow/troubleshooting/refusal/gotcha (grounded in actual pack files read during creation)
- Updated `tools/eval-runner/README.md` with new usage, deps (requests+pyyaml), metrics explanation
- Design decision: kept simple (no heavy deps, direct OpenRouter calls, no live eval run per constraints)

### 2026-04-06 — Obsidian compatibility + validator tooling
- **Schema 2.8** — per-file YAML frontmatter standard; 25-type taxonomy; `.obsidian/` vault config; Dataview + Templater templates
- **Schema 2.9** — `related:` frontmatter field; `.obsidian/graph.json` pre-configured with type color groups and `_index.md` exclusion filter
- `ep-validate.py` — 16-check compliance validator; `ep-doctor.py` — auto-fix (links incl. safe broken-wikilink cleanup, frontmatter, prefixes)
- All community packs (blender-3d, home-assistant, solar-diy) Obsidian-ready with bundled `.obsidian/`
- `template/` vault template — full scaffolding with 5 Templater templates and 7 live Dataview queries
- `obsidian-to-expertpack` skill published to ClawHub (v1.0.1)

### 2026-04-10 — Provenance metadata, graph export, eval baseline, deploy-prep
- **Schema 3.0 — Provenance Metadata:** per-file `id`, `content_hash`, `verified_at`, `verified_by`; manifest `freshness` block; Citation Response Contract
  - `ep-validate.py` extended to 19 checks; `--provenance` flag adds W-PROV-01..04
  - All 7 packs backfilled: ezt-designer (290), brian-gpt (119), blender-3d (35), home-assistant/product (31), home-assistant/process (23), solar-diy/product (21), solar-diy/process (18) — 537 files total
- **Schema 3.1 — Graph Export:** `_graph.yaml` adjacency file spec; `ep-graph-export.py`; wikilinks + `related:` + context hints → typed edges; GraphRAG-compatible
  - ezt-designer: 288 nodes, 152 edges | brian-gpt: 119 nodes, 5 edges
- **Tuned RAG config locked:** chunking 1000t / overlap 0 / hybrid BM25+vector / MMR λ=0.7 / maxResults 10 / minScore 0.35; documented in `guides/consumption.md` v2.2 and `guides/hydration.md`
- **Deploy-prep:** `tools/deploy-prep/ep-strip-frontmatter.py` — strips frontmatter before RAG deploy; source files unchanged
- **Eval discipline rules:** fixed 20-question benchmark set, canonical RAG config, one variable at a time (documented in guides)
- **Eval Run 11 (EZT Designer):** 81.9% correctness, 3.8/5 completeness, 4.3% hallucination, 66.7% refusal — schema v3.1, tuned RAG, GPT-5.3 Chat (23 questions with frontmatter; Run 12 will be first controlled baseline)
- **`expertpack` skill v2.0.5** on ClawHub — updated for schema v3.1 (provenance spec, graph export, 19-check validator, deploy-prep tools)

### 2026-04-15 — Graphiti analysis + intelligence sweep → roadmap additions
- Reviewed [getzep/graphiti](https://github.com/getzep/graphiti): temporal context graph engine; bi-temporal facts, provenance-first triples, hybrid retrieval (semantic + BM25 + graph traversal), MCP server with `search_facts`/`search_nodes` tools.
- **Graphiti vs EP framing:** Graphiti = dynamic agent memory (what's true now / what changed). EP = curated expertise injection (what the model can't know from weights). Complementary, not competitive.
- **3 roadmap items from Graphiti:**
  1. Bi-temporal provenance (`valid_from` + `recorded_at`) — Schema 3.4 candidate
  2. Hybrid KG + vector micro-records export — pilot with EZT Designer entities
  3. EP MCP `search_graph` tool — multi-hop traversal via `_graph.yaml`
- **3 roadmap items from intelligence sweep:**
  1. Claim-to-span verification + `citation_f1` metric — eval runner addition (finding #1)
  2. Schema registry `schemas/registry/` — YAML + JSON-LD micro-record spec (finding #5)
  3. Two-pass retrieve→focus noted on agentic RAG item (finding #3)
- No schemas or pack content modified.

### 2026-04-15 — Bi-temporal provenance, micro-records, claim verifier, schema registry, graph traversal verification

**Schema 3.4 — Bi-temporal provenance:**
- Added `valid_from` (world truth date) + `recorded_at` (ingestion date) to frontmatter spec and micro-record schema
- W-PROV-05 validator rule added; both fields optional
- Most valuable for product feature / policy files with a known real-world effective date
- Graphiti analysis was the catalyst: their temporal fact model mapped cleanly onto EP's existing provenance layer

**Hybrid KG + vector micro-records export:**
- `tools/micro-record-exporter/ep-micro-record-export.py` — generates JSONL micro-records from any pack
- Reads frontmatter + `_graph.yaml`; uses lead summary blockquote for `canonical_statement`, falls back to first prose paragraph
- `--generate-statements` flag for LLM-assisted statement generation
- Pilot: EZT Designer — 295 records, 153 edges, 226KB JSONL
- Optional next step: load into SQLite/FalkorDB for deterministic ID lookups alongside vector search

**Claim-to-span verification (eval runner addition):**
- `tools/eval-runner/claim_verifier.py` — post-processor that extracts claims from any completed eval result and verifies each against pack spans
- Appends `claim_coverage` + `citation_f1` to per-question details and aggregate scores
- Run after `run_eval.py` to get grounding metrics on any result file

**Schema registry:**
- `schemas/registry/` — descriptive registry specs for AKS and accepted ontology plus usage guide
- Core schema section updated to reference registry

**EP MCP graph traversal verified:**
- `ep_graph_traverse_tool` already fully implemented and deployed — no code work needed
- Smoke tested: `wf-capacity-planning-overview` depth-2 traversal surfaces 7 connected nodes via 8 edge traversals (scheduling algorithms, workload partitioning concepts, 2 related workflows)

---

*Update this file when meaningful progress happens on any vector. This is the single source of truth for the improvement project.*
