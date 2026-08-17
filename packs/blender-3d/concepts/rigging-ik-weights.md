---
id: blender-3d/concepts/rigging-ik-weights
title: "Rigging — IK vs FK, Weight Painting, and Vertex Groups"
type: concept
tags:
  - rigging
  - ik
  - weight-paint
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/animation-rigging.md
related:
  - rigging-armatures.md
  - animation-shape-keys.md
content_hash: sha256:066061954b4870a97fd807f2a024aba463787998814faab2ca8a6879e6c04e55
---

# Rigging — IK vs FK, Weight Painting, and Vertex Groups

FK rotates a parent and children follow; IK plants an endpoint and solves the chain backward. Weight painting assigns per-vertex bone influence — vertex groups the Armature Modifier reads. Auto-normalize and feathered joint weights prevent collapsing deformation.

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

