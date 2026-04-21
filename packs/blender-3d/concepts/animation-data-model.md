---
id: blender-3d/concepts/animation-data-model
title: "Animation — Data Model, Keyframing, and Graph Editor"
type: concept
tags:
  - animation
  - keyframes
  - graph-editor
  - f-curves
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-04-21"
verified_by: agent
supersedes:
  - concepts/animation-rigging.md
related:
  - animation-nla-drivers.md
  - rigging-armatures.md
  - animation-shape-keys.md
---

# Animation — Data Model, Keyframing, and Graph Editor

---

## The Animation Data Model

**The chain:** Object/Bone property → F-Curve → Action → NLA strip → Final transform

- An **F-Curve** is a single animated property — one curve for X location, one for Y, one for Z, etc.
- A set of F-Curves grouped together is an **Action** — a "clip" named and saved
- An object has one **Active Action** at a time (shown in the Action Editor dropdown)
- Actions pushed down to the **NLA Editor** become strips that can be blended, sequenced, and layered

**Critical implication:** Recording keyframes in the Graph Editor edits the *active Action*. Switching the active Action by clicking a different one creates keyframes in that Action. People accidentally create dozens of Actions named "Action.001", "Action.002" this way.

**Action users:** Actions have user counts. An Action with no users will be purged on save. Set Fake User (`F` in the Action dropdown) on Actions you want to keep.

---

## Keyframing Workflow

### Inserting Keyframes

`I` in the 3D Viewport opens the Insert Keyframe menu:

| Option | What It Keys |
|--------|-------------|
| Location | X, Y, Z position |
| Rotation | Rotation (whichever mode the object uses) |
| Scale | X, Y, Z scale |
| Location, Rotation & Scale | All nine channels |
| Visual Location | Actual viewport position (for constrained objects) |
| Available | Only properties that already have keyframes |

**Visual Keying vs. Regular Keying:** When an object is constrained, its transform channels reflect the *pre-constraint* values. `Visual Keying` bakes the *visual* position — what you actually see. Use Visual Keying when baking constraint animations or finalizing IK poses to FK.

**Auto-Keying:** Enable with the red dot button in the Timeline header. Any change to an object/bone property automatically creates a keyframe. Pairs well with `Replace` mode (only keys properties that already have keyframes) vs `Add & Replace` (keys everything you touch).

### Keyframe Types

Right-click a keyframe to change type:

| Type | Behavior |
|------|----------|
| Keyframe (Bezier) | Smooth in/out interpolation. Default. |
| Linear | Constant velocity between keys. Good for mechanical motion. |
| Constant | Holds value until next keyframe, then snaps. Good for on/off switches. |

---

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
