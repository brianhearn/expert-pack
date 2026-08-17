---
title: "ESPHome Climate and mmWave Sensors"
type: concept
tags:
  - esphome-fundamentals
  - bme280
  - scd41
  - ld2410
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/esphome-sensors-climate
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - esphome-sensors-control.md
  - esphome-yaml.md
  - presence-mmwave.md
content_hash: sha256:0e25a989060e7f776961ed5ac23d56fe932f5a2236f013b24839e018d314ebc1
---
# ESPHome Climate and mmWave Sensors

The common ESPHome sensor patterns are BME280/SHT31/AHT20 for temperature and humidity, SCD40/SCD41 for CO2, and LD2410/LD2450 mmWave for presence. A $20 SCD41 beats a $100 commercial CO2 monitor on HA integration.

## Sensor Components — Common Patterns

### Temperature + Humidity (BME280 / SHT31 / AHT20)

```yaml
# BME280 on I2C
i2c:
  sda: GPIO21
  scl: GPIO22

sensor:
  - platform: bme280_i2c
    temperature:
      name: "Temperature"
      oversampling: 16x
      filters:
        - offset: -0.5           # Calibration offset if needed
    pressure:
      name: "Pressure"
    humidity:
      name: "Humidity"
    address: 0x76               # or 0x77 depending on SD0 pin
    update_interval: 60s
```
### CO2 Sensor (SCD40/SCD41 — the gold standard for air quality)

```yaml
# SCD41 on I2C — most accurate consumer CO2 sensor
i2c:
  sda: GPIO21
  scl: GPIO22

sensor:
  - platform: scd4x
    co2:
      name: "CO2"
      id: co2_sensor
    temperature:
      name: "Temperature (SCD41)"
    humidity:
      name: "Humidity (SCD41)"
    update_interval: 60s
    automatic_self_calibration: true   # Calibrates to outdoor air (400ppm) periodically

# Optional: LED indicator for CO2 levels
# Green < 800ppm, Yellow 800-1200ppm, Red > 1200ppm
```

The SCD41 costs ~$20-30 for the breakout board. A commercial CO2 monitor with HA integration (like Aranet4) costs $100+.
### mmWave Presence Detection (LD2410)

```yaml
# LD2410 connected via UART
uart:
  tx_pin: GPIO17
  rx_pin: GPIO16
  baud_rate: 256000
  parity: NONE
  stop_bits: 1

ld2410:  # Auto-detects via UART

binary_sensor:
  - platform: ld2410
    has_target:
      name: "Presence"
    has_moving_target:
      name: "Moving Target"
    has_still_target:
      name: "Still Target"

sensor:
  - platform: ld2410
    moving_distance:
      name: "Moving Distance"
    still_distance:
      name: "Still Distance"
    moving_energy:
      name: "Moving Energy"
    still_energy:
      name: "Still Energy"
    detection_distance:
      name: "Detection Distance"

number:
  - platform: ld2410
    timeout:
      name: "Timeout (s)"      # How long to hold after last motion — tune this!
    max_move_distance_gate:
      name: "Max Move Distance"
    max_still_distance_gate:
      name: "Max Still Distance"
```

**LD2410 vs LD2450:** The LD2410B/C is single-zone (is there a target? yes/no + distance). The LD2450 (used in Apollo R PRO-1) supports tracking up to 3 targets with X/Y coordinates — enabling zone-based detection ("person is in zone A vs zone B").

## Related Concepts

- [[esphome-sensors-control.md|esphome sensors control]]
- [[esphome-yaml.md|esphome yaml]]
- [[presence-mmwave.md|presence mmwave]]
