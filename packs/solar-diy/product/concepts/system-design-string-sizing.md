---
title: "String sizing — cold Voc and hot Vmp"
type: concept
tags: [system-design, string-sizing, voc, inverter-string]
pack: solar-diy-product
retrieval_strategy: standard
id: solar-diy/product/concepts/system-design-string-sizing
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
requires:
  - inverter-string.md
related:
  - system-design-fundamentals.md
  - inverter-string.md
  - nec-rapid-shutdown.md
content_hash: sha256:230aea9d46fc8b326ffb68912bd1cabf92fba863ce510ce49121ee574fd0bce3
---

# String sizing — cold Voc and hot Vmp

String sizing is the voltage-limit calculation for string and string+optimizer systems. Microinverters skip it. Too many modules and cold-weather Voc exceeds the inverter maximum (damage or fire). Too few and hot-weather Vmp falls below MPPT minimum (dropout or underperformance).

## Maximum string (cold)

```
Voc_max = Voc × [1 + ((T_low - 25°C) × (TempCoef_Voc / 100))]
Max panels per string = Inverter max voltage ÷ Voc_max
```

Voc and TempCoef_Voc come from the module datasheet (TempCoef_Voc is negative %/°C). T_low is ASHRAE 2% low ambient. Round **down**.

## Minimum string (hot)

```
Vmp_min = Vmp × [1 + ((T_high + T_add - 25°C) × (TempCoef_Vmp / 100))]
Min panels per string = Inverter min MPPT voltage ÷ Vmp_min
```

T_high is ASHRAE 2% high. T_add by mount: roof parallel 6" standoff +30°C; roof flush +35°C; ground/pole +25°C. Round **up**.

## Worked example

Example equipment (verify current datasheets): 485W module Voc=45.9V, Vmp=45.63V, TempCoef_Voc=−0.27%/°C, TempCoef_Vmp=−0.34%/°C; SMA CORE1 max 1000V, MPPT 550–800V. Site: Portland, OR (T_low=−7°C, T_high=32°C, flush roof).

```
Voc_max = 45.9 × [1 + ((-7 - 25) × (-0.0027))] = 49.87V
Max panels = 1000 ÷ 49.87 = 20.05 → 20 max

Vmp_min = 45.63 × [1 + ((32 + 35 - 25) × (-0.0034))] = 39.11V
Min panels = 550 ÷ 39.11 = 14.06 → 15 min
```

Each string: 15–20 modules. The formulas are permanent; the example SKUs are not.

<!-- refresh
  decay: fast-moving
  as_of: 2026-Q1
  fields: [example_panel_model_specs, example_inverter_model_specs]
  source: manufacturer datasheets (qcells.com, sma.de)
  method: "The MATH is permanent — formulas never change. The example equipment specs may be outdated. Verify panel Voc/Vmp/TempCoef and inverter voltage ranges on current datasheets before using for real system design."
-->

## Temperature data

Solar ABCs / UCF ASHRAE lookup, NREL PVWatts, NOAA extremes. Do not size strings on average temperatures.

## Related Concepts

- [[inverter-string]]
- [[system-design-fundamentals]]
- [[nec-rapid-shutdown]]
