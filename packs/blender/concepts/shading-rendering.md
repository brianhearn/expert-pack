# Shading and Rendering

Blender's rendering system is one of its strongest features, offering two production-quality render engines alongside a flexible node-based material system. The gap between "technically correct" and "looks good" in rendering is enormous — this file focuses on the decision-making layer.

---

## EEVEE vs Cycles — When to Use Each

This is the most common rendering question for intermediate users. The answer is not "Cycles is better" — they're tools for different jobs.

### Use EEVEE When:
- **Speed is critical** — product visualization, motion graphics, game cinematics, broadcast
- **Real-time preview matters** — iterating on look development where waiting for Cycles is impractical
- **Stylized output** — EEVEE's rasterization artifacts can be art-directed; Cycles is too physically correct for some styles
- **Grease Pencil** — Grease Pencil is fundamentally designed for EEVEE; Cycles support is secondary
- **Motion blur, depth of field** — EEVEE's implementations are fast and often good enough
- **Arch-viz previsualization** — before committing to a full Cycles render

### Use Cycles When:
- **Photorealism is the goal** — product photography replacement, VFX plates, photorealistic environments
- **Transparent/refractive materials** — glass, water, gemstones. EEVEE's screen-space reflections miss offscreen objects; Cycles handles these physically
- **Caustics** — light focusing through glass. EEVEE can't do this; Cycles can (with some configuration)
- **Complex indirect lighting** — Global illumination (light bouncing off colored walls, color bleed) is physically correct in Cycles; EEVEE approximates it
- **Subsurface scattering** — skin, wax, marble. Cycles does this accurately; EEVEE Next approximates
- **Volumetrics** — fog, fire, smoke. Both support this, but Cycles is more accurate
- **Final frames for client delivery** — when quality is non-negotiable

### The Practical Answer
Many professionals do their look development in EEVEE (fast iteration) and switch to Cycles for final renders. Use EEVEE's "Render" mode in the viewport aggressively — you get near-final quality lighting instantly.

---

## EEVEE Next (Blender 4.2+)

EEVEE was completely rewritten in Blender 4.2 as "EEVEE Next." Key improvements:

- **Ray-traced shadows** (GPU-accelerated) — dramatically better than old shadow maps
- **Screen-space global illumination (SSGI)** — better color bleed and indirect lighting
- **Improved subsurface scattering** — more accurate skin/wax rendering
- **Better volumetric shadows** — previously a significant limitation
- **GPU-only rendering** — EEVEE Next requires a GPU; CPU-only machines cannot use it

**Remaining limitations of EEVEE (even Next):**
- Screen-space reflections miss anything offscreen or behind the camera
- No true global illumination — indirect light is approximated
- Volume rendering is still less accurate than Cycles
- Some complex shader node combinations don't work the same as in Cycles
- Transparent shadows are simulated, not physically traced

---

## Cycles: GPU and Performance

### GPU Rendering

Cycles GPU rendering is dramatically faster than CPU in most cases. Configuration:

`Edit → Preferences → System → Cycles Render Devices`

| GPU Backend | For |
|-------------|-----|
| CUDA | Older NVIDIA (GTX 900 series through RTX 20xx) |
| OptiX | NVIDIA RTX series — uses hardware ray tracing; significantly faster |
| HIP | AMD GPUs (RX 5000+) |
| Metal | Apple Silicon (M1/M2/M3) and AMD Mac GPUs |
| oneAPI | Intel Arc GPUs |

**Enable GPU render:** After setting up in Preferences, in Render Properties → Render Device → GPU Compute.

**Hybrid CPU+GPU:** Blender can use both CPU and GPU simultaneously. Often not worth it — the slower CPU tiles slow down the overall render. Test with your specific hardware.

### Key Render Settings (Cycles)

**Samples:** The number of ray paths traced per pixel.
- Viewport: 32–64 samples is usually enough for previews
- Render: 256–1024 for most scenes; very noisy environments (interior, night scenes, DOF) need 1000+
- Adaptive Sampling is enabled by default in modern Blender — it stops sampling each pixel when it converges, dramatically reducing render times

**Denoising:** Removes noise from Cycles renders.
- **OpenImageDenoise (OIDN):** CPU-based, very high quality, works on any machine
- **OptiX Denoiser:** NVIDIA-only, very fast GPU denoising, slightly lower quality than OIDN
- **NLM (Non-local Means):** Built-in, slower, lower quality — rarely used now
- **Render pass denoising:** For animation, denoise via the Compositor using the Denoising Data render pass — frame-by-frame denoising can flicker; temporal denoising (DaVinci Resolve's temporal denoiser, NEATVIDEO) is better for animation

**Light Paths:**
- Max bounces (Total/Diffuse/Glossy/Transmission/Volume/Transparent) control how many times a ray can bounce
- The defaults are conservative. For most scenes: Total 12, Diffuse 4, Glossy 4, Transmission 12
- For interior scenes or complex glass: increase Transmission and Total bounces
- `Render Properties → Light Paths → Clamp → Indirect Light` — clamping indirect light to 10-15 eliminates fireflies (bright pixel artifacts) at the cost of slight energy loss. Set this early.

**Film Transparency:** Enables transparent background rendering (alpha channel). In `Render Properties → Film → Transparent`. Essential for compositing.

---

## The Principled BSDF: Your Primary Shader

The Principled BSDF is Blender's implementation of Disney's PBR model. It handles 90% of real-world materials well.

### Key Parameters

| Parameter | Range | Behavior |
|-----------|-------|----------|
| Base Color | 0–1 RGB | The diffuse/albedo color. For metals, this is the tint color. |
| Metallic | 0 or 1 | 0 = dielectric (plastic, wood, skin). 1 = metal. Values between are physically wrong — avoid for realism. |
| Roughness | 0–1 | 0 = perfect mirror. 1 = fully diffuse. Controls micro-surface detail. |
| IOR | 1.0–3.0 | Index of Refraction for glass/liquid. Water=1.33, Glass=1.5, Diamond=2.42. |
| Alpha | 0–1 | Transparency via cutout (sharp edges) or blend (soft edges). Blend mode set in Material properties. |
| Normal | Vector | Input for Normal Map node output. For adding surface micro-detail. |
| Specular | 0–1 | Fresnel reflection intensity for dielectrics. Usually leave at 0.5 (physically correct for most materials). |
| Specular Tint | 0–1 | Tints the reflection to the base color. Physical only for metals (already handled by Metallic). |
| Transmission | 0–1 | Glass/liquid transparency (subsurface transmission, not cutout). |
| Emission Color | Color | Surface emissive light output. Combine with Emission Strength to control intensity. |
| Subsurface Weight | 0–1 | SSS amount. Controls how much light scatters below the surface (skin, wax, leaves). |

### PBR Workflow Pattern

Standard texture-driven PBR setup:
```
Texture Coordinate (UV) → Mapping → Image Texture (Base Color) → [Base Color input]
                          Mapping → Image Texture (Roughness) → [Roughness input]
                          Mapping → Image Texture (Metallic) → [Metallic input]
                          Mapping → Image Texture (Normal, Non-Color) → Normal Map node → [Normal input]
```

**The Mapping node** is between Texture Coordinate and Image Texture. It lets you control UV tiling, offset, and rotation for all textures simultaneously. Connect one Mapping node and branch out to all Image Texture nodes — this is the standard pattern.

**Color Space matters:**
- Base Color, Emission: **sRGB** (for image textures representing color)
- Roughness, Metallic, Normal, AO: **Non-Color** (these are data maps, not color maps — treating them as sRGB shifts values incorrectly)

This is a very common mistake — Normal maps especially get connected without setting the Image Texture node to Non-Color, resulting in wrong normals.

---

## Procedural Textures

Blender's procedural texture nodes create textures mathematically — no image files needed.

### Key Nodes

**Noise Texture:** Generates organic, cloud-like patterns. Key settings: Scale (frequency), Detail (fractal octaves), Roughness (octave contribution falloff), Distortion (turbulence). Output: Fac (grayscale), Color (colorized noise), Vector (distorted positions).

**Voronoi Texture:** Cell-based patterns — rocks, scales, leather pores, crystals. Feature type: F1 (cell centers), F2 (second-nearest), Distance to Edge (cell outlines).

**Wave Texture:** Sine wave bands or rings. Combine with Noise for realistic wood grain, marble.

**Musgrave Texture:** Fractal landscapes, terrain-like noise. More control over fractal character than Noise.

**Color Ramp:** Remaps a grayscale value to a color gradient. Essential for converting procedural noise into specific colors/materials. One of the most-used nodes in any shader tree.

**Math node:** Mathematical operations on float values. Useful for: clamp (0–1), remap (using multiply+add), power (contrast control), greater than/less than (masking).

**Mix Node (Shader):** Blends two shaders using a factor. The factor can be a texture, making it a material mask.

---

## UV Mapping

### What UVs Are

UV coordinates are 2D texture coordinates assigned to 3D vertices. They determine how a 2D image "wraps" onto a 3D surface. "U" = horizontal axis, "V" = vertical axis (both from 0 to 1).

Every vertex in a UV map can have different UV coordinates per face (this is how UVs work at seams — the same 3D vertex may appear in two different places in UV space).

### Unwrapping Methods

**Smart UV Project (`U → Smart UV Project`):** Automatically cuts seams and unwraps. Fast. Results in many small UV islands, poor for texture painting. Excellent for:
- Objects that will use tiling/procedural materials
- Background objects where texture quality isn't critical
- Quick unwraps for testing

**Unwrap (mark seams first):** Better quality. Workflow:
1. In Edit Mode, select edges where you want seams (natural creases, hidden areas)
2. `Ctrl+E → Mark Seam` (edges turn orange/red)
3. Select all (`A`), then `U → Unwrap`
4. View in UV Editor — island placement will be based on your seams
5. Scale, pack, and arrange islands in the UV Editor

**Seam placement strategy:**
- Put seams in hidden areas (underside of arms, inside of collar, bottom of objects)
- Follow natural creases and silhouette edges when possible
- Seams should cut the UV into islands that can lie flat (like unfolding a cardboard box)

**Cylindrical/Spherical Unwrap:** Quick for simple shapes. Cylinder maps project from a cylinder; Sphere from a sphere. Appropriate for pipes, balls, but not for organic shapes.

### UV Stretching

Blue = compressed, Red = stretched (enable in UV Editor overlay: `Stretching`). Aim for green (no distortion). Stretching causes textures to look squished or blurry.

Fix stretching by:
- Adding more seams to allow flatter unfolding
- Using `Average Island Scale` (in UV Editor, `UV → Average Island Scale`) to normalize all islands to the same texel density
- Manually repositioning UV points in the UV editor

---

## Normal Maps and Displacement

### Normal Maps
A Normal Map encodes per-pixel surface normal directions as colors. Blue-ish images are normal maps (where blue = straight up in tangent space). They fake surface bumps without adding geometry.

**How to connect:**
```
Image Texture (Non-Color) → Normal Map node → [Normal input of Principled BSDF]
```

Never connect a Normal Map image directly to the Normal input — it requires the Normal Map node to convert from tangent space colors to actual normal vectors.

**Tangent space vs Object space normal maps:**
- Tangent space (blue-purple images): Work on any UV layout, work with animation. Default. Use in Blender.
- Object space (rainbow-colored): Baked to a specific mesh orientation. Break with animation. Don't use in Blender unless specifically required.

### Displacement
Real displacement actually moves geometry. Two types:

**Bump Map (fake):** Uses a grayscale texture to fake surface detail without moving geometry. Connected to the `Displacement → Height` input, or to Principled BSDF Bump. Very fast. Can't see in silhouette. Good for: subtle surface detail, concrete, skin pores.

**True Displacement (Cycles only):** Actually subdivides and moves geometry. Enable in `Material Properties → Settings → Displacement: Displacement Only` (or Displacement and Bump). Requires many subdivisions to look good — use Subdivision Surface modifier or Adaptive Subdivision.

**Adaptive Subdivision (Cycles):** Cycles can subdivide geometry at render time to the level needed for displacement. Enable in `Render Properties → Subdivision → Experimental feature set`. Then the Subdivision Surface modifier uses a render-time tessellation pass. This is how you get displacement without having millions of polygons in your viewport.

---

## HDRI Lighting Setup

### What an HDRI Is
A panoramic 360° photograph (or CGI image) with real light intensity data stored in floating-point format (not clamped to 0–1 like regular images). The light intensities can be thousands of times brighter than the surroundings, making it physically accurate as a light source.

### Setup in World Shader
1. Go to `Shader Editor`
2. Switch from `Object` to `World` in the dropdown
3. Delete the default Background node
4. Add `Environment Texture` node (`Shift+A → Texture → Environment Texture`)
5. Open your HDRI file in the node
6. Connect to `Background` node → `World Output`
7. Adjust `Background Strength` for overall intensity

For rotation: Add `Texture Coordinate → Vector → Mapping → Environment Texture`. Use the Mapping node's Z rotation to rotate the HDRI.

**Free HDRI sources:**
- **Poly Haven** (polyhaven.com) — CC0 license, excellent quality, up to 16K resolution. The definitive free source.
- **HDRI Haven** (now merged into Poly Haven)
- **AmbientCG** — also excellent for PBR textures and HDRIs

---

## Render Settings That Matter

### Film Settings
- **Exposure:** Adjusts overall image brightness after rendering. Non-destructive.
- **Transparent Background:** Renders alpha channel for compositing. Enable in `Film → Transparent`.
- **Filter Size:** Anti-aliasing filter size. Higher = slightly blurrier but smoother edges.

### Color Management
- **Color Space:** sRGB for display, Linear for compositing. Don't change this unless you know what you're doing.
- **View Transform:** Filmic (default since 2.79) compresses highlights naturally, like film. AgX (added in 4.0) is an even better tone mapper. Raw is linear (blown-out highlights).
- **Exposure/Gamma:** Quick brightness/contrast adjustment. Prefer adjusting lighting over using these.

### Output Format
- For stills: **PNG** (lossless) or **OpenEXR** (16/32-bit floating point, for compositing)
- For animation: **EXR sequences** for compositing, **FFmpeg video** for quick previews
- Never render animation directly to a video file — if Blender crashes at frame 2000, you lose everything. Render image sequences, then compile to video

---

## Common Rendering Mistakes

### Fireflies (Bright Pixel Artifacts)
**Cause:** High-variance path tracing — occasionally a ray finds an extremely bright path (caustic, small bright light, sharp reflection).
**Fix:** `Render Properties → Light Paths → Clamp → Indirect Light: 10` (or 5–15). Also check for any Emission materials with very high Strength values.

### Noise / Grainy Image
**Cause:** Insufficient samples, or a difficult scene (small lights, complex indirect paths).
**Fix:** Increase samples. Enable adaptive sampling. Check light path settings. Make lights larger (larger lights = faster noise convergence). Enable denoising.

### Dark/Black Render in EEVEE
**Cause:** No World lighting, no lights in the scene, or lights on a hidden collection.
**Fix:** Add an HDRI to the World shader, add lights, check collection visibility in View Layer.

### Pink Textures
**Cause:** Blender can't find the image file (moved, renamed, or never packed).
**Fix:** `File → External Data → Find Missing Files`. Or `File → External Data → Pack Resources` to embed all images.

### Materials Look Different in EEVEE vs Cycles
**This is expected.** EEVEE is an approximation. Specific differences:
- Transmission (glass) looks very different — EEVEE requires `Render Properties → Screen Space Reflections` enabled and the material in `Blend Mode: Alpha Hashed`
- Subsurface scattering quality differs significantly
- Complex multi-bounce reflections are not present in EEVEE
- Some shader nodes (Volume Scatter, Holdout, some OSL) don't work in EEVEE

### Black Shadows on EEVEE
**Cause:** Shadow distance too small, or shadow cascade resolution too low.
**Fix:** Increase Shadow Distance in EEVEE render settings. Increase Cube Shadow Map resolution (for point/spot lights).
