---
title: Summary — Workflows Overview
type: summary
tags:
- summaries
- workflows-overview
pack: blender-3d
retrieval_strategy: standard
id: blender-3d/summaries/workflows-overview
verified_at: '2026-04-10'
verified_by: agent
---
# Summary — Workflows Overview

This summary covers all 5 workflow files in the Blender 3D pack. For detailed information, follow the links to source files.

---

## Character Animation — Rig, Animate, Export

The full pipeline: Armature rigging → Mesh binding → Walk cycle → Lip sync → NLA layering → Game engine export.

**Rigging essentials:**
- Use `.L` / `.R` bone naming suffixes (not `_Left`) for Mirror X and Symmetrize to work
- Rigify (built-in add-on) generates production-ready FK/IK rigs from a positioned meta-rig — fastest path for humanoids
- Manual rigging: IK constraint on the chain's last bone, Pole Target to control elbow/knee direction, adjust Pole Angle in 90° increments
- Automatic Weights = starting point only; always refine with Weight Paint (Auto Normalize always ON)

**Walk cycle (8-frame at 24fps):**
- Frame 1: Contact L (left heel strikes, right toe off); Frame 3: Down (lowest point); Frame 5: Contact R; Frame 7: Down R
- Hips: 5–10° left-right rotation, 2–4cm up-down translation, lateral sway over weight-bearing leg
- Shoulders counter-rotate opposite to hips; arms swing opposite to legs
- Loop: copy frame 1 to frame 9 → Cycles F-Curve modifier or Extrapolation → Cyclic

**Lip sync:**
- Shape Keys for phoneme groups (M/B/P, OOH, EE/I, AH/AA, F/V, TH, L/D/N)
- Timing: 0 two frames before phoneme, 0.8–1.0 at peak, ramp to 0 over 2–4 frames
- Rhubarb Lip Sync / Papagayo-NG for automated phoneme timing from audio

**NLA workflow:**
- Push Actions down → NLA strips; layer additive tracks (breathing, blinks) on top with blend type Add/Combine
- Before game export: `Object → Animation → Bake Action` with Visual Keying to flatten all NLA to pure keyframes

→ Source: [[character-animation.md]]

---

## Hard Surface Modeling — SubD, Boolean, Polish

The foundational workflow: **low-poly control cage + Subdivision Surface modifier**.

**Core workflow:**
1. Build control cage (~50–200 polys), all quads
2. Apply scale (`Ctrl+A → Scale`) before anything else
3. Add Subdivision Surface (viewport level 1–2, render level 2–3)
4. Add support loops flanking sharp edges (2 loops per edge, one each side)
5. Model should look correct at Level 2 — if not, fix topology, don't raise the level

**Key rules:**
- Shade Smooth is required after SubD for correct shading
- Poles on curved areas = star shading artifacts; move poles to flat areas
- Modifier stack: Mirror → Bevel (angle-based) → SubD
- Boolean stack: Boolean (Exact solver) → Bevel → SubD
- Boolean cleanup: Merge by Distance → knife new loops through n-gons → Dissolve unnecessary edges
- Mirror seam fix: enable Clipping in Mirror modifier

**Key tools:**
- Bevel (`Ctrl+B`): scroll = segment count, `P` = profile, `C` = clamp overlap
- Loop Cut (`Ctrl+R`): scroll before click = multiple parallel loops
- Inset (`I`): `I` again = per-face mode; essential for panel lines and recessed detail
- Knife (`K`): `Z` = cut-through, `C` = 45° constraint

→ Source: [[hard-surface-modeling.md]]

---

## Motion Graphics — Procedural and Shader-Driven Animation

MoGraph in Blender uses Geometry Nodes for procedural motion + EEVEE for fast iteration.

**Geometry Nodes patterns:**
- `Scene Time` node (Seconds, Frame) = keyframe-free time source for all procedural animation
- Staggered instance animation: `Index ÷ count = stagger` → subtract from global time → Smooth Step for easing → per-instance timing offset
- Vertex wave: `X position × frequency + Scene Time × speed → Sine → amplitude → Set Position Z`
- Typewriter text (4.x): `String to Curves` + animated `Slice String` count

**Shader-driven animation:**
- Keyframe shader node values directly in the Shader Editor (`I` over the value)
- Object custom property + Driver → shader input = material reacting to animated properties
- Animated Noise Texture W channel = organic "breathing" surface without rigs

**Camera animation:**
- Follow Path constraint + Track To Empty = decoupled camera movement and look-at (easier to control than keyframed camera)
- Overshoot handles in Graph Editor = springy MoGraph landing feel
- F-Curve Noise modifier = procedural camera shake without keyframes

**Loops:**
- Cycles F-Curve modifier (Repeat) = infinite keyframe-free loop
- Geometry Nodes loop: `Scene Time (Seconds) → Modulo (loop_duration) → Divide by loop_duration` = 0–1 loop value at any frame

**Rendering:**
- Iterate in EEVEE (10–100× faster); switch to Cycles for final frames only
- Bake Geometry Nodes simulations before final render

→ Source: [[motion-graphics.md]]

---

## Product Visualization — Studio Lighting and Materials

Professional product rendering prioritizes material accuracy, controlled lighting, and camera precision.

**Studio lighting (three-point):**
- Key: Area light, 45° from camera, 30° above, 100–500W
- Fill: opposite side, 25–50% of key strength
- Rim: behind/above, 50–150% of key for edge separation
- HDRI at 0.2–0.5 strength for ambient fill; area lights for controlled highlights (hybrid approach)
- Sweep background: curved floor-to-wall plane eliminates the visible corner

**Material presets (Principled BSDF):**
- Polished chrome: Metallic=1.0, Roughness=0.05–0.15
- Brushed metal: Metallic=1.0, Roughness=0.4, Anisotropic=0.7–0.9
- Clear glass: Transmission=1.0, IOR=1.52, Roughness=0.0; glass needs physical thickness (≥1–2mm)
- Rubber: Roughness=0.8–1.0, Sheen Weight=0.3–0.5
- Always add Noise Texture to Roughness input at 0.05–0.15 to break up uniform surfaces

**Camera:**
- 50mm = natural; 85–100mm = consumer goods; 135–200mm = jewelry/watches
- DoF: F/8–16 for full sharpness, F/2.8–4.0 for selective focus

**Turntable:**
- Empty parent rotated 0°→360° with Linear F-Curve interpolation (constant speed)
- 240 frames = 10 seconds at 24fps; lights either fixed (highlight sweep) or rotating with product (static look demo)

**Render:**
- Cycles: 512–2048 samples, Glossy bounces=8, Transmission=12, Film Transparent ON
- Render to multilayer EXR for compositing flexibility

→ Source: [[product-visualization.md]]

---

## Scene Optimization — Viewport, Render, and Render Farm

Blender performance problems are usually: too much unique geometry, too many textures in VRAM, or wrong render settings.

**Viewport performance:**
- Instancing is the highest-leverage optimization: `Alt+D` (linked duplicate), Collection Instances, GeoNodes `Instance on Points`
- Subdivision Surface viewport level: set to 1 (or 0 for off-camera); render level: 2–3
- Particle system viewport: 10–25% display; render: 100%
- Per-object: set Display As Bounds for distant objects; disable viewport visibility for objects not needed

**Render performance (Cycles):**
- Samples: use Adaptive Sampling + denoising rather than high raw counts
- GPU rendering: set in Preferences → System → Cycles Render Devices, then Render Properties → Device: GPU Compute
- Light path bounces: reduce Total to 8, Diffuse to 3; keep Glossy at 4, Transmission at 8+ for glass
- Simplify (Render Properties → Simplify): non-destructive global texture/subdivision cap for test renders

**VRAM management:**
- Reduce texture resolution, pack RGB/A channels into single textures, convert 32-bit EXR to 8-bit PNG where precision isn't needed
- Out-of-core rendering (Preferences → System → Cycles): textures in CPU RAM, slower but allows scenes larger than VRAM

**Render farm prep:**
- `File → External Data → Make All Paths Relative` (convert all absolute paths)
- Bake all physics simulations to shared network storage before submitting
- All render nodes must use the exact same Blender version
- Per-node render command: `blender -b scene.blend -o //renders/frame_#### -s 1 -e 100 -a`
- Portal lights at window openings dramatically improve interior scene convergence

→ Source: [[scene-optimization.md]]
