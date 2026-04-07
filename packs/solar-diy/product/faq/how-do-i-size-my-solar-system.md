---
title: How Do I Size My Solar System?
type: faq
tags:
- faq-system-sizing
- product
- pvwatts
- solar-panels-2026
- system-design-fundamentals
- system-design-phase
pack: solar-diy-product
retrieval_strategy: standard
---
<!-- context: section=product, topic=faq-system-sizing, related=system-design-fundamentals,solar-panels-2026,system-design-phase,pvwatts -->

> **Lead summary:** System sizing starts with your annual kWh consumption, local peak sun hours (from NREL PVWatts), a 75–85% derate factor, and any future loads like an EV. Most US homes need 6–12 kW DC to cover 100% of consumption. Size for your 5-year future load, not today's bills.

# How Do I Size My Solar System?

## Step 1: Know Your Annual kWh

Pull 12 months of utility bills and add up your total annual kWh consumption. If you don't have 12 months of history, multiply your typical monthly bill by 12. Example: 1,000 kWh/month × 12 = 12,000 kWh/year.

## Step 2: Find Your Peak Sun Hours

Use [NREL PVWatts](https://pvwatts.nrel.gov) for your ZIP code and roof orientation. Enter a 1 kW system, south-facing at your roof pitch, and note the annual kWh output — this is your peak sun hours equivalent per kW of DC capacity.

Typical values:
- Southern US (AZ, TX, FL): 1,500–1,900 kWh/kW/year
- Mid-Atlantic (NC, VA, MD): 1,300–1,500 kWh/kW/year  
- Pacific Northwest (OR, WA): 1,000–1,200 kWh/kW/year

## Step 3: Calculate Required System Size

```
System kW-DC = Annual kWh ÷ PVWatts kWh/kW
```

Example: 12,000 kWh ÷ 1,400 kWh/kW = 8.57 kW-DC → round up to 9 kW

## Step 4: Account for Future Loads

Add expected new loads **before** finalizing size:
- **EV charger** (EVSE Level 2): adds ~3,000–5,000 kWh/year per vehicle
- **Heat pump (replacing gas furnace)**: adds ~2,000–4,000 kWh/year
- **Pool equipment**: adds ~2,000–6,000 kWh/year

Many people size too small and wish they'd added more capacity.

## Step 5: Apply the 120% Rule Check

Your solar breaker cannot exceed 20% of the service panel bus bar rating:
- 200A bus bar → max 40A solar breaker → max ~9.6 kW AC continuous
- If your system exceeds this, a supply-side connection or panel upgrade is needed

## Converting kW to Panel Count

Divide system kW-DC by the panel wattage, then round up:
- 9 kW ÷ 0.440 kW (440W panels) = 20.5 panels → 21 panels
- 9 kW ÷ 0.480 kW (480W panels) = 18.75 panels → 19 panels

## Related

- Full design methodology: [[system-design-fundamentals.md|`system-design-fundamentals.md`]]
- String sizing (voltage math): `02-system-design.md`
- PVWatts: https://pvwatts.nrel.gov
