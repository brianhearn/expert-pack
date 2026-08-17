# Agent pack structure (person, subtype: agent, v1.7)

Load with `schemas.md` and `schemas-person.md`. Canonical: `schemas/agent.md`.

```
manifest.yaml          # type: person, subtype: agent, schema_version: "1.7"
overview.md
MIGRATION.md           # replaces person LEGACY.md
operational/           # tools, infrastructure, integrations, routines, safety
mind/                  # PRESCRIPTIVE values, skills, relational, preferences, reasoning, tensions
relationships/people.md
facts/                 # personal, timeline, career
presentation/          # speech-patterns, modes
decisions/             # optional
lessons/               # distilled experience atoms (not an aggregator layer)
training/              # optional, on_demand
meta/                  # privacy, conflicts, resolutions
```

No secrets in `operational/`. Mind files prescribe behavior (“I do X”), they do not describe a human.
