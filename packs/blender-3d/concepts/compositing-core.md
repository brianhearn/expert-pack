---
id: blender-3d/concepts/compositing-core
title: "Compositing — Core Setup and Denoising"
type: concept
tags:
  - compositing
  - denoising
  - render-passes
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-04-21"
verified_by: agent
supersedes:
  - concepts/compositing.md
related:
  - compositing-color-grading.md
  - compositing-effects.md
  - shading-engines.md
---

# Compositing — Core Setup and Denoising

Blender's Compositor is a node-based post-processing system operating on render output, render passes, and imported images/video. Its power is in multi-pass compositing — separating a render into diffuse, shadow, reflection, and depth components and recombining them with independent control.

---

## The Compositor vs Viewport Compositor

**Compositor (classic):** Node graph accessed via the Compositing workspace. Runs after `F12` (render). Enable with `Use Nodes` checkbox.

**Viewport Compositor (Blender 4.0+):** Real-time compositor in the 3D Viewport. Enable per-viewport in `Viewport Shading → Compositor → Camera`. Limited node support but useful for real-time color grading preview. Not a replacement for the full compositor.

---

## The Render Layer Node

The primary input is the **Render Layers** node (`Shift+A → Input → Render Layers`). Default outputs:
- `Image` — final combined render
- `Alpha` — transparency mask
- `Depth` (Z) — distance from camera per pixel

Enable render passes in View Layer Properties → Passes:
- `Diffuse Direct/Indirect`, `Specular Direct/Indirect`, `Emission`, `Environment`, `Shadow`, `AO`
- `Normal`, `Position` — surface/world data
- `Cryptomatte` — ID masks for objects and materials
- `Denoising Data` — albedo and normals for OpenImageDenoise

### Standard Minimal Node Setup

```
[Render Layers] → Denoise → [Color Balance] → [Glare] → [Composite]
                              ↓
                           [Viewer]
```

- `Denoise`: Remove Cycles noise. Connect `Image`, `Normal` (Denoise Normal pass), `Albedo` (Denoising Albedo pass)
- `Color Balance`: Basic color grading
- `Glare`: Bloom/flare effects
- `Composite`: Required output node — compositor does nothing without it
- `Viewer`: Preview any intermediate step in the Image Editor

---

## Denoising in the Compositor

### Render Pass Denoising (Recommended)

Denoise individual render passes separately then recombine — preserves detail in bright areas that combined denoising can blur.

**Enable passes:** View Layer Properties → Passes → Data: enable `Denoising Albedo` and `Denoising Normal`.

**Denoise node setup:**
```
[Render Layers] → Denoise → ...
  Denoising Normal ↗
  Denoising Albedo ↗
```

**Denoise node settings:**
- `HDR Mode`: Enable for high-dynamic-range images. Generally leave enabled.
- `Prefilter`: `None` (fastest), `Fast`, `Accurate` (best quality). For stills: Accurate. For animation: Fast.

### OptiX vs OpenImageDenoise

Set in `Render Properties → Sampling → Denoise`:
- **OpenImageDenoise (OIDN):** CPU-based, high quality, works on any machine. OIDN v2 in Blender 4.x is significantly better than older versions.
- **OptiX:** NVIDIA RTX GPU, very fast, slightly lower quality on complex scenes.

### Denoising Temporal Flicker (Animation)

Per-frame denoising can create a "swimming" look in fine details across frames. Fixes:
1. More samples per frame (reduces noise)
2. Use OptiX temporal denoising if available
3. Post-process with DaVinci Resolve's Temporal Noise Reduction or NeatVideo
4. Increase `Temporal` in OIDN settings when available

---

## Render Passes and Multi-Pass Compositing

Multi-pass compositing is the professional approach.

**The classic recombination:**
```
Diffuse Direct + Diffuse Indirect = Total Diffuse
Specular Direct + Specular Indirect = Total Specular
Total Diffuse + Total Specular + Emission + Environment = Reconstructed Image
```

By separating passes, you can boost reflections without affecting diffuse, change shadow color, remove environment noise without touching character passes, and adjust AO intensity separately.

### Cryptomatte — Object/Material Isolation Masks

Cryptomatte generates object isolation masks directly from a render — accurate edge anti-aliasing included.

**Enable:** View Layer Properties → Passes → `Cryptomatte Object` and `Cryptomatte Material`.

**Usage:**
1. Add `Cryptomatte` node (`Shift+A → Matte → Cryptomatte`)
2. Connect Render Layers `Image` and the crypto passes
3. Click `Pick`, then click any object in the rendered image
4. The Cryptomatte node outputs a `Matte` with a perfect edge-antialiased mask

This replaces the old manual "Object Index" pass workflow and is dramatically better at edges.

---

## OpenEXR Multilayer — The Pro Format

OpenEXR multilayer stores multiple render passes in a single file with 32-bit floating point precision. Lossless. Large files.

**When to use EXR:**
- Any project requiring compositing over multiple sessions
- When you might need to re-composite without re-rendering
- When client deliverables require raw passes

**When PNG is fine:**
- Personal projects, quick renders
- Final delivery only (not meant for compositing)

---

## GPU Compositing (4.x)

Enable in `Preferences → System → GPU Compositing`. With a capable GPU, compositing can be 5–20× faster. Most core nodes (Denoise with OptiX, Blur, Glare, Color Balance, Mix) have GPU support. Some matte operations remain CPU-only.
