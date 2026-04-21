---
title: "Phase 7: Operations & Maintenance"
type: "phase"
tags: [battery-systems-2026, inspection-commissioning, monitoring, phase-7-operations-maintenance, process, solar-panels-2026]
pack: "solar-diy-process"
retrieval_strategy: "atomic"
id: solar-diy/process/phases/07-operations-maintenance
verified_at: "2026-04-21"
verified_by: agent
schema_version: "4.1"
concept_scope: single
---

# Phase 7: Operations & Maintenance

<!-- context: section=process, topic=phase-7-operations-maintenance, related=inspection-commissioning,battery-systems-2026,solar-panels-2026,monitoring -->

> **Lead summary:** A well-installed solar system requires minimal maintenance but rewards attentive monitoring. The main ongoing tasks are: monitoring production against expectations, annual cleaning (in most climates), periodic visual inspections, degradation tracking over years, and proactive warranty management. Most system problems are caught early through monitoring — set up alerts on day one and check monthly.

## What to Expect from Your System

### Normal Production Patterns
- **Seasonal variation**: Winter production will be 40–70% of summer production in most US locations (shorter days, lower sun angle, more cloudy weather)
- **Daily variation**: Production follows a bell curve peaking at solar noon, with weather causing day-to-day variation
- **Degradation**: First-year LID (Light-Induced Degradation) may reduce output 1–2% in year one; long-term degradation is ~0.3–0.5%/year for quality panels
- **Temperature effects**: Hot summer days produce less power per panel than spring/fall despite more sun hours (temperature coefficient)

### Realistic Year-One Performance
Your PVWatts estimate is a 30-year weather average. Year one actual production will likely be within ±15% of the estimate. A significant shortfall (>15% below estimate) warrants investigation.

**Common reasons for underperformance in year one:**
- Inverter settings not optimized
- Shading not fully accounted for in the estimate
- Weather year that differs significantly from historical average
- Soiling (dust, pollen, bird droppings)
- Partial clamps on panels affecting temperature
- A microinverter or optimizer that failed out of box

## Monitoring

### Set Up Alerts
Most inverter monitoring platforms support production alerts. Configure at minimum:
- **No-production alert**: If the system produces nothing on a clear day, something is wrong
- **Low-production alert**: If daily production is <70% of expected on a clear day, investigate
- **Equipment fault alerts**: Inverter faults, microinverter offline alerts, battery fault codes

### Monthly Check
- Log in to your monitoring platform
- Review monthly production vs expected (PVWatts gives monthly estimates)
- Note any error codes or offline equipment
- Verify battery state of health (if applicable)

### Annual Review
- Download full-year production data
- Compare actual vs estimated (PVWatts) by month
- Calculate your actual capacity factor (annual kWh ÷ system kW DC ÷ 8,760 hours)
- Track year-over-year production to measure actual degradation
- Review your utility bills to confirm expected savings

### Monitoring Platform Specifics
- **Enphase Enlighten**: Per-panel production data; excellent fault detection. App shows each microinverter.
- **SolarEdge**: Per-optimizer production via monitoring portal. Battery SOC and flows visible if using Home Hub.
- **Fronius Solar.web**: String-level monitoring; inverter status history.
- **Tesla app**: Real-time energy flows (solar, battery, grid, home); historical data. Also shows outage backup events.

## Cleaning

### When to Clean
- **Most climates**: Once or twice per year, typically before peak summer production season
- **Dusty/arid climates** (Southwest US): May need quarterly cleaning
- **Heavy pollen regions**: Spring cleaning after pollen season is especially valuable
- **After major events**: Dust storms, nearby construction, wildfire ash — clean promptly

### How to Clean
- **Best time**: Early morning before panels heat up (thermal shock risk if cold water on hot panels)
- Use plain water and a soft brush or squeegee — no abrasive cleaners or soaps (streak residue)
- A soft-bristled brush on an extension pole lets you clean from the ground
- For roof work, use fall protection
- Avoid high-pressure washers — they can damage panel coatings and moisture-seal junction boxes
- Don't scratch the panel surface — even fine scratches reduce light transmission

### Soiling Loss
Research suggests typical soiling loss is 1–5% in most US climates. In desert areas without regular cleaning, losses can exceed 10%. Clean panels simply and the production numbers confirm whether cleaning helped.

## Visual Inspections

### Annual Roof Inspection
Coincide with cleaning. From the ground (binoculars) or roof (with fall protection):
- [ ] All panels secure in racking — no gaps, loose clamps, or vibrating panels
- [ ] Racking rails intact — no visible cracking or corrosion
- [ ] Roof mounts: no shifted flashing, no visible gaps
- [ ] Conduit intact — no cracked conduit, exposed wire, or broken supports
- [ ] No vegetation growth encroaching on panels or underneath them
- [ ] No panel discoloration, hotspots, or visible cell damage

### Panel Condition
- **Hotspots**: Darkened areas on panel cells visible in strong light — caused by cracked cells or delamination. Report to manufacturer under product warranty.
- **Delamination**: Bubbling or separation of the panel encapsulant from the glass. A warranty claim.
- **Soiling patterns**: Unusual heavy soiling in specific areas may indicate bird perching — consider bird deterrents
- **Cracked panels**: Usually from hail or physical impact; file insurance claim and warranty claim

### Inverter and Battery
- [ ] No error codes or warning lights
- [ ] Ventilation openings clear (inverters are air-cooled; blocked vents reduce lifespan)
- [ ] No unusual sounds (buzzing or clicking beyond normal operation)
- [ ] Battery enclosure intact; no signs of leaking, swelling, or heat damage

## Degradation Tracking

Quality solar panels degrade slowly over time. Tracking actual degradation helps you know if your system is performing as warranted.

### How to Calculate Degradation
```
Degradation rate (%/year) = (Year 1 production - Year N production) ÷ (Year 1 production × (N-1))
```
Normalize for weather variation by comparing PVWatts predictions year-over-year alongside your actuals.

### What's Normal
- Year 1 (LID): 0–2% loss
- Years 2–25: 0.25–0.5%/year for quality panels
- At 0.5%/year, a 400W panel produces ~362W at year 25 (about 90.5%)
- **If you see >1%/year consistent degradation**: file a warranty claim

### Panel Warranty Claims
Warranty claims require documentation:
- Your original purchase receipt (keep this forever)
- System monitoring data showing production history
- Independent production testing (some warranty claims require a licensed electrician or third-party testing firm to document)
- Contact manufacturer's warranty claims department, not your installer (if installer has closed)

## Battery Health

### Monitoring Battery Degradation
- Most battery systems report state of health (SOH) in their monitoring apps
- LFP batteries (Tesla Powerwall 3, Franklin WH, etc.) are rated for 3,000–6,000 cycles to 80% SOH
- Daily cycling (time-of-use arbitrage) degrades batteries faster than weekly cycling (emergency backup only)
- Unexpected rapid capacity loss → warranty claim

### Battery Warranty Claims
Battery warranties are typically:
- 10 years / 70% remaining capacity (minimum)
- Some warranties specify throughput (e.g., 10 MWh per kWh of nominal capacity)
- Document your cycling history via monitoring data

## Inverter Maintenance and Lifespan

- String inverters: 10–15 year lifespan typical; plan for replacement around year 15
- Microinverters: 25-year warranty from Enphase; designed to match panel life
- Inverter replacement cost: $1,500–$4,000 for string inverter; budget for this in your 15-year plan

Some inverters have firmware updates that improve performance or add features — check manufacturer websites annually.

## Seasonal Considerations

### Winter
- Snow on panels: most systems shed snow quickly due to panel heat and slick glass surface. Don't attempt to remove snow from the roof — not worth the injury risk for minor production gains.
- Ice dams: solar racking can create snow retention points that contribute to ice dams in cold climates. Monitor your roof edges.
- Shorter days, lower sun angle — normal low production period

### Summer
- Hot days produce less power per panel than spring/fall (temperature coefficient)
- Check inverter ventilation — ambient temps >40°C can cause inverter thermal throttling
- Peak production season — compare against your estimates

### Severe Weather Preparation
- Hail: panels are rated for 1" hail at 50 mph (some for larger). After severe hail, inspect panels for cracks and file insurance claim if damaged.
- Wind: inspect racking after major wind events (>80 mph)
- Hurricane/tropical storm: consider disconnecting and covering system if you're in the direct path of a major storm

## 10-Year Milestone Review

Around year 10, do a comprehensive system review:
- [ ] Actual vs estimated cumulative production documented
- [ ] Panel degradation rate calculated
- [ ] All warranty documentation confirmed current (contact manufacturer if warranty holder has changed)
- [ ] Inverter condition assessed (string inverters approaching replacement window)
- [ ] Battery health reviewed; replacement timeline estimated
- [ ] Net metering policy current (policies change — verify you're still on your expected tariff)
- [ ] Reassess system expansion: additional panels, more battery, EV charger integration?

## Related

- Performance troubleshooting: `../../product/troubleshooting/`
- Product specifications for warranty reference: `../../product/specifications/`
