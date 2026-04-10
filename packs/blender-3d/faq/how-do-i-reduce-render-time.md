---
title: How Do I Reduce Render Time?
type: faq
tags:
- compositing
- faq
- render-performance
- scene-optimization
- shading-rendering
pack: blender-3d
retrieval_strategy: standard
id: blender-3d/faq/how-do-i-reduce-render-time
verified_at: '2026-04-10'
verified_by: agent
---
<!-- context: section=faq, topic=render-performance, related=shading-rendering,scene-optimization,compositing -->

# How Do I Reduce Render Time?

> **Lead summary:** Reduce render time by lowering samples (use denoising to compensate), switching to GPU rendering, simplifying materials (reduce Subsurface Scattering, glass bounces), using Light Path tricks for invisible complexity, enabling persistent data, and optimizing tile size (large tiles for GPU, auto for CPU in Blender 4.x).

## Quick Wins (Minutes to Implement)

- **Enable denoising** — OpenImageDenoise (CPU) or OptiX Denoiser (NVIDIA). Lets you cut sample count by 50-75% with minimal quality loss.
- **Switch to GPU rendering** — Render Properties → Device → GPU Compute. Multiple GPUs scale nearly linearly.
- **Reduce Light Bounces** — Render Properties → Light Paths. Set Total to 8, Glossy to 4, Transmission to 8. Most scenes look identical at these values vs. unlimited.
- **Enable Persistent Data** — Render Properties → Performance → Persistent Data. Avoids reloading the BVH between frames in animations.

## Material Optimization

- **Subsurface Scattering** is expensive — use it only on hero objects. Background characters can use diffuse approximations.
- **Glass/Transmission** bounces are the biggest single performance hit. Reduce Max Bounces for Transmission or use the Light Path node's "Is Camera Ray" to swap glass for transparent on indirect rays.
- **Displacement** — use bump mapping instead of true displacement where possible. True displacement subdivides geometry.

## Scene-Level Optimization

- **Use instances** (Alt+D, not Shift+D) for repeated objects — one mesh in memory regardless of count.
- **Simplify panel** (Render Properties → Simplify) — globally reduce subdivision levels, texture resolution, and particle count for preview or draft renders.
- **Render Region** — in Viewport, press Ctrl+B to render only the area you're iterating on.

## Advanced

- **Adaptive Sampling** (on by default in 4.x) — automatically reduces samples in low-noise regions. Set noise threshold to 0.01 for production, 0.1 for previews.
- **Light Linking** (Blender 4.0+) — control which lights affect which objects, reducing unnecessary light calculations.
- **View Layer splitting** — render complex scenes in passes and composite them. Faster iteration on individual elements.

## Related

- [[shading-rendering.md|Shading & Rendering]]
- [[scene-optimization.md|Scene Optimization Workflow]]
- [[compositing.md|Compositing]]
