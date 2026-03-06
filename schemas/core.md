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

**Hierarchical retrieval:** Packs with `summaries/` and `propositions/` directories support multi-granular retrieval. Broad questions match section summaries first; factual questions match atomic propositions; detail questions match content files. This layered approach improves both precision and token efficiency. See type-specific schemas for implementation details.

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
| Conflict resolution | Never overwrite — flag and ask the human |
| Version control | Git-native, semantic versioning |

---

*Schema version: 1.4*
*Last updated: 2026-03-06*
