---
id: blender-3d/concepts/shading-principled-bsdf
title: "Shading — The Principled BSDF"
type: concept
tags:
  - shading
  - materials
  - principled-bsdf
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/shading-rendering.md
related:
  - shading-procedural-textures.md
  - shading-uv-maps.md
  - shading-eevee.md
content_hash: sha256:72c924ab2730f324744491f0f8dc047fafc1bb5e752424cb66502f79f734f892
---

# Shading — The Principled BSDF

The Principled BSDF is Blender's Disney PBR shader and handles most real-world materials. Metallic is 0 or 1, roughness controls micro-surface, and texture color space (sRGB vs Non-Color) is the usual source of wrong-looking maps.

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

