---
title: "ESPHome First Flash and OTA"
type: concept
tags:
  - esphome-fundamentals
  - ota
  - web.esphome.io
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/esphome-flash-ota
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - esphome-what.md
  - esphome-yaml.md
  - esphome-ha-integration.md
content_hash: sha256:0182515c839b8ca074c75d66d78c7712a9f05dd527399199ee18a254e3e0ae19
---
# ESPHome First Flash and OTA

The first flash needs a USB cable. After the device is on WiFi, every later update is OTA from the ESPHome dashboard or CLI. Use the HA add-on, web.esphome.io, or `esphome run`.

## First Flash: USB, Then OTA Forever

The first time you flash a device, you need a physical USB connection. After that, all updates are Over-The-Air (OTA) — no more USB cable.

### Initial Flash Options

**Option 1: ESPHome Dashboard (Add-on) — Easiest**
1. Install "ESPHome" add-on from HA Add-on Store
2. Open ESPHome Dashboard
3. Click "New Device" → follow wizard → plug ESP32 via USB to HA host (if Raspberry Pi/mini-PC) or use web serial in browser
4. Dashboard compiles and flashes automatically

**Option 2: web.esphome.io (No installation needed)**
- Navigate to https://web.esphome.io in Chrome/Edge
- Connect ESP32 via USB to your computer
- Flash a basic config, then adopt into HA ESPHome add-on

**Option 3: ESPHome CLI**
```bash
# Install on your computer (requires Python)
pip install esphome

# Create a config, compile and flash
esphome run my_device.yaml
```

### OTA Updates (all subsequent flashes)
Once a device is on your network, ESPHome handles OTA:
```bash
# Dashboard: click "Install" → picks OTA automatically if device is online
# CLI: esphome run my_device.yaml  # auto-detects OTA vs USB
```

## Related Concepts

- [[esphome-what.md|esphome what]]
- [[esphome-yaml.md|esphome yaml]]
- [[esphome-ha-integration.md|esphome ha integration]]
