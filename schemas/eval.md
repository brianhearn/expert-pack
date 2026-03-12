# ExpertPack Evaluation Schema

*Framework for measuring and improving ExpertPack quality across all pack types. Defines how any pack can assess its retrieval accuracy, response quality, token efficiency, and structural health.*

---

## Purpose

An ExpertPack without evaluation is an opinion. This schema defines a standard way to:

1. **Measure response quality** — Is the pack producing correct, grounded answers?
2. **Measure efficiency** — How many tokens and how much time does it cost?
3. **Measure structural health** — Does the pack follow schema conventions?
4. **Track improvement** — Compare before/after when changes are made

Every pack type (person, product, process) uses the same evaluation framework. What changes is the content of the eval set, not the measurement methodology.

---

## Directory Structure

```
packs/{pack-slug}/
├── eval/                          ← Evaluation artifacts
│   ├── _index.md                  ← Overview of eval coverage and status
│   ├── questions.yaml             ← The eval set: questions + expected answers
│   ├── results/                   ← Scored eval run outputs
│   │   └── {YYYY-MM-DD}-{label}.yaml
│   └── baselines/                 ← Saved baseline snapshots for comparison
│       └── {YYYY-MM-DD}-{label}.yaml
```

**Context tier:** Tier 3 (on-demand). Eval artifacts are never loaded during normal pack consumption — only during evaluation and improvement workflows.

---

## The Eval Set (questions.yaml)

The core artifact. A list of question-answer pairs with metadata that enables automated and human evaluation.

### Format

```yaml
# eval/questions.yaml
version: "1.0"
pack_slug: "{pack-slug}"
pack_type: "{person|product|process}"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"

questions:
  - id: "q001"
    question: "How do I create a new territory from scratch?"
    category: "workflow"           # See category taxonomy below
    difficulty: "basic"            # basic | intermediate | advanced
    expected_answer: |
      Concise correct answer that a knowledgeable agent should produce.
      Include key facts that MUST appear in a correct response.
    required_facts:
      - "Must mention creating a project first"
      - "Must reference the markup tools"
      - "Should mention saving/publishing"
    expected_sources:
      - "workflows/create-territory.md"
      - "concepts/territories.md"
    anti_hallucination:
      - "Should NOT claim you can import territories from Excel directly"
    tags: ["getting-started", "territories"]

  - id: "q002"
    question: "What did grandpa think about the space program?"
    category: "recall"
    difficulty: "intermediate"
    expected_answer: |
      Answer should reflect the person's actual recorded views,
      using their voice/tone if the pack has presentation data.
    required_facts:
      - "Must reference specific views captured in the pack"
    expected_sources:
      - "mind/science-technology/space-program.md"
    anti_hallucination:
      - "Should NOT invent opinions not in the pack"
    tags: ["beliefs", "science"]
```

### Question Categories

Categories are pack-type flexible. Use what applies:

| Category | Applies To | What It Tests |
|----------|-----------|---------------|
| `concept` | All | "What is X?" — retrieval of explanatory content |
| `workflow` | Product, Process | "How do I X?" — retrieval of procedural steps |
| `recall` | Person | "What did they think/say about X?" — memory retrieval |
| `troubleshoot` | Product | "X isn't working" — diagnostic reasoning |
| `factual` | All | "When/where/who?" — precise fact retrieval |
| `opinion` | Person | "What was their view on X?" — belief/value retrieval |
| `decision` | Product, Process | "Why did we/they choose X?" — decision record retrieval |
| `comparison` | All | "What's the difference between X and Y?" — multi-source synthesis |
| `edge-case` | All | Unusual, ambiguous, or boundary questions |
| `out-of-scope` | All | Questions the pack should NOT answer (tests refusal) |

### Difficulty Levels

| Level | Definition |
|-------|-----------|
| `basic` | Answer is in a single, obvious file. Direct retrieval. |
| `intermediate` | Answer requires synthesizing 2-3 files or navigating cross-references. |
| `advanced` | Answer requires deep reasoning, resolving ambiguity, or combining distant content. |

### Building an Eval Set

**Minimum viable eval set:** 30 questions (10 basic, 12 intermediate, 8 advanced), covering at least 3 categories relevant to the pack type.

**Sources for questions:**
- Real user questions (support tickets, chat logs, interview transcripts)
- Schema-derived coverage (one question per major section)
- Edge cases and known failure modes
- Out-of-scope questions (does the agent correctly decline?)
- Adversarial questions (attempts to induce hallucination)

**Guidelines:**
- Include at least 5 `out-of-scope` questions — knowing what NOT to answer is as important as knowing what to answer
- `anti_hallucination` entries are critical — they define specific wrong answers that indicate the model is fabricating
- `expected_sources` enables retrieval quality measurement independent of generation quality
- Update the eval set as the pack grows; a stale eval set gives false confidence

---

## Metrics

### Response Quality Metrics

| Metric | What It Measures | How to Score |
|--------|-----------------|-------------|
| **Correctness** | Does the answer contain the required facts? | % of `required_facts` present in the response |
| **Groundedness** | Is every claim traceable to pack content? | % of response claims backed by pack files |
| **Hallucination Rate** | Does the response contain fabricated information? | % of responses containing `anti_hallucination` violations |
| **Refusal Accuracy** | Does the agent correctly decline out-of-scope questions? | % of `out-of-scope` questions properly declined |
| **Completeness** | Does the answer cover all relevant aspects? | Subjective 1-5 scale or % of expected points covered |
| **Voice Fidelity** | Does the response match the pack's presentation style? | Person packs: does it sound like the person? (subjective 1-5) |

### Retrieval Quality Metrics

| Metric | What It Measures | How to Score |
|--------|-----------------|-------------|
| **Hit Rate** | Does retrieval return the expected source files? | % of questions where `expected_sources` appear in retrieved chunks |
| **Precision@K** | Of top K retrieved chunks, how many are relevant? | Relevant chunks / K (typically K=5) |
| **Retrieval Latency** | Time from query to chunks returned | Milliseconds |

### Efficiency Metrics

| Metric | What It Measures | How to Score |
|--------|-----------------|-------------|
| **Input Tokens** | Tokens sent to the model (prompt + context) | Count per query |
| **Output Tokens** | Tokens generated by the model | Count per query |
| **Total Tokens** | Input + Output | Count per query |
| **Cost per Query** | Dollar cost of the API call | Calculated from model pricing |
| **End-to-End Latency** | Total time from question to answer delivered | Milliseconds |
| **Time to First Token** | Time until the model starts generating | Milliseconds |

### Esoteric Knowledge Metrics

| Metric | What It Measures | How to Score |
|--------|-----------------|-------------|
| **EK Ratio** | Proportion of pack propositions containing esoteric knowledge | See [core.md — EK Ratio](core.md#esoteric-knowledge-ek-ratio) for full methodology |
| **EK by Section** | Which sections contribute most/least esoteric knowledge | EK ratio calculated per `propositions/{section}.md` file |
| **GK Bloat** | How much pack space is consumed by general knowledge | Total tokens in low-EK files / total pack tokens |

**Methodology:** EK ratio is measured via proposition-level blind probing — asking frontier models each proposition as a question without pack context. See [core.md — Measuring EK Ratio](core.md#measuring-ek-ratio) for the complete protocol.

**Including EK in eval runs:** Add an `ek_ratio` block to results files:

```yaml
ek_ratio:
  value: 0.72
  models_probed: ["gpt-5", "claude-opus-4", "gemini-2"]
  propositions_total: 142
  ek_count: 83
  partial_count: 21
  gk_count: 38
  by_section:
    troubleshooting: 0.89
    process/gotchas: 0.84
    concepts/esphome: 0.78
    concepts/core-architecture: 0.21
    overview: 0.15
```

**Actionable insights from EK metrics:**
- **Low EK sections** (< 0.30) are candidates for compaction — compress to glossary entries or brief context
- **High EK sections** (> 0.80) are the pack's core value — invest in deeper hydration, better propositions, and lead summaries
- **GK bloat** above 30% suggests the pack needs an EK-focused pruning pass
- **EK ratio trending down** between measurements means model training data is absorbing the pack's domain — time to deepen with more tribal knowledge

### Measuring EK Across Pack Types

The standard EK measurement protocol uses `propositions/` files — atomic factual statements that can be converted to probe questions. This works directly for product and process packs. Person packs require adaptation:

**Product packs:** Standard protocol. Extract propositions from concepts, workflows, troubleshooting, specifications. Probe with factual questions.

**Process packs:** Standard protocol with adjustment. Extract propositions from phases, decisions, gotchas, regulations. Some process propositions are procedural ("Phase 3 requires a structural inspection before framing begins") — convert these to "what happens after X?" or "what is required before Y?" style questions.

**Person packs:** Adapted protocol. Person packs store knowledge in `verbatim/`, `mind/`, `facts/`, and `relationships/` — not traditional propositions. To measure EK:
1. Extract testable claims from `facts/` (biographical data) and `mind/` (beliefs, positions) — these behave like propositions
2. For `verbatim/` content (stories, reflections), extract the unique factual claims embedded in narratives ("Brian watched the Apollo 11 launch from a sailboat named Dulcinea")
3. Skip `presentation/` (speech patterns, voice) — these are inherently esoteric and unmeasurable via blind probing
4. For public figures, EK ratio of `facts/` and known positions may be lower; for private individuals, nearly everything is EK
5. Report person-pack EK ratio with a note: "EK ratio reflects `facts/` and `mind/` content only; `verbatim/` and `presentation/` are EK by definition and excluded from measurement"

**Composite packs:** Measure each sub-pack independently and report per-sub-pack EK ratios alongside the composite ratio.

### Pack Health Metrics (Structural)

| Metric | What It Measures | How to Score |
|--------|-----------------|-------------|
| **Schema Conformance** | Do files follow size, naming, header conventions? | % of files passing validation |
| **Section Coverage** | What % of expected schema sections are populated? | Populated sections / expected sections |
| **Index Completeness** | Do all directories have current `_index.md` files? | % of content directories with up-to-date indexes |
| **Cross-Reference Integrity** | Do internal markdown links resolve? | % of links that point to existing files |
| **Freshness** | How recently was content updated? | Days since last update, per section |
| **File Size Compliance** | Are content files within the 1-3KB guideline? | % of files within range (excluding known exceptions) |
| **Provenance Coverage** | Do content files have source attribution? | % of files with provenance frontmatter |

---

## Eval Dimensions

Three independent variables affect pack-powered response quality. When running evaluations, vary one dimension at a time and hold the others constant — otherwise you can't attribute changes in metrics.

### The Three Dimensions

| Dimension | What It Is | Examples |
|-----------|-----------|---------|
| **Structure** | The pack's schema, file organization, chunking, cross-references, context tiers, and content quality | Splitting oversized files, adding summary layers, improving cross-references, adding missing content |
| **Model** | The backend LLM processing queries against the pack | Gemini Flash, Claude Sonnet, GPT-5 Mini — same pack, different reasoning capabilities |
| **Agent Training** | System prompts, agent instructions, and guidance docs that tell the agent *how* to use the pack | Feature frequency guidance, disambiguation rules, response patterns, persona instructions |

### Why This Matters

- A stronger **model** can mask structural problems in the pack (brute-forcing answers from poorly organized content)
- Better **agent training** can compensate for pack gaps (guidance docs that say "default to X when the user says Y")
- Better **structure** improves results across all models and training configurations

The highest-leverage improvements are **structural** — they compound across every model and every agent configuration. Agent training is second (transferable across models). Model upgrades are third (expensive and vendor-dependent).

### Declaring Dimensions in Eval Runs

Every eval run must declare what changed relative to the baseline:

```yaml
dimensions:
  structure:
    version: "2.0.0"           # Pack version from manifest
    changes: "Split 7 oversized files, added summary layers"
  model:
    name: "gemini-2.0-flash"
    provider: "openrouter"
  agent_training:
    version: "1.0"             # Version or hash of system prompt / guidance docs
    changes: "Added territory planning guidance doc"
```

When comparing runs, only draws conclusions about the dimension that changed. If structure AND model changed between runs, the comparison is informational but not attributable.

---

## Eval Run Results

Each eval run produces a results file capturing scores, dimensions, and per-question details.

### Format

```yaml
# eval/results/{YYYY-MM-DD}-{label}.yaml
run_date: "YYYY-MM-DD"
label: "{descriptive label, e.g., baseline-gemini-flash}"
eval_set_version: "1.0"
questions_total: 50
questions_evaluated: 50

# What was tested (see Eval Dimensions above)
dimensions:
  structure:
    version: "2.0.0"
    changes: ""
  model:
    name: "gemini-2.0-flash"
    provider: "openrouter"
  agent_training:
    version: "1.0"
    changes: ""

# Aggregate scores
scores:
  correctness: 0.82          # % of required facts present
  groundedness: 0.91         # % of claims backed by pack content
  hallucination_rate: 0.06   # % of responses with fabrications
  refusal_accuracy: 1.00     # % of out-of-scope correctly declined
  retrieval_hit_rate: 0.78   # % where expected sources were retrieved
  avg_input_tokens: 3200     # Average input tokens per query
  avg_output_tokens: 450     # Average output tokens per query
  avg_latency_ms: 2100       # Average end-to-end latency
  avg_cost_usd: 0.003        # Average cost per query

# Per-question details
details:
  - id: "q001"
    correctness: 1.0
    facts_present: ["Must mention creating a project first", "Must reference the markup tools", "Should mention saving/publishing"]
    facts_missing: []
    hallucinations: []
    sources_retrieved: ["workflows/create-territory.md", "concepts/territories.md"]
    sources_expected: ["workflows/create-territory.md", "concepts/territories.md"]
    input_tokens: 2800
    output_tokens: 380
    latency_ms: 1950
    notes: ""
```

### Baselines

Save a results file to `eval/baselines/` to mark a comparison point. Label it clearly:

```
eval/baselines/2026-03-10-initial-baseline.yaml
eval/baselines/2026-03-24-after-file-splitting.yaml
eval/baselines/2026-04-07-after-query-routing.yaml
```

Baselines enable A/B comparison: "after splitting oversized files, correctness went from 0.82 → 0.88 and avg_input_tokens dropped from 3200 → 2100."

---

## Eval Workflow

### For Pack Builders

1. **Build the eval set** — Create `eval/questions.yaml` with 30+ questions covering your pack's key scenarios
2. **Run baseline** — Execute the eval set against the current pack + model configuration. Save to `eval/baselines/`.
3. **Make improvements** — Split files, add content, refine cross-references, tune context tiers
4. **Re-run eval** — Execute the same eval set. Compare to baseline.
5. **Iterate** — If metrics improved, save new baseline. If not, investigate why.

### For Framework Developers

When changing the schema or core conventions:
1. Run evals across multiple pack types before the change
2. Make the change
3. Re-run evals
4. Document the impact in the schema changelog

### Automation

The eval workflow can be partially automated:
- **Retrieval scoring** — fully automatable (compare retrieved files to expected_sources)
- **Correctness scoring** — semi-automatable (LLM-as-judge checks for required_facts)
- **Hallucination detection** — semi-automatable (LLM-as-judge checks for anti_hallucination violations)
- **Groundedness** — requires comparing response claims against pack content (LLM-as-judge)
- **Voice fidelity** — primarily human evaluation (person packs)

An eval runner script should:
1. Load the eval set
2. For each question: query the pack-powered agent, capture response + metadata
3. Score each response against expected answers
4. Produce aggregate metrics + per-question details
5. Save results to `eval/results/`

---

## Relationship to Other Schemas

- **core.md** — Eval schema follows all core conventions (MD-canonical, file naming, tiers)
- **Pack type schemas** — Question categories align with type-specific directory structures
- **manifest.yaml** — Add optional `eval` block for eval set metadata:

```yaml
# Optional addition to manifest.yaml
eval:
  eval_set: "eval/questions.yaml"
  latest_baseline: "eval/baselines/2026-03-10-initial-baseline.yaml"
  last_eval_run: "2026-03-10"
  ek_ratio: 0.72              # Latest measured EK ratio (also declared at top level)
```

---

*Schema version: 1.2*
*Created: 2026-03-05*
*Last updated: 2026-03-12*
