---
id: blender-3d/concepts/sculpting-dyntopo
title: "Sculpting — Dyntopo (Dynamic Topology)"
type: concept
tags:
  - sculpting
  - dyntopo
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/sculpting.md
related:
  - sculpting-multires-remesh.md
  - sculpting-brushes.md
content_hash: sha256:079e8f676880273d7ef53dcb8f5d5ee32f567b5c8d5c1306b030fcc7c4d911f7
---

# Sculpting — Dyntopo (Dynamic Topology)

Blender's sculpt system operates in three distinct paradigms. Choosing the wrong one for the task is the most common sculpting mistake. Dyntopo dynamically adds and removes triangles under the brush so you can explore form without a pre-subdivided mesh. It destroys UVs, vertex groups, and shape keys, so production detail belongs on Multires.

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

