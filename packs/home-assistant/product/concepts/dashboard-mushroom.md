---
title: "Mushroom Dashboard Cards"
type: concept
tags:
  - dashboard-design
  - mushroom
  - hacs
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/dashboard-mushroom
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - dashboard-custom-cards.md
  - dashboard-cards.md
  - integrations-hacs.md
content_hash: sha256:7b3d6ce06afdac077585b2f1b6909dc9a673f69e45373d3425525b14f7b7e087
---
# Mushroom Dashboard Cards

Mushroom cards are the most-used HACS frontend set — Material-style, mobile-first, and visually consistent. The chips card is the usual status bar; install via HACS → Frontend → Mushroom.

## Custom Cards via HACS — The Real Dashboard Power

The built-in cards cover 60% of needs. The remaining 40% — especially visual polish, complex displays, and flexible layouts — requires custom cards installed via HACS.

### Mushroom Cards — The Most Important Custom Set

Mushroom cards are the most widely-used custom card set in HA, with over 2 million active installs. They provide a clean, consistent Material Design-inspired visual language.

**Why Mushroom cards:**
- Visually cohesive — all cards look like they belong together
- Mobile-first design
- Highly customizable via chip-style indicators
- Active development with frequent updates
- Comprehensive card coverage

**Install:** HACS → Frontend → Search "Mushroom" → Install → Restart HA

**Key Mushroom card types:**

| Card | Use For |
|------|---------|
| `mushroom-title-card` | Section headers with optional subtitle |
| `mushroom-entity-card` | Single entity, clean display |
| `mushroom-light-card` | Light control with brightness/color |
| `mushroom-climate-card` | Thermostat control |
| `mushroom-media-player-card` | Now playing + transport controls |
| `mushroom-alarm-control-panel-card` | Alarm arming/disarming |
| `mushroom-cover-card` | Blinds, garage, covers |
| `mushroom-number-card` | Numeric input sliders |
| `mushroom-person-card` | Person location/presence |
| `mushroom-chips-card` | Row of small indicator chips (status bar) |
| `mushroom-template-card` | Fully template-driven custom card |

The `mushroom-chips-card` pattern is particularly powerful for status bars:
```yaml
type: custom:mushroom-chips-card
chips:
  - type: state
    entity: alarm_control_panel.home
    icon_color: red
    tap_action:
      action: navigate
      navigation_path: /security
  - type: entity
    entity: sensor.indoor_temperature
  - type: conditional
    conditions:
      - condition: state
        entity: binary_sensor.washer_running
        state: "on"
    chip:
      type: entity
      entity: binary_sensor.washer_running
      name: Laundry
```

## Related Concepts

- [[dashboard-custom-cards.md|dashboard custom cards]]
- [[dashboard-cards.md|dashboard cards]]
- [[integrations-hacs.md|integrations hacs]]

Sources: [Mushroom cards thread](https://community.home-assistant.io/t/mushroom-cards-build-a-beautiful-dashboard/388590).
