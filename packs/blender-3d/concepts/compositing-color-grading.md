---
id: blender-3d/concepts/compositing-color-grading
title: "Compositing — Color Management and Color Grading"
type: concept
tags:
  - compositing
  - color-grading
  - agx
  - filmic
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
  - compositing-effects.md
---

# Compositing — Color Management and Color Grading

---

## Color Management — Filmic and AgX

**The pipeline:**
```
Scene Linear (render calculations) → View Transform → Display Output
```

Set in `Render Properties → Color Management`.

### View Transforms

| Transform | Behavior | Use When |
|-----------|----------|----------|
| AgX | Best tone mapper — natural highlight rolloff, no hue shift in bright areas. Default in 4.0+ | Current standard recommendation |
| Filmic | Very good — was default before AgX. Slightly more "cinematic" contrast | Backward compat, personal preference |
| Raw | No tone mapping — highlights blow out | When you control tone mapping externally |
| False Color | Debug tool — shows exposure levels as false colors | Evaluating exposure |

**AgX vs Filmic:** AgX has better chromatic accuracy in highlights. A bright orange light won't hue-shift toward yellow/white (as Filmic would). For most work, prefer AgX in Blender 4.x.

### Look Presets

Under the View Transform, `Look` adjusts contrast curves on top of the tone mapper:
- None, Very Low Contrast, Low Contrast, Medium High Contrast, High Contrast, Very High Contrast
- `Medium High Contrast` with AgX is a solid default for product visualization

### Exposure and Gamma

- `Exposure`: Global brightness in linear space. +1 = double brightness. Prefer adjusting lights/world over this.
- `Gamma`: Power curve on the output. Don't use for correction — use Color Balance instead.

---

## Color Grading — Standard Node Setup

```
[Render Layers] → Denoise → Color Balance → Hue Saturation Value → Composite
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

**Classic orange-and-teal look (Lift/Gamma/Gain):**
- Lift: Slight cyan tint (RGB: 0.9, 1.0, 1.1)
- Gain: Slight warm tint (RGB: 1.1, 1.0, 0.9)
- Gamma: Lift midtones slightly

---

## Vignette Setup

No dedicated node. Achieve with an Ellipse Mask and Color Balance:

```
[Ellipse Mask] → Blur (high value) → Invert → Mix (Multiply mode) → Composite
                                                     ↑ Image input
```

---

## Lens Distortion

Adds barrel/pincushion distortion like a real lens:

```
[Render Layers] → Lens Distortion → Composite
```

Settings:
- `Distortion`: -0.1 to +0.1 for subtle barrel (negative) or pincushion (positive)
- `Dispersion`: Chromatic aberration (color fringing). Very subtle (0.01–0.05) for realism.
- `Jitter`: Add subtle noise to avoid patterned artifacts

---

## Working with Video Input

1. `Input → Movie Clip` node — loads a video file
2. Process through nodes (color grade, denoise, etc.)
3. Output to `Composite` node
4. Render in `Output Properties` with image/video format

For motion tracking: the Movie Clip Editor tracks footage, which feeds into the compositor via `Input → Movie Clip` with the track data accessible via `Tracking`. This is how Blender does basic VFX compositing (3D object tracked and composited onto real footage).
