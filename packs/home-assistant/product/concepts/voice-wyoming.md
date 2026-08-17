---
title: "Wyoming Voice Protocol"
type: concept
tags:
  - voice-assistant
  - wyoming
  - local-voice
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/voice-wyoming
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - voice-assist-pipeline.md
  - voice-local-stt-tts.md
  - voice-wake-words.md
content_hash: sha256:8b8ae48dc5cb4d23857babbb37139c9712d076b8586aae7cf128a1b81db47e6b
---
# Wyoming Voice Protocol

Wyoming is HA's purpose-built protocol for connecting voice processing services (STT, TTS, wake word) to Home Assistant over the local network. It is designed for streaming audio, so STT can start before the utterance is finished.

## The Wyoming Protocol

Wyoming is HA's purpose-built protocol for connecting voice processing services to HA. Each service (STT, TTS, wake word) runs as a separate Wyoming-compatible server, and HA connects to it over the local network.

**Why Wyoming instead of HTTP?** Wyoming is designed for streaming audio — it supports real-time audio streaming for STT rather than requiring a complete audio file before processing starts. This reduces latency significantly.

**Wyoming add-ons available in HA OS:**

| Add-on | Service | Resource Use |
|--------|---------|-------------|
| Wyoming Faster Whisper | STT | Medium-High CPU or GPU |
| Wyoming Piper | TTS | Low CPU |
| Wyoming OpenWakeWord | Wake word detection | Low CPU |
| Wyoming Satellite | Turn any device into a satellite | Runs on remote hardware |

**Setup flow for local voice:**
1. Install Wyoming Faster Whisper add-on → configure model size
2. Install Wyoming Piper add-on → select voice
3. Install Wyoming OpenWakeWord add-on
4. In Settings → Voice Assistants → Create pipeline → assign each component
5. Done — the pipeline is now fully local

## Related Concepts

- [[voice-assist-pipeline.md|voice assist pipeline]]
- [[voice-local-stt-tts.md|voice local stt tts]]
- [[voice-wake-words.md|voice wake words]]

Sources: [Wyoming integration](https://www.home-assistant.io/integrations/wyoming/).
