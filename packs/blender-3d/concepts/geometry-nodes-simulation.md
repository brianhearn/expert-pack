---
id: blender-3d/concepts/geometry-nodes-simulation
title: "Geometry Nodes — Simulation Nodes (Blender 3.6+)"
type: concept
tags:
  - geometry-nodes
  - simulation
  - temporal
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
  - physics-rigid-soft-cloth.md
---

# Geometry Nodes — Simulation Nodes (Blender 3.6+)

Simulation Nodes added temporal simulation to Geometry Nodes. A Simulation Zone (Simulation Input + Simulation Output nodes) creates a loop that runs once per frame, carrying state from the previous frame.

---

## How It Works

The Simulation Zone uses two nodes: `Simulation Input` and `Simulation Output`. Everything between them is the simulation "step" that runs each frame.

```
Geometry → [Simulation Input] → (per-frame logic nodes) → [Simulation Output] → Geometry
```

The `Simulation Output`'s `Geometry` socket feeds back into the `Simulation Input`'s `Geometry` socket on the next frame — this is what makes it stateful.

---

## What This Enables

- **Particle systems from scratch:** Emit points, apply forces via Math nodes, update positions each frame
- **Custom rigid body behavior:** Track object positions as attributes, apply velocity + gravity manually
- **Sand, granular matter:** Collision with geometry, settling behavior
- **Reaction-diffusion patterns:** Turing patterns, Conway's Game of Life in 3D
- **Growth simulations:** L-systems, organic growth along surfaces

---

## The Catch

Simulation Nodes must be evaluated **sequentially from frame 1**. You cannot jump to frame 100 without computing frames 1–99.

**Always bake before rendering:** Click `Bake` in the Modifier properties. Otherwise, scrubbing the timeline triggers full re-simulation.

---

## Example: Simple Gravity Points

```
[Sim Input Geometry] 
  → Store Named Attribute "velocity" 
  → Set Position (old pos + velocity × delta_time) 
  → [Store Named Attribute "velocity" with value = old_velocity + (0,0,-9.8) × delta_time]
[Sim Output]
```

The `delta_time` socket (available on the Simulation Input) provides the per-frame time step, enabling frame-rate-independent simulation.

---

## Caching

The Simulation Zone has a cache built into the modifier:
- `Bake`: Writes simulation to disk (in the project's blend file directory or a custom path)
- After baking, scrubbing the timeline plays back from cache without re-simulating

Simulation Zone caches are separate from the traditional Blender point cache system.

---

## Performance Considerations

Simulation Nodes are expensive — they evaluate every frame sequentially from the start frame. Cache simulations using the Simulation bake in the modifier properties before doing any heavy scrubbing or rendering.
