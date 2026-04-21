---
id: blender-3d/concepts/geometry-nodes-core
title: "Geometry Nodes — Core Concepts"
type: concept
tags:
  - geometry-nodes
  - procedural
  - fields
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-04-21"
verified_by: agent
supersedes:
  - concepts/geometry-nodes.md
related:
  - geometry-nodes-nodes-reference.md
  - geometry-nodes-patterns.md
  - geometry-nodes-simulation.md
---

# Geometry Nodes — Core Concepts

Geometry Nodes is Blender's procedural geometry system — a visual, node-based programming environment for creating and modifying geometry. Introduced in Blender 2.92 (2021), it represents a paradigm shift from in-place modifiers to a functional, non-destructive pipeline.

---

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

## Fields: The Most Important Concept

**A field is NOT a single value. A field is a recipe for computing a value per element.**

When you connect a `Position` node to another node, you are not passing the position of some object. You are passing a *field* that says "evaluate to the position of whatever element is being processed."

Think of a field like a function `f(element)` rather than a constant value.

**Why this matters:**

`Random Value` node → you don't get one random number. You get a *field* that evaluates to a different random number for each element. Every vertex, face, or point gets its own random value.

`Position` node connected to `Set Position → Offset` → offsets each element by *its own* position (which scales everything outward from the origin).

**The mental model:**
- Most numeric values in Geometry Nodes are fields (per-element recipes)
- A constant value (like `0.5`) is a trivially constant field — same for every element
- A `Position` or `Index` or `Normal` field is different for each element

**Practical example:** `Distribute Points on Faces` — the `Density` input is a *field*. Connect a noise texture to make some areas denser. The noise is evaluated *per-face* during distribution.

**Where fields appear:** Look for the purple tint on socket inputs — those accept fields (per-element values). White/gray sockets typically require single values.
