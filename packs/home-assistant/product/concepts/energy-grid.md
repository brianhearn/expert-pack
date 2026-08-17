---
title: "Grid Energy and Cost Tracking"
type: concept
tags:
  - energy-management
  - grid
  - tariff
  - nordpool
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/energy-grid
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - energy-dashboard.md
  - energy-solar-battery.md
  - energy-riemann-utility.md
content_hash: sha256:be2046acf9a2446b7a80e050f6cc6ba1e4a41aaac9eaa901912bcf3bca87f321
---
# Grid Energy and Cost Tracking

Grid setup is selecting consumption and return-to-grid kWh sensors, then attaching a price — fixed, time-of-use via a template sensor, or a live pricing integration (Nordpool, Tibber, Octopus, ENTSO-E). Hardware options include P1/DSMR, Emporia Vue, Sense, and Shelly EM.

## Grid Setup

### Basic Grid Configuration

In Settings → Energy → Add Grid Consumption/Return, you select your consumption and return-to-grid sensors. These are cumulative kWh sensors from your utility meter integration or energy monitor.

**Options by region:**

**EU P1 reader:** In the Netherlands, Belgium, and other countries with DSMR-standard smart meters, a P1 cable reader connects directly to your meter and exposes consumption + return sensors. The `dsmr` integration handles this. The meter provides the sensors in exactly the right format — no conversion needed.

**US Emporia Vue:** The Emporia Vue 2 (whole-home + individual circuit monitoring) has a solid HA integration. It provides per-circuit power sensors; you'll need the Riemann sum conversion for energy.

**US Sense:** The Sense integration provides whole-home consumption. Device-level detection is AI-based and sometimes inaccurate, but the total consumption sensor is reliable.

**Shelly EM/3EM:** Excellent choice for European installations (single/three-phase). Provides per-phase power and energy sensors. The energy sensors are accurate and correctly configured for HA out of the box.

### Cost Tracking

Once your consumption sensor is configured, add pricing:

**Fixed rate:**
- Simple: enter your rate in $ or € per kWh
- Update it manually when your tariff changes

**Time-of-use rates:**
Use a template sensor that returns different prices based on time of day:

```yaml
template:
  - sensor:
      - name: "Current Electricity Price"
        unique_id: current_electricity_price
        unit_of_measurement: "USD/kWh"
        state_class: measurement
        state: >
          {% set hour = now().hour %}
          {% if hour >= 16 and hour < 21 %}
            0.32  {# Peak rate #}
          {% elif hour >= 21 or hour < 9 %}
            0.12  {# Off-peak rate #}
          {% else %}
            0.20  {# Mid-peak rate #}
          {% endif %}
```

Then select this sensor as the "price entity" in the Energy Dashboard grid configuration.

**Dynamic pricing via integration:**
- **Nordpool** integration: real-time hourly electricity prices for Nordic countries
- **Tibber** integration: real-time pricing + energy management (EU)
- **Octopus Energy** integration: Agile Octopus real-time UK pricing
- **ENTSO-E** integration: EU day-ahead market prices

With dynamic pricing, automations can automatically shift loads to cheap periods.

## Related Concepts

- [[energy-dashboard.md|energy dashboard]]
- [[energy-solar-battery.md|energy solar battery]]
- [[energy-riemann-utility.md|energy riemann utility]]
