---
title: "ESPHome BLE Proxy"
type: concept
tags:
  - esphome-fundamentals
  - bluetooth-proxy
  - ble
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/esphome-ble-proxy
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - esphome-what.md
  - presence-wifi-ble.md
  - esphome-ha-integration.md
content_hash: sha256:42825e9f6df563bae58b37d21ec9680d343f92dd02e9d2ed5eeac7690467111d
---
# ESPHome BLE Proxy

Any ESP32 can become a Bluetooth antenna for HA. `bluetooth_proxy` plus `esp32_ble_tracker` extends BLE range so thermometers, plant sensors, scales, and phone presence work throughout the house. One proxy per floor is enough.

## BLE Proxy — Turning ESP32s into Bluetooth Antennas

This is one of the most valuable and underappreciated ESPHome features. ESP32s placed around the house extend HA's Bluetooth range, enabling detection of BLE devices anywhere in the home.

```yaml
# Add to any ESP32 ESPHome config to make it a BLE proxy
bluetooth_proxy:
  active: true              # Active mode: sends connection requests, enables config of BLE devices
                            # vs passive: scan-only, lower power

esp32_ble_tracker:
  scan_parameters:
    active: true
    interval: 1100ms
    window: 1100ms
    continuous: true
```

**What BLE proxy enables:**
- Bluetooth integration devices (thermometers, plant sensors, scales, etc.) work even if they're far from the HA host
- Presence detection via phone BLE (see [[presence-sensor-fusion.md|Presence fusion]])
- Govee/Xiaomi/SwitchBot Bluetooth sensors work throughout the house
- HA automatically uses whichever proxy is closest to a device

**Best placement:** One ESP32 BLE proxy per floor or large area. They don't need to do anything else (though combining with a climate sensor in the same device is common).

## Related Concepts

- [[esphome-what.md|esphome what]]
- [[presence-wifi-ble.md|presence wifi ble]]
- [[esphome-ha-integration.md|esphome ha integration]]

Sources: [bluetooth_proxy](https://esphome.io/components/bluetooth_proxy.html).
