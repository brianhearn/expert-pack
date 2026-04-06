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
| **Small Files** | 1–3KB per content file, one topic per file |
| **RAG-Optimized** | `##` section headers at natural topic breaks for quality chunking |
| **Retrieval-Optimized** | Multi-layer retrieval: summaries, propositions, lead summaries, glossary |
| **Layered Loading** | Three-tier context: always → searchable → on-demand |
| **Source-Tracked** | Provenance frontmatter traces content back to its origin |
| **Cross-Referenced** | Relative markdown links between related files |
| **Obsidian-Native** | Per-file YAML frontmatter on all content files; valid Obsidian vault out of the box |
| **Schema-Versioned** | Type schemas carry semantic versions; packs declare their target |
| **Eval-Driven** | Measurable quality with standardized eval sets and automated scoring |
| **Git-Native** | Version controlled, diffable, collaborative |
| **Never Overwrite** | Contradictions are flagged for human resolution |

---

## How Schemas Work

The schema system has two layers:

### Core Schema ([schemas/core.md](schemas/core.md)) — v2.9
Shared principles and conventions that apply to every ExpertPack:
- The MD-canonical principle
- Required files (`manifest.yaml`, `overview.md`)
- Directory conventions (`_index.md`, `_access.json`)
- File structure rules (size, naming, headers)
- Cross-referencing patterns
- Layered loading strategy (three-tier context: always → searchable → on-demand)
- Retrieval optimization layers (summaries, propositions, lead summaries, glossary)
- Volatile data isolation (`volatile/` directory + frontmatter TTL for time-bound EK)
- Source provenance tracking
- Schema versioning system
- Conflict resolution
- Agent consumption patterns

### Type-Specific Schemas
Each pack type has its own schema that extends core with domain-specific structure:

- **[schemas/person.md](schemas/person.md)** (v1.6) — Mind taxonomy (9 universal categories), verbatim content with story card frontmatter, two-tier content system (verbatim → summary mirroring), biographical facts, timeline, relationships, legacy/memorial mode, privacy modes, presentation (voice, appearance), reasoning and conflict handling
- **[schemas/product.md](schemas/product.md)** (v1.8) — Concepts, workflows, troubleshooting (errors, diagnostics, common mistakes), screens/interface specs, FAQ, commercial info, entity cross-references, timeline, decisions, customers, limitations, competitive landscape, mental model, lead summaries, glossary
- **[schemas/process.md](schemas/process.md)** (v1.4) — Phases with enhanced structure, decisions, checklists, roles, resources, examples, gotchas, exceptions, variants
- **[schemas/composite.md](schemas/composite.md)** (v1.1) — Multi-pack deployments with role assignments, context tier overrides, cross-pack conflict resolution
- **[schemas/eval.md](schemas/eval.md)** (v1.2) — Evaluation framework for measuring pack quality (response quality, retrieval quality, efficiency, pack health)

A pack declares its type in `manifest.yaml`, which determines which type-specific schema applies.

---

## Packs Are Instances

A pack is an instantiation of a schema — a concrete knowledge base about a specific person, product, or process.

```
ExpertPack/
├── schemas/               ← The blueprints
│   ├── core.md            ← Shared principles (v2.9)
│   ├── person.md          ← Person-pack schema (v1.6)
│   ├── product.md         ← Product-pack schema (v1.8)
│   ├── process.md         ← Process-pack schema (v1.4)
│   ├── composite.md       ← Composite schema (v1.1)
│   └── eval.md            ← Eval framework (v1.2)
│
├── guides/                ← Practical how-to guides for pack builders
│   ├── hydration.md           ← Complete hydration lifecycle
│   └── consumption.md         ← How to deploy and consume packs with AI agents
│
├── tools/                 ← Tooling for pack development
│   ├── eval-ek.py         ← EK ratio measurement via blind probing
│   └── eval-runner/       ← Automated eval execution and scoring
│
├── skills/                ← Agent skills for pack creation and export
│
└── packs/                 ← The instances
    ├── home-assistant/    ← Composite pack: Home Assistant (EK 54%)
    ├── blender-3d/        ← Product pack: Blender 3D (EK 42%)
    └── solar-diy/         ← Composite pack: Solar & Battery DIY (EK 52%)
```

Creating a new pack means:
1. Choose the type (person, product, or process)
2. Create a directory under `packs/`
3. Add `manifest.yaml` and `overview.md` (required)
4. Populate directories per the type-specific schema
5. Follow core principles for all content

---

## Retrieval Optimization

Basic RAG — embed documents, retrieve top-k chunks — works, but it leaves precision and token efficiency on the table. ExpertPacks use a multi-layer retrieval system where each layer handles a different query granularity. See [schemas/core.md](schemas/core.md) for the full specification.

| Layer | What It Does | Best For |
|-------|-------------|----------|
| **Summaries** (`summaries/`) | Section-level summaries following the RAPTOR pattern | Broad questions ("what can this product do?") |
| **Propositions** (`propositions/`) | Atomic factual statements extracted from content | Specific factual questions ("what's the upload limit?") |
| **Lead Summaries** | 1–3 sentence blockquote at the top of content files | Ensuring first-chunk relevance for high-traffic topics |
| **Glossary** (`glossary.md`) | Maps user language to technical terms | Bridging vocabulary gaps in retrieval |
| **Content Files** | Focused 1–3KB files with `##` headers | Detailed topic coverage |

**The three-layer rule:** When splitting oversized files, always generate summaries and propositions alongside the split files. Naive splitting loses cross-topic context and makes retrieval worse, not better. The three layers together (split files + summaries + propositions) consistently outperform any single optimization.

---

## How Agents Consume Packs

### Discovery
1. Read `manifest.yaml` — understand what the pack covers, its type, and scope
2. Read `overview.md` — get enough context to route queries
3. This is the **minimal** loading level — enough for pack awareness

### Retrieval
For a specific question, agents use hierarchical retrieval across the optimization layers:
- **Broad queries** → match section summaries first, drill into content files for detail
- **Factual queries** → match atomic propositions for precise answers
- **Topic queries** → navigate via `_index.md` or RAG search across content files
- **Vocabulary mismatches** → glossary bridges user language to pack terminology

### Update
When adding or changing content:
1. Identify the canonical file
2. Check for contradictions
3. Edit the Markdown file
4. Update any affected JSON indexes, summaries, and propositions
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
   - The agent creates the pack skeleton (manifest.yaml, overview.md, starter directories) and commits it.
3. Crawl & ingest
   - The agent ingests authorized docs, transcribes media, and chunks text with `##` headers for RAG.
4. Expert interviews
   - The agent conducts structured interviews with the pack owner to capture tribal knowledge, edge cases, and decisions. Capture verbatim and distilled forms.
5. Structure & cross-reference
   - The agent files content into the schema taxonomy, adds cross-links, and updates `_index.md` and JSON indexes.
6. Troubleshooting & gotchas
   - The agent synthesizes recurring failures from tickets/forums and expert input into troubleshooting and gotchas files.
7. Gap analysis
   - The agent compares actual content to schema expectations and produces a prioritized gap report for the pack owner.
8. Validation & provenance
   - The agent requests confirmation for ambiguous facts, records provenance, and flags contradictions for human adjudication.
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
- Efficiency metrics (tokens, latency, cost)
- Pack health metrics (structural conformance)
- Eval workflow for pack builders and framework developers

The eval system answers the question: "Is this pack getting better or worse?"

---

## Revision History

| Date | Changed By | Notes |
|------|-----------|-------|
| 2026-02-13 | — | Initial ARCHITECTURE.md |
| 2026-02-16 | — | Unified framework — three pack types, shared schemas |
| 2026-02-18 | — | Person schema: mind taxonomy (9 categories); broadened examples |
| 2026-03-05 | — | Added eval framework (schemas/eval.md); added ROADMAP.md for improvement project |
| 2026-03-09 | — | Updated to reflect schema state: retrieval optimization layers, schema versioning, provenance, eval, updated type-specific schema descriptions |
| 2026-03-13 | — | Schema 2.5: files authored as self-contained 400–800 token retrieval units; schema itself became the chunking strategy |
| 2026-03-27 | — | Schema 2.5 split eval; schema versions advanced (core 2.5→2.6, eval 1.0→1.2, composite 1.0→1.1) |
| 2026-04-01 | — | Schema 2.7: volatile data isolation — `volatile/` directory convention + frontmatter TTL for time-bound EK |
| 2026-04-06 | — | Schema 2.8: Obsidian compatibility — per-file YAML frontmatter, `.obsidian/` reference folder, 25-type taxonomy |
| 2026-04-06 | — | Schema 2.9: Graph view optimization — `graph.json` excludes `_index.md` hubs, `related:` frontmatter for content cross-links, `_index.md` clarified as orientation-only |

---

*This is a living document. Update it as the framework evolves.*
