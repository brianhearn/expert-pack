---
title: "Assist Entity Exposure and Naming"
type: concept
tags:
  - voice-assistant
  - aliases
  - areas
  - device-class
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/voice-assist-practices
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - voice-custom-sentences.md
  - voice-assist-pipeline.md
  - voice-llm-agents.md
content_hash: sha256:f0cd2362871901c0b491ba7c968ad4b909e1a240c2ec1d19621981f21e1cc424
---
# Assist Entity Exposure and Naming

Assist's built-in intent engine and LLM agents work from your exposed entity list. Expose only what you want to control by voice, name entities as Area + Descriptor + Domain, add speech aliases, assign every device to an area, and set device_class to the real function.

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

## Related Concepts

- [[voice-custom-sentences.md|voice custom sentences]]
- [[voice-assist-pipeline.md|voice assist pipeline]]
- [[voice-llm-agents.md|voice llm agents]]
