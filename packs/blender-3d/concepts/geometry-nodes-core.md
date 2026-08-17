---
id: blender-3d/concepts/geometry-nodes-core
title: "Geometry Nodes — What They Are and Core Data Types"
type: concept
tags:
  - geometry-nodes
  - procedural
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/geometry-nodes.md
related:
  - geometry-nodes-fields.md
  - geometry-nodes-flow-creation.md
  - geometry-nodes-simulation.md
content_hash: sha256:5ba982c42b7a10d99069b8d8a3a8c72e0abdcdfeb2470514b1cf3fd7d30aacef
---

# Geometry Nodes — What They Are and Core Data Types

Geometry Nodes is Blender's procedural geometry system — a visual, node-based programming environment for creating and modifying geometry. Introduced in Blender 2.92 (2021), it represents a paradigm shift from in-place modifiers to a functional, non-destructive pipeline.

## What Geometry Nodes Are

Geometry Nodes is a modifier type (`Add Modifier → Geometry Nodes`) that processes geometry through a user-defined node graph. Input geometry goes in, nodes transform it, output geometry comes out.

Think of it as a functional programming language for 3D geometry, expressed visually.

**Key distinction:** Geometry Nodes is NOT the same as Shader Nodes or the Compositor. It operates on geometry, not surface shading.

**What you can do:**
- Scatter objects across a surface (forests, rocks, crowds)
- Create parametric shapes (slider changes → geometry updates)
- Build procedural architecture from parameters
- Create complex motion graphics
- Simulate particles and physical systems (Simulation Nodes, added in 3.6)
- Drive geometry from other geometry

---

## The Paradigm Shift

Classic Blender: geometry modification is linear — start with a mesh, apply operations in sequence.

Geometry Nodes: **functional and non-destructive**:
- Geometry flows through the graph as data
- Nothing is modified in-place — operations return new geometry
- The same input can branch into multiple processing paths
- Everything can be parameterized and driven by inputs

This enables procedural variation, fully parametric models, geometry that responds to other geometry, and instancing at scales impossible with real geometry.

---

## Core Data Types

**Geometry socket (green):** Carries one of: Mesh, Curve, Point Cloud, Instances, or Volume.

**Attributes:** Named data stored on geometry elements. Built-in attributes:
- `position` — (Vector) per point location
- `normal` — (Vector) surface normal
- `index` — (Integer) element index
- `material_index` — (Integer) material slot per face
- `uv_map` — (Vector, Face Corner domain)

Custom attributes can be created with any name and type.

**Attribute domains:** Point, Edge, Face, Face Corner, Instance. Domain matters for attribute transfer — a Face domain attribute is shaped differently than a Point domain attribute.

---

