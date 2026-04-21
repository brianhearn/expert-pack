---
id: blender-3d/concepts/physics-rigid-soft-cloth
title: "Physics — Rigid Body, Soft Body, and Cloth"
type: concept
tags:
  - physics
  - rigid-body
  - cloth
  - soft-body
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-04-21"
verified_by: agent
supersedes:
  - concepts/physics-simulation.md
related:
  - physics-fluids-particles.md
  - geometry-nodes-simulation.md
---

# Physics — Rigid Body, Soft Body, and Cloth

**The fundamental rule:** Bake simulations to disk (or at minimum to RAM cache) before rendering or adjusting the timeline. Never render physics without a bake.

---

## Rigid Body Physics

Rigid bodies are solid, non-deforming objects interacting through collision (built on the Bullet physics library).

### Setup

Set via `Object → Rigid Body → Add Active`. Objects are:
- **Active:** Simulated — falls, bounces, responds to forces
- **Passive:** Static colliders — floors, walls, obstacles. Can be animated.

**Collision Shape (the most critical setting):**

| Shape | Use |
|-------|-----|
| Box | Rectangular objects. Fastest. |
| Sphere | Round objects. Very fast. |
| Convex Hull | Approximates the outer volume. Fast, good enough for most objects. |
| Mesh | Exact mesh collision. Slowest. **Only for passive objects.** |

**The common mistake:** Using Mesh collision shape on active objects. This is 100× slower than Convex Hull and usually produces instability.

### Rigid Body World Settings

`Scene Properties → Rigid Body World`:
- `Substeps per Frame`: Default 10. Increase for fast-moving objects or unstable simulation (try 20–40).
- `Solver Iterations`: Default 10. Increase for stacked objects (try 20–60 for brick towers).

### Baking Rigid Body

`Scene Properties → Rigid Body World → Bake (All Dynamics)`. Converts simulation to regular animation keyframes. After baking, you can scrub freely.

**Unbaking:** `Rigid Body World → Delete All Bakes`.

**Starting conditions tip:** Use rigid body to settle a pile (simulate from frame 0), bake, identify the settled frame, set that as scene's first frame, and re-bake from there.

---

## Soft Body Physics

Soft Body simulates elastic/jelly-like deformation — objects that stretch, bounce, and squash.

**Soft Body vs Cloth:**
- **Soft Body:** 3D volumetric deformation. Jello, bouncy balls, organic objects.
- **Cloth:** Surface simulation. Fabric, flags, soft thin materials.

**Key settings:**
- `Goal`: Spring attachment to original mesh shape. `Goal Strength` is the main control:
  - ~0.7–0.9: Rubber/elastic — bounces back to shape
  - 0–0.3: Jelly/fluid-like — barely holds shape
- `Goal Vertex Group`: Vertices with weight 1.0 = pinned, 0.0 = fully simulated.
- `Edges → Pull/Push/Bending Stiffness`: Controls edge resistance to stretching/compression/bending.

---

## Cloth Simulation

Cloth simulates fabric, flags, curtains, and soft thin objects.

**Key settings:**

| Setting | Effect |
|---------|--------|
| Preset | Quick-start with Denim, Silk, Leather, Cotton, Rubber |
| Stiffness → Tension | Resistance to stretching. High = non-stretch fabric. |
| Stiffness → Bending | Resistance to folding. Low = silk-like drape. High = stiff. |
| Air Viscosity | Resistance to air. Higher = less billowing. |

**Pinning cloth:** Assign a vertex group to the object. In Cloth settings → `Shape → Pin Group`. Pin top edge of flag, waistband of pants, collar of shirt.

**Collision:** Cloth needs collision objects (the character body underneath). Set collision on the body: `Physics Properties → Collision`. Enable `Self Collision` in cloth settings for fabric that bunches up on itself.

### Cloth Quality and Performance

- `Quality Steps`: Default 5. Increase to 10–20 for fine silk or complex collisions.
- A 10,000-polygon cloth at quality 15 can take 2–10 seconds per frame.

### Baking Cloth

`Physics Properties → Cache`. Set cache start/end frames, choose a file path, and bake. Blender writes per-frame data to disk (in `//blendcache_filename/` by default). If you move the .blend file, bring the cache directory with it or re-bake.

---

## General Physics Best Practices

**Always bake before rendering:** Physics simulations aren't deterministic if run during render. Bake to disk before `F12`.

**Isolate physics objects:** Keep physics objects in dedicated collections for toggling physics on/off and selective re-baking.

**Scale matters enormously:** Blender's physics assume real-world scale (1 Blender unit = 1 meter). Physics that look wrong are often caused by objects at wrong scale. Apply scale (`Ctrl+A → Scale`) before setting up physics.

**Cache management:** Physics caches grow large. A 200-frame fluid simulation at 128 resolution can be 5–50GB. Set cache paths explicitly and clean them up when projects are done.
