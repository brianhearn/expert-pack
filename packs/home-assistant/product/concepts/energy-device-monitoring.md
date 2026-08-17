---
title: "Individual Device Energy Monitoring"
type: concept
tags:
  - energy-management
  - shelly
  - ev-charger
  - smart-plug
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/energy-device-monitoring
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - energy-solar-battery.md
  - energy-dashboard.md
  - energy-automations.md
content_hash: sha256:873e153be3946486a507e2029ef88050ade642ee90bfca7bce3cbb2842bb7674
---
# Individual Device Energy Monitoring

The Energy Dashboard can track high-draw devices separately: EV charger, water heater, HVAC, washer, dryer, dishwasher. Use a clamp monitor (Shelly EM) on 240V dedicated circuits — do not put those loads on a smart plug.

## Individual Device Monitoring

The Energy Dashboard supports tracking specific high-draw devices separately within the total consumption figure:

**Recommended devices to monitor individually:**
- EV charger (often 7-11kW — a major energy consumer)
- Electric water heater / heat pump water heater
- HVAC / heat pump
- Washer and dryer
- Dishwasher

**Smart plug energy monitoring options:**

| Device | Protocol | Accuracy | Notes |
|--------|----------|----------|-------|
| Shelly Plug S / Shelly Plus Plug S | WiFi | ±1% | Best accuracy, local API |
| NOUS A1T | WiFi/Tasmota | ±2% | Pre-flashed Tasmota, budget option |
| Sonoff S31 (flashed) | WiFi/Tasmota | ±2% | Flash with Tasmota for local control |
| IKEA Inspelning | Zigbee | ±2-3% | Native Zigbee, simple setup |
| Nous A5T (Zigbee) | Zigbee | ±2-3% | Zigbee energy monitoring, good value |
| Emporia Vue (whole-home) | WiFi | ±1% | Per-circuit monitoring, US-focused |

**For high-draw dedicated circuits (HVAC, EV charger):** Use a clamp-style energy monitor (Shelly EM) that clips onto the wire in the electrical panel. Do not use a smart plug for 240V circuits — they're not rated for it.

## Related Concepts

- [[energy-solar-battery.md|energy solar battery]]
- [[energy-dashboard.md|energy dashboard]]
- [[energy-automations.md|energy automations]]
