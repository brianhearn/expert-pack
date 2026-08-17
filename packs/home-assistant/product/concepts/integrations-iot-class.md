---
title: "Integration IoT Class and Quality"
type: concept
tags:
  - integrations-guide
  - iot-class
  - quality-scale
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/integrations-iot-class
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - integrations-quality-eval.md
  - integrations-top-used.md
  - integrations-mqtt-cloud.md
content_hash: sha256:a7143dd6905458d4179dfe77d1177bece035c3ad55d0ed3d0aa1ff1288b6aae4
---
# Integration IoT Class and Quality

Every official HA integration has an IoT class describing how it communicates. Local push is instant and works without internet; cloud poll depends on a vendor API that can disappear. The killer question for any WiFi device: if internet dies, does this still work?

## IoT Classes — The Most Important Integration Attribute

Every official HA integration has an **IoT class** — a label describing how it communicates. This is the #1 signal for reliability and independence:

| IoT Class | How It Works | Local Control | Reliability | Example |
|-----------|-------------|---------------|-------------|---------|
| **Local Push** | Device sends data directly to HA, no polling | ✅ Yes | ⭐⭐⭐⭐⭐ | Philips Hue (local), ESPHome, Zigbee |
| **Local Poll** | HA regularly requests data from device on LAN | ✅ Yes | ⭐⭐⭐⭐ | UniFi, some Shelly models |
| **Cloud Push** | Cloud service forwards device data to HA | ❌ Cloud | ⭐⭐⭐ | Nest (cloud API) |
| **Cloud Poll** | HA polls a cloud API for data | ❌ Cloud | ⭐⭐ | Most "smart" WiFi devices |
| **Assumed State** | HA can't confirm device state, assumes it based on last command | N/A | ⭐ | Some RF remotes, IR blasters |

**What this means practically:**
- **Local Push**: instant, always works even without internet, responds in milliseconds
- **Cloud Poll**: depends on manufacturer's server staying up (Tuya shut down in 2023, Wemo shut down their API, etc.), introduces latency (5-30 seconds), stops working if they kill the API
- **Assumed State**: HA "thinks" the light is on but doesn't actually know — if something else changed the state, HA is wrong

**The killer question for any WiFi device:** "If my internet goes down, will this still work?" Local Push = yes. Anything cloud = no.

## Related Concepts

- [[integrations-quality-eval.md|integrations quality eval]]
- [[integrations-top-used.md|integrations top used]]
- [[integrations-mqtt-cloud.md|integrations mqtt cloud]]

Sources: [HA integrations](https://www.home-assistant.io/integrations/).
