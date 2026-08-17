# Person pack structure (v4.1)

Load with `schemas.md`. Canonical: `schemas/person.md`.

```
manifest.yaml
overview.md
facts/                 # personal, career, education, timeline, family-tree
stories/               # one story per file; verbatim lives in the atom
reflections/
opinions/
conversations/
relationships/         # one file per significant relationship
mind/                  # ontology, values, identity, motivations, …
presentation/          # speech-patterns, modes, optional voice/appearance
meta/privacy.md
```

Optional: `creative/`, `letters/`, `speeches/`, `training/` (on_demand). Start with `facts/`, `stories/`, `relationships/`.

Person atoms use the core template. Narrative dirs default to `retrieval_strategy: atomic`. Oversized stories keep one file and add a RFC-004 sidecar ([RFC-002](../../../schemas/rfcs/RFC-002-person-pack-atomic-conceptual.md)); split only if each part is an independently retrievable episode.
