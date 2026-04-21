---
id: blender-3d/concepts/geometry-nodes-patterns
title: "Geometry Nodes — Common Patterns and Advanced Techniques"
type: concept
tags:
  - geometry-nodes
  - patterns
  - scatter
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-04-21"
verified_by: agent
supersedes:
  - concepts/geometry-nodes.md
related:
  - geometry-nodes-core.md
  - geometry-nodes-nodes-reference.md
---

# Geometry Nodes — Common Patterns and Advanced Techniques

Reusable patterns and advanced community-sourced techniques. For core concepts, see geometry-nodes-core.md.

---

## Pattern 1: Scatter Objects on a Surface

```
[Object Info: Source Object] ─→ [Distribute Points on Faces] ─→ [Instance on Points] ─→ [Group Output]
                                    ↑
                              [Group Input: Density]
```

Classic scatter: scatter points across a mesh, place instances at each point. Scale, rotation, and position can be randomized by feeding fields into Instance on Points.

**Key detail:** Use `Collection Info` instead of `Object Info` to scatter from a collection of multiple objects — GeoNodes will randomly pick from the collection for each point.

---

## Pattern 2: Deform Along a Curve

Use `Sample Curve` to get position and tangent along a curve at normalized positions, then use `Set Position` to move points to those positions. Creates a "curve deformer" similar to the Curve modifier but fully procedural.

---

## Pattern 3: Parametric Shape

Group Input → [construction math] → Group Output. Expose key dimensions (width, height, segment count) as Group Inputs. The shape recalculates automatically when modifier parameters change.

---

## Pattern 4: Procedural Variation

Connect `Index → Math (divide by total count) → position/scale/rotation input`. Creates per-instance variation that's deterministic and ordered. Combine with `Random Value` with a seed for chaotic variation.

---

## Advanced: Verlet Integration for Custom Rope/Soft Body

A pure Geometry Nodes alternative to Cloth/Soft Body for controllable elastic behavior (ropes, chains, cables):

1. Create a Simulation Zone with a point line (Mesh Line or Curve to Points)
2. Store `previous_position` as a named attribute via Store Named Attribute
3. Inside the Simulation Zone, nest a **Repeat Zone** (8-12 iterations) for constraint solving:
   - `new_pos = current + (current - previous) × 0.98 + gravity × dt²`
   - Apply distance constraints: if distance between consecutive points > rest_length, move both toward each other proportionally
4. Set `previous = current`, `current = new_pos`
5. Output to Simulation Output

The damping factor (~0.98) prevents energy accumulation. Without distance constraint solving in the Repeat Zone, the rope stretches infinitely.

---

## Advanced: Attribute Transfer Between Mesh and Curve

1. Temporarily convert source geometry with `Curve to Mesh` or `Mesh to Curve`
2. Use `Sample Nearest` to find closest point indices
3. Use `Sample Index` with those indices to read attribute values from source
4. Delete the temporary converted geometry

The `Sample Nearest → Sample Index` two-node pattern is standard for cross-geometry attribute transfer.

---

## GeoNodes vs Modifiers vs Python — When to Use Each

| Tool | Use When |
|------|----------|
| **Built-in Modifier** | The modifier exists and does what you need. Don't reinvent with GeoNodes what's already built. |
| **Geometry Nodes** | You need procedural variation, parametric control, or something no modifier handles. |
| **Python (bpy)** | You need to automate repetitive tasks, batch-process files, create custom UI, interface with external data. |

**GeoNodes is excellent for:** Procedural/parametric work, scatter/distribution workflows, simulation, motion graphics/technical animation.

**GeoNodes is NOT efficient for:** Detailed hand-crafted organic modeling, character rigging, material setup, post-processing.

---

## Known Bugs and Regressions

**GeoNodes Playback Performance Regression (4.x):** Animation playback is measurably slower in Blender 4.3 compared to 3.6 for complex animated setups. Workarounds: bake geometry, replace objects with bounding boxes during preview, use Render > Simplify. For performance-critical projects, 3.6 LTS or 4.2 LTS may perform better.

**Cycles Viewport — Instances in Camera View:** Cycles rendered viewport with many GeoNodes instances is dramatically slower in camera view than in perspective view (BVH rebuilding for instanced geometry within camera bounds). Workaround: `Realize Instances` before output for final renders (increases memory), or work in perspective view while iterating.

**Hidden GeoNodes Modifiers:** Disabling a Geometry Nodes modifier in the viewport (eye icon off) does not fully stop evaluation in all cases. To truly disable: delete the modifier, or add a `Switch` node connected to a boolean input exposed on the modifier panel.
