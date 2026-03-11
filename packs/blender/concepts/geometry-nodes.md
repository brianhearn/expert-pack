# Geometry Nodes

Geometry Nodes is Blender's procedural geometry system — a visual, node-based programming environment for creating and modifying geometry. It was introduced in Blender 2.92 (2021) and has been one of the fastest-evolving parts of Blender since. It represents a paradigm shift in how Blender models can be built.

---

## What Geometry Nodes Are

Geometry Nodes is a modifier type (`Add Modifier → Geometry Nodes`) that processes geometry through a node graph. Unlike other modifiers, the entire logic is user-defined — you build the processing pipeline yourself with nodes.

Think of it as a functional programming language for 3D geometry, expressed visually. Input geometry goes in, nodes transform it, output geometry comes out.

**Key distinction:** Geometry Nodes is NOT the same node system as Shader Nodes or the Compositor. It operates on geometry, not on surface shading. The mental model is different.

**What you can do with Geometry Nodes:**
- Scatter objects across a surface (forests, rocks, crowds)
- Create parametric shapes (change a number slider → geometry updates)
- Build procedural architecture (buildings from parameters)
- Create complex motion graphics
- Simulate particles and physical systems (Simulation Nodes, added in 3.6)
- Drive geometry from other geometry (deformation based on curves)
- Replace entire modeling workflows with procedural equivalents

---

## The Paradigm Shift

In classic Blender, geometry modification is linear: start with a mesh, apply operations in sequence, get a result. Each modifier modifies the geometry in-place.

In Geometry Nodes, the paradigm is **functional and non-destructive**:
- Geometry flows through the graph as data
- Nothing is modified in-place — operations return new geometry
- The same input can branch into multiple processing paths
- Everything can be parameterized and driven by inputs

This creates possibilities that are impossible with the classic modifier stack:
- Procedural variation (randomized but controllable placement)
- Fully parametric models (change one value, everything adapts)
- Geometry that responds to other geometry
- Instancing at scales that would be impossible with real geometry

---

## Core Concepts

### Geometry Socket

The primary data type in Geometry Nodes. A geometry socket carries one of:
- **Mesh** — polygon mesh data (vertices, edges, faces, face corners)
- **Curve** — Bezier or NURBS curve data
- **Point Cloud** — unconnected points with attributes but no topology
- **Instances** — references to geometry (not actual copies) with transforms
- **Volume** — voxel grid data (for smoke/fluid simulation output)

The green sockets in the node graph carry geometry. Most nodes consume geometry on the left and produce geometry on the right.

### Attributes

An **attribute** is named data stored on elements of geometry. Every piece of geometry can have many attributes.

**Built-in attributes** (always present):
- `position` — (Vector) Location of each point/vertex
- `normal` — (Vector) Surface normal direction
- `index` — (Integer) Element index (0, 1, 2...)
- `material_index` — (Integer) Which material slot this face uses
- `uv_map` — (Vector, Face Corner domain) UV coordinates

**Custom attributes:** You can create your own named attributes with any name and any data type. These persist through the Geometry Nodes stack and can be read/written by any node.

**Attribute domains** — What kind of element the attribute is stored on:
- **Point** (vertex for meshes, point for point clouds, control point for curves)
- **Edge** — per-edge data
- **Face** — per-face data
- **Face Corner** — per face-vertex data (allows UV seams — same vertex has different UV values on different faces)
- **Instance** — per-instance data in a collection of instances

The domain matters for attribute transfer. A `Face` domain attribute becomes a different shape of data than a `Point` domain attribute.

---

## Fields: The Most Important Concept

**This is the #1 concept people struggle with when learning Geometry Nodes.**

A **field** is NOT a single value. A field is a **recipe for computing a value per element**.

When you connect a `Position` node to another node, you are not passing the position of some object. You are passing a *field* that says "evaluate to the position of whatever element is being processed."

Think of a field like a function `f(element)` rather than a constant value.

**Why this matters:**

If you use the `Random Value` node, you don't get one random number — you get a *field* that evaluates to a different random number for each element it's applied to. Every vertex, face, or point gets its own random value.

If you use the `Position` node, connecting it to `Set Position → Offset` doesn't move everything by "the position" — it offsets each element by *its own* position (which would scale everything outward from the origin).

**The mental model:**
- Most numeric values in Geometry Nodes are fields (per-element recipes)
- When a node processes geometry, it evaluates each field for each element
- A constant value (like `0.5`) is a trivially constant field — the same value for every element
- A `Position` or `Index` or `Normal` field is different for each element

**Practical example:**
`Distribute Points on Faces` scatters points across a mesh. The `Density` input is a *field* — you can connect a procedural noise texture to make some areas denser than others. The noise is evaluated *per-face* during distribution.

**Where fields appear:**
Look for the purple tint on socket inputs — those accept fields (per-element values). White/gray sockets typically require single values.

---

## Essential Nodes Reference

### Flow Control

| Node | Purpose |
|------|---------|
| Group Input | The inputs to your node group (exposed as modifier parameters) |
| Group Output | The final geometry output |
| Join Geometry | Combines multiple geometry streams into one |

### Creation

| Node | Purpose |
|------|---------|
| Mesh Primitives (Cube, Cylinder, etc.) | Create basic mesh shapes procedurally |
| Mesh Line | Create a line of vertices |
| Mesh Grid | Create a grid mesh |
| Curve Primitives | Create curves procedurally |
| Points | Create a point cloud |

### Modification

| Node | Purpose |
|------|---------|
| Set Position | Move geometry — the fundamental deformation node |
| Transform Geometry | Apply a full transform (location/rotation/scale) to geometry |
| Merge by Distance | Weld nearby vertices (equivalent to "Remove Doubles") |
| Subdivide Mesh | Subdivide within the node graph |
| Extrude Mesh | Extrude faces/edges/vertices |
| Flip Faces | Flip face normals |

### Points and Instances (the most powerful workflow in GeoNodes)

| Node | Purpose |
|------|---------|
| Distribute Points on Faces | Scatter points on a mesh surface (Poisson or Random) |
| Instance on Points | Place instances of a geometry at each point position |
| Realize Instances | Convert instances to actual geometry (expensive!) |
| Object Info | Get a reference to another object's geometry |
| Collection Info | Get a reference to a collection of objects |
| Random Value | Generate random values (field — different per element) |

### Attributes

| Node | Purpose |
|------|---------|
| Store Named Attribute | Save a computed field value as a named attribute |
| Named Attribute | Retrieve a named attribute from geometry |
| Attribute Statistic | Compute min/max/mean/std of an attribute over geometry |
| Capture Attribute | Sample an attribute at a specific point in the graph (freeze it) |
| Transfer Attribute | Interpolate attributes from one geometry to another |

---

## Common Patterns

### Pattern 1: Scatter Objects on a Surface

```
[Object Info: Source Object] ─→ [Distribute Points on Faces] ─→ [Instance on Points] ─→ [Group Output]
                                    ↑
                              [Group Input: Density]
```

This is the classic scatter pattern — scatter points across a mesh, place instances at each point. Scale, rotation, and position can all be randomized by feeding fields into Instance on Points.

**Key detail:** Use `Collection Info` instead of `Object Info` to scatter from a collection of multiple objects — GeoNodes will randomly pick from the collection for each point.

### Pattern 2: Deform Along a Curve

Use `Sample Curve` to get position and tangent along a curve at normalized positions, then use `Set Position` to move points to those positions. This creates a "curve deformer" similar to the Curve modifier but fully procedural.

### Pattern 3: Parametric Shape

Group Input → [your construction math] → Group Output. Expose key dimensions (width, height, segment count) as Group Inputs. The shape recalculates automatically when you change the modifier parameters.

### Pattern 4: Procedural Variation

Connect `Index → Math (divide by total count) → position/scale/rotation input`. This creates per-instance variation that's deterministic (same result every time) and ordered. Combine with `Random Value` with a seed for chaotic variation.

---

## Instances vs Realized Geometry

**Instances** are lightweight references — Blender renders them directly without duplicating the geometry in memory. 10,000 tree instances = 1 tree's worth of geometry data in memory.

**Realize Instances** converts instances to actual geometry — suddenly you have 10,000 trees' worth of geometry. The viewport may freeze. The mesh becomes editable but enormous.

**Rule:** Keep geometry as instances as long as possible. Only call Realize Instances when you actually need to edit the individual elements of the realized geometry.

**When you are forced to realize:**
- When you need to run `Merge by Distance` on the instanced geometry
- When you need per-element operations (like extrude) on instance elements
- When exporting to game engines (they typically can't use GeoNodes instances directly)

**Alternative to realize:** Many operations work *on* instances without realizing them. `Instance on Points` with the right inputs can do what you might think requires realization.

---

## Performance Considerations

Geometry Nodes can generate enormous amounts of geometry. Key practices:

1. **Instance, don't realize.** Covered above — instances are essentially free.
2. **Limit distribution density.** `Distribute Points on Faces` with density 10 on a large mesh = millions of points. Work at lower density and scale up only for final renders.
3. **Use viewport simplification.** `Scene Properties → Simplification → Max Subdivision` limits density while working.
4. **Use the Viewer node** (Shift+Ctrl+click any output) to inspect intermediate values without full evaluation.
5. **Simulation Nodes are expensive** — they evaluate every frame sequentially from the start frame. Cache simulations using the Simulation bake in the modifier properties.
6. **Realize Instances as late as possible** — ideally only for export.

---

## GeoNodes vs Modifiers vs Python — When to Use Each

| Tool | Use When |
|------|----------|
| **Built-in Modifier** | The modifier exists and does what you need. Don't reinvent with GeoNodes what's already built. |
| **Geometry Nodes** | You need procedural variation, parametric control, or something no modifier handles. Complex scatter, procedural architecture, parametric shapes. |
| **Python (bpy)** | You need to automate repetitive tasks, batch-process files, create custom UI panels, interface with external data, or need algorithms that GeoNodes can't express cleanly. |

**GeoNodes is NOT a replacement for all modeling.** It's excellent for:
- Anything procedural or parametric
- Scatter/distribution workflows
- Simulation
- Motion graphics / technical animation

It's NOT efficient for:
- Detailed hand-crafted organic modeling (use mesh tools)
- Character rigging (use armatures)
- Material setup (use Shader Nodes)
- Post-processing (use Compositor)

---

## Simulation Nodes (Blender 3.6+)

Simulation Nodes added temporal simulation to Geometry Nodes. A Simulation Zone (Simulation Input + Simulation Output nodes) creates a loop that runs once per frame, carrying state from the previous frame.

**What this enables:**
- Particle-like simulations without Blender's legacy particle system
- Custom cloth, fluid, or agent simulations
- Procedural growth over time
- Anything that requires "remembering" state between frames

**The catch:** Simulation Nodes must be evaluated sequentially from frame 1. You cannot jump to frame 100 without computing frames 1–99. Always **bake** simulations before rendering animation: click `Bake` in the Modifier properties. Otherwise, scrubbing the timeline triggers full re-simulation.

**Simulation zone state:** The geometry that "flows back" from the Simulation Output to the Simulation Input is the persistent state. You can store arbitrary attributes in this state to track custom properties over time.
