---
id: blender-3d/concepts/shading-hdri-lighting
title: "Shading — HDRI Lighting"
type: concept
tags:
  - shading
  - hdri
  - lighting
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
  - shading-eevee.md
content_hash: sha256:b5bac7ba2858504e7e7a8a8042d89ea8e52e490930b1d7b28562bc90d4ec7a4e
---

# Shading — HDRI Lighting

HDRI lighting uses a high-dynamic-range environment image as the World background so reflections and ambient light match a real location. Setup is an Environment Texture in the World shader, with a Mapping node for rotation.

## HDRI Lighting Setup

### Setup in World Shader

1. Go to Shader Editor
2. Switch from `Object` to `World` in the dropdown
3. Add `Environment Texture` node (`Shift+A → Texture → Environment Texture`)
4. Open your HDRI file
5. Connect to `Background` node → `World Output`
6. Adjust `Background Strength` for overall intensity

For rotation: Add `Texture Coordinate → Vector → Mapping → Environment Texture`. Use Mapping node's Z rotation.

**Free HDRI sources:**
- **Poly Haven** (polyhaven.com) — CC0 license, excellent quality, up to 16K resolution. The definitive free source.
- **AmbientCG** — excellent for PBR textures and HDRIs

