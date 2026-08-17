# ExpertPack Schema Summary for Export

Projection of repo `schemas/` (family 4.1). Canonical text wins if this file disagrees. Filing rules match `skills/expertpack/references/schemas.md`.

## Pack types

| Type | Subtype | Purpose |
|------|---------|---------|
| person | (none) | Human knowledge — stories, mind, relationships, presentation |
| person | agent | AI agent — operational config, prescriptive mind, tools, safety |
| product | — | Concepts, workflows, interfaces, troubleshooting |
| process | — | Phases, decisions, checklists, gotchas |
| composite | — | Wires packs with roles and conflict rules |

## Agent pack (person, subtype: agent)

```
packs/{agent-slug}/
├── manifest.yaml          # type: person, subtype: agent, schema_version: "1.7"
├── overview.md
├── MIGRATION.md
├── operational/           # tools, infrastructure, integrations, routines, safety
├── mind/                  # prescriptive: values, skills, relational, preferences, reasoning, tensions
├── relationships/people.md
├── facts/                 # personal, timeline, career
├── presentation/          # speech-patterns, modes
├── decisions/             # optional atoms
├── lessons/               # distilled experience atoms
├── meta/privacy.md
└── training/              # optional, on_demand
```

## Person pack

```
facts/   relationships/   mind/   stories/   reflections/   opinions/
conversations/   presentation/   meta/privacy.md
```

## Product pack (v4.1)

```
concepts/   workflows/   interfaces/   troubleshooting/
commercial/   faq/   # faq/ is optional and cross-cutting only
```

Concept files are self-contained retrieval units (opening paragraph, body, optional FAQs and related terms, `requires:`).

## Process pack (v4.1)

```
fundamentals/   phases/   decisions/   checklists/   gotchas/   exceptions/
```

## Composite manifest

```yaml
type: composite
schema_version: "1.2"
entry_point: "overview.md"
packs:
  - path: "../packs/agent-slug"
    role: voice
  - path: "../packs/knowledge-slug"
    role: knowledge
conflicts:
  priority: [agent-slug, knowledge-slug]
  strategy: "flag"           # fail_closed | flag | priority
  isolation:
    voice_must_not_assert_knowledge: true
    knowledge_must_not_override_voice: true
    respect_access_tiers: true
```

## Key rules

1. Markdown canonical — all knowledge in `.md` files
2. Concept atoms: 400–800 tokens, 1,000-token ceiling; one dominant topic per file
3. `retrieval_strategy`: `standard` | `atomic` | `navigation`
4. kebab-case filenames and slugs
5. No secrets
6. `manifest.yaml` and `overview.md` required
7. Distill, don't copy raw workspace state
8. Graph projection is `_graph.yaml` + `ontology.yaml`
