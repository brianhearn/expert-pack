---
name: ontology-to-expertpack
description: "Convert an Ontology skill knowledge graph into a structured ExpertPack. Use when migrating from the Ontology skill's entity/relation graph (memory/ontology/graph.jsonl) to ExpertPack's richer format with multi-layer retrieval, EK measurement, and portable deployment. Output is Obsidian-compatible — includes YAML frontmatter on all content files and can be opened as an Obsidian vault. Triggers on: 'ontology to expertpack', 'convert ontology', 'export ontology', 'migrate ontology', 'ontology graph to pack', 'upgrade ontology'. Requires the Ontology skill's graph.jsonl and optionally schema.yaml."
metadata:
  openclaw:
    homepage: https://expertpack.ai
    requires:
      bins:
        - python3
---

# Ontology to ExpertPack Converter

Converts an OpenClaw Ontology skill's append-only knowledge graph into a fully compliant ExpertPack with multi-layer retrieval support.

## How to Use

Run the converter script:

```bash
python3 {skill_dir}/scripts/convert.py \
  --graph memory/ontology/graph.jsonl \
  --output ~/expertpacks/my-knowledge-pack
```

**Optional flags:**

- `--schema memory/ontology/schema.yaml` — uses type definitions and relation rules
- `--name "My Knowledge Pack"` — custom pack name (defaults to "Ontology Export")
- `--type auto|person|product|process|composite` — override auto-detected pack type

## What It Produces

A complete ExpertPack at the output directory:

- `manifest.yaml` — pack identity, type, context tiers, EK metadata placeholder
- `overview.md` — summary of graph contents, entity/relation counts, navigation guide
- Content organized by mapped category (relationships/, workflows/, facts/, concepts/, operational/, governance/)
- `_index.md` in each content directory
- Wikilinks / `related:` on atoms — then `ep-graph-export` for `_graph.yaml` (do not emit `relations.yaml`)
- `glossary.md` — entity types and terms
- Retriever-anchored opening definitions and `##` section headers for optimal chunking

Filenames use kebab-case. Concept atoms target 400–800 tokens with a 1,000-token ceiling; procedural/reference files stay focused and independently retrievable.

## Post-Conversion Steps

1. `cd` into the generated ExpertPack directory
2. Verify content files are 400–800 tokens each (Schema 2.5 — no external chunker needed for correctly-sized files)
3. Run `python tools/graph-export/ep-graph-export.py .` to write `_graph.yaml`
4. Run EK evaluator to measure esoteric knowledge ratio
4. Review and refine `manifest.yaml` context tiers
5. Commit to git and share via expertpack.ai or ClawHub

See [expertpack.ai](https://expertpack.ai) and the `expertpack` ClawHub skill for full pack maintenance workflows.

Keep the output pack git-friendly and ready for iterative deepening.