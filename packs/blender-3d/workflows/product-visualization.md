---
title: Product Visualization Workflow
type: workflow
tags:
- product-visualization
- workflows
pack: blender-3d
retrieval_strategy: atomic
id: blender-3d/workflows/product-visualization
verified_at: '2026-04-10'
verified_by: agent
---

<!-- context: blender-3d/workflows/product-visualization -->

# Product Visualization Workflow

> **Lead summary:** Product visualization prioritizes material accuracy, controlled lighting, and camera precision over artistic creativity. The workflow is: studio lighting environment → physically accurate PBR materials → camera setup with correct focal length → render settings tuned for still images or turntable animations. The decisions that separate professional product renders from hobbyist attempts are surface detail (fingerprints, micro-scratches, real roughness variation), light quality (area lights with correct size/falloff, not point lights), and denoising strategy (high enough samples that denoising doesn't smear detail).

---

## Studio Lighting Setup

### The Three-Point Foundation

Product photography uses a three-point setup adapted from still photography:

**Key light (primary):** Largest, softest light source. Defines the main shadow.
```
Type: Area Light
Shape: Rectangle (for directional highlights on products)
Size: 0.5m–2m depending on product scale
Strength: 100–500W (Cycles) or adjust until key areas hit target exposure
Position: 45° from camera left or right, 30° above product height
```

**Fill light (secondary):** Reduces shadow contrast without eliminating it.
```
Type: Area Light  
Size: Same or slightly larger than key
Strength: 25–50% of key (creates 2:1 or 4:1 lighting ratio)
Position: Opposite side from key, same height or slightly lower
Color: Slightly warm or cool vs key for subtle color contrast
```

**Rim/back light:** Separates the product from the background.
```
Type: Area Light or Spot
Size: Smaller than key (creates sharper specular edge)
Strength: 50–150% of key
Position: Behind and above the product, aimed at rear edges
```

### HDRI as Base Environment

For product work, combine HDRI (ambient/fill) with area lights (controlled highlights):

```
World → Surface → Environment Texture → .hdr file
Strength: 0.2–0.5 (low — just for ambient base, not primary lighting)
```

The HDRI prevents pitch-black shadows and adds subtle environmental bounce. The area lights control the intentional highlights. This hybrid approach is standard in commercial product rendering.

**HDRIs for studio work (all from polyhaven.com):**
- `studio_small_03` — clean neutral studio, subtle gradient
- `studio_country_hall` — warm studio tones
- `christmas_photo_studio_07` — high-key white studio look
- Use `Rotation` on the Mapping node to orient the HDRI so interesting highlights land where you want

### Background — Sweep (Cyc Wall)

A curved background plane that eliminates the corner between floor and wall:

1. Add a `Plane`, extrude one edge up, add a `Subdivision Surface` modifier (level 3), select the corner edge loop, `G → Z` to raise it into a curved sweep
2. Or: use a `Curve` path — simpler to control the sweep angle
3. Material: pure white diffuse OR a gradient from light grey to white going up

**Infinite white background trick:** Use a `Background` shader in the World with pure white (1.0, 1.0, 1.0) at high strength (3–5). Anything lit to white or above clips to white in the render, creating a seamlessly blown-out white background without needing a physical plane.

---

## HDRI Lighting Control

### Rotating Without Affecting Background

To rotate the HDRI environment without rotating the background image visible in the render:

```
World Material node setup:
Texture Coordinate (Generated) → Mapping (Rotation Z: X°) → Environment Texture → Background
```

Add a `Light Path` node to separate the sky from lighting:

```
Is Camera Ray ──┐
                ├→ Mix Shader → Background
Environment ────┘
(Is Camera: show solid color)
(Not camera: use HDRI)
```

This lets you render with HDRI lighting while showing a solid color (or gradient) as the visible background.

### Isolating Highlights

To control exactly where a specular highlight falls on a reflective product:

1. Use an area light with a small size (1–5cm for tight highlights, 20–50cm for broad ones)
2. Place the area light perpendicular to the surface normal at the reflection angle
3. Use `LookDev` mode to preview specular highlights without full render
4. The position rule: the light appears at the reflection of the camera position across the surface normal

---

## Material Setup for Photorealism

### Principled BSDF Parameter Reference

For common product materials:

**Polished metal (aluminum, chrome):**
```
Base Color: (0.9, 0.9, 0.9) — light grey, not pure white
Metallic: 1.0
Roughness: 0.05–0.15
```

**Brushed metal:**
```
Base Color: (0.7, 0.7, 0.72)
Metallic: 1.0
Roughness: 0.4
Anisotropic: 0.7–0.9
Anisotropic Rotation: 0.0
(Add an Anisotropic Tangent for curved surfaces)
```

**Matte plastic:**
```
Base Color: product color
Metallic: 0.0
Roughness: 0.6–0.8
Specular IOR Level: 0.5
```

**Glossy plastic:**
```
Base Color: product color
Metallic: 0.0
Roughness: 0.1–0.25
Specular IOR Level: 0.5
IOR: 1.46
```

**Clear glass:**
```
Base Color: (1.0, 1.0, 1.0) white
Transmission Weight: 1.0
IOR: 1.52 (glass) or 1.333 (water)
Roughness: 0.0 (polished) or 0.05–0.1 (frosted)
Metallic: 0.0
```

**Rubber/silicone:**
```
Base Color: material color
Metallic: 0.0
Roughness: 0.8–1.0
Sheen Weight: 0.3–0.5
Sheen Roughness: 0.5
```

### Surface Imperfection Textures

Perfect materials look fake. Add imperfection layers:

**Fingerprint/smudge overlay:**
```
Node setup:
Image Texture (fingerprint_smudge.jpg) → Bump Node (Strength: 0.2) → Normal
Image Texture (same) → ColorRamp (black→white) → Math (Multiply, 0.05) → add to Roughness
```

**Micro-scratch overlay:**
```
Image Texture (scratches_fine.jpg, tiled at 8–16x scale) 
→ Normal Map → Normal input
Adds fine scratches to metal without altering overall roughness
```

Free imperfection textures: [ambientcg.com](https://ambientcg.com), [polyhaven.com], [textures.com] (some free)

**Roughness variation:** Real surfaces have spatially varying roughness — the middle of a phone screen is cleaner than the edges. Use a Gradient Texture or hand-painted roughness map to vary it spatially.

### Node Setup for a Multi-Layer Product Material

```
Node setup (plastic with label):

─── LAYER 1: Base plastic ────────────────────────────
Principled BSDF → (base plastic params)

─── LAYER 2: Label/print ─────────────────────────────
Image Texture (label.png) → Alpha channel → Mix Shader weight
Principled BSDF (label: higher roughness, colored)

─── LAYER 3: Clearcoat ───────────────────────────────
Coat Weight: 1.0, Coat Roughness: 0.0–0.05 (on the base Principled BSDF)
(Simulates the shiny topcoat over a printed label)

─── FINAL COMBINATION ────────────────────────────────
Mix Shader (factor = label alpha) → Material Output
```

---

## Camera Setup

### Focal Length for Products

Focal length dramatically affects product photography feel:

| Focal Length | Effect | Best For |
|-------------|--------|----------|
| 24–35mm | Wide, slight distortion, spacious | Lifestyle context shots |
| 50mm | Natural, minimal distortion | Standard product shots |
| 85–100mm | Moderate compression, flattering | Consumer goods, cosmetics |
| 135–200mm | Strong compression, isolated feel | Jewelry, watches, technical products |

**Set in:** `Properties → Camera → Focal Length` or `N` panel in camera view.

For products without a real-world scale reference, set Scene Units to metric and ensure the product is actual size (a smartphone is 15cm tall, a wine bottle is 30cm, etc.). Wrong scale gives wrong depth of field and lighting behavior.

### Depth of Field

```
Camera properties → Depth of Field:
Focus Object: Empty placed at the product's sharpest point (or set F-stop manually)
F-Stop: 8.0–16.0 for "everything sharp" commercial look
F-Stop: 2.8–4.0 for selective focus (background blur)
```

Cycles: DoF is physically accurate — matches real photography aperture behavior.
EEVEE: DoF is a screen-space effect — less accurate, but fast. Increase `Max Size` in EEVEE DoF settings to prevent harsh edges.

### Lens Distortion

Real camera lenses have slight barrel distortion. To add:
```
Compositor → Lens Distortion node
Distortion: 0.02–0.05 (subtle, adds realism)
Dispersion: 0.003 (chromatic aberration — very subtle)
```

---

## Turntable Animation

### Clean Turntable Setup

**Method 1 — Rotate the product:**
```python
# Keyframe rotation on an empty parent
# Frame 1: Rotation Z = 0°, Frame 250: Rotation Z = 360°
# Add Cycles modifier for seamless loop
```

1. Place an **Empty** at the product's center of mass
2. Parent the product (and lights if needed) to the Empty
3. Key Empty Rotation Z: frame 1 = 0°, frame 251 = 360°
4. In the Graph Editor, set the F-curve interpolation to **Linear** (no easing — constant rotation speed)
5. Add a **Cycles** modifier to loop if needed

**Method 2 — Rotate the camera:**
```
Camera on circular path using Follow Path constraint:
1. Add Bezier Circle, scale to orbit radius
2. Add Camera, select Camera → select Circle → Ctrl+P → Follow Path
3. Animate the Path offset from 0 to 100% over desired frames
4. Track To constraint on camera targeting the product
```

### Turntable Render Settings

For a 10-second turntable at 24fps = 240 frames. At 30fps = 300 frames.

```
Output: /renders/turntable_####
Format: PNG (for compositing) or JPEG (direct use)
Resolution: 1920×1080 (web), 3840×2160 (4K marketing), 2048×2048 (square social media)
Frame Range: 1–240 (or 1–300 for 30fps)
```

**Even lighting across 360°:** Light the product so highlights appear at aesthetically pleasing angles every ~90°. If lights are fixed to the world, the product rotates through them — the highlight sweep is part of the visual interest. If lights rotate with the product, the look is static (works for material demos, not lighting demos).

---

## Render Settings for Product Shots

### Cycles Settings (Still Images)

```
Samples: 512–2048 (still images; higher for glass/metallic products with complex caustics)
Denoiser: Intel Open Image Denoise (OIDN) or OptiX (NVIDIA GPU)
Denoiser Input Passes: use Color + Diffuse + Glossy passes for better detail preservation

Light Paths:
  Max Bounces Total: 12
  Diffuse: 4
  Glossy: 8 (important for reflective products)
  Transmission: 12 (critical for glass products)
  Volume: 0 (unless product has volumetric material)
  Transparent: 8

Film:
  Filter: Gaussian, Width: 1.5px (softer) or Box (sharper)
  Transparent: ON (for PNG with alpha background)
```

### EEVEE Settings (Quick Previews or NPR Stylization)

```
Render:
  Samples: 64–128
  Ambient Occlusion: ON, Distance: 0.1–0.3m
  Bloom: ON only if product has glow elements
  Screen Space Reflections: ON (Thickness: 0.1, Edge Fade: 0.05)

Shadows:
  Cube Size: 2048 (point/spot lights)
  Cascade Size: 2048 (sun/directional)
  Soft Shadows: ON
```

### Render Passes for Compositing

Render to multilayer EXR for maximum post-processing flexibility:

```
View Layer → Passes:
Combined: ON
Z (Depth): ON
Diffuse Direct + Indirect: ON
Glossy Direct + Indirect: ON
Shadow: ON
Ambient Occlusion: ON
```

In the Compositor, route individual passes through Color Balance, Curves, and Glow nodes before recombining. This lets you boost specularity, add glow to glossy highlights, or darken shadows without re-rendering.

### Post-Processing in Compositor

Minimal but effective product render compositing:

```
Compositor node chain:
Render Layers → Lens Distortion (subtle) → Color Balance → Glare (Bloom, small) → Viewer/Output

Glare settings for subtle highlight bloom:
  Type: Bloom, Streaks, or Ghosts
  Quality: High
  Threshold: 0.85 (only very bright highlights glow)
  Strength: 0.3–0.5
```

---

## Common Product Visualization Pitfalls

**Uniform roughness:** Every surface in real life has roughness variation — fingerprints, wear, dust. Add a Noise Texture mixed into the Roughness input at low strength (0.05–0.15 mix factor) to break up perfectly uniform surfaces.

**Wrong IOR on glass:** Default glass often uses IOR 1.45. Actual values: crown glass = 1.52, borosilicate = 1.47, crystal = 1.54, water = 1.333. Wrong IOR changes the refraction angle, making glass look plastic.

**Infinite thin glass:** Glass objects need actual thickness (wall thickness of at least 1–2mm in real-world units) for refraction to render correctly in Cycles. A plane with a glass material refracts incorrectly.

**Area lights too small:** An area light smaller than the specular highlight it creates looks like a point light — hard edges, harsh falloff. Size the area light larger than the intended specular highlight size.

**No color management:** `Render → Color Management → View Transform: Filmic` (not Standard) for photorealistic renders. Filmic handles highlight rolloff like real film/cameras. Standard clips highlights to white harshly.

**Missing subsurface scattering:** Organic products (candles, soaps, skin-colored plastics) need SSS. `Principled BSDF → Subsurface Weight: 0.1–0.5`, `Subsurface Radius: (1.0, 0.2, 0.1)` for warm skin-like SSS.
