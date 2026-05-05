# ExpertPack Ontology Suggest

`ep-ontology-suggest.py` proposes a lightweight ontology from an existing ExpertPack. It is **review-first**: output is suggestions only, not authoritative schema changes.

The tool uses the compact AKS projection from pack Markdown plus existing `requires:` / `related` edges to propose:

- category nodes by content role (`concept`, `workflow`, `failure-mode`, etc.)
- repeated candidate entities/terms with evidence records
- explicit graph edges already present in frontmatter or `_graph.yaml`

## Usage

```bash
# Generate suggestions
python tools/ontology-suggest/ep-ontology-suggest.py /path/to/pack
python tools/ontology-suggest/ep-ontology-suggest.py /path/to/pack --format json --output suggestions.json

# Create an empty accepted ontology registry
python tools/ontology-suggest/ep-ontology-suggest.py /path/to/pack --init-ontology

# Compare suggestions against an explicit accepted ontology
python tools/ontology-suggest/ep-ontology-suggest.py /path/to/pack --ontology /path/to/ontology.yaml
```

Default output is `ontology-suggestions.yaml` in the pack root. If `ontology.yaml` exists, suggestions are compared against accepted entities/relations and marked `existing` or `suggested`.

## Review Workflow

1. Run `ep-validate.py --aks` first so the compact projection is complete enough.
2. Run ontology suggest.
3. Review candidate entities and categories.
4. Accept useful entities into `ontology.yaml`.
5. Re-run suggestions; accepted entities/relations should show as `existing`.
6. Reject generic tags or accidental capitalized phrases.

Do not ingest suggestions automatically into production retrieval without owner review.

## Accepted Ontology Format

Accepted ontology lives in `ontology.yaml` at the pack root by default and follows `schemas/registry/ontology.schema.yaml`:

```yaml
schema: expertpack.ontology.v1
pack: my-pack
updated_at: '2026-05-05'
entities:
  - id: entity:territory
    label: Territory
    kind: concept
    aliases: [territories, sales territory]
    accepted_at: '2026-05-05'
    accepted_by: human
    evidence:
      - my-pack/concepts/territory
relations:
  - source: entity:territory
    target: entity:zip-code
    kind: contains
    accepted_at: '2026-05-05'
    accepted_by: human
```
