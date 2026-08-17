---
title: "String inverters with power optimizers"
type: concept
tags: [inverter-types, power-optimizers, solaredge, mlpe]
pack: solar-diy-product
retrieval_strategy: standard
id: solar-diy/product/concepts/inverter-optimizers
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - inverter-types.md
related:
  - inverter-microinverters.md
  - inverter-string.md
  - nec-rapid-shutdown.md
  - nec-rapid-shutdown-editions.md
content_hash: sha256:78ed03f8006b63d7839e15f284d987527f4035ae03a9137960e65af02fdad058
---

# String inverters with power optimizers

SolarEdge's residential architecture puts a DC-DC optimizer on each panel and keeps a central string inverter for DC-to-AC. Optimizers are MLPE, so they satisfy rapid shutdown and give panel-level MPPT without a microinverter on every module.

## How it works

Panel produces DC → optimizer runs per-panel MPPT → optimized DC goes to the central inverter → inverter converts to AC. String voltage is held in a narrower band, which simplifies the inverter.

## Pros and cons

**Pros:** per-panel optimization and monitoring; rapid shutdown built in; usually cheaper than a full microinverter array.

**Cons:** proprietary SolarEdge lock-in; the central inverter is still a single point of failure; more parts than pure string; field reports of higher warranty-claim rates as of 2025–2026; failed optimizers still mean on-roof access.

<!-- refresh
  decay: fast-moving
  as_of: 2026-Q1
  fields: [solaredge_reliability_status]
  source: r/solar, Solar Power World, SolarEdge investor relations
  method: "SolarEdge reliability concerns may improve or worsen. Check r/solar for installer sentiment and SolarEdge announcements for product revisions."
-->

**Best for:** moderate shade, panel-level monitoring without full microinverter cost, mid-range budgets.

## Choosing among the three

| Factor | Microinverter | String | String + optimizer |
|--------|:---:|:---:|:---:|
| Complex / multi-orientation roof | Best | Poor | Good |
| Partial shading | Best | Poor | Good |
| Lowest cost | Highest | Lowest | Middle |
| Rapid shutdown | Built-in | Needs addition | Built-in |
| Expandability | Easy | Harder | Medium |
| Monitoring | Panel | String | Panel |
| Single point of failure | None | Inverter | Inverter |

A newer string path is UL 3741 hazard-control (no MLPE). Adoption is early and not every AHJ accepts it — see [[nec-rapid-shutdown]].

## Related Concepts

- [[inverter-microinverters]]
- [[inverter-string]]
- [[nec-rapid-shutdown]]
