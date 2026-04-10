---
title: "Freshness Guide — Solar DIY Pack"
type: "volatile"
tags: []
pack: "solar-diy-product"
retrieval_strategy: "standard"
id: solar-diy/product/freshness
verified_at: "2026-04-10"
verified_by: agent
---

# Freshness Guide — Solar DIY Pack

*How to keep this pack current. Lists all time-variant data points, their expected decay rate, and how to obtain current values.*

Last full review: 2026-03-10

## Time Variance Categories

| Category | Meaning | Review Cycle |
|----------|---------|--------------|
| 🔴 Volatile | Changes weeks-to-months | Quarterly |
| 🟡 Fast-moving | Changes every few months to a year | Semi-annually |
| 🟢 Slow-moving | Changes every 1-3 years | Annually |
| ⚪ Permanent | Doesn't change | Never (unless fundamentally wrong) |

## Time-Variant Data Points

### specifications/solar-panels-2026.md

| Data Point | Category | How to Refresh | Reference Value (2026-03) |
|-----------|----------|----------------|--------------------------|
| Top 10 panel rankings | 🟡 | Check [Clean Energy Reviews](https://www.cleanenergyreviews.info/blog/most-efficient-solar-panels) (updated monthly) | Aiko #1 at 25.0% |
| Panel pricing per watt | 🔴 | Check [EnergySage marketplace](https://www.energysage.com/solar/) or request installer quotes | $2.25-3.75/W range |
| Panel warranty terms | 🟢 | Check manufacturer websites directly | Maxeon 40yr, most others 25yr |
| Cell technology landscape | 🟢 | Clean Energy Reviews annual technology overview | TOPCon dominant, back-contact premium |
| Specific model numbers/wattages | 🟡 | Manufacturer websites, EnergySage panel database | See table in file |

### specifications/battery-systems-2026.md

| Data Point | Category | How to Refresh | Reference Value (2026-03) |
|-----------|----------|----------------|--------------------------|
| Battery installed prices | 🔴 | [EnergySage battery storage](https://www.energysage.com/solar/battery-storage/), installer quotes | PW3 ~$10.5-14K, Enphase ~$6-8K/unit |
| Battery specs (capacity, power) | 🟡 | Tesla, Enphase, FranklinWH product pages | See comparison table in file |
| Battery warranty terms | 🟢 | Manufacturer warranty documents | Tesla 10yr, Enphase 15yr, Franklin 15yr |
| New battery products entering market | 🟡 | [Solar Power World](https://www.solarpowerworldonline.com/), [PV Magazine](https://pv-magazine-usa.com/) | Three main players as of Q1 2026 |
| Gateway/controller pricing | 🔴 | Installer quotes, manufacturer price lists | $1,000-3,000 range |

### concepts/nec-rapid-shutdown.md

| Data Point | Category | How to Refresh | Reference Value (2026-03) |
|-----------|----------|----------------|--------------------------|
| NEC code section numbers & requirements | 🟢 | NFPA 70 (new edition every 3 years; next: 2026) | Current: NEC 2023, section 690.12 |
| State/jurisdiction NEC adoption | 🟡 | [NFPA adoption map](https://www.nfpa.org/education-and-research/electrical/nec-enforcement-maps) | Most on 2017/2020, 4+ on 2023 |
| UL 3741 listed products | 🟡 | UL product database, manufacturer announcements | Adoption growing but still early |

### faq/general.md

| Data Point | Category | How to Refresh | Reference Value (2026-03) |
|-----------|----------|----------------|--------------------------|
| Average system cost per watt | 🔴 | EnergySage Solar Marketplace data, SEIA reports | $2.50-3.50/W before incentives |
| Federal ITC percentage | 🟢 | IRS.gov, SEIA incentive tracker | 30% under IRA (through 2032) |
| State incentive programs | 🟡 | [DSIRE database](https://www.dsireusa.org/) | Varies by state |
| Net metering policies by state | 🟡 | DSIRE, state PUC websites | NEM 3.0 in CA, varies elsewhere |
| Average US home electricity usage | 🟢 | EIA Residential Energy Consumption Survey | ~10,000-11,000 kWh/yr |

### concepts/system-design-fundamentals.md

| Data Point | Category | How to Refresh | Reference Value (2026-03) |
|-----------|----------|----------------|--------------------------|
| String sizing math/formulas | ⚪ | N/A — physics doesn't change | Permanent |
| ASHRAE temperature data | 🟢 | Solar ABCs reference map | Permanent for a given site |
| Peak sun hours by region | ⚪ | N/A — long-term climate averages | Stable unless climate shifts |
| Temperature adders for mounting | ⚪ | NEC / PV industry standard | +25°C ground, +30-35°C roof |

### concepts/inverter-types.md

| Data Point | Category | How to Refresh | Reference Value (2026-03) |
|-----------|----------|----------------|--------------------------|
| Inverter architecture concepts | ⚪ | N/A — fundamental technology | Permanent |
| Brand market positioning | 🟡 | Industry news, company financials | Enphase leads micros, SolarEdge optimizers |
| Specific model numbers | 🟡 | Manufacturer product pages | IQ8 series, SolarEdge optimizers |

### troubleshooting/common-mistakes/top-diy-mistakes.md

| Data Point | Category | How to Refresh | Reference Value (2026-03) |
|-----------|----------|----------------|--------------------------|
| All content | ⚪/🟢 | Best practices are stable; code references may shift with new NEC editions | Permanent concepts, slow-moving code refs |

## Refresh Workflow

When refreshing this pack:

1. Start with 🔴 Volatile items — pricing and availability change fastest
2. Check 🟡 Fast-moving items — new products, ranking shifts, policy changes
3. Leave 🟢 and ⚪ items unless a major event triggers a change (new NEC edition, major manufacturer bankruptcy, etc.)
4. Update the "Reference Value" column after verification
5. Update "Last full review" date at top of this file
6. Commit with message: `Refresh: solar-diy freshness review YYYY-MM-DD`
