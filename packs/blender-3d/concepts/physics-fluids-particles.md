---
id: blender-3d/concepts/physics-fluids-particles
title: "Physics — Mantaflow Fluids, Smoke, and Particle Systems"
type: concept
tags:
  - physics
  - mantaflow
  - fluid
  - particles
  - smoke
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-04-21"
verified_by: agent
supersedes:
  - concepts/physics-simulation.md
related:
  - physics-rigid-soft-cloth.md
---

# Physics — Mantaflow Fluids, Smoke, and Particle Systems

---

## Mantaflow: Fluid, Smoke, and Fire

Mantaflow (integrated in Blender 2.82) is Blender's current fluid and gas simulation engine.

### Fluid (Liquid) Setup

1. Create a **Domain** object (a box that contains the simulation): `Physics → Fluid → Type: Domain`
2. Create one or more **Flow** objects (the fluid source): `Physics → Fluid → Type: Flow`
3. Optionally, create **Effector** objects (solid colliders): `Physics → Fluid → Type: Effector`

**Domain settings (critical):**

| Setting | Effect |
|---------|--------|
| Resolution Divisions | Voxel resolution. Default 32 = very low. Production: 128–256. Avoid above 256. |
| Time Scale | Slow motion (<1.0) or fast forward (>1.0) |
| Cache Type | Replay (slow, no disk), Modular (intermediate), All (full disk cache) |
| Cache Path | Where to save simulation data (required for baking) |

**Resolution is everything:** A 128-resolution domain is ~64× larger than 32 (3D), simulates 64× more voxels. Start with 32 for rapid testing, increase to 128–200 for final renders.

**Baking liquid:** `Domain → Cache → Bake Data`. A 200-frame 128-resolution fluid bake can take 30 minutes to several hours.

**Rendering liquid:** Liquid simulation generates a mesh. After baking data, bake the mesh separately. Apply a water material (Principled BSDF with Transmission ≈ 1.0 and IOR ≈ 1.33).

### Smoke and Fire

Same pipeline but `Domain Type: Gas`.

**Smoke Domain settings:**

| Setting | Effect |
|---------|--------|
| Temperature Difference | Heat smoke emits (0 = no buoyancy) |
| Vorticity | Turbulence/swirling |
| Dissolve | Whether smoke dissipates over time |
| High Resolution | Adds noise detail without full voxel re-simulation |

**Fire:** Set Flow object Fuel > 0. Add a Volume material to the domain:
```
Attribute "density" → Principled Volume (Density input)
Attribute "flame" → Multiply (×3) → Emission Strength input
Attribute "color" → Emission Color input
```

---

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
