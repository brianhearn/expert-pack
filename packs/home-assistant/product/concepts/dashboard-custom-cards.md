---
title: "button-card and Other HACS Cards"
type: concept
tags:
  - dashboard-design
  - button-card
  - mini-graph
  - auto-entities
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/dashboard-custom-cards
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - dashboard-mushroom.md
  - dashboard-cards.md
  - integrations-hacs.md
content_hash: sha256:f7efd70aeea879ef02058ad1fed8ae5e4a29ba6ae3cb6d21aeedf8888904c3cc
---
# button-card and Other HACS Cards

button-card is the most flexible custom card when you need pixel-level control. The other must-haves are mini-graph-card, auto-entities, layout-card, apexcharts-card, weather-chart-card, and lovelace-home-feed-card — all via HACS Frontend.

### button-card — Ultimate Flexibility

`button-card` by RomRider is the most flexible custom card in existence. Fully template-driven, custom styles, icon/color/text can all be dynamic. Used for power-user dashboards.

```yaml
type: custom:button-card
entity: light.kitchen_ceiling
name: Kitchen
icon: mdi:ceiling-light
color_type: icon
color: auto
tap_action:
  action: toggle
hold_action:
  action: more-info
state:
  - value: "on"
    icon: mdi:ceiling-light
    color: amber
  - value: "off"
    icon: mdi:ceiling-light-outline
    color: var(--disabled-text-color)
```

The learning curve is steeper than Mushroom — use Mushroom for most needs, `button-card` when you need pixel-perfect custom control.
### Other Must-Have Custom Cards

| Card | Purpose |
|------|---------|
| **mini-graph-card** | Beautiful sparkline/area chart for sensors, much nicer than built-in history graph |
| **auto-entities** | Dynamically generates card lists based on entity filters (all lights that are on, all low battery sensors) |
| **layout-card** | Advanced layouts: CSS grid, horizontal/vertical stacks with precise control |
| **apexcharts-card** | Publication-quality charts for energy, temperature, statistics |
| **weather-chart-card** | Detailed weather forecast visualization |
| **lovelace-home-feed-card** | Activity feed — recent events, notifications, upcoming calendar events |

Install all via HACS → Frontend tab.

## Related Concepts

- [[dashboard-mushroom.md|dashboard mushroom]]
- [[dashboard-cards.md|dashboard cards]]
- [[integrations-hacs.md|integrations hacs]]
