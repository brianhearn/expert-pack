---
title: "Built-In Dashboard Cards"
type: concept
tags:
  - dashboard-design
  - tile
  - gauge
  - conditional
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/dashboard-cards
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - dashboard-mushroom.md
  - dashboard-layouts.md
  - dashboard-actions-themes.md
content_hash: sha256:238f5a4903ff0f298fab478c32d9318174f8edf44629e456c9710d3e00750e9e
---
# Built-In Dashboard Cards

The built-in cards that matter are Tile (modern default), Entity, Gauge, History Graph, Conditional, Entities list, and the limited built-in Button. Tile plus Conditional covers most actionable dashboards before you reach for HACS.

## Card Types That Matter

### Tile Card (Modern Default)
The Tile card is the successor to Entity card for most use cases. Shows entity state, icon, and name. Supports tap/hold actions. Multiple display modes.

```yaml
type: tile
entity: light.kitchen_ceiling
name: Kitchen Lights
color: amber
tap_action:
  action: toggle
hold_action:
  action: more-info
```

Tile cards work well for lights, switches, locks, covers (blinds/garage), and simple sensors.
### Entity Card
The classic. Shows an entity with its state. Less visual than Tile but useful for showing raw values (sensors, text-based states). Supports tap/hold actions.

```yaml
type: entity
entity: sensor.outdoor_temperature
name: Outdoor Temp
icon: mdi:thermometer
```
### Gauge Card
For sensors with numeric ranges. Shows a visual meter with configurable severity levels.

```yaml
type: gauge
entity: sensor.living_room_co2
name: CO2
min: 400
max: 2000
needle: true
severity:
  green: 400
  yellow: 800
  red: 1200
```
### History Graph Card
Shows a time-series chart of one or more sensors. Essential for temperature, humidity, energy monitoring.

```yaml
type: history-graph
entities:
  - entity: sensor.bedroom_temperature
    name: Bedroom
  - entity: sensor.living_room_temperature
    name: Living Room
hours_to_show: 24
```
### Conditional Card
Shows or hides a card based on entity state. This is how you build adaptive dashboards.

```yaml
type: conditional
conditions:
  - condition: state
    entity: binary_sensor.security_armed
    state: "on"
card:
  type: alarm-panel
  entity: alarm_control_panel.home
```

Use conditional cards for:
- Security controls that only show when armed
- Guest mode indicators
- Alert banners when something needs attention
- Media controls that only show when something is playing
### Entities Card (List)
Shows multiple entities in a list view. Good for status panels.

```yaml
type: entities
title: "Security"
entities:
  - entity: binary_sensor.front_door
    name: Front Door
  - entity: binary_sensor.back_door
    name: Back Door
  - entity: binary_sensor.garage_door
    name: Garage Door
```
### Button Card (Built-in)
Simple tap button to call a service. The built-in version is limited — see `button-card` custom component for real power.

## Related Concepts

- [[dashboard-mushroom.md|dashboard mushroom]]
- [[dashboard-layouts.md|dashboard layouts]]
- [[dashboard-actions-themes.md|dashboard actions themes]]
