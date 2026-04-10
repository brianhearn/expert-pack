---
title: "Phase 3: Component Selection"
type: "phase"
tags: [battery-systems-2026, inverter-types, permitting, phase-3-component-selection, process, solar-panels-2026, system-design]
pack: "solar-diy-process"
retrieval_strategy: "atomic"
id: solar-diy/process/phases/03-component-selection
verified_at: "2026-04-10"
verified_by: agent
---

# Phase 3: Component Selection

<!-- context: section=process, topic=phase-3-component-selection, related=solar-panels-2026,battery-systems-2026,inverter-types,system-design,permitting -->

> **Lead summary:** Component selection takes your system design spec and turns it into a specific bill of materials. The five main component categories are panels, inverter, battery (if included), racking/mounting, and balance-of-system (BOS) electrical hardware. Each category has real tradeoffs; this phase walks through selection criteria, common choices, and pitfalls. Order equipment only after your permit application is in (or close) — equipment specs appear on permit drawings.

## Procurement Timing

A common mistake: ordering everything the day you make your decisions. Before placing major orders:
1. Finalize your permit application (it requires specific equipment documentation)
2. Get your permit approved (or at minimum submitted) before scheduling installation
3. Verify that your chosen equipment is available with reasonable lead times (some inverters and batteries have 4–12 week waits)
4. Check for price changes — panel and inverter prices fluctuate with tariffs and supply chain

It's acceptable to order racking, BOS hardware, and panels after permit submittal. Hold off on the battery order until permit approval if budget is tight — battery costs are high and policies sometimes change during review.

## 1. Solar Panels

### Selection Criteria
| Criterion | What to Look For |
|-----------|-----------------|
| Wattage | Higher wattage = fewer panels for same output (400–500W range in 2026) |
| Efficiency | Higher = smaller physical footprint for same output; matters for constrained roofs |
| Cell technology | TOPCon: mainstream efficiency; HJT: high efficiency, excellent temp coefficient; BC: highest efficiency, premium cost |
| Temperature coefficient | Closer to 0%/°C is better (less production loss on hot days); HJT best in class |
| Degradation rate | Linear warranty matters; look for <0.5%/year (0.25–0.4% is current best-in-class) |
| Product warranty | 25–30 years is standard; verify the manufacturer has US presence for warranty service |
| Power warranty | 80–90% at 25 years is standard; 86–90% represents best-in-class |

### Brands and Tier
Tier 1 refers to bankability (Bloomberg tier 1 = financially stable manufacturer). It does NOT mean best quality — it means the company is likely to honor warranties.

**US market leaders (2026):**
- **Qcells (Hanwha)**: Made-in-USA options (Georgia facility), solid quality, competitive pricing
- **REC**: Norwegian-owned, premium quality, excellent temperature coefficient
- **Jinko, Longi**: Chinese manufacturers, large market share, competitive pricing, Tier 1
- **Canadian Solar**: Chinese-owned, long track record, good value
- **SunPower / Maxeon**: Premium back-contact panels, highest efficiency, premium cost, US-founded

**For DIY buyers:** Availability from wholesale distributors (Sonepar, Rexel, CED, local solar distributors) matters. Some brands are installer-channel only and hard to get without a contractor account.

### What to Avoid
- Unknown/unverified manufacturers with no US service infrastructure
- Panels with shorter than 25-year product warranties
- Panels where the importer is a shell company (warranty worthless if they close)
- Damaged panels (shipping damage voids warranties)

## 2. Inverter

Your inverter architecture was decided in Phase 2. Now select the specific model.

### String Inverter Selection
| Spec | What to Match |
|------|--------------|
| Max input voltage | Must exceed your calculated worst-case string Voc (with safety margin) |
| MPPT range | Must encompass your calculated string Vmp at temperature extremes |
| Max input current per MPPT | Must accommodate your panel Isc × 1.25 NEC factor × number of strings |
| AC output | Match to your service panel capacity and interconnection agreement |
| CEC efficiency | Higher is better; 97–99% is current best-in-class |
| Rapid shutdown | Must comply with NEC 2017/2020/2023 690.12 for your jurisdiction |

**Major brands:** SMA, Fronius, SolarEdge (with optimizers), Growatt (budget), Solis (budget)

### Microinverter Selection
- Match microinverter max input power to your panel wattage (most support 125–160% panel oversizing)
- Verify CEC rating at your grid voltage (240V for US residential)
- Check trunk cable compatibility for your roof run lengths
- Enphase IQ8 series is the dominant market option; also consider APSystems

### Battery-Ready Inverters
If you're not adding battery now but may later, consider a hybrid inverter that supports DC battery coupling. This avoids replacing the inverter when you eventually add storage.

**Hybrid inverter brands:** Enphase IQ Battery (uses microinverter ecosystem), SolarEdge Home Hub, Sol-Ark, Schneider Electric, Victron Energy (off-grid/hybrid specialty)

## 3. Battery System (if applicable)

See `../../product/specifications/battery-systems-2026.md` for detailed specs.

### Selection Criteria
| Criterion | What to Look For |
|-----------|-----------------|
| Usable capacity | Match to your backup load × backup duration (from Phase 2 sizing) |
| Continuous power | Must cover your largest simultaneous loads |
| Surge capacity | Must handle motor starting loads (A/C LRA check) |
| Chemistry | LFP: safer, longer cycle life, better for daily cycling; NMC: higher energy density |
| Coupling type | AC-coupled: more flexible installation; DC-coupled: more efficient, requires compatible inverter |
| Warranty | 10 years / 70% remaining capacity is standard; verify throughput warranty if cycling daily |
| Backup capability | AC-coupled batteries can back up the grid-tied inverter; verify this with both manufacturers |

### AC-Coupled vs DC-Coupled
- **AC-coupled** (Powerwall 3, Enphase IQ): Battery connects at AC side; works with most grid-tied inverters; slightly less efficient (each DC-AC-DC conversion loses ~3–5%)
- **DC-coupled** (Sol-Ark, SolarEdge Home Hub): Battery connects at DC side before inverter; more efficient; requires a compatible hybrid inverter

For most DIY retrofits and new installs with standard grid-tied inverters, AC-coupled is simpler and more flexible.

## 4. Racking and Mounting

Racking is the structural system that attaches panels to your roof. Choose based on roof type.

### Comp Shingle (Most Common)
- L-foot mounts with flashing (penetration mounts) — industry standard
- **Brands:** Iron Ridge, Unirac, Ecofoot, QuickMount PV
- Use Code-compliant flashing (QuickBOLT or similar with LABC/ICC ESR listing)
- Rails: most installers use 1.5" or 2.5" extrusion; 2.5" for long runs with wind/snow loads
- Ensure rail splices are centered between mounts, not directly on mounts

### Standing Seam Metal
- S-5! clamp mounts — no penetrations required, fastest install
- Verify clamp compatibility with your specific seam profile

### Flat Roof
- Ballasted racking (no penetrations) — calculate wind uplift for your zone; ballast weights are significant
- Low-profile flush (minimal penetrations) — better for commercial; some residential applications

### Ground Mount
- Top-of-pole or ground-mount racking: more expensive but no roof penetrations, better shading control, easier maintenance
- Requires concrete footings (engineered)
- May require separate electrical permit and trenching for wire run to house

## 5. Balance of System (BOS) Hardware

The wiring, overcurrent protection, and disconnects that complete the electrical system.

### DC Side (Array to Inverter)
- **PV wire**: USE-2 or PV Wire, 600V or 1000V rated; minimum 10 AWG for most residential strings
- **MC4 connectors**: Use manufacturer-matched connectors; mixing brands is a code violation and fire hazard
- **String combiners**: Needed for 3+ strings; includes fusing
- **DC disconnect**: Required by code at the inverter; many inverters include this

### AC Side (Inverter to Panel)
- **Conduit**: EMT (indoors/in conduit), PVC (outdoor/underground), or direct-burial wire
- **Service entrance equipment**: Verify your main service panel has space for a solar breaker (NEC 705.12 bus bar calculation)
- **Production meter**: Required by most utilities; installer usually handles this
- **AC disconnect**: Required outside at meter by most utilities; lockable

### Rapid Shutdown
Per NEC 2017/2020/2023 Section 690.12, you need a rapid shutdown system for rooftop arrays. Options:
- Microinverters and most modern power optimizers are compliant by default
- String inverters require a separate rapid shutdown device (e.g., Tigo, SolarEdge TS4 rapid shutdown module) **unless** the inverter is within 1 foot of the array boundary

### Wire Sizing
Wire sizing follows NEC 690 and 310. Key rules:
- Size DC wires to 156% of the panel's Isc (NEC 690.8)
- Size AC wiring per inverter nameplate current × 125% (NEC 705)
- Voltage drop: aim for <2% on DC, <1.5% on AC conductors

## Phase 3 Output: Bill of Materials

Before submitting your permit application, you'll have:
- Panel model, wattage, count, and datasheet
- Inverter model and datasheet / cut sheet
- Battery model and datasheet (if applicable)
- Racking system and mounting hardware specs
- Wire sizes and conduit runs planned
- All UL listings confirmed (UL 1703 for panels, UL 1741 for inverters, UL 9540 for batteries)

## Related

- Panel specs: `../../product/specifications/solar-panels-2026.md`
- Battery specs: `../../product/specifications/battery-systems-2026.md`
- Inverter types: `../../product/concepts/inverter-types.md`
- Phase 4: `04-permitting.md`
