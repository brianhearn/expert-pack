---
title: ESPHome Fundamentals — Custom Hardware at Minimal Cost
type: concept
tags:
- concepts
- esphome-fundamentals
- integrations-guide
- presence-detection
- protocols
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/esphome-fundamentals
verified_at: '2026-04-10'
verified_by: agent
---
<!-- context: section=concepts, topic=esphome-fundamentals, related=protocols,integrations-guide,presence-detection -->
---
sources:
  - type: documentation
    url: "https://esphome.io/index.html"
    date: "2026-03"
  - type: documentation
    url: "https://esphome.io/components/esp32.html"
    date: "2026-03"
  - type: documentation
    url: "https://esphome.io/components/bluetooth_proxy.html"
    date: "2026-03"
  - type: community
    url: "https://community.home-assistant.io/t/esphome-getting-started-guide/389710"
    date: "2025-10"
  - type: community
    url: "https://www.reddit.com/r/homeassistant/comments/1bxkz9p/esphome_megathread/"
    date: "2025-09"
---

# ESPHome Fundamentals — Custom Hardware at Minimal Cost

> **Lead summary:** ESPHome is the missing piece for any sensor that doesn't exist commercially or costs too much. You write a YAML config file that describes your hardware, flash it to a $5-15 ESP32 microcontroller, and HA discovers it automatically via its native API — fully local, zero cloud dependency. A CO2 sensor, mmWave presence detector, plant moisture monitor, or LED controller built with ESPHome costs $10-40 vs $50-150 commercial equivalent. This is not a hobbyist toy — ESPHome is production-ready, used in millions of HA deployments, and actively maintained by Nabu Casa (the HA company).

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

### Garage Door Controller

A classic ESPHome project — add smart control to any garage door opener:

```yaml
cover:
  - platform: template
    name: "Garage Door"
    device_class: garage
    lambda: |-
      if (id(door_sensor).state) {
        return cover::COVER_OPEN;
      } else {
        return cover::COVER_CLOSED;
      }
    open_action:
      - switch.turn_on: relay_garage
      - delay: 500ms
      - switch.turn_off: relay_garage
    close_action:
      - switch.turn_on: relay_garage
      - delay: 500ms
      - switch.turn_off: relay_garage

binary_sensor:
  - platform: gpio
    pin:
      number: GPIO34
      mode: INPUT_PULLUP
    name: "Door Open Sensor"
    id: door_sensor
    device_class: garage_door

switch:
  - platform: gpio
    pin: GPIO26
    name: "Garage Relay"
    id: relay_garage
    restore_mode: ALWAYS_OFF
```

### LED Strip Controller (WLED integration or native ESPHome)

For addressable LED strips (WS2812B, SK6812, etc.):

```yaml
light:
  - platform: esp32_rmt_led_strip
    rgb_order: GRB
    pin: GPIO16
    num_leds: 60
    rmt_channel: 0
    chipset: WS2812
    name: "Kitchen Counter Lights"
    effects:
      - pulse:
      - rainbow:
      - addressable_rainbow:
      - addressable_color_wipe:
```

Or use WLED firmware for complex effects — it has its own HA integration but runs on ESP32/ESP8266.

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
- Presence detection via phone BLE (see [[presence-detection.md|Presence Detection]])
- Govee/Xiaomi/SwitchBot Bluetooth sensors work throughout the house
- HA automatically uses whichever proxy is closest to a device

**Best placement:** One ESP32 BLE proxy per floor or large area. They don't need to do anything else (though combining with a climate sensor in the same device is common).

## Integration with Home Assistant

When an ESPHome device powers up and connects to the same network as HA, it announces itself via mDNS. HA automatically discovers it and shows a notification: "New ESPHome device found."

**Accept the integration → device and all entities appear automatically.**

Each sensor/switch/light defined in the YAML config becomes an HA entity:
- `sensor.bedroom_climate_temperature` (from `name: "Temperature"` in config named `bedroom-climate`)
- `binary_sensor.bedroom_climate_presence`
- `switch.bedroom_climate_garage_relay`

### Entity Naming Convention
ESPHome entity IDs follow: `domain.device_name_entity_name` where:
- Device name: the `name:` in `esphome:` block (spaces become underscores)
- Entity name: the `name:` in each component block

**Tip:** Use `id:` in components to reference them internally in the ESPHome YAML without affecting the HA entity name. Use `name:` for what appears in HA.

### Device Grouping in HA
All entities from one ESPHome device appear under one "Device" in HA (Settings → Devices). Assign the device to an Area for clean organization:
- ESPHome: `bedroom-climate` device in HA
- Assigned to Area: "Bedroom"
- All entities inherit the area context

### The `disabled_by_default: true` Pattern
Some sensors produce a lot of data you don't always need. Mark them as disabled by default in ESPHome:

```yaml
sensor:
  - platform: ld2410
    moving_energy:
      name: "Moving Energy"
      disabled_by_default: true   # Only enable in HA UI if you need it
```

This keeps the HA entity count manageable.

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

## Related

- [[presence-detection.md|Presence Detection]] — BLE proxy and mmWave for presence
- [[protocols.md|Smart Home Protocols]] — ESPHome's place in the protocol landscape
- [[integrations-guide.md|Integrations Guide]] — ESPHome integration in HA
