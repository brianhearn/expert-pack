---
title: "Dashboard Actions, Themes, and Anti-Patterns"
type: concept
tags:
  - dashboard-design
  - tap-action
  - themes
  - conditional
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/dashboard-actions-themes
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - dashboard-layouts.md
  - dashboard-organization.md
  - dashboard-cards.md
content_hash: sha256:1872356d93834bd1f1a6c0ca05d0da4b90e13883ad99773b8aa7bfb1dda8304a
---
# Dashboard Actions, Themes, and Anti-Patterns

Cards support tap, hold, and double-tap actions (toggle, more-info, navigate, call-service). Conditional cards hide security or media controls until they matter. Themes come from HACS; the maintenance anti-pattern is dumping every entity onto one dashboard.

## Conditional Visibility Patterns

### Guest Mode — Show Different UI to Guests
```yaml
# In a conditional card:
conditions:
  - condition: state
    entity: input_boolean.guest_mode
    state: "off"
card:
  type: alarm-panel   # Hide security panel from guests
```

### Alert Banner
```yaml
type: conditional
conditions:
  - condition: numeric_state
    entity: sensor.living_room_co2
    above: 1000
card:
  type: markdown
  content: >
    ⚠️ **High CO2 Alert** — Living room CO2 is
    {{ states('sensor.living_room_co2') }} ppm.
    Open a window.
```

### Media-Only Controls
```yaml
conditions:
  - condition: state
    entity: media_player.tv
    state_not: "off"
card:
  type: custom:mushroom-media-player-card
  entity: media_player.tv
```

## Tap Actions, Hold Actions, Double-Tap Actions

Every card supports three action types:

```yaml
tap_action:        # Quick tap
  action: toggle   # or: call-service, navigate, more-info, url, none

hold_action:       # Long press
  action: more-info  # Opens full entity detail panel

double_tap_action: # Double tap (power users)
  action: navigate
  navigation_path: /lights
```

Common patterns:
- **Tap: toggle** — turn light on/off
- **Hold: more-info** — see history, attributes, full control panel
- **Hold: navigate** — go to room-specific dashboard
- **Tap: call-service** — run a script or scene

## Theme Customization

HA ships with light and dark themes. The visual design can be improved with community themes.

**Install themes via HACS:** HACS → Frontend → search theme names.

Popular themes:
- **Google Home** — Material Design, clean
- **Mushroom** — Designed for Mushroom card users (pairs naturally)
- **iOS Dark Mode** — iOS-inspired dark theme
- **Metrology** — Windows 11 Fluent design inspiration

Apply theme: Profile → Theme (top right) or set globally in configuration.yaml:
```yaml
frontend:
  themes: !include_dir_merge_named themes/
```

**Token-level customization** (fine-grained colors): Each HA theme is a set of CSS custom properties. You can override individual tokens in your own theme file:
```yaml
# themes/my_theme.yaml
my_theme:
  # Primary colors
  primary-color: "#2196F3"
  accent-color: "#FF9800"
  # Background
  primary-background-color: "#1a1a1a"
```

## Dashboard Maintenance Anti-Patterns

**Don't add every entity to the dashboard.** 200 entities on one dashboard is useless. Be ruthless — only show what someone needs to see or control today.

**Don't rely on dashboard for automation control.** If a critical automation breaks when someone deletes a dashboard card, that's a design flaw. Dashboards are UI. Automations should run independently.

**Don't skip mobile testing.** Most cards look great on 1440p desktop and terrible on 375px mobile. Always check.

**Do use Sections layout for all new dashboards.** The old Masonry layout is maintained for compatibility, not for new work.

## Related Concepts

- [[dashboard-layouts.md|dashboard layouts]]
- [[dashboard-organization.md|dashboard organization]]
- [[dashboard-cards.md|dashboard cards]]
