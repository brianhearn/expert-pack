---
title: "ESPHome Garage Door and LED Control"
type: concept
tags:
  - esphome-fundamentals
  - cover
  - ws2812
  - wled
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/esphome-sensors-control
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - esphome-sensors-climate.md
  - esphome-yaml.md
  - esphome-hardware-troubleshoot.md
content_hash: sha256:6e2839c0210e4453be90c6516ba0f7f250c0fe651d921f26a01fbd5096e654f3
---
# ESPHome Garage Door and LED Control

Two classic ESPHome actuators are a template garage-door cover (relay pulse plus reed sensor) and an `esp32_rmt_led_strip` for WS2812/SK6812. Complex LED effects can instead run WLED with its own HA integration.

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

## Related Concepts

- [[esphome-sensors-climate.md|esphome sensors climate]]
- [[esphome-yaml.md|esphome yaml]]
- [[esphome-hardware-troubleshoot.md|esphome hardware troubleshoot]]
