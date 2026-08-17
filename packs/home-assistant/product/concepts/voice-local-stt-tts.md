---
title: "Local STT and TTS — Faster Whisper and Piper"
type: concept
tags:
  - voice-assistant
  - whisper
  - piper
  - stt
  - tts
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/voice-local-stt-tts
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - voice-wyoming.md
  - voice-assist-pipeline.md
  - voice-llm-agents.md
content_hash: sha256:1b251f7ee3a0d25b6154d1c3f017e1dfe44c22a427055c62d4823f9545927213
---
# Local STT and TTS — Faster Whisper and Piper

Fully local Assist uses Faster Whisper for speech-to-text and Piper for text-to-speech. An N100 mini-PC handles this well; a Pi 4 can manage with the tiny Whisper model and noticeable latency.

## Local STT: Faster Whisper

[Faster Whisper](https://github.com/SYSTRAN/faster-whisper) is a reimplementation of OpenAI's Whisper model that runs 4x faster with less memory using CTranslate2. It's the standard for local HA STT in 2026.

### Model Sizes and Performance

| Model | VRAM/RAM | Speed (CPU) | Speed (GPU) | Accuracy |
|-------|----------|-------------|-------------|----------|
| `tiny` | ~250MB | Fast (Pi 4 ok) | Very fast | Acceptable |
| `base` | ~500MB | OK on N100 | Very fast | Good |
| `small` | ~1GB | Slow on Pi 4 | Fast | Very good |
| `medium` | ~3GB | Too slow (CPU) | OK | Excellent |
| `large-v3` | ~6GB | Not practical | Good GPU only | Best |

**Practical guidance:**
- **Raspberry Pi 4 (4GB):** `tiny` model only. Expect 3-8 second transcription latency. Usable but not great UX.
- **Intel N100 mini-PC:** `small` model works well. 1-3 second latency. This is the sweet spot for local-only with no GPU.
- **GPU (any NVIDIA with 4GB+):** `medium` or `large-v3`. Sub-1 second latency. Excellent accuracy.
- **Intel Arc GPU or iGPU:** Experimental support, improves over `tiny` but less optimized than NVIDIA.

**Configure in Wyoming Faster Whisper add-on:**
```yaml
language: en
model: small-int8   # int8 quantized = faster, slightly less accurate
beam_size: 1        # Lower = faster, less accurate; higher = slower, better
initial_prompt: "Turn on, turn off, set brightness, open, close, lock, unlock."
```

The `initial_prompt` tip is underutilized: providing context words biases transcription toward smart home vocabulary, reducing misheard commands like "turn off the kitchen light" → "turn up the kitchen light."

## Local TTS: Piper

[Piper](https://github.com/rhasspy/piper) is the standard local TTS engine for HA. It produces high-quality, natural-sounding speech and runs in real-time on a Raspberry Pi 4. Developed by the rhasspy project (same team behind much of HA's voice work).

**Key advantages:**
- Runs fast even on CPU hardware
- Large library of voices across many languages
- Open source, actively maintained
- Per-language models (~50-100MB each)

**Voice selection:** Download from the [Piper voices repository](https://huggingface.co/rhasspy/piper-voices). English options include `en_US-amy-medium`, `en_US-lessac-high`, `en_GB-alan-medium` and many others. The `-high` quality models are larger but more natural.

**Configure in Wyoming Piper add-on:**
```yaml
voice: en_US-lessac-high   # High quality US English
```

For most users, the voice quality difference between `-medium` and `-high` is noticeable enough to prefer `-high` unless storage/RAM is constrained.

## Related Concepts

- [[voice-wyoming.md|voice wyoming]]
- [[voice-assist-pipeline.md|voice assist pipeline]]
- [[voice-llm-agents.md|voice llm agents]]
