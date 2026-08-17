---
title: "NEC 690.12 editions, marking, and MLPE risk"
type: concept
tags: [nec, rapid-shutdown, ul-3741, code-compliance]
pack: solar-diy-product
retrieval_strategy: standard
id: solar-diy/product/concepts/nec-rapid-shutdown-editions
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
requires:
  - nec-rapid-shutdown.md
related:
  - nec-rapid-shutdown.md
  - inverter-string.md
  - inverter-optimizers.md
content_hash: sha256:5aa00354e0c56ac4fca3bab12e64611e99c8ea3cd7786df14a6f4ac68df5126d
---

# NEC 690.12 editions, marking, and MLPE risk

Which rapid-shutdown method you must use is an edition-and-AHJ question, not a national default. As of early 2026 most US jurisdictions are on NEC 2017 or 2020; a minority have 2023; some are still on 2014. Always ask the building department which edition they enforce.

## Edition timeline

**2014** — 690.12 first appears. Outside-the-array only. No inside-array rule.

**2017** — Inside-array 80V/30s added. MLPE was the only practical path. This edition drove Enphase and SolarEdge into default residential specs.

**2020** — UL 3741 (PV Hazard Control) linked in. String systems can comply without per-module electronics via voltage limits, firefighter-interaction protection, or both.

**2023** — Parking/carport/trellis structures exempt (no firefighter rooftop ops). Exterior-terminated non-building-attached arrays per 230.6 are not controlled conductors. Inside-array option (3) deleted — evaluate per UL 3741. Marking moved from 690.56(C) to 690.12(D). PVHCE added as an 80V/30s method.

<!-- refresh
  decay: fast-moving
  as_of: 2026-Q1
  fields: [nec_adoption_by_state, jurisdiction_counts]
  source: https://www.nfpa.org/education-and-research/electrical/nec-enforcement-maps
  method: "NFPA maintains an interactive NEC adoption map. State adoption changes as legislatures act. The next NEC edition (2026) may begin adoption cycles soon."
-->

## Marking (2023, 690.12(D))

A rapid-shutdown label at or near the main service disconnect must say the building has PV with rapid shutdown, how to initiate it, and what equipment type is used.

## Why MLPE count matters

Each MLSD multiplies connections (oxidation, dust, mating faults). Extra electronics add noise that can false-trip or mask arc-fault detection. At 0.075% annual failure (750 ppm), 4,000 MLPE devices imply 45–60 failures over 15–20 years. Replacing an optimizer means pulling modules. Ten-year-old parts may be unobtainable. That is the reliability case for UL 3741 when the AHJ will accept it.

## Related Concepts

- [[nec-rapid-shutdown]]
- [[inverter-string]]
- [[inverter-optimizers]]
