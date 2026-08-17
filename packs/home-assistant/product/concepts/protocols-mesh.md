---
title: "Mesh Network Concepts — Zigbee, Z-Wave, Thread"
type: concept
tags:
  - protocols
  - mesh
  - coordinator
  - zha
  - zigbee2mqtt
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/protocols-mesh
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - protocols-comparison.md
  - protocols-decision.md
  - network-zigbee-zwave.md
content_hash: sha256:dd7a895051a26d9463178bbaf629553ababc03315fc13f8cbdcc5636c014c138
---
# Mesh Network Concepts — Zigbee, Z-Wave, Thread

On Zigbee, Z-Wave, and Thread, mains-powered router devices relay messages and extend the mesh; battery end devices do not. The coordinator USB stick is the brain. In HA, start with ZHA; switch to Zigbee2MQTT when you need a device ZHA does not support.

## Mesh Network Concepts

Understanding mesh networking applies to Zigbee, Z-Wave, and Thread:

### Router vs End Device
- **Router devices** (mains-powered): stay awake, relay messages, extend the mesh. More routers = better coverage and reliability.
- **End devices** (battery-powered): connect to nearest router, sleep between transmissions, do NOT relay messages.

**Critical implication:** A battery-powered sensor in your garden shed only works if there's a mains-powered device (smart plug, light) within range to route its messages. Plan your mesh by placing mains-powered devices strategically.

### Coordinator
The coordinator is the "brain" of a Zigbee or Z-Wave network — it manages device pairing, routing tables, and network keys. In HA, this is typically a USB dongle plugged into your HA host.

**Popular coordinators:**
- Zigbee: Home Assistant Connect ZBT-1/ZBT-2 (official), Sonoff ZBDongle-E, SLZB-06/07 (Ethernet)
- Z-Wave: Home Assistant Connect ZWA-2 (official), Zooz ZST39, Aeotec Z-Stick

<!-- refresh
  decay: fast-moving
  as_of: 2026-Q1
  fields: [coordinator_models, recommended_dongles]
  source: https://www.home-assistant.io/integrations/zha/, community forums
  method: "Coordinator recommendations shift as new hardware releases. Check r/homeassistant for current recommendations and HA official hardware page."
-->

### Zigbee in HA: ZHA vs Zigbee2MQTT

Two main ways to run Zigbee in HA:

| | ZHA (Zigbee Home Automation) | Zigbee2MQTT |
|---|---|---|
| **Type** | Built-in HA integration | Add-on (runs Mosquitto MQTT broker) |
| **Setup** | Simpler — plug in coordinator, configure in UI | More involved — install add-on, configure MQTT |
| **Device support** | Good (~2000 devices) | Excellent (~3500+ devices) |
| **Configuration** | UI-based | Mix of UI and YAML |
| **Community preference** | Fine for most users | Power users often prefer |
| **Protocol independence** | Tied to HA | Can work without HA (just needs MQTT) |

**Recommendation:** Start with ZHA for simplicity. Switch to Zigbee2MQTT if you need a specific unsupported device or want more control. Migration between them is possible but not seamless.

## Related Concepts

- [[protocols-comparison.md|protocols comparison]]
- [[protocols-decision.md|protocols decision]]
- [[network-zigbee-zwave.md|network zigbee zwave]]
