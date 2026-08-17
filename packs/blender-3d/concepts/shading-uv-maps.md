---
id: blender-3d/concepts/shading-uv-maps
title: "Shading — UV Maps, Normals, and Displacement"
type: concept
tags:
  - shading
  - uv-mapping
  - normals
  - displacement
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/shading-rendering.md
related:
  - shading-principled-bsdf.md
  - shading-hdri-lighting.md
content_hash: sha256:da73ab37c08c30b5ab2db44af96ce7138211f21b495e6158f987bdc967a4e9c5
---

# Shading — UV Maps, Normals, and Displacement

UV maps assign 2D texture coordinates to 3D vertices so image textures sit on a mesh. Seam placement, stretch, and the Normal Map node (never a raw image into Normal) determine whether maps look correct; Cycles can also displace geometry.

## UV Mapping

### What UVs Are

UV coordinates are 2D texture coordinates assigned to 3D vertices. "U" = horizontal axis, "V" = vertical axis (both 0 to 1). The same 3D vertex may appear in two different places in UV space (at seams).

### Unwrapping Methods

**Smart UV Project (`U → Smart UV Project`):** Automatic — many small UV islands, fast. Good for objects with tiling/procedural materials.

**Unwrap (mark seams first):** Better quality:
1. In Edit Mode, select edges where you want seams
2. `Ctrl+E → Mark Seam`
3. Select all (`A`), then `U → Unwrap`

**Seam placement strategy:**
- Put seams in hidden areas (underside of arms, inside collar, bottom of objects)
- Follow natural creases and silhouette edges
- Seams should cut the UV into islands that can lie flat (like unfolding a cardboard box)

**UV Stretching:** Blue = compressed, Red = stretched (enable `Stretching` in UV Editor overlay). Fix by adding more seams or using `Average Island Scale` to normalize texel density.

---

## Normal Maps and Displacement

### Normal Maps

A Normal Map encodes per-pixel surface normal directions as colors (blue-ish images).

**How to connect:**
```
Image Texture (Non-Color) → Normal Map node → [Normal input of Principled BSDF]
```

Never connect a Normal Map image directly to the Normal input — it requires the Normal Map node to convert from tangent space colors to actual normal vectors.

**Tangent space (blue-purple images):** Work on any UV layout, work with animation. Use this in Blender.

### Displacement

**Bump Map (fake):** Grayscale texture fakes surface detail without moving geometry. Connected to `Displacement → Height` input. Very fast. Can't see in silhouette.

**True Displacement (Cycles only):** Actually subdivides and moves geometry. Enable in `Material Properties → Settings → Displacement: Displacement Only`. Requires many subdivisions.

**Adaptive Subdivision (Cycles):** Enable in `Render Properties → Subdivision → Experimental feature set`. Cycles subdivides geometry at render time to the level needed for displacement. High-detail displacement without millions of viewport polygons.

---

