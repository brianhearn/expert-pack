---
id: blender-3d/concepts/physics-particles
title: "Physics — Particle Systems and Force Fields"
type: concept
tags:
  - physics
  - particles
  - hair
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/physics-simulation.md
related:
  - physics-mantaflow.md
  - physics-soft-cloth.md
content_hash: sha256:db55cd07a11dcfb3dc553b6ee1008ba3821599016821d25840ad27c405c22850
---

# Physics — Particle Systems and Force Fields

Particle systems emit points that can instance objects, draw as hair, or react to force fields. Emitter settings control count, lifetime, and gravity; Hair Particles and the 4.x Curves object cover grooming; force fields add wind and turbulence.

## Particle Systems

### Emitter Particles

`Object Properties → Particles → +`. Key emitter settings:

| Setting | Effect |
|---------|--------|
| Number | Total particle count |
| Start / End | Frame range for emission |
| Lifetime | How many frames each particle lives |
| Gravity | Gravity strength (1.0 = Earth) |
| Emit From | Faces (surface), Volume, Verts |

**Rendering particles:**
- `Object`: Each particle becomes an instance of a specified object. Very efficient — 100,000 object instances is manageable.
- `Collection`: Randomly picks from a collection for each particle.
- `Path`: Renders as hair-like paths (grass, fur primitives).

Object instance performance: far more efficient than Geometry Nodes scatter for some use cases, but less flexible.

### Hair Particles

`Particles + → Type: Hair`

**Hair workflow:**
1. Set `Hair Length`, `Segments` (higher = smoother), and `Number`
2. In `Particle Edit Mode` (`Ctrl+Tab`): comb, cut, length-paint hair manually
3. Use `Children` to generate child hairs from guide hairs (guides = 100–500, children = 50,000+)

**Hair Curves (Blender 4.x):** Blender 4.0+ introduced a dedicated `Curves` object type for hair, replacing Hair Particles for most professional work. The Curves object has dedicated sculpt brushes for styling, is a proper geometry object, integrates with Geometry Nodes, and renders correctly with Cycles hair rendering.

### Force Fields

`Object → Quick Effects → Effectors` or `Add → Force Field`:

| Force Field | Effect |
|-------------|--------|
| Force | Directional force (like a fan). Positive = push, negative = pull. |
| Wind | Directional wind with turbulence. |
| Vortex | Rotational swirl (tornado). |
| Turbulence | Adds chaos/noise to particle motion. |
| Drag | Slows particles (fluid resistance). |

Force fields have `Strength`, `Shape`, `Falloff` (how quickly effect diminishes with distance), and `Maximum Distance`.

A particle system responds to all force fields in the scene (or a specific field collection set in the particle system settings). Classic fire simulation: Wind (upward buoyancy) + Turbulence (organic chaos).

