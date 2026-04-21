---
id: blender-3d/concepts/modeling-topology
title: "Modeling — Topology Principles and Edit Mode Operations"
type: concept
tags:
  - modeling
  - topology
  - edit-mode
  - retopology
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-04-21"
verified_by: agent
supersedes:
  - concepts/modeling-fundamentals.md
related:
  - modeling-modifiers.md
  - sculpting-paradigms.md
---

# Modeling — Topology Principles and Edit Mode Operations

---

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

## Common Modeling Mistakes

### Unapplied Scale (The #1 Gotcha)
**Symptom:** Subdivision Surface creates uneven smoothing, physics behaves oddly, textures scale inconsistently.
**Cause:** Scaled the object in Object Mode without applying the scale. Modifiers and physics use the object's scale — a scale of (1, 1, 3) means physics thinks the object is 3x taller.
**Fix:** `Ctrl+A → Scale` to apply the scale, baking it into the mesh. Do this before applying modifiers or setting up physics.

### N-Gons Under Subdivision Surface
N-gons (5+ sided faces) create unpredictable smoothing. Use `Overlay → Mesh Analysis → N-Gons` to check.

### Overlapping Vertices
Fix with `Mesh → Merge by Distance` (select all in Edit Mode). Set the merge distance appropriately for your scale.

### Non-Manifold Geometry
A manifold mesh is one where every edge is shared by exactly 2 faces. Non-manifold geometry causes issues with Solidify modifier, 3D printing, Boolean operations, and physics simulation.
Check: `Select → Select All by Trait → Non-Manifold`.

---

## Retopology

Retopology creates new, clean topology over existing high-resolution geometry (usually a sculpt).

**When you need it:**
- After sculpting a character (sculpt mesh = millions of tris, useless for animation)
- After importing CAD or scan data (non-quads, excessive density)

**Manual retopo workflow:**
1. Add a new empty mesh object on top of the sculpt
2. Enable `Snap to Face` with `Project Individual Elements`
3. Use `LoopTools` add-on (built-in) for evenly-spaced loops
4. Draw quads with `F` (face creation)
5. Use `Shrinkwrap` modifier (Nearest Surface mode) for real-time snapping

**Automated retopo:**
- **QuadriFlow** (built-in, `Mesh → Remesh → QuadriFlow`) — creates all-quad mesh
- **Instant Meshes** (external free tool) — often better results than QuadriFlow for complex shapes
- **Remesh modifier** (Voxel mode) — for uniform density mesh for further sculpting

**After retopology:** Bake normal maps from the high-res sculpt onto the low-res retopo mesh using Blender's bake system (`Properties → Render → Bake`, type `Normal`, `Selected to Active`).
