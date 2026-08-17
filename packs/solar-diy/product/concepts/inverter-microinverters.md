---
title: "Microinverters"
type: concept
tags: [inverter-types, microinverters, mlpe, component-selection]
pack: solar-diy-product
retrieval_strategy: standard
id: solar-diy/product/concepts/inverter-microinverters
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - inverter-types.md
related:
  - inverter-string.md
  - inverter-optimizers.md
  - nec-rapid-shutdown.md
  - system-design-fundamentals.md
content_hash: sha256:dea65b0ad327bf2ca6c4ec1fcd9e8fd61fc133cd4ebdc2f218623c96a07bbad2
---

# Microinverters

A microinverter is a per-panel AC inverter: each module converts DC to AC at the roof so panels operate independently. Enphase (IQ8 / IQ8+) dominates residential; AP Systems is the usual alternative. Microinverters are MLPE and inherently satisfy NEC rapid shutdown.

## How it works

Panel produces DC → microinverter converts to AC immediately → AC power flows to the electrical panel. Each panel operates completely independently. There is no high-voltage DC homerun on the roof (each panel converts to ~240V AC).

## Pros and cons

**Pros:** shading on one panel does not drag neighbors; no single inverter failure takes down the array; panel-level monitoring; built-in rapid shutdown; easy one-panel expansion; safer DC profile on the roof.

**Cons:** higher cost per watt than string; more roof components over 25 years; peak efficiency slightly lower than the best string inverters (~96–97% vs ~97–98%); replacement is on-roof under the module.

**Best for:** complex roofs, partial shading, systems that may grow, safety-conscious installs.

<!-- refresh
  decay: fast-moving
  as_of: 2026-Q1
  fields: [enphase_model_series, market_leadership]
  source: https://enphase.com/homeowners/microinverters
  method: "Check Enphase product page for current model series. IQ8 may be superseded by IQ9 or later. Check Solar Power World for market share shifts."
-->

## Related Concepts

- [[inverter-string]]
- [[inverter-optimizers]]
- [[nec-rapid-shutdown]]
