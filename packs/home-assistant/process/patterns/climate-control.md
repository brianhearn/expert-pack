---
title: Climate Control Automation Patterns
type: pattern
tags:
- pattern
- climate-control
- automation
- thermostat
- home-assistant-process
pack: home-assistant-process
retrieval_strategy: standard
id: home-assistant/process/patterns/climate-control
verified_at: '2026-04-10'
verified_by: agent
---
---
sources:
  - type: documentation
    url: "https://www.home-assistant.io/integrations/generic_thermostat/"
    date: "2026-03"
  - type: documentation
    url: "https://www.home-assistant.io/integrations/schedule/"
    date: "2026-03"
  - type: community
    url: "https://community.home-assistant.io/t/climate-automation-patterns-megathread/490321"
    date: "2025-11"
  - type: community
    url: "https://www.reddit.com/r/homeassistant/comments/1e4r2v8/hvac_automation_guide_2025/"
    date: "2025-07"
---

# Climate Control Automation Patterns

> **Lead summary:** Climate automation is where home automation pays for itself in energy savings and comfort. The core patterns — schedule-based temperatures, presence-based setbacks, and window-open pauses — are simple to implement and generate real savings. More advanced patterns (per-room TRVs, pre-conditioning, solar-aware cooling) require more investment but deliver more value. The key insight is that most HVAC systems can be automated without replacing the thermostat — a $10 temperature sensor + HA's `generic_thermostat` can make a dumb baseboard heater smart, and IR blasters ($30) can control almost any HVAC system that has a remote.

## The generic_thermostat: Making Dumb Heaters Smart

The `generic_thermostat` integration turns any on/off switch + temperature sensor into a smart thermostat in HA. It implements a simple hysteresis controller: heat/cool to target ± deadband, turn on when below lower threshold, turn off when above upper threshold.

```yaml
# configuration.yaml
climate:
  - platform: generic_thermostat
    name: "Study Heater"
    unique_id: study_generic_thermostat
    heater: switch.study_space_heater      # The switch controlling your heater
    target_sensor: sensor.study_temperature  # Temperature sensor in the room
    min_temp: 15
    max_temp: 26
    ac_mode: false          # Set true for cooling
    target_temp: 20         # Default setpoint
    cold_tolerance: 0.5     # Turn on when temp drops 0.5°C below target
    hot_tolerance: 0.5      # Turn off when temp rises 0.5°C above target
    min_cycle_duration:
      seconds: 60           # Minimum on/off cycle to protect relays
    keep_alive:
      minutes: 5            # Send command every 5 min even if no change (prevents drift)
    initial_hvac_mode: "heat"
    away_temp: 15           # Temperature when in away mode
    precision: 0.1
```

**What you get:**
- A full `climate` entity with HVAC modes (heat/off/auto)
- Target temperature control from dashboard or voice
- Compatible with all HA automations that use `climate` entities
- Works with the schedule helper for time-based control

**Temperature sensor placement matters:** Put the sensor at body level in the zone the heater controls, away from the heater itself (thermal bleed causes oscillation). In a study, desk height in the center of the room is ideal.

**For AC mode:** Set `ac_mode: true`. The heater switch becomes the AC switch. HA turns it on when temperature exceeds the target + hot_tolerance.

## Schedule-Based Climate

The **Schedule helper** (Settings → Helpers → Create Helper → Schedule) creates a weekly schedule template that returns `true` or `false` for each time slot. Combined with a climate automation, it drives time-based temperature setbacks automatically.

**Create a schedule helper:**
```
Name: "Comfort Hours Schedule"
Schedule:
  Weekdays: 07:00-09:00, 17:00-22:00
  Weekends: 08:00-23:00
```

**Automation using the schedule:**
```yaml
automation:
  - alias: "Climate Schedule"
    mode: single
    triggers:
      - trigger: state
        entity_id: schedule.comfort_hours
    actions:
      - choose:
          # Schedule active = comfort temperature
          - conditions:
              - condition: state
                entity_id: schedule.comfort_hours
                state: "on"
            sequence:
              - action: climate.set_temperature
                target:
                  entity_id: climate.main_thermostat
                data:
                  temperature: 21
          # Schedule inactive = setback temperature
          - conditions:
              - condition: state
                entity_id: schedule.comfort_hours
                state: "off"
            sequence:
              - action: climate.set_temperature
                target:
                  entity_id: climate.main_thermostat
                data:
                  temperature: 17
```

**Alternative: Use climate.set_hvac_mode for true setbacks:**
Instead of just lowering the temperature, put the thermostat in `away` mode during setback periods, or turn it off entirely. The generic_thermostat's `away_temp` activates when HVAC mode is set to `heat` but the away preset is selected:

```yaml
- action: climate.set_preset_mode
  target:
    entity_id: climate.study_heater
  data:
    preset_mode: "away"  # Uses away_temp from config
```

## Presence-Based Climate

The cleanest energy-saving automation: don't heat or cool an empty house.

### Basic Presence Setback

```yaml
automation:
  - alias: "HVAC Presence Setback"
    mode: single
    triggers:
      - trigger: state
        entity_id: binary_sensor.anyone_home     # Group presence sensor
        to: "off"
        for: "00:15:00"  # Wait 15 min to avoid setback during quick trips
    actions:
      - action: climate.set_preset_mode
        target:
          entity_id: climate.main_thermostat
        data:
          preset_mode: "away"
  
  - alias: "HVAC Presence Resume"
    mode: single
    triggers:
      - trigger: state
        entity_id: binary_sensor.anyone_home
        to: "on"
    actions:
      - action: climate.set_preset_mode
        target:
          entity_id: climate.main_thermostat
        data:
          preset_mode: "home"
```

**The 15-minute delay for setback** prevents the thermostat from going to away mode when you step out briefly. The return trigger has no delay — when someone comes home, comfort should start immediately (or see pre-conditioning pattern below).

### Presence + Schedule Combined

Reality: you want presence-based setback, BUT you also don't want the house to heat up to comfort temperature at 2 AM when someone comes home late. Combine both:

```yaml
automation:
  - alias: "HVAC Presence Resume with Schedule Check"
    mode: single
    triggers:
      - trigger: state
        entity_id: binary_sensor.anyone_home
        to: "on"
    actions:
      - choose:
          # Arrival during comfort hours: full comfort temp
          - conditions:
              - condition: state
                entity_id: schedule.comfort_hours
                state: "on"
            sequence:
              - action: climate.set_temperature
                target:
                  entity_id: climate.main_thermostat
                data:
                  temperature: 21
          # Arrival outside comfort hours: modest recovery temp
          - conditions:
              - condition: state
                entity_id: schedule.comfort_hours
                state: "off"
            sequence:
              - action: climate.set_temperature
                target:
                  entity_id: climate.main_thermostat
                data:
                  temperature: 18  # Warm enough to be comfortable, not full comfort
```

## Window-Aware Climate

Heating with windows open wastes energy and strains the HVAC system. Automate the pause:

```yaml
automation:
  - alias: "Pause HVAC When Window Open"
    mode: single
    triggers:
      - trigger: state
        entity_id:
          - binary_sensor.living_room_window
          - binary_sensor.bedroom_window
          - binary_sensor.kitchen_window
        to: "on"
        for: "00:02:00"  # Only act if window stays open 2+ minutes (not just a quick peek)
    actions:
      - variables:
          previous_temp: "{{ state_attr('climate.main_thermostat', 'temperature') }}"
      - action: climate.turn_off
        target:
          entity_id: climate.main_thermostat
      - action: notify.mobile_app_brians_phone
        data:
          message: >
            🪟 HVAC paused — 
            {{ expand(trigger.entity_id) | map(attribute='name') | join(', ') }} open.
  
  - alias: "Resume HVAC When All Windows Closed"
    mode: single
    triggers:
      - trigger: state
        entity_id:
          - binary_sensor.living_room_window
          - binary_sensor.bedroom_window
          - binary_sensor.kitchen_window
        to: "off"
    conditions:
      # All windows must be closed
      - condition: state
        entity_id: binary_sensor.living_room_window
        state: "off"
      - condition: state
        entity_id: binary_sensor.bedroom_window
        state: "off"
      - condition: state
        entity_id: binary_sensor.kitchen_window
        state: "off"
    actions:
      - action: climate.turn_on
        target:
          entity_id: climate.main_thermostat
```

**For multi-zone systems:** Trigger per-zone. Only pause the zone for the room with the open window — don't penalize the whole house because one bedroom window is open.

## Humidity Management

High bathroom humidity → mold. Low house humidity → dry air, static, discomfort. Automate both.

### Bathroom Fan Automation (Humidity-Triggered)

The challenge: bathroom humidity rises and falls slowly. A simple threshold trigger fires too late (fan turns on when you're already done) and turns off too early (before humidity clears).

Better approach: detect the **rate of rise**:

```yaml
template:
  - sensor:
      - name: "Bathroom Humidity Rate of Change"
        unique_id: bathroom_humidity_roc
        unit_of_measurement: "%/min"
        state: >
          {% set current = states('sensor.bathroom_humidity') | float(0) %}
          {% set previous = state_attr('sensor.bathroom_humidity', 'yesterday') | float(current) %}
          {{ ((current - previous) / 5) | round(2) }}
```

This approach is imprecise — HA doesn't natively provide previous values in templates. A cleaner solution uses the `derivative` platform:

```yaml
sensor:
  - platform: derivative
    name: "Bathroom Humidity Change Rate"
    source: sensor.bathroom_humidity
    time_window: "00:05:00"  # Rate of change over 5 minutes
    unit_time: min
    round: 2
```

**Fan automation:**
```yaml
automation:
  - alias: "Bathroom Fan - Humidity Control"
    mode: restart
    triggers:
      # Turn on when rapid humidity rise detected (shower starting)
      - trigger: numeric_state
        entity_id: sensor.bathroom_humidity_change_rate
        above: 3  # Rising more than 3% per minute
    actions:
      - action: switch.turn_on
        target:
          entity_id: switch.bathroom_fan
      # Keep running until humidity drops back near baseline
      - wait_for_trigger:
          - trigger: numeric_state
            entity_id: sensor.bathroom_humidity
            below: 65  # Or below baseline + 5%
        timeout: "01:00:00"
        continue_on_timeout: true
      - action: switch.turn_off
        target:
          entity_id: switch.bathroom_fan
```

### Whole-Home Humidity

Humidifiers and dehumidifiers can be controlled via generic_thermostat in `ac_mode` with a humidity sensor (substituting temperature for humidity). Or use the `climate` entity if your humidifier has an integration.

## Multi-Zone Climate: TRVs

Thermostatic Radiator Valves (TRVs) attached to radiators or fan-coil units give per-room temperature control. Zigbee TRVs integrate with HA as `climate` entities.

**Recommended Zigbee TRVs (2025-2026):**

| Model | Price | Notes |
|-------|-------|-------|
| MOES BRT-100 | ~$25-30 | Popular, Z2MQTT support, good accuracy |
| Danfoss Ally | ~$45 | Premium quality, direct HA integration |
| Aqara SRTS-A01 | ~$35 | Zigbee, HomeKit, HA integration |
| SALUS TRV10RFP | ~$30 | Good Z2MQTT support |
| Sonoff TRVZB | ~$25 | New (2024), good support, affordable |

**TRV-based per-room automation:**
```yaml
automation:
  - alias: "Office TRV - Work Hours"
    mode: single
    triggers:
      - trigger: time
        at: "08:30:00"
    conditions:
      - condition: time
        weekday: [mon, tue, wed, thu, fri]
    actions:
      - action: climate.set_temperature
        target:
          entity_id: climate.office_trv
        data:
          temperature: 22
  
  - alias: "Office TRV - After Hours"
    mode: single
    triggers:
      - trigger: time
        at: "18:00:00"
    actions:
      - action: climate.set_temperature
        target:
          entity_id: climate.office_trv
        data:
          temperature: 16
```

**Multi-zone consideration:** If your main boiler doesn't know TRVs have closed all valves, it keeps running and wastes energy. Advanced setups send a "demand" signal to the boiler based on whether any TRV is calling for heat. This typically requires an extra relay or smart boiler integration.

## Pre-Conditioning: Heat Before Arrival

Start heating/cooling before someone arrives home, so it's comfortable when they walk in.

**Method 1: Time-based pre-conditioning**
```yaml
automation:
  - alias: "Pre-condition for Evening Arrival"
    mode: single
    triggers:
      - trigger: time
        at: "16:30:00"  # 30 minutes before typical 5 PM arrival
    conditions:
      - condition: state
        entity_id: binary_sensor.anyone_home
        state: "off"  # Only if no one is home yet
      - condition: time
        weekday: [mon, tue, wed, thu, fri]
    actions:
      - action: climate.set_temperature
        target:
          entity_id: climate.main_thermostat
        data:
          temperature: 21
```

**Method 2: GPS-based pre-conditioning (better)**
Using the companion app's distance-to-home sensor:

```yaml
automation:
  - alias: "Pre-condition on Approach"
    mode: single
    triggers:
      - trigger: numeric_state
        entity_id: sensor.brians_phone_distance_from_home
        below: 5  # km — within 5km of home
    conditions:
      - condition: state
        entity_id: person.brian
        state: "not_home"  # Not already home
      - condition: time
        after: "16:00:00"
        before: "20:00:00"
    actions:
      - action: climate.set_temperature
        target:
          entity_id: climate.main_thermostat
        data:
          temperature: 21
      - action: notify.mobile_app_brians_phone
        data:
          message: "🏠 Pre-heating home — see you in ~{{ (state_attr('sensor.brians_phone_distance_from_home', 'value') | float / 60 * 60) | round(0) }} minutes"
```

## External Temperature Integration

On mild days, running AC when you could just open windows wastes energy and money.

```yaml
automation:
  - alias: "Suggest Open Windows Instead of AC"
    mode: single
    triggers:
      - trigger: state
        entity_id: climate.main_thermostat
        to: "cool"  # AC just turned on
    conditions:
      - condition: numeric_state
        entity_id: sensor.outdoor_temperature
        below: 22  # Outside temp below indoor target
      - condition: numeric_state
        entity_id: sensor.outdoor_humidity
        below: 70  # Not too humid outside
    actions:
      - action: climate.turn_off
        target:
          entity_id: climate.main_thermostat
      - action: notify.mobile_app_brians_phone
        data:
          title: "🌬️ Open the windows?"
          message: >
            It's {{ states('sensor.outdoor_temperature') }}°C outside — 
            cooler than your AC setpoint. Consider opening windows instead.
          data:
            actions:
              - action: OPEN_WINDOWS_NOTED
                title: "Thanks, I'll open them"
              - action: KEEP_AC_ON
                title: "No, keep AC on"
```

Handle the notification response:
```yaml
automation:
  - alias: "Open Windows Suggestion - Keep AC On"
    triggers:
      - trigger: event
        event_type: mobile_app_notification_action
        event_data:
          action: KEEP_AC_ON
    actions:
      - action: climate.set_hvac_mode
        target:
          entity_id: climate.main_thermostat
        data:
          hvac_mode: cool
```

## Common Integrations

### Smart Thermostats with Direct HA Support

**Ecobee:** Official integration, full control + sensor readings from room sensors. Ecobee room sensors appear as temperature sensors in HA. The integration polls via Ecobee's API (cloud).

**Nest (via Google SDM API):** Google's official Device Access program gives local-ish API access. Requires developer registration (~$5 one-time) and Google Cloud project setup. Integration is stable and actively maintained.

**Honeywell/Resideo:** Via cloud API. Works but latency is higher than desired.

### Dumb HVAC via IR Blaster

If your AC/heat pump uses a remote control, an IR blaster can control it:

**Broadlink RM4 Pro (~$30):** WiFi IR blaster with HA integration. Learn the IR codes from your remote, then send them from HA. Appears as a `remote` entity.

**ESPHome IR Transmitter (DIY, $5):** IR LED + ESP32 running ESPHome. More flexible, local-only, no cloud.

```yaml
# ESPHome IR example for a Mitsubishi mini-split
climate:
  - platform: mitsubishi_heatpump
    name: "Living Room AC"
    # Uses ClimateIR component for standard protocols
```

The ESPHome ClimateIR component supports many manufacturers (Mitsubishi, Daikin, Fujitsu, LG, Samsung, Panasonic). If your brand is supported, you get a proper `climate` entity — not just a dumb IR blaster.

**Limitation of IR:** No feedback. HA sends a command but doesn't know if the AC actually changed state (the remote disappeared, power outage reset it, etc.). Add a temperature sensor in the room to verify effect.

## Related

- Presence Detection — The multi-sensor presence model that powers presence-based climate
- Energy Management — Track HVAC energy consumption, optimize for solar excess
- Automation Fundamentals — Triggers, conditions, modes for climate automations
