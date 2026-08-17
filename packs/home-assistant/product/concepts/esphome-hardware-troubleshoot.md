---
title: "ESPHome Hardware Combos and Troubleshooting"
type: concept
tags:
  - esphome-fundamentals
  - troubleshooting
  - i2c
  - apollo
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/esphome-hardware-troubleshoot
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - esphome-sensors-climate.md
  - esphome-ha-integration.md
  - esphome-flash-ota.md
content_hash: sha256:48eeaf1cc20a6181973fe1173cc3a3572d9e0cabf44753d23bfc70687ff18257
---
# ESPHome Hardware Combos and Troubleshooting

Typical ESPHome builds cost $8–50 depending on the sensor. If a device will not join WiFi, use the fallback AP; watchdog reboots are usually wiring or power; I2C misses need `scan: true`. ESPHome is 2.4 GHz only.

## Common ESPHome Hardware Combos

| Use Case | Microcontroller | Sensor/Module | Total Cost |
|----------|----------------|---------------|-----------|
| Temperature + humidity | ESP32-C3 | BME280 or AHT20+BMP280 | ~$8-12 |
| CO2 monitor | ESP32-C3 | SCD40 or SCD41 | ~$25-35 |
| mmWave presence | ESP32-C3 | LD2410B or LD2450 | ~$12-20 |
| Presence + temp combo | ESP32-C3 | LD2410 + BME280 | ~$15-25 |
| Air quality (PM2.5) | ESP32 | PMS5003 + SCD41 | ~$35-50 |
| BLE proxy only | Any ESP32 | (no external sensor) | ~$5-8 |
| Plant moisture | ESP32-C3 | Capacitive soil sensor | ~$8-12 |
| Garage door | ESP32 + relay | Reed switch + 5V relay | ~$12-18 |
| LED controller (addressable) | ESP32 | WS2812B strip | $15-40 |
| Smart plug (power monitoring) | ESP8266 | PZEM-004T module | ~$15 |

**Buying tips:**
- Amazon: slightly higher prices, 2-day shipping, easier returns
- AliExpress: 50-70% cheaper, 2-6 week shipping — buy in bulk when using AliExpress
- Apollo Automation (apolloautomation.com): pre-built ESPHome sensors, good quality, US-based
- Athom (via AliExpress): pre-built ESPHome plugs and sensors with decent quality

## Troubleshooting ESPHome Devices

**Device won't connect to WiFi:**
- Enable the fallback AP (it appears in available WiFi networks), connect to it, access `192.168.4.1` to reconfigure WiFi
- Check for wrong SSID (ESPHome is 2.4 GHz only — won't connect to 5 GHz or mixed networks with same name)

**Device keeps rebooting (watchdog restart):**
- Check logs: `esphome logs my_device.yaml` — usually a sensor wiring issue or I2C address conflict
- Check power supply — ESP32 drawing too much current for USB power source

**Entity unavailable in HA:**
- Check the device is online via ESPHome dashboard (green dot = connected to API)
- Verify the HA integration is using the right IP or hostname
- mDNS resolution issues: try using IP address instead of hostname in the HA integration config

**I2C device not found:**
- Scan for I2C devices in ESPHome:
```yaml
i2c:
  scan: true    # Logs all found I2C addresses on startup
```

## Related Concepts

- [[esphome-sensors-climate.md|esphome sensors climate]]
- [[esphome-ha-integration.md|esphome ha integration]]
- [[esphome-flash-ota.md|esphome flash ota]]
