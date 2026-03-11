# Home Assistant Platform Reference

## What Home Assistant Is

Home Assistant (HA) is an **open-source home automation platform** built by the Open Home Foundation and backed commercially by Nabu Casa. It runs locally on your hardware — a Raspberry Pi, mini-PC, NAS, or VM — and serves as the central hub for all your smart home devices, regardless of brand or protocol.

Unlike cloud-dependent smart home platforms (Google Home, Amazon Alexa, Apple HomeKit), Home Assistant stores your data locally, works without internet access, and integrates with over 3,000 devices and services through its integration library. The core philosophy is **local-first, open, and privacy-respecting**.

## Key Capabilities

- **Protocol-agnostic:** Integrates Zigbee, Z-Wave, Matter/Thread, Wi-Fi, Bluetooth, and cloud APIs under one roof
- **Automation engine:** Trigger → condition → action model with full Jinja2 templating
- **Dashboard system:** Drag-and-drop Lovelace UI, fully customizable cards and views
- **ESPHome:** First-class support for custom ESP32/ESP8266-based sensors and devices
- **Voice assistant:** Local Assist pipeline (Wake word → STT → NLP → TTS), optional cloud
- **Energy monitoring:** Real-time energy dashboard with solar, grid, and battery tracking
- **Remote access:** Secure remote connection via Nabu Casa Cloud or self-hosted (NGINX/Cloudflare)

## This Pack Covers

This is the **reference layer** — it answers questions about what Home Assistant *is* and how it *works* internally:

| Section | Contents |
|---------|----------|
| [concepts/](concepts/_index.md) | Architecture, protocols, automation engine, YAML, ESPHome, dashboards, integrations, presence detection, voice assistant, energy management, networking, backup |
| [troubleshooting/](troubleshooting/_index.md) | Diagnostic guide, common mistakes |
| [faq/](faq/common-questions.md) | Frequently asked questions |
| [glossary.md](glossary.md) | Terminology and definitions |

## What This Pack Does NOT Cover

The **how to build a smart home** journey — phased guidance, decision frameworks, and implementation patterns — lives in the companion **[process pack](../process/overview.md)**. Use both together for the full picture.

## Version Coverage

This pack targets **Home Assistant 2026.3+**. Core concepts are stable across recent versions, but specific UI interactions and YAML syntax may vary slightly on older releases.
