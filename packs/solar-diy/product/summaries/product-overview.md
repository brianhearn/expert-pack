---
title: Summary — Solar DIY Product Pack Overview
type: summary
tags:
- product-overview
- summaries
pack: solar-diy-product
retrieval_strategy: standard
id: solar-diy/product/summaries/product-overview
verified_at: "2026-04-10"
verified_by: agent
---
# Summary — Solar DIY Product Pack Overview

This summary covers all technology reference content in the Solar DIY product pack. Follow links to source files for full detail.

---

## Inverter Types — The Fundamental Architecture Decision

Residential solar uses three inverter architectures: **microinverters** (one per panel, Enphase dominates), **string inverters** (one central unit, SMA/Fronius/SolarEdge), and **string inverters with power optimizers** (SolarEdge hybrid). Microinverters and optimizers are both MLPE (Module-Level Power Electronics), which satisfies NEC rapid shutdown requirements.

The key trade-off: microinverters cost more but offer per-panel monitoring, shading resilience, and no high-voltage DC on the roof. String inverters cost 20–40% less for unshaded simple roofs. String inverters with optimizers split the difference — per-panel monitoring and MPPT, but still a central DC→AC conversion point.

→ Source: [[inverter-types.md]]

---

## NEC Rapid Shutdown — Code Requirement Every DIYer Must Know

NEC 690.12 requires all residential rooftop solar systems to reduce conductor voltage within the array boundary to ≤80V within 30 seconds of shutdown initiation — primarily for firefighter safety. This applies to building-mounted arrays only (ground mounts are exempt).

Three compliance paths: MLPE (microinverters/optimizers — compliant by design), module-level shutdown devices (added per-panel), or UL 3741 PV Hazard Control Systems. The Rapid Shutdown Initiation Device (RSID) and its labeling are required at the utility meter or AHJ-specified location.

**Critical:** Jurisdictions adopt NEC editions at different times. Always verify which NEC edition your AHJ enforces before designing.

→ Source: [[nec-rapid-shutdown.md]]

---

## System Design Fundamentals — The Four Core Calculations

Every system design requires four calculations:

1. **Array sizing** — divide annual kWh consumption by local peak sun hours, apply 75–85% derate factor
2. **String sizing** — verify cold-day Voc doesn't exceed inverter maximum, verify hot-day Vmp stays in MPPT range
3. **Battery sizing** — multiply critical load (kWh/day) × backup days ÷ usable DoD
4. **120% rule check** — solar breaker ≤ 20% of service panel bus bar rating

Use NREL's PVWatts for production estimates. String sizing errors are the most dangerous: using nominal voltage instead of temperature-corrected Voc is the most common mistake.

→ Source: [[system-design-fundamentals.md]]

---

## Solar Panels 2026 — Current Market

Standard residential panels now produce 440–500W. The market splits between:
- **Premium N-type back-contact** (Aiko, Recom, LONGi Hi-MO X10, Maxeon): 23–25% efficiency, best temperature coefficient, 25–40 year warranties, higher cost (~$0.45–0.60/W)
- **High-volume TOPCon** (Jinko, Trina, Qcells, REC): 22–24% efficiency, lower cost (~$0.25–0.35/W), still excellent for DIY

PERC panels are now largely displaced. All US-market panels must carry UL 1703 or UL 61730 listing.

→ Source: [[solar-panels-2026.md]]

---

## Battery Systems 2026 — The Top Three

All three leading systems use LFP chemistry (safer, longer-lived than NMC):

| Product | Capacity | Key Advantage | Warranty |
|---------|----------|--------------|---------|
| Tesla Powerwall 3 | 13.5 kWh | Built-in 11.5 kW inverter | 10 years |
| Enphase IQ Battery 5P | 5 kWh/module | Modular, AC-coupled, 15-yr warranty | 15 years / 6,000 cycles |
| FranklinWH aPower 2 | 15 kWh | Highest surge (185A LRA) | 15 years |

Choose based on: existing inverter compatibility, backup load requirements, and expansion plans. The 30% federal ITC applies to batteries that are primarily solar-charged.

→ Source: [[battery-systems-2026.md]]

---

## Troubleshooting & Common Mistakes

The most costly DIY product errors:
- **String sizing with nominal Voc** (not temperature-corrected) → inverter overvoltage damage
- **Missing or wrong NEC labels** → inspection failure
- **Mixed MC4 connector brands** → code violation, fire risk
- **Battery in hot unconditioned space** → warranty void, premature degradation

→ Source: [[top-diy-mistakes.md]]
