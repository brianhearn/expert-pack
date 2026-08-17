---
title: "String inverters"
type: concept
tags: [inverter-types, string-inverter, component-selection]
pack: solar-diy-product
retrieval_strategy: standard
id: solar-diy/product/concepts/inverter-string
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - inverter-types.md
related:
  - inverter-microinverters.md
  - inverter-optimizers.md
  - nec-rapid-shutdown.md
  - nec-rapid-shutdown-editions.md
  - system-design-fundamentals.md
  - system-design-string-sizing.md
content_hash: sha256:baed38a02d53ea47d4b1003b1288c61159054714b0697e304c2bacdf6b9e72b2
---

# String inverters

A string inverter is one central DC-to-AC converter for a series-wired string of panels. SMA Sunny Boy and Fronius Primo/Symo are the usual residential brands. A string inverter alone does **not** satisfy rapid shutdown — add shutdown devices or a UL 3741 system.

## How it works

Panels produce DC → DC flows through a series string → the central inverter converts to AC. All panels in a string share the same current, so the weakest module limits the string.

## Pros and cons

**Pros:** lowest cost per watt; fewer components; highest peak efficiency (~97–98%); ground-level service; decades of field history.

**Cons:** shade or a weak panel limits the whole string; inverter failure takes down the array; string-level (not panel-level) monitoring; requires [[system-design-string-sizing]] against temperature extremes.

**Best for:** simple unshaded roofs with one orientation, budget installs, ground-mounts.

<!-- refresh
  decay: fast-moving
  as_of: 2026-Q1
  fields: [string_inverter_brand_models]
  source: manufacturer product pages (sma.de, fronius.com, solaredge.com)
  method: "Check manufacturer sites for current model lines. Model names change but the architecture concepts above are permanent."
-->

## Related Concepts

- [[inverter-microinverters]]
- [[inverter-optimizers]]
- [[system-design-string-sizing]]
- [[nec-rapid-shutdown]]
