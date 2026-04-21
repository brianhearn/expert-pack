---
id: blender-3d/concepts/sculpting-brushes-masking
title: "Sculpting — Brushes, Face Sets, and Masking"
type: concept
tags:
  - sculpting
  - brushes
  - masking
  - face-sets
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-04-21"
verified_by: agent
supersedes:
  - concepts/sculpting.md
related:
  - sculpting-paradigms.md
---

# Sculpting — Brushes, Face Sets, and Masking

---

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

## Face Sets

Face Sets are colored regions that act as isolation masks. Persistent per-face (vs vertex-based masks).

**Operations:**
- `Ctrl+W`: paint a new face set under the cursor
- `W → Extract Face Set`: Creates a new object from the selected region
- `Alt+H` on a face set: hides everything except that set

**Face set automasking:** Toggle in header — brushes only affect the face set under the cursor.

**Workflow:** Segment a character into logical face sets (head, torso, left arm, right arm, etc.) at the start of the session. Toggle visibility freely to work in isolation.

---

## Masking

Masks prevent brush strokes from affecting masked areas. Per-vertex (gradient capable), different from Face Sets (per-face, binary).

- `M`: toggle mask view
- `Ctrl+click` with any brush: paint a mask
- `Alt+M`: invert mask
- `W → Mask → Mask from Cavity`: auto-generates mask in recessed areas — useful for adding dirt/detail to only crevices
- `B`, `L`: box/lasso mask painting

### Automask

Per-brush masking that automatically restricts strokes:

| Automask Type | Effect |
|---------------|--------|
| Topology | Only affects connected geometry |
| Face Sets | Only affects the face set under the cursor |
| Cavity | Only affects protruding areas |
| Normal Limit | Only affects faces within an angle threshold |
| View Normal | Only affects faces pointing toward the camera |

"Topology + Normal Limit" is a popular combination for detailing without stroke bleed-through.

---

## Mesh Filters

Applied via `Ctrl+T` — brush-like effects across the entire mesh without a stroke:

| Filter | Effect |
|--------|--------|
| Smooth | Global smooth |
| Surface Smooth | Projects smoothing onto the surface plane |
| Inflate | Uniform inflate/deflate |
| Relax | Relaxes topology toward even distribution |
| Sharpen | Enhances existing high-frequency details |
| Random | Adds noise (sculpt-level jitter) |

**Surface Smooth** is particularly useful after remeshing — smooths without significantly altering surface position.

---

## Performance Tuning

**Multires display optimization:**
- Keep `Preview` level 2–3 lower than your Sculpt level
- Disable face overlays during heavy sculpting

**Memory:** A level-6 Multires on a 5000-vertex mesh = ~20 million vertices in memory. Blender needs ~4× this in actual RAM (undo history, attributes). 32GB RAM is comfortable; 16GB will struggle.

**Undo:** Sculpt undo is expensive — each stroke is a separate undo step. Reduce undo steps in `Preferences → System → Memory & Limits → Undo Steps` if running out of RAM.
