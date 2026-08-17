---
id: blender-3d/concepts/compositing-passes-exr
title: "Compositing — Render Passes, OpenEXR, and GPU"
type: concept
tags:
  - compositing
  - render-passes
  - openexr
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/compositing.md
related:
  - compositing-core.md
  - shading-cycles.md
content_hash: sha256:27aae2cdccb8181a670cd2fc9786bcbd335e602ac277b24cabd4fe82e8eb5ea2
---

# Compositing — Render Passes, OpenEXR, and GPU

Multi-pass compositing splits a render into diffuse, specular, emission, and mask components so you can grade and isolate without re-rendering. OpenEXR multilayer stores those passes in one 32-bit file; GPU compositing speeds the node graph in 4.x.

## Render Passes and Multi-Pass Compositing

Multi-pass compositing is the professional approach.

**The classic recombination:**
```
Diffuse Direct + Diffuse Indirect = Total Diffuse
Specular Direct + Specular Indirect = Total Specular
Total Diffuse + Total Specular + Emission + Environment = Reconstructed Image
```

By separating passes, you can boost reflections without affecting diffuse, change shadow color, remove environment noise without touching character passes, and adjust AO intensity separately.

### Cryptomatte — Object/Material Isolation Masks

Cryptomatte generates object isolation masks directly from a render — accurate edge anti-aliasing included.

**Enable:** View Layer Properties → Passes → `Cryptomatte Object` and `Cryptomatte Material`.

**Usage:**
1. Add `Cryptomatte` node (`Shift+A → Matte → Cryptomatte`)
2. Connect Render Layers `Image` and the crypto passes
3. Click `Pick`, then click any object in the rendered image
4. The Cryptomatte node outputs a `Matte` with a perfect edge-antialiased mask

This replaces the old manual "Object Index" pass workflow and is dramatically better at edges.

---

## OpenEXR Multilayer — The Pro Format

OpenEXR multilayer stores multiple render passes in a single file with 32-bit floating point precision. Lossless. Large files.

**When to use EXR:**
- Any project requiring compositing over multiple sessions
- When you might need to re-composite without re-rendering
- When client deliverables require raw passes

**When PNG is fine:**
- Personal projects, quick renders
- Final delivery only (not meant for compositing)

---

## GPU Compositing (4.x)

Enable in `Preferences → System → GPU Compositing`. With a capable GPU, compositing can be 5–20× faster. Most core nodes (Denoise with OptiX, Blur, Glare, Color Balance, Mix) have GPU support. Some matte operations remain CPU-only.

