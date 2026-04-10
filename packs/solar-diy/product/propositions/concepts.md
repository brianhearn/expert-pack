---
title: "Propositions — Solar Product Concepts"
type: "proposition"
tags: [concepts, propositions]
pack: "solar-diy-product"
retrieval_strategy: "standard"
id: solar-diy/product/propositions/concepts
verified_at: "2026-04-10"
verified_by: agent
---

# Propositions — Solar Product Concepts

Atomic factual statements extracted from product concept and specification files.

---

### inverter-types.md

- The three main residential inverter architectures are microinverters (one per panel), string inverters (one central unit), and string inverters with power optimizers (MLPE hybrid).
- Enphase dominates the microinverter market; SolarEdge dominates the string-with-optimizer segment.
- Microinverters produce AC power at each panel; string inverters convert DC from series-connected panels to AC at a single central point.
- Both microinverters and power optimizers are classified as MLPE (Module-Level Power Electronics).
- MLPE satisfies NEC 690.12 rapid shutdown requirements; string inverters without MLPE require separate rapid shutdown devices.
- Microinverters provide panel-level monitoring, allowing per-panel production diagnosis.
- String inverters cost 20–40% less than equivalent microinverter systems for a standard unshaded roof.
- One failed microinverter reduces output by approximately 1/N of the array (where N = panel count); one failed string inverter takes the whole system offline.
- SolarEdge power optimizers are DC devices mounted under each panel; they communicate with a single string inverter via the DC bus.
- String inverters typically have a 10–15 year lifespan; Enphase microinverters carry a 25-year warranty.
- A single shaded panel in a string pulls down production for all other panels in that string; MLPE systems eliminate this "Christmas light" effect.
- Microinverter systems can be expanded one panel at a time; string inverter expansion requires verifying remaining inverter input capacity.
- SolarEdge HomeHub and Enphase IQ8 systems natively support battery integration; plain string inverters require AC coupling for battery add-on.

### nec-rapid-shutdown.md

- NEC 690.12 requires residential rooftop solar systems to reduce conductors within the array boundary to ≤80V within 30 seconds of shutdown initiation.
- NEC 690.12 applies to building-integrated or building-mounted systems only; ground-mounted arrays are not subject to rapid shutdown.
- The primary purpose of rapid shutdown is firefighter safety — allowing crews to safely access rooftops without live conductor exposure.
- Three compliance methods exist: MLPE (microinverters or power optimizers), module-level shutdown devices (MLD or PVRSS), and UL 3741 PV Hazard Control Systems.
- The rapid shutdown initiation device (RSID) must be accessible at the utility meter or another location determined by the AHJ.
- NEC 2014 only required conductors outside the array boundary to de-energize; NEC 2017 added the 80V within-array requirement.
- NEC 2023 consolidated rapid shutdown rules into a single 690.12 section and updated labeling requirements in 690.12(D).
- Parking canopy and carport structures are exempt from rapid shutdown per NEC 2023 (690.12(A)(2)).
- Jurisdictions vary in NEC edition adoption — some are on 2014 or 2017 rather than 2020 or 2023; always verify with your AHJ.
- Enphase IQ8 and all current Enphase microinverters include built-in rapid shutdown compliant with NEC 2017 and 2020.
- SolarEdge optimizers with the SetApp commissioning tool also satisfy rapid shutdown requirements without additional hardware.
- The label "SOLAR PV SYSTEM EQUIPPED WITH RAPID SHUTDOWN" is required at the RSID per NEC 690.12(D).

### system-design-fundamentals.md

- Array sizing starts with annual kWh consumption divided by local peak sun hours divided by 365 to get daily kWh target, then adjusted for system efficiency losses.
- PVWatts (NREL) is the industry-standard free tool for estimating annual solar production based on location, tilt, azimuth, and system size.
- System efficiency losses (derate factor) are typically 75–85%, accounting for wiring losses, inverter efficiency, temperature, soiling, and shading.
- String sizing must calculate both maximum voltage (cold-day Voc × temperature coefficient × number of panels) and minimum voltage (hot-day MPPT range).
- Maximum string voltage must not exceed the inverter's rated maximum input voltage (typically 600V or 1000V for residential systems).
- ASHRAE 2% design temperatures are used for cold-day voltage calculations — the temperature reached or exceeded 2% of hours.
- Battery sizing for backup is calculated by multiplying critical load (kWh/day) by backup days desired, divided by depth of discharge (DoD).
- LFP (lithium iron phosphate) batteries have a 80–100% usable depth of discharge; NMC batteries are typically limited to 80% DoD.
- The 120% rule (NEC 705.12) limits the solar breaker size to ≤20% of the service panel bus bar rating.
- A 200A bus bar panel can accommodate a maximum 40A solar breaker, supporting up to approximately 9.6 kW AC at 240V with a 25% capacity margin.
- Azimuth affects annual production significantly: south-facing (180°) maximizes annual production; east/west loses 15–20%; north loses 35–45% in northern latitudes.
- Roof pitch (tilt) affects production seasonally: steeper tilts favor winter production; shallower tilts favor summer production in northern latitudes.
- Production monitoring should compare actual kWh to PVWatts monthly estimates; a sustained >15% shortfall warrants investigation.

### solar-panels-2026.md

- Standard residential solar panels in 2026 produce 440–500W per panel, up from 300–400W in 2020.
- The residential solar panel market splits between premium back-contact N-type panels (23–25% efficiency) and high-volume TOPCon panels (22–24% efficiency).
- Back-contact cell technologies (Aiko, Recom, LONGi Hi-MO X10, Maxeon 7) place all contacts on the rear, maximizing active cell area.
- TOPCon (Tunnel Oxide Passivated Contact) uses N-type silicon with thin tunnel oxide to reduce recombination losses.
- PERC panels (P-type with rear passivation) dominated 2018–2022 but are now largely displaced by N-type technologies at similar price points.
- Typical residential panel prices in 2026: value TOPCon at ~$0.25–0.35/W, premium back-contact at ~$0.45–0.60/W (panel only, not installed).
- Maxeon offers a 40-year product and performance warranty — the longest in the residential market.
- JinkoSolar, Trina Solar, Qcells, and REC are the leading high-volume TOPCon brands for residential installations.
- Temperature coefficient (Pmax) measures production loss per degree Celsius above 25°C; N-type panels have better (lower) temperature coefficients than P-type PERC.
- A temperature coefficient of -0.30%/°C means a panel rated at 400W at 25°C produces ~388W at 55°C (typical NOCT conditions).
- All panels marketed in the US must carry UL 1703 or UL 61730 safety listing.
- Panel efficiency is the percentage of incident sunlight converted to electricity; 22% efficiency means 220W per square meter at STC.
- Higher efficiency panels reduce roof space required per kW: 440W panels at 22% efficiency occupy ~2m² vs ~2.5m² for an equivalent 300W 19% panel.

### battery-systems-2026.md

- The three leading residential batteries in 2026 are Tesla Powerwall 3 (13.5 kWh, $9,200), Enphase IQ Battery 5P ($4,000/5 kWh module), and FranklinWH aPower 2 (15 kWh, ~$10,500).
- All three leading battery systems use LFP (lithium iron phosphate) chemistry, which is safer, longer-lasting, and more temperature-tolerant than NMC.
- Tesla Powerwall 3 includes a built-in 11.5 kW solar inverter, replacing a separate string inverter for integrated hybrid systems.
- Enphase IQ Battery 5P is modular — add blocks in 5 kWh increments; each block has its own internal microinverter for AC coupling.
- FranklinWH aPower 2 has the highest surge capability (185A LRA) of the leading residential systems, supporting whole-home loads including well pumps.
- Tesla Powerwall 3 has a 10-year warranty; Enphase IQ Battery 5P and FranklinWH have 15-year warranties.
- Battery capacity ratings are usable kWh, not gross kWh; LFP batteries are typically rated at 90–100% usable depth of discharge.
- Time-of-use (TOU) arbitrage — charging at cheap off-peak rates and discharging at peak rates — can generate ROI independent of solar production.
- A standard 13.5 kWh battery provides backup for approximately 1–2 days of essential loads (refrigerator, lights, phone charging, internet).
- DC-coupled batteries (connected to the DC bus of a hybrid inverter) are slightly more efficient than AC-coupled (connected to the AC bus).
- AC-coupled batteries (including Enphase IQ Battery) can be added to any existing grid-tied system without replacing the inverter.
- The federal ITC (30%) applies to battery systems if charged primarily by solar (>75% solar-charged per IRS guidelines).
- Operating temperature limits: Tesla Powerwall 3 (32°F–122°F / 0°C–50°C); installing in unconditioned spaces exceeding these limits voids the warranty.
