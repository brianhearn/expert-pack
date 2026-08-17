---
id: blender-3d/concepts/modeling-topology
title: "Modeling — Topology Principles and Edit Mode"
type: concept
tags:
  - modeling
  - topology
  - edit-mode
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/modeling-fundamentals.md
related:
  - modeling-retopology.md
  - modeling-modifier-stack.md
  - sculpting-dyntopo.md
content_hash: sha256:7fddbbd63732381991e921cc2a69f9b87d30246f6cfaeb4165a8a107d480e8c2
---

# Modeling — Topology Principles and Edit Mode

Topology is the arrangement of vertices, edges, and faces. Quad edge loops that follow surface contours subdivide and deform cleanly; poles, n-gons, and unapplied scale are the usual sources of pinching and modifier or physics bugs.

## Why Topology Matters

Topology — the arrangement of vertices, edges, and faces — has direct, concrete consequences:

**For subdivision:** Subdivision Surface averages neighboring vertices. Triangles (tris) or poles (vertices with 5+ edges) create pinching, lumps, and artifacts. Quads subdivide predictably.

**For deformation/animation:** When a character bends at the elbow, edges must flow *around* the joint in loops. Bad edge flow causes collapsing, pinching, and "candy wrapper" twists.

**For shading:** Non-planar quads (four vertices not on the same plane) cause shading inconsistencies. N-gons on curved surfaces cause hard shading edges.

**For UV mapping:** Dense poles (6+ edges meeting at a vertex) stretch UV maps badly.

**The rule:** Aim for **all quads**, arranged in **edge loops** that follow the natural contours of the surface.

### Poles

A pole is any vertex where the number of connected edges is not 4.
- **3-pole (E-pole):** Common at corners, topology transitions. Acceptable in most locations.
- **5-pole (N-pole):** Creates a subtle pinch under Subdivision Surface. Acceptable away from curved surfaces and deformation zones.
- **6+-pole:** Highly problematic. Avoid almost everywhere.

The art of topology is routing edge loops so that poles end up in "safe" locations — flat areas, hidden areas, areas that don't deform.

---

## Edit Mode Essentials

### Selection Modes
`1` = Vertex select, `2` = Edge select, `3` = Face select. Hold `Shift` to combine modes.

### Core Operations and Shortcuts

| Operation | Shortcut | Notes |
|-----------|----------|-------|
| Extrude | `E` | Extrudes selection along normals. `Alt+E` for extrude menu. |
| Inset | `I` | Creates an inset face. `I` again while insetting = per-face mode. |
| Bevel | `Ctrl+B` | Bevels edges. Scroll wheel controls segment count. `V` for vertex bevel. |
| Loop Cut | `Ctrl+R` | Adds an edge loop. Scroll before clicking to add multiple. |
| Knife | `K` | Free-cut polygons. `Z` = cut-through. `Enter` to confirm. |
| Bridge Edge Loops | `Ctrl+E → Bridge Edge Loops` | Connects two edge loops with new faces. |
| Fill | `F` | Creates a face from selected vertices/edges. |
| Merge | `M` | Merges selected vertices. |
| Dissolve | `Ctrl+X` | Removes vertices/edges while preserving surrounding topology. |
| Separate | `P` | Separates selected geometry into a new object. |

### Proportional Editing
`O` toggles proportional editing. Edits fall off gradually to surrounding vertices. Scroll wheel changes radius. **#1 source of "why did my whole mesh move?"** — users forget it's on.

### Pivot Points (`Period` key):
- **Bounding Box Center:** Geometric center of selection
- **3D Cursor:** Transforms around the red/white circle (position with `Shift+RMB`)
- **Individual Origins:** Each selected element transforms around its own center — critical for scaling multiple faces independently
- **Active Element:** The last-selected element

---

