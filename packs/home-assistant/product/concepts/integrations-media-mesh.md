---
title: "Top Integrations — Media, Voice, Mesh, Weather"
type: concept
tags:
  - integrations-guide
  - zha
  - mqtt
  - nabu-casa
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/integrations-media-mesh
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - integrations-top-used.md
  - integrations-mqtt-cloud.md
  - protocols-comparison.md
content_hash: sha256:b42358726cdbdbdda902aa317f4e054a7df24a2cb21d5b5b8ced58b7b7a41154
---
# Top Integrations — Media, Voice, Mesh, Weather

The other high-usage integrations are media players (Sonos, Plex, Apple TV), Assist plus Google/Alexa bridges, ZHA or Zigbee2MQTT, Z-Wave JS, weather providers, MQTT, Node-RED, and Nabu Casa Cloud.

### Media

**Plex** (local/cloud) — works well, discovers media servers on LAN.

**Sonos** (local push) — best-in-class speaker integration. Entity state updates are real-time.

**Spotify** (cloud) — connect and control Spotify playback. Cloud-dependent but Spotify's API has been stable.

**Apple TV** (local push) — control Apple TV, track what's playing, use presence for "TV watching" state.

**Chromecast/Google TV** (local push) — solid integration, works well for media player state.

**Samsung SmartThings TV** (local) — newer Samsung TVs (2018+) support local control via websocket.
### Voice & Assistants

**Assist** (built-in, local) — HA's own voice assistant. Fully local with Whisper (speech-to-text) + Piper (text-to-speech) add-ons. No cloud required.

**Google Assistant / Alexa** — cloud bridges that make HA entities visible to voice assistants. Require Nabu Casa subscription or self-hosted HTTPS endpoint.
### Zigbee & Z-Wave

**ZHA (Zigbee Home Automation)** — built-in, simpler setup, ~2000 device support
**Zigbee2MQTT** — add-on, more complex, ~3500+ device support, more customization

**Z-Wave JS** — the only maintained Z-Wave integration for HA. Works with Z-Wave JS UI add-on for network management.
### Weather & Environment

**Open-Meteo** (cloud poll) — free, no API key, EU-based (GDPR compliant), excellent forecast accuracy.

**OpenWeatherMap** (cloud poll) — free tier with API key, widely used.

**Meteorologisk Institutt (Met.no)** — Norwegian weather service, no API key, good global coverage.

**AccuWeather** — has a free tier (100 calls/day), more detailed forecasts.
### Utility & Automation Helpers

**MQTT** (local push) — the universal protocol bridge. If a device supports MQTT, it can be integrated. Powers Zigbee2MQTT, Tasmota, custom DIY sensors.

**Node-RED** (via HACS integration) — alternative automation engine running as a HA add-on. Visual flow-based programming. Useful for complex automations where HA's automation editor is limiting.

**Home Assistant Cloud (Nabu Casa)** — $6.50/month. Provides: remote access without port forwarding, Google/Alexa bridge, webhook relay. Not required but simplest remote access solution.

## Related Concepts

- [[integrations-top-used.md|integrations top used]]
- [[integrations-mqtt-cloud.md|integrations mqtt cloud]]
- [[protocols-comparison.md|protocols comparison]]
