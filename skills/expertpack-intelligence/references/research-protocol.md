# Research Protocol (Step 1)

Hard stop at **30 minutes**. Transferable approaches only — not a literature review.

## Query set

Run these in parallel, then synthesize. Skip generic “what is RAG” tutorials.

1. **Esoteric / tribal / unpublished knowledge for AI agents** — how teams inject knowledge that is not in frontier weights (not generic document RAG).
2. **Contextual retrieval** — query-time document prefixes, chunk↔document linking, late interaction.
3. **Agentic / multi-pass RAG** — retrieve → focus / rewrite → retrieve; query routing.
4. **Memory architectures** — episodic agent memory vs curated expertise injection. EP is the latter; note complements, do not copy the former wholesale.
5. **Graph + vector hybrids** — GraphRAG, temporal graphs, dependency expansion. Mark Graphiti-style bi-temporal facts as already integrated unless the source shows a new mechanism.
6. **Progressive-disclosure skills / context loading** — how agents load filing rules without dumping the whole spec.
7. **Claim-to-span grounding** — mark Reconstruct Mode / TAC as already integrated unless the source shows a new mechanism.

Prefer primary sources (vendor research posts, papers, shipped open-source READMEs) over listicles. Record URL + date accessed for every source you keep.

## Already integrated (do not re-propose)

Unless the source shows a *material* change EP does not have:

- Graphiti-style bi-temporal facts → `valid_from` / `recorded_at`, W-PROV-05
- Hybrid KG + vector micro-records → AKS JSONL export
- Reconstruct Mode / fragment provenance → RFC-003
- Typed Answer Contract → TAC + `claim_verifier --tac`
- `requires:` expansion (depth 2, count 3, token-budget capped) → EP MCP 0.4+
- Schema-aware chunking / atomic-conceptual files → RFC-001 / core 4.1
- Chunk sidecars for oversized atomic files → RFC-004

## Scoring rubric

A candidate must pass **all** of these before it can be a top-3:

| Gate | Fail if |
|------|---------|
| Framework-first | The change only helps one pack or one vendor runtime |
| Pack-type agnostic | It only works for product *or* person *or* process |
| Measurable | You cannot name a before/after metric |
| Axioms 11–13 | It adds standalone summaries, propositions, FAQ hubs, or other aggregators |
| Anti-compaction | It “saves tokens” by densifying prose or stripping examples |

Allowed metrics: retrieval hit rate, correctness, completeness, hallucination rate, tokens/query, EK ratio, TAC claim coverage / citation F1.

## Output shape

Emit **exactly 3** suggestions. Use this block per item:

```markdown
### R{n}. {short title}

- **Approach:**
- **Source:** {title} — {URL} ({YYYY-MM-DD})
- **EP mapping:** {schema / tool / guide that would change}
- **Metric:** {name + how we would measure}
- **Risk:**
- **Next action:** consider | pilot | reject
```

`consider` = write a ROADMAP checkbox. `pilot` = small measurable experiment on a real pack. `reject` = log why, do not carry forward.

If you have fewer than 3 that pass the rubric, emit the passers and fill remaining slots with `reject` plus the closest miss and why it failed. Do not pad with axiom-hostile ideas.
