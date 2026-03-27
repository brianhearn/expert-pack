# ExpertPack Improvement Roadmap

*Ongoing project to improve performance, accuracy, efficiency, and usability of the ExpertPack framework. Started 2026-03-05.*

---

## Vision

Make ExpertPacks measurably better across all pack types (person, product, process) — faster retrieval, fewer tokens, less hallucination, easier to build, and continuously improving as LLMs advance.

## Principles

- **Framework-first** — improvements live in the schema/framework, not buried in one pack
- **Pack-type agnostic** — everything should work for person, product, and process packs equally
- **Measurable** — no vibes-based "improvement"; every change needs a before/after metric
- **Test with real packs** — validate improvements against actual deployed packs, not just theory

---

## Improvement Vectors

### 1. Evaluation & Metrics
Define how any pack measures quality. Without this, everything else is guessing.
- [x] **Eval framework schema** — standard format for Q&A eval sets, quality scoring
- [ ] **Pack health metrics** — schema conformance, coverage, freshness, cross-ref integrity
- [ ] **Runtime metrics** — tokens/query, latency, cost, retrieval precision
- [x] **Eval runner** — tool/script that executes eval sets and produces scorecards
- [x] **First pack baseline** — run eval against a real deployed pack to establish baseline numbers

### 2. Performance & Token Efficiency
Reduce latency and token consumption for pack-powered interactions.
- [ ] **Split oversized files** — enforce 1-3KB guideline across all packs
- [ ] **Query routing** — classify questions and scope retrieval to relevant directories
- [ ] **Summary layers** — lightweight summary files for dense reference content
- [ ] **Context tier enforcement** — runtime should respect always/searchable/on-demand tiers
- [ ] **Semantic caching** — cache frequent query patterns to avoid redundant RAG + LLM
- [ ] **Conversation-aware retrieval** — don't re-retrieve files already in context

### 3. Response Quality & Accuracy
Reduce hallucinations and improve answer completeness.
- [ ] **Grounding citations** — require agents to cite specific pack files in answers
- [ ] **Confidence tagging** — content-level confidence (expert-verified, crawled, inferred)
- [ ] **Contradiction detection** — surface conflicting chunks at runtime instead of guessing
- [x] **Hallucination measurement** — automated detection via LLM-as-judge against pack content

### 4. Pack Creation & Training
Make it easier to build and maintain packs.
- [ ] **Pack scaffolding CLI** — `expertpack init --type product --name "Acme"`
- [ ] **Validation tool** — `expertpack validate ./my-pack/` checks conformance
- [ ] **Guided interview mode** — agent-driven structured knowledge capture
- [ ] **Population playbooks** — interactive recipes per source type

### 5. Schema Evolution
Keep the framework current as LLMs advance.
- [ ] **Summary layers** — thin retrieval-optimized summaries over verbatim content; RAG hits summary first, pulls detail on demand. Each summary links back to source-of-truth file. (Source: OpenAI compaction analysis, 2026-03-05)
- [ ] **Context-tier compaction** — ruthlessly compress Tier 1 to identity+voice+navigation only (<5KB); push everything else to Tier 2/3. Audit current packs for tier discipline.
- [ ] **Structured fact tables** — replace narrative repetition with key/value facts, decision tables, canonicalized terms/glossaries for deduplication and retrieval precision
- [ ] **Entity cross-reference indexes** — use entities.json as canonical registry with aliases for term normalization (evaluate whether current RAG actually benefits)
- [ ] **File size flexibility** — revisit 1-3KB for large-context models; maybe a "dense mode"
- [x] **Chunking strategy review** — We built and validated a schema-aware chunker that respected structural elements like headers, lead summaries, proposition groups, and glossary tables. This produced +9.4% correctness and -52% tokens on EZT Designer eval (2026-03-13). The core insight led directly to Schema 2.5: files authored as self-contained 400–800 token retrieval units require no preprocessing — the schema itself became the chunking strategy.
- [ ] **Agentic RAG patterns** — multi-step retrieval, query refinement
- [ ] **Minimum capability declarations** — manifest field for required model capabilities
- [ ] **Regular schema review cadence** — triggered by major model releases

### 6. Continuous Intelligence
Stay current with developments that could improve the framework.
- [x] **X daily scan** — Already running (captures design learnings)
- [x] **Weekly web intelligence sweep** — Wednesdays 14:00 UTC, GPT-5 Mini, logs to logs/expertpack-intelligence.md
- [ ] **Schema review triggers** — flag when new model capabilities make assumptions revisitable

---

## Status Log

### 2026-03-05 — Project Kickoff + Baseline Captured
- Defined the six improvement vectors
- Decision: start with eval framework (Vector 1) as foundation for everything else
- Decision: framework-first, pack-type agnostic approach
- Completed eval framework schema (`schemas/eval.md`) with eval dimensions concept
- Built eval runner + scorer scripts (`ExpertPacks/ezt-designer/eval/run-eval.py`, `score-eval.py`)
- First eval set built (50 questions, 8 categories) for EZT Designer product pack
- Set up weekly web intelligence sweep cron (Wednesdays 14:00 UTC)
- **BASELINE CAPTURED:** 50/50 questions, 0 errors
  - Correctness: 79% | Completeness: 3.8/5 | Hallucination: 10% (5/50) | Refusal: 0% (0/8)
  - Tokens: avg 4,372 in / 840 out / 9,348 total per question | 467K total
  - Model: GPT-5 Mini via OpenRouter | Avg latency: 21.8s
  - Results: `ExpertPacks/ezt-designer/eval/baselines/2026-03-05-baseline.yaml`
- **Key findings:**
  - Concept (94%) and Comparison (94%) categories are strong
  - Refusal accuracy is 0% — bot never declines out-of-scope questions
  - 5 hallucinations: q028 (invented flag names), q037 (oversold), q041 (false export guarantee), q047 (AAD details), q048 (fabricated tech stack)
  - Weak retrieval for q009, q014, q019 — right content exists but wasn't found
- **Improvement plan (in order):**
  1. Agent training (SOUL.md refusal + grounding rules) → re-eval
  2. Pack structure (split oversized files) → re-eval
  3. Content gaps (missing docs, disambiguation layer) → re-eval
  - Each step = one dimension change for clean attribution

---

*Update this file when meaningful progress happens on any vector. This is the single source of truth for the improvement project.*
