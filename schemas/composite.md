# Composite Pack Schema

*Blueprint for combining multiple ExpertPacks into a single deployment — a CEO agent backed by a person pack and a product pack, a company knowledge base spanning multiple products, or any scenario where an AI agent needs expertise from more than one domain. This schema extends [core.md](core.md); all shared principles apply.*

---

## Purpose

Individual ExpertPacks capture deep knowledge about one thing — a person, a product, or a process. But real-world AI deployments rarely need just one domain. A founder's AI assistant needs to sound like the founder (person pack) while knowing the company's products (product pack) and sales methodology (process pack). A support agent might need knowledge across three product lines.

A composite pack is the orchestration layer. It doesn't contain knowledge itself — it declares which packs to combine, how they relate, and how the agent should prioritize when loading context or resolving conflicts.

---

## When to Use a Composite

**Use a composite when:**
- An agent needs knowledge from two or more packs simultaneously
- You want one pack to define the agent's *voice* while others define its *knowledge*
- Multiple product packs need to coexist with shared context strategy
- You need cross-pack conflict resolution rules

**Don't use a composite when:**
- A single pack covers the entire domain — just use that pack directly
- Packs are used independently by different agents — no composition needed

---

## Directory Structure

```
composites/{composite-slug}/
├── manifest.yaml          ← Composite identity (required)
├── overview.md            ← What this composite does, who it's for (required)
├── overrides/             ← Optional context tier overrides and cross-pack rules
│   └── context.yaml       ← Tier overrides per pack (optional)
└── supplements/           ← Optional composite-only content
    └── {file}.md          ← Bridging content not in any constituent pack
```

A composite is intentionally thin. The knowledge lives in the constituent packs — the composite just wires them together.

---

## Composite Manifest

```yaml
# Required
name: "Human-readable composite name"
slug: "composite-slug"
type: "composite"
version: "1.0.0"
description: "What this composite creates and who it's for"
entry_point: "overview.md"
schema_version: "1.0"

# Required: constituent packs
packs:
  - path: "../packs/jane-doe"           # Relative path to pack
    role: voice                          # This pack defines personality/tone
  - path: "../packs/acme-widget"
    role: knowledge                      # This pack provides domain knowledge
  - path: "../packs/acme-sales-process"
    role: knowledge

# Optional: context strategy overrides
context:
  overrides:
    # Promote a file from Tier 2 → Tier 1 for this deployment
    "acme-widget":
      always:
        - commercial/pricing.md
    # Demote verbose content to Tier 3 for this deployment
    "jane-doe":
      on_demand:
        - mind/tensions.md

# Optional: conflict resolution
conflicts:
  priority: [jane-doe, acme-widget, acme-sales-process]  # First pack wins ties
  strategy: "flag"    # "flag" (ask human) | "priority" (auto-resolve by order)

# Recommended
author: "Who created this composite"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
```

---

## Pack Roles

Every constituent pack in a composite has a role that determines how the agent uses it:

| Role | Purpose | Behavior |
|------|---------|----------|
| **voice** | Defines how the agent sounds and behaves | Agent loads this pack's presentation layer (speech patterns, personality, tone) into Tier 1. At most one pack should have this role. |
| **knowledge** | Provides domain expertise | Agent loads this pack's content per its declared context tiers. Multiple packs can have this role. |

### Voice vs. Knowledge

This distinction matters. When a founder's AI assistant answers a product question, it should:
- **Sound like** the founder (voice pack → person pack's `presentation/speech_patterns.md`)
- **Know about** the product (knowledge pack → product pack's `concepts/`, `workflows/`, etc.)

Without explicit roles, an agent might adopt the dry tone of a product manual or hallucinate personal opinions about technical features. The role system makes the separation clear.

### When No Voice Pack Exists

If no pack has `role: voice`, the agent uses its default personality. This is fine for deployments like multi-product support bots where no human persona is desired.

---

## Context Strategy in Composites

Composites aggregate the [context tiers](core.md#context-strategy) from all constituent packs. The loading process:

### 1. Collect Tier Declarations

Each constituent pack declares its own context tiers in its `manifest.yaml`. The composite starts with these.

### 2. Apply Role-Based Defaults

- **Voice pack:** `presentation/speech_patterns.md` is promoted to Tier 1 (always loaded) if not already there
- **All packs:** `manifest.yaml` and `overview.md` remain Tier 1 per core defaults

### 3. Apply Composite Overrides

The composite's `context.overrides` can promote or demote files for this specific deployment. This lets you tune token budget without modifying the underlying packs.

**Example:** A product pack marks `commercial/pricing.md` as Tier 2 (searchable), but a sales-focused composite promotes it to Tier 1 (always loaded) because pricing comes up in every conversation.

### 4. Token Budget Awareness

Multiple packs means more Tier 1 content competing for the context window. Composites should be deliberate about what's always-loaded:

- **Budget guideline:** Total Tier 1 content across all packs should stay under 10KB. If it exceeds this, review what's truly needed every conversation vs. what can be searched on demand.
- **The voice pack's Tier 1 takes priority** — personality files are needed on every turn.
- **Knowledge packs should lean on Tier 2** — let RAG pull relevant content per query rather than pre-loading everything.

---

## Cross-Pack Conflict Resolution

When multiple packs contain information about the same topic, conflicts can arise. The composite manifest defines how to handle them:

### Priority Order

```yaml
conflicts:
  priority: [jane-doe, acme-widget, acme-sales-process]
```

The priority list determines which pack's information takes precedence. Typically:
- Person packs rank highest (the human's word overrides documentation)
- Product packs rank above process packs (product truth over methodology)

### Resolution Strategy

| Strategy | Behavior |
|----------|----------|
| **flag** | Present both versions to the user and ask for resolution. Safest option. Default if not specified. |
| **priority** | Automatically use the higher-priority pack's version. Faster but risks silent errors. |

### Conflict Examples

- Person pack says "we deprecated Feature X last quarter" but product pack still documents it → person pack wins (priority) or flag for review
- Two product packs describe overlapping concepts differently → priority order or flag
- Process pack references a product capability that the product pack doesn't document → flag as a gap

---

## Supplements Directory

Sometimes a composite needs content that doesn't belong in any individual pack — bridging material that only makes sense in the context of multiple packs combined.

```
supplements/
├── cross-product-comparison.md    ← Comparing features across two product packs
├── founder-product-vision.md      ← Connecting the founder's philosophy to product decisions
└── unified-glossary.md            ← Terms used across all constituent packs
```

Supplement files follow the same rules as any ExpertPack content: Markdown, 1–3KB, section headers for RAG. They default to Tier 2 (searchable) unless overridden.

**Keep supplements minimal.** If content logically belongs in one pack, put it there. Supplements are for genuinely cross-cutting content.

---

## Creating a Composite

### Agent Workflow

1. **Identify the packs.** Determine which existing packs the deployment needs.
2. **Assign roles.** Decide which pack (if any) defines the agent's voice.
3. **Create the composite directory** with `manifest.yaml` and `overview.md`.
4. **Review combined Tier 1 budget.** Sum the always-loaded content from all packs. If it exceeds ~10KB, add context overrides to demote lower-priority files to Tier 2.
5. **Set conflict rules.** Define priority order and resolution strategy.
6. **Test retrieval.** Ask questions that span multiple packs to verify the agent pulls from the right sources and sounds consistent.
7. **Write supplements** only if cross-pack bridging content is genuinely needed.

### Example Composites

**Founder AI Assistant:**
```yaml
packs:
  - path: "../packs/jane-doe"
    role: voice
  - path: "../packs/acme-widget"
    role: knowledge
  - path: "../packs/acme-sales-process"
    role: knowledge
```
Sounds like the founder. Knows the product and sales methodology.

**Multi-Product Support Bot:**
```yaml
packs:
  - path: "../packs/product-a"
    role: knowledge
  - path: "../packs/product-b"
    role: knowledge
  - path: "../packs/product-c"
    role: knowledge
```
No voice pack — uses default agent personality. Routes questions to the right product pack.

**Personal Legacy AI:**
```yaml
packs:
  - path: "../packs/grandpa-bob"
    role: voice
  - path: "../packs/family-history-research"
    role: knowledge
```
Sounds like Grandpa Bob. Also knows the family's genealogical research.

---

## Auto-Discovery & Export

An AI agent running on a platform like OpenClaw accumulates knowledge across dozens of files over weeks or months — daily journals, session states, archived memories, project files, tool configs, learned preferences. Most of this raw state is noise for bootstrapping a new instance. The auto-discovery process distills an agent's accumulated knowledge into a structured composite ExpertPack.

### The Problem

A long-running agent's workspace might contain:
- 50+ daily journal files
- Memory archives with historical decisions
- Project status files for multiple products
- Tool configuration with learned infrastructure knowledge
- Behavioral patterns refined through hundreds of conversations
- Relationship context built up over time

Exporting this raw state is useless — it's too large, too noisy, and too platform-specific. What's needed is **distillation**: compress months of accumulated knowledge into structured, deduplicated, classified packs that a new instance can load and immediately be competent.

### Discovery Flow

When an agent is prompted to export itself as an ExpertPack:

```
1. SCHEMA FETCH
   Agent reads the public ExpertPack schemas (core.md, person.md, product.md, process.md, composite.md)
   to understand what pack types exist and what they contain.

2. STATE SCAN
   Agent inventories its own knowledge base:
   - Workspace files (SOUL.md, IDENTITY.md, AGENTS.md, TOOLS.md, USER.md, etc.)
   - Memory files (MEMORY.md, memory/*.md, session-state.md)
   - Project files (STATUS.md, project-specific docs)
   - Configuration (cron jobs, integrations, routines)
   - Conversation history (patterns, not raw transcripts)

3. KNOWLEDGE CLUSTERING
   Agent classifies each knowledge chunk by domain:
   - "This is about me (the agent)" → agent pack
   - "This is about my user" → person pack
   - "This is about Product X" → product pack
   - "This is how Process Y works" → process pack
   Clustering uses structural heuristics (file paths, content type) and
   semantic analysis (what is this knowledge actually about?).

4. COMPOSITE PROPOSAL
   Agent presents a proposed manifest to the user:
   "I've identified:
    - 1 agent pack (myself — subtype: agent)
    - 1 person pack (Brian Hearn)
    - 2 product packs (EasyTerritory, OpenClaw)
    - 3 process packs (deployment, backup-routines, content-publishing)
   Shall I proceed? Any adjustments?"

5. USER CONFIRMATION
   User reviews, adjusts scope (add/remove packs, rename, set access tiers),
   and confirms.

6. DISTILLATION
   For each proposed pack, the agent:
   a. Extracts relevant knowledge from raw state files
   b. Deduplicates — merges overlapping facts, prefers newest
   c. Resolves conflicts — flags ambiguities for user review
   d. Structures — writes EP-compliant files with proper frontmatter,
      headers, and cross-references per the relevant schema
   e. Validates — ensures nothing operationally critical was lost

7. COMPOSITE GENERATION
   Agent creates the composite manifest wiring all packs together:
   - Agent pack gets role: voice
   - All others get role: knowledge
   - Conflict priority order based on knowledge authority
   - Context tier overrides tuned for the deployment

8. PRIVACY REVIEW
   Agent flags sensitive content for user review:
   - API keys, tokens, passwords → NEVER included
   - Personal details about the user → access tier: private
   - Infrastructure specifics → access tier: private
   - General knowledge and patterns → access tier: public

9. PACKAGING
   Write all packs and the composite to disk. Commit to git.
   The result is a self-contained composite EP ready for import.
```

### Distillation Rules

The distillation step is where most of the value is created. Raw state → structured knowledge requires intelligent compression:

**Extraction:** Scan all state files and identify discrete knowledge assertions. A daily journal entry like "Figured out that the Bizzy droplet's SSH rate-limits after 3 rapid connections" becomes a fact in `operational/infrastructure.md` about SSH rate limiting.

**Classification:** For each assertion, determine which pack and section it belongs to. Ambiguous cases (is Caddy config knowledge about infrastructure or about a deployment process?) should be placed in the most actionable location and cross-referenced.

**Deduplication:** The same fact may appear in multiple journal entries, memory files, and session states. Merge into a single canonical assertion. When versions conflict, prefer the most recent unless an older version was explicitly confirmed.

**Compression ratio:** A well-distilled export should be **10–20% the volume** of the raw state while retaining **90%+ of actionable knowledge**. Six months of daily journals about deployment issues becomes a concise `process/deployment/` pack with lessons learned. Hundreds of session-state snapshots become a single `operational/routines.md` with the current operational patterns.

**What to discard:**
- Transient session state (what was in-progress at a specific moment)
- Routine heartbeat logs with no actionable findings
- Duplicate or superseded information
- Raw conversation transcripts (unless a specific exchange is worth preserving in `verbatim/decisions/`)

**What to always preserve:**
- Learned behavioral patterns and preferences
- Infrastructure knowledge and operational procedures
- Relationship context (especially communication preferences)
- Safety contracts and guardrails
- Failure post-mortems and lessons learned
- Tool expertise and integration knowledge

### Import & Hydration

The reverse of export: given a composite EP, bootstrap a new agent instance.

**Platform-specific hydration** maps EP files to platform state files. For OpenClaw:

| EP Source | OC Target | Notes |
|-----------|-----------|-------|
| `agent/{slug}/overview.md` | `SOUL.md` + `IDENTITY.md` | Split identity from personality |
| `agent/{slug}/mind/values.md` + `operational/safety.md` | `AGENTS.md` | Merge behavioral rules |
| `agent/{slug}/operational/tools.md` | `TOOLS.md` | Agent configures credentials separately |
| `agent/{slug}/relationships/people.md` (primary-user) | `USER.md` | Extract primary user entry |
| `agent/{slug}/operational/routines.md` | `HEARTBEAT.md` + cron jobs | Recreate platform-specific schedules |
| `agent/{slug}/presentation/` | `SOUL.md` (personality section) | Communication style and modes |
| `person/{slug}/` | `MEMORY.md` + `memory/` | User knowledge → memory files |
| `product/{slug}/` | Workspace project files | Product knowledge → reference docs |
| `process/{slug}/` | Workspace process docs | Process knowledge → runbooks |

**Post-hydration verification:** After import, the agent should be able to:
1. Correctly identify itself (name, personality, communication style)
2. Know its primary user (name, preferences, timezone, role)
3. Describe its available tools and infrastructure
4. Execute its standard routines (or know what routines to recreate)
5. Answer questions about its product and process domains

A quick verification prompt: *"Summarize who you are, who you work for, what tools you have, and what your typical day looks like."* A well-hydrated agent should answer all four confidently.

### Example: OpenClaw Instance Export

```yaml
# composites/easybot-full/manifest.yaml
name: "EasyBot — Full Instance Export"
slug: "easybot-full"
type: "composite"
version: "1.0.0"
schema_version: "1.0"
description: "Complete knowledge export of the EasyBot OpenClaw instance"
entry_point: "overview.md"

packs:
  - path: "../packs/easybot"
    role: voice
  - path: "../packs/brian-hearn"
    role: knowledge
  - path: "../packs/easyterritory"
    role: knowledge
  - path: "../packs/openclaw-ops"
    role: knowledge

conflicts:
  priority: [easybot, brian-hearn, easyterritory, openclaw-ops]
  strategy: "flag"

context:
  overrides:
    "easybot":
      always:
        - operational/safety.md
    "brian-hearn":
      on_demand:
        - verbatim/
```

---

## Relationship to Core Schema

Composites follow all [core.md](core.md) principles:
- Markdown-first for supplements
- Git-versioned
- Semantic versioning in the manifest
- Conflict resolution defers to humans

The key difference: composites contain *references* to packs, not knowledge content. The thin orchestration layer is intentional — knowledge belongs in packs, composition belongs in composites.

---

*Schema version: 1.1*
*Last updated: 2026-03-10*
