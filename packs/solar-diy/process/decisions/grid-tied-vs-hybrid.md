---
title: "Decision: Grid-Tied vs Hybrid vs Off-Grid"
type: "decision"
tags: [battery-systems-2026, component-selection, decision-grid-tied-vs-hybrid, inverter-types, process, system-design]
pack: "solar-diy-process"
retrieval_strategy: "standard"
id: solar-diy/process/decisions/grid-tied-vs-hybrid
verified_at: "2026-04-10"
verified_by: agent
---

# Decision: Grid-Tied vs Hybrid vs Off-Grid

<!-- context: section=process, topic=decision-grid-tied-vs-hybrid, related=battery-systems-2026,inverter-types,system-design,component-selection -->

> **Lead summary:** Most residential solar in the US is grid-tied — it sells excess power to the utility and draws from the grid at night. Hybrid systems add battery storage for backup capability and bill optimization. Off-grid systems operate completely independently of the utility. In 2026, hybrid (grid-tied + battery) is the fastest-growing configuration as battery costs have dropped and net metering has weakened in several states.

## The Three System Configurations

### Grid-Tied (No Battery)

**How it works:** Solar panels generate DC power, the inverter converts to AC, and excess production feeds back to the utility grid (net metering). At night or on cloudy days, you draw from the grid.

**Key characteristics:**
- Simplest and least expensive configuration
- System shuts down during grid outages (anti-islanding protection requirement — protects utility workers)
- Depends entirely on net metering economics for financial return
- No backup capability — power outage = your solar is off too

**Best for:**
- Homeowners in states with good net metering (full retail credit for exports)
- Budget-constrained buyers who want maximum production per dollar
- Areas with few power outages
- Commercial properties where backup is handled by generators or other means

**Economics:** Payback period typically 6–10 years for grid-tied systems in favorable net metering states.

### Hybrid (Grid-Tied + Battery)

**How it works:** Solar charges both the battery and feeds the grid. During an outage, the battery disconnects from the grid (islanding) and provides power to backed-up loads. In normal operation, the battery either stores energy for evening use or provides backup power.

**Key characteristics:**
- Moderate additional cost ($8,000–$25,000+ for battery and equipment beyond grid-tied)
- Provides backup power during grid outages
- Enables energy arbitrage (charge at night when rates are low, discharge when rates are high)
- Requires a critical loads panel or whole-home backup configuration
- More complex installation and permitting

**Operating modes:**
1. **Backup only**: Battery stays at 100% SOC, only discharges on outage. Simple, maximizes battery lifespan.
2. **Self-consumption**: Battery charges from solar excess, discharges in evening to reduce grid import.
3. **Time-of-use arbitrage**: Battery charges from grid at off-peak rates, discharges during peak-rate hours.
4. **Storm/outage anticipation mode** (Powerwall "Storm Watch"): Pre-charges to 100% when weather forecast indicates grid risk.

**Best for:**
- States with time-of-use (TOU) rates where evening peak rates are 2–4× off-peak (California, Hawaii, Arizona, Massachusetts, New York)
- Areas with frequent power outages (Florida storms, Texas grid events, rural areas)
- States with weakened net metering (California NEM 3.0) where battery arbitrage is more valuable than export credits
- Homeowners with medical equipment, home offices, or other resilience needs

**Economics:** Battery payback is harder to justify on economics alone in most markets. Backup value (insurance) and peace of mind are often the real justification. In high-TOU states, battery ROI is increasingly compelling.

### Off-Grid

**How it works:** System operates completely independently of the utility grid. Solar charges a battery bank; the battery powers the home. A generator provides backup on extended cloudy periods.

**Key characteristics:**
- Highest cost — requires large battery bank (3–7 days of autonomy) and backup generator
- No utility bill — but also no utility backup
- Significantly more complex system design, installation, and operation
- Requires load management discipline (can't run high-draw appliances simultaneously on small systems)
- Professional design and installation strongly recommended

**Who this is actually for:**
- Properties without utility grid access (rural land, cabins, remote homesteads)
- Properties where grid connection cost would be prohibitive ($20,000–$50,000+ for long utility runs)
- Homeowners with strong ideological commitment to energy independence (and the budget and commitment to support it)

**Off-grid is NOT recommended as a cost-saving measure for grid-accessible properties.** The battery and generator costs almost always exceed 20 years of grid bills.

## The Net Metering Factor

This is the most important economic variable in the grid-tied vs hybrid decision.

### Full Retail Net Metering (NEM 1.0/2.0)
Your exported solar power is credited at the full retail electricity rate. If you pay $0.15/kWh to buy power and you export 1 kWh, you get a $0.15 credit.

- **Battery value is low** in this model — if you can sell excess at full retail, storing it in a battery (with round-trip losses) is economically suboptimal
- **Grid-tied is the economic winner** in full retail NEM states

### Avoided Cost / Export Rate Net Billing (NEM 3.0 style)
Your exported solar power is credited at a lower avoided-cost rate (wholesale) — often $0.03–$0.08/kWh vs retail rates of $0.15–$0.40/kWh.

- **Battery value is high** — it's better to self-consume or store than to export at a low rate
- **Hybrid systems become much more attractive** in this model
- California's NEM 3.0 (adopted 2023) is the primary example; some other states are moving in this direction

### Time-of-Use Rates
If your utility charges different rates by time of day (typical peak: 4–9pm), battery storage enables arbitrage:
- Charge from solar during off-peak hours (or cheap overnight grid power)
- Discharge during high-rate evening hours
- In California, Hawaii, and parts of the Northeast: peak rates 3–5× off-peak rates create real battery ROI

## Battery Sizing for Hybrid Systems

Sizing depends on which operating mode you're targeting:

### Backup Only Sizing
```
Required kWh = (Critical load power, kW) × (Target backup hours) ÷ DoD
```

**Example essential loads (kW):**
- Refrigerator: 0.1–0.2 kW
- LED lights (10 bulbs): 0.05 kW
- Internet router + modem: 0.02 kW
- Phone charging: 0.02 kW
- Small TV: 0.05 kW
- **Total essentials: ~0.5–0.8 kW continuous**

For 24 hours of essentials: 0.7 kW × 24 hours ÷ 0.90 DoD = **18.7 kWh**
(One Tesla Powerwall 3 at 13.5 kWh usable covers ~16–18 hours of essential loads)

**If you want to run central A/C during backup:** add 3–5 kW continuous + motor startup surge (LRA). One Powerwall 3 can run a 3-ton A/C unit but will deplete in hours. Two Powerwalls recommended for extended A/C backup.

### Self-Consumption Sizing
Battery should roughly match daily excess solar production.

**Example:** 10 kW array in Tampa, FL produces ~45 kWh on a clear summer day. Home uses 30 kWh/day. Excess production: ~15 kWh. A single 13.5 kWh battery captures most of this excess; 2 batteries captures more but with diminishing returns.

## Backup Architecture: Critical Loads Panel vs. Whole-Home

### Critical Loads Panel
- A subpanel fed from the battery backup side; only backed-up circuits are in this panel
- Less expensive: smaller battery, simpler installation
- During outage: only circuits in the critical loads panel have power
- Common in first-generation battery installs

### Whole-Home Backup
- The battery (via a gateway/transfer switch) backs up the entire service panel
- More expensive: requires larger battery capacity and a gateway device
- During outage: entire home functions normally (or within battery capacity limits)
- Tesla Powerwall 3, Enphase IQ System Controller 3 (IQ+), and Sol-Ark support whole-home backup

**Tesla Powerwall 3 (2026):** 13.5 kWh usable, 10 kW continuous, 185A peak surge for 10 seconds — supports whole-home backup for most homes without whole-home A/C running

## Permitting Implications

- **Grid-tied**: Straightforward interconnection application; most utilities have a streamlined process
- **Hybrid**: Requires battery storage specifications in permit; may require battery room ventilation documentation; fire code requirements for LFP batteries
- **Off-grid**: No interconnection application needed; may still require building permit for electrical work; well-pump and septic pump considerations

## State Policy Trends (2026)

- **California**: NEM 3.0 makes battery storage economically compelling for new installations
- **Hawaii**: Similar policy trajectory to California; battery-plus-solar is standard
- **Texas**: ERCOT grid events have driven strong battery adoption for resilience
- **Florida**: Frequent hurricane season disruptions driving battery adoption; net metering still favorable
- **Most other states**: Net metering still favorable; hybrid adoption is growing but driven more by resilience than economics

## The "Battery Later" Option

One common strategy: install grid-tied now and add battery later.

**Works well if:**
- You're cost-constrained now
- You want to see how solar performs before committing to battery
- You're choosing microinverters (AC-coupled battery can be added anytime)

**Watch out for:**
- Inverter compatibility: some string inverters require a specific battery-compatible model for future AC coupling — verify before buying
- Net metering policy change risk: some states' net metering policies could change during your payback period, retroactively making battery more valuable
- Hybrid inverter now: if there's any chance you'll add battery, consider a hybrid inverter from the start (avoids an inverter replacement later)

## Quick Decision Guide

**Grid-tied only if:**
- Full retail net metering in your state
- Budget-constrained
- Area has reliable grid

**Hybrid if:**
- TOU rates with significant peak/off-peak spread
- Net billing or NEM 3.0 in your state
- Frequent outages or resilience value
- You want backup capability

**Off-grid only if:**
- No utility grid access or grid connection is prohibitively expensive

## Related

- Battery product comparisons: `../../product/specifications/battery-systems-2026.md`
- Inverter topology for hybrid systems: `inverter-topology.md`
- Phase 2 battery sizing: `../phases/02-system-design.md`
