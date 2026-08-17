---
id: blender-3d/concepts/rigging-armatures
title: "Rigging — Armatures and Constraints"
type: concept
tags:
  - rigging
  - armatures
  - constraints
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/animation-rigging.md
related:
  - rigging-ik-weights.md
  - animation-data-model.md
  - animation-shape-keys.md
content_hash: sha256:d368ae7143ac4501b254e576f9ac39cb6fb27ef88559069cbdda0f54f1dbb61d
---

# Rigging — Armatures and Constraints

An Armature is a bone hierarchy that deforms a mesh through the Armature Modifier. Constraints copy transforms, limit motion, or solve IK; naming prefixes (`DEF_`, `MCH_`, `L_`/`R_`) keep production rigs readable.

## Armature Basics

An **Armature** is a Blender object containing bones. Bones form a hierarchy (parent-child). The Armature deforms mesh objects via the **Armature Modifier**.

**Bone anatomy:**
- **Head** — start of the bone (parent connection point)
- **Tail** — end of the bone (where child bones connect from)
- **Roll** — rotation around the bone's Y axis
- **Connected** — when a child bone's head is merged with parent's tail

### Building an Armature

In Edit Mode on the Armature object:
- `E` from a bone's tail: extrude a new connected child bone
- `Shift+A`: add a disconnected bone at cursor location
- `Ctrl+P`: set parent; `Alt+P`: clear parent

**Naming convention:** Use a prefix system — `L_`/`R_` for left/right, `ORG_` for original deform bones, `MCH_` for mechanism bones (no deform), `DEF_` for deform bones.

**Bone Collections (4.0+):** Replaced the old 32-layer system. Organize control bones, deform bones, and helper bones into named collections with toggle visibility.

---

## Constraints

Key constraints:

| Constraint | Use |
|------------|-----|
| Copy Location / Rotation / Scale | Makes a bone follow another object/bone's transform |
| Track To | Bone Y+ axis always points at a target |
| Stretch To | Stretches bone toward a target (elastic limbs) |
| IK (Inverse Kinematics) | Solve chain to reach a target |
| Limit Rotation | Clamp rotation to a range (prevents knee bending backward) |
| Damped Track | Like Track To but smoother for follow-through |
| Child Of | Makes a bone a "child" of another object (weapon pick-up) |
| Action | Drives a specific Action based on a bone's rotation |

---

