---
id: blender-3d/concepts/animation-data-model
title: "Animation — Data Model and Keyframing"
type: concept
tags:
  - animation
  - keyframes
  - actions
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
  - animation-graph-editors.md
  - animation-nla.md
  - animation-drivers.md
  - rigging-armatures.md
content_hash: sha256:33cdd669ecdeaba21a42380e6ee190924d557cec503516497432fbb439795989
---

# Animation — Data Model and Keyframing

Blender animation is a chain: a property's F-Curve lives in an Action, and Actions become NLA strips. Keyframes record property values over time; the active Action is what the Graph Editor and auto-key actually edit.

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

