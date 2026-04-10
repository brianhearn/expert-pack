---
title: "Propositions — Solar Process Phases"
type: "proposition"
tags: [phases, propositions]
pack: "solar-diy-process"
retrieval_strategy: "standard"
id: solar-diy/process/propositions/phases
verified_at: "2026-04-10"
verified_by: agent
---

# Propositions — Solar Process Phases

Atomic factual statements extracted from the seven process phase files.

---

### phases/01-site-assessment.md

- A thorough site assessment covers four areas: roof condition and orientation, shading analysis, structural capacity, and utility interconnection feasibility.
- South-facing roofs (azimuth ~180°) at 20–35° pitch maximize annual production in the continental US.
- A roof 15+ years old or showing signs of wear should be replaced before solar installation to avoid costly panel removal during re-roofing.
- Shading analysis must be conducted at solar noon for the worst shading months (November–January) in the northern hemisphere.
- A shading analysis tool (Solmetric SunEye, Solar Pathfinder app, or PVGIS) is required for accurate production estimates.
- Trees within 30 feet of the array that are still growing should be accounted for in 10-year shading projections.
- Structural capacity evaluation is required for most jurisdictions; most residential roofs with standard 24" rafter spacing can support solar arrays without modification.
- Interconnection feasibility means confirming the utility will accept a grid-tied connection; some utilities have interconnection queues that add 6–18 months to timelines.
- Utility interconnection capacity limits apply in some high-solar-penetration areas; submitting the interconnection application early (Phase 1–2) avoids surprises.
- Equipment such as chimneys, vents, and HVAC units create setback requirements (typically 18" per NEC 690.10 for access and egress pathways).

### phases/02-system-design.md

- System design produces four key outputs: a load analysis (annual kWh target), an array sizing calculation, a string sizing table, and a battery sizing estimate.
- Annual load analysis starts with 12 months of utility bills to calculate average daily kWh consumption.
- System size should be designed for the 5-year future load, including planned EV charging, heat pump, or pool equipment additions.
- PVWatts is used to calculate the system kW-DC needed to produce the target annual kWh, given the site's location, orientation, and tilt.
- String sizing calculations require panel Voc, temperature coefficient, ASHRAE design temperatures, inverter MPPT range, and inverter maximum input voltage.
- String design must satisfy: (max string voltage) ≤ inverter max input AND (min MPPT voltage) ≤ (min string voltage) ≤ (max MPPT voltage).
- Battery sizing for full backup requires load profiling: which circuits will be backed up and what their combined daily kWh consumption is.
- Wire sizing must follow NEC 690 requirements: PV source circuits typically require conductors rated 125% of short-circuit current (Isc) × 1.25 for conduit fill.
- The single-line diagram (SLD) produced in Phase 2 is the primary document submitted with the building permit application.

### phases/03-component-selection.md

- The five main component categories for a solar system BOM are: panels, inverter, battery (optional), racking/mounting hardware, and balance-of-system (BOS) electrical hardware.
- BOS electrical hardware includes: wire/conduit, combiners, disconnects, circuit breakers, labels, MC4 connectors, junction boxes, and grounding hardware.
- Equipment should be ordered only after the building permit application is submitted (or at minimum, after the design is finalized), because permit drawings list specific equipment.
- Racking systems must carry an ICC ESR (Evaluation Service Report) listing for the roof type and the local wind and snow loads.
- Racking load ratings are specific to roof type and lag bolt size; do not substitute hardware without verifying the ESR.
- For US grid-tied systems, all inverters must be UL 1741 listed (domestic use) or UL 1741 SA listed (advanced inverters with grid support functions).
- Purchasing from a solar wholesale distributor (CED Greentech, SunWatts, BayWa) rather than Amazon or Home Depot provides access to commercial-grade equipment with proper documentation.
- Equipment warranties require manufacturer registration within 30–90 days of installation; register equipment before starting installation.

### phases/04-permitting.md

- A residential solar permit application typically requires: a single-line diagram (SLD), a site plan (roof layout with dimensions and setbacks), and product spec sheets for all major components.
- Most jurisdictions use SolarPermit.org or a local variant for expedited online permits; requirements vary by county and state.
- The building permit process takes 1–4 weeks in most jurisdictions; utility interconnection takes 4–12 weeks (and up to 6 months in congested areas).
- Both permit applications (building and utility interconnection) should be submitted simultaneously to run in parallel.
- The utility interconnection application (PV Interconnection Agreement or PTI) includes: inverter size, system kW-DC, estimated annual production, and a one-line diagram.
- NEC 705.12 (the 120% rule) determines whether a supply-side or load-side connection is used — this must be resolved during design, not permitting.
- Supply-side connections (before the main breaker) bypass the 120% rule but require a fusible disconnect and have other requirements.
- HOAs in most US states can impose aesthetic restrictions on solar (e.g., black-on-black panels only) but generally cannot prohibit solar installations.

### phases/05-installation.md

- Installation proceeds in logical sequence: roof mounts → rails → panel mounting → DC wiring → inverter → battery → AC wiring → grounding → labeling.
- Fall protection (harness, roof anchor, lanyard) is required at 6 feet height per OSHA standards; no exceptions for DIY work.
- Never work alone on a roof — always have a second person present who can contact emergency services.
- Solar string conductors (PV wire) are energized whenever there is light, including dim daylight; treat them as live at all times.
- High-voltage DC is more dangerous than AC because DC arcs sustain themselves; AC arcs extinguish at zero crossings.
- Roof lag bolts must achieve minimum 2.5" embedment into rafter wood; sheathing-only attachment will fail under wind load.
- L-foot roof mounts must be flashed per manufacturer instructions: shingle above over the top of the flashing, shingle below under the bottom of the flashing foot.
- MC4 connectors must be from the same manufacturer throughout a string; mixing brands is a code violation and a fire risk.
- NEC 690 requires extensive labeling: panels, source circuit conductors at all junction points, DC disconnect, AC disconnect, solar breaker, rapid shutdown initiation device, and conduit (every 10 feet).
- The main service panel solar breaker should be turned off and verified deenergized with a multimeter before any service panel wiring work.
- String systems should have open-circuit voltage measured at each string before connecting to the inverter; verify polarity and expected voltage range.

### phases/06-inspection-commissioning.md

- Two inspections must pass before operating a grid-tied solar system: AHJ (building/electrical) inspection and utility interconnection inspection.
- The AHJ inspection verifies code compliance: panel layout, racking, labeling, rapid shutdown, grounding, and service panel connection.
- The utility inspection verifies interconnection agreement compliance and triggers the meter swap to a bidirectional net meter.
- Missing NEC labels are the #1 cause of AHJ inspection failures.
- The utility issues a PTO (Permission to Operate) letter after both inspections pass; the system must not be energized for export before PTO.
- Wait for the utility to install a bidirectional net meter before exporting power; running export without a net meter creates billing disputes.
- The federal Investment Tax Credit (30%) is claimed on IRS Form 5695 in the tax year the system is placed in service.
- SREC (Solar Renewable Energy Certificate) markets in NJ, MA, PA, MD, and DC allow homeowners to sell certificates for additional income.
- The IRS "placed in service" date for the ITC is the date the system is commissioned and operational, not the purchase date.
- String inverter commissioning requires measuring open-circuit voltage at the DC inputs before connection, then powering up AC then DC disconnects in sequence.
- Monitoring should be configured on day one; set up no-production and low-production alerts immediately after commissioning.

### phases/07-operations-maintenance.md

- Solar panel production varies seasonally: winter production is typically 40–70% of summer production in most US locations.
- Year-one production will typically be within ±15% of the PVWatts annual estimate; a sustained >15% shortfall warrants investigation.
- Typical panel degradation is 0.3–0.5%/year for quality panels after the first year; first-year LID (Light-Induced Degradation) may cause an additional 1–2% loss.
- Panel cleaning is recommended once or twice per year (spring and fall) in most climates; quarterly in dusty desert climates.
- High-pressure washers should not be used on solar panels — they can damage panel coatings and compromise junction box moisture seals.
- String inverters have a typical lifespan of 10–15 years and should be budgeted for replacement around year 15.
- Enphase microinverters carry a 25-year warranty designed to match panel lifespan.
- Annual visual inspection checklist: panel security, racking integrity, roof mount condition, conduit integrity, no vegetation encroachment.
- Hotspots (dark areas on individual cells, visible in strong light) indicate cracked cells or delamination and should be documented and reported for warranty claims.
- Battery state of health (SOH) should be monitored via the manufacturer's app; capacity loss >20% before warranty expiration is a valid warranty claim.
- LFP batteries rated for 3,000–6,000 cycles to 80% SOH; daily cycling (TOU arbitrage) depletes cycle life faster than weekly backup cycling.
- After major weather events (hail, high winds), inspect panels for cracks and racking for shifted components.
