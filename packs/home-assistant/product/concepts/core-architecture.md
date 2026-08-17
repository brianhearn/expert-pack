---
title: "Core Architecture — The HA Hierarchy"
type: concept
tags:
  - core-architecture
  - integrations
  - devices
  - entities
  - areas
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/core-architecture
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - core-state-machine.md
  - core-services-install.md
  - protocols-comparison.md
content_hash: sha256:297e2c0e801af6cbaabc39b4a8c6f5090556f55e21fe79ab43916e786312ae33
---
# Core Architecture — The HA Hierarchy

Home Assistant is organized as integration → device → entity → state → attributes. An integration is the software bridge, a device groups related entities, and the entity is the atomic unit automations and dashboards actually read. Understanding this hierarchy is the pack's entry concept.

## The Hierarchy

```
Integration (software bridge)
  └── Device (physical or logical unit)
        └── Entity (sensor, switch, light, etc.)
              └── State (on/off, 72°F, detected, etc.)
                    └── Attributes (brightness, color, battery %)
```

### Integrations

An integration is a piece of software that connects Home Assistant to an external system — hardware, cloud service, protocol, or platform. Examples: Philips Hue integration talks to the Hue Bridge. MQTT integration connects to an MQTT broker. Weather integration pulls forecast data from an API.

**Key facts:**
- Over 2000 official integrations exist
- Most are configured via the UI (Settings → Devices & Services → Add Integration)
- Some require YAML configuration in `configuration.yaml`
- Custom integrations (via HACS) extend beyond official support
- Integrations can be cloud-dependent (marked with ☁️ icon) or fully local

### Devices

A device is a logical grouping of related entities. One physical device typically creates one HA device with multiple entities. Example: a Zigbee motion sensor (one device) creates entities for motion detection, temperature, light level, and battery percentage.

**Key facts:**
- Devices are created automatically by integrations — you don't create them manually
- A device can belong to one Area (room/zone)
- Device info includes manufacturer, model, firmware version
- Some "devices" are logical, not physical (weather service creates a device with forecast entities)

### Entities

The atomic unit of HA. An entity represents one measurable or controllable thing. Every entity has:
- **Entity ID** — unique identifier (format: `domain.name`, e.g., `light.living_room`, `sensor.outdoor_temp`)
- **State** — current value (`on`, `off`, `72.5`, `home`, `detected`)
- **Attributes** — additional data beyond the state (brightness, color_temp, battery, friendly_name)
- **Domain** — what type of entity it is (light, switch, sensor, binary_sensor, climate, etc.)

**Key facts:**
- Entity IDs are permanent once created — renaming requires care (automations reference them)
- States are always strings internally (even numbers)
- The state + attributes together describe everything HA knows about that entity right now
- Entity history is recorded in the database (configurable retention)

### Areas

Organizational grouping for devices and entities by physical location (room, floor, zone). Areas are optional but highly recommended — they enable floor plans, area-based automations ("turn off all lights in the bedroom"), and dashboard organization.

## Related Concepts

- [[core-state-machine.md|core state machine]]
- [[core-services-install.md|core services install]]
- [[protocols-comparison.md|protocols comparison]]

Sources: [HA concepts and terminology](https://www.home-assistant.io/getting-started/concepts-terminology/).
