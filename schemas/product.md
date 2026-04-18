# Product Pack Schema

*Blueprint for ExpertPacks that capture deep knowledge about a product or platform — concepts, workflows, troubleshooting, and the tribal knowledge that lives in support teams' heads. Applicable to software, hardware, medical devices, consumer products, or any product with enough complexity to benefit from structured expert knowledge. This schema extends [core.md](core.md); all shared principles apply.*

**Schema version:** 4.0 (2026-04-18)

**What changed in 4.0** — Adopted the atomic-conceptual content model per [RFC-001](rfcs/RFC-001-atomic-conceptual-chunks.md). Removed `summaries/`, `propositions/`, and `sources/` directory recommendations. Per-concept FAQs and related terms now live inside concept files. See [core.md § Atomic-Conceptual Content Files](core.md#atomic-conceptual-content-files).

---

## Purpose

A product pack gives an AI agent the same depth of knowledge as a veteran product expert. Unlike generic RAG over documentation (which is written for humans browsing, not AI reasoning), a product pack structures knowledge around how support interactions actually flow — what things are, how to do things, what went wrong, and what the product costs.

**V1 Goal:** An agent that can *guide humans* through the product — answering questions, walking through workflows, and troubleshooting issues.

---

## Directory Structure

```
packs/{product-slug}/
├── manifest.yaml          ← Pack identity and metadata (required)
├── overview.md            ← Product summary — load first, always (required)
├── glossary.md            ← Term definitions + vocabulary bridging (recommended) ← See core.md Retrieval Optimization
├── entities.json          ← Entity cross-reference index (recommended)
│
├── concepts/              ← The mental model
│   ├── _index.md          ← Directory of all concepts
│   └── {concept}.md       ← One concept per file
│
├── workflows/             ← Step-by-step procedures
│   ├── _index.md          ← Directory of all workflows
│   └── {workflow}.md      ← One task per file
│
├── interfaces/            ← Interface documentation (UI screens, panels, endpoints, or physical controls)
│   ├── _index.md          ← Directory of all interfaces
│   └── {interface}.md     ← One interface per file (include variant notes where applicable)
│
├── specifications/        ← Technical specs, requirements, compliance (optional)
│   ├── _index.md
│   └── {spec}.md          ← One spec category per file
│
├── troubleshooting/       ← Problem resolution
│   ├── errors/            ← Specific error messages + fixes
│   │   └── {error}.md
│   ├── diagnostics/       ← "Not working" decision trees
│   │   └── {issue}.md
│   └── common-mistakes/   ← Gotchas and forgotten steps
│       └── {mistake}.md
│
├── faq/                   ← Cross-cutting questions only (optional, v4.0+: per-concept FAQs live in concept files)
│   └── {category}.md
│
├── facts/                 ← Product history (optional)
│   ├── timeline.md        ← Chronological product event history
│   └── releases.md        ← Significant releases with context and impact
│
├── decisions/             ← Architecture/product decision records (optional)
│   ├── _index.md          ← Directory of all decisions
│   └── {YYYY-MM-DD}-{slug}.md  ← One decision per file, dated
│
├── customers/             ← Customer reality layer (optional)
│   ├── _index.md
│   ├── segments.md        ← Who uses the product and how
│   ├── feedback.md        ← Pain points, objections, churn reasons, feature requests
│   └── success-stories.md ← Wins, case studies, reference customers
│
│
└── commercial/            ← Business/sales information (optional)
    ├── _index.md
    ├── capabilities.md
    ├── pricing.md
    ├── deployment.md
    ├── security.md
    ├── limitations.md     ← Known weaknesses, poor-fit scenarios, constraints
    └── landscape.md       ← Market positioning, key competitors, differentiation
```

**Required:** `manifest.yaml`, `overview.md`
**Recommended:** `entities.json`, `concepts/`, and `workflows/`
**Optional:** Everything else, based on pack focus and available content

---

## Why These Categories?

These aren't arbitrary. They map to how product interactions actually flow:

1. **Customer asks a question** → Check the relevant concept's `## Frequently Asked` section (v4.0) or `faq/` for cross-cutting questions
2. **Customer needs to do something** → Load the relevant `workflows/` file
3. **Customer doesn't understand something** → Load the relevant `concepts/` file
4. **Something went wrong** → Navigate `troubleshooting/` decision trees
5. **Prospect evaluating the product** → Load `commercial/` + `overview.md` + `customers/`
6. **"Why did we do X?"** → Load the relevant `decisions/` record
7. **"When did X happen?"** → Check `facts/timeline.md`
8. **"What do real users think?"** → Load `customers/feedback.md` + `customers/success-stories.md`

An agent answering a "how do I..." question should pull from `workflows/`. An agent answering a "what is..." question should pull from `concepts/`. An agent answering a "why did we..." question should pull from `decisions/`. This separation makes retrieval more precise.

---

## Content Templates

### overview.md

```markdown
# {Product Name}

## What It Is
One paragraph: what the product does, who it's for.

## Key Capabilities
- Capability 1
- Capability 2
- Capability 3

## How It Fits
Where this product sits in the broader ecosystem.

## Getting Started
How to access the product, first steps.
```

### Concept File (concepts/{concept}.md)

Mental model, terminology, how things work.

```markdown
# {Concept Name}

## What It Is
Clear explanation of the concept.

## Why It Matters
When/why users encounter this concept.

## How It Works
Mechanics, rules, behavior.

## Example
Concrete example to illustrate.

## Related
- [Other Concept](other-concept.md)
- [Relevant Workflow](../workflows/relevant-workflow.md)
```

#### Recommended: concepts/mental-model.md

Every product pack should include a `mental-model.md` as the root concept — the "what this product fundamentally IS" that all other concepts hang off of. This gives agents a conceptual understanding beyond technical architecture.

```markdown
# {Product Name} — Mental Model

## Core Abstraction
What the product fundamentally is, in one paragraph. The central metaphor or framing
that makes everything else make sense.

## How Value Flows
The path from user input to user outcome. What goes in, what happens, what comes out.
Not implementation detail — the conceptual pipeline.

## Key Abstractions
The 3-5 concepts a user must understand to use the product effectively.
Each links to its full concept file.

- [{Abstraction 1}]({concept-1}.md) — one-line role
- [{Abstraction 2}]({concept-2}.md) — one-line role
- [{Abstraction 3}]({concept-3}.md) — one-line role

## System Boundaries
What the product does and does NOT do. Where it ends and other tools begin.
Integrations, handoff points, and explicit non-goals.
```

### Workflow File (workflows/{workflow}.md)

Step-by-step procedures for accomplishing tasks. The Steps section adapts to the product type — for software this may describe screens and UI interactions; for hardware or physical products it may describe physical operations, adjustments, or checks; for APIs it may describe request sequences and expected responses.

```markdown
# {Task Name}

## Goal
What the user is trying to accomplish.

## Prerequisites
- What must be true before starting
- What they need to have ready

## Steps

### 1. {First Step}
{Action to take}

- **Where:** {Screen, panel, component, or area}
- **What to do:** {Specific action — click, adjust, connect, configure}
- **You should see/hear/feel:** {Expected result}

### 2. {Second Step}
...

## Completion
How to know it worked. What they should observe when done.

## Common Issues
- **{Problem}:** {Solution}

## Related
- [Relevant Concept](../concepts/relevant-concept.md)
- [Related Workflow](related-workflow.md)
```

### Interface File (interfaces/{interface}.md)

Documentation for an interface — UI screen, physical panel, API endpoint, or other interaction surface. For visual interfaces (UI screens, physical panels), use the **spatial-first format** below to organize elements by their physical screen region. For APIs, use a request/response contract format instead.

**Design principles for interface documentation:**

1. **Spatial-first layout.** Organize elements by their physical screen region, not by feature category. An agent guiding a user needs to say "in the top-left toolbar, the third icon..." — that requires spatial context.
2. **Element-level granularity.** Every clickable, editable, or stateful element gets its own entry. No hand-waving.
3. **Behavioral context.** Each element documents not just *what it is* but *what it does*, *when it's available*, and *what state it produces*.
4. **Markdown is the source of truth.** Screenshots are input during ingestion, not output. The markdown must be rich enough to fully describe every element's identity, location, and behavior without needing the image. Packs contain no binary assets.

**Naming convention:** kebab-case filenames. State variants can be separate files (`{screen-name}--{state}.md`) or documented as sections within the parent file, depending on complexity.

#### Visual Interface Template (UI screens, physical panels)

```markdown
---
sources:
  - type: screenshot-ingestion
    screen: "{screen-name}"
    captured: "YYYY-MM-DD"
    product_version: "{version}"
    captured_by: "{who}"
  - type: expert-walkthrough
    contributor: "{name}"
    date: "YYYY-MM-DD"
---

# {Screen/View Name}

{One-paragraph purpose statement: what this screen is for, when users see it, how they get here.}

---

## Region: {Region Name}

*Location: {spatial descriptor — e.g., "top bar, full width" | "left panel, below header" | "center overlay"}*

### {Sub-section or Tool Group}

{Brief description of this group's purpose.}

**Elements:**

| # | Element | Type | Location | Description | States/Behavior |
|---|---------|------|----------|-------------|-----------------|
| 1 | {Label/Name} | {type} | {position within region} | {What it does} | {When available, state changes, dynamic behavior} |
| 2 | ... | ... | ... | ... | ... |

### {Next Sub-section}
...

---

## Region: {Next Region}
...

---

## Interactions & Mode Switches

{Document mutual exclusivities, mode switches, state transitions between regions.}

## Dynamic Behavior

{Document elements that appear/disappear based on context, content, or state.}

## Related

- [{Workflow}](../workflows/{workflow}.md)
- [{Concept}](../concepts/{concept}.md)
- [{Other Interface}]({other-interface}.md)

## Open Questions

{Unresolved items needing expert clarification. Remove this section when all questions are resolved.}
```

See [Reference Tables: Interfaces](#reference-tables-interfaces) below for the standardized region taxonomy, element type vocabulary, and spatial descriptors to use in the `Type`, `Location`, and `Region` fields.

#### API / Endpoint Interface Template

```markdown
# {Interface Name}

## Purpose
What this interface is for, when clients interact with it.

## Endpoint
`{METHOD} {path}` — base URL, authentication requirements.

## Request Contract
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| {field} | {type} | {yes/no} | {description} |

## Response Contract
| Field | Type | Description |
|-------|------|-------------|
| {field} | {type} | {description} |

## Common Tasks
- [Related Workflow](../workflows/{workflow}.md)

## Error Codes
| Code | Meaning | Resolution |
|------|---------|------------|
| {code} | {why} | {fix} |
```

**Element detail guidelines (all interface types):**
- **Buttons / Controls:** What it does, prerequisites, what happens after
- **Fields / Parameters:** What data, required/optional, validation, examples
- **States:** Normal, loading, error states and how to detect them
- **Variants:** Platform or model differences to be aware of

#### Interface Quality Checklist

Before marking an interface document as complete:

- [ ] Every visible interactive element is documented
- [ ] Every element has a behavioral description (not just identification)
- [ ] Spatial attribution is clear enough for an agent to guide a user to any element
- [ ] Dynamic/conditional behavior is documented
- [ ] Mode switches and mutual exclusivities are noted
- [ ] Provenance frontmatter is present
- [ ] Cross-references to workflows and concepts are added
- [ ] Open Questions section is empty or removed (all resolved)

### Error File (troubleshooting/errors/{error}.md)

```markdown
# {Error Message or Code}

## When It Appears
What action triggers this error.

## What It Means
Why this error occurs.

## How to Fix
Step-by-step resolution.

## Prevention
How to avoid this error in the future.
```

### Diagnostic File (troubleshooting/diagnostics/{issue}.md)

```markdown
# {Problem Description}

*"I'm trying to {action} but {unexpected result}."*

## Expected Behavior
What should happen when everything is working correctly.

## Diagnostic Questions

### What are you seeing?
- **{Symptom A}** → [Check X](#check-x)
- **{Symptom B}** → [Check Y](#check-y)

### Check X
{Diagnostic step}
- **If {result}:** {Resolution}
- **If not:** [Check Y](#check-y)

## Common Causes
1. {Cause} — {Quick fix}
2. {Cause} — {Quick fix}
```

### Common Mistake File (troubleshooting/common-mistakes/{mistake}.md)

```markdown
# {Mistake Description}

## Symptom
What the user experiences.

## The Mistake
What they did (or didn't do).

## The Fix
How to correct it.

## How to Avoid
What to remember for next time.
```

### FAQ content (v4.0: embedded in concept files)

Schema v4.0+ packs embed FAQs inside the primary concept file they answer for, as H3 questions under a `## Frequently Asked` section. See [core.md § Atomic-Conceptual Content Files](core.md#atomic-conceptual-content-files).

A standalone `faq/` directory is only appropriate for cross-cutting questions that genuinely don't belong to any single concept (e.g., "What is {product-name}?"). Per-concept FAQs live with the concept; duplication across files is forbidden and will be flagged by `ep-validate`.

### Commercial Files (commercial/)

Business information for sales scenarios. See individual templates:

- **pricing.md** — Pricing model, tiers, what affects cost
- **deployment.md** — Architecture, requirements, data residency, or installation/unboxing and site requirements for hardware
- **security.md** — Certifications, data protection, authentication
- **capabilities.md** — What it can do, strengths, roadmap
- **limitations.md** — Known weaknesses, constraints, poor-fit scenarios (see below)
- **landscape.md** — Market positioning, competitors, differentiation (see below)

#### commercial/limitations.md

Every product has weaknesses. Documenting them explicitly prevents unrealistic or overly optimistic agent responses and helps route prospects to alternatives when the product isn't a good fit.

```markdown
# Limitations & Constraints

## Known Limitations
- {Limitation 1} — {context, workaround if any}
- {Limitation 2} — {context, workaround if any}

## Poor-Fit Scenarios
Situations where this product is NOT the right choice:
- {Scenario} — {why, what to recommend instead}

## Scaling Constraints
Performance or capacity boundaries the product hits at scale.

## Competitive Disadvantages
Areas where competitors genuinely do better. Be honest — agents that dodge
weaknesses lose credibility.

## Technical Debt (High-Level)
Known areas of the product that are aging, fragile, or overdue for rework.
Not implementation detail — just enough for an agent to set expectations.
```

#### commercial/landscape.md

Market positioning and competitive context. One file rather than per-competitor profiles — keeps maintenance manageable and prevents rot.

```markdown
# Market Landscape

## Positioning
Where this product sits in the market. Target segment, price tier, key differentiators.

## Key Competitors

### {Competitor 1}
- **Strengths:** {what they do well}
- **Weaknesses:** {where they fall short}
- **Target customers:** {who they serve best}
- **How we differ:** {honest differentiation}

### {Competitor 2}
...

## Differentiation Matrix

| Capability | Us | {Competitor 1} | {Competitor 2} |
|------------|-----|------|------|
| {Capability 1} | ✅ Strong | ⚠️ Partial | ❌ No |
| {Capability 2} | ⚠️ Partial | ✅ Strong | ✅ Strong |
```

**Maintenance note:** Competitive intelligence ages fast. Date the file and review quarterly. When a competitor entry hasn't been updated in 6+ months, flag it as potentially stale.

---

### Product Facts (facts/)

Historical and versioning context for the product. Optional but high-value for agents answering "when" and "why" questions.

#### facts/timeline.md

The product's chronological spine — events that shaped it. Parallel to the person pack's life timeline, adapted for product event types.

```markdown
# Product Timeline

## Early Development (2015–2016)

### 2015-Q3 — Project started
- **Type:** inception
- **Notes:** Initial prototype built as internal tool
- **Related:** [ADR-001: Build vs. buy decision](../decisions/2015-09-15-build-vs-buy.md)

### 2016-03 — Public launch
- **Type:** launch
- **Notes:** V1.0 released at partner conference
- **Related:** [V1.0 Release](releases.md#v10)

## Growth Phase (2016–2019)
...
```

**Event types:** `inception`, `launch`, `major-release`, `minor-release`, `pivot`, `outage`, `deprecation`, `architectural-rewrite`, `acquisition`, `partnership`, `pricing-change`, `security-incident`, `team-change`, `market-shift`, `milestone`

**Guidelines:**
- Organize by era with `##` headers (flexible — years, phases, or whatever fits the product's history)
- Each event gets a `###` header with date and short title
- Include: type, brief notes, and links to decisions/releases/related docs
- Keep entries brief — the timeline is a spine, not a narrative
- When the timeline exceeds ~50 events, split by era into separate files

#### facts/releases.md

Significant releases with context that changelogs don't capture — why the release mattered, expected impact, and any unintended consequences.

```markdown
# Significant Releases

## V3.0 — "Routing Engine Rewrite" (2024-06)

### What Changed
- Complete rewrite of the routing engine from scratch
- Bulk optimization now supports 500+ stops per route

### Why It Mattered
Customers were hitting the 50-stop limit and churning to competitors.
The old engine was architecturally unable to scale beyond this.

### Impact
- 40% reduction in routing-related support tickets
- Three enterprise deals closed that were blocked on routing capacity

### Unintended Consequences
- Legacy route files from V2 required manual migration
- Some V2 workarounds broke because the new engine handles edge cases differently

### Related
- [ADR-012: Routing engine rewrite](../decisions/2024-01-15-routing-engine-rewrite.md)
- [Timeline: V3.0 release](timeline.md#2024-06--v30-released)

---

## V2.5 — "Power BI Native Visual" (2023-01)
...
```

**Guidelines:**
- Focus on **significant** releases — not every patch. A release is significant if it changed user behavior, resolved a strategic gap, or had notable consequences.
- When the file grows beyond ~20 releases, split by major version (`facts/releases-v1.md`, `facts/releases-v2.md`)
- Link to timeline events and decision records

---

### Decision Records (decisions/)

Product and architectural decision records — the "why" behind the "what." Based on the ADR (Architecture Decision Record) pattern, extended to cover product decisions, not just technical ones.

Decision records prevent repeated debates and preserve institutional reasoning. When someone asks "why do we use X instead of Y?" or "why doesn't the product support Z?", the answer lives here.

#### Decision Record Template (decisions/{YYYY-MM-DD}-{slug}.md)

```markdown
# ADR-{NNN}: {Decision Title}

- **Date:** YYYY-MM-DD
- **Status:** accepted | superseded | deprecated | proposed
- **Superseded by:** [ADR-{NNN}](YYYY-MM-DD-new-decision.md) (if applicable)

## Context
What is the issue that we're seeing that is motivating this decision or change?

## Options Considered

### Option A: {Name}
- **Pros:** {advantages}
- **Cons:** {disadvantages}

### Option B: {Name}
- **Pros:** {advantages}
- **Cons:** {disadvantages}

## Decision
What is the change that we're proposing and/or doing?

## Rationale
Why this option over the others. The reasoning, not just the conclusion.

## Consequences
What becomes easier or more difficult to do because of this change?
Include both positive and negative consequences.

## Outcome (added retrospectively)
What actually happened after implementing this decision?
Added months/years later when the consequences are known.
```

**Guidelines:**
- File naming: `YYYY-MM-DD-{slug}.md` — date of the decision, kebab-case description
- Number decisions sequentially (ADR-001, ADR-002, ...) for easy reference in conversation
- Status lifecycle: `proposed` → `accepted` → optionally `superseded` or `deprecated`
- When a decision is superseded, add `superseded_by` link and update the old record's status — don't delete it
- The **Outcome** section is added retrospectively — it's some of the most valuable content because it captures what actually happened vs. what was expected
- Decision records are append-mostly: once accepted, the Context/Options/Decision/Rationale sections don't change. Only Status and Outcome get updated.

---

### Customer Reality Layer (customers/)

Grounds the product pack in actual user experience rather than internal engineering assumptions. Without this, agent responses skew toward feature lists and technical architecture while missing the human side — who uses this, what they struggle with, what success looks like.

#### customers/segments.md

Who uses the product and how. Combines traditional "personas" with concrete use case documentation.

```markdown
# Customer Segments

## {Segment Name} (e.g., "Sales Operations Leaders")

### Who They Are
Role, company size, industry vertical, technical sophistication.

### What They Use the Product For
Primary use cases, typical workflows, which features they rely on most.

### How They Measure Success
What "working" looks like for this segment. Metrics they care about.

### Common Pain Points
Recurring frustrations, unmet needs, things they wish were different.

### Related
- [Workflow: {Their key workflow}](../workflows/{workflow}.md)
- [Success Story: {Company}](#success-stories)

## {Next Segment}
...
```

#### customers/feedback.md

The unfiltered customer reality — pain points, objections, churn reasons, and feature requests. This is what the sales and support teams hear daily but rarely gets captured in product docs.

```markdown
# Customer Feedback

## Common Objections (Pre-Sale)
- **"{Objection}"** — {How to address it, what's true about it}
- **"{Objection}"** — {How to address it, what's true about it}

## Pain Points (Post-Sale)
- **{Pain point}** — {Frequency, severity, known workarounds, related roadmap items}

## Churn Reasons
- **{Reason}** — {How often, what segment, any preventive measures}

## Top Feature Requests
- **{Request}** — {Who wants it, business case, current status}
```

**Agent behavior:** When a prospect raises an objection that appears in this file, the agent should address it honestly — acknowledge what's true, explain what's being done, and avoid dismissing legitimate concerns.

#### customers/success-stories.md

Wins, case studies, and reference customers. Concrete evidence that the product delivers value.

```markdown
# Success Stories

## {Customer Name} — {One-line outcome}
- **Segment:** {Which segment they belong to}
- **Challenge:** {What they were trying to solve}
- **Solution:** {How they used the product}
- **Result:** {Quantified outcome if possible}
- **Quote:** "{Customer quote}" — {Person, Title}

## {Next Customer}
...
```

---

## Reference Tables: Interfaces

See [references/interface-vocabulary.md](references/interface-vocabulary.md) for standardized region names, element types, and spatial descriptors to use in interface element tables.

---

## Atomic-Conceptual Content

Schema v4.0+ product packs use **atomic-conceptual concept files**: each concept in `concepts/` is a self-contained retrieval unit carrying its definition, body, FAQs, related terms, and (optionally) key propositions in a single file. The deprecated `summaries/`, `propositions/`, and per-domain `glossary-{domain}.md` aggregator files are replaced by this model.

See [core.md § Atomic-Conceptual Content Files](core.md#atomic-conceptual-content-files) for the full pattern, and [`references/granularity-guide.md`](references/granularity-guide.md) for embed-vs-promote decision rules.

---

## Specifications Directory (specifications/)

Optional directory for technical specifications, requirements, and compliance information. Use when the product has formal specs, regulatory constraints, or technical compatibility matrices.

- **Software:** System requirements, API specifications, browser compatibility, performance benchmarks
- **Hardware:** Dimensions, materials, electrical ratings, operating conditions, safety certifications
- **Any product:** Compliance standards, regulatory certifications, compatibility matrices

Template for specifications/{spec}.md:

```markdown
# {Specification Name}

## Summary
One-paragraph summary of what this specification covers.

## Scope
What components, models, or versions this spec applies to.

## Details
Technical parameters, tolerances, compliance statements, or API contracts.

## Related
- [Related Specification](../specifications/other-spec.md)
- [Related Concept](../concepts/related-concept.md)
```

---

## Sources Directory (sources/) — DEPRECATED in v4.0

*The `sources/` ingestion-artifacts directory is deprecated in schema v4.0. It was found to score broadly as an aggregator during retrieval and was deleted from the reference ezt-designer pack on 2026-04-17 with measurable retrieval improvement. Source-provenance tracking lives in per-file `verified_at` / `source:` frontmatter (see [core.md](core.md#provenance-metadata)) and in the pack-level `sources/_coverage.md` coverage map. The old `sources/{source}.md` per-source index files are no longer part of the schema.*

### Source Index File (sources/{source}.md)

One file per major source material. For a video, this is a scene-by-scene index with timestamps and extracted artifacts. For a documentation site, this is a page inventory with extraction status.

**Video source template:**

```markdown
---
source_type: video
title: "{Video Title}"
duration: "MM:SS"
file: "{filename or URL}"
ingested: "YYYY-MM-DD"
---

# {Video Title}

## Overview
What this video covers, target audience, product version shown.

## Scene Index

| Timestamp | Scene | Entities | Extracted To |
|-----------|-------|----------|-------------|
| 00:00-01:30 | Introduction and login | authentication, dashboard | concepts/authentication.md |
| 01:30-03:45 | Creating a new project | projects, templates | workflows/create-project.md |
| 03:45-05:20 | Configuring settings | settings-panel, user-roles | interfaces/settings-panel.md |
| 05:20-06:00 | Common error: permissions | permission-denied | troubleshooting/errors/permission-denied.md |

## Extraction Status
- **Workflows extracted:** 3 of 5 identified
- **Interfaces documented:** 2 of 4 screens shown
- **Gaps:** Settings sub-panels not yet documented, error at 07:15 not captured
```

**Documentation source template:**

```markdown
---
source_type: documentation
url: "{base URL}"
pages_total: {N}
ingested: "YYYY-MM-DD"
---

# {Documentation Source Name}

## Pages Indexed

| Page | Status | Extracted To |
|------|--------|-------------|
| Getting Started | ✅ Complete | workflows/getting-started.md |
| API Reference | ✅ Complete | specifications/api.md |
| Troubleshooting | ⏳ Partial | troubleshooting/errors/ |
| Release Notes | ❌ Not started | — |
```

**Interview source template:**

```markdown
---
source_type: interview
with: "{Person Name}"
role: "{Their role}"
date: "YYYY-MM-DD"
duration: "MM:SS"
---

# Interview: {Person Name}

## Topics Covered

| Timestamp | Topic | Extracted To |
|-----------|-------|-------------|
| 00:00-05:30 | Common new-user mistakes | troubleshooting/common-mistakes/ |
| 05:30-12:00 | Undocumented feature: bulk import | workflows/bulk-import.md |
| 12:00-15:45 | Edge case: large datasets | faq/performance.md |

## Key Insights
- Bullet-point summary of tribal knowledge captured
- Things that surprised the interviewer or contradicted documentation

## Follow-up Needed
- Topics mentioned but not fully explored
- References to other people who know more
```

### Maintenance

Update source index files when:
- New content is extracted from an existing source
- A gap is filled that was previously noted
- The source material is updated (new product version, revised documentation)

Source indexes make re-ingestion efficient: when a product ships a new version, the builder agent can review source indexes to identify which videos/docs need re-processing and which pack files may be affected.

---

## Entity Cross-Reference (entities.json)

`entities.json` is a manually maintained cross-reference index at the pack root. It tells an agent *where to look* when a topic comes up.

### What It Solves

When new information arrives (e.g., "user roles now support custom permissions"), the agent needs to:
1. Know that `user-roles` is a documented entity
2. Find all files that discuss it — concept, workflows, FAQ mentions
3. Update all relevant files, not just one

Without a cross-reference, the agent would have to search every file — slow, error-prone, and likely to miss mentions in unexpected places.

### Structure

**Example** `entities.json` entry:

```json
{
  "entities": [
    {
      "id": "user-roles",
      "name": "User Roles",
      "type": "core-feature",
      "description": "Permission levels that control what users can see and do",
      "related": ["teams", "access-control"],
      "files": {
        "concept": "concepts/user-roles.md",
        "workflows": ["workflows/assign-role.md"],
        "mentions": ["overview.md", "faq/general.md"]
      }
    }
  ]
}
```

### Entity Types

| Type | Examples |
|------|---------|
| `core-feature` | Key capabilities, primary functions |
| `component` | Sub-systems, modules, physical parts |
| `integration` | Third-party connections, accessories, companion products |
| `infrastructure` | Underlying systems the product depends on |
| `category` | Umbrella groupings |
| `specification` | Technical specs, compliance standards, certifications |

### Maintenance

Update `entities.json` whenever:
- A new concept, workflow, or feature file is added
- A new entity is introduced in the product
- Cross-references change (a feature is mentioned in a new file)

This is a navigation index — structured data that helps agents *find* content, not content itself. The knowledge lives in `.md` files; `entities.json` just tells you where to look.

---

## Product-Specific Manifest Fields

Beyond the core manifest fields defined in [core.md](core.md):

```yaml
# Required
name: "Product Name"
slug: "product-slug"
type: "product"
version: "1.0.0"
description: "Expert knowledge for {product}"
entry_point: "overview.md"

# Product-specific
product_version: "2024.1+"
vendor: "Company Name"
website: "https://example.com"

# What personas this pack serves
focus:
  - support      # Customer support scenarios
  - sales        # Sales/marketing scenarios
  # - training   # Internal training

# What sections are included
sections:
  - concepts
  - workflows
  - troubleshooting
  - faq
  - commercial
  - facts
  - decisions
  - customers

# What topics/features are covered
scope:
  - feature-1
  - feature-2
  - integration-1

# Entry points
index_files: "_index.md"

# Dependencies (other packs required)
dependencies: []
```

---

## Agent Consumption Patterns

### Support Scenario
1. Load `manifest.yaml` + `overview.md` — understand the product
2. Classify the question: concept / how-to / troubleshooting / pricing
3. Load the relevant `_index.md` for the target section
4. Load the specific file that answers the question
5. Cross-reference related files via markdown links
6. Synthesize an answer that cites specific content

### Sales Scenario
1. Load `overview.md` + `commercial/capabilities.md`
2. Pull from `commercial/pricing.md`, `commercial/deployment.md`, or `commercial/security.md` as needed
3. Reference `concepts/` for technical depth
4. Check `customers/segments.md` — does this prospect match a known segment?
5. Reference `customers/success-stories.md` for social proof
6. Check `commercial/limitations.md` — be honest about fit; check `commercial/landscape.md` for competitive positioning

### Strategic / "Why" Scenario
1. Load `decisions/_index.md` — find the relevant decision record
2. Load the specific decision file for context, options, rationale, and outcome
3. Cross-reference `facts/timeline.md` for temporal context
4. Reference `facts/releases.md` if the question relates to a specific version

### Customer Objection Scenario
1. Load `customers/feedback.md` — find the specific objection or pain point
2. Cross-reference `commercial/limitations.md` — is the concern valid?
3. Reference `customers/success-stories.md` — how do similar customers succeed despite this?
4. Synthesize an honest response that acknowledges reality while providing context

### Update Scenario
1. New product information arrives
2. Load `entities.json` — identify affected entities
3. Find all files via entity cross-reference
4. Update Markdown files (following conflict resolution rules from [core.md](core.md))
5. Update `entities.json` if new entities or file references were created
6. Update `facts/timeline.md` if the change is historically significant
7. Update `facts/releases.md` if tied to a release

---

## Pack Population

For detailed guidance on all population methods — documentation ingestion, visual ingestion, video ingestion, technical artifact analysis, expert walkthroughs, observation & testing, and feedback mining — see the [Hydration Guide](../guides/hydration.md).

The guide covers each method's pipeline, strengths, limitations, and applicability across pack types. It also provides a recommended ordering for combining methods when building a product pack.

---

## Creating a New Product Pack

For the full agent-first creation playbook (initialization, population methods, entities.json, customer layer, history, decision records, retrieval layers), see [guides/hydration.md](../guides/hydration.md).

Key principles:
- Use the schema as the filing map. Decide where content belongs by content type (concepts, workflows, troubleshooting, etc.).
- Build `entities.json` as the knowledge graph emerges — it makes targeted updates fast.
- Record provenance for every file. Never overwrite expert-verified content without reconfirmation.
- Prioritize troubleshooting/ and interfaces/ early for support readiness.


*Schema version: 3.1*
*Last updated: 2026-04-10*
