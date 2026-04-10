---
title: Summary — Solar DIY Process Pack Overview
type: summary
tags:
- process-overview
- summaries
pack: solar-diy-process
retrieval_strategy: standard
id: solar-diy/process/summaries/process-overview
verified_at: "2026-04-10"
verified_by: agent
---
# Summary — Solar DIY Process Pack Overview

This summary covers all seven project phases plus decisions and gotchas. Follow links to source files for full detail.

---

## The Seven-Phase Arc

A residential solar project spans 3–9 months across seven sequential phases. The critical path is usually the utility interconnection application (4–12 weeks), not the build itself. Most timeline waste comes from sequential rather than parallel permitting.

| Phase | Duration | Critical Action |
|-------|----------|----------------|
| 1 — Site Assessment | 1–2 weeks | Shading analysis, roof evaluation |
| 2 — System Design | 2–4 weeks | String sizing calculations, single-line diagram |
| 3 — Component Selection | 1–2 weeks | BOM finalized, equipment ordered |
| 4 — Permitting | 4–12 weeks | Building permit + utility interconnection (run in parallel!) |
| 5 — Installation | 2–5 days | Physical installation work |
| 6 — Inspection & Commissioning | 2–8 weeks | AHJ inspection, utility meter swap, PTO |
| 7 — Operations & Maintenance | Ongoing | Monitoring, cleaning, annual inspection |

→ Source: [[overview.md|process/overview.md]]

---

## Phase 1: Site Assessment — Know Before You Design

Four areas to evaluate: roof condition and orientation, shading analysis, structural capacity, utility interconnection feasibility.

- South-facing roof at 20–35° pitch is ideal
- Roofs 15+ years old should be replaced before solar
- Shading analysis required for worst-case months (November–January), not just summer
- Submit utility interconnection inquiry early — some areas have 6–18 month queues

→ Source: [[01-site-assessment.md]]

---

## Phase 2: System Design — The Math That Matters

Four outputs required: load analysis, array sizing, string sizing table, battery sizing. The most critical and most error-prone is **string sizing**.

String sizing must satisfy TWO constraints simultaneously:
1. Max string voltage (cold Voc × panels) ≤ inverter max input voltage
2. Min MPPT voltage (hot Vmp × panels) ≥ inverter MPPT minimum

Use ASHRAE 2% design temperatures for cold-day calculations. When in doubt, reduce string length by one panel — conservative is safe, overvoltage is dangerous.

→ Source: [[02-system-design.md]]

---

## Phase 3: Component Selection — BOM to Build

Five component categories: panels, inverter, battery (optional), racking, BOS electrical hardware. Order only after permit application is in (or nearly submitted). Buy from solar wholesale distributors (CED Greentech, SunWatts) for commercial-grade equipment with proper UL documentation.

Racking must carry an ICC ESR for your roof type and local wind/snow loads. Register all equipment warranties before installation.

→ Source: [[03-component-selection.md]]

---

## Phase 4: Permitting — The Critical Path

Two applications to submit in parallel:
- **Building permit** (AHJ): requires SLD, site plan, equipment spec sheets; takes 1–4 weeks
- **Utility interconnection** (PTI/PV Agreement): takes 4–12 weeks, sometimes 6 months

The utility process is almost always the critical path. Starting it the same week as the building permit saves 4–10 weeks. Resolve the 120% rule and supply-side vs. load-side connection question during design, not permitting.

→ Source: [[04-permitting.md]]

---

## Phase 5: Installation — Safety First

Work sequence: roof mounts → rails → panels → DC wiring → inverter/battery → AC wiring → grounding → labeling.

**Non-negotiable safety rules:**
- Fall protection required (OSHA: 6 feet) — harness, anchor, lanyard
- Never work alone on a roof
- Solar conductors are live in any light — treat all DC wiring as energized
- High-voltage DC arcs sustain themselves (unlike AC); treat it with extra caution

Most common installation errors: missing labels, MC4 brand mixing, sheathing-only lag bolts, improper flashing.

→ Source: [[05-installation.md]]

---

## Phase 6: Inspection & Commissioning — Two Gates to PTO

AHJ inspection → utility inspection → PTO letter → net meter swap → system energized.

- Missing labels are the #1 inspection failure cause; use an NEC-compliant label kit
- Wait for the utility to install the bidirectional net meter before exporting
- The federal ITC (30%) is claimed on IRS Form 5695 for the tax year of commissioning
- Set up monitoring alerts immediately after commissioning; don't assume it's working without verification

→ Source: [[06-inspection-commissioning.md]]

---

## Phase 7: Operations & Maintenance — Long-Term Stewardship

The system is largely self-managing, but monitoring and annual inspection prevent costly surprises.

- Set up "no production" and "low production" alerts in the monitoring platform on day one
- Annual production should track within ±15% of PVWatts estimate; sustained shortfall warrants investigation
- Clean panels once or twice per year; quarterly in desert climates; use plain water and soft brush only
- String inverters (10–15 year lifespan) should be budgeted for replacement around year 15
- Document degradation year-over-year; >1%/year sustained degradation is a warranty claim trigger

→ Source: [[07-operations-maintenance.md]]

---

## Key Decisions

**DIY vs. Contractor:** DIY saves 30–50% of cost. Most DIYers hire an electrician for service panel work only. Requires electrical experience, comfort with roof work, and time (80–200 hours).

**Grid-Tied vs. Hybrid:** Grid-tied is less expensive but provides no backup power. Hybrid adds battery. Off-grid requires 3–10× more battery capacity. Net metering policy changes (NEM 3.0 in CA) are making battery economics better.

**Inverter Topology:** Microinverters for complex/shaded roofs. String inverters for large simple unshaded arrays (cost savings). Optimizers for a middle ground.

→ Sources: [[diy-vs-contractor.md]] | [[grid-tied-vs-hybrid.md]] | [[inverter-topology.md]]

---

## Top Gotchas

1. Mounting on an old roof — costs $2,000–$6,000 for panel removal during re-roofing
2. Underestimating winter shading (trees, dormers) from summer site visits
3. Sizing for current loads, not future EV/heat pump additions
4. String sizing with nominal Voc (not temperature-corrected)
5. Sequential permit submissions instead of parallel (wastes 4–10 weeks)
6. Failing to confirm separate net metering enrollment after interconnection

→ Source: [[common-mistakes.md]]
