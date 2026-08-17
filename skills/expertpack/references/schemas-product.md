# Product pack structure (v4.1)

Load with `schemas.md`. Canonical: `schemas/product.md`.

```
manifest.yaml
overview.md
meta/source-coverage.md          # retrieval_strategy: navigation
concepts/                        # one concept = one file
workflows/                       # atomic procedures
interfaces/
troubleshooting/                 # errors/, diagnostics/, common-mistakes/ → atomic
commercial/                      # optional
customers/                       # optional
decisions/                       # optional ADRs
specifications/                  # optional
facts/                           # optional timeline / releases
faq/                             # optional — cross-cutting only
```

Required: `manifest.yaml`, `overview.md`. Each content directory gets `_index.md`.

`retrieval_strategy` defaults: `concepts/` and `interfaces/` → `standard`; `workflows/` and troubleshooting leaves → `atomic`; `meta/source-coverage.md` → `navigation`.

Operational atoms (workflow, decision, gotcha, phase) may add optional `activation:` (`tools`, `constraints`, `next`). Do not put it on concepts.
