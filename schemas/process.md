# Process Pack Schema

*Blueprint for ExpertPacks that capture a complex process — multi-phase endeavors like building a home, starting a business, or designing a landscape. This schema extends [core.md](core.md); all shared principles apply.*

---

## Purpose

A process pack turns an AI agent into an expert guide for a complex, multi-phase process. Unlike a product pack (which documents a specific tool) or a person pack (which captures a human), a process pack captures the *how-to* of a significant real-world endeavor — the phases, decisions, gotchas, and tribal knowledge that separate experienced practitioners from beginners.

The target user is someone undertaking a process for the first (or second) time who needs structured guidance without hiring a full-time consultant.

**Examples:**
- Architecting and building a new home
- Starting and incorporating a new business
- Creating a professional landscape design
- Planning and executing a kitchen renovation
- Setting up a home recording studio
- Navigating the private pilot certification process

---

## High-level design goals

1. Capture the sequential flow (phases) and the decision points that cause branches.
2. Surface the hard-won heuristics (gotchas) and examples that make novices competent quickly.
3. Provide the operational artifacts people actually need: checklists, templates, budgets, schedules, and regulatory references.
4. Keep files small and focused so RAG retrieves precise chunks (1–3KB per file guideline).
5. Make the pack discoverable via `_index.md` files and manifest-declared context tiers.

---

## Directory Structure (recommended)

```
packs/{process-slug}/
├── manifest.yaml          ← Pack identity and metadata (required)
├── overview.md            ← What this process is, who it's for (required)
├── variants.md            ← Major process forks and alternative paths (recommended)
│
├── fundamentals/          ← Core concepts & domain knowledge required before starting
├── glossary/              ← Terminology and short definitions (searchable)
├── phases/                ← Sequential stages of the process (backbone)
├── decisions/             ← Key decision points with criteria and tradeoffs
├── checklists/            ← Actionable, phase-aligned checklists
├── exceptions/            ← Failure modes, escalation paths, recovery procedures
├── scheduling/            ← Timelines, dependencies, lead times, seasonal constraints
├── budget/                ← Cost breakdowns, financing, templates, cost drivers
├── roles/                 ← Stakeholders, responsibilities, how to work with them
├── regulations/           ← Permits, codes, licensing, compliance & region notes
├── templates/             ← Document templates, contracts, applications, forms
├── resources/             ← Tools, vendors, materials, buying guides
├── examples/              ← Case studies, post-mortems, and retrospectives
├── gotchas/               ← Common mistakes, traps, and prevention patterns
└── faq/                   ← Cross-cutting questions only (optional, v4.0+: per-concept FAQs live inside concept files)
```

Notes:
- Each directory should include `_index.md` describing contents and links to files.
- Files should be named kebab-case and kept focused (one topic per file).
- `fundamentals/` and `glossary/` help novices build mental models before they act.
- `gotchas/` captures preventive knowledge ("don't forget X"); `exceptions/` captures reactive knowledge ("X happened, now what").

---

## Manifest Extensions

Process packs extend the [core manifest](core.md) with these fields:

```yaml
# Required
name: "Building a Custom Home"
slug: "custom-home-build"
type: "process"
version: "1.0.0"
description: "Complete guide to architecting and building a custom home"
entry_point: "overview.md"

# Process-specific fields
domain: "construction"              # High-level domain (construction, business, creative, etc.)
typical_duration: "12-18 months"    # Typical timeline
complexity: "high"                  # low | medium | high
cost_range: "$250K–$1M+"           # Approximate cost range (optional)
professional_required: true          # Whether professionals are typically needed
regions: ["US"]                     # Geographic relevance (if applicable)

# Sections included (manifest-driven inventory)
sections:
  - fundamentals
  - glossary
  - phases
  - decisions
  - checklists
  - exceptions
  - scheduling
  - budget
  - roles
  - regulations
  - templates
  - resources
  - examples
  - gotchas
  - faq

# Recommended context strategy (manifest context block supported by core.md)
context:
  always:
    - overview.md
    - manifest.yaml
  searchable:
    - fundamentals/
    - glossary/
    - phases/
    - decisions/
    - checklists/
    - exceptions/
    - resources/
    - roles/
    - regulations/
    - examples/
    - gotchas/
    - faq/
    - variants.md
  on_demand:
    - templates/
    - budget/
    - scheduling/
```

---

## Component Templates (high-level)

Below are templates and guidance for the most important directories.

### Overview (`overview.md`)

Keep this short and always-loadable. The agent should load this on every session to understand the pack's scope.

```markdown
# {Process Name}

## What This Process Is
One paragraph describing the end result and who benefits.

## Who This Is For
Primary audience and skill level.

## Typical Duration & Cost
High-level ranges and major cost drivers.

## Phase Map
The ordered sequence of all phases with dependencies and typical durations.
This is the structural backbone — an agent reads this to understand the
full process arc before diving into any specific phase.

1. **[{Phase 1}](phases/{phase-1}.md)** — {one-line purpose} ({duration})
2. **[{Phase 2}](phases/{phase-2}.md)** — {one-line purpose} ({duration})
   - Depends on: Phase 1 completion
3. **[{Phase 3}](phases/{phase-3}.md)** — {one-line purpose} ({duration})
   - Depends on: Phase 2 deliverables
   - Can run in parallel with: Phase 4
4. **[{Phase 4}](phases/{phase-4}.md)** — {one-line purpose} ({duration})

## Major Variants
Brief summary of the major forks in this process. See [variants.md](variants.md)
for full detail on how each variant changes the phase sequence.

- **{Variant A}** — {how it differs, which phases change}
- **{Variant B}** — {how it differs, which phases change}

## When to Get Professional Help
Which parts typically require external experts.
```

### Fundamentals (`fundamentals/{topic}.md`)

Conceptual material that helps the user understand *why* steps exist.

```markdown
# Fundamentals: {Topic}

## What It Is
Short definition and why it matters.

## How It Works
High-level mechanics and mental models.

## Where It Shows Up
Links to phases/decisions where this concept matters.

## Further Reading
Links to deeper resources.
```

### Glossary (`glossary/{term}.md`)

Short, plain-English definitions for domain terms. Useful for RAG when users ask "what is X?".

### Phases (`phases/{phase}.md`)

Phases are the backbone of the process. Each phase file is a self-contained guide to that stage — what goes in, what happens, what comes out, and what can go wrong.

```markdown
# Phase: {Phase Name}

## Overview
What this phase accomplishes and why it matters.

## Inputs / Prerequisites
What must exist before this phase can start:
- **Preceding phases:** [{Phase X}]({phase-x}.md) must be complete
- **Artifacts needed:** {documents, approvals, materials, decisions}
- **Conditions:** {seasonal, regulatory, financial readiness}

## Completion Triggers
How to know this phase is done — not just "activities finished" but
observable criteria an agent can verify:
- [ ] {Deliverable 1} produced and approved
- [ ] {Inspection/review} passed
- [ ] {Handoff} to {next phase/role} completed

## Duration & Lead Times
Typical duration and items with long lead times (e.g., windows, custom cabinets).

## Key Activities
- Activity 1
- Activity 2

## Roles Involved
Who participates in this phase and what they do:
- **{Role}** — {responsibility in this phase}
- **{Role}** — {responsibility in this phase}

## Deliverables
Artifacts produced at the end of the phase.

## Handoffs
What gets passed to the next phase and to whom:
- **To [{Next Phase}]({next-phase}.md):** {what artifacts/approvals transfer}
- **To [{Role}](../roles/{role}.md):** {what they need to receive}

## Budget Items
Summarize the major budget lines relevant to this phase and link to budget files.

## Variants
How this phase changes under different process variants (if applicable):
- **{Variant A}:** {what's different — skipped steps, additional requirements, different roles}
- **{Variant B}:** {what's different}
See [variants.md](../variants.md) for the full variant overview.

## Checklist
Link to `checklists/{phase}-checklist.md`.

## Common Mistakes
Link to gotchas.

## What Can Go Wrong
Link to relevant `exceptions/` files for failure modes specific to this phase.
```

### Decisions (`decisions/{decision}.md`)

Decision templates unchanged — emphasize cost, schedule, and risk tradeoffs. Always link to phases and budget impact.

### Checklists (`checklists/{checklist}.md`)

Actionable items with verification steps and sign-off criteria.

### Scheduling (`scheduling/{schedule}.md`)

Guidance on sequencing, parallel work, seasonal constraints, and a few example Gantt templates. Include notes on lead times and supplier SLAs.

### Budget (`budget/{budget-template}.md`)

Breakdowns and templates for estimating and tracking costs. Include example spreadsheets or CSV snippets for ingestion.

### Roles (`roles/{role}.md`)

Define stakeholder roles, scope, how to hire/contract them, typical costs, and what good looks like.

```markdown
# Role: {Role Name}

## What They Do
Core responsibilities and scope of this role in the process.

## Authority Level
What decisions this role can make:
- **Decision-maker:** {what they decide unilaterally}
- **Advisor:** {what they recommend but don't decide}
- **Executor:** {what they carry out}
- **Approver:** {what requires their sign-off}

## When They're Involved
Which phases this role participates in and how:
- [Phase X](../phases/{phase-x}.md) — {their role in this phase}
- [Phase Y](../phases/{phase-y}.md) — {their role in this phase}

## How to Find / Hire
Where to find this person, typical costs, red flags, what good looks like.

## Working With Them
Communication expectations, how often to check in, common friction points.
```

### Regulations (`regulations/{topic}.md`)

Permits, codes, licenses. Include jurisdiction notes and links to authoritative sources. Mark sensitive legal content as guidance, not legal advice.

### Templates (`templates/{template}.md`)

Contracts, purchase orders, RFIs, permit application checklists. Prefer short, editable templates.

### Exceptions (`exceptions/{exception}.md`)

Failure modes, escalation paths, and recovery procedures. While `gotchas/` captures preventive knowledge ("don't forget X"), exceptions capture reactive knowledge ("X happened, now what"). Every non-trivial process has failure modes — permits get denied, vendors go bankrupt, inspections fail, funding falls through.

```markdown
# Exception: {Failure Description}

## What Happened
The failure mode — what went wrong and how you'd recognize it.

## Which Phase(s)
Where in the process this can occur:
- [Phase X](../phases/{phase-x}.md) — {how it manifests in this phase}

## Impact
What this failure does to the overall process:
- **Timeline:** {delays, blocked phases}
- **Budget:** {additional costs, sunk costs}
- **Quality:** {compromises required}

## Escalation Path
Who needs to know and in what order:
1. {First contact — role, what to tell them}
2. {Second contact — if first can't resolve}

## Recovery Procedure
Step-by-step recovery:
1. {Immediate action — stop the bleeding}
2. {Assessment — understand scope of damage}
3. {Resolution — fix or work around}
4. {Verification — confirm recovery is complete}

## Fallback / Alternative
If recovery isn't possible, what's the alternative path?

## Prevention
How to reduce the likelihood of this failure in the future.
Link to relevant `gotchas/` entries.
```

**Guidelines:**
- One file per failure mode — keep them focused and independently retrievable
- Link exceptions to the phases where they can occur
- Include real examples when available (from `examples/` case studies)
- Distinguish between recoverable failures (fix and continue) and process-ending failures (must restart or abandon)

### Variants (`variants.md`)

Most real-world processes have major forks — building with a general contractor vs. owner-building, incorporating as an LLC vs. S-Corp, renovating a kitchen vs. a full gut job. `variants.md` documents these top-level forks and how they change the phase sequence.

```markdown
# Process Variants

## Default Path
Brief description of the "standard" path the phase sequence assumes.

## Variant: {Variant Name}

### When to Choose This
Under what circumstances this variant applies.

### How It Differs
Which phases change, which are skipped, which are added:
- **{Phase X}:** {modified — what's different}
- **{Phase Y}:** {skipped in this variant}
- **{New Phase}:** {added — only in this variant}

### Implications
- **Timeline:** {faster/slower, by how much}
- **Budget:** {cheaper/more expensive, why}
- **Risk:** {higher/lower, what changes}
- **Professional requirements:** {different roles needed}

## Variant: {Next Variant}
...
```

**Guidelines:**
- Phase files reference `variants.md` and include a `## Variants` section noting how they change per variant
- Variants are not separate packs — they're documented forks within one pack
- If a variant changes more than ~60% of the phases, consider whether it should be a separate process pack instead

### Examples and Retrospectives (`examples/`)

Case studies, post-mortems, and retrospective learnings. Include a `## Lessons Learned` section in every example to feed continuous improvement.

```markdown
# Example: {Case Study Title}

## Context
Who did this, when, and under what constraints.

## What Happened
Narrative of how the process played out — decisions made, surprises encountered.

## Outcome
Results — timeline, budget, quality compared to plan.

## Lessons Learned
What worked well, what didn't, and what the person would do differently.
Link to relevant `gotchas/` or `exceptions/` entries that were created
or validated by this experience.
```

### Resources, Gotchas, FAQ

Keep these as before but follow the small-file guideline. Cross-link heavily.

---

## Atomic-Conceptual Content

Schema v4.1 process packs use **atomic-conceptual concept files** the same way product packs do: each concept in `concepts/` (or fundamentals file) is a self-contained retrieval unit sized to fit in one RAG chunk (1,000-token ceiling). Concepts that would exceed the ceiling split into independent atoms; cross-atom dependencies are declared via the `requires:` frontmatter field. The deprecated v3 aggregator pattern (`summaries/`, `propositions/`, per-domain `glossary-{domain}.md`, standalone `faq/`) is replaced by this model.

**Process-pack specifics:**
- `phases/*.md` files are atomic workflows by default (`retrieval_strategy: atomic`) — they retain their step-by-step structure and are NOT absorbed into concept files.
- `decisions/*.md` files remain a first-class type; they document tradeoff reasoning and act as decision records, not concepts.
- `gotchas/` entries live as their own atomic files (same as `troubleshooting/common-mistakes/` in product packs).
- Fundamental concepts and conceptual knowledge gain the same atomic-conceptual treatment: one self-contained file per concept with `## Frequently Asked` and `## Related Terms` sections as needed.

See [core.md § Atomic-Conceptual Content Files](core.md#atomic-conceptual-content-files) for the full pattern, and [`references/granularity-guide.md`](references/granularity-guide.md) for embed-vs-promote and when-to-split decision rules.

---

## Agent Consumption Patterns

- Start with `overview.md` (Tier 1) to route the user's question and understand the phase map.
- Use `_index.md` files to identify candidate files.
- Prefer `fundamentals/` and `glossary/` for conceptual questions.
- Use `phases/` for step-by-step guidance and `checklists/` for action items.
- Check `phases/{phase}.md` **Inputs / Prerequisites** to determine readiness before advising someone to start a phase.
- Use `decisions/` for tradeoff reasoning and `budget/` and `scheduling/` for planning tasks.
- When the user's situation involves a variant (e.g., "I'm owner-building"), load `variants.md` first, then load phase files with awareness of variant-specific differences.
- When something goes wrong, check `exceptions/` for failure-specific recovery procedures — don't confuse with `gotchas/` (which is preventive, not reactive).
- Load `templates/` and full `budget/` spreadsheets on demand (Tier 3).
- Reference `examples/` for real-world context and lessons learned.

---

## Pack Population

For detailed guidance on all population methods, see the [Hydration Guide](../guides/hydration.md).

For process packs, the recommended combining order is:
1. Documentation ingestion → SOPs, runbooks, compliance docs
2. Expert walkthrough → practitioners explain the reality vs. the docs
3. Technical artifact analysis → scripts, automation, monitoring configs
4. Feedback mining → incident reports, audit findings
5. Observation & testing → walk through each phase
6. Consolidate into atomic-conceptual files → per [core.md Atomic-Conceptual Content Files](core.md#atomic-conceptual-content-files), ensure each concept's definition, FAQs, and related terms co-locate in a single concept file. Avoid aggregator directories (`summaries/`, `propositions/`, per-domain glossary files) — they score broadly and displace specific content at retrieval time.

Prioritize practitioner interviews for decisions and gotchas. Use authoritative sources for regulations. Capture real timelines and budgets from case studies in `examples/`.

---

*Schema version: 4.1*
*Last updated: 2026-04-19*
