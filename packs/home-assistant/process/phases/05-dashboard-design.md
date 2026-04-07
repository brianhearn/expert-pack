---
title: 'Phase 5: Dashboard Design'
type: phase
tags:
- 05-dashboard-design
- phases
pack: home-assistant-process
retrieval_strategy: atomic
---
# Phase 5: Dashboard Design

## Goal

Build Lovelace dashboards that make your smart home *usable at a glance* — for you, for your household members who don't want to learn HA, and for phones where small screens matter. Good dashboards reduce friction; bad ones get ignored.

## Prerequisites

- Phase 4 complete (automations running)
- At least 20+ devices and sensors across multiple rooms
- HACS installed (for custom cards)
- Companion app on your phone

---

## Dashboard Philosophy

The best smart home dashboards follow three rules:

1. **Control the common things without drilling down.** Lights, locks, and thermostat should be reachable in 1-2 taps.
2. **Surface what's abnormal, hide the normal.** If everything is fine, the dashboard should be calm. Show alerts, open doors, and unusual states prominently.
3. **Optimize for mobile.** Most people check the dashboard from their phone. Design for a 390px-wide screen first.

---

## Step 1: Understand Lovelace Architecture

HA's dashboard system is called **Lovelace**. Key concepts:

- **Views** — tabs across the top of a dashboard (Home, Security, Climate, etc.)
- **Cards** — individual widgets within a view (entity card, light card, history graph, etc.)
- **Sections** (HA 2024.6+) — a new layout mode with responsive grid columns (replaces manual row placement)
- **YAML vs UI editing** — dashboards can be edited visually or in YAML; YAML mode gives full control

**Sections layout (recommended for new dashboards):**

The Sections layout introduced in HA 2024.6 automatically handles responsive columns — 3 columns on desktop, 2 on tablet, 1 on mobile. Use this by default; it eliminates most mobile layout headaches.

---

## Step 2: Install Essential Cards via HACS

Before designing, install these community cards that dramatically improve the experience:

| Card | Purpose | HACS Install |
|------|---------|-------------|
| **Mushroom Cards** | Beautiful, compact entity/light/climate cards | `mushroom` |
| **Mini Graph Card** | Compact sparkline graphs for sensors | `mini-graph-card` |
| **Lovelace Swipe Card** | Swipeable card groups for mobile | `lovelace-swipe-card` |
| **Button Card** | Fully customizable button/entity card | `button-card` |
| **Auto Entities** | Dynamic card lists based on state filters | `auto-entities` |
| **Decluttering Card** | Templates for repeated card patterns | `decluttering-card` |

**Installation:** HACS → Frontend → Search for card name → Download → Reload browser

---

## Step 3: Design Your Views

A typical household needs 4-6 views:

### View 1: Home (Default)

The main view. Shows the most-used controls and high-level status.

```yaml
# What to put here:
- House mode selector (input_select.house_mode)
- Quick access to all lights (room by room)
- Door/window status (any open?)
- Temperature overview (outdoor + 2-3 indoor)
- Active alerts (if any)
- Media player controls (if actively playing)
```

**Keep this view scannable.** If it takes more than 3 seconds to see what's on/off, it's too cluttered.

### View 2: Rooms (or one view per large room)

Detailed control for each room: all lights with brightness, current sensor readings, devices.

**Mushroom card pattern for a room:**
```yaml
- type: custom:mushroom-light-card
  entity: light.living_room_main
  show_brightness_control: true
  show_color_temp_control: true
  use_light_color: true
  collapsible_controls: false
```

### View 3: Security

All door/window contact sensors, motion sensors, cameras (if any), lock controls, alarm panel.

**Auto-entities for open doors:**
```yaml
- type: custom:auto-entities
  card:
    type: entities
    title: "Open Doors & Windows"
  filter:
    include:
      - domain: binary_sensor
        attributes:
          device_class: door
          state: "on"
      - domain: binary_sensor
        attributes:
          device_class: window
          state: "on"
  sort:
    method: name
```

### View 4: Climate

Thermostat controls, temperature history graphs, humidity, CO2 if monitored.

### View 5: Energy (After Phase 6)

Power consumption overview, solar production (if applicable), energy history.

### View 6: Admin

Automations on/off toggles, system health, device battery levels (low battery alerts), HA server status.

---

## Step 4: Mobile Optimization

Test every view on your phone. Common mobile problems and fixes:

| Problem | Fix |
|---------|-----|
| Cards too narrow/tall | Switch to Sections layout mode |
| Too many taps to reach common controls | Move frequent items to the first view |
| Text too small | Use Mushroom cards (larger touch targets) |
| Horizontal scroll feels slow | Remove swipe-heavy card layouts |
| Dashboard not loading (slow) | Reduce cards on default view, use lazy-loading views |

**Phone-specific tips:**
- Enable **Keep Screen On** in the companion app for wall-mounted tablet dashboards
- Use **Fully Kiosk Browser** (Android) for dedicated wall tablets — it handles wake-on-motion and keeps the screen on
- Create a **separate dashboard** for wall-mounted tablets vs. phone use

---

## Step 5: Badges and Notifications Banner

**Badges** appear below the navigation and show persistent status:

```yaml
# In dashboard YAML — show count of low battery devices
- type: state-label
  entity: sensor.low_battery_count
```

Create a `sensor.low_battery_count` template sensor:
```yaml
template:
  - sensor:
      - name: "Low Battery Count"
        unit_of_measurement: "devices"
        state: >
          {{ states.sensor | selectattr('attributes.device_class', 'eq', 'battery')
            | selectattr('state', 'lt', '20') | list | count }}
```

---

## Step 6: User-Specific Dashboards

Give household members who don't want to manage HA a **simplified dashboard**:

1. Create a new dashboard: Settings → Dashboards → Add Dashboard
2. Name it for the user (e.g., "Family View")
3. Add only the cards they'll actually use (lights, music, temperature, TV)
4. In their user profile, set this as their default dashboard

Users without admin access can still control everything — they just don't see the complexity.

---

## Checklist

- [ ] Mushroom Cards and other essential HACS cards installed
- [ ] Sections layout used for new dashboards
- [ ] Home view is scannable in <3 seconds
- [ ] Security view shows all door/window sensors at a glance
- [ ] Dashboard tested on phone — all controls reachable in 2 taps
- [ ] Simplified family dashboard created (if others in household)
- [ ] Low battery sensor/badge set up
- [ ] Auto-entities cards used for dynamic lists (not hardcoded lists)

## What's Next

→ [[06-advanced-features.md|Phase 6: Advanced Features]] — Voice assistant, energy monitoring, and presence detection
