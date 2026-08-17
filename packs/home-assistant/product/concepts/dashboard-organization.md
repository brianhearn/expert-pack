---
title: "Dashboard Organization Strategy"
type: concept
tags:
  - dashboard-design
  - mobile-first
  - views
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/dashboard-organization
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - dashboard-layouts.md
  - dashboard-cards.md
  - dashboard-actions-themes.md
content_hash: sha256:ed65a575540a7ae717de20cb89a685034bfc79ba4344c6625071aaa324b9967c
---
# Dashboard Organization Strategy

Build purpose-specific dashboards (Overview, rooms, Security, Energy, Admin), not one giant page. Design for 375px phones first and apply the three-second rule: status and daily controls visible without hunting.

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

## Related Concepts

- [[dashboard-layouts.md|dashboard layouts]]
- [[dashboard-cards.md|dashboard cards]]
- [[dashboard-actions-themes.md|dashboard actions themes]]
