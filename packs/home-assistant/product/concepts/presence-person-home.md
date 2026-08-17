---
title: "Unified Person-Home Template"
type: concept
tags:
  - presence-detection
  - template
  - delay-off
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/presence-person-home
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - presence-bayesian.md
  - presence-sensor-fusion.md
  - yaml-templates.md
content_hash: sha256:15ae83554fdcc3ef1a9e84ac7128d98f75b7ec54c5cdb0b6799fcbc837c461bc
---
# Unified Person-Home Template

A template binary sensor can require two of four presence signals (or a high-confidence Bayesian) before declaring someone home. `delay_off` keeps the sensor on through brief WiFi drops so lights do not cut out mid-room.

## Template Sensor: Unified "Person Home" State

Combine multiple imperfect trackers into one reliable sensor:

```yaml
template:
  - binary_sensor:
      - name: "Brian Home Reliable"
        unique_id: brian_home_reliable
        device_class: presence
        delay_off: "00:05:00"  # Don't flip to 'away' until 5 minutes of no evidence
        state: >
          {% set phone_home = is_state('person.brian', 'home') %}
          {% set wifi_home = is_state('device_tracker.brians_phone_wifi', 'home') %}
          {% set ble_home = is_state('device_tracker.brians_phone_ble', 'home') %}
          {% set mmwave_active = is_state('binary_sensor.living_room_mmwave', 'on') %}
          
          {# Require at least 2 of 4 signals, OR Bayesian is high confidence #}
          {% set signal_count = [phone_home, wifi_home, ble_home, mmwave_active] | select('true') | list | count %}
          {% set bayesian_home = is_state('binary_sensor.brian_home_bayesian', 'on') %}
          
          {{ signal_count >= 2 or bayesian_home }}
        availability: >
          {{ not is_unavailable('person.brian') }}
```

**Key detail:** The `delay_off` attribute on the template binary_sensor means the sensor stays "on" (home) for 5 minutes after the conditions stop being true. This prevents the lights going off just because your phone briefly dropped WiFi when walking from the living room to the kitchen.

## Related Concepts

- [[presence-bayesian.md|presence bayesian]]
- [[presence-sensor-fusion.md|presence sensor fusion]]
- [[yaml-templates.md|yaml templates]]
