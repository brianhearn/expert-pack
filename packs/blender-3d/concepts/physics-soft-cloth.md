---
id: blender-3d/concepts/physics-soft-cloth
title: "Physics — Soft Body, Cloth, and Bake Practice"
type: concept
tags:
  - physics
  - soft-body
  - cloth
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/physics-simulation.md
related:
  - physics-rigid-body.md
  - physics-particles.md
content_hash: sha256:8a4bc1a7e0334a421ee7d867331bdb986b01ac3c7463705b652cecdaa24bdb84
---

# Physics — Soft Body, Cloth, and Bake Practice

Soft Body simulates volumetric squash-and-stretch; Cloth simulates thin fabric surfaces. Both need pinning or goal weights, collision objects, and a disk-cache bake. Scale (1 Blender unit = 1 meter) and baking before F12 apply to all Blender physics.

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

