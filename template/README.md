# ExpertPack Vault Template

A ready-to-go [Obsidian](https://obsidian.md) vault for building an [ExpertPack](https://expertpack.ai) — a structured knowledge pack that gives AI agents deep expertise in a specific domain.

**[🌐 expertpack.ai](https://expertpack.ai)** · **[📦 ExpertPack on GitHub](https://github.com/brianhearn/expert-pack)** · **[💎 What is an ExpertPack?](#what-is-an-expertpack)**

---

## What is an ExpertPack?

An ExpertPack is a structured, Markdown-first knowledge pack that gives an AI agent expertise it can't get from its training weights alone.

The core idea: not all knowledge in a pack is equally valuable. Knowledge the model already has is dead weight — it burns tokens without adding capability. What matters is **esoteric knowledge (EK)** — the tribal knowledge, undocumented behavior, domain-specific gotchas, and practitioner wisdom that frontier LLMs can't produce on their own.

ExpertPacks are measured by their **EK ratio**: the percentage of content that frontier models (GPT, Claude, Gemini) cannot correctly answer without the pack loaded. A pack with an 0.80 EK ratio means 80% of its content adds genuine capability the model didn't have.

---

## What's in This Template

```
your-pack/
├── .obsidian/              ← Pre-configured Obsidian settings
│   ├── app.json            ← Relative links, sensible defaults
│   ├── community-plugins.json
│   ├── plugins/
│   │   ├── dataview/       ← Live query engine
│   │   └── templater-obsidian/ ← Smart note creation
│   └── templates/          ← EP-schema frontmatter templates
│       ├── new-concept.md
│       ├── new-workflow.md
│       ├── new-faq.md
│       ├── new-troubleshooting.md
│       └── new-volatile.md
├── manifest.yaml           ← Pack identity (fill this in first)
├── overview.md             ← Entry point for AI agents
├── DESIGN.md               ← Author notes: scope, audience, non-goals, key decisions
├── TOOLS.md                ← Integrator notes: retrieval, MCP tools, agent workflows
├── glossary.md             ← (Optional) lean cross-cutting terms only
├── Dashboard.md            ← Live Dataview dashboard
├── concepts/               ← Atomic-conceptual concept files (v4.1): one self-contained file per concept
├── workflows/              ← Step-by-step procedures (atomic retrieval)
├── troubleshooting/        ← Errors, diagnostics, common mistakes
├── faq/                    ← Cross-cutting questions only (per-concept FAQs live inside concept files)
├── meta/source-coverage.md  ← Research coverage audit trail
├── volatile/               ← Time-bound content with TTL (`_index.md` explains format)
└── eval/                   ← Quality eval benchmark
```

---

## Quick Start

### 1. Clone or download

```bash
# Option A — clone the ExpertPack repo and copy the template folder
git clone https://github.com/brianhearn/expert-pack.git
cp -r ExpertPack/template my-pack-name

# Option B — download the template folder directly from GitHub
```

### 2. Open in Obsidian

- Open Obsidian → **Open folder as vault** → select your `my-pack-name` folder
- Go to **Settings → Community plugins** → enable Community plugins
- Click **Browse** and install **Dataview** and **Templater**
- Enable both plugins

### 3. Fill in `manifest.yaml`

Open `manifest.yaml` and fill in:
- `name`, `slug`, `type` (product/person/process), `description`
- `author`, `created`, `updated`

### 4. Start hydrating

Create new content files using Templater templates:
- **Cmd/Ctrl+P** → "Templater: Create new note from template"
- Pick the template matching your content type (concept, workflow, FAQ, etc.)
- Frontmatter fills in automatically

### 5. Check your Dashboard

Open `Dashboard.md` for a live view of:
- Content by type
- Files missing frontmatter
- Volatile content expiring soon
- EK scores (after you run evals)

---

## Content Types

| Type | Directory | retrieval_strategy | When to use |
|---|---|---|---|
| `concept` | `concepts/` | standard | Core knowledge, mental models, "what is X" |
| `workflow` | `workflows/` | **atomic** | Step-by-step procedures, "how do I X" |
| `troubleshooting` | `troubleshooting/` | **atomic** | Errors, diagnostics, fixes |
| `gotcha` | `troubleshooting/common-mistakes/` | **atomic** | Non-obvious pitfalls, anti-patterns |
| `faq` | `faq/` | standard | Frequently asked questions (one per file) |
| `volatile` | `volatile/` | standard | Time-bound content with refresh TTL |

**Atomic** files are retrieved whole — never split by RAG chunkers. Use for anything where partial retrieval would produce dangerous or misleading output (procedures, error fixes).

---

## File Size Target

**400–800 tokens per file** (~1,600–3,200 characters). This is the ExpertPack chunking strategy: author files at target size so any RAG chunker passes them through intact. The schema IS the chunking strategy.

Hard ceiling: 1,000 tokens (~4,000 chars) for concept files in schema v4.1. Atomic files (workflows, troubleshooting) may exceed this.

---

## EK Ratio: Measure What Your AI Is Missing

Once your pack has content, measure its EK ratio:

```bash
clawhub install expertpack-eval
```

The eval skill blind-probes frontier models (no pack loaded) and measures what percentage of your pack's propositions they can't answer — pulled from concept-file `## Key Propositions` sections and body prose. This tells you:
- How much of your content is genuinely valuable to an AI agent
- Which sections have the highest knowledge density
- Where to focus future hydration effort

**EK ratio targets:**

| Score | Meaning |
|---|---|
| 0.80+ | Exceptional — almost entirely esoteric |
| 0.60–0.79 | Strong — majority esoteric |
| 0.40–0.59 | Mixed — significant general knowledge padding |
| < 0.40 | Weak — most content already in model weights |

---

## Using Your Pack with AI Agents

### OpenClaw (RAG)
Add to `openclaw.json`:
```json
{
  "agents": { "defaults": { "memorySearch": {
    "extraPaths": ["/path/to/your-pack"]
  }}}
}
```

### Claude Code / Cursor / Gemini
Point the agent at your pack directory. The `overview.md` is the entry point — load it first.

### Any RAG system
Files are pre-sized at 400–800 tokens. Point any vector store at the pack directory with `chunk_size=1000` (passes all files through intact).

---

## Learn More

- **[ExpertPack Schema docs](https://expertpack.ai/#schemas)** — Full specification
- **[Community packs](https://github.com/brianhearn/expert-pack/tree/main/packs)** — See real examples (Blender 3D, Home Assistant, Solar DIY)
- **[ExpertPack on GitHub](https://github.com/brianhearn/expert-pack)** — Star if useful ⭐
- **[expertpack-eval skill](https://clawhub.ai/skills/expertpack-eval)** — EK ratio measurement
- **[expertpack-export skill](https://clawhub.ai/skills/expertpack-export)** — Export an AI agent as an ExpertPack
