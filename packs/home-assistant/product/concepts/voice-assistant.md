---
title: Voice Assistants with Home Assistant Assist
type: concept
tags:
- automation-fundamentals
- concepts
- esphome-fundamentals
- integrations-guide
- voice-assistant
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/voice-assistant
verified_at: "2026-04-21"
verified_by: agent
schema_version: "4.1"
concept_scope: single
---
<!-- context: section=concepts, topic=voice-assistant, related=esphome-fundamentals,integrations-guide,automation-fundamentals -->
---
sources:
  - type: documentation
    url: "https://www.home-assistant.io/voice_control/"
    date: "2026-03"
  - type: documentation
    url: "https://www.home-assistant.io/integrations/wyoming/"
    date: "2026-03"
  - type: community
    url: "https://community.home-assistant.io/t/year-of-the-voice-megathread/531913"
    date: "2025-12"
  - type: community
    url: "https://community.home-assistant.io/t/espHome-voice-assistant-satellite/591342"
    date: "2025-09"
---

# Voice Assistants with Home Assistant Assist

> **Lead summary:** Home Assistant Assist is HA's built-in voice assistant — fully local, no subscriptions, no cloud required. The pipeline is: Wake Word → STT (speech-to-text) → Intent Recognition → TTS (text-to-speech) → spoken response. Running it entirely locally is achievable on modest hardware (an N100 mini-PC handles it well; a Pi 4 can manage with tradeoffs). The 2023-2024 "Year of the Voice" initiative transformed Assist from a novelty into a practical system. In 2026 it remains a work in progress — powerful if you invest in setup, frustrating if you expect Alexa-level polish out of the box.

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

## Best Practices for Assist

These are the practices that separate a frustrating voice setup from one that actually works.

### 1. Expose Minimum Entities

Assist's built-in intent engine (and LLM agents) work from your entity list. Exposing 500 entities means:
- The intent engine has to search through all of them for matches
- LLM agents have larger context = higher cost + slower responses
- Ambiguous names cause confusing responses ("which living room light do you mean?")

**Rule:** Only expose entities you actually want to control by voice. The Assist configuration in HA lets you set which entities are exposed:

Settings → Voice Assistants → [your assistant] → Exposed Entities

Or in entity settings: set the "Voice Assistant" toggle per entity.

### 2. Name Entities Logically

Voice commands use entity names. The formula:
**[Area] + [Descriptor] + [Domain]**

Examples:
- `Kitchen ceiling light` (not `light_1` or `ikea tradfri bulb`)
- `Living room floor lamp`
- `Bedroom main light`
- `Front door lock`
- `Master bath humidity sensor`

Bad names are the #1 cause of failed voice commands. "Turn on the kitchen light" will match `Kitchen ceiling light` and `Kitchen ceiling light` — but not `tradfri_bulb_7` or `light.ikea_e27_white_spectrum`.

### 3. Use Aliases for Speech Variations

In each entity's settings, you can add **aliases** — alternative names Assist will recognize:

- Entity: `Living room television` → Aliases: `TV`, `telly`, `the TV`
- Entity: `Kitchen ceiling light` → Aliases: `kitchen light`, `kitchen lights`
- Entity: `Guest bedroom` → Aliases: `spare room`, `the spare`

Aliases are especially important for rooms where people naturally say different things ("spare room" vs "guest bedroom").

### 4. Assign ALL Devices to Areas

Voice commands frequently use area-based matching: "turn off the bedroom lights" works by finding all entities in the `bedroom` area with a light domain. If devices aren't assigned to areas, voice commands targeting areas will silently miss them.

**Checklist:** Settings → Areas & Zones → each area → verify all expected devices appear

Devices not assigned to any area also won't work with area-targeted commands. This is the second most common reason voice commands partially fail.

### 5. Match device_class to Real Function

Home Assistant's intent engine uses `device_class` to understand what an entity is. If a Zigbee smart plug controlling an irrigation valve has `device_class: outlet` (the default), Assist doesn't know it's a valve. Set it correctly:

```yaml
# In customize.yaml or entity settings:
switch.irrigation_valve:
  device_class: valve
  friendly_name: "Garden irrigation valve"

binary_sensor.window_sensor:
  device_class: window
  friendly_name: "Living room window"
```

Correct device_class also improves dashboard display (window sensors show as open/closed windows, not generic binary sensors) and enables more specific voice commands.

## Custom Sentences

Assist's built-in sentence coverage is limited to common smart home commands. You can extend it with custom sentences defined in YAML files.

**Location:** `config/custom_sentences/en/` (create if it doesn't exist)

**Example — custom commands:**
```yaml
# config/custom_sentences/en/custom.yaml
language: "en"
intents:
  GoodNight:
    data:
      - sentences:
          - "good night"
          - "I'm going to bed"
          - "goodnight"
  
  MovieMode:
    data:
      - sentences:
          - "movie time"
          - "start movie mode"
          - "we're watching a movie"
```

Then in `configuration.yaml` (or `intents.yaml`):
```yaml
intent_script:
  GoodNight:
    speech:
      text: "Good night! Lights off and alarm set."
    action:
      - action: script.good_night_routine
  
  MovieMode:
    speech:
      text: "Enjoy the movie!"
    action:
      - action: scene.turn_on
        target:
          entity_id: scene.movie_mode
```

Custom sentences support slots (variables), lists, and wildcards. You can build surprisingly capable custom commands this way.

## LLM Conversation Agents

For natural language that goes beyond predefined sentences, you can replace HA's built-in intent engine with an LLM. In Settings → Voice Assistants → your pipeline → "Conversation Agent": select an LLM-based agent.

**Available options:**
- **OpenAI Conversation** (official integration): GPT-4o, GPT-4o-mini. Costs money per query but excellent accuracy.
- **Google Generative AI Conversation**: Gemini models. Good quality, competitively priced.
- **Anthropic Conversation**: Claude models. Available via official integration.
- **Local LLM via Ollama**: Free, private, but requires powerful hardware (7B+ parameter models need 8GB+ RAM).

**What LLM agents enable:**
- Natural phrasing: "make it darker in here" → adjusts brightness
- Multi-device commands: "turn off all the lights except the hallway"
- Context-aware queries: "is anyone home?"
- Ambiguity resolution: asks follow-up questions

**What they don't (yet) enable:**
- Multi-turn conversation (each command is still stateless in 2026)
- Reasoning about the future ("remind me when the laundry is done" requires separate automation)
- Learning your preferences over time

**Cost management with LLM agents:** Expose only the entities you actually want to control by voice (see best practices above). Each query sends your full exposed entity list to the LLM. 50 entities vs 500 entities = dramatically different API costs.

**Example LLM conversation integration config:**
```yaml
# configuration.yaml
openai_conversation:
  api_key: !secret openai_api_key
  chat_model: gpt-4o-mini   # Cheaper, fast, good for home control
  max_tokens: 150
  temperature: 0.2          # Low temperature = more consistent, predictable responses
  prompt: >
    You are a home assistant controlling a smart home. Be concise.
    When you don't understand a request, ask for clarification.
    Never invent devices that aren't in the entity list.
```

## Current Limitations (2026)

Assist is impressive for an open-source local system, but know what you're getting into:

**Non-English language support:** Coverage varies dramatically by language. English, German, French, and Dutch have good coverage. Many other languages have partial or community-maintained sentence packs. Check the [HA intents repository](https://github.com/home-assistant/intents) for your language's coverage.

**No multi-turn conversation:** Each command is stateless. "Turn on the kitchen light. Make it brighter. Now warmer." requires three separate commands — Assist doesn't remember the kitchen light was mentioned in step one.

**STT accuracy varies by accent:** Whisper models are trained primarily on North American English. British, Australian, Indian, and other accents show higher error rates, especially with the `tiny` and `base` models. The `large-v3` model handles accents much better.

**Wake word false activation:** In homes with TVs, podcasts, or similar audio, wake words will occasionally trigger on similar-sounding words. False activation rate varies from daily to rarely based on your household.

**Response latency on local hardware:** Even with optimized models, a fully local pipeline on modest hardware takes 2-5 seconds from wake word to response. Cloud-based systems typically respond in <1 second. This is an ergonomics consideration.

**Limited device feedback in responses:** Built-in Assist doesn't always give useful status responses. "Is the front door locked?" may not return a useful answer without custom sentence configuration.

## Related

- [[esphome-fundamentals.md|ESPHome Fundamentals]] — Building ESP32 voice satellites
- [[integrations-guide.md|Integration Guide]] — Connecting OpenAI, Anthropic, and other LLM providers
- [[automation-fundamentals.md|Automation Fundamentals]] — Building automations triggered by voice intents
