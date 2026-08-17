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
schema_version: "1.2"

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

# Optional: conflict resolution (default strategy remains flag)
conflicts:
  priority: [jane-doe, acme-widget, acme-sales-process]  # First pack wins remaining ties
  strategy: "flag"    # fail_closed | flag | priority
  isolation:
    voice_must_not_assert_knowledge: true
    knowledge_must_not_override_voice: true
    respect_access_tiers: true
  tie_break: [authority_boundary, confidence, verified_at]

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
- **Sound like** the founder (voice pack → person pack's `presentation/speech-patterns.md`)
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

- **Voice pack:** `presentation/speech-patterns.md` is promoted to Tier 1 (always loaded) if not already there
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

When multiple packs contain information about the same topic, conflicts can arise. The composite declares the rules; the consumer applies them. Executable contract: [`tools/composite/conflict.py`](../tools/composite/conflict.py) (run `python tools/composite/test_conflict.py`). Markdown in the constituent packs remains canonical — this resolver does not write packs.

Resolution order is **fail-closed by construction**: isolation and authority run *before* strategy. A claim that should never have been visible must not win a priority tie.

### 1. Isolation

```yaml
conflicts:
  isolation:
    voice_must_not_assert_knowledge: true   # default
    knowledge_must_not_override_voice: true # default
    respect_access_tiers: true              # default
```

| Rule | Behavior |
|------|----------|
| `respect_access_tiers` | Drop claims whose `access_tier` is not in the consumer's allowed set (e.g. `family` / `private` never enter a `public` composite). |
| `voice_must_not_assert_knowledge` | A `role: voice` pack must not invent product/process facts. Tone travels; knowledge does not. |
| `knowledge_must_not_override_voice` | A knowledge pack must not rewrite speech, values, or persona. |

### 2. Authority

Drop any remaining claim that is outside its pack's [`authority_boundary`](core.md#authority-boundary) (`in_authority: false`). If nothing remains, **refuse** (no-source-no-claim). Do not guess.

### 3. Strategy (only after filters)

```yaml
conflicts:
  priority: [jane-doe, acme-widget, acme-sales-process]
  strategy: "flag"    # default; production help-bots should prefer fail_closed
  tie_break: [authority_boundary, confidence, verified_at]
```

The priority list is a *remaining-claim* order, not a license to leak isolated or out-of-authority content. Typical ranking: person/voice first, then product, then process.

| Strategy | Behavior |
|----------|----------|
| **fail_closed** | If remaining claims disagree, refuse. Do not pick a winner. Recommended for support / public composites. |
| **flag** | Present both versions and ask a human. Default if `strategy` is omitted (backward compatible). |
| **priority** | Use the first remaining pack in `priority`. Same-rank ties use `tie_break`. |

`tie_break` after isolation/authority: `confidence` rank is `expert-verified` > `crawled` > `inferred`, then newer `verified_at`.

### Worked examples

These three cases are encoded in `tools/composite/test_conflict.py`.

**1. Person vs product deprecation (flag).** Person pack: "Feature X was deprecated last quarter." Product pack: "Feature X is documented as current." Isolation does not apply (both are knowledge). Claims disagree → `strategy: flag` returns both; `fail_closed` refuses. Never silently merge into "supported."

**2. Shared term, two products (fail_closed).** Product A: "A territory is a zip cluster." Product B: "A territory is a sales team." Neither pack is out of authority for its own product. They disagree → `fail_closed` refuses rather than invent a blended definition.

**3. Family fact in a public composite (isolation).** Voice pack at `access_tier: family` asserts a health diagnosis. Knowledge pack has a public emigration date. `respect_access_tiers` with `allowed_tiers: [public]` drops the family claim *before* priority. The voice pack must not leak private facts even if it is first in `priority`.

---

## Supplements Directory

Sometimes a composite needs content that doesn't belong in any individual pack — bridging material that only makes sense in the context of multiple packs combined.

```
supplements/
├── cross-product-comparison.md    ← Comparing features across two product packs
├── founder-product-vision.md      ← Connecting the founder's philosophy to product decisions
└── unified-glossary.md            ← Terms used across all constituent packs
```

Supplement files follow the same rules as any ExpertPack content: Markdown, one dominant topic per file, retriever-friendly opening paragraph, and `##` section headers for RAG. Concept-like supplements should target 400–800 tokens with a 1,000-token ceiling. They default to Tier 2 (searchable) unless overridden.

**Keep supplements minimal.** If content logically belongs in one pack, put it there. Supplements are for genuinely cross-cutting content.

---

## Creating a Composite

### Agent Workflow

1. **Identify the packs.** Determine which existing packs the deployment needs.
2. **Assign roles.** Decide which pack (if any) defines the agent's voice.
3. **Create the composite directory** with `manifest.yaml` and `overview.md`.
4. **Review combined Tier 1 budget.** Sum the always-loaded content from all packs. If it exceeds ~10KB, add context overrides to demote lower-priority files to Tier 2.
5. **Set conflict rules.** Define isolation, `fail_closed` vs `flag` vs `priority`, and a remaining-claim priority list. Run `python tools/composite/test_conflict.py` against any custom cases.
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
- Raw conversation transcripts (unless a specific exchange is worth preserving as a `conversations/` atom or decision record)

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

### Example: Agent Instance Export

```yaml
# composites/atlas-full/manifest.yaml
name: "Atlas — Full Instance Export"
slug: "atlas-full"
type: "composite"
version: "1.0.0"
schema_version: "1.2"
description: "Complete knowledge export of the Atlas AI assistant instance"
entry_point: "overview.md"

packs:
  - path: "../packs/atlas"
    role: voice
  - path: "../packs/jamie-chen"
    role: knowledge
  - path: "../packs/acme-crm"
    role: knowledge
  - path: "../packs/deploy-workflow"
    role: knowledge

conflicts:
  priority: [atlas, jamie-chen, acme-crm, deploy-workflow]
  strategy: "flag"
  isolation:
    voice_must_not_assert_knowledge: true
    knowledge_must_not_override_voice: true
    respect_access_tiers: true
  tie_break: [authority_boundary, confidence, verified_at]

context:
  overrides:
    "atlas":
      always:
        - operational/safety.md
    "jamie-chen":
      on_demand:
        - conversations/
```

---

## Relationship to Core Schema

Composites follow all [core.md](core.md) principles:
- Markdown-first for supplements
- Git-versioned
- Semantic versioning in the manifest
- Conflict resolution is fail-closed by construction (isolation + authority first); `flag` still defers remaining disagreements to humans

The key difference: composites contain *references* to packs, not knowledge content. The thin orchestration layer is intentional — knowledge belongs in packs, composition belongs in composites.

---

*Schema version: 1.2*
*Last updated: 2026-08-17*
