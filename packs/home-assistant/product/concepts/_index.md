---
title: "Concepts"
type: "index"
tags: [concepts]
pack: "home-assistant-product"
retrieval_strategy: navigation
id: home-assistant/product/concepts/_index
verified_at: "2026-08-17"
verified_by: agent
schema_version: "4.1"
---
# Concepts

Core knowledge for understanding and building with Home Assistant. Start with Core Architecture — everything else builds on it.

## Core architecture
- core-architecture.md — Integration → device → entity → state hierarchy
- core-state-machine.md — Event loop and `state_changed`
- core-services-install.md — Services/actions and HA OS vs Container vs Core vs Supervised

## Protocols
- protocols-comparison.md — Zigbee, Z-Wave, WiFi, Thread, Matter, Bluetooth, ESPHome at a glance
- protocols-decision.md — What to pick when starting, and when Matter/WiFi/ESPHome fit
- protocols-mesh.md — Routers vs end devices, coordinators, ZHA vs Zigbee2MQTT

## Automations
- automation-trigger-action.md — Triggers and the three-part model
- automation-conditions-actions.md — Conditions as gates, actions as the work
- automation-modes.md — single / restart / queued / parallel
- automation-templates-blueprints.md — Jinja2 in automations, blueprints, entity_id vs device_id

## Presence
- presence-phone-limits.md — Why phone-only tracking fails, and WAF
- presence-sensor-fusion.md — Multi-sensor strategy and the Companion-app layer
- presence-wifi-ble.md — WiFi router tracking and ESPHome BLE proxies
- presence-mmwave.md — mmWave radar and door-sensor edge detection
- presence-home-vs-room.md — House-level vs room-level presence
- presence-bayesian.md — Bayesian binary sensor
- presence-person-home.md — Unified person-home template with `delay_off`
- presence-pitfalls.md — Common pitfalls and community gotchas

## YAML
- yaml-vs-ui.md — When YAML vs UI, and `configuration.yaml` structure
- yaml-includes.md — `!include` and directory merge patterns
- yaml-packages.md — Feature-based packages
- yaml-secrets-env.md — `secrets.yaml` and `!env_var`
- yaml-templates.md — Reusable Jinja2 and template best practices
- yaml-template-extensions.md — HA-specific template functions
- yaml-validation.md — YAML gotchas and `ha core check`

## ESPHome
- esphome-what.md — What ESPHome is, ESP32 vs ESP8266
- esphome-flash-ota.md — First USB flash, then OTA
- esphome-yaml.md — Device YAML skeleton
- esphome-sensors-climate.md — BME280, SCD41, LD2410 patterns
- esphome-sensors-control.md — Garage door and LED strips
- esphome-ble-proxy.md — ESP32 as a Bluetooth antenna
- esphome-ha-integration.md — Native API discovery and entity naming
- esphome-hardware-troubleshoot.md — Hardware combos and device troubleshooting

## Dashboards
- dashboard-layouts.md — Sections, Masonry, Panel, Sidebar
- dashboard-organization.md — One dashboard per use case, mobile-first
- dashboard-cards.md — Tile, Entity, Gauge, History Graph, Conditional
- dashboard-mushroom.md — Mushroom card set
- dashboard-custom-cards.md — button-card, mini-graph, auto-entities
- dashboard-actions-themes.md — Tap/hold, themes, maintenance anti-patterns

## Integrations
- integrations-iot-class.md — Local push vs cloud poll
- integrations-quality-eval.md — Quality scale and pre-install checklist
- integrations-top-used.md — Network, climate, lighting, security integrations
- integrations-media-mesh.md — Media, voice, Zigbee/Z-Wave, weather, MQTT helpers
- integrations-hacs.md — HACS install and safety
- integrations-mqtt-cloud.md — MQTT bridge and cloud-to-local playbook
- integrations-troubleshooting.md — Reload, debug logging, monthly breaks
- integrations-reliability.md — Vendor API kills and HACS break cadence

## Voice
- voice-assist-pipeline.md — What Assist is, cloud vs local
- voice-wyoming.md — Wyoming streaming protocol
- voice-satellites-hardware.md — ESPHome satellites and BOX-3
- voice-wake-words.md — OpenWakeWord and MicroWakeWord
- voice-local-stt-tts.md — Faster Whisper and Piper
- voice-assist-practices.md — Expose, name, alias, areas, device_class
- voice-custom-sentences.md — Custom sentences and intent_script
- voice-llm-agents.md — LLM conversation agents
- voice-limitations-2026.md — What Assist still cannot do

## Energy
- energy-dashboard.md — What the dashboard shows and the kWh requirement
- energy-riemann-utility.md — Power→energy Riemann sum and utility_meter
- energy-grid.md — Grid sensors and cost / tariff tracking
- energy-solar-battery.md — Inverter production, forecast, battery charge/discharge
- energy-device-monitoring.md — EV, HVAC, and plug-level monitoring
- energy-gotchas.md — Resets, statistics delay, recorder bloat
- energy-automations.md — Solar excess, off-peak EV, budget alerts

## Network
- network-vlan.md — Why isolation matters and the VLAN layout
- network-mdns.md — mDNS/multicast across VLANs
- network-dhcp-dns.md — DHCP reservations and IoT DNS sinkholes
- network-wifi.md — 2.4 GHz IoT SSIDs
- network-zigbee-zwave.md — Off-IP meshes, USB extension, channels
- network-remote-access.md — Nabu Casa, VPN, reverse proxy; never 8123
- network-cameras-hardware.md — Camera VLAN, Frigate, router/switch/AP picks

## Backup and migration
- backup-builtin.md — Full vs partial built-in backups
- backup-automated.md — Off-device 3-2-1 strategies
- backup-testing.md — Restore tests that actually matter
- backup-sd-card.md — Why SD cards die and how to move to SSD
- backup-hardware-migration.md — Backup → flash → restore → move sticks
- backup-zigbee-coordinator.md — Same stick vs new coordinator
- backup-migration-paths.md — Pi SSD, N100, Proxmox, 2025–2026 hardware
- backup-disaster-recovery.md — Config extract, corrupt DB, dead storage
