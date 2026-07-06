# ExpertPack (EP) Axioms

These axioms guide all ExpertPack development decisions.

---

1. **Esoteric knowledge (EK)** is knowledge that only exists outside the weights of frontier-lab LLMs.

2. EPs have a **subject matter** — the person, product, or process (or combination) that they cover.

3. EPs **maximize the ratio of EK** to other knowledge available in LLMs.

4. **EP hydration** is the process of populating the pack with EK.

5. Any **compaction** during EP hydration attempts to minimize loss of EK.

6. The **quality** of an EP is the product of:
   a. **Compactness** of EK in the EP vs the raw source data size (maintaining minimum loss)
   b. **Volume** of esoteric knowledge (while internal redundancy is minimal)
   c. **Retrieval quality** — ability to find all of the correct EK for a given prompt
   d. **Minimal data decay** — prefer knowledge that is static and resilient; for time-bound EK (pricing, API specs, current metrics), isolate it in `volatile/`, declare a `refresh` interval in frontmatter, and exclude it from EK ratio measurement; volatile content that cannot be refreshed is a quality liability

7. The **market value** of an EP is the product of:
   a. **EP quality** (see axiom 6)
   b. **Market potential** — are there a lot of people engaged with the subject matter
   c. **Agentic correlation** — there is some reasonable means for interaction with an agent, either directly or indirectly, as an AI agent subject matter assistant to a person

8. The **cost** to make an EP increases with the amount of EK that must come through human exchange (e.g. interview) and the amount of compute (LLM API tokens).

9. The **EK ratio** of an EP is the proportion of its propositions that frontier LLMs cannot correctly answer without the pack. EK ratio is empirically measurable via blind probing (see core.md — Esoteric Knowledge Ratio) and should be tracked as a first-class quality metric.

10. **Hydration should prioritize EK.** During population, content that the model already knows (general knowledge, well-documented patterns, common definitions) should receive minimal treatment. Content the model cannot produce — tribal knowledge, undocumented behavior, domain-specific edge cases, expert judgment — should receive maximum hydration effort. The goal is not to document everything, but to document what *only this pack* can provide.

11. **One topic = one file.** The retrieval unit is the file. Never split a topic across files that will be retrieved independently — doing so forces the retrieval system to choose between fragments of the same answer. If a topic has a summary and supporting detail, they belong in the same file: the lead sentence is the summary, the body is the detail.

12. **No standalone summary files.** A file whose sole purpose is to summarize other files adds zero EK and actively harms retrieval quality in a retrieval-first pack. Such files score broadly across queries (because they mention everything) and displace specific, high-EK files from the result set. Summaries belong as the lead sentence of the file they describe — not as separate artifacts. This applies equally to proposition files, source digest files, and any cross-cutting aggregate that restates content already present in atomic files.

13. **Pack content strategy must match the intended retrieval model.** A pack built for *LLM-reads-all* (full context injection) can afford cross-cutting summaries and aggregate digests — the model reads everything. A pack built for *retrieval-first* (EP MCP, RAG) requires atomic, non-overlapping files with strong lead sentences — the model reads only what retrieval selects. Mixing strategies degrades retrieval quality. Choose one and hydrate accordingly.

---

## Operational contracts (implements axioms 6 and 13)

These are not new axioms — they are the **2026-07-06 enforcement and verification layer** that makes retrieval-first packs auditable in practice:

| Contract | Implements | Spec / tool |
|----------|------------|-------------|
| **Strict frontmatter gate** | Axiom 6 (quality, minimal decay) — packs cannot drift into unverifiable metadata | `ep-validate --strict`, `schemas/registry/frontmatter.schema.json`, CI |
| **Fragment provenance / Reconstruct Mode** | Axiom 6c (retrieval quality) — prove *which span* was retrieved | RFC-003, `schemas/core.md` |
| **Chunk metadata sidecars** | Axioms 11–13 — oversized atomic/reference files stay whole without arbitrary token splits | RFC-004, `ep-chunk-annotate.py` |
| **Typed Answer Contract (TAC)** | Axiom 6c — every agent claim maps to a retrieved fragment | `typed-answer.spec.yaml`, `validate_tac.py` |

See [ARCHITECTURE.md](ARCHITECTURE.md) for how these fit the framework; see [ROADMAP.md](ROADMAP.md) (2026-07-06) for implementation status.
