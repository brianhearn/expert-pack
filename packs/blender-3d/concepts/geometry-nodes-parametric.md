---
id: blender-3d/concepts/geometry-nodes-parametric
title: "Geometry Nodes — Parametric Shapes and Procedural Variation"
type: concept
tags:
  - geometry-nodes
  - patterns
  - parametric
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/geometry-nodes.md
related:
  - geometry-nodes-scatter-deform.md
  - geometry-nodes-advanced-patterns.md
content_hash: sha256:63aafae573e9198e8bd75c80ac24144bc2071b7f0df7f5f6274db8e0e743250f
---

# Geometry Nodes — Parametric Shapes and Procedural Variation

Parametric Geometry Nodes graphs expose dimensions as Group Inputs so a modifier slider rebuilds the shape. Procedural variation uses Index or Random Value fields so each element gets a deterministic or seeded offset.

## Pattern 3: Parametric Shape

Group Input → [construction math] → Group Output. Expose key dimensions (width, height, segment count) as Group Inputs. The shape recalculates automatically when modifier parameters change.

---

## Pattern 4: Procedural Variation

Connect `Index → Math (divide by total count) → position/scale/rotation input`. Creates per-instance variation that's deterministic and ordered. Combine with `Random Value` with a seed for chaotic variation.

---

