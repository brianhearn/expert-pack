# Consumption Guide

*How to deploy an ExpertPack as the knowledge backend for an AI agent. Covers platform integration, chunking strategy, RAG configuration, model selection, agent training, and the eval-driven improvement loop — all grounded in real experiments on a deployed product pack.*

---

## Philosophy

An ExpertPack is not a chatbot — it's a knowledge layer. The consuming agent provides personality, conversation management, and tool use. The pack provides domain expertise the model cannot produce on its own.

Three principles guide consumption:

1. **The pack's value is proportional to its EK ratio.** Content the model already knows is dead weight — it burns tokens without adding value. High-EK packs give the model capabilities it genuinely cannot achieve alone.

2. **Retrieval precision matters more than model capability.** A weaker model with precisely retrieved context outperforms a stronger model with sloppy retrieval. Getting the right content into the context window matters more than how smart the model is. (See [Evidence](#evidence-what-works-and-what-doesnt) below.)

3. **Three independent dimensions determine quality.** Structure (the pack), Model (the LLM), and Agent Training (system prompts) each affect output quality independently. Improve them one at a time, measure the impact, and don't confuse which dimension caused a change.

---

## Platform Integration

### OpenClaw

The native deployment platform. Add the pack path to `memorySearch.extraPaths` in your `openclaw.json`:

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "extraPaths": ["path/to/pack"]
      }
    }
  }
}
```

OpenClaw auto-indexes all `.md` files in the specified paths. For best results, pre-chunk with the [schema-aware chunker](../tools/schema-chunker/) and point `extraPaths` at the `.chunks/` directory instead (see [Chunking Strategy](#chunking-strategy)).

**Recommended RAG settings for chunked packs:**

```json
{
  "memorySearch": {
    "extraPaths": ["path/to/pack/.chunks"],
    "chunking": { "tokens": 500, "overlap": 0 },
    "query": {
      "hybrid": {
        "enabled": true,
        "mmr": { "enabled": true, "lambda": 0.7 },
        "temporalDecay": { "enabled": false }
      }
    }
  }
}
```

- **Overlap 0** — pre-chunked files are already semantically complete; overlap would duplicate content
- **MMR enabled (λ=0.7)** — prevents near-duplicate proposition/summary/content chunks from crowding results
- **Temporal decay off** — pack knowledge doesn't expire based on file modification time

### Cursor / Claude Code / IDE Agents

Place the pack in your project directory. IDE agents discover and index workspace files automatically.

- **Cursor:** Reference from `.cursorrules` or let the agent discover pack files via workspace indexing
- **Claude Code:** Reference from `CLAUDE.md` or let the agent discover it
- **Other IDE agents:** Place pack where the agent's workspace indexer can find it

For IDE agents, the pack's small-file structure (1–3KB per content file) is already optimized for their built-in chunking. Schema-aware pre-chunking is optional but still beneficial.

### Custom / API Integrations

Feed `.md` files into your vector store or embedding pipeline. The ExpertPack structure is designed for this:

- **Small files** (1–3KB each) produce high-relevance chunks with any splitter
- **`##` headers** provide natural split points for any markdown-aware chunker
- **Context tiers** from `manifest.yaml` tell you what to always include vs. index vs. skip
- **Propositions** can be embedded directly as atomic retrieval units

For custom integrations, respect the context tier declarations in `manifest.yaml`:
- **Tier 1 (Always):** Include in every prompt as system context
- **Tier 2 (Searchable):** Index in your vector store for retrieval
- **Tier 3 (On-demand):** Skip indexing; load only on explicit request

### Direct Context Window (Small Packs)

Packs under ~20 files / 30KB can load entirely into the context window. Skip RAG — concatenate Tier 1 files + all Tier 2 files directly into the system prompt.

This works well for:
- Person packs in conversational chat
- Small process packs (< 15 phases)
- Demos and showcases
- Any deployment where simplicity beats token efficiency

For larger packs, RAG retrieval is essential — a 200-file pack won't fit in context, and even if it could, the model's attention degrades with excessive context length.

---

## Chunking Strategy

**This is the single most impactful consumption decision.** How you chunk the pack for retrieval determines correctness, hallucination rate, and token efficiency more than any other factor.

### The Problem with Generic Chunkers

Most RAG systems chunk files by character or token count. They don't understand Markdown structure. A generic chunker will:

- Split a lead summary from its `# Title`
- Cut a proposition group between the `### source.md` header and its bullet list
- Slice a glossary table mid-row
- Orphan a `<!-- refresh -->` metadata block from the content it describes
- Break a `##` section in the middle of a thought

The result: every retrieved chunk is an arbitrary text slice that may have lost its context. You spent effort structuring knowledge with headers, lead summaries, and grouped propositions — and the chunker throws that structure away.

### Schema-Aware Chunking

The [schema-aware chunker](../tools/schema-chunker/) pre-processes ExpertPack files into semantically coherent chunk files. Each output file is one complete thought, sized to fit within the RAG system's token budget. The consuming platform's chunker then passes each file through 1:1 — no re-splitting.

**What it respects:**
- `##` headers as semantic boundaries (never splits mid-section)
- Lead summaries stay attached to their `# Title`
- Proposition groups (`### source.md` + bullet list) stay intact
- Glossary category tables stay together
- YAML frontmatter stays with the first chunk
- `<!-- refresh -->` metadata stays with its content
- `_index.md` files chunked as single units when possible
- **Atomic vs. sectioned strategies** per directory and per file (see below)
- **Sequence metadata** in chunk source comments for sectioned splits

**Usage:**

```bash
python3 tools/schema-chunker/chunk.py --pack ./packs/my-pack --output ./packs/my-pack/.chunks
```

Then point your RAG system at `.chunks/` instead of the raw pack directory. See the [chunker README](../tools/schema-chunker/README.md) for the full CLI reference.

### Atomic vs. Sectioned Strategies

*(Schema 2.4+)*

Not all content should be split the same way. A 10-step workflow must be retrieved whole — retrieving step 5 of 10 without context produces hallucinated instructions. A large concept file with independent sections can be split safely.

The schema-aware chunker supports two strategies:

| Strategy | Behavior | Default For |
|----------|----------|-------------|
| **atomic** | Emit the entire file as a single chunk, regardless of size. Never split. | `workflows/`, `troubleshooting/errors/`, `troubleshooting/diagnostics/`, `troubleshooting/common-mistakes/` |
| **sectioned** | Split on `##` headers, then `###` if oversized, then paragraphs. Standard behavior. | `concepts/`, `interfaces/`, `faq/`, `propositions/`, `summaries/`, `commercial/`, and all other directories |

**Why workflows are atomic:** Workflows are step-by-step procedures where each step depends on the previous. Retrieving a fragment without the surrounding steps causes the model to fill gaps with fabricated UI paths and invented interactions.

**Why troubleshooting is atomic:** Error resolution files (symptom → cause → fix) and diagnostic decision trees lose their logical flow when split. An agent that retrieves only the "fix" without the "symptom" and "cause" gives dangerously decontextualized advice.

#### Directory Defaults

The chunker maps ExpertPack directory conventions to default strategies automatically:

| Directory | Default Strategy | Rationale |
|-----------|-----------------|-----------|
| `workflows/` | atomic | Procedures are indivisible |
| `troubleshooting/errors/` | atomic | Error + fix is one unit |
| `troubleshooting/diagnostics/` | atomic | Decision trees are indivisible |
| `troubleshooting/common-mistakes/` | atomic | Symptom + fix is one unit |
| `interfaces/` | sectioned | Large files; regions are independent |
| `concepts/` | sectioned | Sections are self-contained |
| `faq/` | sectioned | Each Q&A stands alone |
| `propositions/` | sectioned | Groups of atomic facts |
| `summaries/` | sectioned | Section summaries are independent |
| `commercial/` | sectioned | Topics within commercial docs are independent |
| All others | sectioned | Safe default |

#### Per-File Override

Any content file can override its directory default by declaring a `retrieval` block in its YAML frontmatter:

```yaml
---
retrieval:
  strategy: atomic
---
```

Precedence: **frontmatter override → directory default → sectioned fallback.**

Use this when a file's retrieval needs differ from its directory convention — e.g., a concept file that contains a critical decision framework that must not be fragmented.

#### Sequence Metadata

When a file IS split (sectioned strategy), the chunker embeds sequence metadata in each chunk's source comment so consuming agents know how many sibling chunks exist and how to find them:

```
<!-- source: concepts/territories.md | section: How It Works (part 3 of 7) | sequence: concepts--territories--*.md -->
```

The `part X of Y` tells the agent this is an incomplete fragment. The `sequence` glob tells it where to find the full set. An agent receiving a sequence-tagged chunk should load all sibling chunks before synthesizing an answer.

#### Atomic Chunks and Size Limits

Atomic files may exceed the chunker's default character budget. This is expected and acceptable — the alternative (splitting a workflow) is worse than a larger chunk. RAG systems with hard size limits should index the full atomic chunk for retrieval, and optionally generate a summary companion chunk for lightweight search matching.

### Evidence: What Works and What Doesn't

These results come from 6 controlled experiments on a deployed product pack (EZT Designer, 204 source files, 50-question eval set), each changing one variable at a time:

| Change | Correctness | Hallucination | Input Tokens | Verdict |
|--------|------------|---------------|-------------|---------|
| **Baseline** (generic chunks, GPT-5 Mini) | 79.0% | 10.0% | 4,372 | Starting point |
| File splitting alone | 76.9% (-2.1%) | 12.0% (+2%) | 3,686 | ❌ Lost context |
| Prose compaction (~40% denser) | 76.8% (-2.2%) | 14.0% (+4%) | 3,721 | ❌ Harder to parse |
| Summaries + propositions + splits | 78.7% (-0.3%) | 6.0% (-4%) | 3,733 | ✅ First quality win |
| Model upgrade (GPT-5.3 Chat) | 80.1% (+1.1%) | 4.0% (-6%) | 3,050 | ✅ Better reasoning |
| **Schema-aware chunking** (GPT-5 Mini) | **88.4%** (+9.4%) | **4.0%** (-6%) | **2,111** (-52%) | 🔥 Best single change |

**Key takeaways:**

- **Schema-aware chunking is the highest-impact single change.** +9.4% correctness and -52% tokens — bigger than any model upgrade, content edit, or RAG config tweak.
- **Splitting alone hurts.** Sub-files lose the surrounding context that helped the model. Never split without adding retrieval layers (summaries + propositions).
- **Compaction hurts.** Removing examples and shortening explanations makes text harder for models to parse. The "redundant" content was reasoning scaffolding.
- **Retrieval precision > model capability.** GPT-5 Mini with schema chunks (88.4%) beat GPT-5.3 Chat with generic chunks (80.1%). Getting the right content into context matters more than how smart the model is.

---

## Context Tier Loading

ExpertPacks declare a three-tier context strategy in `manifest.yaml`. The consuming agent should respect these tiers to balance depth with token efficiency. See [core.md — Context Strategy](../schemas/core.md#context-strategy) for the full specification.

### Tier 1 — Always

Loaded at session start, every conversation. These establish the agent's domain awareness:

- `manifest.yaml` — what the pack is
- `overview.md` — entry point, key capabilities
- `glossary.md` — vocabulary bridging for every query
- Identity/voice files (person packs)

**Keep Tier 1 under 5KB total.** Every token here is spent on every conversation turn. If a Tier 1 file exceeds 3KB, consider whether parts belong in Tier 2.

### Tier 2 — Searchable

The bulk of knowledge — indexed for RAG retrieval. Loaded when the conversation touches a relevant topic:

- Content files (concepts, workflows, troubleshooting)
- Section summaries (`summaries/`)
- Atomic propositions (`propositions/`)
- Directory indexes (`_index.md`)

Design Tier 2 files to be independently useful. An agent loading a single file should get a complete, actionable answer without needing to load five siblings for context.

### Tier 3 — On-Demand

High-token or specialized content, loaded only on explicit request:

- Full verbatim transcripts (person packs)
- Training data
- Raw exports and archival material
- Coverage maps and changelogs

### Hierarchical Retrieval

Packs with summaries and propositions support multi-granularity retrieval:

1. **Broad questions** ("what can this product do?") → match section summaries → provide complete overview
2. **Specific factual questions** ("what's the max stops per route?") → match atomic propositions → load source file for context if needed
3. **Follow-up questions** → navigate via `_index.md` and cross-references → drill into detail files

This layered approach improves both precision and token efficiency over flat retrieval against hundreds of content files.

---

## Model Selection

Choosing the right model is NOT about picking the best model — it's about picking the right model for the job. Our experiments showed that model capability matters far less than most people assume, *if retrieval is precise.*

### What the Experiments Showed

| Metric | GPT-5 Mini + schema chunks | GPT-5.3 Chat + generic chunks |
|--------|---------------------------|-------------------------------|
| Correctness | **88.4%** | 80.1% |
| Hallucination | **4.0%** | 4.0% |
| Refusal accuracy | 50.0% | **75.0%** |
| Input tokens | **2,111** | 3,050 |

The cheaper, faster model with precise retrieval beat the expensive model with sloppy retrieval on correctness. But the expensive model was dramatically better at instruction following (refusal accuracy: 75% vs 50%).

**The lesson:** Model capability matters most for **instruction following** — can it follow scope rules, decline out-of-scope questions, and respect SOUL.md guidelines? It matters less for **factual correctness** when the retrieval layer provides the right content.

### Selection Criteria

| Priority | Factor | Why |
|----------|--------|-----|
| 1 | **Instruction following** | Can it follow SOUL.md scope rules? Decline out-of-scope? This is the primary differentiator between models. |
| 2 | **Context window** | Must fit Tier 1 + typical retrieval results. Usually 8–16K tokens is sufficient with good chunking. |
| 3 | **Speed / latency** | User-facing agents need fast time-to-first-token. A 10-second response kills UX. |
| 4 | **Cost per query** | Support bots may handle thousands of queries/day. A 7x cost difference adds up. |
| 5 | **Reasoning depth** | Only critical for multi-step troubleshooting or synthesis across many files. |

### Recommendations by Use Case

**Customer support bot** — Fast, cheap, good instruction following. GPT-5 Mini, Gemini Flash, or similar. Invest in pack structure and chunking instead of model capability. If refusal accuracy matters (it usually does), test your specific model against out-of-scope questions before deploying.

**Expert assistant (internal)** — Stronger reasoning justified. Sonnet, Opus, or GPT-5.3 class. Users are employees who need nuanced multi-step answers. Cost per query is less important than answer quality.

**Demo / showcase** — Best available model for wow factor. Cost is secondary. You want the most impressive responses possible.

**High-volume API integration** — Cheapest model that meets quality thresholds. Run evals on candidate models against the same pack. The model that hits your correctness target at the lowest cost wins.

---

## Agent Training (SOUL.md)

The agent's system prompt or SOUL.md file tells it WHO it is and HOW to use the pack. This is the second-highest-leverage dimension after pack structure — good agent training transfers across model upgrades.

### The SOUL.md Pattern

A SOUL.md for a pack-powered agent should cover:

```markdown
# SOUL.md — {Agent Name}

## Identity
You are {name}, a {role} specializing in {domain}.
You are powered by the {pack name} ExpertPack.

## Scope
Answer questions about {in-scope topics}.
Do NOT answer questions about {out-of-scope topics}.
When asked about something outside your scope, say: "{refusal message}".

## Response Style
- {Length guidelines}
- {Format preferences — bullets, prose, code blocks}
- {Citation style — reference pack files? Quote sources?}
- {Uncertainty handling — "If you're not sure, say so"}

## Anti-Hallucination Rules
- Only answer from the knowledge provided in your ExpertPack context
- If the pack doesn't cover a topic, recommend {fallback: docs URL, support email, etc.}
- Never invent feature names, configuration options, or workflow steps
```

### Out-of-Scope Handling

Critical for product support bots — users *will* ask off-topic questions.

**Refusal accuracy depends heavily on model capability.** In our experiments, refusal accuracy jumped from 0% → 12.5% → 75% across model tiers with the *same* SOUL.md instructions. If refusal matters, test your specific model.

**Explicit rules beat implicit ones:**
- ✅ "Do NOT answer questions about competitor products, pricing of other services, or general IT troubleshooting"
- ❌ "Stay focused on our product" (too vague — the model doesn't know what's out of scope)

**Include examples** of valid and invalid questions in the SOUL.md when possible. Models follow examples better than abstract rules.

### Anti-Hallucination Guidance

Three effective prompting patterns:

1. **"If you're not sure, say so."** Simple and effective. Reduces confident fabrication.
2. **"Only answer from the knowledge provided."** Explicitly scopes the model to pack content.
3. **"When the pack doesn't cover a topic, recommend contacting support at {URL}."** Gives the model a graceful fallback instead of making something up.

These complement the pack's structural anti-hallucination features (lead summaries with "NOT" facts, propositions with precise values, glossary with correct terminology).

---

## Eval-Driven Improvement

Consumption quality is measurable. Don't optimize blind — run evals, identify failure patterns, fix the right dimension, and verify the fix worked.

### The Improvement Loop

1. **Deploy** pack with initial config (chunking, model, SOUL.md)
2. **Build eval set** — 30+ questions covering key scenarios (see [eval schema](../schemas/eval.md))
3. **Run baseline eval** — save results for comparison
4. **Identify failure patterns** — categorize failures by type (see table below)
5. **Fix one dimension at a time** — structure, model, or agent training
6. **Re-run eval** — compare to baseline
7. **If improved, save new baseline.** If not, investigate why.

### Common Failure Patterns

| Symptom | Likely Cause | Which Dimension | Fix |
|---------|-------------|----------------|-----|
| Wrong answer on a covered topic | Retrieval miss — right content exists but wasn't found | Structure | Add lead summary, improve `##` headers, run schema-aware chunker, check glossary for vocabulary gaps |
| Confident wrong answer | Hallucination — model fabricating | Structure + Training | Add anti-hallucination facts to relevant files; add "only answer from provided knowledge" to SOUL.md |
| Incomplete answer | Content gap or retrieval returning partial context | Structure | Check if content exists; if yes, add propositions for precise retrieval |
| Answers questions it shouldn't | Weak refusal / scope creep | Training + Model | Strengthen SOUL.md scope rules with explicit examples; consider model upgrade |
| Refuses questions it should answer | Over-scoped or model confused | Training | Relax scope rules, add examples of valid questions |
| Vocabulary mismatch | User terms don't match pack terms | Structure | Update glossary with user language mappings in "Common User Language" column |
| Slow responses | Too many tokens retrieved, model too large | Structure + Model | Reduce chunk size, tighten retrieval, or use a faster model |
| High token cost | Retrieval returning too much context | Structure | Schema-aware chunking (cut tokens 52% in our experiments), enable MMR to reduce duplicates |

### The Three Dimensions (Revisited)

When evaluating changes, attribute improvements to the correct dimension:

| Dimension | Leverage | Transferability | Cost |
|-----------|---------|----------------|------|
| **Structure** | Highest | Compounds across all models and configs | Time to restructure + re-chunk |
| **Agent Training** | Second | Transfers across model upgrades | Time to write/refine SOUL.md |
| **Model** | Third | Vendor-dependent, may regress on updates | Ongoing per-query cost |

**Always optimize structure first.** A well-structured pack with precise chunking makes every model perform better. Agent training is second — good scope rules and anti-hallucination guidance transfer when you swap models. Model upgrades are last resort — they're the most expensive and least durable improvement.

---

## Monitoring in Production

After deployment, ongoing quality management:

- **Track common questions** that produce poor answers → feed back into the eval set and hydration priorities
- **Monitor token usage per query** — rising tokens may indicate retrieval drift or configuration changes
- **Watch for model degradation** after provider updates — models can regress on specific tasks between versions
- **Re-run evals quarterly** or after any change to pack content, model, or RAG configuration
- **Re-measure EK ratio** after major model releases — knowledge that was esoteric may become general, signaling a need for deeper hydration

---

## Quick-Start Checklist

A condensed deployment checklist for getting a pack into production:

- [ ] **Choose platform** — OpenClaw, IDE agent, custom API, or direct context window
- [ ] **Run schema-aware chunker** — `python3 chunk.py --pack ./pack --output ./pack/.chunks`
- [ ] **Configure RAG** — chunk size 500, overlap 0, MMR enabled, temporal decay off
- [ ] **Write SOUL.md** — identity, scope rules, response style, anti-hallucination guidance
- [ ] **Select model** — balance cost, speed, and instruction following for your use case
- [ ] **Load Tier 1 files** — manifest, overview, glossary in system prompt or always-load config
- [ ] **Build eval set** — 30+ questions covering basic, intermediate, advanced, and out-of-scope
- [ ] **Run baseline eval** — save results
- [ ] **Identify and fix failures** — one dimension at a time (structure → training → model)
- [ ] **Deploy and monitor** — track question patterns, token usage, and model behavior over time

---

*Guide version: 1.1*
*Last updated: 2026-03-26*
