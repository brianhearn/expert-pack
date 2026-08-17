---
title: "What ESPHome Is — ESP32 vs ESP8266"
type: concept
tags:
  - esphome-fundamentals
  - esp32
  - esp8266
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/esphome-what
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - esphome-flash-ota.md
  - esphome-yaml.md
  - esphome-ble-proxy.md
content_hash: sha256:8c14727e0802f21c5f5b379570910073cca4995467242667aacc814db69f2478
---
# What ESPHome Is — ESP32 vs ESP8266

ESPHome turns a YAML description of your hardware into firmware for a $5–15 ESP microcontroller. HA discovers the device via the native API — fully local, no cloud. Always buy ESP32 for new work; ESP8266 is leftover-drawer only.

## What ESPHome Is

ESPHome is a framework that turns YAML configuration files into firmware for ESP microcontrollers. You describe your hardware in YAML (what sensors are connected to which pins, what the WiFi credentials are, etc.) and ESPHome generates and compiles C++ firmware — without you writing a line of C++.

**Why this matters:**
- ESP32 dev boards cost $5-12 on Amazon or AliExpress
- Sensors (temperature, humidity, CO2, radar, light, etc.) cost $2-20
- Total cost: $10-35 for a sensor that would cost $50-150 commercially
- No cloud: ESPHome devices talk directly to HA via a native API (encrypted, local)
- Instant state updates: native API pushes updates vs MQTT polling
- Deep HA integration: entities auto-discovered, attributes exposed, device page in HA

ESPHome is maintained by Nabu Casa and ships as an official add-on in HA OS. It's not a community hack — it's a first-class citizen.

## ESP32 vs ESP8266 — Always Choose ESP32

The ESP8266 was the original "cheap WiFi microcontroller." The ESP32 superseded it and is the correct choice for essentially all new projects.

| Feature | ESP8266 | ESP32 |
|---------|---------|-------|
| Price | ~$3-5 | ~$5-10 |
| RAM | 80 KB | 520 KB+ |
| CPU | Single core 80/160 MHz | Dual core 240 MHz |
| Bluetooth | ❌ No | ✅ Yes (BLE 4.2/5.0) |
| Bluetooth Proxy | ❌ Not possible | ✅ Core feature |
| GPIO pins | 17 usable | 34+ usable |
| ADC channels | 1 (unreliable) | 18 (reliable) |
| Hardware encryption | ❌ | ✅ |
| ESPHome support | Legacy | Full |

**Only reason to use ESP8266 today:** You have them in a drawer and want to use them up. For anything new, buy ESP32.

**Popular ESP32 boards:**

| Board | Notes |
|-------|-------|
| **ESP32-WROOM-32 / D1 Mini32** | Generic, cheap ($5-8), good for most projects |
| **ESP32-S3** | More GPIO, USB native, better for LED projects |
| **ESP32-C3** | RISC-V core, BLE 5.0, very cheap ($4-6), no dual-core |
| **ESP32-C6** | WiFi 6 + Zigbee/Thread capable (future-proof) |
| **Seeed XIAO ESP32C3** | Tiny form factor, good for embedded projects |

The Apollo Automation sensors (popular mmWave + HA sensors) use ESP32-C3 or S3. Athom (sells pre-flashed ESPHome plugs/sensors) uses various ESP32 variants.

## Related Concepts

- [[esphome-flash-ota.md|esphome flash ota]]
- [[esphome-yaml.md|esphome yaml]]
- [[esphome-ble-proxy.md|esphome ble proxy]]

Sources: [ESPHome docs](https://esphome.io/index.html).
