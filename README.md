# ExpertPack

**Give your AI the knowledge it's missing.**

Esoteric knowledge (EK) is knowledge not found in the weights of frontier LLMs — the tribal knowledge in your support team's heads, the gotchas your engineers learned the hard way, the decision patterns that were never documented. ExpertPacks deliver this knowledge to any AI agent in a way that **minimizes token cost and maximizes prompt quality through RAG**.

Every pack is measured by its **EK ratio** — the proportion of content that frontier models cannot correctly produce on their own. During hydration, every fact is triaged: esoteric knowledge gets maximum treatment, general knowledge gets compressed to scaffolding. The result is dense, high-value context that makes your AI genuinely expert — not just articulate.

**[🌐 expertpack.ai](https://expertpack.ai)** · **[📦 Free Packs](#free-community-packs)** · **[📖 Schemas](#schemas)** · **[🧪 Evaluation](#evaluation)**

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

---

## EK-Optimized Retrieval

ExpertPacks go beyond basic RAG with a multi-layer retrieval system and EK-aware hydration.

### Retrieval Layers

| Layer | What It Does | Why It Matters |
|-------|-------------|----------------|
| **Summaries** (`summaries/`) | Section-level RAPTOR-style summaries | Broad questions match summaries first; agents drill into detail files |
| **Propositions** (`propositions/`) | Atomic factual statements per section | Specific factual queries match exact propositions, not paragraphs |
| **Lead Summaries** | Blockquote at top of content files | First RAG chunk contains the core answer, not preamble |
| **Glossary** (`glossary.md`) | Maps user vocabulary to technical terms | Bridges the gap between how users ask and how docs are written |

### EK Triage During Hydration

Every extracted fact passes through the EK triage pipeline:

- **EK** (model wrong/refuses) → Full treatment: dedicated file, lead summary, proposition extraction
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

### Schema-Aware Chunker

Generic RAG chunkers split files by character count — they don't understand markdown structure. The [schema-aware chunker](tools/schema-chunker/) pre-processes ExpertPack files into semantically coherent chunks that respect `##` headers, lead summaries, proposition groups, glossary tables, and content-type-aware strategies — workflows and troubleshooting files are kept atomic (never split), while reference content is sectioned on headers. Per-file overrides via `retrieval.strategy` frontmatter.

**Results on a real product pack (EZT Designer):**
- **+9.4% correctness** (79% → 88.4%) — best improvement from any single change
- **-52% input tokens** (4,372 → 2,111 avg per query)
- **-60% hallucination** (10% → 4%)

Designed for [OpenClaw](https://openclaw.ai) — outputs pre-sized `.md` files that OpenClaw's indexer passes through as single chunks. See the [chunker README](tools/schema-chunker/README.md) for integration details.

---

## Schemas

| Schema | Version | What It Covers |
|--------|---------|---------------|
| [core.md](schemas/core.md) | 2.4 | Shared principles: MD-canonical, file structure, retrieval optimization, chunking strategies, EK ratio, context tiers, provenance |
| [person.md](schemas/person.md) | 1.6 | Person packs: verbatim, mind taxonomy, relationships, presentation, agent subtype |
| [product.md](schemas/product.md) | 1.8 | Product packs: concepts, workflows, interfaces, troubleshooting, commercial, customers |
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
├── README.md                ← This file
├── LICENSE                  ← Apache 2.0
│
├── schemas/                 ← Pack blueprints (the framework)
│   ├── core.md              ← Shared principles (v2.4)
│   ├── person.md            ← Person-pack schema (v1.6)
│   ├── product.md           ← Product-pack schema (v1.8)
│   ├── process.md           ← Process-pack schema (v1.4)
│   ├── composite.md         ← Composite schema (v1.1)
│   └── eval.md              ← Evaluation framework (v1.2)
│
├── guides/                  ← Practical guides
│   ├── hydration.md         ← Complete hydration lifecycle: planning → population → retrieval optimization → validation (v1.0)
│   └── consumption.md       ← How to deploy and consume packs with AI agents (v1.0)
│
├── tools/                   ← Tooling
│   ├── eval-ek.py           ← EK ratio measurement via blind probing
│   └── schema-chunker/      ← Schema-aware chunking for OpenClaw RAG (+9.4% correctness)
│
├── skills/                  ← Agent skills
│   └── expertpack-export/   ← Auto-discover & export agent → EP
│
├── packs/                   ← Pack instances
│   ├── home-assistant/      ← Home automation (composite, EK 54%)
│   ├── blender-3d/          ← 3D software (product, EK 42%)
│   ├── solar-diy/           ← Solar & battery DIY (composite, EK 52%)
│   └── ezt-designer/        ← Territory management (product, private)
│
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
