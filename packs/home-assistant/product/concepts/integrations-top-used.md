---
title: "Top Integrations — Network, Climate, Lighting, Security"
type: concept
tags:
  - integrations-guide
  - unifi
  - hue
  - frigate
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/integrations-top-used
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - integrations-media-mesh.md
  - integrations-iot-class.md
  - integrations-hacs.md
content_hash: sha256:df0eaecce38ee963e81055754324eb458a3850094ea274b4f381136b8df3fc3b
---
# Top Integrations — Network, Climate, Lighting, Security

Most HA installs use a short list of integrations, not the 3,000+ catalog. By analytics.home-assistant.io usage, the high-value ones on the infrastructure and home-ops side are UniFi, energy monitors, Hue/LIFX/Zigbee lighting, and Frigate or UniFi Protect for cameras.

## Top Integrations by Real Usage

Based on analytics.home-assistant.io reporting (integrations with the most active installs):

### Network & Infrastructure

**UniFi Network** (local poll)
The gold standard for WiFi-based device tracking. If you have a UniFi router, this integration provides device presence tracking via DHCP leases + active client tracking. More reliable than phone-based detection. No cloud dependency.

**AdGuard Home** (local poll)
DNS-level ad blocking with HA controls. Toggle filtering, monitor request counts, block specific devices from internet access.

**Pi-hole** — similar to AdGuard, DNS-level blocking
### Climate & Energy

**HACS: Generic Thermostat** is built-in — create a smart thermostat from any temperature sensor + switch.

**Nest** (cloud poll) — Google's smart thermostat. Works but cloud-dependent. If offline = manual thermostat.

**Ecobee** (cloud poll) — popular alternative to Nest. Same cloud caveat.

**Tesla** (cloud poll) — vehicle integration. Check Tesla's history of breaking third-party API access before relying heavily on this.

**Local energy monitoring options:** Shelly EM (local push), Emporia Vue (local API available), PZEM via ESPHome.
### Lighting

**Philips Hue** — operates in two modes:
- *Local API (v2)*: connects to Hue Bridge on LAN — fast, local push, recommended
- *Cloud (older API)*: deprecated, avoid

**LIFX** — cloud or local. The local integration (`lifx` using UDP broadcast) is excellent. Supports all color features locally.

**Zigbee (ZHA / Zigbee2MQTT)** — the ideal: remove the manufacturer's app entirely and control all Zigbee lights via HA.
### Security & Cameras

**Frigate** (local, via MQTT or custom integration)
The most powerful self-hosted NVR with object detection. Runs locally on HA host or separate server. Detects people, cars, animals, packages. Integrates with HA for notifications and automations triggered by detected objects.
→ Install: `custom:frigate-hacs` from HACS, runs as a HA add-on or separate Docker container

**Ring** (cloud push) — doorbell/cameras. Works but cloud-only. Ring has a history of API changes.

**Unifi Protect** (local push) — best local camera system. If you have Unifi hardware, this is the local alternative to Ring/Nest cam.

**Reolink** (local) — budget IP cameras with good local HA support. Notable exception in the budget camera space.

## Related Concepts

- [[integrations-media-mesh.md|integrations media mesh]]
- [[integrations-iot-class.md|integrations iot class]]
- [[integrations-hacs.md|integrations hacs]]

Sources: [HA integration analytics](https://analytics.home-assistant.io/integrations).
