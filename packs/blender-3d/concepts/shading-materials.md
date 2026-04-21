---
id: blender-3d/concepts/shading-materials
title: "Shading — Principled BSDF, Procedural Textures, and UV Mapping"
type: concept
tags:
  - shading
  - materials
  - principled-bsdf
  - uv-mapping
  - hdri
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-04-21"
verified_by: agent
supersedes:
  - concepts/shading-rendering.md
related:
  - shading-engines.md
---

# Shading — Principled BSDF, Procedural Textures, and UV Mapping

---

## The Principled BSDF: Your Primary Shader

The Principled BSDF is Blender's implementation of Disney's PBR model. It handles 90% of real-world materials well.

### Key Parameters

| Parameter | Range | Behavior |
|-----------|-------|----------|
| Base Color | 0–1 RGB | The diffuse/albedo color. For metals, this is the tint color. |
| Metallic | 0 or 1 | 0 = dielectric (plastic, wood, skin). 1 = metal. Values between are physically wrong. |
| Roughness | 0–1 | 0 = perfect mirror. 1 = fully diffuse. Controls micro-surface detail. |
| IOR | 1.0–3.0 | Index of Refraction. Water=1.33, Glass=1.5, Diamond=2.42. |
| Alpha | 0–1 | Transparency via cutout (sharp) or blend (soft). |
| Specular | 0–1 | Fresnel reflection intensity for dielectrics. Leave at 0.5 (physically correct for most materials). |
| Transmission | 0–1 | Glass/liquid transparency. |
| Emission Color | Color | Surface emissive light output. Combine with Emission Strength to control intensity. |
| Subsurface Weight | 0–1 | SSS amount — how much light scatters below the surface (skin, wax, leaves). |

### Standard Texture-Driven PBR Setup

```
Texture Coordinate (UV) → Mapping → Image Texture (Base Color) → [Base Color input]
                          Mapping → Image Texture (Roughness) → [Roughness input]
                          Mapping → Image Texture (Metallic) → [Metallic input]
                          Mapping → Image Texture (Normal, Non-Color) → Normal Map node → [Normal input]
```

**The Mapping node** lets you control UV tiling, offset, and rotation for all textures simultaneously. Connect one Mapping node and branch out to all Image Texture nodes.

**Color Space matters:**
- Base Color, Emission: **sRGB**
- Roughness, Metallic, Normal, AO: **Non-Color** (data maps, not color maps)

Normal maps especially get connected without setting to Non-Color, resulting in wrong normals.

---

## Procedural Textures

**Noise Texture:** Organic, cloud-like patterns. Settings: Scale (frequency), Detail (fractal octaves), Roughness (octave falloff), Distortion (turbulence).

**Voronoi Texture:** Cell-based patterns — rocks, scales, leather pores, crystals. Feature type: F1 (cell centers), F2 (second-nearest), Distance to Edge (cell outlines).

**Wave Texture:** Sine wave bands or rings. Combine with Noise for realistic wood grain, marble.

**Color Ramp:** Remaps a grayscale value to a color gradient. One of the most-used nodes — essential for converting procedural noise into specific colors/materials.

**Math node:** Mathematical operations on float values. Useful for: clamp (0–1), remap (multiply+add), power (contrast control), greater than/less than (masking).

---

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
