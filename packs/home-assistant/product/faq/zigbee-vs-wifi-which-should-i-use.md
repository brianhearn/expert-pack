---
title: Zigbee vs WiFi — Which Should I Use for Smart Home Devices?
type: faq
tags:
- faq
- integrations-guide
- protocol-selection
- protocols
pack: home-assistant-product
retrieval_strategy: standard
---
<!-- context: section=faq, topic=protocol-selection, related=protocols,integrations-guide -->

# Zigbee vs WiFi — Which Should I Use for Smart Home Devices?

> **Lead summary:** For most smart home devices (sensors, plugs, bulbs, switches), **use Zigbee**. Zigbee is local-only, low-power, meshes automatically, and has thousands of compatible devices starting at $7-15 each. WiFi devices are tempting because "no hub needed" — but most are cloud-dependent, strain your router at scale, and stop working when the manufacturer's server goes down. Reserve WiFi for cameras, video doorbells, and devices that don't exist in Zigbee.

## The Core Problem with WiFi Devices

WiFi smart devices are marketed as "no hub required." That sounds simpler — and short-term, it is. Long-term:

- **Most are cloud-dependent:** A TP-Link Kasa plug, Tuya sensor, or Wemo switch routes commands through the manufacturer's server. When that server has an outage (happens monthly) or shuts down permanently (Tuya, Wemo, Insteon have all done this), your devices stop working from HA.
- **They don't scale:** A home with 50 WiFi IoT devices adds 50 clients to your router and AP. Consumer routers often cap at 100-150 total devices. At 50 IoT devices plus phones, laptops, and TVs, performance degrades.
- **Higher power draw:** Battery-powered WiFi devices drain in days. No good WiFi battery sensors exist as a result.
- **Security surface:** Each WiFi device is directly on your network and often connecting outbound to servers in other countries.

## Why Zigbee Is Better for Most Devices

**Zigbee advantages:**
- Fully local — HA talks directly to the coordinator, no internet required
- Mesh network — mains-powered devices relay messages, coverage improves as you add devices
- Low power — battery sensors last 1-3 years on a coin cell
- Huge ecosystem — 3,500+ confirmed compatible devices at every price point
- Cheap — sensors from $7, plugs from $12, bulbs from $8
- Coordinator is a single $20-30 USB dongle

**Zigbee with HA works via:**
- **ZHA** (Zigbee Home Automation) — built into HA, easier setup
- **Zigbee2MQTT** — more devices supported, better tools, requires MQTT broker

## When WiFi Is the Right Choice

WiFi is appropriate for:
- **Cameras and video doorbells** — need high bandwidth that Zigbee can't provide
- **Smart appliances** — washers, refrigerators, EV chargers that only come in WiFi
- **Shelly devices** — well-regarded for local WiFi control (Shelly plugs, dimmers, energy monitors)
- **ESPHome DIY sensors** — ESP32-based custom sensors use WiFi but connect directly to HA via a local API

## The Practical Transition

If you're invested in WiFi devices already:
- Check if your device's HA integration is "Local Poll" or "Cloud Poll" (see integration docs)
- Shelly, TP-Link Kasa, and LIFX all have reasonable local API support
- Cheap Tuya devices can often be reflashed with Tasmota or ESPHome firmware for local control
- As WiFi devices age out, replace them with Zigbee equivalents

## Setup Requirements

**Zigbee setup:**
1. Buy a Zigbee USB coordinator (~$20-30): Sonoff Dongle Plus-P, SMLIGHT SLZB-07
2. Plug into HA host via USB 2.0 extension cable (avoids USB 3.0 interference)
3. Configure ZHA or Zigbee2MQTT in HA
4. Pair devices

That's it. One coordinator handles 100+ devices.

→ See [[protocols.md]] for the full protocol comparison
→ See [[integrations-guide.md]] for evaluating specific WiFi integrations
