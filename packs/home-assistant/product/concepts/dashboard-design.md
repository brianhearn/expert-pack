---
title: Dashboard Design — Practical Patterns for Useful UIs
type: concept
tags:
- concepts
- core-architecture
- dashboard-design
- integrations-guide
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/dashboard-design
verified_at: '2026-04-10'
verified_by: agent
---
<!-- context: section=concepts, topic=dashboard-design, related=core-architecture,integrations-guide -->
---
sources:
  - type: documentation
    url: "https://www.home-assistant.io/dashboards/"
    date: "2026-03"
  - type: documentation
    url: "https://www.home-assistant.io/dashboards/sections/"
    date: "2026-03"
  - type: community
    url: "https://community.home-assistant.io/t/mushroom-cards-build-a-beautiful-dashboard/388590"
    date: "2025-11"
  - type: community
    url: "https://www.reddit.com/r/homeassistant/comments/1bq2xnd/dashboard_design_guide_2025/"
    date: "2025-07"
---

# Dashboard Design — Practical Patterns for Useful UIs

> **Lead summary:** A well-designed HA dashboard is the difference between a smart home you actually use and one you manage via terminal. The key insight most people miss: dashboards should be **actionable**, not informational. Show what you need to control right now, not every sensor in the house. Use sections layout (HA 2024.4+) as the default — it's responsive and well-supported. Spend your custom card budget on Mushroom cards (clean, consistent, mobile-friendly) rather than building complex layouts. Your phone is your primary dashboard — design for 375px wide screens.

## Dashboard Types (Layouts)

HA supports four dashboard layout types. Choosing the right one matters:

### Sections Layout (Default since 2024.4) — Recommended
The new standard. Sections layout uses a responsive grid that adapts to screen size:
- Desktop: multi-column grid
- Tablet: 2 columns
- Mobile: 1-2 columns depending on card width

Cards are arranged in named sections (like rows), each with its own heading. Within sections, cards can span 1, 2, 3, or full-width columns. Drag-and-drop reordering works well.

**Use this for:** All new dashboards. It's the direction HA is heading.

### Masonry Layout (Legacy default)
Cards arranged in columns like Pinterest. Column count adjusts to screen width. Cards float to the shortest column automatically.

**The problem with Masonry:** Cards shift around between screen sizes in unexpected ways. Hard to maintain consistent visual grouping. Still works fine but feels dated.

**Use this for:** Migrating existing Masonry dashboards — don't break what works.

### Panel Layout
One card fills the entire page. Useful for:
- Full-screen floor plan (custom Floorplan card)
- Full-screen camera view
- Full-screen map/map card

### Sidebar Layout
Cards in two columns — narrow sidebar + main content area. Less common.

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

## Dashboard Organization Strategy

### One Dashboard Per Use Case

Don't build one giant dashboard. Build purpose-specific dashboards:

| Dashboard | Audience | Contents |
|-----------|----------|---------|
| **Overview** | Everyone | Current status chips, active alerts, most-used controls, weather |
| **Living Room** | In-room | TV/media controls, lighting, climate, that room's devices |
| **Bedroom** | In-room | Sleep scene, alarm, climate, do-not-disturb status |
| **Security** | Admin | All door/window sensors, cameras, alarm control |
| **Energy** | Admin | Power monitoring, solar, battery, per-device usage |
| **Admin/Debug** | Power user | System status, entity counts, recorder stats, log viewer |

Navigation between dashboards via the sidebar or via `navigate` tap actions.

### Mobile-First Design Principles

**The vast majority of HA daily use is on phones.** Design for phones first.

- Test every dashboard on your phone before considering it done
- Sections layout: set card column span to 1 for most cards (full-width on mobile)
- Tile/Mushroom cards scale better on mobile than entity card lists
- Avoid tables and history graphs that require horizontal scrolling
- Conditional cards reduce clutter — don't show things that aren't relevant right now
- Use clear labels — your partner can't guess what `sensor.0x00158d` means
- Large tap targets — buttons should be easy to tap while holding a coffee mug

### The "Useful in 3 Seconds" Rule

Every dashboard should let any household member understand what's happening and take action in 3 seconds. This means:
- Status at a glance (chips bar: armed/away/temperature/active alerts)
- Most-used controls immediately visible (lights, thermostat)
- No hunting through sub-menus for daily actions

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

## Related

- [[core-architecture.md|Core Architecture]] — Entities, areas, and organization
- [[integrations-guide.md|Integrations Guide]] — What's available to display
- [[yaml-configuration.md|YAML Configuration]] — Dashboard YAML for advanced customization
