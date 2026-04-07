---
title: Do I Need a Battery with Solar?
type: faq
tags:
- battery-systems-2026
- faq-battery-decision
- grid-tied-vs-hybrid
- product
- system-design-fundamentals
pack: solar-diy-product
retrieval_strategy: standard
---
<!-- context: section=product, topic=faq-battery-decision, related=battery-systems-2026,grid-tied-vs-hybrid,system-design-fundamentals -->

> **Lead summary:** A battery is not required for solar to work — grid-tied systems function without one. A battery is needed if you want backup power during outages, or if you want to shift solar production to high-rate evening hours (time-of-use arbitrage). Battery costs dropped significantly in 2023–2026; the 30% federal ITC now applies to battery storage, making economics more favorable.

# Do I Need a Battery with Solar?

## The Short Answer

You do **not** need a battery for solar to work. Grid-tied systems without batteries are the most common residential configuration. They generate power when the sun shines, send excess to the grid, and draw from the grid at night.

**You need a battery if:**
- You want backup power during grid outages
- Your utility has high TOU evening rates (e.g., California >$0.45/kWh at peak)
- Net metering rates are poor (e.g., California NEM 3.0 pays ~$0.05/kWh for export)
- You want to maximize self-consumption of your solar production

**You don't need a battery if:**
- Your utility has a generous net metering policy (1:1 retail-rate credit for export)
- Backup power isn't a priority
- Budget is the primary constraint

## What a Battery Actually Does

A grid-tied system without battery will **shut off during a grid outage**, even if the sun is shining. This is required by NEC anti-islanding rules — inverters must disconnect when the grid goes down to protect utility workers.

A battery + hybrid inverter creates an energy island: the solar and battery power your home, and the grid-tie disconnects. This is how Tesla Powerwall, Enphase IQ Battery, and FranklinWH systems provide backup.

## What Can a 13.5 kWh Battery Power?

A standard Powerwall 3 (13.5 kWh usable) with typical solar charging:

| Scenario | Days of Backup |
|---------|---------------|
| Essential loads only (fridge, lights, internet, phones) | 2–4 days |
| Moderate use (essentials + some lighting + fans) | 1–2 days |
| Full house (AC, electric stove, EV charging) | 4–8 hours |

Solar recharging during the day extends backup indefinitely in sunny weather.

## Battery Cost vs. ROI

Leading options in 2026:
- **Tesla Powerwall 3**: ~$9,200 installed (includes inverter)
- **Enphase IQ Battery 5P**: ~$4,000–$5,000 per 5 kWh module installed
- **FranklinWH aPower 2**: ~$10,500 installed (15 kWh)

After the 30% federal ITC:
- Powerwall 3: ~$6,440 net cost
- One Enphase module: ~$2,800–$3,500 net cost

TOU arbitrage payback in CA (charging at $0.15/kWh off-peak, discharging at $0.50/kWh peak): ~$1,000–$2,000/year savings → 5–8 year payback.

## Related

- Full battery comparison: [[battery-systems-2026.md|`battery-systems-2026.md`]]
- Grid-tied vs. hybrid decision: `grid-tied-vs-hybrid.md`
- System design for battery sizing: [[system-design-fundamentals.md|`system-design-fundamentals.md`]]
