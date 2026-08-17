---
title: "Voice Satellites and Hardware"
type: concept
tags:
  - voice-assistant
  - satellites
  - esphome
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/voice-satellites-hardware
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - voice-wake-words.md
  - voice-assist-pipeline.md
  - esphome-what.md
content_hash: sha256:553ec249a7be3abec8f1b656e983b90d05f696330088ee7a764bffa003287101
---
# Voice Satellites and Hardware

A satellite is a remote microphone/speaker that connects back to the Assist pipeline on your HA server. You can speak to the Companion app, a dashboard, or dedicated hardware — from a $13 ESPHome DIY satellite to the ESP32-S3-BOX-3.

## Hardware Options for Voice Satellites

A "satellite" is a remote microphone/speaker device that connects back to the Assist pipeline running on your HA server. You don't need a satellite on every device — you can speak to your phone (Companion app), your dashboard, or dedicated hardware.

### Voice Preview Edition / ESPHome Satellite ($13 DIY)

The community-built ESPHome satellite is an ESP32-S3 with a microphone and speaker. It runs ESPHome firmware with the `voice_assistant` component and connects directly to your HA Assist pipeline via the native API.

**Hardware:**
- ESP32-S3-DevKitC-1 (~$5-8)
- INMP441 I2S microphone (~$2)
- MAX98357A I2S amplifier + small speaker (~$3-5)
- Total: ~$13-18 depending on parts and speaker quality

**ESPHome YAML skeleton:**
```yaml
esphome:
  name: voice-satellite-kitchen

esp32:
  board: esp32-s3-devkitc-1

i2s_audio:
  - id: i2s_in
    i2s_lrclk_pin: GPIO3
    i2s_bclk_pin: GPIO2
  - id: i2s_out
    i2s_lrclk_pin: GPIO6
    i2s_bclk_pin: GPIO5

microphone:
  - platform: i2s_audio
    i2s_audio_id: i2s_in
    i2s_din_pin: GPIO4
    adc_type: external
    pdm: false

speaker:
  - platform: i2s_audio
    i2s_audio_id: i2s_out
    i2s_dout_pin: GPIO7

voice_assistant:
  microphone: mic_id
  speaker: speaker_id
  use_wake_word: true
  noise_suppression_level: 2
  auto_gain: 31dBFS
  volume_multiplier: 2.0
  on_tts_end:
    - light.turn_on:
        id: led_ring
        effect: "Pulse"
```

The `voice_assistant` component handles the entire pipeline: wake word detection (runs locally on the ESP32 using MicroWakeWord), audio capture, streaming to HA, playing the response.
### ESP32-S3-BOX-3 (~$50)

The official HA-recommended satellite. Seeed Studio produces a pre-built device with a screen, good microphone array, and speaker. It runs ESPHome firmware and is supported by the ESPHome project. The screen can display current assistant state, entity status, and media info.

**Advantages over DIY:**
- Better microphone (dual-mic array with wake word LED indicator)
- Built-in speaker with reasonable quality
- Screen for visual feedback
- Ready to flash — no soldering
- Officially supported firmware maintained by ESPHome team
### Analog Phone via ESPHome

One of the more creative community projects: repurposing an old desk telephone as a voice satellite. Lift the handset, speak your command, hang up for playback stop. The retro aesthetic is either charming or horrifying depending on your taste.
### HA Companion App (Phones/Tablets)

The simplest satellite — your existing phone. Long-press the HA logo on the iOS/Android Companion app, or configure an Assist button on your dashboard. Good for testing, less good as a permanent room solution.

## Related Concepts

- [[voice-wake-words.md|voice wake words]]
- [[voice-assist-pipeline.md|voice assist pipeline]]
- [[esphome-what.md|esphome what]]

Sources: [ESPHome voice satellite thread](https://community.home-assistant.io/t/espHome-voice-assistant-satellite/591342).
