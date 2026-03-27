# Hydration Guide

*The complete lifecycle for filling an ExpertPack with knowledge — from planning through population, retrieval optimization, validation, and maintenance. This guide is pack-type-agnostic; each method notes which pack types benefit most and where the approach differs. Read this before building any pack.*

---

## Philosophy

**The goal of hydration is not to document everything — it's to document what only this pack can provide.** An ExpertPack is valued by its esoteric knowledge (EK) ratio: the proportion of content that frontier LLMs cannot produce on their own (see [AXIOMS.md](../AXIOMS.md) and [core.md — EK Ratio](../schemas/core.md#esoteric-knowledge-ek-ratio)). Every hydration decision should be filtered through this lens: *Does the model already know this? If yes, minimize. If no, maximize.*

An ExpertPack is only as good as its sources. The best packs combine multiple population methods because no single method captures everything:

- **Documentation gives you the intended behavior.** What the product/process/person is *supposed* to do or be.
- **Technical artifacts give you the actual behavior.** What really happens, including undocumented features, edge cases, and inconsistencies.
- **Expert walkthroughs give you the "why."** Context, history, judgment calls, and tribal knowledge that never gets written down.
- **Observation and testing give you the gaps.** What the docs and experts forgot to mention because they're too close to it.
- **Feedback mining gives you the user reality.** What real people struggle with, not what designers assumed.

No method is inherently superior. The right mix depends on what source materials exist and what kind of pack you're building. Start with whatever you have access to and layer in additional methods as they become available.

---

## Planning a Hydration Campaign

Before diving into population, step back and plan. A well-planned hydration campaign prioritizes the highest-EK sources, avoids wasting effort on general knowledge, and sequences methods so each builds on what came before.

### Source Audit

Start by inventorying everything available:

- **Existing documentation** — docs sites, help articles, manuals, wikis, READMEs, blog posts
- **Technical artifacts** — source code, schemas, configs, CAD files, schematics
- **Visual materials** — screenshots, photos, diagrams, UI mockups
- **Video content** — tutorials, demos, training recordings, conference talks, interviews
- **Human experts** — who has tribal knowledge? Who built it? Who supports it daily?
- **Feedback channels** — support tickets, forum threads, app reviews, social media, bug trackers
- **Published works** (person packs) — books, articles, social media, interview transcripts

Don't evaluate yet — just list everything. You'll prioritize next.

### EK Potential Assessment

For each source, estimate where the esoteric knowledge lives:

| Source Type | Typical EK Density | Notes |
|------------|-------------------|-------|
| Expert tribal knowledge | Very High | Exists only in human heads — highest priority |
| Undocumented code behavior | High | Real behavior vs. documented behavior |
| Support tickets / user complaints | High | Real pain points the model can't invent |
| Internal decision records | High | The "why" behind choices |
| Video walkthroughs with narration | Medium–High | Expert explains "why" alongside "what" |
| Official documentation | Low–Medium | Highest GK contamination risk — probe aggressively |
| Generic technology explanations | Very Low | Skip or 1-line glossary entry |

Focus your campaign on the high-EK sources first. A 2-hour expert walkthrough will generate more pack value than a week of documentation ingestion.

### Method Sequencing by Pack Type

No single method is sufficient. Here's a practical ordering for building a new pack.

**EK triage applies at every step.** Regardless of the population method, every extracted fact passes through the [EK Triage pipeline](#ek-triage--the-default-hydration-filter) before filing. Methods that produce mostly EK (expert walkthroughs, conversational ingestion) can skip the blind probe step — but methods that produce mixed EK/GK (documentation, feedback mining) must probe.

#### Product Pack
1. **Documentation ingestion** — bootstrap the basics (~40-60% coverage)
2. **Technical artifact analysis** — add depth and discover the undocumented (~60-80%)
3. **Visual ingestion** — build interface docs from screenshots or photos (~70-85%)
4. **Expert walkthrough** — fill gaps, validate findings, capture "why" (~85-95%)
5. **Observation & testing** — quality gate, find remaining gaps (~95%+)
6. **Feedback mining** — populate troubleshooting and customer reality (ongoing)

#### Person Pack
1. **Documentation ingestion** — published works, online presence
2. **Conversational ingestion** — stories, beliefs, opinions (ongoing, primary method)
3. **Video ingestion** — talks, interviews, appearances
4. **Expert walkthrough** — the person validates and corrects
5. **Observation & testing** — roleplay conversations to find gaps

#### Process Pack
1. **Documentation ingestion** — SOPs, runbooks, compliance docs
2. **Expert walkthrough** — practitioners explain the reality vs. the docs
3. **Technical artifact analysis** — scripts, automation, monitoring configs
4. **Feedback mining** — incident reports, audit findings
5. **Observation & testing** — walk through each phase

The percentages are rough guides, not targets. Some packs will reach 90% from documentation alone (mature products with good docs). Others will need expert walkthroughs before documentation even makes sense (tribal-knowledge-heavy processes).

---

## Methods at a Glance

| Method | Best For | Applicability |
|--------|----------|---------------|
| [Documentation Ingestion](#documentation-ingestion) | Bootstrapping from existing written materials | Product ✅ Person ✅ Process ✅ |
| [Visual Ingestion](#visual-ingestion) | Capturing interfaces, layouts, physical designs | Product ✅ Person ✗ Process ◐ |
| [Video Ingestion](#video-ingestion) | Real usage, demonstrations, recorded knowledge | Product ✅ Person ✅ Process ✅ |
| [Technical Artifact Analysis](#technical-artifact-analysis) | Extracting knowledge from the product's internals | Product ✅ Person ✗ Process ◐ |
| [Expert Walkthrough](#expert-walkthrough) | Tribal knowledge, edge cases, "why" context | Product ✅ Person ✅ Process ✅ |
| [Conversational Ingestion](#conversational-ingestion) | Capturing voice, stories, opinions, reasoning | Product ◐ Person ✅ Process ◐ |
| [Observation & Testing](#observation--testing) | Validating completeness, finding gaps | Product ✅ Person ✅ Process ✅ |
| [Feedback Mining](#feedback-mining) | Real user problems, pain points, common questions | Product ✅ Person ✗ Process ✅ |

✅ = primary method for this pack type · ◐ = useful but secondary · ✗ = rarely applicable

---

## Documentation Ingestion

**What:** Harvesting existing written materials — docs sites, manuals, spec sheets, help articles, API references, SOPs, runbooks, blog posts, published writing, packaging text.

**Why it works:** Gets you to ~40-60% coverage quickly. Most products, processes, and people with public presence already have substantial written material.

**Why it's not enough:** Documentation is written for humans browsing, not AI reasoning. It's organized by the author's mental model, which may not match how questions are actually asked. It tends to cover the happy path and skip edge cases, error states, and "why" context.

### The Pipeline

1. **Inventory sources** — List all available documentation with URLs, formats, and scope. Create `sources/{doc-source}.md` for each.
2. **Prioritize** — Start with canonical/authoritative sources. Prefer official docs over community wikis over blog posts.
3. **Extract and restructure** — Don't copy-paste. Rewrite content into the pack's file structure: concepts go to `concepts/`, procedures go to `workflows/`, specs go to `specifications/`. Chunk by topic, not by source page.
4. **EK triage** — Documentation is the highest-GK population method. Run every extracted fact through the [EK Triage pipeline](#ek-triage--the-default-hydration-filter). Product-specific configurations and unique behaviors get full treatment; generic technology explanations get compressed to glossary entries or 1-line scaffolding. This step is mandatory during documentation ingestion.
5. **Add RAG-friendly headers** — Ensure every file has `##` headers that enable semantic chunking without losing technical meaning.
6. **Record provenance** — Every file gets frontmatter noting the source URL and extraction date.
7. **Track extraction status** — Update the source index with what's been extracted and what gaps remain.

### Strengths
- Fast bootstrapping — can process large doc sites quickly
- Structured input → structured output
- Easy to track completeness (page inventory vs. extraction status)

### Limitations
- Happy-path bias — docs rarely cover error states or edge cases
- Stale content — docs may lag behind the actual product/process
- Missing "why" — documentation tells you *what* but rarely *why* a decision was made
- Organizational mismatch — source docs may mix topics that should be separate in the pack

### Pack-Type Notes
- **Product:** Primary bootstrap method. Restructure from docs → concepts + workflows + specifications.
- **Person:** Ingest published writing (books, articles, blog posts, social media) into `verbatim/` and `summaries/`. Preserve the person's voice — don't rewrite their words.
- **Process:** Ingest SOPs, runbooks, checklists, compliance docs into `phases/` and `checklists/`.

---

## Visual Ingestion

**What:** Extracting knowledge from images — UI screenshots, product photos, schematics, diagrams, physical panel layouts, packaging, dashboards, architectural drawings.

**Why it works:** Visual sources capture spatial relationships and layout details that text descriptions struggle to convey. A single screenshot can yield a complete element-level inventory of an interface. For physical products, photos reveal component placement, labeling, and ergonomics.

**Key principle:** Images are **input**, not output. The pack stores only Markdown. The visual analysis produces rich text descriptions that fully capture what the image shows, so the consuming agent never needs the image.

### The Pipeline

1. **Capture** — Take screenshots or photos at consistent resolution with realistic sample data/state. For multi-state interfaces, capture each significant state separately.
2. **Analyze** — Use vision-capable AI to identify regions, elements, labels, and spatial relationships. Apply the region taxonomy, element type vocabulary, and spatial descriptors defined in the pack's schema.
3. **Enrich** — Have a domain expert review the AI-generated inventory. Correct misidentifications, add behavioral descriptions (what each element does, when it's available, conditional states), and fill in what vision can't infer.
4. **Connect** — Link interface elements to related workflows and concepts. Update `_index.md` and `entities.json`. Identify workflow gaps (elements with no corresponding workflow doc).
5. **Record provenance** — Frontmatter notes the source type, capture date, and who captured it.

### What to Capture

| State | When to Capture |
|-------|----------------|
| Default/initial state | As it appears on first load or access |
| Each dialog or overlay | When opened, with realistic content |
| Mode-dependent states | When available tools/options change by mode |
| Expanded/collapsed variants | When content differs significantly |
| Error or validation states | When error messages or warnings are visible |
| Empty vs. populated states | When the difference affects available actions |

### Strengths
- Visual ground truth — captures what actually exists, not what someone remembered to document
- Spatial precision — layout, grouping, and element relationships are explicit
- Catches undocumented UI — buttons, options, and states that never made it into docs

### Limitations
- Point-in-time — screenshots become stale when the UI changes
- Can't capture behavior — you see the element but not what happens when you click it
- Vision model accuracy — AI may misidentify elements or miss subtle UI details
- Expert enrichment required — the vision pass alone is typically ~60-70% complete

### Pack-Type Notes
- **Product:** Primary method for building `interfaces/` files. Works for software UIs, hardware control panels, physical product layouts, and dashboards.
- **Process:** Useful for documenting system dashboards, monitoring tools, or physical workspaces involved in the process.
- **Person:** Rarely applicable.

---

## Video Ingestion

**What:** Extracting knowledge from video — tutorials, demos, recorded walkthroughs, training sessions, conference talks, interviews, teardowns, assembly guides, podcasts with video.

**Why it works:** Video shows the product in actual use, captures real workflows with timing and sequence, and reveals UI details and physical interactions that static documentation omits. For person packs, video captures voice, mannerisms, and reasoning in context.

**Key principle:** The pack is the chunking layer. The consuming agent never processes video — it reads small, topic-scoped Markdown files. Chunking happens during pack *creation*, not consumption. Keep master video files intact; do not split them.

### The Pipeline

1. **Keep the master video intact.** The original recording stays as-is for reference and re-processing.
2. **Build a scene index.** Produce `sources/{video-slug}.md` — a timestamped inventory of what happens in the video. Each scene entry captures:
   - Timestamp range (MM:SS–MM:SS)
   - What's happening (action, screen shown, concept explained)
   - Entities referenced (features, UI elements, people, settings)
   - Target pack file (where this content will be extracted to)
3. **Extract pack artifacts from timestamp ranges.** For each scene, create or update the appropriate pack file:
   - UI walkthroughs → `workflows/` with timestamped steps
   - Screen/panel tours → `interfaces/` with layout details
   - Conceptual explanations → `concepts/`
   - Error demonstrations → `troubleshooting/errors/`
   - Tips and gotchas → `troubleshooting/common-mistakes/`
   - Stories and reflections → `verbatim/` (person packs)
4. **Add provenance frontmatter** with source type, video title, and timestamp reference.
5. **Update cross-references** — entities.json, _index.md files, and links between related content.
6. **Track extraction status** in the source index — which scenes are fully extracted, partial, or remaining.

### Chunking Strategy

- **Process by interaction moments**, not arbitrary time windows. A "moment" is a cluster of related actions: navigating to a screen, filling fields, clicking submit, observing the result.
- **Target 30–90 second segments** as a practical default. Short enough for accurate extraction, long enough for a complete interaction.
- **Extract frames at key moments** when visual detail matters — these feed into the visual ingestion pipeline for interface docs.
- **Transcribe narration** for conceptual content. The speaker's explanation of *why* something works is often more valuable than the actions themselves.

### Multiple Videos

When building from multiple videos:
- One `sources/{video-slug}.md` per video
- Use `sources/_index.md` to inventory all videos with their coverage areas
- Cross-reference when videos cover overlapping topics (note which has the better treatment)
- Deduplicate: extract from the best source, note the alternative in provenance

### Strengths
- Shows real usage — captures actual product behavior, not theoretical descriptions
- Reveals sequence and timing — how long things take, what order matters
- Captures narration — the expert's "why" explanation alongside the "what"
- Multi-sensory — voice, visuals, and behavior together

### Limitations
- Labor-intensive — building scene indexes and extracting takes significant effort
- Accuracy depends on model capability — transcription and scene understanding vary
- Stale quickly — product UIs and processes change
- Non-searchable without indexing — raw video has no value to the pack until processed

### Pack-Type Notes
- **Product:** Tutorials and demos are gold for workflows and interfaces. Process by interaction moments.
- **Person:** Talks, interviews, and appearances capture voice, reasoning, and personality. Extract into `verbatim/` preserving the person's words; generate `summaries/` for navigation.
- **Process:** Recorded procedures and training sessions map directly to `phases/` and `checklists/`.

---

## Technical Artifact Analysis

**What:** Analyzing the product's internals directly — source code, configuration files, CAD drawings, circuit schematics, chemical formulations, bills of materials, infrastructure-as-code, database schemas, API contracts.

**Why it works:** This is the single highest-fidelity population method for products with accessible internals. Technical artifacts reveal the *actual* behavior — including undocumented features, hidden options, edge cases, conditional logic, and inconsistencies between documentation and reality. For software products in particular, source code analysis has proven to be transformative: a codebase that took years to build can yield comprehensive interface documentation, business logic extraction, and behavioral specifications in a fraction of the time any other method requires.

### The Pipeline

1. **Gain access** — Obtain read access to the relevant artifacts. For source code: clone the repository. For hardware: obtain schematics, CAD files, or technical drawings. Respect IP and licensing constraints.
2. **Survey the landscape** — Before diving in, understand the structure. For a codebase: identify frameworks, architecture patterns, and file organization. Map out where UI definitions, business logic, data models, and configuration live.
3. **Identify extraction targets** — Determine what types of pack content each artifact type can yield:
   - View/template files → `interfaces/` (screen layouts, elements, states)
   - Business logic / controllers → `concepts/` (algorithms, rules, behaviors)
   - Configuration / constants → `specifications/` (supported values, limits, flags)
   - Data models / schemas → `concepts/` or `specifications/` (entity relationships, field definitions)
   - Error handling code → `troubleshooting/errors/` (error conditions, messages, recovery)
   - Test files → validation of documented behaviors; edge case discovery
4. **Extract systematically** — Process artifact groups in batches. For large codebases, work module-by-module. Create pack files that synthesize what the artifacts reveal, written for a non-technical reader (the consuming agent's user won't read code).
5. **Cross-reference with existing docs** — Technical artifacts often contradict or extend documentation. When they differ, the artifact is usually more current. Flag contradictions for expert review.
6. **Expert validation** — Technical extraction is high-fidelity but can miss *intent*. The code shows what happens; an expert explains why it was built that way and whether the behavior is correct or a known bug.

### What You Can Extract (by artifact type)

| Artifact Type | Yields | Example |
|---------------|--------|---------|
| UI view/template files | Interface docs — every element, state, conditional visibility | TypeScript view + viewmodel → complete screen inventory |
| Business logic modules | Concept docs — algorithms, rules, computation details | Classification engine → how colors are assigned |
| Constants / enums / config | Specification docs — valid values, limits, feature flags | Column flags enum → 33 supported column behaviors |
| API route definitions | Interface docs (API type) — endpoints, contracts, error codes | REST controllers → API specification |
| Database schemas | Entity relationship docs, data model specifications | Schema definitions → entity relationships |
| Error handling / validation | Troubleshooting docs — what triggers errors, exact messages | Validation logic → error catalog with conditions |
| Test suites | Behavioral validation — confirms edge cases, expected outputs | Unit tests → verified behavior specifications |
| CAD / schematic files | Physical interface docs — component placement, connections | Circuit schematic → hardware interface specification |
| Build / deploy configs | Infrastructure specifications, deployment requirements | Dockerfiles, IaC → deployment architecture |

### Strengths
- **Highest fidelity** — artifacts *are* the product; they can't be wrong about what exists
- **Discovers the undocumented** — keyboard shortcuts, hidden features, conditional behaviors, internal states that never made it into docs
- **Massive scale** — a codebase with 100+ views can yield 50+ interface docs in a day
- **Catches inconsistencies** — when the code does something different from the docs, you've found a bug or a doc gap
- **Repeatable** — when the product updates, re-run the extraction on changed files

### Limitations
- **Requires access** — not all products expose their internals; proprietary/closed-source products may not be analyzable
- **Requires technical literacy** — the builder agent needs to understand the relevant technology (programming language, framework, schematic notation)
- **Missing "why"** — code tells you *what* happens, not *why* it was designed that way. Pair with expert walkthroughs.
- **Missing user perspective** — code knows nothing about how users actually experience the product. A feature might exist in code but be invisible to users, or a technically simple feature might cause constant confusion.
- **Context window pressure** — large source files may need to be processed in chunks; the builder agent needs to synthesize across chunks without losing coherence
- **Not all artifacts are equally useful** — test infrastructure, build scripts, and vendored dependencies are usually noise. Focus on views, business logic, and configuration.

### Lessons Learned (from real pack building)

These observations come from applying source code extraction to a production software product pack:

1. **View + viewmodel pairs are the sweet spot for software.** If the codebase separates UI templates from their logic (MVC, MVVM, etc.), processing them as pairs yields complete interface docs — elements from the view, behavior from the viewmodel.
2. **Business logic modules are gold for concepts.** The classification engine, routing algorithm, or permission system — these become rich concept docs that capture algorithmic detail no documentation would ever include.
3. **Batch processing works.** Group related files and process them together in sub-agent batches. This keeps context focused and allows parallel processing.
4. **Cross-reference with existing pack content.** Don't create from scratch — enrich. If a concept doc already exists from documentation ingestion, the source code extraction should add detail and correct inaccuracies, not create a duplicate.
5. **Expert review is still essential.** Source code extraction found that a specific Query Dialog excluded "custom layers" from a feature that the Settings Panel allowed. Only the domain expert could confirm whether this was intentional or a bug. The code is always right about *what*; only humans know if it's *correct*.

### Pack-Type Notes
- **Product:** Primary power method. Software: source code, configs, schemas. Hardware: schematics, CAD, BOMs. Any product: technical specifications, formulations, compliance test results.
- **Process:** Useful when the process involves automated systems — extract from scripts, runbooks-as-code, CI/CD pipelines, monitoring configurations.
- **Person:** Rarely applicable unless the person's work product (code, designs, compositions) is itself being documented.

---

## Expert Walkthrough

**What:** Interactive sessions where a domain expert explains the product, process, or person's domain — demonstrating features, narrating decisions, revealing edge cases, and sharing tribal knowledge.

**Why it works:** Experts carry knowledge that exists nowhere else. The "why" behind design decisions, the workarounds for known issues, the gotchas that only surface after years of use, the customer complaints that shaped the product — none of this is in the docs or the code.

### The Pipeline

1. **Prepare** — Review existing pack content before the session. Identify specific gaps, ambiguities, and areas where documentation conflicts with technical artifacts. Come with targeted questions, not open-ended "tell me about the product."
2. **Guide, don't interview** — Use focused prompts that request specific knowledge:
   - "What do new users get wrong first?"
   - "Walk me through what happens when [specific scenario]."
   - "Why was it built this way instead of [alternative]?"
   - "Describe a time this broke and how you fixed it."
   - "What does the documentation get wrong or leave out?"
3. **Capture in real time** — File knowledge into the pack during or immediately after the session. Don't accumulate a backlog of notes to process later.
4. **Validate technical findings** — Use walkthroughs to confirm or correct what other methods found. Present contradictions between docs and code, ask the expert to resolve.
5. **Create a source index** — `sources/{session-slug}.md` with topics covered, key insights, and follow-up items.
6. **Identify the next session** — End each walkthrough by identifying what to cover next based on revealed gaps.

### Strengths
- **Irreplaceable knowledge source** — tribal knowledge, "why" context, and judgment calls exist only in experts' heads
- **Interactive** — you can drill into surprises, follow tangents, and resolve contradictions on the spot
- **Quality validation** — experts catch extraction errors from other methods
- **Relationship building** — the expert becomes invested in the pack's quality

### Limitations
- **Expert availability** — domain experts are usually busy; their time is the bottleneck
- **Memory bias** — experts may misremember details, especially historical decisions. Cross-reference with artifacts.
- **Curse of knowledge** — experts skip "obvious" things that users struggle with. Ask explicitly about basics.
- **Unstructured** — expert rambles need to be structured into the pack's taxonomy. The builder agent does the filing.

### Pack-Type Notes
- **Product:** Focus on edge cases, undocumented behavior, known bugs, and the "why" behind design decisions. Validate findings from documentation and technical artifact analysis.
- **Person:** The person *is* the expert. Story collection prompts, belief elicitation, and memory walks. Preserve their voice in `verbatim/`.
- **Process:** Focus on practitioners who execute the process daily. Ask about failure modes, workarounds, and the gap between the official process and what actually happens.

---

## Conversational Ingestion

**What:** Capturing knowledge through extended dialogue — interviews, story collection sessions, belief elicitation, podcast-style conversations. Distinct from expert walkthroughs in that the goal is capturing the person's *voice, perspective, and reasoning*, not just factual knowledge.

**Why it works:** Some knowledge is inherently conversational — personal stories, opinions, reasoning patterns, and beliefs emerge naturally in dialogue but resist structured extraction. This is the primary method for person packs and a valuable supplement for any pack type where human judgment and experience matter.

### The Pipeline

1. **Use targeted prompts** — One topic per turn. Request stories, not facts: "Tell me about a time when..." not "What is your opinion on..."
2. **Preserve voice** — Store the person's exact words in `verbatim/`. Add structural headers between natural breaks but never alter phrasing.
3. **Generate summaries** — After each verbatim capture, create a summary with standardized metadata (themes, people, emotions, stakes, turning point).
4. **Cross-reference** — As people, events, and concepts emerge, create or update relationship entries and timeline events.
5. **Elicit reasoning** — Don't just capture positions; capture *how* they think: "How did you decide that?" "What would change your mind?" "What's the strongest counterargument?"

### Strengths
- Captures voice and personality — irreplaceable for person packs
- Reveals reasoning patterns — not just what someone believes but how they think
- Natural and low-friction — most people find conversation easier than writing

### Limitations
- Time-intensive — both the conversation and the post-processing
- Memory distortion — stories shift over time; cross-reference when possible
- Requires skill — the interviewer/agent needs to know when to probe and when to let the person talk

### Pack-Type Notes
- **Person:** Primary method. Story collection, belief elicitation, memory walks, opinion capture.
- **Product:** Useful for capturing customer stories, sales objections, and support narratives for the `customers/` layer.
- **Process:** Useful for capturing practitioner experience and institutional memory about the process.

---

## Observation & Testing

**What:** Using or testing the product/process yourself, then documenting what you find. Includes scenario roleplay ("pretend to be a user asking questions"), hands-on testing, QA-style exploration, field observation, and gap analysis.

**Why it works:** Every other method tells you what the product *should* do or what experts *think* it does. Observation tells you what actually happens when someone encounters it fresh. This is the method that finds the gaps between documentation and reality.

### The Pipeline

1. **Design scenarios** — Create realistic user scenarios that exercise different areas of the pack. Vary the persona (beginner vs. expert), the task (simple lookup vs. complex workflow), and the emotional state (patient exploration vs. urgent troubleshooting).
2. **Execute and observe** — For product packs: actually use the product. For person packs: roleplay asking the "person" questions and see if the pack produces good answers. For process packs: walk through the process steps and note where instructions are unclear.
3. **Document gaps** — Every time the pack can't answer a question, gives an incomplete answer, or gives a wrong answer, record the gap with the exact scenario that triggered it.
4. **Fix immediately or track** — Small gaps (missing detail, unclear wording) can be fixed during the test. Larger gaps (missing concepts, wrong information) get tracked for follow-up.
5. **Re-test after fixes** — Verify that fixes actually solve the problem without introducing new issues.

### Strengths
- **Finds real gaps** — not theoretical gaps, but actual questions the pack can't handle
- **User perspective** — the builder agent temporarily becomes the consumer, seeing the pack through fresh eyes
- **Low cost** — no expert time required for the testing itself
- **Validates everything else** — confirms whether documentation, code extraction, and expert knowledge actually translated into useful pack content

### Limitations
- **Can't discover what it doesn't know to ask** — scenario design is limited by the tester's imagination. Combine with expert walkthroughs to surface scenarios you wouldn't have thought of.
- **Builder bias** — the person who built the pack may unconsciously test the happy path. Have someone else design scenarios when possible.

### Pack-Type Notes
- **Product:** Roleplay as different user personas asking questions. Test support scenarios, sales objections, troubleshooting flows. This is the "quality gate" before deploying a pack.
- **Person:** Roleplay as someone who wants to know about the person — ask biographical, philosophical, and opinion questions. See if the pack produces answers that sound like the real person.
- **Process:** Walk through each phase and checklist. Note where instructions are ambiguous, where prerequisites are missing, and where the process assumes knowledge that isn't documented.

---

## Feedback Mining

**What:** Extracting patterns from user and customer feedback — support tickets, forum threads, app reviews, warranty claims, return reasons, NPS comments, social media complaints, bug reports, feature requests.

**Why it works:** Feedback reveals the *user's* reality, which is often different from the *builder's* reality. The features users struggle with most are rarely the ones experts think are tricky. Feedback mining directly populates troubleshooting, FAQ, and customer reality sections.

### The Pipeline

1. **Collect** — Aggregate feedback from all available channels. Prioritize sources with volume (support tickets, reviews) over anecdotal reports.
2. **Categorize** — Group feedback by type: bug reports, confusion/usability, feature requests, praise, complaints, churn reasons.
3. **Extract patterns** — Identify recurring themes. A single complaint is anecdotal; ten complaints about the same thing are a pattern that needs a troubleshooting doc.
4. **EK triage** — Feedback mining produces a mix of EK (specific workarounds, product-specific gotchas) and GK (generic troubleshooting advice). Run extracted patterns through the [EK Triage pipeline](#ek-triage--the-default-hydration-filter). Specific error workarounds get full treatment; "have you tried restarting?" gets skipped.
5. **Create pack content** — Patterns become:
   - `troubleshooting/common-mistakes/` — things users repeatedly get wrong
   - `troubleshooting/errors/` — error messages users report
   - `faq/` — questions that keep getting asked
   - `customers/feedback.md` — honest capture of pain points and objections
   - `customers/segments.md` — enrichment with real usage patterns
5. **Don't sanitize** — Capture the real feedback, including harsh criticism. Agents that dodge weaknesses lose credibility.

### Strengths
- User-grounded — reflects real problems, not imagined ones
- Prioritizes naturally — high-frequency issues surface first
- Populates the hardest-to-fill sections — troubleshooting and customer reality

### Limitations
- Biased toward negatives — happy users rarely leave feedback
- Volume required — meaningful patterns need enough data points
- Noisy — not all feedback is actionable or relevant

### Pack-Type Notes
- **Product:** Primary method for `troubleshooting/`, `faq/`, and `customers/` sections. Mine support tickets, app reviews, forum posts.
- **Process:** Mine incident reports, post-mortems, audit findings, and compliance violations. These reveal where the process breaks in practice.
- **Person:** Rarely applicable directly, but feedback on a person's published works (book reviews, article comments) can inform `mind/` content.

---

## EK Triage — The Default Hydration Filter

Every fact extracted during hydration passes through the EK triage process before being filed into the pack. This is not optional — it is the default hydration workflow. EK triage ensures that pack content is dominated by knowledge the model cannot produce on its own, while preserving just enough general knowledge to serve as retrieval scaffolding.

### The Pipeline

Every extracted fact follows this flow:

```
Extract fact/knowledge from source
         ↓
   Heuristic check (see matrix below)
         ↓
   Clearly EK? ──→ YES: Full treatment (skip to Filing step)
         ↓ UNCERTAIN
   Blind probe: ask a frontier model the question cold (no pack context)
         ↓
   Model answers correctly? ──→ YES (GK): Compress to 1-line scaffolding
         ↓ NO
   Model wrong/refuses? ──→ Full EK treatment
         ↓ PARTIAL
   Keep as context, highlight the specific detail the model got wrong
```

### Blind Probing Protocol

When the heuristic check doesn't give a clear EK/GK signal:

1. **Generate a question** from the extracted fact that does NOT reveal the specific answer. Strip all numbers, values, and technical details — ask about the topic and let the model supply specifics.
2. **Ask one frontier model** the question with no pack context. A single cheap, fast model (e.g., GPT-4.1-mini, Gemini Flash) is sufficient during hydration triage — you're not measuring EK ratio precisely, just making a filing decision.
3. **Judge the response** against the ground truth fact:
   - **Model nails the specifics** → GK. Compress to scaffolding.
   - **Model gets the topic but misses the specific detail** → Partial. Keep as context, front-load the EK detail.
   - **Model is wrong, vague, or refuses** → EK. Full treatment.

**Cost:** ~3 API calls per fact (question gen + probe + judge) using cheap models ≈ $0.01/fact. For a 200-proposition pack, that's ~$2 — negligible compared to hydration compute.

**When to skip probing:** Expert walkthroughs and conversational ingestion are almost always EK. Don't waste API calls confirming what you already know — tribal knowledge from a domain expert is esoteric by definition. Save probing for documentation ingestion and feedback mining where the EK/GK mix is unpredictable.

### When to Skip Probing

Not all content requires blind probing. Some content types are EK by definition:

**Always EK (skip probing):**
- Person pack `verbatim/` — the person's own words are definitionally esoteric
- Person pack `mind/` — personal beliefs, reasoning patterns, tensions
- Person pack `relationships/` — private relationship context
- Person pack `presentation/` — speech patterns, voice, mannerisms
- Expert walkthrough output — tribal knowledge from domain experts
- Conversational ingestion — private stories, opinions, memories

**Always probe:**
- Documentation ingestion output — highest GK contamination risk
- Feedback mining output — mix of specific gotchas (EK) and generic advice (GK)
- Process pack `fundamentals/` — may overlap with widely-known domain knowledge
- Background context in any pack type — "what is Zigbee," "what is a trust," "what is UV curing"

**Probe selectively:**
- Process pack `phases/` — official process steps may be documented publicly; practitioner additions are EK
- Person pack `facts/` — biographical facts may be publicly known for public figures; private for private individuals
- Product pack `concepts/` — core concepts vs. undocumented behavior

### Filing by Classification

| Classification | Treatment | Purpose |
|---------------|-----------|---------|
| **EK** (model wrong/refuses) | Full treatment: dedicated file or section, lead summary, proposition extraction, careful structuring | This is the pack's core value |
| **Partial** (model vague/approximate) | Standard treatment: include in appropriate file, highlight the specific detail the model missed | The delta between "model knows roughly" and "pack knows precisely" is still valuable |
| **GK scaffolding** (model correct, but needed for retrieval) | 1-3 sentences providing context for nearby EK content. No dedicated file. Glossary entry or inline context only. | Ensures EK content is retrievable — user queries match on GK terms, which lead to EK answers |
| **GK unnecessary** (model correct, no EK depends on it) | Skip entirely. Do not file. | Adding this content would dilute EK ratio without improving retrieval |

### Why Not Exclude GK Entirely?

GK serves three essential roles even in a high-EK pack:

1. **Query scaffolding** — Users ask questions using general vocabulary. *"How does Zigbee work in Home Assistant?"* matches on the GK Zigbee explanation, which contains the EK gotcha about coordinator firmware bugs. Remove the GK and the EK becomes an orphan with no retrieval path.

2. **Context for EK** — Some EK is unintelligible without 1-2 sentences of GK context. *"SiLabs coordinators drop Aqara sensors after 48h due to source routing table overflow"* needs a brief mention of what a coordinator does. The GK is scaffolding, not content.

3. **Model reliability backstop** — Models are mostly right on GK, but not always. If the pack covers a domain end-to-end and the agent answers from the pack, gaps where "the model should know this" become failure points when the model doesn't.

The solution is not to exclude GK but to **compress it ruthlessly** — enough to serve as scaffolding, never enough to become the pack's substance.

### Hydration Priority Matrix

| Source Type | Typical EK Level | Hydration Priority | Rationale |
|------------|-----------------|-------------------|-----------|
| Expert tribal knowledge | Very High | **Extract first, maximum effort** | Exists only in human heads; highest risk of loss |
| Undocumented code behavior | High | **Extract early, full treatment** | Real behavior vs. documented behavior; models don't know the delta |
| Support tickets / gotchas | High | **High priority** | Real user pain points; models hallucinate workarounds |
| Internal decision records ("why") | High | **When available, full treatment** | Models can guess "what" but not "why this way" |
| Product-specific edge cases | Medium–High | **Medium-high** | Interaction quirks, version-specific behavior |
| Expert-validated corrections | Medium–High | **Medium-high** | Where docs are wrong; models trained on wrong docs repeat the error |
| Domain-specific configuration | Medium | **Standard** | Settings, thresholds, compatibility matrices |
| Official docs (unique features) | Medium | **Standard** | Features specific to this product |
| Official docs (common patterns) | Low | **Light touch** | Well-known patterns applied to this product |
| Generic technology explanations | Very Low | **Skip or one-line glossary** | Models already know this |
| Common best practices | Very Low | **Skip or brief mention** | Widely documented across the internet |
| Person interviews / story collection | Very High | **Maximum effort — this IS the pack** | Private memories, opinions, voice patterns — definitionally esoteric |
| Published personal writing (blog, books) | High | **Full treatment** | Original thought and voice, even if publicly accessible |
| Person's biographical facts (dates, places, career) | Medium | **Standard** | Some is verifiable; what makes it EK is the personal context and connections |
| Person's commonly-known public positions | Low | **Light touch** | If a famous person's views are widely known, models may already have them |
| SOPs / runbooks / compliance docs | Medium | **Standard with probing** | Official process may be in training data; the gap between official and actual is EK |
| Practitioner gotchas / failure modes | Very High | **Extract first** | Learned by experience, rarely documented |
| Post-mortems / incident reports | High | **Full treatment** | Specific failures, causes, and fixes — models can't invent these |

### EK Indicators by Method

Each population method has characteristic EK signals:

**Documentation Ingestion:**
- 🟢 High EK: Product-specific configuration, unique feature behavior, version-specific changes
- 🔴 Low EK: Generic architecture overviews, technology primers, standard API patterns

**Technical Artifact Analysis:**
- 🟢 High EK: Undocumented flags, conditional behavior, internal algorithms, error conditions
- 🔴 Low EK: Standard framework patterns, boilerplate, well-known library usage

**Expert Walkthrough:**
- 🟢 High EK: Almost everything — tribal knowledge is esoteric by definition
- 🔴 Low EK: When the expert explains basics they think you need (ask them to skip to the non-obvious)

**Feedback Mining:**
- 🟢 High EK: Specific error workarounds, product-specific gotchas, undocumented limitations
- 🔴 Low EK: Generic troubleshooting advice ("have you tried restarting?")

**Conversational Ingestion (Person packs):**
- 🟢 High EK: Personal stories, private opinions, reasoning patterns, family history, voice/speech patterns — almost all EK
- 🟢 High EK: Unpublished beliefs, tensions, contradictions the person acknowledges
- 🔴 Low EK: When the person restates widely-known facts or common positions
- 🔴 Low EK: For famous/public figures, well-known biographical facts and documented positions

**Observation & Testing (Process packs):**
- 🟢 High EK: Where the actual process diverges from the documented process
- 🟢 High EK: Timing realities, seasonal constraints, regional variations
- 🔴 Low EK: Standard project management practices, generic safety protocols

### The Common-Knowledge Trap

The most common hydration mistake is spending equal effort on general and esoteric knowledge. A 15KB file explaining how Zigbee mesh networking works adds zero value — the model knows this. A 2KB file documenting the specific firmware bug in SiLabs coordinators that drops Aqara sensors after exactly 48 hours is worth more than the entire Zigbee primer.

**Rule of thumb:** If you find yourself writing content that reads like a Wikipedia article, stop. Either the model already knows it, or you're writing for the wrong audience. ExpertPacks are for practitioners who already understand the basics — they need the knowledge that *isn't* on Wikipedia.

---

## Building the Retrieval Layer

Hydrating content files is only half the job. A pack full of well-structured Markdown is still at the mercy of the retrieval system — and most RAG systems are dumb about structured content. This section covers the retrieval optimization layers that bridge the gap between how you *organized* the knowledge and how the consuming agent *finds* it.

These layers are not optional nice-to-haves. In eval experiments on a real product pack, retrieval optimization produced the single largest quality improvement of any change — larger than model upgrades, content edits, or RAG configuration tuning.

### Lead Summaries

Add a 1–3 sentence blockquote at the very top of high-traffic content files that directly answers the most likely query.

```markdown
# User Roles

> **Lead summary:** EZT Designer supports three user roles: Owner, Editor, and Viewer. Owners can manage team members and billing. Editors can create and modify territories but cannot change team settings. There is no "Admin" role — Owner is the highest permission level.

## What It Is
...
```

**Why this matters:** RAG chunkers split files from the top. If the first 400 tokens are a table of contents or general introduction, the most relevant chunk ranks lower than it should. Lead summaries front-load the critical facts — including anti-hallucination "NOT" facts and common gotchas — into the highest-ranked chunk position.

**Where to focus:** Start with the ~15 most-retrieved files (identified via eval results or support ticket analysis). Not every file needs one — prioritize files that answer high-frequency questions.

### Summaries Directory (`summaries/`)

Section-level summaries that enable hierarchical retrieval. One summary file per content section, each 1–3KB of dense bullet points with cross-references to detail files.

```markdown
# Concepts — Summary

Dense bullet-point summary of all concepts in this section.

## Key Topics
- **Territories** — Named geographic regions assigned to reps. See [territories.md](../concepts/territories.md)
- **Routing Optimizer** — TSP solver using genetic algorithm, population 32. See [routing.md](../concepts/routing.md)
- **Data Sources** — Supports Excel, Dynamics 365, Power Platform, SQL Azure. See [data-sources.md](../concepts/data-sources.md)
...
```

**Why summaries matter:** Without summaries, broad questions like "what can this product do?" compete against hundreds of fine-grained files with mediocre relevance. A summary file matches with high relevance and provides a complete broad answer. Detail files then handle follow-ups. This is the RAPTOR pattern — recursive summarization into a retrieval tree.

**Generation rules:**
- Summaries are DERIVED from content files — read all files in a section before writing
- Include cross-references to source files so agents can drill down
- Regenerate when source content changes significantly

### Propositions Directory (`propositions/`)

Atomic factual statements extracted from content files. Each proposition captures exactly ONE fact and is self-contained — readable without any surrounding context.

```markdown
# Concepts — Propositions

### territories.md
- EZT Designer organizes geographic areas into hierarchical territories
- Territories can be defined by postal codes, counties, states, or countries
- A territory can only be assigned to one rep at a time
- Territories support custom color coding based on any numeric metric

### routing-optimizer.md
- The route optimizer uses a TSP (Traveling Salesman Problem) genetic algorithm
- Default population size is 32 candidates per generation
- Maximum stops per route is 150
...
```

**Why propositions matter:** Prose paragraphs contain multiple facts mixed with explanations and transitions. RAG retrieval against prose returns the whole paragraph, only part of which is relevant. Propositions isolate individual facts — each matches precisely or not at all.

**Extraction rules:**
- Each proposition = one fact (not compound statements)
- Self-contained — no "it" or "this" references to surrounding context
- 5–20 propositions per source file, depending on density
- Do NOT invent facts — extract only what the source states
- Regenerate when source content changes

### Glossary (`glossary.md`)

Maps common user vocabulary to precise technical terms. This bridges the gap between how users describe their problems and how the pack documents solutions.

```markdown
# EZT Designer — Glossary

## Territory Terms

| Term | Definition | Common User Language |
|------|-----------|---------------------|
| **Territory** | Named geographic region assigned to a rep | "area", "zone", "region", "turf" |
| **Locked territory** | Territory with editing disabled to prevent changes | "stuck ZIP codes", "can't move", "frozen" |
| **Alignment** | The complete set of territory assignments | "territory map", "the layout", "assignments" |
```

**Why a glossary matters:** Users say "stuck ZIP codes" when the pack documents "locked territories." Without a vocabulary bridge, RAG retrieval fails because the query terms don't match the content terms. A glossary gives RAG an explicit mapping to match against.

**Guidelines:**
- Include the "Common User Language" column — this is what makes glossaries effective
- Keep definitions concise (1-2 sentences)
- Add the glossary to manifest `always` tier (Tier 1) — it's small, high-value, and helps every query
- Update when eval failures reveal vocabulary gaps

### Schema-Aware Chunking

**This is the single highest-impact retrieval optimization.** In eval experiments on a real product pack, schema-aware chunking produced +9.4% correctness, -52% input tokens, and -60% hallucination rate — the largest improvement from any single change, bigger than model upgrades or content edits.

#### Authoring for Retrieval

Author every content file to the 400–800 token target (1,500 token ceiling). These files become self-contained retrieval units. Any standard RAG chunker will pass them through intact.

This preserves:
- Lead summaries attached to titles
- Proposition groups
- Glossary tables
- `<!-- refresh -->` metadata
- Complete `##` sections

**Evidence: What Works and What Doesn't**

These results come from 6 controlled experiments on a real product pack (EZT Designer, 204 source files), each changing one variable at a time:

| Change | Correctness | Hallucination | Tokens | Verdict |
|--------|------------|---------------|--------|---------|
| **Baseline** (generic chunks) | 79.0% | 10.0% | 4,372 | Starting point |
| File splitting alone | 76.9% (-2.1%) | 12.0% (+2%) | 3,686 | ❌ Lost context |
| Prose compaction (~40% denser) | 76.8% (-2.2%) | 14.0% (+4%) | 3,721 | ❌ Harder to parse |
| Summaries + propositions + splits | 78.7% (-0.3%) | 6.0% (-4%) | 3,733 | ✅ First quality win |
| **Schema-aware chunking** | **88.4%** (+9.4%) | **4.0%** (-6%) | **2,111** (-52%) | 🔥 Best single change |

**Key lessons:**
- **Splitting alone loses context.** Sub-files miss the surrounding context that helped the model understand relationships. Don't split without adding retrieval layers.
- **Compaction hurts.** Removing examples and shortening explanations makes text *harder* for models to parse. The "redundant" content was serving as reasoning scaffolding.
- **Three layers together work.** Summaries + propositions + splits compensate for each other: summaries recover broad context, propositions enable precise fact retrieval, splits provide focused detail.
- **Schema-aware chunking is transformative.** Pre-computing semantically coherent chunks means every retrieved result is self-contained and relevant. The insight: **retrieval precision > model capability for factual correctness.** A weaker model with precise chunks outperforms a stronger model with sloppy chunks.

#### Integration

For Schema 2.5+ packs, point your RAG system at the pack root. Author files to the 400–800 token target so they remain intact during indexing.

```bash
# Configure OpenClaw to index the pack directly
# In openclaw.json:
{
  "memorySearch": {
    "extraPaths": ["path/to/pack"],
    "chunking": { "tokens": 1000, "overlap": 0 },
    "query": {
      "hybrid": {
        "mmr": { "enabled": true, "lambda": 0.7 },
        "temporalDecay": { "enabled": false }
      }
    }
  }
}
```

- **Overlap 0** — chunks are already semantically complete
- **MMR enabled** — prevents near-duplicate proposition/summary/content chunks from crowding results
- **Temporal decay off** — pack knowledge doesn't expire by file modification date

### The Three-Layer System

Lead summaries, summaries, propositions, glossary, and schema-aware chunking work as a system. Each layer handles what the others can't:

| Layer | Handles | Without It |
|-------|---------|-----------|
| **Lead summaries** | Front-loads answers into the highest-ranked chunk position | First chunk is preamble, not the answer |
| **Summaries** | Broad questions ("what can it do?") | Every query competes against hundreds of fine-grained files |
| **Propositions** | Specific factual questions ("what's the max?") | Model must extract facts from prose paragraphs |
| **Glossary** | Vocabulary bridging between user language and pack terms | Queries using informal language miss relevant content |
| **Small self-contained files** | Preserves all structural conventions during retrieval | Large files get split by generic chunkers |

Don't build one layer and skip the rest. The three-layer approach (summaries + propositions + split/chunked content files) consistently outperforms any single layer alone.

### Retrieval Anti-Patterns

Based on eval experiments, avoid these common mistakes:

- **Do NOT compact or compress prose to save tokens.** Denser text is harder for models to parse. Examples, explanations, and context that feel redundant to a human serve as reasoning scaffolding for a model. Content quality was never the bottleneck — retrieval precision was.
- **Do NOT split files without adding retrieval layers.** Splitting alone degrades quality. Each fragment loses the surrounding context that made the unified file useful. Always pair splitting with summaries and propositions.
- **Do NOT sacrifice content readability for token efficiency.** Readable prose with `##` headers and concrete examples outperforms tightly compressed bullet lists. Token count at retrieval time matters less than match quality and reasoning support.

---

## Validation

Hydration isn't done until you've measured the result. Eval-driven improvement is not a post-launch activity — it's the final phase of hydration.

### Running Evals

Build an eval set of 30+ questions covering the pack's key scenarios. Include:

- **Basic retrieval** — "What is X?" (single file lookup)
- **Multi-file synthesis** — "How does X relate to Y?" (requires combining information)
- **Troubleshooting** — "X isn't working" (diagnostic reasoning)
- **Out-of-scope** — Questions the agent should decline (tests refusal)
- **Adversarial** — Questions designed to induce hallucination

Run the eval set against the deployed pack + model configuration. Save results as a baseline. See the [eval schema](../schemas/eval.md) for the full format and methodology.

### Content Gap Analysis

Eval failures point directly to hydration gaps:

| Failure Pattern | Likely Cause | Hydration Fix |
|----------------|-------------|---------------|
| Wrong answer on a covered topic | Retrieval miss — content exists but wasn't found | Add lead summary, improve `##` headers, check chunk boundaries |
| Confident wrong answer | Hallucination — model fabricating | Add anti-hallucination facts to relevant files, add propositions |
| Incomplete answer | Content gap or partial retrieval | Check if content exists; add propositions for precise retrieval |
| Vocabulary mismatch | User terms ≠ pack terms | Update glossary with user language mappings |

### EK Ratio Measurement

After hydration, measure the pack's EK ratio via proposition-level blind probing. This tells you what proportion of the pack's content is genuinely esoteric — knowledge the model can't produce alone. See [core.md — EK Ratio](../schemas/core.md#esoteric-knowledge-ek-ratio) for the full measurement protocol.

Target EK ratios:
- **0.80+** — Exceptional. Almost entirely esoteric knowledge.
- **0.60–0.79** — Strong. Look for GK that can be trimmed.
- **0.40–0.59** — Mixed. Review low-EK sections.
- **< 0.40** — Needs major rework. Refocus on tribal/undocumented knowledge.

### The Three Eval Dimensions

Three independent variables affect pack-powered response quality. When evaluating, vary one at a time:

1. **Structure** (highest leverage) — the pack's content, file organization, chunking, retrieval layers. Structural improvements compound across every model and every configuration.
2. **Agent Training** (second) — system prompts, SOUL.md, scope rules. Transferable across models.
3. **Model** (third) — the LLM processing queries. Expensive and vendor-dependent. Matters most for instruction following (refusal), less for factual correctness when retrieval is precise.

---

## Source Provenance

Every file created by any population method must include frontmatter documenting where the content came from. This enables re-ingestion when sources update and traceability when content is questioned.

```yaml
---
sources:
  - type: documentation
    url: "https://docs.example.com/feature"
    ingested: "2026-01-15"
  - type: source-code
    repo: "product-repo"
    files: ["src/views/settings.ts", "src/viewmodels/settings.ts"]
    analyzed: "2026-02-27"
  - type: expert-walkthrough
    contributor: "Jane Smith"
    date: "2026-02-28"
  - type: screenshot-ingestion
    screen: "settings-panel"
    captured: "2026-02-24"
    captured_by: "Jane Smith"
  - type: video
    title: "Product Overview Tutorial"
    ref: "03:12-04:05"
  - type: interview
    with: "John Doe"
    date: "2026-03-01"
  - type: feedback-analysis
    source: "support-tickets-q1-2026"
    analyzed: "2026-03-15"
  - type: observation
    scenario: "new-user-onboarding-test"
    date: "2026-03-20"
---
```

For detailed source tracking across a body of source materials, use `sources/{source}.md` index files as described in the pack type schemas.

---

## Maintenance

Hydration is not a one-time event. Packs need ongoing maintenance as sources update, models evolve, and users reveal gaps.

### Time Variance and Freshness

Not all facts have the same shelf life. A string sizing formula is permanent; a panel's price per watt is stale within months. During hydration, annotate time-variant facts with inline refresh metadata:

```markdown
The Tesla Powerwall 3 is priced at approximately $10,500-14,000 installed.

<!-- refresh
  decay: volatile
  as_of: 2026-Q1
  source: https://www.energysage.com/solar/battery-storage/
  method: "Search 'Tesla Powerwall 3 installed cost [current year]'"
-->
```

**The critical rule: refresh instructions travel with the data.** When a consuming agent encounters a volatile fact, it needs the refresh method right there — not a pointer to a freshness guide it may not load. See [core.md — Time Variance](../schemas/core.md#time-variance) for the full annotation format and decay categories.

Maintain a supplementary `freshness.md` at the pack root for maintainers reviewing overall freshness at a glance.

### Re-Hydration When Sources Update

When the product ships a new version, documentation is revised, or new expert knowledge becomes available:

1. **Identify affected files** — use source provenance frontmatter to trace which pack files came from the updated source
2. **Re-extract** — run the relevant population method on the updated source
3. **EK triage the delta** — new content passes through the same EK filter as initial hydration
4. **Regenerate retrieval layers** — update summaries, propositions, and re-run the schema-aware chunker
5. **Re-run evals** — verify that updates improved (or at least didn't degrade) quality

### EK Ratio Decay

EK ratio naturally **decreases** over time as frontier models absorb more knowledge into their weights. What's esoteric today may become general knowledge in the next training run. This means:

- **Re-measure quarterly** or after major model releases
- **Packs need deepening, not just maintenance.** As models absorb the surface layer, the pack's value depends increasingly on its deepest, most tribal content.
- **Track measurements over time** — declining EK ratio is a signal to invest in deeper expert walkthroughs, undocumented behavior analysis, and edge case documentation.

### Research Coverage Tracking

Every pack should include a `sources/_coverage.md` that honestly documents what knowledge sources were checked, what was extracted, and what remains untouched. This makes the pack's depth and limitations transparent. See [core.md — Research Coverage](../schemas/core.md#research-coverage-sources_coveragemd) for the format and status key.

Update coverage status as you deepen the pack: ⬜ Identified → 🟡 Sampled → ✅ Mined. Known gaps should be specific and actionable — "More research needed" is useless; "Installer forum threads about firmware failure modes not yet mined" tells the next hydrator exactly what to do.

---

*Guide version: 1.0*
*Last updated: 2026-03-13*
