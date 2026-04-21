---
title: "Phase 5: Installation"
type: "phase"
tags: [common-mistakes, dc-wiring, inspection-commissioning, nec-rapid-shutdown, permitting, phase-5-installation, process, racking]
pack: "solar-diy-process"
retrieval_strategy: "atomic"
id: solar-diy/process/phases/05-installation
verified_at: "2026-04-21"
verified_by: agent
schema_version: "4.1"
concept_scope: single
---

# Phase 5: Installation

<!-- context: section=process, topic=phase-5-installation, related=nec-rapid-shutdown,permitting,inspection-commissioning,common-mistakes,racking,dc-wiring -->

> **Lead summary:** Installation day(s) are the most physically demanding part of the project but, with good preparation, among the most straightforward. The work proceeds in a logical sequence: roof penetrations and racking → panel mounting → DC wiring → inverter and battery → AC wiring and service panel → grounding and labeling. Safety is paramount — roof work and high-voltage DC are both lethal hazards. Work with a partner. Never work alone on a roof.

## Pre-Installation Checklist

Before anyone climbs on the roof:
- [ ] Building permit approved and posted (required for inspection)
- [ ] All materials on-site and verified against BOM
- [ ] Layout staked out and double-checked against permit drawings
- [ ] Weather forecast confirmed (no rain, wind <15 mph, extreme temperature)
- [ ] Roof safety equipment on hand: fall protection harness, ridge anchor, lifelines
- [ ] Labeling materials ready: per NEC 690, panels and source circuits require labels at install time
- [ ] Main service panel breaker can be turned off (verify with a multimeter after shutoff)

## Safety Fundamentals

### Roof Work
- **Fall protection is not optional** — a residential fall is fatal or life-altering. OSHA requires fall protection at 6 feet. Use a properly rated roof anchor, harness, and lanyard.
- Work in teams of at least two; one person should be able to contact emergency services at all times
- Never walk on panels — they crack easily and the aluminum frame edges are sharp
- Composition shingle can be slippery when wet or cold; avoid damp conditions

### Electrical Safety
- **High-voltage DC is more dangerous than AC** — solar strings can produce 300–600+ VDC. DC arcs sustain themselves unlike AC arcs that extinguish at zero crossings. A DC arc at panel-level voltage can kill.
- Wear insulated gloves (class 00 or class 0 rubber gloves) when handling live DC wiring
- Before working on any wiring, verify the circuit is deenergized with an appropriately rated meter
- Cover panels with opaque tarps to reduce voltage during installation if practical
- String conductors are energized whenever there is light — even dim daylight

## Step 1: Layout and Racking

### Mark Rafter Locations
- Use a stud finder from the attic side or find rafter tails at the eave
- Mark rafter centerlines on the roof surface with chalk line
- Typical residential rafters: 16" or 24" on center

### Snap Layout Lines
- Measure and snap chalk lines for the bottom rail and top rail positions
- Verify the layout matches your permit drawings (setbacks from ridge, eaves, rakes)
- Double-check that mount locations will hit rafter centers (critical for structural integrity)

### Install Roof Mounts
- Flash each mount penetration correctly — this is the most common source of roof leaks from solar installs
- **For L-foot mounts on shingles**: remove or lift the shingle above the mount location, apply butyl tape sealant, drive lag bolt into rafter center (minimum 2.5" embedment into rafter wood), apply more sealant, reinstall shingles over the flashing foot
- Torque lag bolts to manufacturer spec (typically 12–15 ft-lb for standard L-feet)
- Verify each mount is tight and the flashing is properly integrated under shingles above and over shingles below

### Attach Rails
- Slide rails onto L-foot standoffs
- Level rails front-to-back and along the row (a 4-foot level is your friend)
- Connect rail splices at midpoint between mounts
- Leave a small thermal expansion gap at rail splices (~1/8")
- Verify all rail hardware is torqued per manufacturer specs

## Step 2: Panel Mounting

### Grounding
- Install ground wire through the rail system before panels
- Use manufacturer-approved bonding hardware (bare copper or tinned copper, no aluminum)
- Many modern racking systems include integrated bonding; verify your system's compliance method

### Hang Panels
- Work from top of array downward to avoid stepping on mounted panels
- Start at the end of a row to ensure alignment
- Set each panel in mid-clamps and end-clamps; do not fully tighten until the entire row is positioned
- Check panel alignment (rows and columns) before final torque
- Torque all clamps per manufacturer spec — typically 8–12 ft-lb for mid-clamps

### Panel Orientation
- Most panels are installed in portrait orientation (long side vertical) — reduces racking costs
- Landscape orientation may be needed for some roof configurations or microinverter wiring
- Verify orientation matches permit drawings — inspectors check this

## Step 3: DC Wiring

### Microinverter Systems
- Attach microinverters to rails before or during panel mounting
- Route AC trunk cable along rails (clips every 3–4 feet)
- Connect each microinverter to trunk cable at panel location
- Seal any penetrations through roof deck with approved sealant
- Run trunk cable to combiner/junction box at roof edge

### String Systems (String Inverter or Optimizer)
- Route PV wire from panels along rails using UV-resistant clips or wire clips
- Organize wire runs cleanly — inspectors check for neat installation
- **Do not cross positive and negative conductors** — a shunt fault between them can cause a fire
- Use appropriate weatherproof conduit or direct-burial wire for runs through attic or along exterior walls
- Label positive and negative conductors at every junction point
- At string level, verify polarity before connecting to inverter

### Combiner Box (if applicable)
- Install where accessible (not buried in insulation, accessible without moving panels)
- Land strings per combiner wiring diagram
- Install overcurrent protection per NEC 690.9
- Label each string circuit with source circuit ID

## Step 4: Inverter and Battery Installation

### String Inverter
- Mount inverter on a solid wall — inverters are heavy (30–100 lbs)
- Follow manufacturer's clearance requirements (thermal management needs airflow)
- Typically mounted near the service panel or main disconnect
- DC input: land string conductors per inverter wiring diagram; verify polarity
- AC output: connect to AC disconnect, then to service panel

### Microinverter Combiner
- Mount IQ combiner or equivalent junction box at accessible point
- Trunk cable lands here; runs as 240V AC to the service panel
- Follow manufacturer's wiring diagram for neutrals and grounds

### Battery System
- Mount battery per manufacturer requirements — typically within specified temperature range (not in unconditioned space if too cold/hot)
- Tesla Powerwall and similar units are floor or wall mounted, specify maximum/minimum temperatures
- AC-coupled batteries have their own inverter inside; connect AC input from solar inverter AC output and AC output to loads panel or main panel
- DC-coupled batteries connect at the DC bus of a hybrid inverter — follow hybrid inverter manual exactly
- Commission battery separately per manufacturer procedure before commissioning the full system

## Step 5: AC Wiring and Service Panel

### Service Panel Connection
This is the work that most often requires a licensed electrician — even for DIY solar, local codes may require licensed electrical work at the service panel.

- Turn off main breaker before any panel work
- Verify panel is deenergized with a multimeter at the bus bars
- Run conduit from inverter to panel; size per NEC 690 and local code
- Install solar circuit breaker in panel per permit drawings
- Follow NEC 705.12 bus bar calculation (120% rule — see Phase 4)
- Land hot conductors (typically red and black for 240V), neutral, and ground

### AC Disconnect
- Install externally visible, lockable AC disconnect at utility meter (required by most utilities)
- Label "AC Disconnect — Solar" per NEC 705.10 and 690.54

## Step 6: Grounding and Labeling

### Equipment Grounding
- All metallic equipment housings, racking, panels frames, conduit → connected to equipment grounding conductor (EGC)
- EGC runs back to panel ground bus
- Ground rods: array ground rod at array location, system ground at inverter location (requirements vary by NEC version and AHJ)

### Required NEC Labels
Solar installations require extensive labeling. A label checklist:
- [ ] Each panel: "WARNING — ELECTRIC SHOCK HAZARD" (NEC 690.35 or 690.56)
- [ ] Source circuit conductors: polarity labeled at junction boxes
- [ ] DC disconnect: "PHOTOVOLTAIC SYSTEM DISCONNECT"
- [ ] AC disconnect: "AC DISCONNECT — SOLAR"
- [ ] Main panel solar breaker: "SOLAR ELECTRIC SYSTEM" and rated current
- [ ] Rapid shutdown initiation device: "SOLAR PV SYSTEM EQUIPPED WITH RAPID SHUTDOWN"
- [ ] Interconnection point label per NEC 705.10
- [ ] Battery system: required safety labels per manufacturer and NEC 706
- [ ] Conduit containing PV source circuits: labeled every 10 feet and at conduit entry/exit

**Note:** Missing labels are a common inspection failure. Label everything before the inspector arrives.

## Post-Installation Checklist

Before calling for inspection:
- [ ] All panels mounted and secure
- [ ] All DC wiring complete and labeled; no exposed terminations
- [ ] Inverter mounted and wired (but not yet energized)
- [ ] Battery mounted and wired (but not yet energized)
- [ ] AC wiring to service panel complete
- [ ] All required labels installed
- [ ] Permit drawings on-site and accessible for inspector
- [ ] System photos taken for your records

## Related

- Rapid shutdown compliance: `../../product/concepts/nec-rapid-shutdown.md`
- Common installation mistakes: `../gotchas/common-mistakes.md`
- Phase 6: `06-inspection-commissioning.md`
