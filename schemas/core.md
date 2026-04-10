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

# Freshness tracking (recommended — see Provenance Metadata section)
freshness:
  refresh_cycle: "P90D"          # ISO 8601 duration — expected review cadence
  last_full_review: "YYYY-MM-DD"
  verified_file_count: 0         # How many content files have verified_at set
  total_file_count: 0            # Total content files in pack
  coverage_pct: 0                # Computed: verified_file_count / total_file_count * 100

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

## Scaffolding a New Pack

When creating a new ExpertPack from scratch, follow this sequence:

1. **Create the root directory** — use the pack slug as the folder name (kebab-case)
2. **Copy the `.obsidian/` config folder** into the pack root — from the ExpertPack repo root or the `template/` folder. This makes the pack an immediately usable Obsidian vault.
   ```
   cp -r /path/to/ExpertPack/.obsidian ./your-pack-slug/.obsidian
   ```
   Or use the full template as your starting point:
   ```
   cp -r /path/to/ExpertPack/template ./your-pack-slug
   ```
3. **Create `manifest.yaml`** — fill in all required fields (name, slug, type, version, description, entry_point)
4. **Create `overview.md`** — the entry point every agent reads first
5. **Scaffold content directories** per the type schema — `concepts/`, `workflows/`, `troubleshooting/`, `faq/`, etc. Each directory gets an `_index.md`
6. **Create `glossary.md`** — add terms as hydration proceeds
7. **Create `sources/_coverage.md`** — track what sources have been researched
8. **Begin hydration** — populate content files using EK-aware triage (esoteric knowledge first)
9. **Add retrieval layers** as content grows — `summaries/`, `propositions/`, lead summaries in content files
10. **Measure EK ratio** — run blind-probe eval once the pack has substantive content

**The `.obsidian/` folder is not optional.** Every pack should include it so the pack is immediately openable in Obsidian without any manual setup. It contains pre-configured Dataview and Templater settings that make authoring and reviewing the pack significantly easier.

---

## Directory Conventions

### _index.md Files

Every content directory should have an `_index.md` file. Its role is **orientation only**: it lists what's available and helps agents and humans navigate. It is not a content hub and should not be the center of the graph view.

**What `_index.md` does:**
1. **Agent navigation** — an agent reads the index to discover what's available without loading every file
2. **Broad query matching** — RAG matches an index file against general queries like "what workflows are documented?"

**What `_index.md` does NOT do:**
- It is not the structural center of a section. Its outbound links point down to children, not across to siblings or other sections.
- Cross-section relationships belong on the content files themselves (via `related:` frontmatter or inline links), not on the index.

**Graph view:** The `.obsidian/graph.json` config excludes `_index.md` files from the graph by default (`-_index` filter). This keeps the graph view clean — showing actual concept relationships rather than every node clustering around its index hub. If you want to see index nodes, remove or clear the search filter in Graph View settings.

**Example** `_index.md` for a product pack's concepts directory:

```markdown
---
title: "Concepts"
type: index
tags: [concepts]
pack: "pack-slug"
retrieval_strategy: standard
---

# Concepts

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

### File Size: Retrieval-Ready by Design

Every content file in an ExpertPack should be a self-contained retrieval unit — sized and structured so that any RAG chunker passes it through intact, without splitting.

**Target: 400–800 tokens per file (roughly 1,600–3,200 characters).**

This range ensures files pass through any reasonable chunker's token budget (typically 400–2,500 tokens) as single units. A file within this range is:
- Small enough to never trigger a dumb line-based splitter
- Large enough to carry a complete thought with sufficient context
- Sized to maximize retrieval precision — one file = one topic = one chunk

**Why this matters:** RAG chunkers that split files by character/token count destroy structure — they slice lead summaries from titles, split proposition groups from headers, and orphan metadata from content. By keeping files within the target range, the schema itself prevents this. No external chunking tool is needed.

**Hard ceiling: 1,500 tokens (~6,000 characters) for standard content files.** Files above this will be split by most chunkers and should be broken into focused sub-files. The only exception is files with `retrieval.strategy: atomic` in their frontmatter (workflows, troubleshooting procedures — see Chunking Strategy below).

**When a topic needs more space:**
1. Split into numbered parts with cross-references: `territories-overview.md`, `territories-assignment.md`, `territories-balancing.md`
2. Each part should be independently useful — an agent loading one part gets a complete answer for that sub-topic
3. Add an `_index.md` entry linking the parts together

There are reasonable exceptions: workflow files that must be atomic (see Chunking Strategy), schema/reference documents like this one, and narrative content where splitting would destroy coherence. These exceptions should use `retrieval.strategy: atomic` frontmatter to signal that splitting is not allowed.

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

### Filename Uniqueness (Required)

Every content file in a pack **must have a unique basename** across the entire vault. Duplicate basenames break Obsidian wikilink resolution — the graph draws edges to the wrong file or picks arbitrarily between matches.

**Enforcement: directory prefix convention.** Each directory type is assigned a short prefix. All content files in that directory are named `{prefix}-{slug}.md`. This makes filenames self-describing and collision-free by construction.

Standard prefixes for person packs:

| Directory | Prefix | Example |
|---|---|---|
| `summaries/stories/` | `sum-` | `sum-nina-street.md` |
| `summaries/reflections/` | `sum-` | `sum-ai-personhood.md` |
| `summaries/opinions/` | `sum-` | `sum-on-ai.md` |
| `verbatim/stories/` | `vbt-` | `vbt-nina-street.md` |
| `verbatim/reflections/` | `vbt-` | `vbt-ai-personhood.md` |
| `verbatim/opinions/` | `vbt-` | `vbt-on-ai.md` |
| `mind/` | `mind-` | `mind-epistemology.md` |
| `facts/` | `facts-` | `facts-timeline.md` |
| `meta/` | `meta-` | `meta-changelog.md` |
| `propositions/` | `prop-` | `prop-facts.md` |
| `relationships/` | `rel-` | `rel-people.md` |
| `presentation/` | `pres-` | `pres-modes.md` |

For other pack types (product, process, etc.), define prefixes in the pack's `manifest.yaml` under `file_prefixes`. Choose short (3–5 char) abbreviations that reflect content type.

**Exceptions:** Root-level structural files (`README.md`, `SCHEMA.md`, `STATUS.md`, `glossary.md`, `overview.md`) and `_index.md` directory indexes are exempt — they are already unique by convention.

The EP CLI validator (when available) will enforce this rule and flag any duplicate basenames at pack validation time.

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

### Chunking Strategy

ExpertPack files are designed to be **retrieval-ready by default**. When authored to the file-size guidelines above (400–800 tokens, hard ceiling 1,500 tokens for standard content), each file passes through any RAG platform's chunker as a single unit — no external preprocessing needed. The schema IS the chunking strategy.

This eliminates the need for a schema-aware chunking tool in the standard workflow. The intelligence that was previously in a post-processing tool now lives in the authoring rules: every file is a self-contained retrieval unit by design.

#### Why This Works

RAG chunkers split files when they exceed a token/character budget. If every file is under the budget, the chunker has nothing to split. The result:
- Lead summaries stay with their titles
- Proposition groups stay intact
- Glossary tables stay together
- `<!-- refresh -->` metadata stays with its content
- No lost context, no orphaned fragments

This was validated empirically: pre-sized files (~222 tokens average) pass through intact at any chunker budget from 400 to 2,500+ tokens. The schema-aware chunker we previously recommended showed a +9.4% correctness improvement — but its entire value came from preventing dumb splits of oversized files. When files are correctly sized at authoring time, there's nothing left for a chunking tool to fix.

#### Atomic vs. Sectioned Content

Not all content should follow the standard file-size guidelines. Procedural content that depends on sequential context must be retrieved as a complete unit, even if it exceeds the normal size ceiling.

| Strategy | Behavior | Default For |
|----------|----------|-------------|
| **standard** | Author within 400–800 token target. Chunker passes through whole. | All content files (default) |
| **atomic** | May exceed size ceiling. Must be retrieved whole. Declare in frontmatter. | `workflows/`, `troubleshooting/errors/`, `troubleshooting/diagnostics/`, `troubleshooting/common-mistakes/`, `volatile/` |

**Why workflows are atomic:** Workflows are step-by-step procedures where each step depends on the previous. Retrieving step 5 of 10 without the surrounding steps produces hallucinated instructions — the model fills gaps with fabricated UI paths and invented interactions. Workflow files must be retrieved as complete units or not at all.

**Why troubleshooting is atomic:** Error resolution files (symptom → cause → fix) and diagnostic decision trees lose their logical flow when split. An agent that retrieves only the "fix" without the "symptom" and "cause" gives dangerously decontextualized advice.

#### Per-File Override

Any content file can declare its retrieval strategy via YAML frontmatter:

```yaml
---
retrieval:
  strategy: atomic
---
```

Use this when a file's retrieval needs differ from the standard — e.g., a concept file containing a critical decision framework that must not be fragmented.

#### Sequence Metadata

When a topic spans multiple files (because splitting was needed to stay within size guidelines), include cross-references so consuming agents can find related parts:

```markdown
<!-- sequence: concepts--territories--*.md | part: 2 of 3 -->
```

The `part X of Y` tells the agent this is one piece of a larger topic. The `sequence` glob tells it where to find siblings. An agent receiving a sequence-tagged file should consider loading siblings before synthesizing a complete answer.

#### Pack–Consumer Coordination Contract

The pack author and the consuming agent configuration form a two-party contract:

- **Pack author commits:** "No standard content file exceeds 1,500 tokens (the hard ceiling). Atomic files (workflows, troubleshooting) may be larger but must be retrieved whole."
- **Consumer configures:** Set `chunking.tokens` (or equivalent) to **≥ the pack's hard ceiling** — 1,000 is the recommended minimum for well-authored packs — so no file is ever split.

The invariant is: **`chunking.tokens` > pack's hard ceiling for non-atomic files.** As long as this holds, every file passes through the chunker intact. If a pack deviates from the size target (e.g., during early hydration or with legacy content), the consumer config needs a proportional adjustment.

This is a convention, not an enforced spec. Both sides need to uphold it. If you're consuming a pack you didn't author, verify the file sizes before assuming the default 1,000-token budget is sufficient.

#### Platform Configuration

The pack's file-size constraints interact with three RAG platform knobs. Configure them as a system:

**1. Indexing granularity (`chunking.tokens` or equivalent)**
Set this high enough that pack files pass through whole. For packs authored to spec (400–800 token files), a budget of 800–1,000 tokens ensures no file gets split. Higher budgets (1,500–2,500) are safe but provide no additional benefit for well-sized packs.

**2. Retrieval count (`maxResults` or `top_k`)**
Packs with many small, focused files benefit from retrieving more chunks. Where a pack with 10 large files might need `maxResults: 5`, a well-chunked pack with 100+ small files should use `maxResults: 8–15` to capture enough relevant context.

**3. System prompt overhead**
Every token in your system prompt (SOUL.md, workspace files, platform overhead) competes with retrieved pack content for context window space. In our experiments, static context consumed 72% of every query's input tokens — dwarfing the retrieved pack content. **Minimize your system prompt. Treat it like a Tier 1 file — every token must earn its place.**

**OpenClaw example configuration:**

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "extraPaths": ["path/to/pack"],
        "chunking": { "tokens": 1000, "overlap": 0 },
        "query": {
          "maxResults": 10,
          "hybrid": {
            "enabled": true,
            "mmr": { "enabled": true, "lambda": 0.7 },
            "temporalDecay": { "enabled": false }
          }
        }
      }
    }
  }
}
```

- **tokens: 1000** — comfortably above the 800-token file ceiling; no file gets split
- **overlap: 0** — files are self-contained; overlap would duplicate content
- **maxResults: 10** — more slots for small, precise files (adjust based on pack size)
- **MMR enabled (λ=0.7)** — prevents near-duplicate proposition/summary/content files from crowding results
- **Temporal decay off** — pack knowledge doesn't expire by file modification time

#### Legacy Packs

Packs authored before these file-size guidelines may contain oversized files. Refactor oversized files into focused sub-files following the guidelines above. This is a one-time investment that makes the pack permanently retrieval-ready.

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

## Esoteric Knowledge (EK) Ratio

An ExpertPack's value is directly proportional to the knowledge it contains that frontier LLMs *cannot* produce on their own. This is the **Esoteric Knowledge (EK) ratio** — a first-class quality metric that should be measured and optimized throughout the pack lifecycle.

See [AXIOMS.md](../AXIOMS.md) for the foundational definitions: EK is knowledge that exists only outside the weights of frontier-lab LLMs (Axiom 1), and EPs maximize the ratio of EK to general knowledge (Axiom 3).

### Why EK Ratio Matters

A pack full of content the model already knows is dead weight — it burns tokens without adding value. A pack with high EK density gives the model capabilities it genuinely cannot achieve alone. The distinction between a pack that's "nice to have" and one that's "essential" is almost entirely determined by its EK ratio.

### Terminology

| Term | Definition |
|------|-----------|
| **Esoteric Knowledge (EK)** | Knowledge a frontier LLM cannot correctly produce without the pack |
| **General Knowledge (GK)** | Knowledge a frontier LLM can already produce correctly |
| **EK Ratio** | Proportion of a pack's propositions classified as EK: `(EK + 0.5 × Partial) / Total` |
| **Blind probe** | Asking a model a question derived from a pack proposition *without* the pack loaded |

### Measuring EK Ratio

EK ratio is measured empirically using **proposition-level blind probing:**

1. **Extract propositions** — use the pack's `propositions/` files (one atomic fact per line). If propositions don't exist yet, generate them.

2. **Generate probe questions** — convert each proposition into a natural question. *"The TSP optimizer uses a genetic algorithm with population size 32"* → *"What algorithm does EZT Designer use for route optimization, and what is the default population size?"*

3. **Blind query** — ask 2–3 frontier models (e.g., GPT-5, Claude Opus, Gemini) the question with NO pack context. Just the question.

4. **Score against ground truth** — compare each model's answer to the proposition:

   | Result | Classification | Weight |
   |--------|---------------|--------|
   | Correct and confident | General Knowledge (GK) | 0.0 |
   | Partially correct or vague | Partial | 0.5 |
   | Wrong, hallucinated, or refused | Esoteric Knowledge (EK) | 1.0 |

5. **Use the union rule** — if *any* tested model answers correctly, the proposition is GK. EK means *no* frontier model gets it right.

6. **Calculate:** `EK ratio = (EK_count + 0.5 × Partial_count) / Total_propositions`

### Interpreting EK Ratio

| EK Ratio | Interpretation | Action |
|----------|---------------|--------|
| **0.80+** | Exceptional — almost entirely esoteric | Ideal. Promote this metric prominently. |
| **0.60–0.79** | Strong — majority esoteric content | Good. Look for GK that can be trimmed. |
| **0.40–0.59** | Mixed — significant general knowledge padding | Review low-EK sections. Trim or compress GK. |
| **0.20–0.39** | Weak — most content is already in the model | Major rework needed. Refocus on tribal/undocumented knowledge. |
| **< 0.20** | Minimal value-add | Consider whether the pack's subject matter has enough EK to justify a pack at all. |

### EK Ratio in the Manifest

Packs that have been measured should declare their EK ratio in the manifest:

```yaml
ek_ratio:
  value: 0.72
  measured: "2026-03-12"
  models: ["gpt-5", "claude-opus-4", "gemini-2"]
  propositions_tested: 142
```

This metadata enables marketplaces, consumers, and tooling to assess pack value at a glance.

### EK Ratio Over Time

EK ratio naturally **decreases** as models absorb more of the world's knowledge into their weights. What's esoteric today may become general knowledge in the next training run. This means:

- **Measure periodically** — re-probe quarterly or after major model releases.
- **Packs need deepening, not just maintenance.** As GK absorbs the surface layer, the pack's value increasingly depends on its deepest, most tribal content.
- **Version your measurements** — track EK ratio over time in `meta/` to observe decay trends.

### EK-Aware Hydration

EK ratio is not just a post-hoc measurement — it should guide hydration decisions during pack creation. See the [Hydration Guide](../guides/hydration.md) for the EK Triage process and the Hydration Priority Matrix.

**The principle:** During hydration, every piece of content should pass through an EK filter before receiving full treatment. Content the model already knows gets minimal filing (brief glossary entry or one-line mention). Content the model cannot produce gets maximum effort (full extraction, careful structuring, proposition generation, lead summaries).

**Pack-type considerations:** EK triage intensity varies by content type:
- **Person packs** are almost entirely EK by nature — private stories, beliefs, voice patterns, and relationships exist nowhere in model weights. Skip blind probing for `verbatim/`, `mind/`, `presentation/`, and `relationships/` content. Probe only `facts/` (biographical data that may be publicly known for public figures) and background context added for scaffolding.
- **Product packs** have the highest GK contamination risk — documentation, architecture overviews, and technology primers are often well-represented in training data. Probe all documentation-sourced content. Skip probing for expert walkthroughs and code-analysis findings.
- **Process packs** fall between: official SOPs and standard methodology may be in training data, but practitioner experience, failure modes, timing realities, and regional variations are esoteric. Probe `fundamentals/` and formal process descriptions; skip `gotchas/`, `exceptions/`, and practitioner-contributed content.

### Common-Knowledge Compaction Rule

When general knowledge *must* be present for completeness (e.g., a glossary term for a well-known technology, a basic concept needed as context for esoteric content), apply **maximum compaction:**

- One sentence for the definition, maximum
- Link to the esoteric content that depends on it
- Do NOT write multi-paragraph explanations of things the model already knows

Example — **Good:** `**Zigbee** — Low-power mesh protocol (2.4 GHz, 65K nodes). See [protocols.md](concepts/protocols.md) for HA-specific coordinator firmware quirks and pairing gotchas.`

Example — **Bad:** Three paragraphs explaining what Zigbee is, its history, how mesh networking works, and a comparison with Wi-Fi — all of which the model can produce perfectly without the pack.

---

## Provenance Metadata

ExpertPack files support two complementary provenance layers: **content provenance** (where knowledge came from) and **freshness provenance** (when it was last verified and whether it has changed). Together they enable citation-quality retrieval — agents can return not just content but auditable references.

### File-Level Provenance Frontmatter

Every content file should include provenance fields alongside standard frontmatter:

```yaml
---
title: "Feature X — Concept"
type: concept
tags: [concept, feature-x]
pack: "my-pack"
retrieval_strategy: standard

# Stable citation ID — never changes even if file is renamed/moved
id: "my-pack/concepts/feature-x"

# Freshness provenance
content_hash: "sha256:a3f1c..."   # SHA-256 of file body (below closing ---)
verified_at: "2026-04-10"         # When content was last confirmed accurate
verified_by: "agent"              # "agent" or "human"
---
```

#### `id` — Stable Citation Key

A stable, cross-version identifier for the file. Format: `{pack-slug}/{relative-path-without-extension}`. Assigned at creation and **never changed**, even if the file is renamed or reorganized. This is the retrieval citation key — external references to this file use `id`, not the file path.

- For new packs: generate at file creation time
- For existing packs: backfill by deriving from current path; document the derivation date in `meta/`
- `id` values must be unique within a pack

#### `content_hash` — Drift Detection

SHA-256 hash of the file body (everything below the closing `---` of the frontmatter block). Enables consumers to detect whether a cited file has changed since the citation was made — without re-reading the content.

- Compute and write at authoring/update time
- Recompute whenever file body changes
- A mismatch between stored hash and actual hash is a `W-PROV-02` validator warning

#### `verified_at` — Freshness Signal

ISO date when the content was last confirmed accurate. This is NOT the same as the git commit date — a file can be committed without being reviewed. Agents should caveat answers from files where `verified_at` is older than the pack's `manifest.yaml freshness.refresh_cycle`.

- `verified_by: "human"` — an SME or pack owner reviewed the content
- `verified_by: "agent"` — an agent performed a structured review pass

**Consumer behavior:** At session start, check `manifest.yaml freshness.coverage_pct`. If below 70%, the consuming agent should note that provenance coverage is incomplete and caveat time-sensitive answers accordingly.

### Citation Response Contract

When an agent retrieves content from an ExpertPack, the retrieval response SHOULD include:

```
file        — relative path to source file
id          — stable frontmatter id (if present)
content_hash — from frontmatter (if present)
verified_at  — from frontmatter (if present)
excerpt     — the specific passage retrieved
```

This gives downstream consumers everything needed to build auditable, citable answers — without requiring the agent to re-read files.

### Pack-Level Freshness (manifest.yaml)

Maintain a `freshness` block in `manifest.yaml` (see manifest spec above). Update `verified_file_count`, `total_file_count`, and `coverage_pct` after each review pass. This is a manually maintained summary — it gives consuming agents a single-glance freshness signal without scanning every file.

### Validator Warnings for Provenance

| Code | Condition | Severity |
|------|-----------|----------|
| `W-PROV-01` | Content file missing `verified_at` | Warning |
| `W-PROV-02` | `content_hash` present but doesn't match actual file hash | Warning |
| `W-PROV-03` | `verified_at` older than `manifest.yaml freshness.refresh_cycle` | Warning |
| `W-PROV-04` | Content file missing `id` field | Info |

Provenance warnings do not break the zero-error requirement — they are surfaced separately as quality indicators.

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

### Volatile Files & Frontmatter TTL

The inline `<!-- refresh -->` block handles *individual volatile facts within otherwise-static files*. For content that is **entirely time-bound** — a current pricing page, a live leaderboard snapshot, a current API rate-limit table — use a dedicated **`volatile/` directory** with file-level frontmatter TTL instead.

**Why the distinction matters:** Inline refresh blocks are author-declared hints. Frontmatter TTL is machine-readable and enables automatic staleness detection without parsing markdown content. A consuming agent can check all of `volatile/*.md` in one pass at session start.

**File-level frontmatter:**

```yaml
---
volatile:
  refresh: P30D          # ISO 8601 duration — how often this should be refreshed
  source: https://example.com/pricing   # URL or named refresh procedure
  fetched_at: "2026-04-01"              # when this version was captured
  expires_at: "2026-05-01"              # computed: fetched_at + refresh; agent checks this
---

# Current Pricing

...
```

**`volatile/` directory rules:**
- Lives at the pack root alongside `concepts/`, `workflows/`, etc.
- Files in `volatile/` are always Tier 2 (Searchable) — never Tier 1 (always-loaded)
- Static and volatile content never coexist in the same file — if a file is partly static and partly volatile, split it
- Chunking default for `volatile/` is `atomic` — volatile files are retrieved whole
- Volatile files are **excluded from EK ratio measurement** (see EK Ratio section below); declare `volatile_excluded: true` in the manifest's `ek_ratio` block

**Staleness detection (agent behavior):**
At session start (or first pack query), the agent checks frontmatter `expires_at` across all `volatile/*.md`:
- If `expires_at >= today`: serve content as-is
- If `expires_at < today` and `source` is a URL: auto-refresh using the provided URL and `method`; update `fetched_at` and `expires_at`
- If `expires_at < today` and `source` requires human input: caveat the content and alert the user that it needs refreshing

This is passive, not a cron job — staleness is detected on demand, not on a schedule.

**EK ratio manifest addition:**
```yaml
ek_ratio:
  value: 0.78
  measured_at: "2026-04-01"
  sample_size: 240
  models: ["gpt-5", "claude-opus-4"]
  volatile_excluded: true   # volatile/ files were excluded from this measurement
```

**Relationship to inline refresh blocks:** Both mechanisms coexist.
- Use `<!-- refresh -->` inline blocks for volatile *facts* embedded in otherwise-static files (the existing pattern).
- Use `volatile/` + frontmatter TTL for *entire files* that are time-bound and should be machine-checkable.

When in doubt: if more than ~50% of a file's facts are volatile, move the whole file to `volatile/` with frontmatter TTL. If only a few data points are time-sensitive, keep the file in its normal location and use inline refresh blocks.

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

### Entity Relation Graph (relations.yaml)

Optional file at the pack root (or composite root) that declares typed, directional relationships between named entities across the pack. While markdown links connect *files*, a relation graph connects *concepts* — enabling agents to traverse knowledge by meaning rather than file structure.

**When to use:** Packs with 20+ entities that reference each other across multiple files. Product packs with complex entity models (e.g., "Territory contains Accounts, Account has assigned Rep, Rep belongs to Team"). Composite packs where entities span constituent packs. Person packs with rich relationship networks.

**When to skip:** Small packs where markdown links and `_index.md` provide sufficient navigation. If an agent can find everything via RAG search, a relation graph adds overhead without value.

**Format:**

```yaml
# relations.yaml — Entity Relation Graph
# Typed, directional relationships between named entities.

entities:
  - id: territory
    type: concept
    label: "Territory"
    file: concepts/territories.md

  - id: account
    type: concept
    label: "Account"
    file: concepts/accounts.md

  - id: rep
    type: concept
    label: "Sales Rep"
    file: concepts/reps.md

  - id: optimizer
    type: workflow
    label: "Route Optimizer"
    file: workflows/route-optimization.md

relations:
  - from: territory
    rel: contains
    to: account
    properties:
      cardinality: one_to_many

  - from: account
    rel: assigned_to
    to: rep
    properties:
      cardinality: many_to_one

  - from: optimizer
    rel: operates_on
    to: territory
```

**Entity fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique kebab-case identifier within the pack |
| `type` | Yes | Entity category: `concept`, `workflow`, `interface`, `person`, `tool`, `phase`, `decision` |
| `label` | Yes | Human-readable display name |
| `file` | Recommended | Relative path to the canonical content file for this entity |
| `pack` | Composites only | Slug of the constituent pack this entity belongs to |

**Relation fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `from` | Yes | Source entity id |
| `rel` | Yes | Relationship type (verb phrase, snake_case) |
| `to` | Yes | Target entity id |
| `properties` | No | Optional metadata: `cardinality` (one_to_one, one_to_many, many_to_one, many_to_many), `bidirectional` (bool), `conditional` (string describing when the relation applies) |

**Common relation types:**

| Relation | Typical Usage |
|----------|--------------|
| `contains` | Parent-child hierarchy (Territory contains Accounts) |
| `assigned_to` | Ownership or responsibility (Account assigned to Rep) |
| `depends_on` | Prerequisite or dependency (Phase 3 depends on Phase 2) |
| `operates_on` | Tool/workflow acts on an entity (Optimizer operates on Territory) |
| `extends` | Specialization (AgentPack extends PersonPack) |
| `configured_by` | Settings relationship (Feature configured by Config File) |
| `resolves` | Troubleshooting (Workaround resolves Error) |
| `part_of` | Composition (Chapter part of Process) |

**Rules:**
- `relations.yaml` is a navigation aid, not content — the same rule as JSON indexes. If it disagrees with a Markdown file, the Markdown file wins.
- Entity ids must be unique within the file. In composites, prefix with pack slug to avoid collisions (e.g., `product-a.territory`), or use the `pack` field.
- Keep the graph focused on high-value relationships an agent would actually traverse. A 200-relation graph is noise. Aim for the 15–30 relationships that matter most for navigation and reasoning.
- The graph is optional and additive. Packs without `relations.yaml` work exactly as before — markdown links and `_index.md` handle navigation.

**Agent consumption patterns:**
- **"What depends on X?"** → traverse `depends_on` relations from entity X
- **"What does the Optimizer touch?"** → follow `operates_on` from optimizer entity
- **"Show me everything about Territories"** → find territory entity, follow all outbound relations, load referenced files
- **Cross-pack reasoning** (composites) → "How does the founder's sales philosophy connect to the CRM product?" → traverse relations across pack boundaries

**Context tier:** Tier 2 (Searchable). The relation graph is small and useful for navigation but doesn't need to load every session. Agents query it when they need to traverse entity relationships.

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
| File size | 400–800 tokens per file; 1,500 token ceiling; retrieval-ready by design |
| Section headers | `##` headers at natural topic breaks for RAG chunking |
| Naming | kebab-case for files, directories, and slugs |
| Cross-references | Relative markdown links between related files |
| Entity relations | Optional `relations.yaml` for typed entity graphs; navigation aid, not content |
| Directory indexes | `_index.md` in every content directory |
| Context strategy | Three tiers: always → searchable → on-demand, declared in manifest |
| Retrieval optimization | Summaries (broad), propositions (precise), file splitting, lead summaries (front-loaded answers), and glossary (vocabulary bridging) — use together; see [Retrieval Optimization](#retrieval-optimization) |
| Chunking strategy | The schema IS the chunking strategy. Author files to target size so every file passes through RAG chunkers intact (400–800 tokens). Atomic strategy for workflows/troubleshooting via frontmatter. Consumer config must set `chunking.tokens` ≥ pack's hard ceiling (1,000 recommended); see [Chunking Strategy](#chunking-strategy) |
| Research coverage | Every pack includes `sources/_coverage.md` documenting what was checked, what was extracted, and what's untouched; see [Research Coverage](#research-coverage-sources_coveragemd) |
| Time variance | Annotate time-variant facts inline with `<!-- refresh -->` blocks; maintain `freshness.md` as supplementary index; for entirely time-bound files use `volatile/` directory with frontmatter TTL (`refresh`, `source`, `fetched_at`, `expires_at`); see [Time Variance](#time-variance) |
| EK ratio | Measure and maximize esoteric knowledge ratio; declare in manifest; guide hydration priority; see [Esoteric Knowledge Ratio](#esoteric-knowledge-ek-ratio) |
| Conflict resolution | Never overwrite — flag and ask the human |
| Version control | Git-native, semantic versioning |
| Obsidian compatibility | Per-file YAML frontmatter (`title`, `type`, `tags`, `pack`, `retrieval_strategy`) on all content files; `.obsidian/` reference config in repo root; `[[wikilinks]]` for body cross-links (graph-visible); bare filenames in `related:` frontmatter; unique basenames vault-wide via directory prefix; see [Obsidian Compatibility](#obsidian-compatibility) |

---

## Graph Export (_graph.yaml)

Every pack CAN include a `_graph.yaml` adjacency file at its root. This is optional but recommended for packs used with GraphRAG pipelines or any consumer that benefits from explicit entity/relationship structure.

### Why a graph layer

Markdown-first RAG works well for precise retrieval but lacks explicit relationship traversal. A graph export gives GraphRAG systems a navigable structure without making graph the canonical format — the Markdown files remain the source of truth.

### File format

```yaml
meta:
  pack: "Pack Name"
  slug: "pack-slug"
  generated_at: "2026-04-10T15:55:00Z"
  node_count: 288
  edge_count: 152
  schema_version: "1.0"

nodes:
  - id: "pack-slug/concepts/topic"     # stable frontmatter id
    title: "Topic Title"
    type: "concept"
    file: "concepts/topic.md"           # relative path for content lookup
    verified_at: "2026-04-10"

edges:
  - source: "pack-slug/concepts/topic"
    target: "pack-slug/workflows/related-workflow"
    kind: "wikilink"                    # wikilink | related | context
```

### Edge kinds

| Kind | Derived from |
|------|--------------|
| `wikilink` | `[[target.md]]` body references |
| `related` | `related:` frontmatter list |
| `context` | `<!-- context: ... related=X -->` comment hints |

### Generation

Use the `ep-graph-export` tool in `tools/graph-export/`:

```bash
python3 tools/graph-export/ep-graph-export.py /path/to/pack
```

This requires that content files have `id:` frontmatter (see Provenance Metadata section). Run `ep-validate --provenance` first to identify any files missing `id`.

### Rules

- `_graph.yaml` is **derived** from Markdown content — regenerate it when files are added, removed, or significantly restructured
- It is excluded from RAG indexing (`context.on_demand` or omitted from `extraPaths`) — it is structural metadata, not retrieval content
- Node `id` values are the stable frontmatter IDs — they match the citation IDs in the Provenance Metadata spec
- The graph is NOT bidirectional by default — edges follow the direction of the source reference
- A JSON variant (`_graph.json`) is also acceptable; use `--format json` with the export tool

### GraphRAG compatibility

The flat adjacency list is importable into common graph frameworks:
- **NetworkX:** `G.add_edges_from([(e['source'], e['target']) for e in graph['edges']])`
- **LlamaIndex Knowledge Graph:** feed nodes/edges into `KnowledgeGraphIndex`
- **Neo4j:** map nodes as `:Concept` with `id` as the key property

---

## Obsidian Compatibility

ExpertPacks are valid [Obsidian](https://obsidian.md) vaults. Any EP pack directory can be opened directly in Obsidian with full Dataview query support, graph navigation, and template-based authoring.

### Per-File YAML Frontmatter

All content files must include YAML frontmatter. Required fields:

```yaml
---
title: "Human-readable title (matches # H1 heading)"
type: "concept|workflow|troubleshooting|faq|proposition|summary|source|glossary|overview|index|decision|phase|gotcha|pattern|specification|volatile|fact|mind|relationship|presentation|verbatim|training|meta|timeline|commercial|customer|interface"
tags: [kebab-case-tags, derived-from-section-topic-and-related]
pack: "pack-slug"
retrieval_strategy: "standard|atomic"
---
```

**Required:** `title`, `type`, `tags`, `pack`
**Recommended:** `retrieval_strategy` (defaults to `standard` if omitted)
**Optional:** `ek_score` (float 0.0–1.0, from blind probing), `related` (list of relative paths to semantically related files)

**Type reference:**

| Directory / File | `type` value | `retrieval_strategy` |
|---|---|---|
| `concepts/` | `concept` | `standard` |
| `workflows/` | `workflow` | `atomic` |
| `troubleshooting/` | `troubleshooting` | `atomic` |
| `faq/` | `faq` | `standard` |
| `propositions/` | `proposition` | `standard` |
| `summaries/` | `summary` | `standard` |
| `sources/` | `source` | `standard` |
| `glossary*.md` | `glossary` | `standard` |
| `overview.md` | `overview` | `standard` |
| `_index.md` | `index` | `standard` |
| `decisions/` | `decision` | `standard` |
| `phases/` | `phase` | `atomic` |
| `gotchas/`, `common-mistakes/` | `gotcha` | `atomic` |
| `patterns/` | `pattern` | `standard` |
| `specifications/` | `specification` | `standard` |
| `volatile/`, `freshness.md` | `volatile` | `standard` |
| `facts/` | `fact` | `standard` |
| `mind/` | `mind` | `standard` |
| `relationships/` | `relationship` | `standard` |
| `verbatim/` | `verbatim` | `standard` |
| `commercial/` | `commercial` | `standard` |
| `customers/` | `customer` | `standard` |
| `interfaces/` | `interface` | `standard` |

**Frontmatter position:** Always the first thing in the file, before any `<!-- context: ... -->` annotations:

```
---
frontmatter
---

<!-- context: section=X, topic=Y, related=A,B -->

# Title
...
```

**Note on `retrieval_strategy`:** This replaces the older `retrieval.strategy` nested key. Both are accepted by current tooling; new files should use the flat `retrieval_strategy` key.

### Link Format

ExpertPacks use **Obsidian wikilinks** (`[[filename.md|Label]]`) for body cross-links. Wikilinks are the only link format that renders as graph edges in Obsidian's graph view — standard Markdown links (`[text](file.md)`) are invisible to the graph.

Because all filenames are unique vault-wide (see [Filename Uniqueness](#filename-uniqueness-required)), wikilinks use **bare filenames only** — no paths. `[[sum-nina-street.md|Nina Street]]` not `[[../summaries/stories/sum-nina-street.md|Nina Street]]`.

**Trade-off:** Wikilinks render as raw text on GitHub. This is acceptable — the primary consumption surfaces are Obsidian and agent retrieval, not GitHub browsing. GitHub users can still navigate via directory structure.

The `.obsidian/` reference config should set link format to `shortest` to match — Obsidian will create new links as bare-filename wikilinks by default.

### The `.obsidian/` Reference Folder

The repo root contains a `.obsidian/` folder with pre-configured settings:
- `app.json` — link format, attachment folder, sensible defaults
- `community-plugins.json` — Dataview + Templater enabled
- `plugins/dataview/data.json` — Dataview settings
- `graph.json` — graph view settings with `_index.md` excluded by default (see below)
- `OBSIDIAN-SETUP.md` — setup guide + useful Dataview queries

To use a pack as an Obsidian vault: copy the `.obsidian/` folder into the pack directory, then open that directory as a vault in Obsidian.

### Graph View Configuration

The `.obsidian/graph.json` config ships with `"search": "-_index"` — this excludes all `_index.md` files from the graph view by default.

**Why:** `_index.md` files link to all their children by design (for agent navigation). Without filtering, every section cluster centers on its `_index` hub rather than showing the actual concept topology. Excluding index files reveals the true knowledge graph — content nodes connected by genuine semantic relationships.

**To see index nodes:** Open Graph View → Filters panel → clear or modify the search field.

**Color groups (pre-configured):**
- Blue: `concept` files
- Green: `workflow` files
- Orange: `faq` files
- Red: `troubleshooting` files

### Content Cross-Linking

Content files should link directly to semantically related files. This serves two distinct purposes:

1. **Agent traversal** — An agent that retrieves one file can follow links to neighboring context without firing another RAG query. Dense cross-links turn a flat file collection into a navigable knowledge graph.
2. **Obsidian graph view** — Links become graph edges. A well-linked pack reveals its topology visually; an unlinked pack looks like a disconnected scatter plot.

Use both layers together:

**Layer 1 — `related:` frontmatter** (Obsidian graph edges + RAG metadata):

```yaml
---
title: "Geocoding Overview"
type: concept
tags: [geocoding, data]
pack: "my-pack"
retrieval_strategy: standard
related:
  - wf-import-data.md
  - ts-geocoding-failures.md
---
```

`related:` entries use **bare filenames only** — no directory paths. Since all filenames are unique vault-wide (prefixed by directory type), bare names are unambiguous and compatible with both agent traversal and Obsidian resolution.

**Layer 2 — Inline body wikilinks** (graph edges + agent-readable navigation):

```markdown
**Related:** [[wf-import-data.md|Import Data]], [[ts-geocoding-failures.md|Geocoding Failures]]
```

Both layers are recommended. Frontmatter powers structured queries and agent traversal. Body wikilinks create Obsidian graph edges and surface the connections to agents reading the file directly — they don't need to inspect frontmatter to know where to go next.

#### Link Density by Pack Type

The right amount of cross-linking varies by pack type and content structure:

**Product and process packs:** Link files that share a workflow, a failure mode, or a conceptual dependency. A concept file should link to its related workflows and troubleshooting entries. A workflow should link to the concepts it depends on and the errors it can trigger. Aim for 2–5 related links per file; more than 8 is usually a sign of over-linking.

**Person packs (stories specifically):** Story files should form a traversable graph, not a star. Every story that shares a person, a location, a time period, or a thematic thread should link to its neighbors — bidirectionally. The test: if an agent loads one story from a person's childhood, it should be able to traverse the entire era by following links, without needing to go back through the index.

Person pack linking patterns:
- **Location cluster:** All stories set at the same place link to each other (e.g., all Nina Street stories cross-link)
- **Person thread:** Stories featuring the same recurring character link across the arc
- **Chronological neighbors:** Stories from the same life era link to adjacent periods
- **Thematic echo:** Stories sharing a theme (pranks, faith, electronics) link across locations and eras
- **Verbatim ↔ summary:** Each summary file links to its verbatim counterpart and vice versa (**required** — verbatim files without a summary link are orphaned in graph views)

#### Bidirectionality

Links should be bidirectional where the relationship is symmetric. If file A links to file B, file B should link back to file A. Asymmetric links (A → B but not B → A) create dead ends in agent traversal and leave orphaned nodes in the graph.

The easiest way to maintain bidirectionality: when adding a `related:` entry to a file, also add the reverse link to each target file.

#### What to Link, What to Skip

**Link when:**
- The target file provides necessary context for understanding this one
- They share a central character, location, or event
- They're chronological neighbors in a sequence
- An agent reading this file would predictably want the other one next

**Don't link when:**
- The relationship is distant or generic ("both are about people")
- You'd be linking everything to everything — signal collapses
- The link would only make sense to a human browsing, not an agent retrieving

#### Maintenance

Cross-links decay when files are renamed, moved, or deleted. After any file restructuring, verify that links to the changed file still resolve. A broken link in frontmatter is silent — it won't error, but it will leave an orphaned node in the graph and a dead end for agent traversal. Periodically run:

```bash
grep -r 'related:' . | grep -o '[a-z/_-]*\.md' | sort -u
```

and verify each referenced file exists.

### What Obsidian Adds

With frontmatter in place, Obsidian users get:
- **Dataview queries** — live tables filtering by `type`, `pack`, `ek_score`, `retrieval_strategy`, tags
- **Graph view** — visual map of concept relationships (index hubs excluded by default)
- **Tag pane** — browse all content by type and domain tag
- **Templater templates** — create new EP-schema-compliant files from templates
- **Search** — full-text + frontmatter field search across the pack

---

*Schema version: 3.1*
*Last updated: 2026-04-10*
