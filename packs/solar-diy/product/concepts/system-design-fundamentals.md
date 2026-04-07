---
title: System Design Fundamentals
type: concept
tags:
- concept
- system-design
- solar-fundamentals
- solar-diy-product
pack: solar-diy-product
retrieval_strategy: standard
---
---
sources:
  - type: documentation
    url: "https://www.mayfield.energy/technical-articles/2023-update-how-to-calculate-pv-string-size/"
    date: "2023-11"
  - type: documentation
    url: "https://www.greentechrenewables.com/article/solar-inverter-string-design-calculations"
    date: "2025-12"
---

# System Design Fundamentals

<!-- context: section=product, topic=system-design-fundamentals, related=inverter-types,solar-panels-2026,battery-systems-2026,system-design-phase,string-sizing -->

> **Lead summary:** Residential solar system design involves four key decisions: (1) array sizing based on energy usage and available roof space, (2) inverter selection (micro, string, or optimizer), (3) string sizing calculations using panel voltage specs and local temperature extremes, and (4) battery sizing based on backup goals and load profiles. The most critical calculation is string sizing — too many panels per string can damage the inverter or cause a fire; too few and the system underperforms.

## Step 1: Determine Your Energy Needs

### Read Your Electric Bill
- Find your annual kWh consumption (most bills show 12-month usage)
- Identify seasonal patterns — summer A/C peaks, winter heating
- Typical US home: 10,000-11,000 kWh/year (varies hugely by climate and home size)

### Calculate Required System Size
Basic formula:
```
System size (kW) = Annual kWh ÷ (Peak sun hours/day × 365 × System efficiency)
```

**Peak sun hours** vary by location:
- Northeast US: 3.5-4.5 hours/day
- Southeast US: 4.5-5.5 hours/day
- Southwest US: 5.5-7.0 hours/day

**System efficiency** accounts for all losses (inverter, wiring, soiling, temperature): typically 75-85%

**Example:** 10,000 kWh/year in Florida (5.0 peak sun hours, 80% efficiency):
```
10,000 ÷ (5.0 × 365 × 0.80) = 6.85 kW system
```
With 450W panels, that's about 16 panels.

## Step 2: Assess Your Roof

### Orientation (Azimuth)
- **Due south (180°)** is optimal in Northern Hemisphere
- Southeast or southwest (135°-225°) loses only 5-10% production
- East or west facing loses 15-25% — still viable, especially with microinverters
- North-facing is generally not viable in the US

### Tilt
- Optimal tilt ≈ your latitude for annual production
- Typical residential roofs (4:12 to 8:12 pitch = 18°-34°) are usually close enough
- Flat roofs use tilt racks (adds cost but optimizes production)

### Shading
- Even small shading (chimney shadow, tree branch) dramatically impacts string inverter systems
- Use microinverters or optimizers for partially shaded roofs
- Tools: Google Project Sunroof, Aurora Solar, or a professional shade analysis

### Usable Area
- Subtract setbacks required by code (typically 3 feet from ridge, 18" from edges for fire access)
- Subtract obstructions: vents, pipes, skylights, HVAC equipment
- A 450W panel is approximately 21 sq ft (roughly 3.5' × 6')

## Step 3: String Sizing (String Inverter Systems)

This is the most technical calculation in system design. **Microinverter systems skip this entirely** — each panel operates independently. String sizing only applies to string inverters and string + optimizer systems.

### Why It Matters
Panel voltage changes with temperature. Cold weather increases voltage; hot weather decreases it.
- **Too many panels in a string** → voltage exceeds inverter maximum → damage or fire
- **Too few panels in a string** → voltage drops below inverter minimum → system shuts off or underperforms

### Maximum String Size (Cold Weather Limit)

Determines the maximum number of panels before exceeding inverter voltage limits.

```
Voc_max = Voc × [1 + ((T_low - 25°C) × (TempCoef_Voc / 100))]

Max panels per string = Inverter max voltage ÷ Voc_max
```

Where:
- **Voc** = Panel open circuit voltage from datasheet
- **T_low** = Lowest expected ambient temperature at your site (use ASHRAE 2% low)
- **TempCoef_Voc** = Voltage temperature coefficient from datasheet (%/°C, negative value)
- Round DOWN to nearest whole number (safety margin)

### Minimum String Size (Hot Weather Limit)

Determines the minimum number of panels to keep the inverter in its operating range.

```
Vmp_min = Vmp × [1 + ((T_high + T_add - 25°C) × (TempCoef_Vmp / 100))]

Min panels per string = Inverter min MPPT voltage ÷ Vmp_min
```

Where:
- **Vmp** = Panel voltage at maximum power from datasheet
- **T_high** = Highest expected ambient temperature (use ASHRAE 2% high)
- **T_add** = Temperature adder for mounting method:
  - Roof-mounted, parallel (6" standoff): +30°C
  - Roof-mounted, flush: +35°C
  - Ground or pole mounted: +25°C
- Round UP to nearest whole number

### Worked Example

**Equipment (example — verify current specs on manufacturer datasheets):** 485W panel (Voc=45.9V, Vmp=45.63V, TempCoef_Voc=-0.27%/°C, TempCoef_Vmp=-0.34%/°C) with SMA CORE1 inverter (max 1000V, MPPT range 550-800V)

<!-- refresh
  decay: fast-moving
  as_of: 2026-Q1
  fields: [example_panel_model_specs, example_inverter_model_specs]
  source: manufacturer datasheets (qcells.com, sma.de)
  method: "The MATH is permanent — formulas never change. The example equipment specs may be outdated. Verify panel Voc/Vmp/TempCoef and inverter voltage ranges on current datasheets before using for real system design."
-->

**Site:** Portland, Oregon (T_low=-7°C, T_high=32°C, roof-mounted flush)

**Maximum string:**
```
Voc_max = 45.9 × [1 + ((-7 - 25) × (-0.0027))] = 45.9 × 1.0864 = 49.87V
Max panels = 1000 ÷ 49.87 = 20.05 → 20 panels max
```

**Minimum string:**
```
Vmp_min = 45.63 × [1 + ((32 + 35 - 25) × (-0.0034))] = 45.63 × 0.8572 = 39.11V
Min panels = 550 ÷ 39.11 = 14.06 → 15 panels min
```

**Result:** Each string should have between 15 and 20 panels.

### Temperature Data Sources
- **Solar ABCs** (energyresearch.ucf.edu) — ASHRAE temperature lookup by location
- **PVWatts Calculator** (NREL) — free online tool that does many of these calculations
- **Local weather data** — NOAA records for historical extremes

## Step 4: Battery Sizing

See [[battery-systems-2026.md|Battery Systems 2026]] for product comparisons.

### Key Questions
1. **What loads do you want to back up?** Essential circuits (fridge, lights, Wi-Fi) need ~3-5 kW. Whole-home with A/C needs 10-15 kW+
2. **How long?** One night of essentials ≈ 5-10 kWh. Full day of whole-home ≈ 30-50 kWh
3. **Can your battery handle motor startups?** Check LRA ratings against your A/C compressor and well pump specs
4. **Grid-tied or off-grid?** Grid-tied with backup only needs enough for outage duration. Off-grid needs enough for multiple days of autonomy

## Related

- [[solar-panels-2026.md|Solar Panel Landscape]] — Current panel specs for design calculations
- [[battery-systems-2026.md|Battery Systems]] — Battery comparison for Step 4
- [[inverter-types.md|Inverter Types]] — Architecture selection for Step 2
