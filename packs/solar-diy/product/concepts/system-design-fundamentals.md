---
title: "System design — energy, roof, and battery"
type: concept
tags: [system-design, energy-needs, roof-assessment]
pack: solar-diy-product
retrieval_strategy: standard
id: solar-diy/product/concepts/system-design-fundamentals
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - system-design-string-sizing.md
  - inverter-microinverters.md
  - inverter-string.md
content_hash: sha256:4e17b3c4c1d3446d2bb045963c5f1c96c4688a06053befb2ff9120a643ea3e08
---

# System design — energy, roof, and battery

Residential array sizing starts from annual kWh and usable roof, then inverter architecture, then (for string systems) voltage-limited string math, then battery if you want backup. Peak-sun-hour and efficiency assumptions dominate the kW result; shade and setbacks dominate what actually fits.

## Energy needs

Read the bill for 12-month kWh and seasonal peaks. Typical US home: 10,000–11,000 kWh/year (climate and size swing this hard).

```
System size (kW) = Annual kWh ÷ (Peak sun hours/day × 365 × System efficiency)
```

Peak sun hours: Northeast 3.5–4.5, Southeast 4.5–5.5, Southwest 5.5–7.0. System efficiency (inverter, wiring, soiling, temperature): typically 75–85%.

Example: 10,000 kWh/year in Florida (5.0 PSH, 80%): `10,000 ÷ (5.0 × 365 × 0.80) = 6.85 kW` — about 16 × 450W modules.

## Roof

**Azimuth (Northern Hemisphere):** due south (180°) is best. 135°–225° loses ~5–10%. East/west loses ~15–25% (still viable with microinverters). North is generally not viable in the US.

**Tilt:** ≈ latitude for annual yield. Common 4:12–8:12 (18°–34°) is usually close enough. Flat roofs need tilt racks.

**Shade:** a chimney or branch wrecks a string inverter. Use microinverters or optimizers, and a shade study (Project Sunroof, Aurora, or a pro).

**Usable area:** subtract fire setbacks (often 3 ft from ridge, 18" from edges), vents, skylights, HVAC. A 450W module is about 21 sq ft (~3.5' × 6').

## Battery sizing

1. **Which loads?** Essentials (fridge, lights, Wi-Fi) ~3–5 kW. Whole-home with A/C 10–15 kW+.
2. **How long?** One night of essentials ≈ 5–10 kWh. A full day whole-home ≈ 30–50 kWh.
3. **Motor start?** Check LRA vs A/C compressor and well-pump.
4. **Grid-tied backup vs off-grid?** Backup sizes to outage length; off-grid needs multi-day autonomy.

Product comparisons: [[battery-systems-2026]]. String voltage math: [[system-design-string-sizing]].

## Related Concepts

- [[system-design-string-sizing]]
- [[inverter-microinverters]]
- [[inverter-string]]
- [[battery-systems-2026]]
