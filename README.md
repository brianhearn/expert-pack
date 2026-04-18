# ExpertPack

**Give your AI the knowledge it's missing.**

Esoteric knowledge (EK) is knowledge not found in the weights of frontier LLMs — the tribal knowledge in your support team's heads, the gotchas your engineers learned the hard way, the decision patterns that were never documented. ExpertPacks deliver this knowledge to any AI agent in a way that **minimizes token cost and maximizes prompt quality through RAG**.

Every pack is measured by its **EK ratio** — the proportion of content that frontier models cannot correctly produce on their own. During hydration, every fact is triaged: esoteric knowledge gets maximum treatment, general knowledge gets compressed to scaffolding. The result is dense, high-value context that makes your AI genuinely expert — not just articulate.

**[🌐 expertpack.ai](https://expertpack.ai)** · **[📦 Free Packs](#free-community-packs)** · **[📖 Schemas](#schemas)** · **[🧪 Evaluation](#evaluation)** · **[💎 Obsidian Compatible](#obsidian-compatibility)** · **[🗂️ Vault Template](template/)**

---

## Obsidian Compatibility

ExpertPacks are valid [Obsidian](https://obsidian.md) vaults — open any pack directory directly in Obsidian and get:

- **Dataview queries** — live tables filtering by content type, EK score, retrieval strategy, tags
- **Graph view** — visual map of how pack files relate to each other
- **Tag pane** — browse all content by type and domain tag
- **Full-text search** — across all pack content and frontmatter fields
- **Templater** — create new EP-schema-compliant files from templates

Every content file includes YAML frontmatter (`title`, `type`, `tags`, `pack`, `retrieval_strategy`). The repo includes a `.obsidian/` reference config with Dataview pre-configured and example queries.

**To use a pack in Obsidian:**
1. Copy the `.obsidian/` folder from the repo root into your pack directory
2. Open that directory as a vault in Obsidian
3. Install Dataview + Templater from Community Plugins

**Starting a new pack from scratch?** Use the **[Obsidian Vault Template](template/)** — pre-configured folder structure, Templater templates for every content type, and a live Dataview dashboard.

Link format is standard relative Markdown — packs render correctly on GitHub, in any Markdown reader, and in Obsidian simultaneously.

---

## Why Not Just Search?

**Models don't know what they don't know.** When a model confidently hallucinates, it doesn't trigger a search — it thinks it already knows. An ExpertPack loaded into context preempts the hallucination with the correct answer.

**Search requires the right question.** If the model doesn't know about a specific firmware bug, it won't search for the precise query that finds the fix. You can't search for knowledge you don't know exists.

**Not all knowledge is on the internet.** Source code analysis reveals undocumented behavior. Expert interviews capture tribal knowledge never written down. Person packs contain private stories and reasoning.

---

## Pack Types

### 🧑 Person Packs
Capture a person — stories, beliefs, relationships, voice, and legacy.

**Use cases:** Personal AI assistant, family archive, memorial AI, digital legacy, founder knowledge capture

### 📦 Product Packs
Deep knowledge about a product or platform — concepts, workflows, troubleshooting, and the edge cases documentation never covers.

**Use cases:** AI support agent, sales assistant, training tool, onboarding guide

### 🔄 Process Packs
Complex multi-phase processes — phases, decisions, checklists, gotchas, and the gap between the official process and what actually happens.

**Use cases:** Home building guide, business formation, project management, certification processes

### 🔗 Composites
Combine person, product, and process packs into a single agent deployment with role assignments, context control, and cross-pack conflict resolution.

**Use cases:** CEO AI assistant, multi-product support bot, company knowledge base

---

## Free Community Packs

Open-source ExpertPacks built from real documentation, community forums, and source code analysis. Each pack shows its EK ratio — the percentage of content that frontier AI models cannot produce on their own.

| Pack | Type | Files | Size | EK Ratio | Description |
|------|------|-------|------|----------|-------------|
| [**Home Assistant**](packs/home-assistant/) | Composite | 61 | 684 KB | 54% | Smart home automation — protocols, automations, presence detection, ESPHome, voice, energy, community gotchas |
| [**Blender 3D**](packs/blender-3d/) | Product | 36 | 480 KB | 42% | 3D modeling, animation, sculpting, physics, rendering, Geometry Nodes, Python scripting, production workflows |
| [**Solar & Battery DIY**](packs/solar-diy/) | Composite | 46 | 428 KB | 52% | Residential solar — system design, panels, batteries, NEC code, permitting, installation, troubleshooting |

> 💡 These packs demonstrate the framework with substantive, practitioner-level content. Browse them to see what a well-built ExpertPack looks like.

---

## How It Works

1. **Point your AI at the schema** — pick person, product, or process. The agent reads the schema and knows exactly what to build.
2. **Feed it knowledge** — talk to the agent, point it at websites, drop in documents. It structures everything automatically, triaging each fact for EK during hydration.
3. **Deploy the pack** — drop the folder into any AI agent's workspace. Instant domain expertise — no prompt engineering required.
4. **Measure & improve** — run evals to measure EK ratio, correctness, and hallucination rate. Use results to guide targeted improvements.

### Platform Compatibility

| Platform | Integration |
|----------|-------------|
| **OpenClaw** | Add pack path to `memorySearch.extraPaths`. RAG indexes all `.md` files automatically. |
| **Cursor** | Place pack in project. Cursor indexes workspace files for context. |
| **Claude Code** | Place pack in project. Reference from `CLAUDE.md` or let agent discover it. |
| **Custom / API** | Feed `.md` files into your vector store or context window. Small-file structure (1–3KB each) is optimized for chunked retrieval. |
| **MCP Server** | [ExpertPack MCP](https://github.com/brianhearn/ep-mcp) serves any pack over the Model Context Protocol — connect Claude Desktop, Cursor, Windsurf, or any MCP host instantly. |

---

## EK-Optimized Retrieval

ExpertPacks go beyond basic RAG with a multi-layer retrieval system and EK-aware hydration.

### Atomic-Conceptual Content (Schema v4.0+)

Each concept is a **single self-contained file** carrying everything the retriever needs:

| Element | What It Does | Why It Matters |
|---------|-------------|----------------|
| **Opening paragraph** | 1–3 sentences that define the concept in retriever-friendly terms | First chunk carries the core definition; no throat-clearing |
| **Body sections** | `##`-delimited sub-topics | Chunker splits at headings, aligning retrieval to semantic boundaries |
| **`## Frequently Asked`** | H3-per-question FAQ block | Natural-language query surface; each Q/A becomes its own sub-chunk |
| **`## Related Terms`** | Terms that don't stand alone | Co-locates glossary-style definitions with the parent concept |
| **`## Key Propositions`** | Axiomatic statements (optional) | Precise fact retrieval without aggregator-directory displacement |
| **`## Related Concepts`** | Wikilinks to siblings | EP MCP graph expansion pulls in neighbors when relevant |

This replaces the v3.x pattern of separate `summaries/`, `propositions/`, per-domain `glossary-*.md`, and standalone `faq/` directories — those aggregator files scored broadly on every query and displaced specific content at retrieval time. See [`schemas/rfcs/RFC-001-atomic-conceptual-chunks.md`](schemas/rfcs/RFC-001-atomic-conceptual-chunks.md) for the empirical findings that drove the change and [`schemas/references/granularity-guide.md`](schemas/references/granularity-guide.md) for authoring decisions.

### EK Triage During Hydration

Every extracted fact passes through the EK triage pipeline:

- **EK** (model wrong/refuses) → Full treatment: dedicated concept file with a retriever-anchored opening, detailed body, and `## Key Propositions` if the concept has axiomatic statements
- **Partial** (model vague) → Standard treatment, highlight the specific detail the model missed
- **GK scaffolding** (model correct, but needed for retrieval) → 1-3 sentences max, no dedicated file
- **GK unnecessary** (model correct, no EK depends on it) → Skip entirely

See the [Hydration Guide](guides/hydration.md) for the full hydration pipeline.

---

## Evaluation

Every pack can include an eval suite to measure quality. The [eval schema](schemas/eval.md) defines:

- **EK Ratio** — proportion of propositions that frontier models can't answer without the pack
- **Correctness** — percentage of required facts present in responses
- **Hallucination Rate** — percentage of responses containing fabricated information
- **Refusal Accuracy** — percentage of out-of-scope questions correctly declined
- **Retrieval Hit Rate** — percentage of queries retrieving the expected source files

The included [eval-ek.py](tools/eval-ek.py) tool measures EK ratio via blind probing across multiple frontier models.

### Retrieval-Ready Authoring (Schema 2.5+)

The schema itself is now the chunking strategy. Author content files as self-contained retrieval units **(400–800 tokens, 1,500 token hard ceiling)**. Any RAG chunker will pass these files through intact without splitting, preserving structure, lead summaries, propositions, and metadata.

### Provenance Metadata (Schema 3.0+)

Every content file can carry provenance frontmatter — `id`, `content_hash`, `verified_at`, `verified_by` — enabling auditable citations, change detection, and freshness tracking. The pack manifest includes a `freshness` block for sweep coverage metrics. See the [Citation Response Contract](schemas/core.md) for how retrieval systems should surface provenance.

### Graph Export (Schema 3.1+)

Packs can generate a `_graph.yaml` adjacency file from wikilinks, `related:` frontmatter, and context hint comments. This enables GraphRAG traversal, structural analysis, and cross-pack linking. Generate with [`ep-graph-export.py`](tools/graph-export/ep-graph-export.py).

### ExpertPack MCP Server

[ExpertPack MCP](https://github.com/brianhearn/ep-mcp) exposes any ExpertPack as expertise-as-a-service over the Model Context Protocol. Schema-aware hybrid retrieval (BM25 + vector), graph-aware traversal, frontmatter-aware indexing, provenance metadata extraction, and multi-pack routing — any MCP-compatible agent gets instant access to pack knowledge. A live instance serving the `ezt-designer` pack runs at [expertpack.ai/mcp](https://expertpack.ai/mcp).

---

## Schemas

| Schema | Version | What It Covers |
|--------|---------|---------------|
| [core.md](schemas/core.md) | 3.1 | Shared principles: MD-canonical, file structure, retrieval optimization, chunking strategies, EK ratio, context tiers, provenance metadata, graph export |
| [person.md](schemas/person.md) | 1.6 | Person packs: verbatim, mind taxonomy, relationships, presentation |
| [agent.md](schemas/agent.md) | 1.0 | Agent extension: persona, capabilities, tool access, behavioral rules |
| [product.md](schemas/product.md) | 3.1 | Product packs: concepts, workflows, interfaces, troubleshooting, commercial, customers |
| [process.md](schemas/process.md) | 1.4 | Process packs: phases, decisions, checklists, exceptions, scheduling, regulations |
| [composite.md](schemas/composite.md) | 1.1 | Composites: multi-pack deployment, role assignments, auto-discovery & export |
| [eval.md](schemas/eval.md) | 1.2 | Evaluation: EK ratio, correctness, hallucination, retrieval quality, structural health |

---

## Axioms

ExpertPack development is guided by [10 axioms](AXIOMS.md):

1. **Esoteric knowledge (EK)** is knowledge outside the weights of frontier LLMs
2. EPs have a **subject matter** — person, product, or process
3. EPs **maximize the ratio of EK** to general knowledge
4. **Hydration** is the process of populating the pack with EK
5. **Compaction** minimizes loss of EK
6. **Quality** = compactness × EK volume × retrieval quality × minimal decay
7. **Market value** = quality × market potential × agentic correlation
8. **Cost** increases with human exchange needed + compute tokens
9. **EK ratio** is empirically measurable via blind probing
10. **Hydration should prioritize EK** — minimize general knowledge, maximize what only the pack can provide

---

## Repository Structure

```
ExpertPack/
├── AXIOMS.md                ← 10 guiding axioms for EP development
├── CHANGELOG.md             ← Framework changelog
├── ROADMAP.md               ← Development roadmap
├── README.md                ← This file
├── LICENSE                  ← Apache 2.0
│
├── schemas/                 ← Pack blueprints (the framework)
│   ├── core.md              ← Shared principles (v3.1)
│   ├── person.md            ← Person-pack schema (v1.6)
│   ├── agent.md             ← Agent extension schema (v1.0)
│   ├── product.md           ← Product-pack schema (v3.1)
│   ├── process.md           ← Process-pack schema (v1.4)
│   ├── composite.md         ← Composite schema (v1.1)
│   ├── eval.md              ← Evaluation framework (v1.2)
│   └── references/          ← Extracted reference material
│
├── guides/                  ← Practical guides
│   ├── hydration.md         ← Hydration lifecycle: planning → population → retrieval optimization → validation
│   └── consumption.md       ← Deploying and consuming packs with AI agents (incl. deploy-prep and eval discipline)
│
├── tools/                   ← Tooling
│   ├── validator/           ← ep-validate.py — structural + provenance validation (19 checks)
│   ├── graph-export/        ← ep-graph-export.py — generate _graph.yaml adjacency files
│   ├── deploy-prep/         ← ep-strip-frontmatter.py — strip provenance metadata before RAG deploy
│   └── eval-ek.py           ← EK ratio measurement via blind probing
│
├── skills/                  ← OpenClaw agent skills (also on ClawHub)
│   └── expertpack-export/   ← Auto-discover & export agent → EP
│
├── packs/                   ← Community pack instances
│   ├── home-assistant/      ← Home automation (composite, EK 54%)
│   ├── blender-3d/          ← 3D software (product, EK 42%)
│   └── solar-diy/           ← Solar & battery DIY (composite, EK 52%)
│
├── template/                ← Obsidian vault template for new packs
└── site/                    ← expertpack.ai website source
```

---

## 🦞 OpenClaw Tested

ExpertPack was designed and battle-tested with [OpenClaw](https://openclaw.ai) — the open-source AI agent platform. Every schema change is validated against real agent deployments.

---

## License

Apache 2.0 — see [LICENSE](LICENSE) for details.

The ExpertPack framework (schemas, guides, tooling) is open source. Individual pack instances contain original content and can be licensed independently by their creators.

---

**[Website](https://expertpack.ai)** · **[GitHub](https://github.com/brianhearn/ExpertPack)** · Built by [Brian Hearn](https://github.com/brianhearn)
