---
title: "Multi-Sensor Presence Fusion"
type: concept
tags:
  - presence-detection
  - sensor-fusion
  - companion-app
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/presence-sensor-fusion
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - presence-wifi-ble.md
  - presence-mmwave.md
  - presence-home-vs-room.md
content_hash: sha256:678f75bbc66cd95d165112f7e1a1393e0718c6f6a0198d1b026e69ec050383c7
---
# Multi-Sensor Presence Fusion

The reliable presence pattern is not better phone tracking — it is defense in depth. Multiple independent sensors each contribute evidence for or against presence, fused into a single verdict that degrades gracefully when one layer fails.

## The Multi-Sensor Fusion Strategy

The reliable pattern is not "better phone tracking" — it's **defense in depth**: multiple independent sensors that each contribute evidence for or against presence, fused into a single confident verdict.

```
┌─────────────────────────────────────────────────────┐
│              Person: "Brian Home?" State             │
├──────────────┬──────────────┬───────────────────────┤
│  Phone GPS   │ WiFi Device  │  Bluetooth Proxy      │
│  (coarse,    │  Tracker     │  (room-level,         │
│   delayed)   │  (fast, LAN) │   requires BLE)       │
├──────────────┴──────────────┴───────────────────────┤
│    mmWave Radar (room-level, no false negatives)     │
│    Door Contact Sensors (edge detection)             │
└─────────────────────────────────────────────────────┘
```

Each layer has different strengths and failure modes. Combined, the false negative/positive rate drops dramatically.

### Layer 1: Companion App (Phone GPS + WiFi)

Still valuable as a layer, especially for the "definitely left home" signal. Works best when:
- User has disabled battery optimization for the HA app (see below)
- Zone radius is set to 250-500m to compensate for GPS drift
- "WiFi router integration" augments it (below)

**Android: Disable battery optimization for HA Companion:**
Settings → Apps → Home Assistant → Battery → Unrestricted (not "Optimized")
This step is mandatory on Samsung/Xiaomi/OnePlus. Otherwise the app will be killed within 30-60 minutes.

**iOS: Background App Refresh:**
Settings → Home Assistant → Background App Refresh: ON
Also: Settings → Privacy → Location Services → Home Assistant → Always (not "While Using")

## Related Concepts

- [[presence-wifi-ble.md|presence wifi ble]]
- [[presence-mmwave.md|presence mmwave]]
- [[presence-home-vs-room.md|presence home vs room]]

Sources: [HA presence megathread](https://community.home-assistant.io/t/presence-detection-megathread/580060).
