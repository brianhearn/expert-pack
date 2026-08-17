---
title: "mmWave and Door-Sensor Presence"
type: concept
tags:
  - presence-detection
  - mmwave
  - ld2410
  - door-sensor
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/presence-mmwave
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - presence-sensor-fusion.md
  - presence-wifi-ble.md
  - esphome-sensors-climate.md
content_hash: sha256:1416f0d5754a8efae33a88969ef646197452681d56c79330dd145c9a060fa61d
---
# mmWave and Door-Sensor Presence

mmWave radar detects micro-motion — breathing and stillness — so it does not false-clear when someone sits still. Door contact sensors do not track presence directly, but they are the fastest edge detectors for arrivals and departures.

### Layer 4: mmWave Radar (Room-Level, Foolproof)

mmWave sensors detect micro-motion — breathing, heartbeat, even stillness — making them impervious to the "person sitting still watching TV" false negative that defeats PIR sensors. They are the ground truth at room level.

**2025-2026 mmWave Recommendations:**

| Sensor | Price | Connection | Range | Best For |
|--------|-------|-----------|-------|----------|
| **Apollo MSR-1 / AIR-1** | ~$25-30 | ESPHome (USB-C) | 5-6m | Wired, DIY, best customization |
| **Apollo R PRO-1** | ~$35 | ESPHome (USB-C) | 8m | Best wired option, LD2450 chip for zone detection |
| **Aqara FP300** | ~$35-45 | Zigbee | 5m | Best battery-powered option, official Zigbee |
| **Aqara FP2** | ~$50 | WiFi (HomeKit/HA) | 5m | Reliable, multi-zone (5 zones), well-supported |
| **Sonoff SNZB-06P** | ~$12-15 | Zigbee | 4m | Best budget option, simple binary detection |
| **Tuya mmWave sensors** | ~$10 | WiFi/Zigbee | 4-5m | Inconsistent quality — verify model before buying |

**Apollo series (Apollo Automation)** are popular because they run ESPHome natively and the community firmware exposes all LD2410/LD2450 parameters directly in HA. You can tune sensitivity zones, detection angles, and timeouts from the HA UI.

**Aqara FP300** (released 2024-2025) is the best option for rental situations or anywhere you can't run wiring — USB-C battery-powered, Zigbee, and surprisingly accurate. The main limitation is battery life (~2-3 months depending on activity).

**Sonoff SNZB-06P** is the budget king — $12-15, Zigbee, works with ZHA and Zigbee2MQTT, provides reliable binary occupied/clear detection (not zone-level). For rooms where you just need "occupied or not", this is excellent value.
### Layer 5: Door Contact Sensors as Edge Detectors

Door sensors don't track presence directly, but they provide hard evidence: if the front door opened and no one was detected inside, someone left. If it opened and phone GPS went from "away" to "home" coordinates, someone arrived. Door sensors catch arrivals/departures faster than any other method.

**Pattern:** Use door sensor state change + tracker state as a cross-check:
```yaml
# If front door opens AND all person trackers are "not_home" → someone arrived
trigger:
  - trigger: state
    entity_id: binary_sensor.front_door_contact
    to: "on"
condition:
  - condition: state
    entity_id: person.brian
    state: "not_home"
action:
  - action: input_boolean.turn_on
    target:
      entity_id: input_boolean.possible_arrival_brian
```

## Related Concepts

- [[presence-sensor-fusion.md|presence sensor fusion]]
- [[presence-wifi-ble.md|presence wifi ble]]
- [[esphome-sensors-climate.md|esphome sensors climate]]
