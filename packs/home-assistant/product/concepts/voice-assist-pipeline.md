---
title: "Home Assistant Assist Pipeline"
type: concept
tags:
  - voice-assistant
  - assist
  - pipeline
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/voice-assist-pipeline
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - voice-wyoming.md
  - voice-local-stt-tts.md
  - voice-satellites-hardware.md
content_hash: sha256:d069522587b8090848d99b7cc4eae7a6df4be09bde42a79f652d0d002068fdf2
---
# Home Assistant Assist Pipeline

Home Assistant Assist is HA's built-in voice assistant — fully local, no subscriptions, no cloud required. The pipeline is Wake Word → STT → Intent Recognition → TTS → spoken response. Each stage is a pluggable component, so you can mix Nabu Casa cloud STT/TTS with a local wake word, or run the whole stack on-network.

## What Assist Actually Is

Assist is a pipeline, not a monolithic service. Each stage is a pluggable component:

```
┌──────────────────────────────────────────────────────────────┐
│                     Assist Pipeline                           │
│                                                               │
│  Microphone → [Wake Word] → [STT] → [Intent/NLU] → [TTS]    │
│                                              ↓                │
│                                    Action executed in HA      │
└──────────────────────────────────────────────────────────────┘
```

Each bracket is independently configurable. You can use:
- Nabu Casa Cloud for STT + TTS while running local wake word
- Local Whisper for STT while using Nabu Casa TTS
- An LLM (ChatGPT, Claude, local Ollama) as the intent handler instead of the built-in engine
- Multiple pipelines with different configurations (one for English, one for another language)

**Pipelines are configured at:** Settings → Voice Assistants → Add Assistant

## Cloud vs Local Processing

### Nabu Casa Cloud (Easiest Path)

If you have a Nabu Casa subscription ($75/year), Assist cloud processing is included:
- **STT:** Cloud-based speech recognition (fast, accurate, no local compute needed)
- **TTS:** Cloud-based text-to-speech (good quality, many voices)
- **Setup:** Zero — enable in Settings → Voice Assistants, select "Home Assistant Cloud" for STT and TTS

**Tradeoffs:**
- Requires internet connectivity for every voice command
- Privacy: audio sent to Nabu Casa servers for processing (they state they don't retain it)
- Latency: adds 200-500ms round trip
- Subscription cost, though Nabu Casa also funds HA development

### Fully Local (The Goal)

Fully local means no audio ever leaves your home network. The stack:

| Component | Local Option | Notes |
|-----------|-------------|-------|
| Wake word | OpenWakeWord | CPU only, runs on Pi hardware |
| STT | Faster-Whisper | CPU feasible on N100, GPU preferred |
| Intent | HA built-in | Runs on HA host, no external service |
| TTS | Piper | Fast, high quality, CPU fine |

The local pipeline runs via the **Wyoming protocol** — HA's open standard for connecting external audio services.

## Related Concepts

- [[voice-wyoming.md|voice wyoming]]
- [[voice-local-stt-tts.md|voice local stt tts]]
- [[voice-satellites-hardware.md|voice satellites hardware]]

Sources: [HA voice control](https://www.home-assistant.io/voice_control/).
