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
- [ ] **Eval framework schema** — standard format for Q&A eval sets, quality scoring
- [ ] **Pack health metrics** — schema conformance, coverage, freshness, cross-ref integrity
- [ ] **Runtime metrics** — tokens/query, latency, cost, retrieval precision
- [ ] **Eval runner** — tool/script that executes eval sets and produces scorecards
- [ ] **First pack baseline** — run eval against a real deployed pack to establish baseline numbers

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
- [ ] **Hallucination measurement** — automated detection via LLM-as-judge against pack content

### 4. Pack Creation & Training
Make it easier to build and maintain packs.
- [ ] **Pack scaffolding CLI** — `expertpack init --type product --name "Acme"`
- [ ] **Validation tool** — `expertpack validate ./my-pack/` checks conformance
- [ ] **Guided interview mode** — agent-driven structured knowledge capture
- [ ] **Population playbooks** — interactive recipes per source type

### 5. Schema Evolution
Keep the framework current as LLMs advance.
- [ ] **File size flexibility** — revisit 1-3KB for large-context models; maybe a "dense mode"
- [ ] **Chunking strategy review** — evaluate semantic chunking vs header-based
- [ ] **Agentic RAG patterns** — multi-step retrieval, query refinement
- [ ] **Minimum capability declarations** — manifest field for required model capabilities
- [ ] **Regular schema review cadence** — triggered by major model releases

### 6. Continuous Intelligence
Stay current with developments that could improve the framework.
- [ ] **X daily scan** — ✅ Already running (captures design learnings)
- [ ] **Weekly web intelligence sweep** — search for RAG, knowledge-base, and expertise-capture advances
- [ ] **Schema review triggers** — flag when new model capabilities make assumptions revisitable

---

## Status Log

### 2026-03-05 — Project Kickoff
- Defined the six improvement vectors
- Decision: start with eval framework (Vector 1) as foundation for everything else
- Decision: framework-first, pack-type agnostic approach
- Started drafting eval framework schema (`schemas/eval.md`)

---

*Update this file when meaningful progress happens on any vector. This is the single source of truth for the improvement project.*
