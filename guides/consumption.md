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

OpenClaw auto-indexes all `.md` files in the specified paths. Packs authored to the ExpertPack schema (400–800 token files) pass through OpenClaw's chunker as single units — no pre-processing needed.

**Recommended RAG settings:**

Minimal working config:

```json
{
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
```

Full tuned config (validated on real product packs):

```json
{
  "memorySearch": {
    "extraPaths": ["path/to/pack"],
    "chunking": { "tokens": 1000, "overlap": 0 },
    "query": {
      "maxResults": 10,
      "minScore": 0.35,
      "hybrid": {
        "enabled": true,
        "vectorWeight": 0.7,
        "textWeight": 0.3,
        "candidateMultiplier": 4,
        "mmr": { "enabled": true, "lambda": 0.7 },
        "temporalDecay": { "enabled": false }
      }
    }
  }
}
```

- **tokens: 1000** — comfortably above the pack's 800-token file ceiling; ensures no file is split
- **overlap: 0** — pack files are self-contained retrieval units; overlap duplicates content
- **maxResults: 10** — small, focused files benefit from more retrieval slots (adjust for pack size)
- **minScore: 0.35** — filters low-confidence results; prevents noise from unrelated files in large packs
- **vectorWeight: 0.7 / textWeight: 0.3** — semantic search dominates, keyword matching assists; good balance for structured prose with precise terminology
- **candidateMultiplier: 4** — retrieves 4× the result count before MMR re-ranking, giving the ranker more to work with
- **MMR enabled (λ=0.7)** — prevents near-duplicate proposition/summary/content files from crowding results
- **Temporal decay off** — pack knowledge doesn't expire based on file modification time

### Cursor / Claude Code / IDE Agents

Place the pack in your project directory. IDE agents discover and index workspace files automatically.

- **Cursor:** Reference from `.cursorrules` or let the agent discover pack files via workspace indexing
- **Claude Code:** Reference from `CLAUDE.md` or let the agent discover it
- **Other IDE agents:** Place pack where the agent's workspace indexer can find it

For IDE agents, the small-file structure (400–800 tokens per file) is already optimized for any chunker. No pre-processing needed.

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

ExpertPack files are designed to be **retrieval-ready by default**. When authored to the file-size guidelines in the core schema (400–800 tokens per file; 1,500 token ceiling), each file passes through any RAG platform's chunker as a single unit. The schema IS the chunking strategy — no external preprocessing or schema-aware chunker is needed for new packs.

Author content files as self-contained retrieval units. RAG chunkers that see a file under their token budget leave it intact, preserving lead summaries, proposition groups, glossary tables, and `<!-- refresh -->` metadata.

### Atomic vs. Sectioned Content

Not all content should be authored to the standard size target. Procedural content that depends on sequential context must be retrieved as complete units.

| Strategy | Behavior | Default For |
|----------|----------|-------------|
| **standard** | Author within 400–800 token target. Chunker passes through whole. | All content files (default) |
| **atomic** | May exceed size ceiling. Must be retrieved whole. Declare in frontmatter with `retrieval.strategy: atomic` | `workflows/`, `troubleshooting/errors/`, `troubleshooting/diagnostics/`, `troubleshooting/common-mistakes/` |

**Why workflows are atomic:** Workflows are step-by-step procedures where each step depends on the previous. Retrieving step 5 of 10 without the surrounding steps produces hallucinated instructions — the model fills gaps with fabricated UI paths and invented interactions. Workflow files must be retrieved as complete units or not at all.

**Why troubleshooting is atomic:** Error resolution files (symptom → cause → fix) and diagnostic decision trees lose their logical flow when split. An agent that retrieves only the "fix" without the "symptom" and "cause" gives dangerously decontextualized advice.

### Pack–Consumer Coordination Contract

The pack author and consumer config form a two-party contract. The pack commits to a hard ceiling (1,500 tokens for standard files; atomic files may be larger). The consumer sets `chunking.tokens` ≥ that ceiling so nothing gets split. If you're consuming a pack you didn't author, verify its file sizes before assuming the default 1,000-token budget applies. See [core.md — Pack–Consumer Coordination Contract](../schemas/core.md#packconsumer-coordination-contract) for details.

### Platform Configuration - The Three-Knob Model

The pack's file sizes interact with three RAG knobs:

1. **Indexing granularity (`chunking.tokens`)** — Set to 1000 for authored packs. Ensures no file is split.
2. **Retrieval count (`maxResults`)** — Use 8–15 for packs with many small files to capture sufficient context.
3. **System prompt overhead** — Static context (SOUL.md, always-tier files) consumed 72% of input tokens in experiments. Minimize it to maximize room for retrieved content.

See core schema for detailed OpenClaw config example and full guidance.

The +9.4% correctness improvement came from preventing splits on oversized files. We learned that authoring files as self-contained retrieval units (400–800 tokens) at creation time eliminates the need for any preprocessing. This insight became the foundation of Schema 2.5.

#### Directory Defaults for Atomic vs Sectioned Content

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
| High token cost | Retrieval returning too much context | Structure | Verify file sizes (400–800 tokens), enable MMR to reduce duplicates, reduce maxResults |

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

## Deploy Prep: Strip Frontmatter Before Indexing

YAML frontmatter (`id`, `content_hash`, `verified_at`, `verified_by`) is management metadata — it serves tooling and freshness tracking, not retrieval. Embedding it alongside content dilutes semantic similarity scores and wastes context tokens. Strip it before deploying to your RAG platform.

The source pack (in your repo) retains full provenance. The deployed copy is clean. Deploy artifacts are ephemeral.

```bash
# 1. Strip frontmatter to a temp deploy dir
python3 ExpertPack/tools/deploy-prep/ep-strip-frontmatter.py \
    --src ExpertPacks/my-pack \
    --out /tmp/my-pack-deploy \
    --force

# 2. Package and ship (OpenClaw example)
tar czf /tmp/my-pack-deploy.tar.gz -C /tmp/my-pack-deploy .
scp /tmp/my-pack-deploy.tar.gz root@your-host:/tmp/
ssh root@your-host "rm -rf /root/.openclaw/workspace/my-pack && \
    mkdir -p /root/.openclaw/workspace/my-pack && \
    tar xzf /tmp/my-pack-deploy.tar.gz -C /root/.openclaw/workspace/my-pack"

# 3. Clean up
rm -rf /tmp/my-pack-deploy /tmp/my-pack-deploy.tar.gz
```

See `ExpertPack/tools/deploy-prep/` for the full tool and README.

---

## Eval Discipline

Eval results are only comparable when the conditions are identical. Mixing question sets or configs produces noise, not signal.

- **Fix your question set.** Pick N questions (recommended: 20) and never change them between comparison runs. Tag them `benchmark: true` in `questions.yaml`. Use the full set only for exploratory runs.
- **Lock your config.** The canonical RAG config is your baseline. Changing `chunking.tokens`, `maxResults`, or any other parameter is an explicit experiment — document it, run both old and new on the same question set, label the runs clearly.
- **One variable at a time.** Structure, model, config — change only one per run. Multi-variable changes make causality impossible to trace.

---

## Quick-Start Checklist

A condensed deployment checklist for getting a pack into production:

- [ ] **Choose platform** — OpenClaw, IDE agent, custom API, or direct context window
- [ ] **Author to spec** — keep content files 400–800 tokens (schema IS the chunker)
- [ ] **Configure RAG** — `tokens: 1000`, `overlap: 0`, `maxResults: 10`, MMR enabled, temporal decay off
- [ ] **Write SOUL.md** — identity, scope rules, response style, anti-hallucination guidance
- [ ] **Select model** — balance cost, speed, and instruction following for your use case
- [ ] **Load Tier 1 files** — manifest, overview, glossary in system prompt or always-load config
- [ ] **Strip frontmatter** — run `ep-strip-frontmatter.py` before deploying to your RAG platform
- [ ] **Build eval set** — 20 fixed benchmark questions + additional exploratory questions
- [ ] **Run baseline eval** — save results
- [ ] **Identify and fix failures** — one dimension at a time (structure → training → model)
- [ ] **Deploy and monitor** — track question patterns, token usage, and model behavior over time

---

*Guide version: 2.2*
*Last updated: 2026-04-10*
