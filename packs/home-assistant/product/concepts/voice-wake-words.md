---
title: "Voice Wake Words"
type: concept
tags:
  - voice-assistant
  - wake-word
  - openwakeword
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/voice-wake-words
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - voice-satellites-hardware.md
  - voice-wyoming.md
  - voice-assist-pipeline.md
content_hash: sha256:c39839d3b90fdfb96b183b45406daae9dc6bab54aea2fbc5010434e042eb5936
---
# Voice Wake Words

Wake words are the always-listening local detector that activates the full STT pipeline — the "Hey Siri" / "Alexa" equivalent. OpenWakeWord runs on the HA host; MicroWakeWord runs on the ESP32-S3 satellite itself.

## Wake Words

Wake words are the "Hey Siri" / "Alexa" equivalent — the always-listening local detector that activates the full STT pipeline.

### OpenWakeWord

The primary local wake word engine for HA. Runs on CPU (even ESP32 with MicroWakeWord), lightweight, open source.

**Built-in wake words:** "Hey Jarvis", "Hey Mycroft", "Alexa" (yes, you can use it locally), "OK Nabu", "Hey Nabu"

**Performance:**
- False activation rate: low but not zero (~1-2 false activations per day in a quiet home)
- Missed activation rate: ~5-10% with default sensitivity
- Sensitivity is tunable: higher sensitivity = fewer misses but more false positives

**Custom wake word training:** OpenWakeWord supports training custom wake words with ~30-100 sample recordings. The HA community has a [wake word collection project](https://github.com/fwartner/home-assistant-wakewords-collection) with pre-trained models.

### MicroWakeWord (On-Device)

ESPHome's MicroWakeWord runs directly on the ESP32-S3, so wake word detection happens on the satellite itself. This means:
- Lower latency (no round trip to HA for wake detection)
- Audio only leaves the device after wake word is heard
- Supported words: "OK Nabu", "Hey Jarvis", "Alexa"

For satellite devices, MicroWakeWord is strongly preferred over cloud-side wake detection.

## Related Concepts

- [[voice-satellites-hardware.md|voice satellites hardware]]
- [[voice-wyoming.md|voice wyoming]]
- [[voice-assist-pipeline.md|voice assist pipeline]]
