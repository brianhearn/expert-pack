---
title: "Energy Automations"
type: concept
tags:
  - energy-management
  - solar-excess
  - ev-charging
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/energy-automations
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - energy-gotchas.md
  - energy-grid.md
  - automation-trigger-action.md
content_hash: sha256:f53d88e4cc76e894ed67159be42c337b8492b94d0e12a94226abfa5a77a2c3ea
---
# Energy Automations

Once energy sensors exist, automations can start the dishwasher on solar excess, charge the EV off-peak, and alert when monthly cost crosses a budget. These are numeric_state patterns on excess power, time, and cost sensors.

## Automation Opportunities

With energy monitoring in place, you can automate based on energy state:

### Solar excess — run appliances when production exceeds consumption

```yaml
automation:
  - alias: "Start dishwasher on solar excess"
    trigger:
      - trigger: numeric_state
        entity_id: sensor.solar_excess_power  # Template: production - consumption
        above: 1500  # More than 1.5kW excess
        for: "00:10:00"  # Stable excess for 10 minutes
    condition:
      - condition: state
        entity_id: binary_sensor.dishwasher_door_closed
        state: "on"  # Door closed = ready to run
      - condition: state
        entity_id: input_boolean.dishwasher_eco_mode
        state: "on"
    action:
      - action: switch.turn_on
        target:
          entity_id: switch.dishwasher_power
      - action: notify.mobile_app_brians_phone
        data:
          message: "🌞 Starting dishwasher — solar excess available"
```

### EV charging on off-peak

```yaml
automation:
  - alias: "Start EV charging at off-peak"
    trigger:
      - trigger: time
        at: "23:00:00"
    condition:
      - condition: numeric_state
        entity_id: sensor.ev_battery_level
        below: 80  # Only if not already charged
    action:
      - action: switch.turn_on
        target:
          entity_id: switch.ev_charger
```

### Budget alert

```yaml
automation:
  - alias: "Energy budget alert"
    trigger:
      - trigger: numeric_state
        entity_id: sensor.monthly_energy_cost
        above: 150  # Alert if monthly cost exceeds $150
    action:
      - action: notify.mobile_app_brians_phone
        data:
          title: "⚡ Energy Budget Alert"
          message: >
            Monthly energy cost is ${{ states('sensor.monthly_energy_cost') }}.
            Budget threshold of $150 exceeded.
```

## Related Concepts

- [[energy-gotchas.md|energy gotchas]]
- [[energy-grid.md|energy grid]]
- [[automation-trigger-action.md|automation trigger action]]
