---
id: blender-3d/concepts/sculpting-brushes
title: "Sculpting — Viewport Shading and Core Brushes"
type: concept
tags:
  - sculpting
  - brushes
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/sculpting.md
related:
  - sculpting-masking-facesets.md
  - sculpting-dyntopo.md
content_hash: sha256:4fbbd00218f12ba9cd23f123bc7a45098c9e8aa71a64538ed5f8d0c13a100d56
---

# Sculpting — Viewport Shading and Core Brushes

Sculpt brushes deform mesh vertices under a falloff; MatCap shading and symmetry make form readable while you work. Draw, Clay, Crease, Grab, and texture-driven alphas cover mass, carving, and surface detail.

## Viewport Shading for Sculpting

Turn off overlays. Use MatCap shading:
- `Z` → Solid display
- In viewport shading dropdown → MatCap → Choose a high-contrast clay-like matcap

Good clay matcaps: `clay_brown`, `jade`, `metal_shiny_hair`. Removes material rendering overhead and shows surface detail clearly.

**Symmetry:** `X`, `Y`, `Z` symmetry toggles in the header. For character work, `X` symmetry handles bilateral symmetry. Radial symmetry for patterns (spokes, petals).

---

## Core Brushes

### Form and Mass Brushes

**Draw (`X`):** Default. Pushes geometry outward (or inward with `Ctrl`). The workhorse.

**Clay (`C`):** Accumulates flat layers of "clay" — stops at a plane perpendicular to the stroke direction. More predictable than Draw for building up volume evenly.

**Clay Strips:** Like Clay, but uses a square falloff — better for building sharp ridges or flat planes. Very popular for hard-surface-informed organic work.

**Inflate (`I`):** Moves vertices along their normals. `Ctrl` deflates.

**Smooth (`Shift`):** Hold `Shift` with any brush active. Relaxes vertices toward their average neighbors. Use constantly to clean up stroke artifacts.

### Carving and Detail Brushes

**Crease (`Shift+C`):** Pinches edges together — creates sharp creases, wrinkles, skin folds.

**Pinch (`P`):** Pulls vertices toward the stroke center — creates sharp ridges without removing geometry. Essential for ear helix, eyelid creases, hard crease lines in stylized work.

**Scrape:** Flattens a surface below a plane. Good for flat panels, polishing the forehead or cheeks.

**Grab (`G`):** Moves a cluster of geometry as a unit. Key for adjusting proportions without re-sculpting.

**Snake Hook (`K`):** Stretches and creates tubes of geometry from the surface. Used for horns, spikes, tentacles. Works best with Dyntopo enabled.

### Texture-Driven Brushes

Any brush can have a texture applied to its stroke — how skin pores, scales, and fabric are sculpted:

1. Open a tileable detail texture (grayscale, high contrast)
2. Brush Settings → Texture section: assign the texture
3. Set Mapping to `Area Plane` (tiles across the surface)
4. Adjust texture angle, scale, and strength

**Alpha textures:** A grayscale PNG (white = effect, black = none) defines the brush shape. Invaluable for damage detailing, logos, stamps.

---

