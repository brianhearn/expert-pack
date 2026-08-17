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
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/compositing.md
related:
  - compositing-passes-exr.md
  - compositing-color-grading.md
  - compositing-effects.md
  - shading-cycles.md
content_hash: sha256:fa4d2d7df6345f075d2f88faf6fbc865e49101091be9461be7dc9ea94b03a68e
---

# Compositing — Core Setup and Denoising

Blender's Compositor is a node-based post-processing system operating on render output, render passes, and imported images/video. Its power is in multi-pass compositing — separating a render into diffuse, shadow, reflection, and depth components and recombining them with independent control.

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

