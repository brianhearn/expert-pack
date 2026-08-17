---
id: blender-3d/concepts/modeling-retopology
title: "Modeling — Retopology and Common Mistakes"
type: concept
tags:
  - modeling
  - retopology
  - topology
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/modeling-fundamentals.md
related:
  - modeling-topology.md
  - sculpting-multires-remesh.md
content_hash: sha256:ef8226c46fa9b7c729722d9fc3cc51d0b92ea35c1c623f6e21d0a548e20528ac
---

# Modeling — Retopology and Common Mistakes

Retopology builds new, animation-ready quad topology over a high-resolution sculpt or scan. Unapplied scale, n-gons, overlapping verts, and non-manifold edges are the modeling mistakes that break subdivision, Booleans, and physics before you even retopo.

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

