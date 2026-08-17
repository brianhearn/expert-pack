# Schema Review Protocol (Step 2)

Propose **schema-level** improvements that better meet ExpertPack objectives. Do not edit pack content.

## Read order

1. **Objectives**
   - `AXIOMS.md` (all 13 + operational contracts)
   - `ARCHITECTURE.md` (problem, principles, schema layers, retrieval)
   - `ROADMAP.md` (vision, principles, open Vector 5–6 items)
2. **Canonical contracts**
   - `schemas/schema-index.yaml`
   - `schemas/core.md` (filing rules, atoms, provenance, context tiers, MCP, registry pointers)
   - Type schemas: `product.md`, `person.md`, `process.md`, `agent.md`, `composite.md`, `eval.md`
   - `schemas/registry/` (frontmatter, AKS, chunk-sidecar, TAC, ontology)
3. **What agents actually load**
   - `skills/expertpack/references/schemas.md` and type files `schemas-*.md`
   - `skills/expertpack-export/references/schemas-summary.md`
   - `skills/expertpack/SKILL.md` load sequence

Do not read RFCs in full unless a gap points at one. RFC-002 (person-pack atomic adaptation) is a known open item — confirm it is still the right #1/#2/#3 before re-listing it.

## Score each family against

| Objective | Question |
|-----------|----------|
| EK maximization | Does the schema push authors toward what only this pack can provide? |
| Retrievability | Will an agent find the right atom (opening paragraph, `requires:`, strategy enum, no hubs)? |
| Compactness without EK loss | Does it forbid naive compaction and aggregator files? |
| Decay control | Provenance, volatile isolation, freshness, confidence? |
| Filing-guide quality | Can an agent operator file new content from the *context-loaded* projection without learning a retired contract? |

## Recurring drift to check (not automatic top-3s)

- Condensed skill copy teaching pre-v4.1 chunking (`retrieval.strategy`, `sectioned`) instead of `retrieval_strategy: standard \| atomic \| navigation`
- `relations.yaml` taught as the graph after core retired it for `_graph.yaml` + `ontology.yaml`
- Product `faq/` presented as required rather than optional cross-cutting
- Agent export trees still showing `summaries/`
- `eval.md` / ROADMAP still recommending “summary layers”
- Composite examples on `schema_version: "1.0"` while the type schema is 1.1
- Missing RFC-002 for person-pack verbatim↔atom edge cases

Standing step 3/5 will fix *factual* projection and doc drift. Step 2 top-3s are *design* improvements that need a human gate.

## Output shape

Emit **exactly 3** suggestions, same block as the research protocol, IDs `S1`–`S3`:

```markdown
### S{n}. {short title}

- **Approach:**
- **Source:** {schema path + section} (internal)
- **EP mapping:**
- **Metric:**
- **Risk:**
- **Next action:** consider | pilot | reject
```
