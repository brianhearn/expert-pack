---
id: blender-3d/concepts/animation-nla-drivers
title: "Animation — NLA Editor and Drivers"
type: concept
tags:
  - animation
  - nla
  - drivers
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-04-21"
verified_by: agent
supersedes:
  - concepts/animation-rigging.md
related:
  - animation-data-model.md
  - rigging-armatures.md
---

# Animation — NLA Editor and Drivers

---

## NLA Editor — Non-Linear Animation

The NLA (Non-Linear Animation) Editor treats Actions as clips that can be stacked, blended, and sequenced.

### Workflow

1. Create and finalize an Action in the Graph Editor
2. In the NLA Editor, click **Push Down** (down arrow icon) next to the action name — this pushes the active Action down to an NLA strip
3. The Action now exists as a strip in the NLA track
4. Create a new Action, push it down — repeat
5. NLA strips can be overlapped, scaled, and blended

### NLA Strips

**Strip operations:**
- `Tab` on a strip: enter it and edit the underlying Action
- `G`: slide in time
- `S`: scale (stretch/compress timing)
- `N` panel: strip properties — start/end frame, blend type, influence

**Blend types:** Replace (default, override), Add, Subtract, Multiply, Combine

**Blending:** Two overlapping strips can blend using their influence. An idle animation (100% influence) + "breathing" action (30% influence) = natural layering.

**Tweak Mode:** `Tab` on a selected NLA strip enters Tweak Mode, opening the strip's underlying Action for editing. Exit with `Tab` again.

### NLA for Game Engines

Standard workflow for preparing animations for Unity/Unreal export via FBX:
1. All animations are separate named Actions
2. Each Action is pushed down to the NLA as strips
3. Export with `NLA Strips as Clips` or bake all strips to individual actions
4. Game engine imports each Action as a separate animation clip

---

## Drivers — Property-Driven Animation

Drivers link one property to another (or to a Python expression) rather than to time.

### When to Use Drivers (vs Keyframes)

| Use Drivers | Use Keyframes |
|-------------|---------------|
| Shape key controlled by bone rotation | Facial expression keyed by animator |
| Wheel rotation tied to truck movement | Character walk cycle |
| Procedural material intensity linked to object proximity | Light brightness animating over time |
| Custom rig control widgets | General body movement |
| Any "reactive" relationship between properties | Any time-based animation |

### Creating a Driver

- Right-click any property → `Add Driver`
- Or: `Ctrl+D` on a property
- Or: In Graph Editor, switch to Drivers mode (dropdown in header)

**Driver types:**
- `Averaged Value` — average of all variables (most common for single-variable drivers)
- `Scripted Expression` — arbitrary Python expression (most powerful)
- `Min/Max of Values` — take the min or max from multiple variables

**Variable types:**
- `Single Property` — read any property from any object/bone
- `Rotation Difference` — angle between two bones (excellent for corrective shapes)
- `Distance` — distance between two objects or bones
- `Transform Channel` — a specific transform from a specific object/bone

### Driver Expression Examples

```python
# Remap 0-90 degree bone rotation to 0-1 shape key value
var / 90

# Clamp to 0-1 range
max(0, min(1, var))

# Smooth step (ease in/out) for cleaner transitions
3*var**2 - 2*var**3

# Absolute value (useful for bilateral symmetry drivers)
abs(var)

# Check distance and activate above threshold
max(0, var - 0.5) * 2  # activates when var > 0.5
```

**Corrective shape keys via Rotation Difference:** The most common professional driver setup. A knee or elbow bends, the mesh collapses. Create a corrective shape key that fixes the collapse; add a driver with Rotation Difference between the upper and lower limb bones. The shape key activates as the joint bends.
