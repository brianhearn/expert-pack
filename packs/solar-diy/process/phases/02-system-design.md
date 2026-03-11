# Phase 2: System Design

> **Lead summary:** System design translates your site assessment into a specific array configuration: how many panels, in what arrangement, with which inverter, and what battery capacity. The core calculations are load analysis (how much energy you need), array sizing (how many panels to generate it), string sizing (how to wire panels without damaging equipment), and battery sizing (how much storage for your backup goals). Errors in string sizing are dangerous — verify your math before ordering equipment.

## Step 1: Load Analysis — How Much Power Do You Need?

### Read Your Electric Bills
- Collect 12 months of bills; note the kWh used each month
- Annual total is your baseline consumption
- Identify peak months (summer A/C, winter heat pump, etc.)
- Typical US home: 10,000–11,000 kWh/year; southern states with A/C can be 15,000–25,000 kWh/year

### Decide Your Offset Goal
- **100% offset**: Size the array to produce your full annual consumption. Maximizes long-term savings but maximizes upfront cost.
- **80% offset**: Common compromise — gets you past most of the expensive grid electricity while leaving some room for seasonal variation.
- **Critical loads only**: If battery backup is the primary goal, design for backup runtime rather than production offset.

### Adjust for Future Load Changes
- Electric vehicle: add 2,000–4,500 kWh/year per EV (home charging)
- Heat pump replacement for gas heating: adds 3,000–8,000 kWh/year depending on climate
- Going all-electric: model the full future load, not just today's baseline

## Step 2: Array Sizing — How Many Panels

### Basic Sizing Formula
```
System size (kW DC) = Annual kWh target ÷ (Peak sun hours/day × 365 × System efficiency)
```

**Peak sun hours by region (averages):**
- Pacific Northwest: 3.5–4.2 hrs/day
- Northeast: 3.8–4.5 hrs/day
- Midwest: 4.0–5.0 hrs/day
- Southeast: 4.5–5.5 hrs/day
- Southwest: 5.5–7.0 hrs/day

**System efficiency factor:** 75–82% (accounts for inverter losses, wiring losses, soiling, temperature, and shading). Use 78% as a default; reduce to 70–72% for partially shaded systems.

**Example:**
- 12,000 kWh/year target, Southeast (5.0 hrs/day), 78% efficiency
- System size = 12,000 ÷ (5.0 × 365 × 0.78) = 8.42 kW DC
- At 400W per panel: 21 panels; at 450W per panel: 19 panels

### Sanity-Check with PVWatts
NREL's PVWatts Calculator (pvwatts.nrel.gov) is the industry standard for production estimates. Enter your location, array size, tilt, azimuth, and losses — it outputs monthly and annual production estimates. Use it to validate your sizing math.

### Match Array Size to Available Roof Area
- If available roof area limits panel count below your target system size, revisit offset goal or consider ground mount
- If you have excess roof area, size to 100%+ offset if net metering makes it economical

## Step 3: Inverter Architecture Selection

At this stage you need to commit to your inverter topology. This decision shapes everything about the wiring design.

**Three main architectures:**
1. **String inverter** — All panels in a string feed a single central inverter. Lowest cost, simplest design, vulnerable to shading.
2. **String inverter + power optimizers** — Each panel has an optimizer for individual MPPT; string inverter does the DC-to-AC conversion. Moderate cost, shading tolerant, per-panel monitoring.
3. **Microinverters** — Each panel has its own small inverter. Most expensive per watt, best shading tolerance, best monitoring granularity, easiest to expand later.

See `../decisions/inverter-topology.md` for the full decision framework.

## Step 4: String Sizing (String and Optimizer Systems)

**Skip this section if using microinverters** — each panel is independent, no string sizing needed.

String sizing determines how many panels to wire in series on each string. This is the most technically critical calculation — errors can damage your inverter or create a fire hazard.

### Why Temperature Matters
Panel voltage rises in cold weather and falls in hot weather. You must calculate both limits:
- **Cold limit**: Maximum number of panels before voltage exceeds inverter's maximum input voltage
- **Hot limit**: Minimum number of panels to keep voltage above inverter's minimum MPPT tracking voltage

### Required Data
From the panel datasheet:
- Voc (open circuit voltage at STC)
- Vmp (voltage at maximum power at STC)
- Temperature coefficient of Voc (%/°C, always negative)
- Temperature coefficient of Vmp (%/°C, always negative)

From the inverter datasheet:
- Maximum input voltage (absolute maximum, do not exceed)
- MPPT voltage range (minimum and maximum)

From your site location:
- Lowest expected ambient temperature (use ASHRAE 99.6% dry-bulb temperature — look up by zip code)
- Highest expected ambient temperature (use ASHRAE 2% dry-bulb temperature)

### Maximum String Length (Cold Limit)
```
Voc_adj = Voc × [1 + ((T_min - 25°C) × TempCoef_Voc / 100)]
Max panels = FLOOR(V_max_inverter ÷ Voc_adj)
```
*Where T_min is your site's lowest expected temperature in °C. TempCoef_Voc is a negative number.*

### Minimum String Length (Hot Limit)
```
T_panel = T_max_ambient + mounting_adder
  (roof flush mount: +35°C; roof 6" standoff: +30°C; ground mount: +25°C)
Vmp_adj = Vmp × [1 + ((T_panel - 25°C) × TempCoef_Vmp / 100)]
Min panels = CEILING(V_mppt_min ÷ Vmp_adj)
```

### Practical Example
Panel: 450W (Voc=49.2V, Vmp=41.3V, TempCoef_Voc=-0.27%/°C, TempCoef_Vmp=-0.34%/°C)
Inverter: Max 1000V input, MPPT range 500–850V
Site: Atlanta, GA (T_min = -5°C, T_max = 36°C, roof flush mount)

**Maximum string:**
Voc_adj = 49.2 × [1 + ((-5 - 25) × -0.0027)] = 49.2 × 1.081 = 53.18V
Max panels = FLOOR(1000 ÷ 53.18) = 18 panels

**Minimum string:**
T_panel = 36 + 35 = 71°C
Vmp_adj = 41.3 × [1 + ((71 - 25) × -0.0034)] = 41.3 × 0.8436 = 34.84V
Min panels = CEILING(500 ÷ 34.84) = 15 panels

**Valid string range: 15–18 panels.** Design with 16 or 17 panels per string.

### Number of Strings
```
Number of strings = Total panel count ÷ Panels per string (round appropriately)
Max strings = Inverter max input current ÷ Panel Isc × 1.25 (NEC safety factor)
```
Verify the inverter has enough MPPT inputs for your number of strings. Strings should be equal length whenever possible.

## Step 5: Battery Sizing

Batteries add backup capability and, in some rate structures, significant economic value.

### Define Your Backup Goal First
- **Essential loads backup (common)**: Refrigerator, lights, phone charging, internet router, medical equipment — roughly 1.5–3 kW of continuous draw, 10–20 kWh/day
- **Partial home backup**: Essential loads plus one HVAC zone — 3–6 kW continuous, 15–30 kWh/day
- **Whole-home backup**: Full home including central A/C — 5–15 kW continuous (A/C surge can be 2–5× running watts), 30–60+ kWh/day

### Battery Selection Math
```
Required capacity (kWh) = Daily energy need × Backup days target ÷ DoD limit
```
- Backup days target: 1 day covers most utility outages; 3 days covers 95%+ of outages
- DoD (depth of discharge): LFP batteries are typically rated to 100% DoD but perform better long-term at 90%; NMC at 80–90%

**Example:** 15 kWh/day × 1.5 days ÷ 0.90 DoD = 25 kWh usable capacity needed

### Motor Start Surge — Critical Check
Air conditioners, well pumps, and refrigerators draw 3–7× their running current for the first few seconds on startup (called Locked Rotor Amperage, LRA). Many homeowners size battery power for running loads and are blindsided when the A/C kills the system.

Check your battery's rated surge capacity against your largest motor loads:
- Look up your A/C's LRA on the nameplate or spec sheet
- Compare to battery surge rating (typically 2–3× continuous rating for 5–30 seconds)
- A whole-home battery like Tesla Powerwall 3 has a 10 kW continuous / 185A peak for 10 seconds

### Battery Sizing for Economics (Rate Arbitrage)
Some utilities have time-of-use (TOU) rates with high peak-hour prices (typically 4–9pm). Sizing for daily charge/discharge cycles requires:
```
Battery capacity ≥ (Peak-hour consumption) × 1.2 buffer
Battery power ≥ Peak power draw during that window
```
Consult your utility's rate schedule and model the arbitrage savings before adding battery capacity for economic reasons alone.

## Phase 2 Outputs

Before moving to Phase 3 (Component Selection), document:
- System size: ___kW DC array, ___kW AC inverter
- Panel count: ___ panels @ ___W each
- Inverter architecture: string / optimizers / microinverters
- String configuration (string systems): ___ strings × ___ panels per string
- Battery: ___kWh capacity, ___kW continuous power (or "none")
- Array layout sketch (which panels go where on the roof)
- Production estimate (PVWatts output)

## Related

- Full string sizing worked examples: `../../product/concepts/system-design-fundamentals.md`
- Inverter architecture decision: `../decisions/inverter-topology.md`
- Grid configuration decision: `../decisions/grid-tied-vs-hybrid.md`
- Phase 3: `03-component-selection.md`
