# Person Pack Schema

*Blueprint for ExpertPacks that capture a person — their stories, mind, beliefs, relationships, and voice. This schema extends [core.md](core.md); all shared principles apply.*

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
├── verbatim/              ← The person's actual words (source of truth)
│   ├── stories/           ← Life stories, childhood memories, adventures
│   │   └── _access.json
│   ├── reflections/       ← Essays, thought pieces, intellectual writing
│   ├── opinions/          ← Positions on issues, arguments, commentary
│   └── {custom}/          ← Additional content types as needed
│
├── summaries/             ← AI-generated summaries of verbatim content
│   ├── stories/           ← Story summaries with themes, people, lessons
│   │   ├── _index.json    ← Master story navigation index
│   │   └── _access.json
│   ├── reflections/       ← Reflection summaries with key arguments
│   ├── opinions/          ← Opinion summaries with positions
│   └── {custom}/          ← Mirrors verbatim/ structure
│
├── propositions/          ← Atomic factual statements for precise retrieval (recommended) ← See core.md Retrieval Optimization
│   ├── _index.md          ← Directory of all proposition files
│   └── {section}.md       ← Extracted facts from facts/, mind/, relationships/ files
│
├── facts/                 ← Biographical data (Markdown — canonical)
│   ├── _access.json
│   ├── personal.md        ← Birth, family structure, locations, bio
│   ├── family_tree.md     ← Full genealogy in narrative format
│   ├── career.md          ← Work history timeline
│   ├── education.md       ← Schools, degrees, self-taught subjects
│   └── timeline.md        ← Unified life timeline (events as the backbone)
│
├── relationships/         ← The people graph
│   ├── _access.json
│   └── people.md          ← Everyone mentioned: family, friends, mentors
│
├── mind/                  ← Mind taxonomy: beliefs, sense-making, motivations, and preferences
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
├── presentation/          ← How the avatar should sound and look
│   ├── _access.json
│   ├── speech_patterns.md ← Verbal style, humor, storytelling mode
│   ├── modes.md           ← Role-based voice variants (Dad, Mentor, Professional, etc.)
│   ├── voice/             ← Voice profile for TTS/synthesis
│   └── appearance/        ← Visual appearance for avatar rendering
│
├── training/              ← Fine-tuning data (experimental)
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

Not every directory is required from day one. Start with `facts/`, `verbatim/`, and `relationships/`, then expand as content is collected.

---

## The Two-Tier Content System

Every piece of the person's writing or dictation exists in two forms:

| Layer | Directory | Purpose | Token Cost | When to Use |
|-------|-----------|---------|------------|-------------|
| **Verbatim** | `verbatim/` | Person's exact words | High | Retelling stories, exact quotes, avatar performance, fine-tuning |
| **Summary** | `summaries/` | Structured distillation | Low | Context loading, search results, quick reference, theme analysis |

### Why Both?

An AI retelling a person's story needs their actual words — the humor, the pacing, the details only they would include. But an AI answering "what themes run through their childhood?" just needs the summary. The two-tier system optimizes for both use cases without burning tokens.

### Priority

**Verbatim first, summaries second.** The person's actual words are the source of truth. Summaries are generated from verbatim content. If a summary and verbatim disagree, the verbatim wins.

### Organizing Verbatim and Summary Content

Verbatim and summary directories should mirror each other — if `verbatim/stories/{story-slug}.md` exists, there should be a corresponding `summaries/stories/{story-slug}.md`. Subdirectories within verbatim/ and summaries/ are organized by content type.

Content Type Taxonomy

Verbatim and summary directories are organized by content type. The following taxonomy provides recommended categories — use what fits, extend as needed:

| Content Type | Directory | Description |
|---|---|---|
| Life stories & memories | `stories/` | Narratives, experiences, adventures, childhood memories. Recommended for all person packs. |
| Essays & reflections | `reflections/` | Thought pieces, intellectual writing, personal essays, philosophical or theological exploration |
| Opinions & commentary | `opinions/` | Positions on specific issues, arguments, responses to events, political or cultural commentary |
| Conversations | `conversations/` | Captured dialogues, interviews, dictated Q&A sessions |
| Creative works | `creative/` | Fiction, poetry, song lyrics, music notes, artistic expression |
| Letters & correspondence | `letters/` | Written communications worth preserving |
| Speeches & presentations | `speeches/` | Talks, sermons, keynotes, prepared remarks, toasts |

**Extending the taxonomy:** Packs may add content types not listed here. A pastor might add `sermons/`, a musician `lyrics/`, a traveler `journals/`. Create the subdirectory in both `verbatim/` and `summaries/` and add it to the pack's `_index.md`.

**Mirror rule:** Verbatim and summary directories should always mirror each other. If `verbatim/reflections/` exists, `summaries/reflections/` should too.

Person packs also benefit from propositions — see [Retrieval Optimization](core.md#retrieval-optimization). Extract propositions from `facts/`, `mind/`, and `relationships/` files. Person pack summaries follow the verbatim→summary mirroring pattern described above; propositions follow the standard core pattern.

### Story Cards (Summary Frontmatter)

Every summary file should include standardized YAML frontmatter — the **story card**. This makes summaries filterable and retrievable by date, people, themes, emotions, and more, without requiring the agent to parse freeform text.

**Required frontmatter for summary files:**

```yaml
---
story_id: "childhood-fishing-trip"          # Matches the file slug
title: "The Fishing Trip That Changed Everything"
date_range: "1985-summer"                   # Flexible: YYYY, YYYY-MM, YYYY-MM-DD, "1985-summer", "late-1990s"
location:
  - "Lake Talquin, FL"
people:                                     # IDs matching relationships/people.md entries
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
canonical_verbatim: "verbatim/stories/childhood-fishing-trip.md"
---
```

**Field notes:**
- `story_id` must match the filename slug for cross-referencing
- `date_range` is deliberately flexible — memories rarely come with exact dates
- `people` uses stable IDs from the relationships registry (see [Relationships](#relationships) below)
- `verification` and `memory_quality` prevent the avatar from projecting false confidence about uncertain memories. A `memory_quality: uncertain` story should be prefaced with "I think..." or "If I remember right..."
- `stakes` and `turning_point` are optional but high-value for story retrieval — they capture *why* a story matters, not just what happened
- `source` tracks how the content was captured, which affects how much editorial cleanup is appropriate

**Applying to other content types:** The story card pattern extends to reflections, opinions, and other content types. Not all fields apply everywhere — `turning_point` doesn't make sense for an opinion piece. Use the fields that fit; the `story_id`, `title`, `date_range`, `source`, `verification`, and `memory_quality` fields are recommended for all summary files.

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

These fields are **required** in story card frontmatter for all summary files. They are **recommended** as frontmatter in facts/ files when the source of a biographical fact isn't documentary (e.g., birth dates from memory vs. birth certificates).

---

## Story Intake Workflow

When the person dictates a new story or memory:

1. **Capture** — Record verbatim text from voice dictation or written input into `verbatim/stories/`
2. **Structure** — Add `##` section headers at natural topic breaks (never change the person's words — only insert structural markers between existing paragraphs)
3. **Summarize** — Generate a summary in `summaries/stories/` with themes, people, places, emotions
4. **Cross-reference** — Search existing content for related people, places, events
5. **Update relationships** — Check `relationships/people.md` for new or updated people; add entries
6. **Update index** — Add entry to `summaries/stories/_index.json`
7. **Contradiction check** — Flag any conflicts with existing data for the person to resolve. Log open contradictions in `meta/conflicts.md` (see [Conflicts & Resolutions](#conflicts--resolutions) below and [core.md](core.md) conflict resolution rules)
8. **Update changelog** — Append an entry to `meta/changelog.md` with what was captured, the source, and file names (see [core.md](core.md) content changelog)
9. **Commit** — Git commit and push to preserve versioning

### Voice Dictation Notes

When content arrives via voice dictation, the transcription will be imperfect but authentic. Clean up obvious transcription errors but preserve the person's phrasing, tangents, and style. The goal is *their voice*, not polished prose.

---

## Biographical Data Patterns

### facts/personal.md
Birth date, family structure, locations lived, basic biographical data. Use `##` headers to organize by life period or topic.

### facts/family_tree.md
Full genealogy in narrative Markdown format. This is the canonical version — if a JSON genealogy file exists (e.g., GEDCOM-derived), it is archival only.

### facts/career.md
Work history as a timeline with highlights, key roles, and transitions.

### facts/education.md
Schools, degrees, certifications, and self-taught subjects.

### facts/timeline.md

The unified life timeline — events as the backbone of the person's story. While `career.md`, `education.md`, and `personal.md` organize facts by category, the timeline organizes them chronologically and connects events to stories, reflections, and relationships.

```markdown
# Life Timeline

## Early Childhood (1970–1978)

### 1970 — Born
- **Type:** birth
- **Place:** Tallahassee, FL
- **People:** [mom](#), [dad](#)
- **Related:** [Birth Story](../summaries/stories/birth-story.md)

### 1975 — Started school
- **Type:** education
- **Place:** Lincoln Elementary
- **Related:** [First Day of School](../summaries/stories/first-day.md)

## Adolescence (1978–1988)
...

## College & Early Career (1988–1995)
...
```

**Structure guidelines:**
- Organize by life period with `##` headers (flexible — decades, life stages, or whatever fits)
- Each event gets a `###` header with year/date and short title
- Include: type, place, people involved, and links to related stories/reflections
- Event types: `birth`, `move`, `education`, `job`, `marriage`, `divorce`, `death`, `crisis`, `conversion`, `achievement`, `travel`, `health`, `military`, `legal`, `creative`, `other`
- Keep entries brief — the timeline is a spine, not a narrative. Details live in the linked files
- When the timeline grows beyond ~100 events, consider splitting into separate files by life period

### relationships/people.md

Every person mentioned across the pack: family, friends, mentors, colleagues. Each entry uses a standardized template with stable IDs for cross-referencing from story cards, timeline events, and other content.

**Entry template:**

```markdown
## Mike Hearn {#uncle-mike}

- **ID:** `uncle-mike`
- **Relationship:** Uncle (father's brother)
- **Time period:** Lifelong (born 1948)
- **How they met/connect:** Dad's older brother, constant presence at family gatherings
- **Key facts:** Vietnam veteran, taught me to fish, lived in Panama City
- **Consent:** not-asked
- **Appears in:**
  - [Fishing Trip](../summaries/stories/childhood-fishing-trip.md)
  - [Panama City Summers](../summaries/stories/panama-city-summers.md)
```

**Entry guidelines:**
- **ID** must be stable and kebab-case — used in story card `people` arrays and timeline entries for cross-referencing
- **Time period** captures when the relationship was active: `lifelong`, `1995–2003`, `childhood`, `ongoing`. This prevents the agent from flattening a life into one static social graph
- **Consent** tracks whether this person has been asked about inclusion: `consented`, `not-asked`, `declined`, `deceased`, `public-figure`. See [Privacy & Consent](#privacy--consent) for rules
- **Appears in** links to every file where this person is mentioned — keep this list current when new content references them

**Scaling guidance:** When `people.md` exceeds ~50 entries, split into category files: `relationships/family.md`, `relationships/professional.md`, `relationships/personal.md`. Maintain the same entry template and ID scheme across all files. Update `relationships/_index.md` to list all files.

---

## The Mind Taxonomy

The person's inner life (formerly "worldview" + "preferences") is captured under a unified `mind/` directory. This organizes beliefs, sense-making approaches, values, preferences, skills, and tensions into a consistent filing system for agents.

Each category starts as a single `.md` file but may expand into a subdirectory as content grows (e.g., `mind/ontology/` with multiple files).

### Mind Taxonomy Categories

1. ontology.md — Ontology & Metaphysics
What the person believes is ultimately real and how reality is structured. Includes religious/spiritual worldview, views on consciousness, the nature of God, the soul, materialism vs. dualism, cosmology (as it relates to meaning), and any framework for understanding existence itself.

2. epistemology.md — Epistemology & Sense-Making
How the person determines what is true and updates beliefs. Includes their relationship between faith and reason, trust in institutions, how they weigh evidence, their approach to certainty and doubt, intellectual influences, and how they process new information that challenges existing views.

3. values.md — Values & Moral Framework
What the person considers good, bad, right, and worth protecting. Includes ethical principles, political philosophy (as it reflects values), priorities in life, what they'd sacrifice for, views on justice and fairness, and the moral reasoning behind their positions. Political views live here primarily, with cross-references to epistemology and ontology where those inform the positions.

4. identity.md — Identity & Self-Narrative
How the person understands who they are across roles and time. The story they tell about themselves — key turning points, how they see their own arc, the roles that define them (father, engineer, pilot, apologist), how past experiences shaped who they became. Not external biography (that's `facts/`), but internal self-concept.

5. motivations.md — Motivations, Drives & Temperament
What energizes behavior and shapes emotional responses. Includes personality traits, ambition, what gives them energy vs. drains them, emotional patterns, how they handle stress/failure/success, risk tolerance, introversion/extroversion, and the deeper drives behind their choices.

6. relational.md — Relational & Social Orientation
How the person connects with others. Trust patterns, communication style, conflict approach, how they form and maintain friendships, authority orientation, group behavior vs. one-on-one, loyalty patterns, what they value in others, and how they show care.

7. preferences.md — Preferences, Tastes & Aesthetic Orientation
What the person is drawn to, enjoys, and finds meaningful. Hobbies, media consumption, aesthetic sensibilities, food/music/film/book preferences, leisure activities, guilty pleasures, and what they find beautiful or compelling. Lighter than values — this is about taste, not morality.

8. skills.md — Skills, Competencies & Action Patterns
What the person can do and how they tend to act in the world. Professional expertise, learned skills, problem-solving approach, how they learn new things, domains of competence, work style, tools they reach for, and patterns in how they execute on goals.

9. tensions.md — Tensions, Contradictions & Edge Cases
Where the model breaks — the places where other categories don't fully cohere. Context-dependent behavior switches, acknowledged blind spots, unresolved internal conflicts, things they believe but don't practice (or vice versa), and the messy human reality that neat categories miss. This is some of the most valuable content for authenticity.

### Additional Mind Files (Optional)

10. reasoning.md — Reasoning Patterns & Decision Rules
How the person's beliefs cash out in actual conversation and decision-making. Not *what* they believe (that's the other 9 categories) but *how they reason* when challenged, asked, or deciding. Patterns like: "When asked about X, I reason from Y principle," "I tend to steelman before responding," "I distinguish between confident claims and speculative ones." This file bridges the gap between a list of positions and a living reasoning style. Include examples of real reasoning chains from verbatim content.

11. influences.md — Key Thinkers, Books & Communities
The intellectual and social inputs that shaped the person's mind. Authors, books, podcasts, thinkers, mentors, faith communities, professional networks, formative experiences. Each influence entry should note: what they contributed to the person's thinking, when the influence was strongest, and links to relevant verbatim reflections or opinions where the influence is visible.

**Steelman positions** — Rather than a separate file, capture "strongest arguments against my position and my best response" inline in the relevant mind/ files (ontology, values, epistemology, etc.) under a `## Strongest Counterarguments` section. This keeps counterarguments findable in context rather than siloed.

### Political Views
Political views are cross-cutting: they live primarily in `mind/values.md` with cross-references to `mind/epistemology.md` and `mind/ontology.md` when those domains inform political positions.

---

## Avatar Modes

The same person speaks differently as a dad, a CEO, a mentor, and a friend. `presentation/modes.md` captures these role-based voice variants so the avatar can adjust its register without creating multiple packs.

**Template for `presentation/modes.md`:**

```markdown
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
- Modes complement `speech_patterns.md` — patterns define *how* the person talks; modes define *which version* of them shows up

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
- **Source A:** verbatim/stories/panama-city-summers.md says "summer of '83"
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
- **Files updated:** facts/timeline.md, summaries/stories/panama-city-summers.md
```

**Agent rules:**
- Add to `conflicts.md` immediately when a contradiction is detected — don't wait for the next session
- Never resolve a conflict autonomously — always ask the pack owner
- When resolved, move the entry to `resolutions.md` (append), remove from `conflicts.md`, and update all affected files
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

# Person-specific
subject:
  full_name: "Robert James Smith"
  born: "YYYY-MM-DD"
  location: "City, State"
  alive: true

# Content inventory
sections:
  - verbatim
  - summaries
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

## Access Tiers

(Person schema access tiers unchanged — preserved verbatim)

---

## Tags Taxonomy

(unchanged)

---

## Universal Metadata

(unchanged)

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

This section is a playbook for an AI agent creating and maintaining a person pack. Read the schema above as your filing guide; read the [Hydration Guide](../guides/hydration.md) for how to execute each ingestion method.

Agent-first step-by-step

1. **Read the schema, directory blueprint, and [Hydration Guide](../guides/hydration.md)**
   - Load this file and core.md to understand required files, directories, and content types.
   - Use the schema as the authoritative filing map: when content arrives, determine its target directory by content type (verbatim, summaries, facts, mind, relationships, presentation, training, meta).

2. Initialize the pack
   - Create the pack directory at packs/{person-slug}/.
   - Create required files and minimal structure: manifest.yaml (type: person), overview.md, and starter directories: facts/, verbatim/, relationships/, summaries/, mind/, presentation/, meta/.
   - Commit the initial skeleton to git with a clear message.

3. Onboard the pack owner (the person / pack owner)
   - Introduce yourself as the agent and explain your role: you will guide them through capturing biographical facts, stories, and internal beliefs, and you will file everything using the schema.
   - Ask for consent and access to source materials (documents, websites, recorded audio, support exports, GEDCOMs) and preferred modes of capture (voice dictation, email, shared doc).

4. Collect canonical biographical facts first
   - Guide the person to provide core facts for facts/personal.md: full name, birth date/place, major life locations, family roles, and contact details for immediate relatives.
   - Create facts/career.md as a timeline: ask for employers, roles, dates, notable projects, and transitions. When unsure, suggest prompts: "Where did you work between YEAR and YEAR?" or "Tell me about the role that changed your career trajectory."
   - Create facts/education.md: schools, degrees, certifications, informal study. Use targeted prompts: "List the institutions and years, or say 'unknown' if you prefer not to provide dates."
   - Begin facts/timeline.md with confirmed events — add entries as facts are collected. The timeline becomes the chronological spine that connects all other content.
   - As each fact is confirmed, commit and annotate sources in manifest.yaml sources:[]
   - Set `verification` and `memory_quality` for facts based on source quality (documentary evidence vs. memory vs. hearsay).

5. Drive story collection (verbatim first)
   - Prioritize capturing the person's exact words into verbatim/stories/, verbatim/reflections/, verbatim/opinions/ as appropriate. Use voice dictation or written prompts depending on the owner's preference.
   - Use structured prompts to elicit stories while preserving voice. Examples the agent should use: "Tell me about a childhood memory that shaped you," "Describe a time you failed and what you learned," "Tell the story of how you met [person]." Ask follow-ups for sensory details, dates, feelings, and dialogue.
   - Preserve verbatim text: do not rewrite the person's phrasing. You may insert structural headers (##) between natural breaks but never alter original words.
   - When the person references a person, place, or event, create or update cross-references (see step 7).

6. Summarize continuously
   - After each substantial verbatim entry, generate a summary file in summaries/ with standardized story card frontmatter (see [Story Cards](#story-cards-summary-frontmatter)): story_id, title, date_range, people, themes, emotions, stakes, turning_point, source, verification, memory_quality, sensitivity.
   - Maintain a master index summaries/stories/_index.json and update it with metadata (title, date, tags, people referenced, file path).
   - Use summaries for downstream searches and fast context loading; keep verbatim as the source of truth.
   - Update facts/timeline.md with any new events anchored by the story.

6b. Generate propositions — After populating facts/, mind/, and relationships/ content, extract atomic propositions per [core.md Retrieval Optimization](core.md#retrieval-optimization) guidelines. Store in propositions/ grouped by source file. Regenerate when source content changes significantly.

7. Build and maintain the relationships graph
   - As people appear in stories, create or update relationships/people.md using the standardized entry template: ID, name, relationship, time period, how they connect, key facts, consent status, and cross-references to files where they appear.
   - Assign stable kebab-case IDs to each person — these IDs are used in story card `people` arrays and timeline entries for cross-referencing.
   - Track consent status for each person (see [Privacy & Consent](#privacy--consent)). Flag `not-asked` entries for the pack owner to follow up before content is shared.
   - When ambiguity or conflicting relationships appear, log the contradiction in `meta/conflicts.md` and ask the pack owner to resolve.

8. Populate the mind taxonomy through guided interviews
   - Use the mind/ files as structured prompts. For each file (ontology.md, epistemology.md, values.md, identity.md, motivations.md, relational.md, preferences.md, skills.md, tensions.md) run a short interview designed to fill that category.
   - Example prompt for values.md: "What principles guide your major life choices? Describe two decisions where those values mattered." For epistemology.md: "How do you decide what to trust? Tell me about a time you changed your mind and why."
   - Store the person's answers as both verbatim (if spoken) and a distilled summary entry under mind/. If the owner prefers, allow iterative refinement: draft a summary, read it back, and ask for corrections.
   - After the core 9 files have substance, build mind/reasoning.md by identifying patterns: "When asked about X, how do you reason?" Draw from verbatim reflections and opinions to capture reasoning chains, not just positions.
   - Build mind/influences.md by asking: "Who shaped your thinking the most? What books changed you?" Cross-reference to verbatim content where influences are visible.
   - For each mind file with strong positions, prompt for strongest counterarguments under a `## Strongest Counterarguments` section.

9. Proactively identify gaps and suggest topics
   - Continuously run a gaps analysis: compare the schema's expected sections and common topic lists to the current content inventory.
   - Present the pack owner with concise gap prompts prioritized by value (e.g., missing childhood stories, unclear career transitions, absent values statements). Use checklists and suggested questions to close gaps.

10. Build privacy, consent, and legacy files
   - Early in pack development, create meta/privacy.md with sharing rules by access tier (what's public vs. friends vs. family vs. self).
   - Create meta/consent.md and populate it as people are added to the relationships registry. Flag `not-asked` entries for follow-up before sharing content.
   - When the pack owner signals readiness, guide them through legacy conversations: posthumous wishes, memorial preferences, executors, access rules, and any codeword/verification choices.
   - Draft LEGACY.md from their answers and have them confirm. Store final version under the pack root.

11. Build avatar modes
   - After enough stories and mind content are captured, draft presentation/modes.md with 2-3 initial modes based on the person's most common roles (e.g., parent, professional, friend).
   - Review with the pack owner: "Does this sound like you when you're talking to your kids vs. at work?" Iterate based on feedback.

12. Verification, conflicts, and provenance
   - Record the source for each piece of information in manifest.yaml and in individual file frontmatter or index files.
   - When contradictions arise between verbatim entries or facts, log them in `meta/conflicts.md` with a conflict ID, the conflicting sources, and notes. Do not resolve factual conflicts without explicit confirmation.
   - When the owner resolves a conflict, move the entry to `meta/resolutions.md` (append-only) with the decision, rationale, and date. Update all affected files.

13. Iterative improvement and maintenance
   - As new content arrives, repeat intake: save raw verbatim, generate summaries (with story card frontmatter), update relationships, augment mind taxonomy, update timeline, and re-run the gaps analysis.
   - Periodically review meta/conflicts.md — prompt the owner to resolve outstanding items.
   - Periodically (monthly or on-demand) generate a status summary that lists newly added content, unresolved conflicts, and remaining high-priority gaps.

14. Commit and document actions
   - Commit changes with descriptive messages and update the pack-level README.md and manifest sources.
   - Maintain session logs in meta/sessions.json for auditability.

Notes and principles

- Treat verbatim/ as the canonical source of the person's voice; summaries must never overwrite verbatim.
- The schema is your filing guide — decide where incoming content lives based on the taxonomy. If a new type is needed, create matching directories under verbatim/ and summaries/ and document them in the pack manifest.
- Record provenance for every file (see [Hydration Guide](../guides/hydration.md#source-provenance)) and never overwrite expert-verified content without reconfirmation.
- Use short, specific prompts that request a single story or fact at a time. Ask follow-ups for sensory detail, dates, and significance.

---

## Agent Extension (subtype: agent)

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
schema_version: "1.6"
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
├── verbatim/              ← OPTIONAL: Significant conversations or decisions worth preserving
│   └── decisions/         ← Key discussions that shaped the agent's behavior
│
├── summaries/             ← Distilled knowledge from accumulated experience
│   └── lessons/           ← Patterns learned: what works, what doesn't, failure post-mortems
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
| **Searchable (Tier 2)** | `mind/`, `relationships/`, `facts/`, `operational/`, `summaries/`, `presentation/modes.md` |
| **On-demand (Tier 3)** | `verbatim/`, `training/`, `meta/` |

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

*Schema version: 1.6*
*Last updated: 2026-03-10*
