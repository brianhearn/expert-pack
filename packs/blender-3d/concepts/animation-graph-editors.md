---
id: blender-3d/concepts/animation-graph-editors
title: "Animation — Dope Sheet, Graph Editor, and 4.x Changes"
type: concept
tags:
  - animation
  - graph-editor
  - dope-sheet
  - f-curves
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/animation-rigging.md
related:
  - animation-data-model.md
  - animation-nla.md
content_hash: sha256:4d5509bd99323273631e4fde4e6f9be172d4e3dfca48664f35592e60df161277
---

# Animation — Dope Sheet, Graph Editor, and 4.x Changes

The Dope Sheet shows keyframes as dots on a timeline; the Graph Editor edits the F-Curves between them. Handle type, extrapolation, and F-Curve modifiers (Cycles, Noise) control timing and looping. Blender 4.x replaced bone layers with Bone Collections.

## Dope Sheet

The Dope Sheet shows all keyframes across all channels as dots on a timeline.

**Essential operations:**
- `G` then `X`: slide keyframes left/right on the timeline
- `S` then `X`: scale selected keyframes in time (stretch or compress timing)
- `Box select`: select all keys in a range

**Dope Sheet modes** (dropdown in header):
- `Dope Sheet` — all keyframes in the scene
- `Action Editor` — keyframes in the active Action only
- `Shape Key Editor` — shape key values only

---

## Graph Editor — F-Curve Editing

Y axis = property value. X axis = frame number. A flat horizontal line = constant value. A bezier S-curve = smooth ease-in/ease-out.

**Handle types** (toggle with `V`):
- `Free` — both handles movable independently
- `Aligned` — both handles stay collinear (default for bezier keys)
- `Vector` — handles point toward adjacent keyframes (linear interpolation)
- `Auto` — Blender automatically computes smooth handles
- `Auto Clamped` — Auto, but prevents overshoot

**Extrapolation** (what happens outside the keyframe range):
- `Constant` — value holds at first/last keyframe value (default)
- `Linear` — continues on the slope of the first/last segment
- `Make Cyclic` — repeats the animation curve

**The Cycle modifier:** Better than extrapolation for most cyclic animation. Add via `Modifiers → Cycles`. Lets you set repeat count and blend at loop points. Essential for walk cycles.

**F-Curve Modifiers** (Sidebar `N` → Modifiers tab):
- `Noise` — adds procedural noise (camera shake, organic variation)
- `Cycles` — loops the curve
- `Stepped` — quantizes values to steps (robot motion, pixel art style)
- `Limits` — clamps output to a min/max range

**Camera shake setup:** Select all camera location/rotation curves, add Noise modifier, adjust Scale (timing frequency) and Strength.

---

## Blender 4.x Animation Changes

**Bone Collections (4.0+):** Replaced the 32-layer system. Bones are now organized into named, nestable collections. The old `layer` attribute in Python is now `collections`.

**Rotation Mode:** Blender 4.x encourages Quaternion rotation for rigging (no Gimbal lock) and Euler for user-facing controls.

**Bake Action (for export):** Use `Object → Animation → Bake Action` to bake constraint/IK results to pure keyframes. Required before exporting to FBX/GLTF for game engines.

