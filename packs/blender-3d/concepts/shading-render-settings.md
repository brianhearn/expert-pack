---
id: blender-3d/concepts/shading-render-settings
title: "Rendering — Output Settings and Common Mistakes"
type: concept
tags:
  - rendering
  - render-settings
  - output
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/shading-rendering.md
related:
  - shading-eevee.md
  - shading-cycles.md
  - compositing-core.md
content_hash: sha256:e8bea01d0a81b8a95a878c12d4adc3085a2f4fdddbc392d16494d1e302573934
---

# Rendering — Output Settings and Common Mistakes

Film exposure, transparent background, and output format determine whether a render is usable in compositing. Fireflies, grain, pink textures, and EEVEE-vs-Cycles material mismatch each have a specific cause and fix.

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

