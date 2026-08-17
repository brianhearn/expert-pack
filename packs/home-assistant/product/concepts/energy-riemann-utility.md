---
title: "Riemann Sum Energy and utility_meter"
type: concept
tags:
  - energy-management
  - riemann
  - utility-meter
  - integration
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/energy-riemann-utility
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - energy-dashboard.md
  - energy-grid.md
  - energy-automations.md
content_hash: sha256:b55eb3fd7723daa4a271dd68021745e989534f098f4366a31a3cd265fba32117
---
# Riemann Sum Energy and utility_meter

If you only have a power sensor (W), the `integration` (Riemann sum) platform derives kWh. `utility_meter` then slices that cumulative sensor into daily, monthly, or tariff cycles for cost reporting.

## Converting Power to Energy (Riemann Sum)

If your integration only provides a power sensor (watts), you need to derive an energy sensor. HA's built-in `integration` platform does this using the Riemann sum method — it integrates power over time to calculate energy.

```yaml
# configuration.yaml (or sensor.yaml if split)
sensor:
  - platform: integration
    name: "Living Room TV Energy"
    unique_id: living_room_tv_energy
    source: sensor.living_room_tv_power    # Your W sensor
    unit_prefix: k                          # Result in kWh (not Wh)
    unit_time: h                            # Per hour
    method: left                            # left, right, or trapezoidal
    round: 2
```

**Method explanation:**
- `left` — uses the value at the start of each interval. Slightly underestimates for rising power.
- `right` — uses the value at the end of each interval. Slightly overestimates.
- `trapezoidal` — averages start and end. Most accurate but requires more frequent updates.

For appliances with stable power draw (TV on = ~150W), `left` is fine. For appliances that ramp up and down (HVAC, EV charger), use `trapezoidal`.

**Important:** The accuracy of the Riemann sum depends on how often your power sensor updates. A sensor that only updates every 5 minutes on a rapidly changing load will have significant error. For energy monitoring hardware, configure the update interval to 30-60 seconds.

## The utility_meter Helper

The `utility_meter` integration creates cycle-based consumption tracking from a cumulative sensor. Essential for tracking daily/monthly usage for cost reporting or tariff management.

```yaml
# configuration.yaml
utility_meter:
  daily_energy:
    source: sensor.grid_consumption_kwh
    name: "Daily Energy Consumption"
    cycle: daily
    tariffs:
      - peak
      - off_peak
    
  monthly_energy:
    source: sensor.grid_consumption_kwh
    name: "Monthly Energy Consumption"
    cycle: monthly
  
  yearly_energy:
    source: sensor.grid_consumption_kwh
    name: "Yearly Energy Consumption"
    cycle: yearly
```

**What this gives you:**
- `sensor.daily_energy` — resets to 0 at midnight, shows today's consumption
- `sensor.monthly_energy` — resets at month start
- `sensor.yearly_energy` — resets at year start
- With tariffs: separate tracking for peak/off-peak periods

**Tariff automation (switching between peak/off-peak):**
```yaml
automation:
  - alias: "Set Peak Tariff"
    trigger:
      - trigger: time
        at: "16:00:00"
    action:
      - action: utility_meter.select_tariff
        target:
          entity_id: utility_meter.daily_energy
        data:
          tariff: peak
  
  - alias: "Set Off-Peak Tariff"
    trigger:
      - trigger: time
        at: "21:00:00"
    action:
      - action: utility_meter.select_tariff
        target:
          entity_id: utility_meter.daily_energy
        data:
          tariff: off_peak
```

## Related Concepts

- [[energy-dashboard.md|energy dashboard]]
- [[energy-grid.md|energy grid]]
- [[energy-automations.md|energy automations]]

Sources: [integration](https://www.home-assistant.io/integrations/integration/), [utility_meter](https://www.home-assistant.io/integrations/utility_meter/).
