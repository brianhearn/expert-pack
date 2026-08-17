---
title: "Assist Limitations in 2026"
type: concept
tags:
  - voice-assistant
  - limitations
  - stt
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/voice-limitations-2026
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - voice-llm-agents.md
  - voice-assist-pipeline.md
  - voice-local-stt-tts.md
content_hash: sha256:5f514dd9639d31e91399b77371bb9b314c22563dc6722263e09727cea3cc8f4f
---
# Assist Limitations in 2026

Assist is impressive for an open-source local system, but it is not Alexa-level polish out of the box. In 2026 it still has no multi-turn memory, uneven non-English coverage, accent-sensitive STT, and 2–5 second local latency on modest hardware.

## Current Limitations (2026)

Assist is impressive for an open-source local system, but know what you're getting into:

**Non-English language support:** Coverage varies dramatically by language. English, German, French, and Dutch have good coverage. Many other languages have partial or community-maintained sentence packs. Check the [HA intents repository](https://github.com/home-assistant/intents) for your language's coverage.

**No multi-turn conversation:** Each command is stateless. "Turn on the kitchen light. Make it brighter. Now warmer." requires three separate commands — Assist doesn't remember the kitchen light was mentioned in step one.

**STT accuracy varies by accent:** Whisper models are trained primarily on North American English. British, Australian, Indian, and other accents show higher error rates, especially with the `tiny` and `base` models. The `large-v3` model handles accents much better.

**Wake word false activation:** In homes with TVs, podcasts, or similar audio, wake words will occasionally trigger on similar-sounding words. False activation rate varies from daily to rarely based on your household.

**Response latency on local hardware:** Even with optimized models, a fully local pipeline on modest hardware takes 2-5 seconds from wake word to response. Cloud-based systems typically respond in <1 second. This is an ergonomics consideration.

**Limited device feedback in responses:** Built-in Assist doesn't always give useful status responses. "Is the front door locked?" may not return a useful answer without custom sentence configuration.

## Related Concepts

- [[voice-llm-agents.md|voice llm agents]]
- [[voice-assist-pipeline.md|voice assist pipeline]]
- [[voice-local-stt-tts.md|voice local stt tts]]

Sources: [Year of the Voice megathread](https://community.home-assistant.io/t/year-of-the-voice-megathread/531913).
