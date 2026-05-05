# ExpertPack Registry Schemas

Machine-readable projections of ExpertPack Markdown atoms.

Markdown remains canonical. Registry records are deterministic export artifacts for systems that need compact retrieval rows, graph/triple stores, exact ID lookups, validation, or interop with non-Markdown pipelines.

## Agent Knowledge Schema (AKS)

`agent-knowledge.schema.yaml` defines the compact provenance-first row emitted by:

```bash
python tools/micro-record-exporter/ep-micro-record-export.py \
  --pack path/to/pack \
  --compact \
  --output exports/pack.aks.jsonl
```

AKS is intentionally small. It carries only the fields an agent retrieval pipeline needs to ground an answer and verify the source:

- `schema`
- `id`
- `canonical_statement`
- `title`
- `type`
- `pack`
- `canonical_path`
- `source_span_uri`
- `content_hash`
- `source_checksum`
- optional `verified_at`, `verified_by`, `recorded_at`, `valid_from`
- optional graph fields: `requires`, `related`, `supersedes`

Use AKS when token efficiency, deterministic citations, or easy ingestion into a retrieval/indexing system matters more than preserving the full JSON-LD envelope.

## Full Micro-Records

The default exporter output remains the richer micro-record shape with JSON-LD context, nested `provenance`, lifecycle metadata, tags, and edges. Use full micro-records for archival interchange, richer graph loading, or systems that want the complete record envelope.

## Rule of Thumb

- **Authoring:** Markdown files
- **Agent retrieval / compact pipelines:** AKS JSONL (`--compact`)
- **Graph/registry interchange:** full micro-record JSONL
- **Runtime verification:** EP MCP reconstruct mode
