---
title: Summary — Solar DIY Composite Pack Overview
type: summary
tags:
- pack-overview
- summaries
pack: solar-diy
retrieval_strategy: standard
---
# Summary — Solar DIY Composite Pack Overview

This is a high-level entry point for the Solar DIY ExpertPack. It combines two sub-packs into a single residential solar guide.

---

## What This Pack Covers

The Solar DIY composite pack covers the full arc of a residential solar project: from evaluating whether solar is right for your home, through equipment selection, permitting, installation, and long-term monitoring. It is structured as two sub-packs:

- **Product pack** (`product/`): What the technology IS — inverter types, panel specs, battery systems, NEC rapid shutdown requirements, system design math, troubleshooting
- **Process pack** (`process/`): How to DO it — seven project phases from site assessment through operations, plus decision frameworks and common gotcha patterns

---

## Key Facts at a Glance

| Topic | Key Number |
|-------|-----------|
| Installed cost (contractor) | $20,000–$30,000 for 6–10 kW |
| Installed cost (DIY) | $10,000–$18,000 (equipment + materials) |
| Federal ITC | 30% of total installed cost |
| Typical payback | 6–12 years |
| Project timeline | 3–9 months (permitting dominates) |
| Utility interconnection queue | 4–12 weeks (up to 6 months in CA) |
| Standard panel output 2026 | 440–500W per panel |
| Panel lifespan | 25–30 years (warranty); 40 years for Maxeon |
| String inverter lifespan | 10–15 years |
| Microinverter warranty | 25 years (Enphase) |

---

## The Two Most Important Safety Rules

1. **Never work alone on a roof** — falls from residential roofs are frequently fatal
2. **Solar conductors are live in any daylight** — treat all DC wiring as energized at all times; high-voltage DC arcs sustain themselves

---

## Navigate the Pack

**Technology questions** → start in `product/`
- How inverters work: [[inverter-types.md|`product/concepts/inverter-types.md`]]
- Panel and battery comparisons: [`product/specifications/`](../product/specifications/)
- System design math: [[system-design-fundamentals.md|`product/concepts/system-design-fundamentals.md`]]
- NEC rapid shutdown requirements: [[nec-rapid-shutdown.md|`product/concepts/nec-rapid-shutdown.md`]]
- Rapid reference definitions: [[glossary.md|`product/glossary.md`]]

**Process and how-to questions** → start in `process/`
- Should I DIY or hire? [[diy-vs-contractor.md|`process/decisions/diy-vs-contractor.md`]]
- Do I need a battery? [[grid-tied-vs-hybrid.md|`process/decisions/grid-tied-vs-hybrid.md`]]
- Which inverter type? [[inverter-topology.md|`process/decisions/inverter-topology.md`]]
- Full 7-phase roadmap: [[overview.md|`process/overview.md`]]
- Common mistakes: [[common-mistakes.md|`process/gotchas/common-mistakes.md`]]

**RAG-optimized summaries:**
- Product summary: [[product-overview.md|`product/summaries/product-overview.md`]]
- Process summary: [[process-overview.md|`process/summaries/process-overview.md`]]

**Atomic propositions (for semantic retrieval):**
- Product concepts: [[concepts.md|`product/propositions/concepts.md`]]
- Process phases: [[phases.md|`process/propositions/phases.md`]]
- Decisions & gotchas: [[decisions-gotchas.md|`process/propositions/decisions-gotchas.md`]]
- Pack-level overview: [[overview.md|`propositions/overview.md`]]

---

## The One-Sentence Answer to the Most Common Questions

**"Can I DIY solar?"** — Yes if you have electrical skills and comfort with roof work; expect 80–200 hours and save 30–50% over contractor prices.

**"Do I need a battery?"** — Not to generate solar power, but a grid-tied system without battery goes offline during grid outages. Batteries cost $4,000–$10,500 for leading 5–15 kWh systems and qualify for the 30% ITC.

**"How long does the project take?"** — 3–9 months, mostly waiting on permitting. The utility interconnection application (submit it early!) is usually the critical path.

**"Which inverter is best?"** — Microinverters (Enphase) for complex/shaded roofs. String inverters for large simple south-facing arrays. Optimizers (SolarEdge) for a middle ground.
