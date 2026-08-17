---
title: "ESPHome YAML Structure"
type: concept
tags:
  - esphome-fundamentals
  - yaml
  - api
  - ota
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/esphome-yaml
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - esphome-what.md
  - esphome-sensors-climate.md
  - esphome-flash-ota.md
content_hash: sha256:4e70f48b4bdd117061aa50f5420367310a29657df7a5d4acd9c6660c4d4a4d9d
---
# ESPHome YAML Structure

Every ESPHome config shares the same skeleton: `esphome` name, `esp32` board, `wifi` with fallback AP, encrypted `api`, `ota`, optional `web_server`, and `logger`. Secrets live in ESPHome's own `secrets.yaml`.

## ESPHome YAML Structure

Every ESPHome device config has the same basic structure:

```yaml
# Minimum viable config for ESP32
esphome:
  name: "bedroom-climate"          # Hostname (no spaces, lowercase)
  friendly_name: "Bedroom Climate" # Display name in HA

esp32:
  board: esp32dev                  # Board type (esp32dev covers most generic boards)
  framework:
    type: arduino                  # or 'esp-idf' for advanced use

# WiFi credentials
wifi:
  ssid: !secret wifi_ssid         # Reference secrets.yaml (ESPHome has its own secrets.yaml)
  password: !secret wifi_password
  ap:
    ssid: "Fallback Hotspot"      # Creates AP if WiFi fails (for recovery)
    password: !secret ap_password

captive_portal:                   # Web UI on fallback AP

# HA native API (encrypted connection to HA)
api:
  encryption:
    key: !secret api_encryption_key  # Generate once: esphome generate-key

# OTA updates
ota:
  - platform: esphome
    password: !secret ota_password

# Optional: web server for status/debugging
web_server:
  port: 80

logger:
  level: INFO                     # DEBUG for troubleshooting, INFO for production
```

## Related Concepts

- [[esphome-what.md|esphome what]]
- [[esphome-sensors-climate.md|esphome sensors climate]]
- [[esphome-flash-ota.md|esphome flash ota]]
