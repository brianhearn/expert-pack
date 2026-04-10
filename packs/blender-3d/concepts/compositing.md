---
title: Compositing
type: concept
tags:
- compositing
- concepts
pack: blender-3d
retrieval_strategy: standard
id: blender-3d/concepts/compositing
verified_at: '2026-04-10'
verified_by: agent
---

<!-- context: blender-3d/concepts/compositing -->

# Compositing

> **Lead summary:** Blender's Compositor is a node-based post-processing system that operates on render output, render passes, and imported images/video. It runs after rendering (or in real-time with EEVEE via the Viewport Compositor in 4.x). Its power is in multi-pass compositing — separating a render into diffuse, shadow, reflection, and depth components and recombining them with independent control. Most users underuse it; professional renders almost always require at least denoising, color grading, and glare passes.

---

## The Compositor vs Viewport Compositor

**Compositor (classic):** The node graph accessed via the Compositing workspace or any editor set to Compositor type. Runs after `F12` (render), or on imported images. Results appear in the Image Editor.

**Viewport Compositor (Blender 4.0+):** A real-time compositor that runs in the 3D Viewport on the viewport display. Enable per-viewport in `Viewport Shading → Compositor → Camera`. Limited node support but very useful for real-time color grading preview during lighting. Not a replacement for the full compositor.

**The flow:**
```
Render → Compositor (nodes) → Output (image/video/viewer)
```

Enable the Compositor: `Compositing workspace → Use Nodes checkbox`.

---

## Essential Setup: The Render Layer Node

The Compositor's primary input is the **Render Layers** node (`Shift+A → Input → Render Layers`). It outputs the rendered image plus all enabled render passes.

**Default outputs:**
- `Image` — final combined render (all passes composited by Blender's internal pipeline)
- `Alpha` — transparency mask
- `Depth` (Z) — distance from camera per pixel (in world units)

**Enabled passes (set in View Layer Properties → Passes):**
- `Diffuse Direct/Indirect` — direct/indirect light on diffuse surfaces
- `Specular Direct/Indirect` — reflections
- `Emission` — emissive surfaces
- `Environment` — background/HDRI only
- `Shadow` — shadow contribution
- `AO (Ambient Occlusion)` — AO pass
- `Normal` — surface normals
- `Position` — world-space position (very useful for depth-based effects)
- `Cryptomatte` — ID masks for objects, materials (see below)
- `Denoising Data` — albedo and normals needed for OpenImageDenoise

### Standard Node Setup (Clean Start)

A minimal professional compositor graph:

```
[Render Layers] → Denoise → [Color Balance] → [Glare] → [Composite]
                              ↓
                           [Viewer]
```

- `Denoise`: Remove noise from Cycles. Connect `Image`, `Normal` (from Denoise Normal pass), `Albedo` (from Denoising Albedo pass) inputs
- `Color Balance`: Basic color grading (Lift/Gamma/Gain or Offset/Power/Slope)
- `Glare`: Add lens bloom/flare effects
- `Composite`: The final output node — required for the compositor to do anything
- `Viewer`: Preview any intermediate step in the Image Editor

---

## Denoising in the Compositor

Denoising is one of the most important compositor tasks for Cycles renders.

### Render Pass Denoising (Recommended)

Rather than denoising the combined image, denoise individual render passes separately then recombine. This preserves detail in bright areas that combined denoising can blur.

**Enable Denoising passes:** In View Layer Properties → Passes → Data: enable `Denoising Albedo` and `Denoising Normal`.

**Denoise node setup:**
```
[Render Layers] → Denoise → ...
  Denoising Normal ↗
  Denoising Albedo ↗
```

**Denoise node settings:**
- `HDR Mode`: Enable when denoising high-dynamic-range images (compositor output before color management). Generally leave enabled.
- `Prefilter`: `None` (fastest), `Fast`, `Accurate` (best quality). For stills, use Accurate. For animation, Fast.

### OptiX vs OpenImageDenoise

Set in `Render Properties → Sampling → Denoise`:
- **OpenImageDenoise (OIDN):** CPU-based, works on any machine, high quality. The OIDN v2 in Blender 4.x is significantly better than older versions.
- **OptiX:** NVIDIA RTX GPU, very fast, slightly lower quality than OIDN on complex scenes.

For animation, OIDN can be parallelized across CPU cores but is inherently slow. For production animation denoising, many studios use temporal denoising in a dedicated compositor (DaVinci Resolve Noise Reduction, NeatVideo). These tools analyze multiple frames simultaneously, eliminating the temporal flickering that per-frame Blender denoising can produce.

### Denoising Temporal Flicker (Animation)

The problem: per-frame denoising changes which noise gets removed each frame, creating a "swimming" look in fine details. Fixes:
1. More samples per frame (reduces noise, reduces denoiser work)
2. Use OptiX temporal denoising if available
3. Post-process with DaVinci Resolve's Temporal Noise Reduction or NeatVideo
4. Increase `Temporal` in OIDN settings when available

---

## Color Management — Filmic and AgX

Color management in Blender controls how linear render values are displayed and output.

**The pipeline:**
```
Scene Linear (render calculations) → View Transform → Display Output
```

Set in `Render Properties → Color Management` or `Scene Properties → Color Management`.

### View Transforms

| Transform | Behavior | Use When |
|-----------|----------|----------|
| AgX | Best tone mapper — natural highlight rolloff, no color hue shift in bright areas. Default in 4.0+ | Current standard recommendation |
| Filmic | Very good — was the default before AgX. Slightly more "cinematic" contrast | Backward compat, personal preference |
| Raw | No tone mapping — pure linear output. Highlights blow out. | When you control tone mapping externally |
| False Color | Debug tool — shows exposure levels as false colors | Evaluating exposure |

**AgX vs Filmic:** AgX has better chromatic accuracy in highlights — highly saturated lights don't hue-shift (Filmic would shift a bright orange toward yellow/white; AgX maintains the orange hue longer before white). For most work, prefer AgX in Blender 4.x.

### Look Presets

Under the View Transform, `Look` adjusts contrast curves on top of the tone mapper:
- None, Very Low Contrast, Low Contrast, Medium High Contrast, High Contrast, Very High Contrast
- `Medium High Contrast` with AgX is a solid default for product visualization
- Reduce contrast for flat/matte looks, increase for dramatic/cinematic

### Exposure and Gamma

- `Exposure`: Global brightness in linear space. +1 = double brightness. Prefer adjusting lights/world over this.
- `Gamma`: Power curve on the output. 1.0 = neutral. >1 = brightens midtones. Don't use this for correction — use Color Balance instead.

---

## Render Passes and Multi-Pass Compositing

Multi-pass compositing is the professional approach: render each component separately, composite with full control.

### The Passes Workflow

1. In View Layer Properties → Passes, enable the passes you need
2. After rendering, each pass appears as a separate output on the Render Layers node
3. Recombine passes in the compositor with full per-pass control

**The classic recombination:**
```
Diffuse Direct + Diffuse Indirect = Total Diffuse
Specular Direct + Specular Indirect = Total Specular
Total Diffuse + Total Specular + Emission + Environment = Reconstructed Image
```

By separating these, you can:
- Boost reflections without affecting diffuse (Multiply node on specular pass)
- Change shadow color (Color Balance on shadow pass before adding)
- Remove environment noise without touching character passes
- Adjust AO intensity separately

### Shadow Pass Usage

The shadow pass shows where shadows fall as a dark value. To change shadow color or intensity:

```
[Shadow pass] → Color Balance (change shadow tint) → Mix (Multiply mode with Diffuse Direct)
```

Or to add tinted shadows (artistic look):
```
[Shadow pass] → Color Balance (set lift to blue tint) → Add to scene → Composite
```

### Cryptomatte — Object/Material Isolation Masks

Cryptomatte is the industry-standard method for generating object isolation masks from a render. Instead of rendering separate object masks, Cryptomatte encodes per-pixel object/material IDs using a hash-based system that resolves accurate edge anti-aliasing.

**Enable:** View Layer Properties → Passes → `Cryptomatte Object` and `Cryptomatte Material`.

**Usage in compositor:**
1. Add `Cryptomatte` node (`Shift+A → Matte → Cryptomatte`)
2. Connect the Render Layers `Image` and the crypto passes to the Cryptomatte node
3. Click `Pick` in the Cryptomatte node, then click any object in the rendered image
4. The Cryptomatte node outputs a `Matte` socket with a perfect edge-antialiased mask for that object

This replaces the old manual "Object Index" pass workflow and is dramatically better at edges.

---

## Common Node Setups

### Depth of Field (Post-Process)

Post-process DoF is faster to adjust than render-level DoF but uses a screen-space approximation (can bleed bright objects over dark backgrounds):

```
[Render Layers Image] → Defocus node
[Render Layers Depth Z] → [Defocus Z input]
                         ↑
Set fStop and MaxBlur in Defocus node settings
```

Enable `Use Z-Buffer` in the Defocus node for best results. Set `fStop` to match your camera's focal length setup, or use raw pixel blur amount.

**Limitation:** The `Defocus` node doesn't handle transparency correctly. The camera-level DoF in Cycles is physically accurate (handles transparent geometry, but is slow). For final renders, prefer camera-level DoF.

### Glare (Bloom and Streaks)

The Glare node adds lens glow, bloom, and streaks to bright areas.

```
[Render Layers] → Glare → Composite
```

**Glare types:**

| Type | Effect |
|------|--------|
| Bloom | Soft glow around bright areas. Best for natural light, emissive surfaces. |
| Ghosts | Lens ghost artifacts (aperture shapes). Cinematic lens effect. |
| Streaks | Star-burst streaks from bright points. |
| Fog Glow | Diffuse glow that spreads more uniformly. |

**Key settings:**
- `Threshold`: Only glare pixels brighter than this value. Set high (>1.0 in HDR) to only affect genuinely bright lights, not everything.
- `Size`: Glow radius (in powers of 2)
- `Quality`: Computation quality (High = slow but better)
- `Iterations` (Streaks): Number of streak arms
- `Angle Offset` (Streaks): Rotation per iteration

### Vignette Setup

No dedicated node — achieve it with an Ellipse Mask and ColorBalance:

```
[Ellipse Mask] → Blur (high value) → Invert → Mix (Multiply mode) → Composite
                                                     ↑ Image input
```

Or use a ColorBalance node's Lift (darkens black/shadows) to add darkness to edges — less precise but instant.

### Color Grading — Standard Setup

```
[Render Layers] → Denoise → Color Balance (basic grade) → Hue Saturation Value → Composite
```

**Color Balance node — two modes:**

Lift/Gamma/Gain (most intuitive):
- `Lift`: Affects shadows (add to base dark values)
- `Gamma`: Affects midtones (power curve)
- `Gain`: Affects highlights (multiplicative)

Offset/Power/Slope (industry standard CDL — compatible with professional grading software):
- `Offset`: Additive shift (all values)
- `Power`: Gamma (midtone curve)
- `Slope`: Multiplicative gain

Classic orange-and-teal look in Lift/Gamma/Gain:
- Lift: Slight cyan tint (RGB: 0.9, 1.0, 1.1)
- Gain: Slight warm tint (RGB: 1.1, 1.0, 0.9)
- Gamma: Lift midtones slightly

### Lens Distortion

Adds barrel/pincushion distortion like a real lens:

```
[Render Layers] → Lens Distortion → Composite
```

Settings:
- `Distortion`: -0.1 to +0.1 range for subtle barrel (negative) or pincushion (positive)
- `Dispersion`: Chromatic aberration (color fringing). Very subtle (0.01–0.05) for realism.
- `Jitter`: Add subtle noise to avoid patterned artifacts

---

## Working with Video Input

The compositor can process video files, not just renders:

1. `Input → Movie Clip` node — loads a video file
2. Process through nodes (color grade, denoise, etc.)
3. Output to `Composite` node
4. Render in `Output Properties` with an image/video format

For motion tracking: the Movie Clip Editor tracks footage, which feeds into the compositor via `Input → Movie Clip` with the track data accessible via `Tracking`. This is how Blender does basic VFX compositing (3D object tracked and composited onto real footage).

---

## Performance: CPU vs GPU Compositing

Blender's compositor historically ran on CPU only. Blender 4.0+ added GPU compositing for many nodes.

**Enable GPU compositing:** `Preferences → System → GPU Compositing`. With a capable GPU, compositing can be 5–20× faster.

**Nodes with GPU support (4.x):** Most core nodes including Denoise (on GPU with OptiX), Blur, Glare, Color Balance, Mix. Some nodes remain CPU-only — complex scripts, some matte operations.

**File output:** Use the `File Output` node for automated multi-pass output. Add multiple sockets (one per pass) and set individual output paths and formats. Enables one-render → multiple output files:

```python
# The File Output node supports:
# - EXR (multilayer, all passes in one file)
# - PNG/JPEG (per-pass separate files)
# - OpenEXR multilayer is the professional standard
```

---

## OpenEXR Multilayer — The Pro Format

OpenEXR multilayer stores multiple render passes in a single file with 32-bit floating point precision per channel. Lossless. Large file size.

**Workflow:**
1. In File Output node, set format to `OpenEXR Multilayer`
2. All connected inputs become layers in the EXR file
3. Open the EXR in compositor via `Input → Image` node → switch to EXR layer in the node's layer selector
4. Or use `Image → Split EXR to Multi-layer` to extract passes

**When to use EXR:**
- Any project requiring compositing over multiple sessions (most professional work)
- When you might need to re-composite without re-rendering
- When client deliverables require raw passes for their own compositing

**When PNG is fine:**
- Personal projects, quick renders
- Final delivery only (not meant for compositing)
- When file size and simplicity matter more than flexibility
