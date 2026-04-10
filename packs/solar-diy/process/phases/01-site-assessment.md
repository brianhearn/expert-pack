---
title: "Phase 1: Site Assessment"
type: "phase"
tags: [diy-vs-contractor, permitting, phase-1-site-assessment, process, shading-analysis, system-design]
pack: "solar-diy-process"
retrieval_strategy: "atomic"
id: solar-diy/process/phases/01-site-assessment
verified_at: "2026-04-10"
verified_by: agent
---

# Phase 1: Site Assessment

<!-- context: section=process, topic=phase-1-site-assessment, related=system-design,diy-vs-contractor,permitting,shading-analysis -->

> **Lead summary:** Before designing anything, assess whether your site is actually suitable for solar. A thorough site assessment covers four areas: roof condition and orientation, shading analysis, structural capacity, and utility interconnection feasibility. Skipping this phase leads to expensive surprises — installing on a failing roof, designing around shading you didn't model, or hitting utility interconnection limits that make your project impractical.

## What You're Evaluating

### 1. Roof Condition and Orientation

**Age and condition first.** Solar panels have 25–30 year lifespans. If your roof is 15+ years old or showing wear, re-roof before installing solar. Removing and reinstalling panels costs $2,000–$6,000 — more than many roof repairs.

**Orientation (azimuth):**
- Due south (180°) is optimal for annual production in the Northern Hemisphere
- Southeast or southwest (135°–225°) loses only 5–10% production — often acceptable
- East or west facing loses 15–25% — still viable, especially with microinverters for flat or low-pitch roofs
- North-facing surfaces are not viable in most US locations

**Pitch (tilt):**
- Optimal tilt ≈ your latitude (for annual production maximization)
- Most residential roofs (4:12 to 8:12 pitch = 18°–34°) are near-optimal
- Very low pitch (flat or nearly flat) benefits from tilt racking, which adds cost
- Steep roofs (12:12 = 45°) are fine for production but add installation difficulty and cost

**Usable area:**
- Measure your total south-facing roof sections
- Subtract code-required setbacks: typically 3 feet from ridge, 18" from eaves and rakes (fire code varies — verify your jurisdiction's requirements; some require 36" pathways)
- Subtract obstructions: vents, pipes, skylights, HVAC equipment, chimneys
- A 400–500W panel occupies approximately 20–22 sq ft (roughly 3.5' × 6')
- Rule of thumb: a 10-panel array needs ~220 sq ft of clean, obstruction-free roof

**Roof type:**
- Comp shingle: easiest to work with, standard L-foot flashing mounts
- Standing seam metal: clamp mounts attach without penetrations — excellent
- Exposed fastener metal: penetration mounts required, more leak risk
- Clay/concrete tile: specialized hooks required, higher cost, fragile during installation
- Flat (TPO/EPDM/BUR): ballasted racking avoids penetrations; tilt racks add height and wind load
- Wood shake: not recommended (fire risk with electrical equipment)

### 2. Shading Analysis

Shading is the single biggest performance killer and the most commonly underestimated factor.

**Sources of shading:**
- Trees (seasonal — deciduous trees lose shading in winter but gain it in summer)
- Neighboring structures
- Chimneys, dormers, HVAC units on the roof itself
- Telephone poles and wires

**How shading interacts with your inverter choice:**
- String inverters: the lowest-performing panel in a string drags down the entire string. A single chimney shadow can cut production by 50%+
- Power optimizers (SolarEdge, Tigo): each panel has its own MPPT, so shading on one panel doesn't tank the string
- Microinverters (Enphase): each panel is fully independent — the best choice for complex shading scenarios

**Shading assessment tools:**
- **SolarEdge Designer, Aurora Solar, PVWatts** (online) — require roof measurements and location data
- **Solmetric SunEye** — handheld device for on-site shading analysis; used by installers
- **Google Project Sunroof** — free quick estimate, useful for initial feasibility check
- **Manual shade analysis** — stand at each panel location at solar noon and winter solstice noon; observe what's in the sky

**When shading makes solar impractical:**
- If more than 20% of your best roof faces significant shading during peak hours (10am–2pm), expect significantly reduced production
- Trees can be trimmed or removed — get a quote before writing off a site
- A ground mount may be viable if the roof is unsuitable

### 3. Structural Evaluation

Roof structure must support the additional load of panels and racking.

**Standard panel load:**
- Panels and racking add approximately 2.5–4 psf (pounds per square foot) of dead load
- Most residential roofs are designed for 20–30+ psf snow load in addition to the roof structure itself
- In most cases, residential roofs can support solar without structural upgrades

**When to be concerned:**
- Older homes with undersized or damaged rafters/trusses
- Long rafter spans without intermediate support
- Roofs showing visible sag or distress
- Homes in high snow-load zones that are already near structural limits
- Flat roofs where ballasted racking adds significant concentrated load

**What to do:**
- For standard residential installs: a licensed structural engineer may or may not be required by your jurisdiction — check with your building department
- If you see any signs of structural issues, hire a structural engineer before proceeding
- Permit applications typically require a structural review; many jurisdictions accept manufacturer-provided engineering letters for standard racking systems

### 4. Utility Interconnection Research

Before finalizing your design, understand your utility's requirements and limitations. This is the most overlooked part of site assessment.

**Key questions to answer:**
1. **Who is your utility?** Investor-owned utility (IOU), municipal utility, or rural electric cooperative? Each has different interconnection processes and timelines.
2. **What net metering program are you on?** Net metering 1.0 (full retail credit) vs net billing (avoided cost credit) vs NEM 3.0 (California's newer structure) dramatically affects project economics.
3. **Is there a system size cap?** Many utilities cap residential systems at 120% of your annual consumption. Some have absolute caps (e.g., 10 kW or 25 kW).
4. **What is the interconnection queue wait time?** Some utilities in high-solar-penetration areas have backlogs of 6–18 months.
5. **Is there a hosting capacity constraint on your feeder?** Some distribution feeders are at or near their solar hosting limit — new applications may be denied or require expensive upgrades.
6. **What are the utility's equipment requirements?** Some utilities require specific UL listings, disconnect switches, or specific inverter settings.

**How to find out:**
- Call your utility's interconnection department (not regular customer service)
- Download the utility's Small Generator Interconnection Procedures (SGIP) from their website
- Check your state's public utility commission website for net metering rules
- Talk to a local solar installer — they know the local utility idiosyncrasies

## Site Assessment Checklist

- [ ] Roof age and condition confirmed (replace if >15 years, any signs of wear)
- [ ] Primary and secondary roof faces identified and measured
- [ ] Azimuth for each face recorded (compass or online tool)
- [ ] Pitch for each face measured or calculated
- [ ] Usable area calculated (subtract setbacks and obstructions)
- [ ] Shading analysis completed for peak hours and seasonal variation
- [ ] Structural concerns identified and addressed
- [ ] Utility identified and interconnection requirements researched
- [ ] Net metering/net billing policy documented
- [ ] System size cap or hosting capacity constraints identified

## Outputs of This Phase

Going into Phase 2 (System Design), you should know:
- Total usable roof area (sq ft) on viable faces
- Roof orientation(s) and pitch(es)
- Shading severity (none / minor / moderate / significant)
- Target system size range (based on your energy usage and available area)
- Utility's system size cap
- Net metering policy and projected project economics

## Related

- System sizing math: `../product/concepts/system-design-fundamentals.md`
- Shading's impact on inverter selection: `../decisions/inverter-topology.md`
- Phase 2: `02-system-design.md`
