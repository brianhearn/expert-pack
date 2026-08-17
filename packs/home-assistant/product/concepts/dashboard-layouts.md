---
title: "Dashboard Layout Types"
type: concept
tags:
  - dashboard-design
  - sections
  - masonry
  - lovelace
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/dashboard-layouts
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - dashboard-organization.md
  - dashboard-cards.md
  - dashboard-actions-themes.md
content_hash: sha256:f92ae54245e251cf0b559ac11b1afc27bce8d23260e9815899a0788c55677f45
---
# Dashboard Layout Types

HA has four dashboard layouts. Sections (default since 2024.4) is the one to use for new work — a responsive grid with named rows. Masonry is the legacy Pinterest layout; Panel is one full-page card; Sidebar is uncommon.

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

## Related Concepts

- [[dashboard-organization.md|dashboard organization]]
- [[dashboard-cards.md|dashboard cards]]
- [[dashboard-actions-themes.md|dashboard actions themes]]

Sources: [Dashboards](https://www.home-assistant.io/dashboards/), [Sections](https://www.home-assistant.io/dashboards/sections/).
