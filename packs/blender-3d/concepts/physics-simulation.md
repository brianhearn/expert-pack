---
title: Physics and Simulation
type: concept
tags:
- concepts
- physics-simulation
pack: blender-3d
retrieval_strategy: standard
id: blender-3d/concepts/physics-simulation
verified_at: '2026-04-10'
verified_by: agent
---

<!-- context: blender-3d/concepts/physics-simulation -->

# Physics and Simulation

> **Lead summary:** Blender's physics systems — Rigid Body, Soft Body, Cloth, Mantaflow fluids/smoke, and particle systems — are separate engines with different baking pipelines, cache management strategies, and integration with the rest of the Blender scene. The fundamental rule: bake simulations to disk (or at minimum to RAM cache) before rendering or adjusting the timeline. Never render physics without a bake. The Geometry Nodes Simulation Zone (Blender 4.0+) adds a node-based simulation paradigm that integrates cleanly with the GeoNodes ecosystem.

---

## Rigid Body Physics

Rigid bodies are solid, non-deforming objects that interact through collision. Blender's rigid body system is built on the Bullet physics library.

### Setup

Rigid body is set via `Object → Rigid Body → Add Active` (or from Physics Properties). Objects are either:

- **Active:** Simulated — falls, bounces, responds to forces
- **Passive:** Static colliders — floors, walls, obstacles. Can be animated (animated passive = animated static obstacle)

**Collision Shape:** The most critical setting. The physics engine doesn't use the actual mesh for collision — it uses a simplified shape:

| Shape | Use |
|-------|-----|
| Box | Rectangular objects. Fastest. |
| Sphere | Round objects. Very fast. |
| Capsule | Characters, cylinders |
| Cylinder | Exact cylinder shapes |
| Cone | Cone shapes |
| Convex Hull | Approximates the outer volume. Fast, good enough for most objects. |
| Mesh | Exact mesh collision. Slowest. Only for passive objects — active objects with Mesh shape are extremely slow. |

**The common mistake:** Using Mesh collision shape on active objects. This is 100× slower than Convex Hull and usually produces instability. Use Convex Hull for active objects; use Mesh for passive floors/walls.

### Rigid Body World Settings

`Scene Properties → Rigid Body World`:
- `Substeps per Frame`: Default 10. Increase for fast-moving objects or unstable simulation (try 20–40). More substeps = more accurate but slower bake.
- `Solver Iterations`: Default 10. Increase for stacked objects or complex pile simulations (try 20–60 for brick towers).
- `Speed`: Multiplier on simulation time. <1.0 for slow motion.
- `Collection`: Only objects in this collection participate in rigid body.

### Baking Rigid Body

`Scene Properties → Rigid Body World → Bake (All Dynamics)`. Bakes the entire simulation to keyframes on the objects themselves. After baking, the rigid body data is converted to regular animation keyframes — you can scrub freely.

**Bake vs Point Cache:** Rigid body bakes to object keyframes (visible in the Dope Sheet). This differs from Cloth/Fluid which bake to a point cache file on disk.

**Unbaking:** `Rigid Body World → Delete All Bakes`. Returns to simulation mode.

**Tip — Starting conditions:** By default, simulation starts from the object's position at frame 0. If you want objects to start from rest in a piled arrangement: use rigid body to settle the pile (simulate from frame 0), bake, then identify the frame where they're settled, set that as your scene's first frame, and re-bake from there.

---

## Soft Body Physics

Soft Body simulates elastic/jelly-like deformation — objects that stretch, bounce, and squash.

**When to use Soft Body vs Cloth:**
- **Soft Body:** 3D volumetric deformation. Jello, bouncy balls, organic objects. The simulation affects the entire mesh volume.
- **Cloth:** Surface simulation. Fabric, flags, soft thin materials. Primarily surface-based.

**Key settings (Physics Properties → Soft Body):**

- `Mass`: Total object mass. Affects gravity response.
- `Friction`: Drag against movement. Higher = more damping.
- `Goal`: Spring attachment to the original mesh shape. Edges / Vertices have a `Goal Strength` (0=free, 1=rigid pinned to original shape). This is the main control:
  - Goal Strength ~0.7–0.9: Rubber/elastic — bounces back to shape
  - Goal Strength 0–0.3: Jelly/fluid-like — barely holds shape
  - Goal Min/Max: Different vertices can have different goal strengths via a vertex group
- `Edges → Pull/Push/Bending Stiffness`: Controls how edges resist stretching/compression/bending

**Pinning with vertex groups:** Assign a vertex group to the object. In Soft Body settings, use this as the `Goal Vertex Group`. Vertices with weight 1.0 = pinned (don't move). Vertices with weight 0.0 = fully simulated. This lets you pin part of the mesh (like the top of a flag) while the rest simulates.

---

## Cloth Simulation

Cloth is Blender's surface simulation for fabric, flags, curtains, and soft thin objects.

### Setup

Add via `Physics Properties → Cloth`. The mesh should be a thin surface (not a solid volume). For a t-shirt: model the shirt geometry, add Cloth physics.

**Key settings:**

| Setting | Effect |
|---------|--------|
| Preset | Quick-start with Denim, Silk, Leather, Cotton, Rubber, Custom |
| Mass | Weight per m². Higher = heavier fabric. |
| Air Viscosity | Resistance to air movement. Higher = less billowing. |
| Stiffness → Tension | Resistance to stretching. High = non-stretch fabric. |
| Stiffness → Compression | Resistance to compressing. |
| Stiffness → Shear | Resistance to diagonal deformation. |
| Stiffness → Bending | Resistance to folding. Low = silk-like drape. High = card-board stiff. |

**Pinning cloth:** The same vertex group technique as Soft Body. Pin the waistband of pants, the top edge of a flag, the collar of a shirt. Set the vertex group in `Cloth → Shape → Pin Group`.

**Collision:** Cloth needs collision objects (the character body underneath). Set collision on the body object: `Physics Properties → Collision` with appropriate `Thickness` (0.01–0.05m). The cloth object also has self-collision settings — enable `Self Collision` for fabric that bunches up on itself.

### Cloth Quality and Performance

- `Quality Steps`: Steps per frame. Default 5. Increase to 10–20 for fine silk or complex collisions.
- `Collision Quality`: Collision detection accuracy. Higher = more accurate but slower.
- Cloth simulation is heavy. A 10,000-polygon cloth object at quality 15 can take 2–10 seconds per frame to simulate.

### Cloth Baking

`Physics Properties → Cache`. Set cache start/end frames, choose a file path, and bake. Blender writes per-frame data to disk. After baking, you can scrub freely without re-simulating.

**Point cache:** Cloth (and Soft Body, Fluid) uses Blender's point cache system. Cache files are stored in the specified directory (default: `//blendcache_filename/`). If you move the .blend file, bring the cache directory with it or re-bake.

---

## Mantaflow: Fluid, Smoke, and Fire

Mantaflow (integrated in 2.82) is Blender's current fluid and gas simulation engine.

### Fluid (Liquid) Setup

1. Create a **Domain** object: a box that contains the simulation. `Physics → Fluid → Type: Domain`
2. Create one or more **Flow** objects (the fluid source): `Physics → Fluid → Type: Flow`
3. Optionally, create **Effector** objects (solid colliders in the fluid): `Physics → Fluid → Type: Effector`

**Domain settings (critical ones):**

| Setting | Effect |
|---------|--------|
| Resolution Divisions | Voxel resolution of the simulation. Default 32 = very low. Production: 128–256. Very slow above 256. |
| Time Scale | Slow motion (0.1–0.5) or fast forward (2.0+) |
| End Frame | Simulate only up to this frame |
| Cache Type | Replay (slow, no disk), Modular (intermediate), All (full disk cache) |
| Cache Path | Where to save simulation data (required for baking) |

**Resolution is everything:** A 128-resolution domain is ~64× larger than 32 (3D), simulates 64× more voxels. Start with 32 for rapid testing, increase to 128–200 for final renders.

**Flow settings:**
- Type: `Inflow` (continuous source), `Outflow` (drain), `Geometry` (emit from mesh volume)
- For liquid: usually `Geometry` or `Inflow`
- `Initial Velocity`: Starting velocity of emitted fluid

**Baking liquid:** `Domain → Cache → Bake Data`. A 200-frame 128-resolution fluid bake can take 30 minutes to several hours. Plan accordingly.

**Rendering liquid:** Liquid simulation generates a mesh. In domain settings, `Mesh` tab allows increasing mesh resolution. After baking data, bake the mesh separately. The mesh is what you apply a material to — use a glass or water Principled BSDF shader.

### Smoke and Fire

Same pipeline as fluid but with `Domain Type: Gas`.

**Smoke Domain settings:**

| Setting | Effect |
|---------|--------|
| Temperature Difference | How much heat smoke emits (0 = no buoyancy, 1+ = rises) |
| Vorticity | Turbulence/swirling in the smoke |
| Dissolve | Whether smoke dissipates over time (and how fast) |
| High Resolution | Adds noise detail to smoke without full voxel re-simulation |

**Fire:** Set Flow object Fuel to > 0. Temperature controls flame height. Add a Volume material to the domain:
- `Principled Volume` shader: `Color` = smoke color (dark grey), `Emission Strength` driven by `Flame` attribute
- The `Flame` attribute (0–1) is automatically available in the domain object's material

**Standard fire + smoke material:**
```
Attribute "density" → Principled Volume (Density input)
Attribute "flame" → Multiply (×3) → Emission Strength input
Attribute "color" → Emission Color input
```

Adjust `Density` multiplier to control smoke opacity (too dense = opaque black cloud; too light = invisible).

---

## Particle Systems

### Emitter Particles

`Object Properties → Particles → +`. Default type is Emitter.

**Key emitter settings:**

| Setting | Effect |
|---------|--------|
| Number | Total particle count for the simulation |
| Start / End | Frame range for emission |
| Lifetime | How many frames each particle lives |
| Lifetime Randomness | Variation in per-particle lifetime |
| Emit From | Faces (surface), Volume, Verts |
| Gravity | Gravity strength (1.0 = Earth) |
| Random | Initial velocity randomness |

**Rendering particles:**
- `Object`: Each particle becomes an instance of a specified object. Very efficient — 100,000 object instances is manageable.
- `Collection`: Randomly picks from a collection of objects for each particle
- `Path`: Renders as hair-like paths (use for grass, fur primitives)
- `Halo`: Old-style single billboard sprites — rarely used now

**Object instance performance:** With `Object` rendering, particles use Blender's instancing — the same mesh is drawn 100,000 times with minimal memory overhead. This is the standard technique for scatter (rocks, leaves, grass). Far more efficient than Geometry Nodes scatter for some use cases, but less flexible.

### Hair Particles

Hair is a separate particle mode that renders as curves/strands.

`Particles + → Type: Hair`

**Hair workflow:**
1. Add Hair particle system to mesh
2. Set `Hair Length`, `Segments` (higher = smoother curves), and `Number`
3. In `Particle Edit Mode` (`Ctrl+Tab` on particle object): comb, cut, length-paint hair manually
4. Alternatively, use `Children` to generate child hairs from guide hairs (guides = 100–500, children = 50,000+)

**Hair rendering:**
- In `Render Properties → Hair`, set `Presentation: Path` for curves
- `Thickness`: Hair strand width at root and tip
- Apply a hair material to the particle object (use `Hair BSDF` shader for physically correct hair specular)

**Hair curves (Blender 4.x):** Blender 4.0+ introduced a new `Curves` object type specifically for hair, replacing the old Hair Particles system for most professional work. The Curves object:
- Has dedicated sculpt brushes for styling
- Is a proper geometry object (not a particle system)
- Integrates with Geometry Nodes
- Renders correctly with Cycles hair rendering

### Force Fields

Force fields affect particles and soft/rigid bodies.

`Object → Quick Effects → Effectors` or `Add → Force Field`:

| Force Field | Effect |
|-------------|--------|
| Force | Directional force (like a fan). Positive = push, negative = pull. |
| Wind | Directional wind with turbulence. |
| Vortex | Rotational swirl (tornado). |
| Magnetic | Attracts/repels along the field object's axis. |
| Turbulence | Adds chaos/noise to particle motion. |
| Drag | Slows particles (fluid resistance simulation). |
| Boid | Flocking/swarming behavior for particles. |
| Texture | Velocity driven by a texture's values. |

Force fields have `Strength`, `Shape` (point, line, plane, surface), `Falloff` (how quickly the effect diminishes with distance), and `Maximum Distance`.

**Combining force fields:** A particle system responds to all force fields in the scene (or a specific field collection set in the particle system settings). A classic fire simulation uses Wind for upward buoyancy + Turbulence for organic chaos.

---

## Geometry Nodes Simulation Zone (Blender 4.0+)

The Simulation Zone is a special node pair in Geometry Nodes that enables state-based simulation — the output of one frame feeds into the next.

### How It Works

The Simulation Zone uses two nodes: `Simulation Input` and `Simulation Output`. Everything between them is the simulation "step" that runs each frame.

```
Geometry → [Simulation Input] → (per-frame logic nodes) → [Simulation Output] → Geometry
```

The key: the `Simulation Output`'s `Geometry` socket feeds back into the `Simulation Input`'s `Geometry` socket on the next frame. This is what makes it stateful — changes accumulate.

### What You Can Do

- **Particle systems from scratch:** Emit points, apply forces via Math nodes, update positions each frame
- **Custom rigid body behavior:** Track object positions as attributes, apply velocity + gravity manually
- **Sand, granular matter:** Collision with geometry, settling behavior
- **Reaction-diffusion patterns:** Turing patterns, Conway's Game of Life in 3D
- **Growth simulations:** L-systems, organic growth along surfaces

### Example: Simple Gravity Points

```
[Sim Input Geometry] 
  → Store Named Attribute "velocity" 
  → Set Position (old pos + velocity × delta_time) 
  → [Store Named Attribute "velocity" with value = old_velocity + (0,0,-9.8) × delta_time]
[Sim Output]
```

The `delta_time` socket (available on the Simulation Input) provides the per-frame time step, enabling frame-rate-independent simulation.

### Caching the Simulation Zone

The Simulation Zone has a cache built into the modifier:
- `Cache`: In the GeoNodes modifier properties, a `Simulation Nodes` cache section appears
- `Bake`: Writes the simulation to disk (in the project's blend file directory or a custom path)
- After baking, scrubbing the timeline plays back from cache without re-simulating

Simulation Zone caches are separate from the traditional Blender point cache system — they're stored as `.bphys` or custom files depending on the version.

---

## General Physics Best Practices

**Always bake before rendering:** Physics simulations aren't deterministic if run during render — results can differ between frames. Bake to disk before touching `F12`.

**Isolate physics objects:** Keep physics objects in dedicated collections. This allows toggling physics on/off for viewport performance and enables re-baking without disturbing non-physics objects.

**Scale matters enormously:** Blender's physics assume real-world scale (1 Blender unit = 1 meter). A 2×2×2 unit cube is a 2m×2m box. Physics that look wrong (cloth flying off, fluids behaving strangely) are often caused by objects at wrong scale. Apply scale (`Ctrl+A → Scale`) and verify units before setting up physics.

**Viewport performance during simulation:** Disable Cycles/EEVEE viewport shading while scrubbing cached simulations. Use Workbench or Solid mode to scrub quickly.

**Cache management:** Physics caches grow large. A 200-frame fluid simulation at 128 resolution can be 5–50GB. Set cache paths explicitly (not `//` automatic) so you know where they are, and clean them up when projects are done.
