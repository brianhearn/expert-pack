---
id: blender-3d/concepts/animation-drivers
title: "Animation — Drivers"
type: concept
tags:
  - animation
  - drivers
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/animation-rigging.md
related:
  - animation-nla.md
  - animation-data-model.md
  - animation-shape-keys.md
content_hash: sha256:0b73198cd48e6bf49df850cc1d736ba01bc4a911514bbf7d33d7554a78f98e0e
---

# Animation — Drivers

Drivers link a property to another property or a Python expression instead of to time. Use them for reactive relationships (shape key from bone rotation, wheel from travel); use keyframes for time-based acting.

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

