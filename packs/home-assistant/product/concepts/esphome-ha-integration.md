---
title: "ESPHome Home Assistant Integration"
type: concept
tags:
  - esphome-fundamentals
  - native-api
  - mdns
  - entities
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/esphome-ha-integration
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - esphome-what.md
  - esphome-ble-proxy.md
  - esphome-hardware-troubleshoot.md
content_hash: sha256:de0d64667e1db221aefa1c715579bbaed42491fa276983f96135e5f3be98648f
---
# ESPHome Home Assistant Integration

When an ESPHome device joins the same network as HA, mDNS discovery offers it as an integration and every YAML sensor/switch/light becomes an entity. Use `id:` for internal references and `name:` for the HA-facing label; `disabled_by_default` keeps noisy sensors off until you need them.

## Integration with Home Assistant

When an ESPHome device powers up and connects to the same network as HA, it announces itself via mDNS. HA automatically discovers it and shows a notification: "New ESPHome device found."

**Accept the integration → device and all entities appear automatically.**

Each sensor/switch/light defined in the YAML config becomes an HA entity:
- `sensor.bedroom_climate_temperature` (from `name: "Temperature"` in config named `bedroom-climate`)
- `binary_sensor.bedroom_climate_presence`
- `switch.bedroom_climate_garage_relay`

### Entity Naming Convention
ESPHome entity IDs follow: `domain.device_name_entity_name` where:
- Device name: the `name:` in `esphome:` block (spaces become underscores)
- Entity name: the `name:` in each component block

**Tip:** Use `id:` in components to reference them internally in the ESPHome YAML without affecting the HA entity name. Use `name:` for what appears in HA.

### Device Grouping in HA
All entities from one ESPHome device appear under one "Device" in HA (Settings → Devices). Assign the device to an Area for clean organization:
- ESPHome: `bedroom-climate` device in HA
- Assigned to Area: "Bedroom"
- All entities inherit the area context

### The `disabled_by_default: true` Pattern
Some sensors produce a lot of data you don't always need. Mark them as disabled by default in ESPHome:

```yaml
sensor:
  - platform: ld2410
    moving_energy:
      name: "Moving Energy"
      disabled_by_default: true   # Only enable in HA UI if you need it
```

This keeps the HA entity count manageable.

## Related Concepts

- [[esphome-what.md|esphome what]]
- [[esphome-ble-proxy.md|esphome ble proxy]]
- [[esphome-hardware-troubleshoot.md|esphome hardware troubleshoot]]
