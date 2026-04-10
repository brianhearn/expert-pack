---
title: Summary — Product Concepts Overview
type: summary
tags:
- concepts-overview
- summaries
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/summaries/concepts-overview
verified_at: '2026-04-10'
verified_by: agent
---
# Summary — Product Concepts Overview

This summary covers all concept files in the Home Assistant product pack. For detailed information, follow the links to source files.

---

## What Home Assistant Is

Home Assistant (HA) is an open-source local-first home automation platform. The core mental model is a **state machine**: integrations connect to hardware/services and create entities, entities have states, state changes fire events, automations react to events, and actions change states. Everything in HA flows through this loop.

The entity hierarchy: **Integration → Device → Entity → State → Attributes**. Entity IDs (`light.kitchen_ceiling`, `sensor.outdoor_temp`) are the stable references used across the entire system.

→ Source: [[core-architecture.md]]

---

## Protocols — What to Use for Devices

**Zigbee is the best default choice** for sensors, plugs, switches, and bulbs — local-only, low power, mesh networking, massive device selection, mature ecosystem. Use a USB coordinator dongle (~$20-30) and either ZHA (built-in, simpler) or Zigbee2MQTT (more devices, better tools).

**Z-Wave** (sub-GHz, less interference, pricier) is worth it for locks and thick-walled homes. **ESPHome** on ESP32 microcontrollers is ideal for DIY custom sensors ($10-35 total cost vs $50-150 commercial). **WiFi** devices are acceptable for cameras and high-bandwidth needs but cloud-dependent and scale-limited. **Matter/Thread** is promising but still maturing in 2026.

Most good setups use 2-3 protocols simultaneously.

→ Source: [[protocols.md]]

---

## Automations — The Three-Part Model

Every automation is: **triggers** (OR logic — any one fires the automation) → **conditions** (AND logic — all must pass) → **actions** (sequential steps). 

Critical nuances: use `mode: restart` for motion-activated lights (not the default `single`). Always cast entity states to numbers with `| float` before numeric comparisons. Use `states('entity_id')` not `states.domain.entity.state`. Test templates in Developer Tools → Template before embedding them.

Automation traces (Settings → Automations → Traces) are the most powerful debugging tool — they show exactly what happened at each step.

→ Source: [[automation-fundamentals.md]]

---

## YAML Configuration

The UI handles 90% of HA configuration. Use YAML for: template sensors, complex automation logic, packages (feature-based config bundles), and secrets management. 

Common pitfalls: `'on'`/`'off'` must be quoted (unquoted = boolean), tabs break YAML (use spaces only), always validate with `ha core check` before restarting. The packages pattern (`homeassistant: packages: !include_dir_named packages/`) is the best way to organize large configs into logical feature files.

→ Source: [[yaml-configuration.md]]

---

## Integrations — Quality and Cloud vs Local

Every integration has an **IoT class** that predicts reliability: Local Push (best — instant, no internet needed) → Local Poll → Cloud Push → Cloud Poll (worst — depends on manufacturer's server). Prefer Local Push integrations; avoid Cloud Poll for critical devices.

HACS adds community integrations and frontend cards. Frontend cards (Mushroom, mini-graph-card) are low risk. Custom HACS integrations run with full HA privileges — evaluate security before installing.

→ Source: [[integrations-guide.md]]

---

## Dashboard Design

Use **Sections layout** (default since 2024.4) for all new dashboards — it's responsive and mobile-friendly. Design for phones first (375px wide). The "Useful in 3 Seconds" rule: any household member should understand status and act within 3 seconds.

**Mushroom Cards** (HACS) are the most widely-used custom cards — clean, consistent, mobile-first. Build purpose-specific dashboards (Overview, Room, Security, Energy) rather than one giant view. Conditional cards hide non-relevant controls, reducing clutter.

→ Source: [[dashboard-design.md]]

---

## ESPHome — Custom Sensors

ESPHome generates firmware for ESP32 microcontrollers from YAML config. A complete DIY sensor costs $10-35; a commercial equivalent costs $50-150. Common projects: temperature/humidity (BME280, SHT31), CO2 (SCD41 — gold standard), mmWave presence (LD2410 — detects breathing/stillness), BLE proxy (extends Bluetooth range throughout home), LED strip controller, garage door opener.

ESP32 auto-discovers in HA via mDNS. BLE proxy (`bluetooth_proxy: active: true`) is one of the most underappreciated features — it makes all Bluetooth devices work anywhere in the home.

→ Source: [[esphome-fundamentals.md]]

---

## Network Architecture

IoT devices should be on a separate VLAN (no internet access); HA stays on the trusted network. Key problems to solve: mDNS cross-VLAN discovery (use mDNS reflector or static IPs), DHCP reservations for every IoT device (stable IPs), DNS sinkhole for telemetry blocking.

**Never port-forward port 8123 to the internet.** Use Nabu Casa (easiest, outbound-only tunnel), Tailscale (zero-config VPN), or a reverse proxy with SSL. USB 3.0 RF interference on the Zigbee coordinator is fixed with a USB 2.0 extension cable.

→ Source: [[network-architecture.md]]

---

## Backup and Migration

HA backup/restore is remarkably capable — full restore to new hardware in under 30 minutes including Zigbee mesh (if same coordinator stick is moved). The biggest reliability risk is SD card failure (1-3 year lifespan under HA write load). Use an SSD.

Automate off-device backups (Google Drive Backup add-on or Samba to NAS). Test backups by actually restoring them before an emergency. Intel N100 mini-PCs are the community sweet spot for new dedicated HA hardware in 2025-2026.

→ Source: [[backup-migration.md]]

---

## Presence Detection

Multi-sensor fusion beats single-tracker approaches. Combine: phone GPS (HA Companion app) + WiFi router tracking + BLE proximity (ESPresense or ESP32 BLE proxies) + mmWave radar + door contact sensors. The Bayesian binary sensor fuses these signals into a probability-based presence verdict.

Android battery optimization kills the HA Companion app — set it to "Unrestricted." MAC randomization breaks WiFi tracking unless the Companion app reports a consistent identifier. Solve home-level presence before adding room-level.

→ Source: [[presence-detection.md]]

---

## Voice Assistant (Assist)

Assist is HA's local voice pipeline: Wake Word → STT → Intent → TTS. Each stage is independently configurable (mix local/cloud). Fully local stack: OpenWakeWord + Faster Whisper (STT, `small` model on N100) + Piper (TTS). 

Key rules: expose only entities you want voice-controlled, name them `[Area] [Descriptor] [Domain]`, assign all devices to Areas, add aliases for speech variations. LLM agents (OpenAI, Claude, local Ollama) replace the built-in intent engine for natural language commands. In 2026, Assist is powerful but not yet Alexa-level polish.

→ Source: [[voice-assistant.md]]

---

## Energy Management

The Energy Dashboard needs **cumulative kWh sensors** with `state_class: total_increasing` — not instantaneous power (watts). Convert power sensors to energy sensors using the Riemann sum `integration` platform. The `utility_meter` helper creates daily/monthly/yearly cycle tracking with optional tariff support.

Set up energy sensors as early as possible — HA cannot retroactively capture data before sensors were configured. High-draw 240V circuits (HVAC, EV charger) require clamp-style monitors (Shelly EM), not smart plugs.

→ Source: [[energy-management.md]]
