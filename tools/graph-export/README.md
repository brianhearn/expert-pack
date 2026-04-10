# ep-graph-export

Generates a `_graph.yaml` (or `_graph.json`) adjacency file for an ExpertPack.
Useful for GraphRAG pipelines and any consumer that needs entity/relationship structure alongside the markdown content.

## Usage

```bash
python3 ep-graph-export.py /path/to/pack
python3 ep-graph-export.py /path/to/pack --output _graph.yaml --format yaml
python3 ep-graph-export.py /path/to/pack --output _graph.json --format json
```

## Output format

```yaml
meta:
  pack: "Pack Name"
  slug: "pack-slug"
  generated_at: "2026-04-10T15:55:00Z"
  node_count: 288
  edge_count: 152
  schema_version: "1.0"

nodes:
  - id: "pack-slug/concepts/topic"
    title: "Topic Title"
    type: "concept"
    file: "concepts/topic.md"
    verified_at: "2026-04-10"

edges:
  - source: "pack-slug/concepts/topic"
    target: "pack-slug/workflows/related-workflow"
    kind: "wikilink"   # wikilink | related | context
```

## Edge kinds

| Kind | Source |
|------|--------|
| `wikilink` | `[[target.md]]` references in file body |
| `related` | `related:` frontmatter list |
| `context` | `<!-- context: ... related=X -->` comment hints |

## Requirements

- Files must have `id:` frontmatter (run `ep-validate --provenance` first)
- Files with `type:` of `index`, `source`, `proposition`, `summary`, `training` are excluded
- Structural files (`_index.md`, `overview.md`, `glossary.md`) are excluded from nodes

## GraphRAG compatibility

The output is a flat adjacency list — import into any graph framework:
- **NetworkX:** `G.add_edges_from([(e['source'], e['target']) for e in graph['edges']])`
- **Neo4j/Cypher:** Map nodes as `:Concept` with `id` as the key property
- **LlamaIndex Knowledge Graph:** Feed nodes/edges into `KnowledgeGraphIndex`
