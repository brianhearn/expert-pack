---
id: blender-3d/concepts/geometry-nodes-scatter-deform
title: "Geometry Nodes — Scatter and Curve Deform Patterns"
type: concept
tags:
  - geometry-nodes
  - patterns
  - scatter
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/geometry-nodes.md
related:
  - geometry-nodes-parametric.md
  - geometry-nodes-instances-attributes.md
content_hash: sha256:6591498853ff749396fe679e18a46e90aae09e77f48b06de10d770c30571957f
---

# Geometry Nodes — Scatter and Curve Deform Patterns

Two staple Geometry Nodes patterns are scattering instances on a surface and deforming geometry along a curve. Scatter uses Distribute Points on Faces plus Instance on Points; curve deform samples a curve and Set Position.

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

