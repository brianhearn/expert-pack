---
id: blender-3d/concepts/sculpting-paradigms
title: "Sculpting — Three Paradigms: Dyntopo, Multires, and Remesh"
type: concept
tags:
  - sculpting
  - dyntopo
  - multires
  - remesh
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-04-21"
verified_by: agent
supersedes:
  - concepts/sculpting.md
related:
  - sculpting-brushes-masking.md
  - modeling-topology.md
---

# Sculpting — Three Paradigms: Dyntopo, Multires, and Remesh

Blender's sculpt system operates in three distinct paradigms. Choosing the wrong one for the task is the most common sculpting mistake.

---

## Dyntopo (Dynamic Topology)

Dyntopo dynamically adds and removes triangles under the brush as you sculpt. The mesh isn't subdivided in advance — topology grows where you need it.

**When to use:** Concept sculpting and exploration, adding major forms from a low-poly base, any time you need geometry where the base mesh doesn't have it.

**When NOT to use:** When you have clean topology to preserve, final production sculpting (use Multires instead), after retopology.

**Enable:** Sculpt Mode → Header → Dyntopo checkbox, or `Ctrl+D`.

**Dyntopo settings:**

| Setting | Effect |
|---------|--------|
| Detail Size | Controls triangle size (smaller = more polygons). |
| Detail Type | `Relative` (adapts to distance), `Constant` (fixed world size), `Brush` (detail follows brush size). |
| Refine Method | `Subdivide Edges` (only adds), `Collapse Edges` (only removes), `Subdivide Collapse` (both — best for most work). |

**Performance:** Keep your sculpt under 2M triangles during exploration.

**Warning:** Dyntopo destroys UV maps, vertex groups, shape keys, and any attribute data it touches. Not meant for final production meshes.

**Expert settings for hard-surface concept sculpting:**
- Use **Constant Detail** mode (not Relative) at size 2.0–4.0
- Refine method: **Subdivide Edges only** — preserves sharp transitions
- Detail size **3.5px** is the community-recommended sweet spot for mechanical parts
- Run `Detail Flood Fill` after major strokes to regularize triangle density

---

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
