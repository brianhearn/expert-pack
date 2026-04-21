---
title: Home Assistant Platform Reference
type: overview
tags: []
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/overview
verified_at: "2026-04-21"
verified_by: agent
schema_version: "4.1"
concept_scope: single
---
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
| concepts/ | Architecture, protocols, automation engine, YAML, ESPHome, dashboards, integrations, presence detection, voice assistant, energy management, networking, backup |
| troubleshooting/ | Diagnostic guide, common mistakes |
| [[common-questions.md|faq/]] | Frequently asked questions |
| [[glossary.md]] | Terminology and definitions |

## What This Pack Does NOT Cover

The **how to build a smart home** journey — phased guidance, decision frameworks, and implementation patterns — lives in the companion **[[overview.md|process pack]]**. Use both together for the full picture.

## Version Coverage

This pack targets **Home Assistant 2026.3+**. Core concepts are stable across recent versions, but specific UI interactions and YAML syntax may vary slightly on older releases.
