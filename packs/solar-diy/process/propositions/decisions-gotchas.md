---
title: "Propositions — Solar Process Decisions & Gotchas"
type: "proposition"
tags: [decisions-gotchas, propositions]
pack: "solar-diy-process"
retrieval_strategy: "standard"
id: solar-diy/process/propositions/decisions-gotchas
verified_at: "2026-04-10"
verified_by: agent
---

# Propositions — Solar Process Decisions & Gotchas

Atomic factual statements from decision and gotcha files.

---

### decisions/diy-vs-contractor.md

- DIY solar saves 30–50% of installed cost, typically $8,000–$20,000 on a residential system.
- The most dangerous DIY task is service panel work — it requires working near live 200A buses; many DIYers hire an electrician for this step only.
- Roof work and high-voltage DC both carry fatal risk; both require proper safety equipment and a second person present.
- Skilled DIYers with electrical experience typically spend 80–200 hours on a 6–10 kW installation.
- A hybrid approach — DIY everything except the panel-to-service-panel AC connection — is common and can meet contractor requirements for warranty on some equipment.
- Most residential permit offices accept homeowner-pulled permits for owner-occupied homes, though some jurisdictions require a licensed electrical contractor.
- A contractor-installed system typically costs $3.50–$4.50/W installed; DIY typically achieves $1.50–$2.50/W in equipment and materials.
- DIY voids some equipment installer warranties; check manufacturer warranty terms before ordering.

### decisions/grid-tied-vs-hybrid.md

- Grid-tied (no battery) systems are the least expensive and most common configuration; they cannot provide backup power during grid outages.
- Hybrid systems (grid-tied + battery) provide backup capability and enable bill optimization through time-of-use arbitrage.
- Off-grid systems are sized for the worst solar months (December–January) and require 3–10× more battery capacity than hybrid systems.
- Net metering rate reductions (NEM 3.0 in California, similar cuts in Nevada, Arizona) are accelerating battery adoption by reducing the value of grid export.
- A grid-tied system without anti-islanding protection is illegal and dangerous; all grid-tied inverters must auto-disconnect on grid outage (UL 1741 requirement).
- Hybrid inverters with energy storage interfaces include SolarEdge StorEdge, Solax, Fronius Primo/Symo GEN24, and Tesla Powerwall 3 (all-in-one).
- The economics of hybrid vs grid-tied shift significantly depending on local electricity rates, TOU tariff structure, and utility incentives for battery.
- Battery-only retrofits (adding storage to an existing grid-tied system) are possible using AC-coupled solutions like Enphase IQ Battery or Tesla Powerwall (with existing gateway).

### decisions/inverter-topology.md

- Microinverters are the installer-friendliest choice: no string sizing calculations, native rapid shutdown compliance, and no high-voltage DC runs on the roof.
- Shaded or complex roofs (dormers, multiple roof planes, chimneys) benefit most from microinverter or optimizer solutions.
- A simple south-facing unshaded array with a single roof plane is the optimal use case for a plain string inverter — maximum cost savings, no MLPE needed.
- Power optimizers (SolarEdge) provide individual panel MPPT and monitoring but require a compatible string inverter; the DC bus still runs at optimizer-set voltage.
- String inverters without MLPE require additional rapid shutdown devices to meet NEC 2017+ requirements; this adds cost and complexity.
- For large systems (15 kW+), string inverters remain significantly less expensive than full microinverter solutions.
- The Enphase IQ8 series (IQ8M, IQ8H, IQ8X) supports off-grid operation and microinverter-level islanding without a battery, using Ensemble technology.

### gotchas/common-mistakes.md

- Mounting solar on a roof that will need replacement in <10 years costs $2,000–$6,000 extra for panel removal and reinstallation during re-roofing.
- Shading analysis must cover the worst shading months, not just peak summer; a tree shadow at 10 AM in December can halve winter production.
- Sizing for current consumption (not future loads) is a common mistake; systems become undersized immediately when an EV is added.
- Using nominal voltage (not temperature-corrected Voc) for string sizing is dangerous — cold-morning Voc can exceed inverter max by 10–20%.
- The 120% rule violation (oversized solar breaker for the panel bus bar) is a leading cause of permit rejections.
- Submitting the utility interconnection application after (not in parallel with) the building permit wastes 7–10 weeks of timeline.
- Net metering enrollment is a separate process from interconnection agreement submission at many utilities; confirm enrollment explicitly.
- A field change (even shifting a row a few feet) must be reflected in permit drawings before inspection or the inspection will fail.
- Jurisdictions adopt different NEC editions; a 2023 NEC code design presented to a 2017-edition jurisdiction may have unnecessary (not just correct) requirements.
- Mixed-brand MC4 connections are a known fire cause due to dimensional tolerance differences that create internal arcing over time.
- LFP batteries operated outside their rated temperature range (especially above 50°C / 122°F in summer garages) risk premature degradation and void warranties.
- Failing to configure monitoring alerts on day one means system faults can go undetected for months, silently reducing production and ROI.
