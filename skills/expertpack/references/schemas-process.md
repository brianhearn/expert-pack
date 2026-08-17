# Process pack structure (v4.1)

Load with `schemas.md`. Canonical: `schemas/process.md`.

```
manifest.yaml
overview.md
variants.md            # recommended — major forks
fundamentals/        # concept atoms required before starting
phases/                # backbone; atomic; may use requires: for sequence
decisions/
checklists/
gotchas/               # preventive
exceptions/            # reactive
scheduling/            # optional
budget/                # optional
roles/                 # optional
regulations/           # optional
templates/             # optional
resources/             # optional
examples/              # optional
concepts/              # optional promoted terms
faq/                   # optional — cross-cutting only
```

Process-specific manifest fields: `domain`, `typical_duration`, `complexity`, `sections`.

`phases/*.md` default to `retrieval_strategy: atomic`. Concept-like files in `fundamentals/` / `concepts/` follow the 400–800 / 1,000-token rule.
