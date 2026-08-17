---
title: "Solar and Battery Energy Sensors"
type: concept
tags:
  - energy-management
  - solar
  - battery
  - forecast-solar
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/energy-solar-battery
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - energy-grid.md
  - energy-dashboard.md
  - energy-device-monitoring.md
content_hash: sha256:8860f53050eee623d1181444d5cd83e56f4a98b8bd559b180d9e4f7e44cfbdd0
---
# Solar and Battery Energy Sensors

Solar production is a cumulative kWh sensor from the inverter (SolarEdge, Fronius, Enphase, or a Shelly on the inverter circuit). Forecast.Solar or Solcast can draw the production forecast. Batteries need separate charge and discharge kWh sensors — derive them with Riemann sum if you only have W and %.

## Solar Integration

### Production Sensor

Select your solar production sensor (cumulative kWh from your inverter):

**Common inverter integrations:**
- **SolarEdge:** Official integration, provides production energy sensor
- **Fronius:** Solid integration, well-supported
- **Enphase:** Via Envoy local API
- **Solis/Deye/Sofar:** Via Modbus or cloud API (varying quality)
- **Generic inverter with Shelly EM:** Measure the inverter output circuit directly

### Solar Forecast

The Energy Dashboard can display a production forecast for the current and next day. Two options:

**Forecast.Solar (free tier):**
```yaml
# configuration.yaml
sensor:
  - platform: forecast_solar
    latitude: 51.5074
    longitude: -0.1278
    declination: 30      # Panel tilt from horizontal (degrees)
    azimuth: 180         # Panel facing direction (0=N, 90=E, 180=S, 270=W)
    modules_power: 4800  # Total panel wattage (Wp)
```

Provides `sensor.energy_production_today` and `sensor.energy_production_tomorrow`.

**Solcast (more accurate, free tier up to 10 API calls/day):**
Requires account registration, API key, and the Solcast HA integration from HACS. More accurate than Forecast.Solar because it uses satellite weather data rather than just coordinates.

## Battery Storage

If you have a home battery (Powerwall, Sonnen, BYD, Huawei LUNA, etc.), add charge and discharge sensors in the Energy Dashboard.

Most battery integrations provide:
- `sensor.battery_charge_energy` (kWh put into battery)
- `sensor.battery_discharge_energy` (kWh taken from battery)

If your battery only provides instantaneous state of charge (%) and power (W), you need to derive energy sensors using the Riemann sum method.

**Tesla Powerwall via Powerwall 2 integration:**
The integration provides properly formatted energy sensors. No conversion needed.

**Victron/off-grid systems:**
Connect via Modbus TCP or the Victron MQTT integration. Sensors often need unit and state_class normalization.

## Related Concepts

- [[energy-grid.md|energy grid]]
- [[energy-dashboard.md|energy dashboard]]
- [[energy-device-monitoring.md|energy device monitoring]]
