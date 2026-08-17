---
id: blender-3d/concepts/shading-procedural-textures
title: "Shading — Procedural Textures"
type: concept
tags:
  - shading
  - materials
  - procedural
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
  - shading-uv-maps.md
content_hash: sha256:1125d3c49c436cb70a6e233f08113e4f5c9b22bf9a2233bc165a63c5d9a90284
---

# Shading — Procedural Textures

Procedural textures generate patterns in the shader graph without image files. Noise, Voronoi, Wave, Color Ramp, and Math nodes are the building blocks for wood, stone, masks, and value remapping.

## Procedural Textures

**Noise Texture:** Organic, cloud-like patterns. Settings: Scale (frequency), Detail (fractal octaves), Roughness (octave falloff), Distortion (turbulence).

**Voronoi Texture:** Cell-based patterns — rocks, scales, leather pores, crystals. Feature type: F1 (cell centers), F2 (second-nearest), Distance to Edge (cell outlines).

**Wave Texture:** Sine wave bands or rings. Combine with Noise for realistic wood grain, marble.

**Color Ramp:** Remaps a grayscale value to a color gradient. One of the most-used nodes — essential for converting procedural noise into specific colors/materials.

**Math node:** Mathematical operations on float values. Useful for: clamp (0–1), remap (multiply+add), power (contrast control), greater than/less than (masking).

---

