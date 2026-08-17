---
title: "Smart Home Protocols at a Glance"
type: concept
tags:
  - protocols
  - zigbee
  - z-wave
  - matter
  - thread
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/protocols-comparison
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - protocols-decision.md
  - protocols-mesh.md
  - core-architecture.md
content_hash: sha256:a6e65074bed70b2c656bdfc2a92ed967f4bb5e846138ce6186fd343c46f88d47
---
# Smart Home Protocols at a Glance

For most Home Assistant users in 2025–2026, Zigbee is the best default protocol — local-only, low-power mesh, huge device selection. Z-Wave is the 868/912 MHz alternative; WiFi does not scale; Thread/Matter is promising but young. Most good setups run two or three protocols at once.

## The Protocols at a Glance

| Protocol | Frequency | Mesh? | Hub/Coordinator Required | Max Devices | Power | Local Control | Maturity |
|----------|-----------|-------|--------------------------|-------------|-------|---------------|----------|
| **Zigbee** | 2.4 GHz | ✅ Yes | Yes (dongle or bridge) | No practical limit | Very low (coin cell years) | ✅ Full | Very mature |
| **Z-Wave** | 868/912 MHz | ✅ Yes | Yes (dongle or bridge) | 232 per network | Low | ✅ Full | Very mature |
| **WiFi** | 2.4/5 GHz | ❌ No | No (uses existing router) | ~255 per subnet (often less) | High | ⚠️ Often cloud-dependent | Mature |
| **Thread** | 2.4 GHz | ✅ Yes | Yes (border router) | No practical limit | Very low | ✅ Full | Young |
| **Matter** | Varies (over WiFi, Thread, or Ethernet) | Depends on transport | Depends | Varies | Varies | ✅ Designed for local | Very young |
| **Bluetooth** | 2.4 GHz | Limited (BLE Mesh) | Proximity to HA host | Limited range | Low | ✅ Local | Mature but limited |
| **ESPHome** | 2.4 GHz (WiFi) | ❌ No | No (direct to HA via API) | Limited by WiFi capacity | Moderate | ✅ Full | Mature for DIY |

## Related Concepts

- [[protocols-decision.md|protocols decision]]
- [[protocols-mesh.md|protocols mesh]]
- [[core-architecture.md|core architecture]]
