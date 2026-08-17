---
id: blender-3d/concepts/geometry-nodes-instances-attributes
title: "Geometry Nodes — Instances, Attributes, and Realize"
type: concept
tags:
  - geometry-nodes
  - instances
  - attributes
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/geometry-nodes.md
related:
  - geometry-nodes-flow-creation.md
  - geometry-nodes-scatter-deform.md
content_hash: sha256:46a41fe29152a202d94f9d446a51b02f5bed18a2fb199bc66371e6530ff7b4a4
---

# Geometry Nodes — Instances, Attributes, and Realize

Instances are lightweight references to geometry; attributes are named per-element data. Realize Instances only when you need real mesh operations; Set Position is per-element, Transform is a single matrix; Geometry to Instance speeds large joins.

## Points and Instances (most powerful workflow)

| Node | Purpose |
|------|---------|
| Distribute Points on Faces | Scatter points on a mesh surface (Poisson or Random) |
| Instance on Points | Place instances of a geometry at each point position |
| Realize Instances | Convert instances to actual geometry (expensive!) |
| Object Info | Get a reference to another object's geometry |
| Collection Info | Get a reference to a collection of objects |
| Random Value | Generate random values (field — different per element) |

---

## Attributes

| Node | Purpose |
|------|---------|
| Store Named Attribute | Save a computed field value as a named attribute |
| Named Attribute | Retrieve a named attribute from geometry |
| Attribute Statistic | Compute min/max/mean/std of an attribute over geometry |
| Capture Attribute | Sample an attribute at a specific point in the graph (freeze it) |
| Transfer Attribute | Interpolate attributes from one geometry to another |

---

## Instances vs Realized Geometry

**Instances** are lightweight references — Blender renders them directly without duplicating geometry. 10,000 tree instances = 1 tree's worth of geometry data in memory.

**Realize Instances** converts instances to actual geometry — suddenly you have 10,000 trees' worth of geometry. The viewport may freeze.

**Rule:** Keep geometry as instances as long as possible. Only realize when you actually need per-element editing.

**When you are forced to realize:**
- When you need `Merge by Distance` on instanced geometry
- When per-element operations (like extrude) are needed on instance elements
- When exporting to game engines (they typically can't use GeoNodes instances directly)

---

## Set Position vs Transform: Performance Rule

- **Transform node:** Operates on the entire geometry as a single matrix transform. Use when moving, rotating, or scaling *all* elements.
- **Set Position node:** Evaluates a field per element. Use when applying different offsets to different elements.

On meshes with 100k+ vertices, using Set Position for a uniform translation is measurably slower than Transform.

---

## Geometry to Instance for Join Performance

`Join Geometry` with many inputs (50+) degrades linearly. The `Geometry to Instance` node converts each input to a lightweight instance before joining — dramatically faster for merging procedurally generated segments (road systems, modular architecture). The result is instances — further per-vertex operations require Realize Instances.

