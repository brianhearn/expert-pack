---
id: blender-3d/concepts/shading-engines
title: "Rendering — EEVEE vs Cycles and Render Settings"
type: concept
tags:
  - rendering
  - eevee
  - cycles
  - render-settings
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-04-21"
verified_by: agent
supersedes:
  - concepts/shading-rendering.md
related:
  - shading-materials.md
  - compositing-core.md
---

# Rendering — EEVEE vs Cycles and Render Settings

---

## EEVEE vs Cycles — When to Use Each

### Use EEVEE When:
- Speed is critical — product visualization, motion graphics, broadcast
- Real-time preview matters — iterating on look development
- Stylized output — EEVEE's rasterization can be art-directed
- Grease Pencil — fundamentally designed for EEVEE
- Arch-viz previsualization — before committing to a full Cycles render

### Use Cycles When:
- Photorealism is the goal — product photography replacement, VFX plates
- Transparent/refractive materials — glass, water, gemstones (EEVEE's screen-space reflections miss offscreen objects)
- Caustics — light focusing through glass (EEVEE can't do this)
- Complex indirect lighting — Global illumination is physically correct in Cycles; EEVEE approximates
- Subsurface scattering — skin, wax, marble (Cycles is accurate; EEVEE Next approximates)
- Final frames for client delivery — when quality is non-negotiable

**The practical answer:** Do look development in EEVEE (fast iteration), switch to Cycles for final renders.

---

## EEVEE Next (Blender 4.2+)

EEVEE was completely rewritten in Blender 4.2 as "EEVEE Next." Key improvements:
- Ray-traced shadows (GPU-accelerated) — dramatically better than old shadow maps
- Screen-space global illumination (SSGI) — better color bleed and indirect lighting
- Improved subsurface scattering
- Better volumetric shadows
- GPU-only rendering — EEVEE Next requires a GPU

**Remaining EEVEE limitations (even Next):**
- Screen-space reflections miss anything offscreen or behind the camera
- No true global illumination — indirect light is approximated
- Volume rendering is less accurate than Cycles
- Some complex shader node combinations don't work the same as in Cycles

### EEVEE Next Migration Gotchas (upgrading from < 4.2)

**World Volume Blocks Distant Light:** World volume shaders now completely block sun lights. Old scenes with world volume + sun light will render dark or black. Fix: convert the volume to a physical mesh object.

**Shadow System Rewritten:** Sun light shadow resolution settings cannot be auto-converted. The new `Resolution Limit` replaces per-light resolution. "Shadow buffer full" errors or massive performance drops can occur. Contact Shadows are **removed entirely**.

**Bloom Removed:** Replaced by the realtime compositor `Glare` node (Bloom type). Any tutorial showing Render Properties > Bloom is outdated for 4.2+.

**Material Blend Mode → Render Method:** "Blend Mode" is replaced by "Render Method." Simple materials auto-convert; complex mixed-alpha setups need manual conversion.

---

## Cycles: GPU and Performance

### GPU Rendering

Configure in `Edit → Preferences → System → Cycles Render Devices`:

| GPU Backend | For |
|-------------|-----|
| CUDA | Older NVIDIA (GTX 900 series through RTX 20xx) |
| OptiX | NVIDIA RTX series — hardware ray tracing; significantly faster |
| HIP | AMD GPUs (RX 5000+) |
| Metal | Apple Silicon (M1/M2/M3) and AMD Mac GPUs |

Enable GPU render: `Render Properties → Render Device → GPU Compute`.

### Key Cycles Render Settings

**Samples:**
- Viewport: 32–64 samples for previews
- Render: 256–1024 for most scenes; noisy environments need 1000+
- Adaptive Sampling stops sampling each pixel when it converges — dramatically reduces render times

**Denoising:**
- **OpenImageDenoise (OIDN):** CPU-based, very high quality, works on any machine
- **OptiX Denoiser:** NVIDIA-only, very fast GPU denoising, slightly lower quality
- For animation: temporal denoising in DaVinci Resolve or NeatVideo is better than per-frame Blender denoising

**Light Paths:**
- For most scenes: Total 12, Diffuse 4, Glossy 4, Transmission 12
- For interior scenes or complex glass: increase Transmission and Total bounces
- `Render Properties → Light Paths → Clamp → Indirect Light: 10` — eliminates fireflies at the cost of slight energy loss. Set this early.

---

## Render Settings That Matter

**Film Settings:**
- **Exposure:** Adjusts overall brightness non-destructively.
- **Transparent Background:** Renders alpha channel for compositing. `Film → Transparent`.
- **Filter Size:** Anti-aliasing filter size.

**Output Format:**
- For stills: **PNG** (lossless) or **OpenEXR** (16/32-bit, for compositing)
- For animation: **EXR sequences** for compositing, **FFmpeg video** for quick previews
- Never render animation directly to a video file — if Blender crashes at frame 2000, you lose everything. Render image sequences, then compile to video.

---

## Common Rendering Mistakes

### Fireflies (Bright Pixel Artifacts)
**Cause:** High-variance path tracing — occasionally a ray finds an extremely bright path.
**Fix:** `Render Properties → Light Paths → Clamp → Indirect Light: 10`. Check for Emission materials with very high Strength values.

### Noise / Grainy Image
**Fix:** Increase samples. Enable adaptive sampling. Make lights larger (larger lights = faster noise convergence). Enable denoising.

### Dark/Black Render in EEVEE
**Fix:** Add an HDRI to the World shader, add lights, check collection visibility in View Layer.

### Pink Textures
**Cause:** Blender can't find the image file (moved, renamed, or never packed).
**Fix:** `File → External Data → Find Missing Files`. Or `File → External Data → Pack Resources`.

### Materials Look Different in EEVEE vs Cycles
This is expected. Key differences:
- Transmission (glass) requires `Render Properties → Screen Space Reflections` enabled and material in `Blend Mode: Alpha Hashed`
- Subsurface scattering quality differs
- Complex multi-bounce reflections are not present in EEVEE
