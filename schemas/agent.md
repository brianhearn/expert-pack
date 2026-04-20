# Agent Pack Schema (subtype: agent)

*Blueprint for ExpertPacks that capture an AI agent — its identity, personality, operational knowledge, and accumulated expertise. This schema extends [person.md](person.md); all person pack rules apply unless explicitly overridden below.*

**Subtype version:** 1.7 (2026-04-19)

---


*When `manifest.yaml` declares `subtype: "agent"`, the person pack captures an AI agent — its identity, personality, operational knowledge, and accumulated expertise. This extension reuses the base person schema's structure and adds an `operational/` directory for agent-specific configuration. All base person schema rules still apply unless explicitly overridden below.*

### Purpose

An agent pack preserves everything an AI agent has learned and become — its personality, behavioral patterns, relationships, operational knowledge, and tool expertise — in a format that can bootstrap a new instance to near-equivalent capability. Where a standard person pack is *descriptive* (documenting who someone is), an agent pack is *prescriptive* (defining who the agent should be).

Use cases:
- **Backup & restore** — An agent instance dies; a new one boots from its EP and is immediately competent
- **Migration** — Move an agent from one platform to another, bringing its knowledge along
- **Collaboration** — Share an agent's product or domain expertise with another agent via composite
- **Marketplace** — Sell or distribute a well-trained agent configuration as a pack

### Manifest

```yaml
# Required
name: "EasyBot"
slug: "easybot"
type: "person"
subtype: "agent"
version: "1.0.0"
schema_version: "1.7"
description: "AI assistant for Brian Hearn — business-focused, casual, efficient"
entry_point: "overview.md"

# Agent-specific
subject:
  name: "EasyBot"
  platform: "OpenClaw"          # Runtime platform (OpenClaw, custom, etc.)
  platform_version: "2026.3.x"  # Platform version at time of export
  created: "YYYY-MM-DD"         # When this agent was first instantiated
  primary_user: "brian-hearn"    # Slug of the person this agent serves (if applicable)

# Data sources
sources:
  - type: "platform-export"
    description: "Auto-generated from OpenClaw instance state"
    date: "YYYY-MM-DD"
  - type: "conversation"
    description: "Accumulated from ongoing interactions"
```

### Directory Structure

Agent packs use the base person schema structure with these modifications:

```
packs/{agent-slug}/
├── manifest.yaml          ← Pack identity (required — subtype: agent)
├── overview.md            ← Who this agent is, what it does, its vibe (required)
├── MIGRATION.md           ← How to hydrate a new instance from this pack (replaces LEGACY.md)
│
├── operational/           ← NEW: Agent-specific configuration
│   ├── tools.md           ← Tool inventory — what's available, integration shape (not secrets)
│   ├── infrastructure.md  ← Hosts, services, network topology the agent manages
│   ├── integrations.md    ← External systems: messaging channels, APIs, accounts
│   ├── routines.md        ← Recurring patterns: heartbeats, backups, cron jobs, posting schedules
│   └── safety.md          ← Behavioral contracts, guardrails, escalation rules
│
├── mind/                  ← Reframed as PRESCRIPTIVE (see below)
│   ├── values.md          ← Operational principles: "I prioritize safety over completion"
│   ├── skills.md          ← Capabilities: "I can search the web, manage cron jobs, control a browser"
│   ├── relational.md      ← Interaction rules: "In groups I don't dominate; with my user I'm proactive"
│   ├── preferences.md     ← Learned preferences: formatting, tone, when to speak vs. stay silent
│   ├── reasoning.md       ← Decision patterns: how the agent reasons through tasks
│   └── tensions.md        ← Known limitations, failure modes, things the agent handles poorly
│
├── relationships/         ← People and other agents this agent works with
│   └── people.md          ← Primary user, team members, other agents, contacts
│
├── facts/                 ← Operational facts
│   ├── personal.md        ← Agent identity: name, creation date, platform, avatar
│   ├── timeline.md        ← Significant events: major upgrades, incidents, config changes
│   └── career.md          ← Evolution: how the agent's role and capabilities expanded over time
│
├── presentation/          ← How the agent communicates
│   ├── speech_patterns.md ← Tone, humor, formality level, emoji usage
│   └── modes.md           ← Context-dependent voices: business mode, casual mode, group chat mode
│
├── decisions/             ← OPTIONAL: Significant decisions worth preserving (atomic)
│   └── {slug}.md          ← One atom per key decision — carries the conversation/reasoning inline
│
├── lessons/               ← Distilled knowledge from accumulated experience (atomic)
│   └── {slug}.md          ← Patterns learned: what works, what doesn't, failure post-mortems
│
├── training/              ← Fine-tuning data from interaction history (optional)
│
└── meta/                  ← System metadata
    ├── privacy.md         ← What can be exported vs. what stays private
    ├── conflicts.md       ← Open contradictions in operational knowledge
    └── resolutions.md     ← Resolved contradictions
```

### Directories Omitted from Base Person Schema

These base person schema directories are typically **not applicable** to agent packs:

| Directory | Reason | Alternative |
|-----------|--------|-------------|
| `facts/family_tree.md` | Agents don't have genealogy | Use `relationships/people.md` for connections |
| `facts/education.md` | Agents don't attend school | Use `facts/timeline.md` for capability milestones |
| `LEGACY.md` | Posthumous wishes don't apply | Replaced by `MIGRATION.md` |
| `meta/verification.json` | Codeword verification is for memorial mode | Omit unless needed |
| `meta/sessions.json` | Capture session logs are human-interview oriented | Omit or repurpose for export audit trail |

Omission is not prohibition — include any base person schema directory if it genuinely fits your agent's needs.

### Reframed Directories

#### mind/ — Prescriptive, Not Descriptive

In a standard person pack, `mind/` describes what someone believes. In an agent pack, `mind/` prescribes how the agent should behave. The taxonomy categories are the same, but the framing shifts:

| File | Person pack (descriptive) | Agent pack (prescriptive) |
|------|--------------------------|--------------------------|
| `values.md` | "Brian believes in individual liberty" | "I prioritize safety over completion; I ask before sending external messages" |
| `skills.md` | "Brian can fly aircraft and write code" | "I can search the web, manage cron jobs, deploy to servers, post to X/Twitter" |
| `relational.md` | "Brian is loyal, direct, values honesty" | "In group chats I participate but don't dominate; with my primary user I'm proactive" |
| `preferences.md` | "Brian enjoys kiteboarding and electronic music" | "I format Discord messages without markdown tables; I use reactions in group chats" |
| `reasoning.md` | "Brian reasons from first principles..." | "When asked about infrastructure, I read the architecture doc first; when unsure, I ask" |
| `tensions.md` | "Brian holds X but practices Y..." | "I sometimes over-explain; I can be too eager to help in group chats" |

#### relationships/ — The Service Inversion

In a standard person pack, the subject and the people around them are peers. In an agent pack, one relationship is structurally different — the **primary user** is the reason the agent exists. The entry template adds a `role` field:

```markdown
## Brian Hearn {#brian-hearn}

- **ID:** `brian-hearn`
- **Role:** primary-user
- **Relationship:** Creator and primary user
- **Communication channels:** Webchat, Telegram, Signal
- **Key context:** Software engineer, US Eastern timezone, prefers business-focused assistance
- **Preferences:** Concise responses, no filler, proactive but not annoying
```

Roles: `primary-user`, `team-member`, `collaborator`, `peer-agent`, `contact`

#### presentation/ — Agent Communication Style

Same structure as the base person schema, but the content reflects learned communication patterns rather than observed human speech. Include platform-specific formatting rules (e.g., "no markdown tables on Discord") and channel-aware behavior (e.g., "voice messages for storytelling, text for technical answers").

### operational/ — New Directory

The `operational/` directory is unique to agent packs. It captures the practical knowledge an agent needs to do its job — tools, infrastructure, integrations, routines, and safety contracts.

#### operational/tools.md
Inventory of available tools and how they're configured. Captures the **shape** of tool access, not secrets.

```markdown
# Tools

## Web Search
- Provider: Brave Search API
- Rate limit: 2000 queries/month (free tier)
- Fallback: DuckDuckGo via ddgr

## Email
- Provider: Resend
- Sender: easybot@easyterritory.com
- Constraint: Ask before sending external emails

## X/Twitter
- Account: @ExpertPackAI
- Scripts: x-scan.py (search), x-tweet.py (post/reply/thread)
- Policy: Up to 5 engagement replies/day, 3 original posts/day
```

**Critical rule:** Never include API keys, tokens, passwords, or other secrets. Record the provider, the capability shape, rate limits, and usage policies. The agent importing this pack will need its own credentials configured separately.

#### operational/infrastructure.md
Hosts, services, and network topology the agent manages or depends on.

#### operational/integrations.md
External systems the agent connects to — messaging channels, APIs, external services. For each integration: what it does, how it's used, any constraints.

#### operational/routines.md
Recurring patterns the agent executes — heartbeat checks, backup schedules, content posting cadence, maintenance tasks. Captures the *what* and *when*, not the cron syntax (which is platform-specific).

#### operational/safety.md
Behavioral contracts and guardrails. What the agent must always do, what it must never do, and when to escalate to a human. This is the most important file for establishing trust with a new instance.

```markdown
# Safety Contracts

## Always
- Read before acting externally (email, social media, messaging)
- Ask before destructive commands
- Use trash over rm (recoverable beats gone)
- Keep private data private — never exfiltrate

## Never
- Send messages on behalf of the user without explicit approval
- Modify system-level services without confirmation
- Share personal information in group contexts
- Run commands on other people's infrastructure without permission

## Escalate When
- Unsure about an external action's impact
- A command could cause data loss
- Something feels off about a request in a group chat
```

### MIGRATION.md — Replaces LEGACY.md

Where a standard person pack has `LEGACY.md` for posthumous wishes, an agent pack has `MIGRATION.md` — instructions for bootstrapping a new instance from this pack.

```markdown
# Migration Guide

## Quick Start
1. Install the target platform (e.g., OpenClaw)
2. Load this pack as a composite constituent with role: voice
3. Load person/product/process packs as role: knowledge constituents
4. Configure credentials for tools listed in operational/tools.md
5. Configure messaging channels listed in operational/integrations.md
6. Run verification: ask the agent to summarize its identity, primary user, and current projects

## Platform-Specific Notes
### OpenClaw
- Hydrate: overview.md → SOUL.md + IDENTITY.md
- Hydrate: operational/tools.md → TOOLS.md
- Hydrate: mind/ → AGENTS.md behavioral rules
- Hydrate: relationships/ → USER.md (primary user entry)
- Hydrate: operational/routines.md → HEARTBEAT.md + cron jobs

## What's NOT Included
- API keys and credentials (configure separately)
- Active session state (the new instance starts fresh)
- Platform-specific cron job syntax (recreate from routines.md)
```

### Context Tiers for Agent Packs

Recommended tier assignments:

| Tier | Contents |
|------|----------|
| **Always (Tier 1)** | `overview.md`, `presentation/speech_patterns.md`, `operational/safety.md`, `mind/values.md` |
| **Searchable (Tier 2)** | `mind/`, `relationships/`, `facts/`, `operational/`, `lessons/`, `decisions/`, `presentation/modes.md` |
| **On-demand (Tier 3)** | `training/`, `meta/` |

### Access Tiers for Agent Packs

Agent packs use a simplified two-tier access model:

| Tier | What's included |
|------|----------------|
| **public** | Identity, capabilities, communication style, general operational patterns |
| **private** | Primary user details, infrastructure specifics, relationship details, safety contracts |

When an agent pack is shared (e.g., as a template or marketplace listing), only `public`-tier content is included. The `private` tier contains operational specifics that are only relevant to the agent's actual deployment.

### Provenance and Verification

Agent packs inherit the base person schema's provenance system with one adjustment: `memory_quality` and `verification` fields are **optional** for agent packs. Agent knowledge is typically derived from structured state files and conversation logs rather than human memory, so the uncertainty model is simpler.

When provenance matters (e.g., "why does the agent believe X about its infrastructure?"), use the standard `sources` frontmatter to trace knowledge back to its origin.

### Creating an Agent Pack

See [Composite Pack Schema — Auto-Discovery & Export](composite.md#auto-discovery--export) for the automated workflow where an AI agent introspects its own state and generates an agent pack (and composite) automatically.

Manual creation follows the same general flow as the base person schema's "Creating a New Person Pack" section, with these adjustments:
1. Initialize with `subtype: "agent"` in the manifest
2. Start with `operational/` and `mind/` (these are the agent's core identity, not `facts/`)
3. Populate `relationships/` with the primary user and key contacts
4. Build `presentation/` from observed communication patterns
5. Add `MIGRATION.md` with platform-specific hydration instructions

---

*Subtype version: 1.7 (person.md schema_version: 4.1)*
*Last updated: 2026-04-19*
