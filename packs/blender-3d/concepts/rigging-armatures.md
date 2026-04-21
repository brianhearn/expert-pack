---
id: blender-3d/concepts/rigging-armatures
title: "Rigging — Armatures, Constraints, IK/FK, and Weight Painting"
type: concept
tags:
  - rigging
  - armatures
  - ik
  - weight-paint
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
  - animation-shape-keys.md
---

# Rigging — Armatures, Constraints, IK/FK, and Weight Painting

---

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

## IK vs FK — When to Use Each

**FK (Forward Kinematics):** Default. Rotate the upper arm → the forearm follows. Natural for arcs — swings, reaching up.

**IK (Inverse Kinematics):** Plant the hand in space, the chain solves automatically. Natural for:
- Feet on ground (planted as character moves)
- Hands grabbing a fixed object
- Any time the endpoint needs to be in a specific world position

**IK setup:**
1. Create a control bone at the hand position (no deform, no parent)
2. Add IK constraint to the wrist bone → target = the control bone
3. Set chain length (how many bones the IK solver affects)
4. Create a Pole Target bone to control elbow direction

**IK/FK switching:** Professional rigs have both, with a custom property (0=IK, 1=FK) driving the IK constraint's influence.

**IK Pole Angle:** The pole target tells the IK solver which way the elbow/knee should point. The `Pole Angle` value in the IK constraint requires trial and error to get right.

---

## Weight Painting

Weight Paint Mode paints vertex weights — the influence of each bone on each vertex (0.0 to 1.0). Red = full influence, Blue = none.

### Automatic Weights (Starting Point)

With mesh selected, also select the armature (`Shift+click`), then `Ctrl+P → With Automatic Weights`. Calculates weights based on proximity. Almost never perfect but gives a starting point.

**Failure cases:** Open mesh boundaries, non-manifold geometry, very complex hierarchies.

### Weight Painting Workflow

1. Select the mesh object
2. In Pose Mode, select the bone you want to paint weights for (sets which vertex group is active)
3. Switch to Weight Paint Mode

**Key brushes:**
- `Draw`: paint weight value
- `Blur`: smooth weight transitions between vertices — essential for clean deformation
- `Average`: average weights toward a center value

**Key settings:**
- `Strength`: brush opacity
- `Weight`: value being painted (0–1)
- `Auto Normalize`: keeps total vertex weights summed to 1.0 across all bones — always enable this

**Joints:** A joint (elbow, knee, shoulder) should have weights that feather across 4–8 vertex loops on each side for natural-looking deformation.

---

## Vertex Groups

Vertex Groups are what Weight Paint actually edits. Every bone in an armature that has a deform flag creates a vertex group on the mesh with the same name. The Armature Modifier reads these to deform the mesh.

Add/remove vertices from vertex groups in Edit Mode (Select → Assign/Remove in Vertex Groups panel).
