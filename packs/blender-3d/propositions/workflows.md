---
title: Propositions — Workflows
type: proposition
tags:
- propositions
- workflows
pack: blender-3d
retrieval_strategy: standard
id: blender-3d/propositions/workflows
verified_at: '2026-04-10'
verified_by: agent
---

# Propositions — Workflows

Atomic factual statements extracted from the workflow files.

---

### character-animation.md

- Blender's `.L` / `.R` bone naming suffix enables Mirror X and Symmetrize operations; use `.L` and `.R` (not `_Left` or `_Right`).
- Bone roll (the local X axis rotation) must be consistent across a rig; inconsistent rolls cause twisted deformation and IK flipping.
- Rigify (included add-on) generates a production-ready FK/IK rig with switching from a positioned meta-rig; enable via Preferences → Add-ons → Rigging: Rigify.
- IK chain requires: a control bone at the endpoint (outside the chain), an IK constraint on the chain's last deform bone, a Chain Length, and optionally a Pole Target.
- The IK Pole Angle is adjusted in 90° increments; if the knee flips, adjust the pole target position or pole angle.
- Automatic Weights (`Ctrl+P → With Automatic Weights`) is a starting point for mesh-to-armature binding — always refine with Weight Paint.
- The Weight Paint Gradient tool creates a linear weight falloff between two click points — far more precise than brush painting for joint transitions; use from bone center to joint boundary with Auto Normalize enabled.
- Shoulder deformation cannot be fixed by weight painting alone — it requires twist bones (a bone chain between shoulder and upper_arm with Copy Rotation at Influence 0.5) to distribute rotation across multiple bones.
- The armpit must have horizontal edge loops (wrapping around the arm like rings); vertical-only loops collapse when the arm raises past 90°.
- Corrective Shape Keys driven by a Rotation Difference driver automatically activate as joints bend to restore volume that weight painting can't preserve.
- Critical retopology edge loop placements for animation: horizontal rings at armpit (2+), 3 concentric loops around mouth, loops following nasolabial fold, 2+ concentric rings around eyes, clean loops at wrist/ankle boundaries.
- A model with correct edge loop placement and automatic weights deforms better than a model with bad topology and hours of manual weight painting.
- In a walk cycle, the contact pose (heel strikes ground) occurs at frames 1 and 5 (for an 8-frame cycle at 24fps); the down pose (body lowest) at frame 3, passing pose at frame 5.
- Hips in a walk cycle rotate left-right (~5–10°), translate up-down (~2–4cm bobbing), and sway side-to-side over the weight-bearing leg.
- Shoulders counter-rotate opposite to hips in a walk cycle: left shoulder forward when the right leg is forward.
- To loop a walk cycle, copy frame 1 keyframes to the loop end frame, then use F-Curve Extrapolation Mode → Cyclic or the Cycles modifier with Repeat (in-place) or Repeat with Offset (root motion).
- Lip sync uses Shape Keys for phoneme shapes (M/B/P, OOH, EE/I, AH/AA, F/V, TH, L/D/N) driven by keyframed Value sliders.
- Standard lip sync timing: set shape key value to 0 two frames before the phoneme, ramp to 0.8–1.0 at the peak, ramp back to 0 over 2–4 frames.
- Rhubarb Lip Sync and Papagayo-NG are external tools that analyze audio and output phoneme timings applicable to Blender shape keys via Python script.
- NLA strips are pushed down from the Action Editor with the Push Down button (↓ arrow); the Action then exists as an NLA strip and the Action slot is freed for a new clip.
- Additive NLA tracks (blend type: Add or Combine) layer secondary animations (breathing, blinking, hair sway) on top of primary motion without replacing it.
- Before export to game engines, bake all NLA contributions to a single Action via `Object → Animation → Bake Action` with Visual Keying enabled.
- Animation quality checklist: squash/stretch, anticipation, follow-through, ease in/out F-curves, overlap timing, IK integrity, 24fps viewport playback.

---

### hard-surface-modeling.md

- Hard surface modeling in Blender centers on a clean low-poly control cage + Subdivision Surface modifier; the cage defines shape, support loops control edge sharpness.
- A model should look correct at Subdivision Level 2; if it doesn't, fix the topology — don't increase to Level 3 to hide problems.
- Support loops (holding edges) are placed close to the edge to sharpen; most sharp edges need 2 support loops — one on each side.
- Shade Smooth must be applied after adding Subdivision Surface for correct normal-based shading on hard surface models.
- Incorrect normals (faces pointing inward) appear black; fix with `Mesh → Normals → Recalculate Outside` (`Shift+N` in Edit Mode).
- `Overlay → Face Orientation` shows blue (correct outward normals) and red (inverted normals).
- For Boolean cleanup: `Merge by Distance`, then manually route edge loops from the cut to restore quad flow, using `Knife (K)` to add connecting edges through n-gons.
- The "Boolean float" technique accepts messy topology after Boolean and relies on smooth shading with auto-smooth edges — valid for background objects and game assets at distance.
- Classic hard surface modifier stack: Mirror → Bevel (angle-based) → Subdivision Surface.
- Hard surface with Boolean stack: Boolean → Bevel (angle-based) → Subdivision Surface.
- Bevel (`Ctrl+B`) scroll wheel changes segment count; `P` adjusts profile shape; `C` enables Clamp Overlap (prevents bevel going past adjacent geometry).
- Mirror seam is fixed by enabling Clipping in the Mirror modifier and increasing Merge Distance if vertices aren't connecting.
- Poles in curved areas cause star-shaped shading artifacts under Subdivision Surface; move poles to flat areas.
- Non-planar quads create twisted faces that subdivide oddly; fix with `Face → Flatten Faces` or retopologize.
- Shade Auto Smooth (Blender 4.1+) automatically detects smooth vs sharp edges based on angle threshold.

---

### motion-graphics.md

- The `Scene Time` node in Geometry Nodes exposes the current frame (Frame) and elapsed time in seconds (Seconds) as outputs — the core of keyframe-free procedural animation.
- Staggered instance animation pattern: `Index → Divide by count → stagger_factor`, then subtract from global time to give each instance a unique time offset.
- The `Map Range (Type: Smooth Step)` node provides S-curve ease-in/ease-out on any procedural value without keyframes.
- A sinusoidal vertex wave requires: Position → separate X → Multiply (frequency) → Add (Scene Time × speed) → Sine → Multiply (amplitude) → Set Position Z offset.
- Geometry Nodes text animation (Blender 4.x) uses `String to Curves` with an animated `Slice String` count for a typewriter effect.
- Any Shader node value can be keyframed directly in the Shader Editor by pressing `I` over the value field.
- Connecting an object custom property to a shader via a driver enables the material to react to the object's animated properties.
- Animated Noise Texture with time input on the W channel creates procedural organic surface animation ("breathing" material) without rigs or shape keys.
- Camera Shake is added without keyframes using an F-Curve Noise modifier on location/rotation channels; Scale controls frequency, Strength controls intensity.
- For the `Follow Path` camera rig: draw a Bezier curve, add Follow Path constraint to the camera, add Track To constraint targeting an Empty at the scene center.
- EEVEE Bloom settings for MoGraph neon: Threshold 0.8, Radius 6, Intensity 0.05–0.2; combine with Emission Strength 3–10 on emissive materials.
- For seamless animation loops, use the Cycles F-Curve modifier (Repeat mode) or a Geometry Nodes Modulo of Scene Time Seconds by the loop duration.
- Bake Geometry Nodes simulations before final render: `Object → Geometry Nodes → Bake` prevents recomputation during rendering.
- EEVEE renders 10–100× faster than Cycles; build and iterate MoGraph animations in EEVEE, switch to Cycles only for final frames when needed.

---

### product-visualization.md

- Standard product studio three-point setup: Key (Area, 45° from camera, 30° above), Fill (opposite side, 25–50% of key strength), Rim (behind/above, 50–150% of key strength for edge separation).
- The hybrid HDRI + area light approach is standard in commercial product rendering: HDRI at low strength (0.2–0.5) for ambient fill, area lights for controlled highlights.
- A sweep background (curved floor-to-wall plane) eliminates the visible corner; alternatively, use a pure white World Background at high strength (3–5) for a blown-out white look.
- To rotate HDRI environment without affecting the visible background, use a Light Path `Is Camera Ray` mix to show a solid color to the camera while the HDRI lights the scene.
- Polished aluminum/chrome: Metallic=1.0, Roughness=0.05–0.15; Brushed metal: Metallic=1.0, Roughness=0.4, Anisotropic=0.7–0.9; Clear glass: Transmission=1.0, IOR=1.52, Roughness=0.0.
- Real glass objects need actual physical thickness (at least 1–2mm) for refraction to render correctly in Cycles; a single plane with glass material refracts incorrectly.
- Correct IOR values: crown glass=1.52, borosilicate=1.47, crystal=1.54, water=1.333 — wrong IOR makes glass look plastic.
- Add a Noise Texture mixed into the Roughness input at low strength (0.05–0.15) to break up uniformly perfect surfaces — real surfaces always have roughness variation.
- Focal length dramatically affects product feel: 50mm is natural, 85–100mm gives moderate compression for consumer goods, 135–200mm gives strong compression for jewelry/watches.
- For turntable animation: use an Empty parent rotated from 0° to 360° with Linear F-Curve interpolation (constant speed, no easing); 240 frames = 10 seconds at 24fps.
- Product render Cycles settings: Samples 512–2048, Glossy bounces 8, Transmission bounces 12, Film Transparent ON, OIDN denoiser.
- Missing subsurface scattering on organic products (candles, soaps) makes them look plastic; `Subsurface Weight: 0.1–0.5`, `Subsurface Radius: (1.0, 0.2, 0.1)` for warm SSS.
- Area lights smaller than their intended specular highlight look like point lights — size the area light larger than the intended highlight.
- Render to multilayer EXR with Diffuse, Glossy, Shadow, and AO passes for maximum post-processing flexibility without re-rendering.

---

### scene-optimization.md

- Before optimizing, identify the actual bottleneck: viewport slowness (Statistics overlay), render slowness (Render Statistics), or file size (External Data → Find Missing Files).
- Every unique object has its own draw call; instances share one draw call — instancing is the single highest-leverage viewport performance optimization.
- Linked Duplicates (`Alt+D`) share Object Data; Collection Instances make entire collections a single instanced object; Geometry Nodes Instance on Points creates thousands of instances at negligible overhead.
- Set Subdivision Surface Viewport Level to 1 (or 0 for off-camera objects) and Render Level to 2–3.
- Adaptive Subdivision (Cycles Experimental): subdivides geometry at render time based on screen-space size, giving dense close-up detail with no overhead for distant objects.
- Particle System viewport display should be 10–25% of total count; only render at 100%.
- The relationship between samples and noise reduction is approximately `sqrt(n)`: 4× samples = 2× noise reduction — use adaptive sampling + denoising rather than high raw sample counts.
- When VRAM is exceeded, Cycles falls back to CPU RAM (dramatically slower) or crashes; reduce texture resolution, pack channels, or convert 32-bit EXR textures to 8-bit PNG.
- `Render → Simplify → Texture Limit` non-destructively caps all texture resolutions globally — use during test renders, disable for final.
- Before render farm submission, convert all paths to relative with `File → External Data → Make All Paths Relative`.
- Physics simulations must be baked to disk with a cache path on shared storage accessible by all render farm nodes.
- For distributed rendering: each node renders a frame range; `blender -b scene.blend -o //renders/frame_#### -s 1 -e 100 -a` renders frames 1–100.
- All render farm nodes must use the exact same Blender version — different versions can produce different shader results, noise patterns, and adaptive subdivision behavior.
- Portal lights at window openings in interior scenes guide sampling toward the sky, dramatically improving convergence for daylit interiors.
- Combining multiple render passes (Diffuse Direct + Indirect, Specular Direct + Indirect) in the compositor enables per-component adjustment without re-rendering.
