---
id: blender-3d/concepts/sculpting-multires-remesh
title: "Sculpting — Multires, Remesh, and Head Workflow"
type: concept
tags:
  - sculpting
  - multires
  - remesh
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/sculpting.md
related:
  - sculpting-dyntopo.md
  - modeling-retopology.md
  - sculpting-masking-facesets.md
content_hash: sha256:ec409aea7f1bcbee878bab5ccd3f1f1ddd4b41ba9e82176818025313d0b5ae82
---

# Sculpting — Multires, Remesh, and Head Workflow

Multires subdivides a preserved base mesh so you can sculpt detail by level; remesh rebuilds uniform topology when the mesh is a mess. A typical head workflow is Dyntopo for form, voxel remesh, Multires for detail, then retopo.

## Multi-Resolution (Multires)

Multires is the professional sculpting workflow. Subdivides a mesh into multiple levels and lets you sculpt on each level independently.

**Key principle:** The base mesh topology is preserved. Sculpt high-frequency detail at high levels, major forms at lower levels.

**Setup:**
1. Start with a clean, retopologized mesh (or block-out)
2. Add Multires modifier (`Properties → Modifiers → Multires`)
3. Add subdivisions with `Subdivide` button — 6 levels is common (base → 64x polygon count)
4. Enter Sculpt Mode — sculpt at any level

**Level selector:**
- `Preview` — current level displayed in viewport
- `Sculpt` — which level your brush strokes land on
- `Render` — which level is used at render time

**Sculpt levels workflow:**
- Level 1–2: Block out major forms, proportions
- Level 3–4: Secondary forms (muscle groups, major surface features)
- Level 5–6: Fine detail (skin pores, wrinkles, fabric weave)

**Multires Reshape:** Apply a mesh from another source onto the Multires base cage — useful for baking back external sculpt details.

---

## Remeshing (Voxel and Quad)

Remeshing converts any mesh into clean, uniform topology.

**Voxel Remesh:** `Ctrl+R` in Sculpt Mode. Creates a watertight mesh from voxel representation. Voxel Size controls resolution (smaller = more polygons = more detail preserved).

Good for: combining multiple objects into one mesh, resetting Dyntopo mess before Multires, creating a closed volume from an open mesh.

After voxel remesh, you lose UV maps and vertex groups — but the new mesh is all-quad and uniform, ready for Multires.

**Quad Remesh (4.x):** `Object → Remesh → QuadRemesh`. Uses the instant-meshes algorithm for quad-dominant retopology.

Settings:
- `Target Quads`: how many quads to target
- `Use Vertex Color for Density`: paint density guides with vertex colors
- `Preserve Sharp Edges`: keep hard features

Quad Remesh result is near-production-quality retopology — not perfect, but an excellent starting point. Needs cleanup for complex shapes.

---

## Typical Character Head Sculpt Workflow

1. **Base mesh:** Start with a simple sphere (32×32 UV Sphere) or a refined basemesh with major landmarks blocked in.
2. **Rough form (Dyntopo ON, ~20px detail):** Grab, Snake Hook, Clay for major volumes — cranium, cheekbones, jaw. Keep detail size ~10px.
3. **Voxel remesh:** Once major form is good, remesh at size giving ~200–500k triangles.
4. **Add Multires modifier** (6 subdivisions). Sculpt at level 2–3 for secondary forms.
5. **Secondary forms (level 3):** Muscle groups, orbital rims, nasolabial folds, ear helix shape.
6. **Detail pass (level 5–6):** Pores (texture brush with skin alpha), wrinkles (Crease brush), sub-dermal fat bumps.
7. **Polish:** Smooth, Flatten, Polish brushes.
8. **Retopology:** Quad Remesh for base, then refine manually.

