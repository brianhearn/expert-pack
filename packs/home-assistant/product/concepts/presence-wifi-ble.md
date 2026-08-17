---
title: "WiFi and BLE Presence Layers"
type: concept
tags:
  - presence-detection
  - wifi
  - bluetooth
  - espresence
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/presence-wifi-ble
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - presence-sensor-fusion.md
  - presence-mmwave.md
  - esphome-ble-proxy.md
content_hash: sha256:ca60435cfd1163e259eaafc5b1c7a57d3579d9afd4eff1d651007020657f3cfd
---
# WiFi and BLE Presence Layers

WiFi router device tracking and ESPHome BLE proxies are the two fastest local presence layers after the Companion app. WiFi answers "is this MAC on the LAN?" in seconds; BLE proxies (or ESPresense) push that down to room-level if the device is advertising.

### Layer 2: WiFi Router Device Tracking

Most modern routers (and dedicated integrations like UniFi, FritzBox, eero, GL.iNet) can report which devices are connected to the network. If your phone's MAC address is on the WiFi network, you're home. If it drops off, you've likely left.

**Advantages:**
- Faster than GPS (responds in seconds, not minutes)
- Works for family members who have the WiFi password but not the companion app
- Doesn't depend on app being awake

**Disadvantages:**
- MAC randomization (iOS 14+, Android 10+) rotates MAC addresses, making tracking unreliable unless you reserve a static MAC in the companion app or router
- Brief WiFi disconnections (elevator, moving room to room) cause false "away" signals

**Fix for MAC randomization:** The HA companion app can be configured to report a consistent network identifier. Alternatively, use ping-based detection (device_tracker.ping) against the DHCP reservation IP.
### Layer 3: Bluetooth Proximity via ESPHome BLE Proxy

This is the most underutilized layer and one of the most powerful for room-level presence. ESP32 devices running ESPHome can act as BLE (Bluetooth Low Energy) scanners, detecting the BLE advertisements from phones and BLE tags.

**Setup:**
1. Flash ESP32 with ESPHome (one per room or area)
2. Enable `bluetooth_proxy` component in ESPHome YAML
3. In HA, the ESP32 appears as a Bluetooth proxy — it extends BLE range throughout the house
4. Use the `bluetooth_tracker` integration or the `iBeacon` integration to track BLE-enabled devices

```yaml
# ESPHome BLE proxy configuration
bluetooth_proxy:
  active: true

esp32_ble_tracker:
  scan_parameters:
    active: true
    interval: 1100ms
    window: 1100ms
```

**Practical reality:** Phone BLE is not always discoverable (screen off, power save). Works better with dedicated BLE tags (like Nut mini, Tile, or Apple AirTags via OpenHAB... no — use ESPresense for this pattern). **ESPresense** is a purpose-built firmware for ESP32 that specializes in BLE room-level detection. It tracks specific BLE devices (phone, watch, earbuds) per room.

## Related Concepts

- [[presence-sensor-fusion.md|presence sensor fusion]]
- [[presence-mmwave.md|presence mmwave]]
- [[esphome-ble-proxy.md|esphome ble proxy]]
