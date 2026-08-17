---
id: blender-3d/concepts/physics-rigid-body
title: "Physics — Rigid Body"
type: concept
tags:
  - physics
  - rigid-body
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/physics-simulation.md
related:
  - physics-soft-cloth.md
  - physics-mantaflow.md
content_hash: sha256:43414865179c9f51f10cf78fb459a353418374ab8785d4835e7fb5b053fcdeb3
---

# Physics — Rigid Body

**The fundamental rule:** Bake simulations to disk (or at minimum to RAM cache) before rendering or adjusting the timeline. Never render physics without a bake. Rigid bodies are solid, non-deforming Bullet objects that collide: active bodies simulate, passive bodies are colliders. Mesh collision on active objects is the usual performance and stability mistake.

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

