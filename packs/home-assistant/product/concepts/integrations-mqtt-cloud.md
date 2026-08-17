---
title: "MQTT Bridge and Cloud vs Local"
type: concept
tags:
  - integrations-guide
  - mqtt
  - local-push
  - tasmota
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/integrations-mqtt-cloud
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - integrations-troubleshooting.md
  - integrations-reliability.md
  - integrations-iot-class.md
content_hash: sha256:eeea26a7cf74308a0bf702f227c4b8d5872d219d83993607f5c6b390b4abb8b4
---
# MQTT Bridge and Cloud vs Local

MQTT is the universal protocol bridge — Tasmota, Zigbee2MQTT, and DIY sensors all publish to a broker HA already speaks. If the goal is a local smart home, replace cloud integrations with local equivalents as devices wear out rather than ripping everything at once.

## Cloud vs Local — The Replacement Playbook

If your goal is a truly local smart home (no cloud dependencies), here's what to replace:

| Cloud Integration | Local Alternative |
|-------------------|------------------|
| Tuya / Smart Life | Flash with Tasmota/ESPHome (if ESP chip), or buy Zigbee equivalents |
| Wemo | Replace with Shelly (local) or Zigbee plugs |
| Nest Thermostat | Keep (no good open local alternative) OR Ecobee (same caveat) |
| Ring Doorbell | Reolink doorbell (local) or any RTSP-capable camera + Frigate |
| TP-Link Kasa | The official integration supports local API — configure local mode |
| LIFX | Use local LIFX integration, not cloud |
| Philips Hue | Use Hue Bridge v2 local API |
| SmartThings devices | Depends — some support Zigbee/Z-Wave directly |

**Protocol migration strategy:** Don't rip and replace everything at once. As cloud-dependent devices need replacement, replace them with local equivalents (Zigbee/Z-Wave/ESPHome).

## MQTT — The Universal Protocol Bridge

MQTT is a lightweight pub/sub messaging protocol. It's not a product — it's the glue that connects many different systems to HA.

**When to use MQTT:**
- Tasmota-flashed devices (cloud Tuya devices reflashed with open firmware)
- Zigbee2MQTT (Zigbee through MQTT instead of ZHA)
- DIY sensors (custom ESP firmware, Node-RED to HA)
- Industrial sensors and controllers
- Any device that "speaks MQTT"

**Setup:** Install the Mosquitto MQTT Broker add-on (HA add-on store), then install the MQTT integration in HA. Devices publish to topics, HA subscribes.

**Autodiscovery:** Devices that support MQTT Discovery (Tasmota, Zigbee2MQTT, ESPHome MQTT mode) automatically create entities in HA by publishing their configuration to specific MQTT topics. No manual configuration required.

## Related Concepts

- [[integrations-troubleshooting.md|integrations troubleshooting]]
- [[integrations-reliability.md|integrations reliability]]
- [[integrations-iot-class.md|integrations iot class]]
