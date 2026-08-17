---
title: "Zigbee and Z-Wave Topology on the LAN"
type: concept
tags:
  - network-architecture
  - zigbee
  - z-wave
  - usb-interference
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/network-zigbee-zwave
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - network-wifi.md
  - protocols-mesh.md
  - backup-zigbee-coordinator.md
content_hash: sha256:51695f28a10ecffa8eda31e158ada05ee023ae4ae229074f8b710e43d64ef4d8
---
# Zigbee and Z-Wave Topology on the LAN

Zigbee and Z-Wave are not on your IP network — they are separate meshes. The only IP touchpoint is the USB coordinator. A USB 2.0 extension cable away from USB 3.0 ports is the highest-impact reliability fix, and Zigbee channels 15/20/25/26 avoid WiFi 1/6/11 overlap.

## Zigbee and Z-Wave Network Topology

**Critical understanding:** Zigbee and Z-Wave are NOT on your IP network. They are separate mesh networks with their own addressing, routing, and protocols. The only thing that touches your IP network is the coordinator (USB dongle plugged into HA host).

```
[Zigbee/Z-Wave Mesh Network]           [IP Network]
  Sensor → Router → Router →         USB Coordinator → HA host
  Switch → Router → Coordinator  →  (TCP/IP for HA API)
  Bulb → (directly to coordinator)
```

**Implications:**
- VLANs don't affect Zigbee/Z-Wave at all — they're off-network
- "Zigbee VLAN" is not a thing. Don't try to segment them.
- Security threats to Zigbee are different (RF-based) and managed separately
- IoT isolation of WiFi devices doesn't affect Zigbee/Z-Wave security

### USB Extension Cables: The Most Important Hardware Tip

USB 3.0 ports emit significant RF interference in the 2.4 GHz band — the same band as Zigbee (and some Z-Wave frequencies). A Zigbee coordinator plugged directly into a USB 3.0 port on your HA machine will have dramatically reduced range and reliability.

**Solution:** Use a USB 2.0 extension cable (1-2 meters / 3-6 feet) to move the Zigbee/Z-Wave stick physically away from the USB 3.0 ports and the HA host's RF emissions.

This is one of those tips where the impact is massive and counterintuitive. Reports of range doubling and dropped devices reconnecting are common after adding the extension cable.

### Zigbee Channel Selection

Zigbee uses 2.4 GHz and shares the spectrum with WiFi. WiFi channels 1, 6, and 11 (the standard non-overlapping channels in the US) overlap with certain Zigbee channels.

**Zigbee channels that avoid WiFi overlap:**

| Zigbee Channel | Frequency | Clear of WiFi channels |
|---------------|-----------|----------------------|
| **15** | 2425 MHz | Yes — between WiFi ch 1 and 6 |
| **20** | 2450 MHz | Yes — between WiFi ch 6 and 11 |
| **25** | 2475 MHz | Marginal — near WiFi ch 11 |
| **26** | 2480 MHz | Best interference avoidance |

**Recommended:** Use Zigbee channel 25 or 26 if your WiFi uses channels 1/6/11. Check which channels your WiFi uses with a WiFi analyzer app (WiFi Analyzer on Android, NetSpot on macOS).

In ZHA: Settings → Devices & Services → Zigbee Home Automation → Configure → change channel (requires re-joining devices)

In Zigbee2MQTT: Set `channel` in `configuration.yaml`, restart to apply.

## Related Concepts

- [[network-wifi.md|network wifi]]
- [[protocols-mesh.md|protocols mesh]]
- [[backup-zigbee-coordinator.md|backup zigbee coordinator]]
