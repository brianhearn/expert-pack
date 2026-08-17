---
title: "NEC 690.12 — Rapid shutdown"
type: concept
tags: [nec, rapid-shutdown, code-compliance]
pack: solar-diy-product
retrieval_strategy: standard
id: solar-diy/product/concepts/nec-rapid-shutdown
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - nec-rapid-shutdown-editions.md
  - inverter-microinverters.md
  - inverter-optimizers.md
  - inverter-string.md
  - system-design-string-sizing.md
content_hash: sha256:2a7aa998defd9562402777a8e995592a6da3067aa50eb1614d3d84149ac8d4f3
---

# NEC 690.12 — Rapid shutdown

NEC 690.12 requires residential rooftop PV to drop voltage inside the array boundary to ≤80V within 30 seconds of shutdown, mainly so firefighters can work the roof. Compliance is MLPE (microinverters or optimizers), module-level shutdown devices, or a UL 3741 PV Hazard Control System. Which path is legal depends on the NEC edition your AHJ adopted — see [[nec-rapid-shutdown-editions]].

## Why it exists

Panels produce DC whenever they see light. You cannot switch them off like a branch circuit. Rapid shutdown is for firefighter rooftop operations. It does **not** cover installer safety during construction or maintenance (OSHA and other NEC rules do).

## The two zones

**Outside the array boundary:** controlled conductors must fall to ≤30V within 30 seconds. Required since NEC 2014; well understood.

**Inside the array boundary:** conductors must fall to ≤80V within 30 seconds. Added in NEC 2017 and revised through 2023. This is the requirement that forced MLPE onto most residential roofs.

## Current compliance methods

**MLPE.** Microinverters (Enphase IQ8, etc.) or power optimizers (SolarEdge). Each device can shut its module down. Most common residential path. A string of 5 modules with MLSD has about 2.6× more connection points than a plain string.

**Module-level shutdown devices (MLSD).** Disconnect-only boxes — no MPPT or monitoring. Cheaper than full MLPE, still adds connections.

**UL 3741 PV Hazard Control Systems.** Wire management, conduit protection, and listed system design instead of per-module electronics. Evaluated as a complete system. Fewer connections and fewer long-term MLPE failures, but many AHJs still need education before they accept it.

## Related Concepts

- [[nec-rapid-shutdown-editions]]
- [[inverter-microinverters]]
- [[inverter-optimizers]]
- [[inverter-string]]
