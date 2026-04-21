---
title: Why Does My Physics Simulation Explode?
type: faq
tags:
- common-mistakes
- faq
- physics-simulation
- physics-troubleshooting
pack: blender-3d
retrieval_strategy: standard
id: blender-3d/faq/why-does-my-physics-sim-explode
verified_at: "2026-04-21"
verified_by: agent
schema_version: "4.1"
---
<!-- context: section=faq, topic=physics-troubleshooting, related=physics-simulation,common-mistakes -->

# Why Does My Physics Simulation Explode?

> **Lead summary:** Physics simulations "explode" (objects fly apart, cloth stretches infinitely, fluid goes haywire) due to three common causes: the time step is too large for the collision speed, objects have overlapping geometry at the simulation start, or scale is wrong (Blender's physics engine assumes 1 unit = 1 meter).

## Cause 1: Time Step Too Large

The physics solver calculates forces per frame. If objects move faster than one collision-width per frame, the solver misses the collision entirely and objects pass through each other, then overcorrect violently.

**Fix:**
- Increase **Substeps Per Frame** (Rigid Body World → Substeps). Default is 10; try 20-40 for fast-moving objects.
- For cloth: increase **Quality Steps** in Cloth → Settings. Default 5; try 10-15.
- Lower your timestep: bake at a higher frame rate (120fps) and slow down in the compositor.

## Cause 2: Overlapping Geometry at Start

If objects intersect at frame 1, the solver tries to push them apart instantly — generating extreme forces.

**Fix:**
- Ensure all objects start with clear separation (no interpenetration).
- For cloth over a body: use **Pre-roll** — set the cloth simulation start frame earlier so it has time to settle.
- For rigid bodies: check the collision shapes (Rigid Body → Collision Shape). **Mesh** shape is accurate but slow; **Convex Hull** is faster but can create phantom overlaps with concave objects.

## Cause 3: Wrong Scale

Blender's physics engine assumes **1 Blender unit = 1 meter**. A "building" that's 2 units tall is treated as 2 meters — physics will look wrong because gravity and forces are calibrated to real-world scale.

**Fix:**
- Apply scale on all physics objects: Ctrl+A → Scale.
- Check that your scene scale matches reality. A character should be ~1.7 units tall.
- If working at a different scale intentionally, adjust Scene → Gravity and object masses accordingly.

## Other Common Causes

- **Mass ratios too extreme** — a 0.001 kg cloth on a 10000 kg body. Keep mass ratios under 100:1.
- **Collision margins** — too large creates "force field" effects; too small misses contacts. Default (0.04m) works for most scenes.
- **Not baking** — don't rely on viewport playback. Bake the simulation for stable results: Physics → Rigid Body World → Bake.

## Related

- [[physics-rigid-soft-cloth.md|Physics & Simulation]]
- [[common-mistakes.md|Common Mistakes]]
