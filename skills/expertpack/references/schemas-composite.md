# Composite pack structure (v1.2)

Load with `schemas.md`. Canonical: `schemas/composite.md`.

```yaml
name: "Composite Name"
slug: "composite-slug"
type: composite
version: "1.0.0"
schema_version: "1.2"
entry_point: "overview.md"
packs:
  - path: "../packs/agent-slug"
    role: voice              # at most one voice pack
  - path: "../packs/domain-slug"
    role: knowledge
conflicts:
  priority: [agent-slug, domain-slug]
  strategy: "flag"           # fail_closed | flag | priority
  isolation:
    voice_must_not_assert_knowledge: true
    knowledge_must_not_override_voice: true
    respect_access_tiers: true
  tie_break: [authority_boundary, confidence, verified_at]
```

Roles: `voice` (personality/tone) and `knowledge`. Isolation and authority run before strategy. `fail_closed` refuses on disagreement; `flag` asks a human; `priority` picks the first remaining pack. Executable contract: `tools/composite/conflict.py`. Markdown in constituent packs remains canonical.
