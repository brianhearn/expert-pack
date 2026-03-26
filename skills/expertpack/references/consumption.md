# Consumption Reference

How to deploy an ExpertPack as the knowledge backend for an AI agent.

## Core Principles

1. **Pack value ∝ EK ratio.** Content the model already knows is dead weight.
2. **Retrieval precision > model capability.** A weaker model with precise context beats a stronger model with sloppy retrieval.
3. **Three independent quality dimensions:** Structure (the pack), Model (the LLM), Agent Training (system prompts). Improve one at a time.

## Platform Integration

### OpenClaw

Add pack to `memorySearch.extraPaths` in `openclaw.json`:

```json
{
  "agents": {
    "defaults": {
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
  }
}
```

- **Overlap 0** — pre-chunked files are already semantically complete
- **MMR (λ=0.7)** — prevents near-duplicate chunks from crowding results
- **Temporal decay off** — pack knowledge doesn't expire by file modification time

### IDE Agents (Cursor, Claude Code)

Place the pack in the project directory. Reference from `.cursorrules` or `CLAUDE.md`. The small-file structure (1–3KB) is already optimized for built-in chunking. Schema-aware pre-chunking is optional but still beneficial.

### Custom / API

Feed `.md` files into your vector store. Respect context tiers from `manifest.yaml`:
- **Tier 1 (Always):** Include in every prompt as system context
- **Tier 2 (Searchable):** Index in vector store for retrieval
- **Tier 3 (On-demand):** Skip indexing; load only on explicit request

### Direct Context Window (Small Packs)

Packs under ~20 files / 30KB: skip RAG. Concatenate Tier 1 + Tier 2 files directly into system prompt.

## Schema-Aware Chunking — Evidence

Results from 6 controlled experiments on a deployed product pack (204 source files, 50-question eval):

| Change | Correctness | Hallucination | Tokens | Verdict |
|--------|------------|---------------|--------|---------|
| **Baseline** (generic chunks, GPT-5 Mini) | 79.0% | 10.0% | 4,372 | Starting point |
| File splitting alone | 76.9% (-2.1%) | 12.0% (+2%) | 3,686 | ❌ Lost context |
| Prose compaction (~40% denser) | 76.8% (-2.2%) | 14.0% (+4%) | 3,721 | ❌ Harder to parse |
| Summaries + propositions + splits | 78.7% (-0.3%) | 6.0% (-4%) | 3,733 | ✅ First quality win |
| Model upgrade (GPT-5.3 Chat) | 80.1% (+1.1%) | 4.0% (-6%) | 3,050 | ✅ Better reasoning |
| **Schema-aware chunking** (GPT-5 Mini) | **88.4%** (+9.4%) | **4.0%** (-6%) | **2,111** (-52%) | 🔥 Best single change |

**Key takeaway:** Schema-aware chunking is the highest-impact single change. A cheap model with precise retrieval beat an expensive model with generic retrieval.

## Chunking Strategies (Schema 2.4+)

The chunker applies **atomic** or **sectioned** strategy per file:

| Strategy | Behavior | Default For |
|----------|----------|-------------|
| **atomic** | Entire file as one chunk; never split | `workflows/`, `troubleshooting/errors/`, `troubleshooting/diagnostics/`, `troubleshooting/common-mistakes/` |
| **sectioned** | Split on `##` headers | `concepts/`, `interfaces/`, `faq/`, `propositions/`, `summaries/`, `commercial/`, all others |

**Why atomic matters:** Workflows and troubleshooting are step-by-step procedures or symptom → cause → fix units. Splitting them causes the model to hallucinate missing steps.

**Precedence:** frontmatter override → directory default → sectioned fallback.

Per-file override via YAML frontmatter:
```yaml
---
retrieval:
  strategy: atomic
---
```

**Sequence metadata:** Sectioned splits include `part X of Y` and a `sequence` glob in source comments so consuming agents can find all sibling chunks.

## Context Tier Loading

| Tier | Name | When Loaded | Size Target |
|------|------|-------------|-------------|
| 1 | Always | Every session | < 5KB total |
| 2 | Searchable | On topic match via RAG | Bulk of pack |
| 3 | On-demand | Explicit request only | Verbatim, training, archival |

**Hierarchical retrieval:** Broad questions → match summaries. Factual questions → match propositions. Detail questions → match content files.

## Agent Training (SOUL.md Pattern)

```markdown
# SOUL.md — {Agent Name}

## Identity
You are {name}, a {role} powered by the {pack name} ExpertPack.

## Scope
Answer questions about {in-scope topics}.
Do NOT answer questions about {out-of-scope topics}.
When out of scope: "{refusal message}"

## Response Style
- {Length, format, citation, uncertainty handling}

## Anti-Hallucination
- Only answer from provided ExpertPack context
- If not covered, recommend {fallback: docs URL, support email}
- Never invent feature names, config options, or workflow steps
```

**Refusal accuracy depends heavily on model capability.** Jumped from 0% → 75% across model tiers with the same SOUL.md. If refusal matters, test your specific model.

## Model Selection

| Priority | Factor | Why |
|----------|--------|-----|
| 1 | Instruction following | Scope rules, refusals — primary model differentiator |
| 2 | Context window | Must fit Tier 1 + retrieval results (8–16K usually sufficient) |
| 3 | Speed/latency | User-facing needs fast TTFT |
| 4 | Cost per query | Scales with volume |
| 5 | Reasoning depth | Only critical for multi-step synthesis |

## Eval-Driven Improvement Loop

1. Deploy with initial config → 2. Build eval set (30+ questions) → 3. Run baseline → 4. Identify failure patterns → 5. Fix one dimension → 6. Re-run eval → 7. Compare

### Common Failure Patterns

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Wrong answer on covered topic | Retrieval miss | Add lead summary, improve headers, run chunker, check glossary |
| Confident wrong answer | Hallucination | Add anti-hallucination facts; strengthen SOUL.md |
| Incomplete answer | Content gap or partial retrieval | Check content exists; add propositions |
| Answers off-topic questions | Weak refusal | Strengthen scope rules with examples; upgrade model |
| Vocabulary mismatch | User terms ≠ pack terms | Update glossary "Common User Language" column |
| High token cost | Over-retrieval | Schema-aware chunking, enable MMR |

### Optimization Priority

1. **Structure** — highest leverage, compounds across all models
2. **Agent Training** — transfers across model upgrades
3. **Model** — most expensive, least durable

## Quick-Start Checklist

- [ ] Choose platform (OpenClaw, IDE, custom, direct context)
- [ ] Run schema-aware chunker
- [ ] Configure RAG (chunk 500, overlap 0, MMR on, decay off)
- [ ] Write SOUL.md (identity, scope, style, anti-hallucination)
- [ ] Select model (balance cost, speed, instruction following)
- [ ] Load Tier 1 files in system prompt
- [ ] Build eval set (30+ questions)
- [ ] Run baseline eval
- [ ] Fix failures (structure → training → model)
- [ ] Deploy and monitor
