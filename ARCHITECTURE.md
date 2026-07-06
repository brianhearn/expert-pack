# ARCHITECTURE.md — ExpertPack Framework

*What ExpertPacks are, how they work, and why they're structured this way.*

---

## The Problem

Frontier AI models know a lot about the world, but they know almost nothing about *your* product, *your* life, or *your* process. Ask an LLM about your company's software and you'll get vague, outdated, or hallucinated answers. Ask it about your grandfather and it has nothing. Ask it how to build a custom home and you'll get generic advice that misses the gotchas.

RAG helps — stuff some documents into a vector store — but raw documentation makes a poor expert. Docs are written for humans browsing, not for AI reasoning. An expert system needs something different: structured knowledge that mirrors how a veteran practitioner thinks.

That's what an ExpertPack is.

---

## What is an ExpertPack?

An ExpertPack is a structured knowledge package that gives an AI agent deep expertise in a specific domain. It's a portable, git-native, Markdown-first knowledge base designed to be consumed by AI agents and readable by humans.

ExpertPacks come in three types:

| Type | What It Captures | Example |
|------|-----------------|---------|
| **Person** | A human being — stories, mind, beliefs, relationships, voice | BobGPT — a father's life archive for his family |
| **Product** | A product or platform — concepts, workflows, troubleshooting, tribal knowledge | AcmeHQ — expert knowledge for a project management platform |
| **Process** | A complex endeavor — phases, decisions, checklists, gotchas | Building a custom home, starting a business, landscape design |

Each type follows a type-specific schema that defines its directory structure and content patterns. All types share a common set of core principles.

---

## Core Principles

These apply to every ExpertPack. See [schemas/core.md](schemas/core.md) for the full specification.

| Principle | Rule |
|-----------|------|
| **MD-Canonical** | Markdown is the source of truth for all content; JSON is navigation only |
| **One Source of Truth** | Each fact lives in exactly one place |
| **Small Atomic Files** | Concept atoms target 400–800 tokens with a 1,000-token ceiling; one dominant topic per file |
| **RAG-Optimized** | `##` section headers at natural topic breaks for quality chunking |
| **Retrieval-Optimized** | Atomic-conceptual files: one concept per file, retriever-anchored opening, FAQ surface, `requires:` dependencies |
| **Layered Loading** | Three-tier context: always → searchable → on-demand |
| **Source-Tracked** | Provenance frontmatter traces content back to its origin |
| **Cross-Referenced** | Relative markdown links between related files |
| **Obsidian-Native** | Per-file YAML frontmatter on all content files; valid Obsidian vault out of the box |
| **Schema-Versioned** | Type schemas carry semantic versions; packs declare their target |
| **Eval-Driven** | Measurable quality with standardized eval sets, automated scoring, and Typed Answer Contract (TAC) verification |
| **Enforceable Schema** | `ep-validate --strict` + CI/pre-commit gate the frontmatter contract before indexing |
| **Git-Native** | Version controlled, diffable, collaborative |
| **Never Overwrite** | Contradictions are flagged for human resolution |

---

## How Schemas Work

The schema system has two layers:

### Core Schema ([schemas/core.md](schemas/core.md)) — v4.1
Shared principles and conventions that apply to every ExpertPack:
- The MD-canonical principle
- Required files (`manifest.yaml`, `overview.md`)
- Directory conventions (`_index.md`, `_access.json`)
- File structure rules (size, naming, headers; 1,000-token ceiling for concept files)
- Cross-referencing patterns
- Layered loading strategy (three-tier context: always → searchable → on-demand)
- Atomic-conceptual content model (one concept = one file = one retrieval unit)
- `requires:` frontmatter for directional dependency expansion
- Volatile data isolation (`volatile/` directory + frontmatter TTL for time-bound EK)
- Source provenance tracking
- Fragment provenance and Reconstruct Mode (RFC-003); Typed Answer Contract (RFC/registry)
- Chunk metadata sidecars for oversized atomic/reference files (RFC-004)
- Structural validation gate (`ep-validate --strict`, ingest pipeline)
- Schema versioning system
- Conflict resolution
- Agent consumption patterns

### Type-Specific Schemas
Each pack type has its own schema that extends core with domain-specific structure:

- **[schemas/person.md](schemas/person.md)** (v4.1) — Stories, reflections, opinions, conversations, mind taxonomy, biographical facts, timeline, relationships, privacy modes, presentation (voice, appearance), reasoning and conflict handling
- **[schemas/product.md](schemas/product.md)** (v4.1) — Concepts, workflows, troubleshooting (errors, diagnostics, common mistakes), screens/interface specs, FAQ, commercial info, entity cross-references, timeline, decisions, customers, limitations, competitive landscape, mental model
- **[schemas/process.md](schemas/process.md)** (v4.1) — Phases with enhanced structure, decisions, checklists, roles, resources, examples, gotchas, exceptions, variants
- **[schemas/composite.md](schemas/composite.md)** (v1.1) — Multi-pack deployments with role assignments, context tier overrides, cross-pack conflict resolution
- **[schemas/eval.md](schemas/eval.md)** (v1.3) — Evaluation framework for measuring pack quality (response quality, retrieval quality, efficiency, pack health, TAC scoring)

### Registry Specs (`schemas/registry/`)

Machine-readable projections and response contracts that extend core without replacing Markdown as canonical:

- **frontmatter** — per-file YAML contract + JSON Schema (`--strict` gate)
- **agent-knowledge (AKS)** — compact provenance-first JSONL export
- **chunk-sidecar** — header-aware chunk boundaries for oversized atomic/reference files
- **typed-answer (TAC)** — machine-verifiable agent answer envelopes
- **ontology** — accepted entity/category registry for graph export

See [schemas/registry/README.md](schemas/registry/README.md).

A pack declares its type in `manifest.yaml`, which determines which type-specific schema applies.

---

## Packs Are Instances

A pack is an instantiation of a schema — a concrete knowledge base about a specific person, product, or process.

```
ExpertPack/
├── schemas/               ← The blueprints
│   ├── core.md            ← Shared principles (v4.1)
│   ├── registry/          ← Machine-readable specs (frontmatter, AKS, sidecars, TAC)
│   ├── rfcs/              ← Cross-repo contracts (Reconstruct Mode, chunk sidecars)
│   ├── person.md          ← Person-pack schema (v4.1)
│   ├── product.md         ← Product-pack schema (v4.1)
│   ├── process.md         ← Process-pack schema (v4.1)
│   ├── composite.md       ← Composite schema (v1.1)
│   └── eval.md            ← Eval framework (v1.3)
│
├── template/              ← Vault scaffold (DESIGN.md, TOOLS.md, Obsidian config)
│
├── guides/                ← Practical how-to guides for pack builders
│   ├── hydration.md           ← Complete hydration lifecycle
│   └── consumption.md         ← How to deploy and consume packs with AI agents
│
├── tools/                 ← Tooling for pack development
│   ├── cli/expertpack.py      ← Unified CLI (init, validate, doctor, migrate, …)
│   ├── validator/             ← ep-validate.py, ep-doctor.py
│   ├── chunker/               ← ep-chunk-annotate.py (RFC-004 sidecars)
│   ├── tac/                   ← validate_tac.py (Typed Answer Contract)
│   ├── ingest-gate.py         ← validate → strip → export pipeline
│   ├── validate-all.py        ← CI/pre-commit runner
│   ├── eval-runner/           ← Eval execution, claim_verifier (--tac)
│   ├── micro-record-exporter/ ← AKS / full micro-record JSONL
│   ├── graph-export/          ← ep-graph-export.py
│   ├── deploy-prep/           ← ep-strip-frontmatter.py
│   └── eval-ek.py             ← EK ratio measurement via blind probing
│
├── skills/                ← Agent skills for pack creation and export
│
└── packs/                 ← The instances
    ├── home-assistant/    ← Composite pack: Home Assistant (EK 54%)
    ├── blender-3d/        ← Product pack: Blender 3D (EK 42%)
    └── solar-diy/         ← Composite pack: Solar & Battery DIY (EK 52%)
```

Creating a new pack means:
1. Run `python tools/cli/expertpack.py init <slug> --type product|person|process` (or copy `template/`)
2. Edit `manifest.yaml`, `overview.md`, `DESIGN.md`, and `TOOLS.md`
3. Populate directories per the type-specific schema
4. Backfill provenance: `expertpack checksum --apply`
5. Validate: `expertpack validate --strict` (must pass before indexing)
6. Commit

---

## Retrieval Architecture

Basic RAG — embed documents, retrieve top-k chunks — works, but it leaves precision and token efficiency on the table. ExpertPacks (schema v4.0+) solve this through **atomic-conceptual content files**: each concept is a single self-contained retrieval unit, structured so that the chunker produces precise, query-matching sub-chunks at natural section boundaries. See [schemas/core.md](schemas/core.md#atomic-conceptual-content-files) for the full specification.

| Element | What It Does | Best For |
|---------|-------------|----------|
| **Opening paragraph** | Retriever-anchored definition (1–3 sentences) | Carries the core definition up front |
| **Body sections (`##`)** | Organize the atom for the reader | Whole atom retrieves as one unit; headings are for navigation, not for splitting |
| **`## Frequently Asked` (H3 per Q)** | Natural-language question surface | Matches colloquial user queries right inside the parent atom |
| **`## Related Terms`** | Co-located relative vocabulary | Glossary-style matching without aggregator displacement |
| **`## Related Concepts`** | Wikilinks to siblings | Reader navigation and Obsidian graph view |
| **`requires:` frontmatter (v4.1)** | Directional dependencies on other atoms | Retrieval auto-expands to include required atoms (depth 2, count 3 cap) |

This is the current retrieval model as of schema v4.1. See [`schemas/core.md`](schemas/core.md) for the full specification and [`schemas/rfcs/RFC-001-atomic-conceptual-chunks.md`](schemas/rfcs/RFC-001-atomic-conceptual-chunks.md) for the empirical findings that drove the design.

#### Oversized atomic/reference files (RFC-004)

Workflows and reference files that legitimately exceed the token ceiling carry a **`.chunks.yaml` sidecar** (`ep-chunk-annotate.py`) so runtime chunkers split at the same `##`/`###` boundaries the author intended. EP MCP consumes the sidecar for deterministic re-assembly when present.

#### Auditable retrieval and answers

| Layer | Contract | Where |
|-------|----------|-------|
| **Retrieval** | Fragment provenance + Reconstruct Mode (`fragment_id`, `line_range`, span hash) | `schemas/core.md`, [RFC-003](schemas/rfcs/RFC-003-fragment-provenance-reconstruct-mode.md), EP MCP |
| **Response** | Typed Answer Contract — every claim maps to source fragments | `schemas/registry/typed-answer.spec.yaml`, `templates/TAC-PROMPT.md` |

Reconstruct Mode is opt-in at query time (`reconstruct=true`). TAC is opt-in at the agent prompt level but required when auditable answers are a domain requirement.

---

### Provenance-First Micro-Records

For machine pipelines, ExpertPack can export each Markdown atom as a canonical micro-record JSONL row. The Markdown file remains the source of truth; the micro-record is a deterministic projection optimized for graph stores, exact ID lookup, compact retrieval, and agent verification.

Two export shapes are supported:

- **Full JSON-LD record** — preserves the registry-style envelope, nested `provenance`, lifecycle metadata, tags, `requires`, and graph-derived `related` edges.
- **Compact record (`--compact`)** — keeps only the fields needed for token-efficient grounded retrieval: `id`, `canonical_statement`, `type`, `pack`, `source_span_uri`, `content_hash`, `verified_at`, `requires`, `related`, and optional fragment fields (`fragment_id`, `line_range`, `span_hash`) for Reconstruct Mode pipelines.

**Ingest gate:** No pack enters the index without passing `ep-validate --strict`. `tools/ingest-gate.py` chains validate → `ep-strip-frontmatter` → `ep-micro-record-export --strict`.

This gives ExpertPack a clean bridge between human-readable Markdown and hybrid KG/vector systems: Markdown for authorship, compact JSONL for deterministic retrieval infrastructure, fragment provenance for span-level audit.

## How Agents Consume Packs

### Discovery
1. Read `manifest.yaml` — understand what the pack covers, its type, and scope
2. Read `overview.md` — get enough context to route queries
3. This is the **minimal** loading level — enough for pack awareness

### Retrieval
For a specific question, agents use the atomic-conceptual model:
- **Broad queries** → opening paragraph of each concept file carries the retriever-anchored definition
- **Factual queries** → body sections and `## Frequently Asked` blocks match specific questions within the atom
- **Topic queries** → navigate via `_index.md` or RAG search across content files
- **Vocabulary mismatches** → `## Related Terms` co-locates glossary definitions with the parent concept
- **Dependency chains** → `requires:` frontmatter causes retrieval to auto-include prerequisite atoms (depth 2, up to 3 additional files)
- **Auditable answers** → enable Reconstruct Mode for span-level citations; require TAC JSON when claims must map to retrieved fragments

### Update
When adding or changing content:
1. Identify the canonical file
2. Check for contradictions
3. Edit the Markdown file
4. Update `_index.md` if new files were added
5. Commit with a descriptive message

---

## Content Creation

ExpertPacks are intended to be created and maintained by AI agents. The creation pipeline below is written as an agent-operated workflow — the agent is the operator, the human is the pack owner or domain expert who supplies knowledge and approvals.

### Where Pack Content Comes From

| Source | Quality | Coverage |
|--------|---------|----------|
| **Expert interviews / dictation** | Highest — captures tribal knowledge | Decisions, gotchas, real experience |
| **Existing documentation** | Medium — written for human browsing | Concepts, basic workflows |
| **Video tutorials / walkthroughs** | High — shows actual usage | Workflows, screen knowledge |
| **Support tickets / forums** | High — real problems | Troubleshooting, FAQ |
| **Personal experience** | Highest — authentic, specific | Stories, beliefs, examples |

### Agent-operated Creation Pipeline

1. Schema read-in
   - The agent loads type-specific and core schemas and uses them as the filing guide.
2. Skeleton initialization
   - Run `expertpack init <slug> --type …` (or copy `template/`). Review `DESIGN.md` and `TOOLS.md`.
3. Crawl & ingest
   - The agent ingests authorized docs, transcribes media, and structures content with `##` headers. Obsidian vaults: `expertpack migrate obsidian <vault> --output …` produces `_migration-report.md`.
4. Expert interviews
   - The agent conducts structured interviews with the pack owner to capture tribal knowledge, edge cases, and decisions. Capture verbatim and distilled forms.
5. Structure & cross-reference
   - The agent files content into the schema taxonomy, adds cross-links, and updates `_index.md`.
6. Troubleshooting & gotchas
   - The agent synthesizes recurring failures from tickets/forums and expert input into troubleshooting and gotchas files.
7. Gap analysis
   - The agent compares actual content to schema expectations and produces a prioritized gap report for the pack owner.
8. Validation & provenance
   - Run `expertpack doctor --fix hash --apply` then `expertpack validate --strict`. Sidecars for oversized atomic/reference files: `expertpack chunk-annotate --apply`. Flag contradictions for human adjudication.
9. Commit & reporting
   - The agent commits changes with descriptive messages and produces status summaries of new content and remaining gaps.
10. Ongoing maintenance
   - The agent monitors new sources, ingests updates, and repeats the pipeline under human supervision.

Practical prompting guidance for agents

- Ask one focused question per prompt during interviews and request concrete examples or steps.
- Present clarifying choices when uncertain and ask the pack owner to pick or correct.
- Frame gap reports as short checklists with suggested interview prompts.

Notes

- The agent is responsible for structuring and filing content; humans are responsible for providing knowledge and resolving conflicts.
- Record provenance for every file; prefer human confirmation before making authoritative edits.

---

## Evaluation

Every ExpertPack can include an evaluation suite to measure and track quality over time. The eval framework is pack-type agnostic — the same metrics and methodology work for person, product, and process packs.

See [schemas/eval.md](schemas/eval.md) for the full specification, including:
- Standard eval set format (questions + expected answers + anti-hallucination checks)
- Response quality metrics (correctness, groundedness, hallucination rate)
- Retrieval quality metrics (hit rate, precision)
- **TAC scoring** — structural validity and claim coverage via `claim_verifier.py --tac`
- Efficiency metrics (tokens, latency, cost)
- Pack health metrics (structural conformance via `ep-validate --strict`)
- Eval workflow for pack builders and framework developers

The eval system answers the question: "Is this pack getting better or worse?"

---

## Revision History

| Date | Changed By | Notes |
|------|-----------|-------|
| 2026-02-13 | — | Initial ARCHITECTURE.md |
| 2026-03-09 | — | Added eval framework, retrieval optimization layers, schema versioning, provenance |
| 2026-04-06 | — | Obsidian compatibility; graph view optimization |
| 2026-04-14 | — | Schema v4.0: atomic-conceptual content model (RFC-001); aggregator directories retired |
| 2026-04-19 | — | Schema v4.1: strict one-concept-per-file, `requires:` dependencies, 1,000-token ceiling |
| 2026-04-23 | — | ARCHITECTURE.md rewritten to reflect v4.1 as current model |
| 2026-07-06 | — | Enforcement gate, RFC-003/004, TAC, expertpack CLI, updated tools tree and onboarding flow |

---

*This is a living document. Update it as the framework evolves.*
