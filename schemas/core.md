# ExpertPack Core Schema

*Shared principles and conventions that apply to every ExpertPack, regardless of type. Type-specific schemas (person, product, process) extend these rules — they don't replace them.*

---

## The MD-Canonical Principle

This section includes updated guidance for how ExpertPacks are created and maintained: they are designed to be created and maintained by AI agents. Treat the schema as the agent's filing guide — the agent reads the schema to learn the pack structure and uses it to decide where content belongs. Humans (pack owners or domain experts) provide the knowledge; the agent handles structuring, parsing, and file management.

**Markdown is the canonical format for all knowledge content.** Every fact, story, concept, workflow, belief, or piece of expertise lives in a `.md` file. These files are the source of truth. They are human-readable, AI-consumable, git-versionable, and compatible with any RAG system. No proprietary formats, no databases, no lock-in.

**JSON is only for navigation and indexing.** Structured data files like `entities.json`, `_index.json`, and `_access.json` help agents *find* content — they are not content themselves. If a JSON file and a Markdown file disagree, the Markdown file wins.

**YAML is for pack identity.** Every pack has a `manifest.yaml` that declares what the pack is. This is metadata about the pack, not knowledge content.

**One source of truth per fact.** A piece of information should live in exactly one place. No mirrors, no regeneration steps, no dual JSON+MD for the same data. When something needs to be referenced from multiple locations, use markdown links to point to the canonical source.

### Exceptions

Some structured data is legitimately better as JSON — genealogy data derived from GEDCOM, complex entity cross-references, training data in JSONL format. These are acceptable when they serve a genuinely different purpose (programmatic access, visualization, machine learning) from the canonical Markdown. In such cases, the Markdown version is always the source of truth and the JSON is labeled as archival or supplementary.

---

## Required Files

Every pack must include these files at its root:

### manifest.yaml

The pack's identity card. Declares what the pack is, what it covers, and how to consume it.

```yaml
# Required fields
name: "Human-readable pack name"
slug: "kebab-case-identifier"
type: "person|product|process"
version: "1.0.0"
description: "What this pack contains and who it's for"
entry_point: "overview.md"

# Optional fields
subtype: "agent"   # Optional subtype that activates type-specific extensions
                   # Currently defined: "agent" (person type) — see person.md

# Recommended fields
author: "Who created this pack"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"

# Context strategy (recommended for packs with 15+ files)
# See "Context Strategy" section for full documentation
context:
  always: []      # Tier 1: loaded every session
  searchable: []  # Tier 2: indexed for RAG retrieval (default for unlisted files)
  on_demand: []   # Tier 3: loaded only on explicit request

# Type-specific fields are defined in each type schema
```

The `type` field determines which type-specific schema applies. See [person.md](person.md), [product.md](product.md), or [process.md](process.md).

### Subtypes

The optional `subtype` field activates extensions within a type-specific schema without creating a new top-level pack type. Subtypes inherit all of their parent type's structure, conventions, and rules — they add or reframe directories and fields for a specialized use case.

Currently defined subtypes:

| Type | Subtype | Schema Reference | Purpose |
|------|---------|-----------------|---------|
| person | `agent` | [person.md — Agent Extension](person.md#agent-extension-subtype-agent) | AI agent identity, operational config, and accumulated knowledge |

Subtypes are optional. A pack with no `subtype` field uses the base type schema as-is. When a `subtype` is declared, the agent should read the corresponding extension section in the type schema for additional directories, manifest fields, and behavioral guidance.

### overview.md

The first file any agent or human should read. Provides enough context to understand what the pack covers and how to navigate it. This is the entry point — load it first, always.

For product packs: what the product does, who it's for, key capabilities.
For person packs: who the person is, what's captured, why it exists.
For process packs: what the process achieves, when to use it, who it's for.

---

## Directory Conventions

### _index.md Files

Every content directory should have an `_index.md` file that serves as a table of contents. It lists and links to all files in that directory with brief descriptions.

Index files serve two purposes:
1. **Agent navigation** — an agent can read the index to discover what's available without loading every file
2. **Broad query matching** — RAG can match an index file against general queries like "what workflows are documented?"

**Example** `_index.md` for a product pack's concepts directory:

```markdown
# {Section Name}

{Brief description of what this directory contains.}

- [{Topic}]({topic}.md) — {One-line description}
- [{Topic}]({topic}.md) — {One-line description}
- [{Topic}]({topic}.md) — {One-line description}
```

### _access.json Files

Access control metadata at the directory level. Defines who can see content in that directory. Used primarily in person-type packs where privacy tiers matter, but available to any pack type.

```json
{
  "default_access": "public",
  "overrides": {
    "private-file.md": "self"
  }
}
```

Access tiers (from most to least open): `public`, `friends`, `family`, `self`.

Type-specific schemas may define additional access semantics — see [person.md](person.md) for the full access tier model including posthumous rules.

---

## File Structure Rules

### File Size: 1–3KB Per File

Keep individual content files small and focused. A file about "User Roles" should not also contain pricing information. One topic per file.

**Why this matters:** RAG chunkers split files into ~400-token windows. Large files produce poor search results — a 20KB file about "everything the product does" will match almost any query with mediocre relevance. Small, focused files produce high-relevance matches.

There are reasonable exceptions: reference documents (like this schema), index files, and narrative content (verbatim stories) may be longer. The guideline applies to knowledge content files that agents will retrieve via search.

### Section Headers for RAG Chunking

Every content file should use `##` section headers at natural topic breaks. Without headers, RAG chunkers produce arbitrary slices that split mid-thought. With headers, chunks align to semantic boundaries.

**Example** content file with proper section headers:

```markdown
# User Roles

## What It Is
Clear explanation of the concept.

## How It Works
Mechanics, rules, behavior.

## Example
Concrete illustration.
```

Each `##` section should be about one sub-topic and produce a coherent chunk on its own. This is cheap to implement and has outsized impact on retrieval quality.

### Naming Conventions

- **Files:** `kebab-case.md` — lowercase, hyphens between words
- **Directories:** `kebab-case/` — lowercase, hyphens between words
- **Pack slugs:** `kebab-case` — matches the directory name
- **No spaces, no underscores in filenames** (exception: legacy files that predate this convention)

---

## Retrieval Optimization

RAG retrieval quality depends on more than just file size. These patterns apply to every pack type and work together as a system — each layer compensates for what the others can't do alone.

### Summaries Directory (summaries/)

Recommended directory containing section-level summaries that enable hierarchical retrieval. Summaries give RAG a coarse-grained layer: broad questions match summaries first, then the agent drills into detail files. This follows the RAPTOR pattern — recursive summarization into a retrieval tree.

**Why summaries matter:** Without summaries, every query competes against hundreds of fine-grained content files. A question like "what can this product do?" matches dozens of files with mediocre relevance. A summary file matches with high relevance and provides a complete broad answer. Fine-grained files then handle follow-ups like "how does the optimizer work exactly?"

**Structure:** One summary file per content section. Each summary is 1–3KB of dense, fact-packed bullet points covering the key topics in that section, with cross-references to the detailed files.

```markdown
# {Section Name} — Summary

Dense bullet-point summary of all topics covered in this section.

## Key Topics
- **{Topic 1}** — {one-line summary}. See [{detail file}](../section/detail.md)
- **{Topic 2}** — {one-line summary}. See [{detail file}](../section/detail.md)
...
```

**Generation rules:**
- Summaries are DERIVED from content files — they are not canonical content
- Read all files in the section before writing the summary
- Include cross-references to source files so agents can drill down
- Regenerate summaries when source content changes significantly
- Keep each summary under 3KB — dense facts, not prose paragraphs

**Context tier:** Searchable (Tier 2). Summaries are indexed for RAG retrieval alongside content files.

**Person pack note:** Person packs use a special verbatim→summary mirroring pattern where each verbatim content file has a corresponding summary file with story card frontmatter. See [person.md](person.md) for the full two-tier content system.

---

### Lead Summaries

Recommended pattern: add a 1–3 sentence blockquote at the very top of high-traffic content files that directly answers the most likely query. Lead summaries ensure that even if RAG retrieves only the first chunk of a file, the agent gets the core answer immediately.

**Format:**

```markdown
# {Title}

> **Lead summary:** {Direct answer to the most common question this file addresses. Include key anti-hallucination facts and common gotchas. 1-3 sentences max.}

## What It Is
...
```

**Why this matters:** RAG chunkers typically split files from the top. If the first 400 tokens are a table of contents or general introduction, the most relevant chunk may rank lower than a chunk from a less-relevant file that happens to lead with the answer. Lead summaries front-load the critical facts into the highest-ranked chunk position.

**What to include in a lead summary:**
- The direct answer to the most common query about this topic
- Critical "NOT" facts (anti-hallucination) — things the system does NOT do
- Key prerequisites or gotchas that users commonly miss
- Vocabulary bridges — mention the common user language for technical terms

**When to add lead summaries:** Focus on files that appear in eval failures or that address high-traffic support topics. Not every file needs one — start with the ~15 most-retrieved files and expand based on eval results.

**Context tier:** Lead summaries are part of the content file itself — they inherit the file's tier (typically Tier 2, Searchable).

---

### Glossary (glossary.md)

Recommended file at the pack root that maps common user language to precise technical terms. A glossary bridges the vocabulary gap between how users describe problems and how the pack documents solutions.

**Why a glossary matters:** Users say "stuck ZIP codes" when the pack documents "locked territories." Users say "records missing" when the pack documents "silent truncation" or "upload record limit." Without a vocabulary bridge, RAG retrieval fails because the query terms don't match the content terms. A glossary file gives RAG an explicit mapping to match against.

**Structure:**

```markdown
# {Pack Name} — Glossary

Quick-reference definitions for {product/domain} terminology. Maps common user language to precise technical terms.

## {Category}

| Term | Definition | Common User Language |
|------|-----------|---------------------|
| **{Technical Term}** | {Precise definition} | "{how users say it}", "{alternate phrasing}" |
| **{Technical Term}** | {Precise definition} | "{how users say it}", "{alternate phrasing}" |
```

**Guidelines:**
- Group terms by category (e.g., "Territory Terms", "Data Terms", "Workflow Terms")
- Include the `Common User Language` column — this is what makes glossaries effective for RAG
- Keep definitions concise (1-2 sentences) with the key distinguishing fact
- Include anti-patterns in definitions where relevant (e.g., "NOT drag-and-drop")
- Update the glossary when eval failures reveal vocabulary gaps between user queries and pack content
- Add the glossary to the manifest's `always` context tier so it loads every session

**Context tier:** Always (Tier 1). The glossary is small, high-value, and helps with every query.

---

### Propositions Directory (propositions/)

Recommended directory containing atomic factual statements extracted from content files. Propositions enable high-precision retrieval: when a user asks a specific factual question, the RAG system can match an exact proposition rather than a paragraph that happens to contain the answer.

**Why propositions matter:** Prose paragraphs contain multiple facts mixed with explanations, examples, and transitions. RAG retrieval against prose returns the whole paragraph, only part of which is relevant. Propositions isolate individual facts into standalone retrieval units — each one matches precisely or not at all.

**Structure:** One proposition file per content section. Each file contains atomic facts grouped by source file, formatted as bullet lists.

```markdown
# {Section Name} — Propositions

### {source-filename.md}
- {Self-contained factual statement}
- {Self-contained factual statement}
- {Self-contained factual statement}

### {another-source-file.md}
- {Self-contained factual statement}
...
```

**Extraction rules:**
- Each proposition must be self-contained — readable without any surrounding context
- Each proposition captures exactly ONE fact (not compound statements)
- Propositions are DERIVED from content files — content files remain canonical
- Do NOT invent facts — extract only what the source file states
- Target 5–20 propositions per source file, depending on information density
- Regenerate propositions when source content changes

**Context tier:** Searchable (Tier 2). Propositions are indexed for RAG retrieval alongside content files and summaries.

**Quality control:** Hallucinated propositions are dangerous — they inject false facts into the retrieval layer. When generating propositions, verify each statement against the source file. When in doubt, omit rather than fabricate.

---

### File Splitting Rules

When a content file grows beyond the 1–3KB target, splitting it improves retrieval precision — but splitting alone is not enough.

**When to split:** When a content file exceeds ~10KB, split it into focused sub-files within a subdirectory. Each sub-file should cover one sub-topic and be independently useful without needing to load sibling files for context.

**IMPORTANT — Naive splitting loses context.** When you split a large file, you break the cross-topic connections that existed when everything was in one place. An agent that retrieves only one sub-file after splitting loses the surrounding context it previously had. Splitting without compensating for this degradation makes quality worse, not better.

**The fix — three layers together:**
1. **Split the file** into focused sub-files (precision)
2. **Generate a summary** for the section that covers all sub-files (broad context recovery)
3. **Extract propositions** from each sub-file (precise fact retrieval)

The three-layer approach (split files + summaries + propositions) consistently outperforms any single change alone. Don't split without also generating the retrieval layers.

---

### Optimization Anti-Patterns

Based on eval experiments, avoid these common mistakes:

**Do NOT compact or compress prose to save tokens.** Denser text is harder for models to parse correctly. Examples, explanations, and context that feel redundant to a human often serve as reasoning scaffolding for a model. The content quality was never the bottleneck — retrieval precision was.

**Do NOT split files without adding retrieval layers.** Splitting alone degrades quality. An agent that retrieves one fragment of what used to be a unified file loses the context that made that file useful. Always pair splitting with summaries and propositions.

**Do NOT sacrifice content readability for token efficiency.** Readable, well-structured prose with `##` headers and concrete examples outperforms tightly compressed bullet lists. Token count at retrieval time matters less than match quality and reasoning support.

---

### Eval-Driven Improvement

Retrieval quality is measurable — don't optimize blind.

**Build an eval set.** After building a pack, write 10–20 test questions covering the pack's key topics. Include questions that should be answered, questions that should be refused (out-of-scope), and questions requiring synthesis across multiple files.

**Track metrics.** For each eval question measure: correctness (did the agent answer accurately?), completeness (did it cover the full answer?), hallucination rate (did it invent facts not in the pack?), and refusal accuracy (did it correctly decline out-of-scope questions?).

**Use results to guide optimization.** A low completeness score on broad questions suggests missing summaries. High hallucination rate on specific facts suggests missing or poorly structured propositions. Incorrect answers on specific topics point to content gaps or ambiguous source files.

**Model capability matters.** The same pack can produce substantially different quality on different models. Run evals on your target model, not just the best available model. Optimizations that help a weaker model may be unnecessary for a stronger one — and vice versa.

---

## Source Provenance

Every content file should track where its information came from. This is especially important for packs built from multiple sources (documentation, videos, interviews, support tickets) where an agent may later need to verify, update, or trace content back to its origin.

### Frontmatter Convention

Add a `sources` block at the top of any content file derived from a specific external source:

```markdown
---
sources:
  - type: video
    title: "Product Overview Walkthrough"
    ref: "03:12-04:05"
  - type: documentation
    url: "https://docs.example.com/feature-x"
    date: "2026-01-15"
---
```

### Source Types

| Type | Fields | Use Case |
|------|--------|----------|
| `video` | `title`, `ref` (timestamp range), `file` (optional filename) | Video tutorials, recorded walkthroughs, demos |
| `documentation` | `url`, `date` (access/publish date) | Help sites, API docs, manuals |
| `interview` | `with` (person), `date`, `ref` (optional timestamp) | Expert walkthroughs, SME interviews |
| `support` | `ticket` (ID or URL), `date` | Support tickets, forum threads |
| `conversation` | `date`, `channel` (optional) | Chat-based knowledge capture |

**Rules:**
- Provenance is recommended for all content, required for content derived from video or interview sources
- Multiple sources per file are allowed (a workflow might combine documentation + video + interview)
- The `ref` field for video sources uses `MM:SS-MM:SS` or `HH:MM:SS-HH:MM:SS` format
- Provenance frontmatter is metadata, not content — it does not count against the 1–3KB file size guideline
- When a source is updated (new product version, revised documentation), provenance helps identify which pack files need review

---

## Research Coverage (sources/_coverage.md)

Every pack should include a **coverage map** that honestly documents what knowledge sources were checked during pack creation, what was extracted, and what remains untouched. This makes the pack's depth and limitations transparent to consumers and maintainers.

### Why Coverage Tracking Matters

A pack built from 5 web searches and the builder's existing knowledge looks the same as one built from 50 sources — unless coverage is documented. Without a coverage map:

- Consumers can't assess the pack's authority or completeness
- Maintainers don't know where to focus deepening efforts
- Gaps are invisible — the pack presents a confident facade over shallow research

### Coverage Map Structure

```markdown
# Research Coverage — {Pack Name}

Pack version: 1.0.0
Initial research: YYYY-MM-DD
Last deepened: YYYY-MM-DD
Estimated knowledge coverage: {low|medium|high} — {brief justification}

## Source Inventory

### Forums & Communities
| Source | Status | Value | Notes |
|--------|--------|-------|-------|
| r/{subreddit} (XXK members) | ✅ Mined | High | Top 50 threads by upvotes reviewed |
| {dedicated forum} | ⬜ Identified | Unknown | Not yet accessed |

### Video Content
| Source | Status | Value | Notes |
|--------|--------|-------|-------|
| {YouTube channel} (XXK subs) | 🟡 Sampled | High | 3 of ~40 relevant videos transcribed |

### Trade Publications
| Source | Status | Value | Notes |
|--------|--------|-------|-------|

### Manufacturer/Vendor Documentation
| Source | Status | Value | Notes |
|--------|--------|-------|-------|

### Regulatory & Standards Bodies
| Source | Status | Value | Notes |
|--------|--------|-------|-------|

### Books & Courses
| Source | Status | Value | Notes |
|--------|--------|-------|-------|

## Known Gaps
- {Specific knowledge area known to be thin or missing}
- {Source identified but not yet mined}

## Priority Sources for Next Pass
1. {Highest-value unmined source and what it would add}
2. {Next source}
```

### Status Key

| Status | Meaning |
|--------|---------|
| ✅ Mined | Source thoroughly reviewed and relevant knowledge extracted |
| 🟡 Sampled | Source partially reviewed — some content extracted, more available |
| ⬜ Identified | Source known to exist but not yet accessed |
| ❌ Checked, low value | Source reviewed but contained little unique knowledge |

### Rules

- **Every pack must have a coverage map.** Even a simple one with 5 entries is better than none — it's an honest statement of research depth.
- **Coverage maps are append-only for sources.** When deepening a pack, update status from ⬜ → 🟡 → ✅ but don't remove sources.
- **The "Estimated knowledge coverage" is a judgment call,** not a calculated metric. `low` = shallow research, known major gaps. `medium` = key sources covered but long tail untouched. `high` = comprehensive research across multiple source types.
- **Known Gaps should be specific.** "More research needed" is useless. "Installer forum threads about Enphase IQ8 firmware failure modes not yet mined" is actionable.

**Context tier:** Tier 3 (on-demand). Coverage maps are maintenance metadata, not consumed during normal use.

---

## Time Variance

Not all facts in a pack have the same shelf life. A string sizing formula is permanent; a panel's price per watt is stale within months. ExpertPacks must distinguish between durable knowledge and time-variant data — and handle each appropriately.

### The Principle: Store the Method, Not the Value

For any fact that changes faster than the pack's expected update cycle, store:

1. **What it is** — the concept or data point (e.g., "installed cost per kWh for home batteries")
2. **How to obtain the current value** — a URL, search query, API endpoint, or procedure
3. **A reference value with a date** — for ballpark/sanity-check purposes, clearly marked as a snapshot

### Time Variance Categories

| Category | Symbol | Meaning | Typical Decay | Examples |
|----------|--------|---------|---------------|---------|
| **Permanent** | ⚪ | Doesn't change | Never | Physics formulas, mathematical relationships, fundamental concepts |
| **Slow-moving** | 🟢 | Changes every 1-3 years | Annual review | Code editions, warranty terms, industry standards |
| **Fast-moving** | 🟡 | Changes every few months | Semi-annual review | Product rankings, model specs, new entrants |
| **Volatile** | 🔴 | Changes weeks-to-months | Quarterly review | Pricing, incentive amounts, availability, stock-like values |

### Inline Refresh Metadata

The critical rule: **refresh instructions must travel with the data, not live in a separate file.** When a consuming agent encounters a volatile fact, it needs the refresh method right there — not a pointer to a freshness guide it may not load.

Every time-variant data point in a content file should carry its own refresh metadata using a YAML-style annotation block:

```markdown
The Tesla Powerwall 3 is priced at approximately $10,500-14,000 installed.

<!-- refresh
  decay: volatile
  as_of: 2026-Q1
  source: https://www.energysage.com/solar/battery-storage/
  method: "Search 'Tesla Powerwall 3 installed cost [current year]' or request local installer quotes"
-->
```

**For tables with multiple volatile values**, place the refresh block after the table covering all volatile cells:

```markdown
| Feature | Tesla Powerwall 3 | Enphase IQ 5P |
|---------|-------------------|---------------|
| Capacity | 13.5 kWh | 5.0 kWh |
| Approx price | ~$10,500-14,000 | ~$6,000-8,000 |

<!-- refresh
  decay: fast-moving
  as_of: 2026-Q1
  fields: [capacity, price, power_output]
  source: https://www.energysage.com/solar/battery-storage/
  method: "Check manufacturer product pages and EnergySage for current specs and pricing"
-->
```

**Refresh block fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `decay` | Yes | `volatile`, `fast-moving`, `slow-moving`, or `permanent` |
| `as_of` | Yes | When this data was last verified (YYYY-QN or YYYY-MM-DD) |
| `source` | Yes | URL or description of where to get the current value |
| `method` | Recommended | Human/agent-readable instructions for refreshing (search query, steps, or API call) |
| `fields` | Optional | Which specific data points in the preceding content this covers (for tables with mixed permanence) |

**Why HTML comments?** They're invisible in rendered markdown but parseable by agents and tooling. They don't clutter the reading experience but are always present when the content is loaded into context.

### Freshness Guide (freshness.md)

A **supplementary** index at the pack root that provides a bird's-eye view of all time-variant data across the pack. This is NOT the primary refresh metadata — that lives inline with the data (above). The freshness guide is for:

- Pack maintainers reviewing overall freshness at a glance
- Automated tooling scanning for overdue refresh cycles
- Onboarding new contributors to the pack's maintenance needs

```markdown
# Freshness Guide — {Pack Name}

Last full review: YYYY-MM-DD

## {source-file.md}

| Data Point | Decay | Review Cycle | Last Verified |
|-----------|-------|-------------|---------------|
| Panel pricing per watt | 🔴 Volatile | Quarterly | 2026-Q1 |
| Top 10 rankings | 🟡 Fast-moving | Semi-annual | 2026-03 |
| NEC code section numbers | 🟢 Slow-moving | Annual | 2026-03 |
| String sizing formula | ⚪ Permanent | Never | N/A |
```

**Context tier:** Tier 2 (Searchable).

**Relationship to inline metadata:** The freshness guide is derived from the inline refresh blocks. If they disagree, the inline block is the source of truth (it's closer to the data). When refreshing the pack, update the inline blocks first, then regenerate or update the freshness guide.

### Design Guidance

- **Refresh metadata travels with the data.** This is the non-negotiable rule. A volatile fact without an inline refresh block is a bug — it will become wrong and nobody will know how to fix it.
- **Don't avoid time-variant facts** — packs that omit pricing, product names, and current specs to avoid staleness end up too abstract to be useful. Include them, but annotate them.
- **Include enough permanent context** that the pack remains valuable even when volatile data is stale. A good pack with stale pricing is still useful; a pack that's mostly stale pricing is not.
- **Prefer durable knowledge.** When choosing what to cover in depth, bias toward process, technique, decision frameworks, and concepts — knowledge that doesn't expire. Include volatile specs as supporting context, not as the pack's core value.
- **Agents consuming the pack** should parse refresh blocks before presenting volatile data as current. If `as_of` is more than one review cycle old, the agent should caveat the answer and offer to look up the current value using the provided `source` and `method`.

---

## Cross-Referencing

### Markdown Links

Files reference each other with relative Markdown links. This creates a navigable knowledge graph.

**Example** cross-references between a workflow and a concept:

```markdown
See [User Roles](../concepts/user-roles.md) for background on permissions.
Related workflow: [Invite a Team Member](../workflows/invite-team-member.md)
```

Links should be meaningful — don't link for the sake of linking, but do connect related content so an agent (or human) can follow the thread.

### JSON Navigation Indexes

For structured navigation beyond what `_index.md` provides, packs can include JSON index files. These are navigation aids, not content:

- **`entities.json`** (product packs) — Cross-reference of entities to the files that document them
- **`_index.json`** (any pack) — Structured metadata index for filtering and search (e.g., stories by theme, date, people)

JSON indexes answer the question "where should I look?" Markdown files answer "what do I need to know?"

---

## Context Strategy

Not every query needs the full pack. A 50-file pack loaded entirely into context burns tokens and dilutes relevance. ExpertPack uses a three-tier context strategy that balances depth with efficiency.

### The Three Tiers

| Tier | Name | Purpose | When Loaded |
|------|------|---------|-------------|
| **1** | **Always** | Core identity and voice — the minimum an agent needs to *be* this pack | Every conversation, automatically |
| **2** | **Searchable** | Knowledge content indexed for retrieval — loaded when relevant to the current topic | On topic match via RAG or agent navigation |
| **3** | **On-demand** | High-token or specialized content — loaded only when explicitly needed | Direct request, retelling, fine-tuning, deep dives |

### Tier Semantics

**Always (Tier 1)** — Files the agent must load at the start of every session. These establish identity: who/what the pack represents, how the agent should sound, and the essential facts needed to avoid obvious errors. Keep this tier small — ideally under 5KB total. If an always-loaded file exceeds 3KB, consider whether parts of it belong in Tier 2.

**Searchable (Tier 2)** — The bulk of the pack's knowledge. These files are indexed by RAG or listed in `_index.md` files for agent navigation. They load when the conversation touches a relevant topic. Most content files — summaries, concepts, workflows, mind taxonomy, relationships — live here. Design these files to be independently useful: an agent loading a single file should get a complete, actionable answer without needing to load five other files first.

**On-demand (Tier 3)** — Content that's valuable but expensive or situational. Full verbatim transcripts (high token cost), training data (machine consumption only), raw exports, or archival material. An agent should only load these when the task specifically requires them — retelling a story in someone's exact words, generating fine-tuning data, or doing deep research.

### Declaring Tiers in the Manifest

Each pack declares its context strategy in `manifest.yaml` using a `context` block. Files and directories are assigned to tiers by path:

```yaml
# Example: Context strategy for a person pack
context:
  always:
    - overview.md
    - facts/personal.md
    - presentation/speech_patterns.md
  searchable:
    - summaries/
    - relationships/
    - mind/
    - facts/
  on_demand:
    - verbatim/
    - training/
```

**Rules:**
- Paths are relative to the pack root
- Directory paths (trailing `/`) include all files in that directory and subdirectories
- A file can only belong to one tier — if a file matches multiple tiers, the most specific path wins (file path beats directory path)
- `manifest.yaml` and `overview.md` are implicitly Tier 1 even if not listed
- Files not matched by any tier default to **Searchable** (Tier 2)

### Defaults

If a pack omits the `context` block entirely, the following defaults apply:

| Tier | Default Contents |
|------|-----------------|
| **Always** | `manifest.yaml`, `overview.md` |
| **Searchable** | Everything else |
| **On-demand** | Nothing (all content is searchable) |

This is a safe default — no content is hidden from search, and identity files load automatically. Packs should declare explicit tiers once they grow beyond ~15 files, when token efficiency starts to matter.

### Design Guidance

- **Keep Tier 1 lean.** Every token in Tier 1 is spent on every conversation. A bloated always-load tier wastes budget on turns where the information isn't needed.
- **Summaries belong in Tier 2, verbatim in Tier 3.** This is the core efficiency pattern: search against distilled summaries, load full text only when voice fidelity matters.
- **`_index.md` files are Tier 2 by default.** They help agents discover what's available without loading every file.
- **Review tiers as the pack grows.** What starts as a 10-file pack with everything searchable may need tier refinement at 50 files.

---

## Content Changelog

Every pack should maintain a `meta/changelog.md` — an append-only log of what content was added, updated, or removed, when, and from what source. This is the pack's provenance record.

```markdown
## YYYY-MM-DD
- Added {N} verbatim stories (source: voice dictation): {file-list}
- Generated summaries for {file-list}
- Updated relationships/people.md: added {person}
- Source: {channel/method}
```

**Rules:**
- Append new entries at the top (most recent first)
- One entry per intake session or batch of related changes
- Include the source (voice dictation, website scrape, document import, conversation)
- Include file names or counts so the log is auditable against git history
- Agents should update the changelog as part of every content intake workflow

**Context tier:** `meta/changelog.md` defaults to Tier 3 (on-demand). It is not loaded during normal conversations — only when someone asks about content history, provenance, or what's been captured.

**Session continuity:** Agents maintaining a pack across multiple sessions should keep a persistent reference to the changelog in their session state or working memory. This ensures that even after session restarts, the agent can quickly determine what content exists, what's missing, and where intake left off — without reloading the entire pack. A one-line pointer is sufficient:

```
Pack status → {pack-path}/meta/changelog.md (content inventory at bottom)
```

---

## Conflict Resolution

**Never overwrite, always ask the human.**

When new information contradicts existing content:
1. **Check** the relevant file(s) for conflicts with the new input
2. **If conflict found:** Do NOT overwrite. Flag the contradiction and present both versions to the pack owner
3. **Log the conflict** so nothing is lost

This applies to all pack types. Memory is messy, documentation drifts, products change. Earlier information may be correct, or the new version may be a correction. Only the human can adjudicate.

Examples of contradictions to catch:
- Different dates or versions for the same event/release
- Conflicting descriptions of how a feature works
- Inconsistent facts, relationships, or process steps
- Information that doesn't align with previously established content

---

## Source of Truth Hierarchy

When multiple representations of the same information exist:

1. **Markdown content files** — always canonical
2. **YAML manifest** — canonical for pack identity metadata
3. **JSON navigation indexes** — derived from content, updated when content changes
4. **External sources** (websites, databases, APIs) — may be more current but are not part of the pack until incorporated into Markdown files

---

## Git & Version Control

ExpertPacks are designed to live in git repositories. This gives you:
- **Version history** — every change is tracked
- **Collaboration** — multiple contributors via branches and pull requests
- **Distribution** — clone, fork, or submodule a pack into any project
- **Diffing** — see exactly what changed between versions

### Commit Practices

- Commit when meaningful work is complete, not after every keystroke
- Use descriptive commit messages that explain *what changed and why*
- Tag releases with semantic versions matching `manifest.yaml`

---

## Versioning

ExpertPacks use three complementary versioning layers: schema versioning (for the pack type blueprint), pack versioning (for the pack instance), and content versioning (git commits).

### Schema Versioning

- Each type-specific schema file (e.g., `schemas/core.md`, `schemas/person.md`, `schemas/product.md`, `schemas/process.md`) carries a semantic schema version at the bottom of the file in the format `Schema version: MAJOR.MINOR` (for example `1.0`, `1.1`, `2.0`).
- A **MAJOR** schema bump indicates a breaking structural change: renamed directories, removed required files, or fundamental reorganization that may require pack migration.
- A **MINOR** schema bump indicates additive, backwards-compatible changes: new optional directories, clarified guidance, new templates, or additional recommendations. Packs targeting an older minor version remain conformant — the new features are optional.
- Every pack's `manifest.yaml` MUST include a `schema_version` field declaring which version of the type-specific schema it was built against. Example (add to the required fields section in `manifest.yaml`):

```yaml
schema_version: "1.0"  # Version of the type-specific schema this pack conforms to
```

- When a schema receives a MAJOR bump, pack authors and consumers should treat the change as requiring migration. When a schema receives a MINOR bump, packs on the previous minor version remain valid and can adopt new features at their discretion.

### Pack Versioning

Packs already include a `version` field in `manifest.yaml`. Follow semantic versioning practices for pack releases:
- **MAJOR**: Fundamental restructuring of content or directories, incompatible reorganizations
- **MINOR**: Significant new content sections or new directories that add capability without breaking consumers
- **PATCH**: Content updates, corrections, or additions that do not change the pack's structure

Bundle changes logically into commits and tag releases to mark pack versions.

### Content Versioning

Git is the content versioning system — every commit is a version of the pack's content. Follow clear commit message conventions to make history machine-readable and human-friendly:
- Content additions: `Add {type}: {description}` (e.g., `Add story: childhood fishing trip`)
- Content updates: `Update {file}: {what changed}` (e.g., `Update career.md: add 2025 role change`)
- Structure changes: `Refactor {what}: {why}` (e.g., `Refactor mind/: add tensions category`)
- Schema changes: `Schema {version}: {what changed}` (e.g., `Schema 1.1: add mind taxonomy`)

---

## Agent Consumption Patterns

These patterns describe how an AI agent should work with any ExpertPack:

### Discovery (Tier 1 — Always)
1. Read `manifest.yaml` — understand what the pack covers, its type, and its context strategy
2. Read `overview.md` and any other Tier 1 files — establish identity and voice
3. This gives enough awareness to route queries and respond in character

### Retrieval (Tier 2 — Searchable)
For a specific question, the agent either:
- **Navigates:** Reads `_index.md` for the relevant section, picks the right file
- **Searches:** Uses RAG/vector search to find relevant chunks across all Tier 2 files
- **Both:** RAG finds candidates, agent reads the full file for complete context

**Hierarchical retrieval:** Packs with `summaries/` and `propositions/` directories support multi-granular retrieval. Broad questions match section summaries first; factual questions match atomic propositions; detail questions match content files. This layered approach improves both precision and token efficiency. See the [Retrieval Optimization](#retrieval-optimization) section above for implementation details and anti-patterns.

### Deep Loading (Tier 3 — On-demand)
When the task requires full source material:
- Retelling a story in the person's exact words → load verbatim
- Generating training data → load training files
- Comprehensive audit or migration → load everything

### Update
When adding or changing content:
1. Identify the canonical file for the information
2. Check for contradictions (see Conflict Resolution above)
3. Make the edit in the Markdown file
4. Update any affected JSON indexes
5. Commit with a descriptive message

---

## Shared Principles Summary

These principles apply to every ExpertPack, regardless of type:

| Principle | Rule |
|-----------|------|
| Canonical format | Markdown for content, YAML for identity, JSON for navigation only |
| One source of truth | Each fact lives in exactly one place |
| File size | 1–3KB per content file, one topic per file |
| Section headers | `##` headers at natural topic breaks for RAG chunking |
| Naming | kebab-case for files, directories, and slugs |
| Cross-references | Relative markdown links between related files |
| Directory indexes | `_index.md` in every content directory |
| Context strategy | Three tiers: always → searchable → on-demand, declared in manifest |
| Retrieval optimization | Summaries (broad), propositions (precise), file splitting, lead summaries (front-loaded answers), and glossary (vocabulary bridging) — use together; see [Retrieval Optimization](#retrieval-optimization) |
| Research coverage | Every pack includes `sources/_coverage.md` documenting what was checked, what was extracted, and what's untouched; see [Research Coverage](#research-coverage-sources_coveragemd) |
| Time variance | Annotate time-variant facts inline with `<!-- refresh -->` blocks; maintain `freshness.md` as supplementary index; see [Time Variance](#time-variance) |
| Conflict resolution | Never overwrite — flag and ask the human |
| Version control | Git-native, semantic versioning |

---

*Schema version: 2.0*
*Last updated: 2026-03-10*
