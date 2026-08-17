---
id: blender-3d/concepts/physics-mantaflow
title: "Physics — Mantaflow Fluids, Smoke, and Fire"
type: concept
tags:
  - physics
  - mantaflow
  - fluid
  - smoke
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/physics-simulation.md
related:
  - physics-particles.md
  - physics-rigid-body.md
content_hash: sha256:762335cda7f2b3ade850f934e8efde780316d70d6e58260a259eb56f2ffca6a8
---

# Physics — Mantaflow Fluids, Smoke, and Fire

Mantaflow is Blender's fluid and gas engine. A Domain contains the sim, Flow objects emit liquid or smoke/fire, and Effectors collide. Resolution divisions dominate quality and bake time; gas domains use a Principled Volume material.

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

