---
title: "Home-Level vs Room-Level Presence"
type: concept
tags:
  - presence-detection
  - room-presence
  - home-presence
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/presence-home-vs-room
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - presence-sensor-fusion.md
  - presence-mmwave.md
  - presence-bayesian.md
content_hash: sha256:0b71e767cc4dbe7adb8780fb30454070606ce131741ab8fe5c21f14343671b17
---
# Home-Level vs Room-Level Presence

Home-level presence asks "is anyone home?" or "is Brian home?" Room-level asks "which room is Brian in?" They are different problems: phone/WiFi/door sensors for the house, mmWave and BLE for the room. Solve home-level first.

## Home-Level vs Room-Level Presence

These are two different problems with different solutions:

| | Home-Level | Room-Level |
|---|---|---|
| **Question** | Is anyone home? Is Brian home? | Which room is Brian in? |
| **Sensors** | Phone GPS, WiFi, door sensors | mmWave, BLE proximity, PIR |
| **Complexity** | Medium | High |
| **Use case** | HVAC, security, welcome automations | Motion lighting, TV automation, specific room scenes |
| **Reliability needed** | High (seconds matter) | High (false positives annoying) |

**Most HA users should solve home-level presence first**, then add room-level only for specific automations where it adds real value (like adjusting lighting when moving between rooms).

**Room-level approach:** One mmWave per room (for high-value automations) + ESPresense BLE proxies (ESP32 per room) for identity-aware room tracking. The combination lets you answer: "Brian is in the living room right now."

## Related Concepts

- [[presence-sensor-fusion.md|presence sensor fusion]]
- [[presence-mmwave.md|presence mmwave]]
- [[presence-bayesian.md|presence bayesian]]
