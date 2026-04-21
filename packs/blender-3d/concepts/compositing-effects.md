---
id: blender-3d/concepts/compositing-effects
title: "Compositing — Common Effects Nodes"
type: concept
tags:
  - compositing
  - effects
  - glare
  - depth-of-field
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-04-21"
verified_by: agent
supersedes:
  - concepts/compositing.md
related:
  - compositing-core.md
  - compositing-color-grading.md
---

# Compositing — Common Effects Nodes

---

## Depth of Field (Post-Process)

Post-process DoF is faster to adjust than render-level DoF but uses a screen-space approximation (can bleed bright objects over dark backgrounds):

```
[Render Layers Image] → Defocus node
[Render Layers Depth Z] → [Defocus Z input]
```

Enable `Use Z-Buffer` in the Defocus node for best results. Set `fStop` to match camera focal settings, or use raw pixel blur.

**Limitation:** The `Defocus` node doesn't handle transparency correctly. For final renders, prefer camera-level DoF in Cycles (physically accurate, handles transparent geometry — but slow).

---

## Glare (Bloom and Streaks)

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
- `Threshold`: Only glare pixels brighter than this value. Set high (>1.0 in HDR) to only affect genuinely bright lights.
- `Size`: Glow radius (in powers of 2)
- `Quality`: Computation quality (High = slow but better)
- `Iterations` (Streaks): Number of streak arms
- `Angle Offset` (Streaks): Rotation per iteration

**EEVEE 4.2+ note:** The Bloom render property was removed in EEVEE Next. Replace it with a `Glare` node (Bloom type) in the compositor with the realtime compositor enabled.

---

## Shadow Pass Usage

The shadow pass shows where shadows fall as a dark value. To change shadow color or intensity:

```
[Shadow pass] → Color Balance (change shadow tint) → Mix (Multiply mode with Diffuse Direct)
```

Or to add tinted shadows (artistic look):
```
[Shadow pass] → Color Balance (set lift to blue tint) → Add to scene → Composite
```

---

## File Output Node

Use the `File Output` node for automated multi-pass output. Add multiple sockets (one per pass) and set individual output paths and formats.

Supports:
- EXR (multilayer, all passes in one file)
- PNG/JPEG (per-pass separate files)
- OpenEXR multilayer is the professional standard

Enables one-render → multiple output files in different formats.
