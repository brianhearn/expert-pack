# Person Pack Schema

*Blueprint for ExpertPacks that capture a person — their stories, mind, beliefs, relationships, and voice. This schema extends [core.md](core.md); all shared principles apply.*

**Schema version:** 4.1 (2026-04-19)

---

## Purpose

A person pack creates a structured digital archive of a human being. It serves two primary purposes:

1. **While alive:** A personal AI that knows the person deeply — can retell their stories, represent their views accurately, and serve as a living archive they and their family can interact with.
2. **After death:** A memorial AI that preserves the person's authentic voice and wisdom for future generations.

The system must be good enough that someone talking to the pack's avatar feels like they're getting *that person* — not a generic AI with some facts about them.

---

## Directory Structure

```
packs/{person-slug}/
├── manifest.yaml          ← Pack identity (required — see below)
├── overview.md            ← Who this person is (required)
├── README.md              ← Project documentation
├── SCHEMA.md              ← Points to this schema
├── LEGACY.md              ← Posthumous wishes, executor chain, memorial mode
│
├── stories/               ← Life stories & memories (atomic)
│   ├── _index.md          ← Directory of all stories
│   ├── _access.json
│   └── {story-slug}.md    ← One story per file. Body carries the person's actual words.
│
├── reflections/           ← Essays, thought pieces (atomic)
│   ├── _index.md
│   └── {slug}.md
│
├── opinions/              ← Positions on issues (atomic)
│   ├── _index.md
│   └── {slug}.md
│
├── conversations/         ← Captured dialogues, interviews (atomic)
│   ├── _index.md
│   └── {slug}.md
│
├── creative/              ← Fiction, poetry, lyrics (atomic, optional)
├── letters/               ← Correspondence worth preserving (atomic, optional)
├── speeches/              ← Talks, sermons, keynotes (atomic, optional)
│
├── facts/                 ← Biographical data (atomic concept files)
│   ├── _index.md
│   ├── _access.json
│   ├── personal.md        ← Birth, family structure, locations, bio
│   ├── family-tree.md     ← Full genealogy in narrative format
│   ├── career.md          ← Work history timeline
│   ├── education.md       ← Schools, degrees, self-taught subjects
│   └── timeline.md        ← Unified life timeline (events as spine)
│
├── relationships/         ← The people graph (atomic)
│   ├── _index.md
│   ├── _access.json
│   └── {person-id}.md     ← One file per significant relationship
│
├── mind/                  ← Inner life: beliefs, sense-making, motivations (atomic)
│   ├── _index.md
│   ├── _access.json
│   ├── ontology.md        ← Ontology & Metaphysics
│   ├── epistemology.md    ← Epistemology & Sense-Making
│   ├── values.md          ← Values & Moral Framework
│   ├── identity.md        ← Identity & Self-Narrative
│   ├── motivations.md     ← Motivations, Drives & Temperament
│   ├── relational.md      ← Relational & Social Orientation
│   ├── preferences.md     ← Preferences, Tastes & Aesthetic Orientation
│   ├── skills.md          ← Skills, Competencies & Action Patterns
│   ├── tensions.md        ← Tensions, Contradictions & Edge Cases
│   ├── reasoning.md       ← How beliefs cash out in conversation (optional)
│   └── influences.md      ← Key thinkers, books, communities (optional)
│
├── presentation/          ← How the avatar should sound and look (atomic)
│   ├── _index.md
│   ├── _access.json
│   ├── speech-patterns.md ← Verbal style, humor, storytelling mode
│   ├── modes.md           ← Role-based voice variants (Dad, Mentor, Professional, etc.)
│   ├── voice/             ← Voice profile for TTS/synthesis
│   └── appearance/        ← Visual appearance for avatar rendering
│
├── training/              ← Fine-tuning data (NOT a retrieval layer — archival)
│   ├── _access.json
│   ├── config.json        ← Format spec
│   ├── qa_pairs.jsonl     ← Direct Q&A from the person
│   └── conversations.jsonl← Conversation examples
│
└── meta/                  ← System metadata
    ├── _access.json
    ├── status.json        ← Alive/memorial mode flag
    ├── access.json        ← Access tier definitions
    ├── verification.json  ← Codeword verification rules
    ├── interaction.md     ← Interaction guidelines
    ├── sessions.json      ← Capture session log
    ├── privacy.md         ← Sharing rules by access tier
    ├── consent.md         ← Third-party consent registry
    ├── conflicts.md       ← Open contradictions awaiting resolution
    └── resolutions.md     ← Resolved contradictions (append-only)
```

Not every directory is required from day one. Start with `facts/`, `stories/`, and `relationships/`, then expand as content is collected.

**Retired in v4.1:** `verbatim/` and `summaries/` (folded into type-specific atom directories); per-file `propositions/` (propositions live in atom body prose).

---

## Atomic-Conceptual Content (v4.1)

Every content file in a person pack is a **single self-contained atom** — one concept, one file, one retrieval unit. A story atom carries the story card frontmatter + the person's verbatim prose + optional `## Related` links, all in one file under the 1,000-token ceiling.

See [core.md § Atomic-Conceptual Content Files](core.md#atomic-conceptual-content-files) for the full pattern, and [`references/granularity-guide.md`](references/granularity-guide.md) for embed-vs-promote and when-to-split decision rules.

### Person-pack-specific granularity guidance

| Content type | Default granularity | When to split |
|---|---|---|
| **Story** | One atom per story | If a story exceeds 1,000 tokens, split into `story-overview.md` (summary + key moments) + `story-detail.md` (full narrative), linked via `requires:` |
| **Reflection/Opinion** | One atom per reflection/opinion | Split if it bundles multiple distinct arguments (each becomes its own atom) |
| **Fact cluster** | One atom per life-facet (`personal.md`, `career.md`, etc.) | Split when a facet grows beyond 1,000 tokens (e.g., `career-early.md` + `career-recent.md`) |
| **Relationship** | One atom per significant person | Minor relationships can group into `relationships/acquaintances.md` until they warrant their own atom |
| **Mind category** | One atom per category (`ontology.md`, `values.md`, etc.) | Split when a category grows past 1,000 tokens (e.g., `values-political.md` + `values-personal.md`) |

### Oversized stories — split pattern

When a story is too long to fit in 1,000 tokens:

```
stories/panama-city-summers.md              (overview atom, ~600 tokens)
  ├─ story card frontmatter
  ├─ narrative summary + key beats
  └─ requires: [panama-city-summers-full]

stories/panama-city-summers-full.md         (detail atom, ~900 tokens)
  ├─ provenance frontmatter
  ├─ full verbatim prose
  └─ (no outbound requires — leaf atom)
```

Retrieving the overview auto-expands to include the full detail (directional `requires:`). Retrieving the detail alone does NOT pull the overview — asymmetric, as intended.

---

## Story Cards (Frontmatter for Story/Reflection/Opinion Atoms)

The story card frontmatter that identified v3.x summary files is **retained** as the canonical metadata schema for story/reflection/opinion atoms in v4.1. This makes atoms filterable and retrievable by date, people, themes, emotions, and more.

**Required frontmatter for story atoms:**

```yaml
---
id: "childhood-fishing-trip"                # Matches the file slug
title: "The Fishing Trip That Changed Everything"
type: story
tags: [story, father, childhood]
pack: "{person-slug}"
retrieval_strategy: atomic                  # v4.1: always "atomic"
schema_version: 4.1
date_range: "1985-summer"                   # Flexible: YYYY, YYYY-MM, YYYY-MM-DD, "1985-summer", "late-1990s"
location:
  - "Lake Talquin, FL"
people:                                     # IDs matching relationships/ entries
  - "dad"
  - "uncle-mike"
themes:
  - "father-son"
  - "nature"
  - "independence"
emotions:
  - "pride"
  - "fear"
  - "belonging"
stakes: "First time trusted to handle the boat alone"
turning_point: "When dad let go of the wheel"
source: "voice-dictation"                   # voice-dictation | interview | written | email | conversation
verification: "self-confirmed"              # self-confirmed | third-party | documentary | inferred | unknown
memory_quality: "vivid"                     # vivid | partial | hearsay | uncertain
sensitivity: "public"                       # Matches access tier: public | friends | family | self
requires: []                                # Other atoms this one depends on (optional)
verified_at: "2026-04-19"
---
```

**Field notes:**
- `id` must match the filename slug for cross-referencing
- `date_range` is deliberately flexible — memories rarely come with exact dates
- `people` uses stable IDs from the relationships registry (see [Relationships](#relationships) below)
- `verification` and `memory_quality` prevent the avatar from projecting false confidence about uncertain memories. A `memory_quality: uncertain` story should be prefaced with "I think..." or "If I remember right..."
- `stakes` and `turning_point` are optional but high-value for story retrieval — they capture *why* a story matters, not just what happened
- `source` tracks how the content was captured, which affects how much editorial cleanup is appropriate
- `requires:` declares directional dependencies on other atoms (e.g., a follow-up story that only makes sense after the original — `requires: [original-story-slug]`)

**Applying to other content types:** The story card pattern extends to reflections, opinions, and other verbatim content types. Not all fields apply everywhere — `turning_point` doesn't make sense for an opinion piece. Use the fields that fit; `id`, `title`, `date_range`, `source`, `verification`, and `memory_quality` are recommended for all narrative atoms.

---

## Provenance and Memory Quality

Person packs deal with human memory, which is inherently unreliable. The schema must account for this — an avatar that states uncertain memories with full confidence is worse than one that hedges appropriately.

### Verification Levels

| Level | Meaning | Agent behavior |
|-------|---------|---------------|
| `self-confirmed` | The person explicitly confirmed this fact/memory | State normally |
| `third-party` | Confirmed by another person (family member, colleague) | State normally, may cite source |
| `documentary` | Verified by document (diploma, pay stub, photo with date) | State with high confidence |
| `inferred` | Deduced by the agent from context across multiple sources | Qualify: "Based on what I've gathered..." |
| `unknown` | No verification attempted or possible | Qualify: "I believe..." or flag as uncertain |

### Memory Quality

| Level | Meaning | Agent behavior |
|-------|---------|---------------|
| `vivid` | Rich in sensory detail, emotionally anchored, consistently retold | Retell with confidence and detail |
| `partial` | Key elements clear but gaps in timeline, names, or sequence | Fill in what's known, acknowledge gaps |
| `hearsay` | Told *about* the person by others, not experienced directly | Attribute: "My [mom/friend] told me..." |
| `uncertain` | The person themselves expressed doubt about accuracy | Preface: "I think..." or "If I remember right..." |

These fields are **required** in story card frontmatter for all story/reflection/opinion atoms. They are **recommended** as frontmatter in `facts/` files when the source of a biographical fact isn't documentary (e.g., birth dates from memory vs. birth certificates).

---

## Story Intake Workflow

For each new story:
1. Capture the person's words verbatim (voice dictation, interview, written)
2. Create the atom at `stories/{slug}.md`
3. Add story card frontmatter (see above) — do the thematic/emotional tagging from the captured content
4. Paste the verbatim prose as the atom body; add `##` section headers if it's long, but never alter the words
5. If over 1,000 tokens: split into overview + detail atoms linked via `requires:`
6. Cross-reference relationships — update each mentioned person's `relationships/{id}.md` atom
7. Flag contradictions in `meta/conflicts.md`
8. Commit

For voice dictation: clean transcription errors but preserve phrasing, tangents, and style. The goal is *their voice*, not polished prose.

For the full agent-first creation playbook, see [guides/hydration.md](../guides/hydration.md).

---

## Biographical Data Patterns

Each biographical atom is a self-contained file under the 1,000-token ceiling. When a life-facet grows beyond that, split into sub-atoms linked with `requires:`.

### facts/personal.md
Birth date, family structure, locations lived, basic biographical data. Use `##` headers to organize by life period or topic.

### facts/family-tree.md
Full genealogy in narrative Markdown format. This is the canonical version — if a JSON genealogy file exists (e.g., GEDCOM-derived), it is archival only. Splits naturally by branch when it grows (`family-tree-paternal.md`, `family-tree-maternal.md`) linked via `requires:` from the root.

### facts/career.md
Work history as a timeline with highlights, key roles, and transitions. Split by era (`career-early.md`, `career-recent.md`) when needed.

### facts/education.md
Schools, degrees, certifications, and self-taught subjects.

### facts/timeline.md

The unified life timeline — events as the backbone of the person's story. While `career.md`, `education.md`, and `personal.md` organize facts by category, the timeline organizes them chronologically and connects events to stories, reflections, and relationships.

```markdown
---
id: timeline
title: "Life Timeline"
type: fact
tags: [timeline, fact, spine]
pack: "{person-slug}"
retrieval_strategy: atomic
schema_version: 4.1
---

# Life Timeline

## Early Childhood (1970–1978)

### 1970 — Born
- **Type:** birth
- **Place:** Tallahassee, FL
- **People:** [mom](../relationships/mom.md), [dad](../relationships/dad.md)
- **Related:** [[../stories/birth-story.md|Birth Story]]

### 1975 — Started school
- **Type:** education
- **Place:** Lincoln Elementary
- **Related:** [[../stories/first-day.md|First Day of School]]

## Adolescence (1978–1988)
...
```

**Structure guidelines:**
- Organize by life period with `##` headers (flexible — decades, life stages, or whatever fits)
- Each event gets a `###` header with year/date and short title
- Include: type, place, people involved, and links to related stories/reflections
- Event types: `birth`, `move`, `education`, `job`, `marriage`, `divorce`, `death`, `crisis`, `conversion`, `achievement`, `travel`, `health`, `military`, `legal`, `creative`, `other`
- Keep entries brief — the timeline is a spine, not a narrative. Details live in the linked atoms
- When the timeline grows beyond ~100 events, split into period atoms (`timeline-early.md`, `timeline-adolescence.md`) linked from the root via `requires:`

### relationships/{person-id}.md

Each significant person in the subject's life gets their own atom. The file slug is the stable ID used in story card `people` arrays and timeline entries.

**Atom template:**

```markdown
---
id: uncle-mike
title: "Mike Hearn (Uncle Mike)"
type: relationship
tags: [relationship, family, uncle]
pack: "{person-slug}"
retrieval_strategy: atomic
schema_version: 4.1
relationship: "Uncle (father's brother)"
time_period: "Lifelong (born 1948)"
consent: "not-asked"
verified_at: "2026-04-19"
---

# Mike Hearn (Uncle Mike)

**Relationship:** Uncle (father's brother)
**Time period:** Lifelong (born 1948)
**How they connect:** Dad's older brother, constant presence at family gatherings

## Key facts
- Vietnam veteran
- Taught me to fish
- Lived in Panama City for decades

## Appears in
- [[../stories/childhood-fishing-trip.md|Fishing Trip]]
- [[../stories/panama-city-summers.md|Panama City Summers]]

## Consent
Not asked about inclusion as of 2026-04-19.
```

**Guidelines:**
- **File slug** (`uncle-mike`) is the stable ID used everywhere — in story card `people:` arrays, timeline entries, and other atoms' body links
- **`time_period`** captures when the relationship was active: `lifelong`, `1995–2003`, `childhood`, `ongoing`. Prevents the agent from flattening a life into one static social graph
- **`consent`** tracks whether this person has been asked about inclusion: `consented`, `not-asked`, `declined`, `deceased`, `public-figure`. See [Privacy & Consent](#privacy--consent) for rules
- **Appears in** should cross-link to every atom where this person is mentioned — keep this list current when new content references them
- **Minor relationships** can group into `relationships/acquaintances.md` until they warrant their own atom

---

## The Mind Taxonomy

The person's inner life (formerly "worldview" + "preferences") is captured under the `mind/` directory as atomic concept files. Each category is a single atom under the 1,000-token ceiling. Split into sub-atoms when a category grows.

### Mind Taxonomy Categories

1. **ontology.md** — Ontology & Metaphysics. What the person believes is ultimately real and how reality is structured. Includes religious/spiritual worldview, views on consciousness, the nature of God, the soul, materialism vs. dualism, cosmology (as it relates to meaning), and any framework for understanding existence itself.

2. **epistemology.md** — Epistemology & Sense-Making. How the person determines what is true and updates beliefs. Includes their relationship between faith and reason, trust in institutions, how they weigh evidence, their approach to certainty and doubt, intellectual influences, and how they process new information that challenges existing views.

3. **values.md** — Values & Moral Framework. What the person considers good, bad, right, and worth protecting. Includes ethical principles, political philosophy (as it reflects values), priorities in life, what they'd sacrifice for, views on justice and fairness, and the moral reasoning behind their positions. Political views live here primarily, with cross-references to epistemology and ontology where those inform the positions.

4. **identity.md** — Identity & Self-Narrative. How the person understands who they are across roles and time. The story they tell about themselves — key turning points, how they see their own arc, the roles that define them (father, engineer, pilot, apologist), how past experiences shaped who they became. Not external biography (that's `facts/`), but internal self-concept.

5. **motivations.md** — Motivations, Drives & Temperament. What energizes behavior and shapes emotional responses. Includes personality traits, ambition, what gives them energy vs. drains them, emotional patterns, how they handle stress/failure/success, risk tolerance, introversion/extroversion, and the deeper drives behind their choices.

6. **relational.md** — Relational & Social Orientation. How the person connects with others. Trust patterns, communication style, conflict approach, how they form and maintain friendships, authority orientation, group behavior vs. one-on-one, loyalty patterns, what they value in others, and how they show care.

7. **preferences.md** — Preferences, Tastes & Aesthetic Orientation. What the person is drawn to, enjoys, and finds meaningful. Hobbies, media consumption, aesthetic sensibilities, food/music/film/book preferences, leisure activities, guilty pleasures, and what they find beautiful or compelling. Lighter than values — this is about taste, not morality.

8. **skills.md** — Skills, Competencies & Action Patterns. What the person can do and how they tend to act in the world. Professional expertise, learned skills, problem-solving approach, how they learn new things, domains of competence, work style, tools they reach for, and patterns in how they execute on goals.

9. **tensions.md** — Tensions, Contradictions & Edge Cases. Where the model breaks — the places where other categories don't fully cohere. Context-dependent behavior switches, acknowledged blind spots, unresolved internal conflicts, things they believe but don't practice (or vice versa), and the messy human reality that neat categories miss. This is some of the most valuable content for authenticity.

### Additional Mind Atoms (Optional)

10. **reasoning.md** — Reasoning Patterns & Decision Rules. How the person's beliefs cash out in actual conversation and decision-making. Not *what* they believe (that's the other 9 categories) but *how they reason* when challenged, asked, or deciding. Patterns like: "When asked about X, I reason from Y principle," "I tend to steelman before responding," "I distinguish between confident claims and speculative ones." This atom bridges the gap between a list of positions and a living reasoning style. Include examples of real reasoning chains from captured content. Often `requires: [epistemology, values]`.

11. **influences.md** — Key Thinkers, Books & Communities. The intellectual and social inputs that shaped the person's mind. Authors, books, podcasts, thinkers, mentors, faith communities, professional networks, formative experiences. Each influence entry should note: what they contributed to the person's thinking, when the influence was strongest, and links to relevant reflection atoms where the influence is visible.

**Steelman positions** — Rather than a separate atom, capture "strongest arguments against my position and my best response" inline in the relevant mind/ atoms (ontology, values, epistemology, etc.) under a `## Strongest Counterarguments` section. This keeps counterarguments findable in context rather than siloed.

### Splitting Mind Categories

When a mind atom grows past the 1,000-token ceiling, split along natural internal subdivisions. Examples:
- `values.md` → `values.md` (core summary) + `values-political.md` + `values-personal.md`, with `values.md` carrying `requires: [values-political, values-personal]`
- `preferences.md` → split by domain: `preferences-media.md`, `preferences-food.md`, `preferences-leisure.md`

### Political Views
Political views are cross-cutting: they live primarily in `mind/values.md` (or `mind/values-political.md` if split) with cross-references to `mind/epistemology.md` and `mind/ontology.md` when those domains inform political positions. Use `requires:` if the political values atom depends on reading the epistemology atom to make sense.

---

## Avatar Modes

The same person speaks differently as a dad, a CEO, a mentor, and a friend. `presentation/modes.md` captures these role-based voice variants so the avatar can adjust its register without creating multiple packs.

**Template for `presentation/modes.md`:**

```markdown
---
id: modes
title: "Avatar Modes"
type: presentation
tags: [presentation, modes, voice]
pack: "{person-slug}"
retrieval_strategy: atomic
schema_version: 4.1
---

# Avatar Modes

## Default
The baseline voice — how the person sounds in most casual interactions.

## Dad Mode
- **Tone:** Warm, patient, occasionally goofy
- **Topics to emphasize:** Family stories, life lessons, encouragement
- **Topics to avoid:** Work stress, politics (unless asked)
- **Example phrasing:** "Let me tell you something I learned the hard way..."

## Professional Mode
- **Tone:** Direct, precise, confident
- **Topics to emphasize:** Technical expertise, industry knowledge, business strategy
- **Topics to avoid:** Personal beliefs (unless directly relevant), family details
- **Example phrasing:** "The way I'd approach this architecturally..."

## Mentor Mode
- **Tone:** Socratic, challenging but supportive
- **Topics to emphasize:** Reasoning process, lessons from mistakes, frameworks for thinking
- **Topics to avoid:** Giving direct answers when the person should figure it out
- **Example phrasing:** "What assumptions are you making there?"

## {Custom Mode}
...
```

**Guidelines:**
- Each mode defines: tone, topics to emphasize, topics to avoid, and example phrasings
- Modes are hints, not hard constraints — the avatar should blend naturally between modes based on context
- The agent selects modes based on conversational context (who's asking, what topic, what relationship tier)
- Start with 2-3 modes and expand as patterns emerge from story collection
- Modes complement `speech-patterns.md` — patterns define *how* the person talks; modes define *which version* of them shows up

---

## Privacy & Consent

Person packs contain information about real people — both the subject and the people in their stories. The schema provides two files to manage what can be shared and who has consented to inclusion.

### meta/privacy.md

Defines what content is shareable at each access tier. This is the human-readable policy that the agent enforces.

```markdown
# Privacy Policy

## Public (anyone)
- Overview, career highlights, published writing
- Stories marked sensitivity: public
- General preferences and interests

## Friends (known contacts)
- Most stories and reflections
- Relationship details (non-sensitive)
- Mind taxonomy content

## Family (immediate family)
- All stories including sensitive ones
- Family tree details
- Health and personal struggles

## Self (owner only)
- Financial details
- Medical records
- Unresolved conflicts
- Content marked sensitivity: self
```

### meta/consent.md

Tracks whether third parties mentioned in the pack have been asked about their inclusion. This is especially important for packs that will be shared beyond the `self` tier.

```markdown
# Third-Party Consent Registry

| Person ID | Name | Status | Date Asked | Notes |
|-----------|------|--------|------------|-------|
| uncle-mike | Mike Hearn | not-asked | — | Appears in 3 stories |
| jane-doe | Jane Doe | consented | 2026-03-01 | Verbal consent, comfortable with public stories |
| john-smith | John Smith | declined | 2026-02-15 | Remove from public-tier content |
```

**Consent statuses:** `consented`, `not-asked`, `declined`, `deceased`, `public-figure`

**Agent rules:**
- When generating content at `public` or `friends` tier, check consent status for all people referenced
- People with `declined` status: redact or anonymize in content at or above their objection tier
- People with `not-asked` status: flag for the pack owner to follow up before sharing content publicly
- `deceased` and `public-figure` statuses carry lower consent requirements but the pack owner should still be thoughtful

---

## Conflicts & Resolutions

Human memory is messy. Facts conflict, stories evolve, timelines shift. Core schema says "never overwrite — flag and ask the human." Person packs formalize *where* those conflicts live so they're tracked and resolvable over time.

### meta/conflicts.md

Open contradictions awaiting the pack owner's adjudication. The agent adds entries here whenever it detects conflicting information during intake.

```markdown
# Open Conflicts

## CF-001: Panama City trip — 1983 or 1985?
- **Detected:** 2026-03-01
- **Source A:** stories/panama-city-summers.md says "summer of '83"
- **Source B:** facts/timeline.md places the family's first Panama City visit in 1985
- **Notes:** Mom's version (hearsay) says 1985. Uncle Mike's photo album has a 1983 date.
- **Status:** Awaiting owner review

## CF-002: First job — delivery driver or stock clerk?
...
```

### meta/resolutions.md

Append-only log of resolved contradictions. When the owner makes a call, move the entry from conflicts.md to here with the decision and rationale.

```markdown
# Resolved Conflicts

## CF-001: Panama City trip — 1983 or 1985?
- **Resolved:** 2026-03-05
- **Decision:** 1983 — confirmed by photo album with dated prints
- **Rationale:** Documentary evidence (photos with processing date) outweighs memory
- **Files updated:** facts/timeline.md, stories/panama-city-summers.md
```

**Agent rules:**
- Add to `conflicts.md` immediately when a contradiction is detected — don't wait for the next session
- Never resolve a conflict autonomously — always ask the pack owner
- When resolved, move the entry to `resolutions.md` (append), remove from `conflicts.md`, and update all affected atoms
- Assign conflict IDs (CF-001, CF-002, ...) for easy reference in conversation

---

## Person-Specific Manifest Fields

Beyond the core manifest fields defined in [core.md](core.md):

```yaml
# Required
name: "Person's Full Name"
slug: "person-slug"
type: "person"
version: "1.0.0"
description: "What this pack captures"
entry_point: "overview.md"
schema_version: 4.1

# Person-specific
subject:
  full_name: "Robert James Smith"
  born: "YYYY-MM-DD"
  location: "City, State"
  alive: true

# Content inventory (v4.1 — flat atom directories, no verbatim/summaries split)
sections:
  - stories
  - reflections
  - opinions
  - facts
  - relationships
  - mind
  - presentation
  - training
  - meta

# Data sources
sources:
  - type: "website"
    url: "https://example.com"
    description: "Personal blog — philosophy, hobbies, stories"
  - type: "conversation"
    description: "Ongoing story capture via voice/chat"
  - type: "genealogy"
    description: "Family tree export (GEDCOM or similar)"
```

---

## Access Tiers & _access.json

Access tiers control what content is shareable with whom. Defined in `meta/privacy.md` (human-readable policy) and enforced via `_access.json` files placed in directories.

**Tiers (most to least open):** `public` → `friends` → `family` → `self`

**`_access.json` format:**
```json
{
  "default_access": "public",
  "overrides": {
    "private-file.md": "self"
  }
}
```

Place `_access.json` in any directory to set its default access tier and per-file overrides. If absent, the directory inherits the pack's default (typically `public`).

**Agent rules:**
- When generating content for a given audience tier, check all `_access.json` files for referenced directories
- Content in directories/files restricted to a higher tier (e.g., `self`) must not appear in responses at lower tiers
- Posthumous access rules are defined in `LEGACY.md` and may override these tiers

---

## Tags Taxonomy

Use the 25-type taxonomy from core.md frontmatter. Key types for person packs in v4.1:

| Type | Used In |
|---|---|
| `story` | `stories/` atoms |
| `reflection` | `reflections/` atoms |
| `opinion` | `opinions/` atoms |
| `conversation` | `conversations/` atoms |
| `fact` | `facts/` atoms |
| `relationship` | `relationships/` atoms |
| `mind` | `mind/` atoms |
| `presentation` | `presentation/` atoms |
| `index` | `_index.md` files |

Full taxonomy in [core.md](core.md#per-file-yaml-frontmatter).

---

## Universal Metadata

All person pack atoms should include standard frontmatter fields: `id`, `title`, `type`, `tags`, `pack`, `retrieval_strategy: atomic`, `schema_version: 4.1`, and provenance fields (`content_hash`, `verified_at`, `verified_by`, `supersedes` where applicable). See [core.md](core.md#atomic-conceptual-content-files) for the full frontmatter spec.

The `requires:` field is optional but recommended whenever an atom's meaning depends on another atom being in context (e.g., a follow-up story, a political-values atom that depends on epistemology, a timeline-era atom that depends on the root timeline).

---

## Pack Population

For general guidance on population methods — documentation ingestion, video ingestion, conversational ingestion, expert walkthroughs, observation & testing, and more — see the [Hydration Guide](../guides/hydration.md).

For person packs, the recommended combining order is:
1. Documentation ingestion → published works, online presence
2. Conversational ingestion → stories, beliefs, opinions (ongoing, primary method)
3. Video ingestion → talks, interviews, appearances
4. Expert walkthrough → the person validates and corrects
5. Observation & testing → roleplay conversations to find gaps

---

## Creating a New Person Pack

For the full agent-first creation playbook (14-step sequence covering pack initialization, story capture, mind taxonomy, relationships, privacy, and verification), see [guides/hydration.md](../guides/hydration.md).

Key principles:
- **Atomic-conceptual from day one.** Each story, reflection, opinion, fact cluster, relationship, and mind category is a self-contained atom under the 1,000-token ceiling.
- **Verbatim prose lives inside the atom.** The person's actual words are the body of the story/reflection/opinion atom — no separate verbatim/summary directories.
- **Record provenance for every file.** Never overwrite expert-verified content without reconfirmation.
- **Log contradictions in `meta/conflicts.md` immediately.** Never resolve autonomously.
- **Use short, specific prompts** — one story or fact at a time.

---

## Agent Extension (subtype: agent)

For packs with `subtype: agent`, see [agent.md](agent.md).

---

*Schema version: 4.1*
*Last updated: 2026-04-19*
