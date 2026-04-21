---
title: Blender Community Mining — 2026-03-13
type: source
tags:
- community-mining
- blender-community
pack: blender-3d
retrieval_strategy: standard
id: blender-3d/_community-mining-2026-03-13
verified_at: "2026-04-21"
verified_by: agent
schema_version: "4.1"
---

# Blender Community Mining — 2026-03-13

Sources: Blender Stack Exchange, Blender Developer Blog, Blender Projects tracker, Polycount, community forums.
Purpose: High-EK findings to integrate into pack files for improved EK ratio.

---

## Category 1: EEVEE Next Migration (4.2 LTS)

### 1.1 World Volume Blocks All Distant Light
- **Source:** developer.blender.org/docs/release_notes/4.2/eevee_migration
- **Content:** In EEVEE Next (4.2+), world volume shaders now completely block distant light (world lights and sun lights). Old scenes with world volume + sun light will go dark. Fix: convert the volume to a physical mesh object. A conversion operator appears in Help menu or World > Volume panel — but only if there's something to convert.
- **Target:** concepts/shading-rendering.md

### 1.2 Shadow System Completely Rewritten
- **Source:** developer.blender.org/docs/release_notes/4.2/eevee_migration
- **Content:** Sun light shadow resolution settings cannot be auto-converted. The new "Resolution Limit" setting replaces per-light resolution. If your old resolution was much lower than the new default, expect massive performance penalty or "Shadow buffer full" errors. Fix: increase Resolution Limit to lower resolution. Contact Shadows are removed entirely — the new shadow maps are accurate enough. Soft Shadows moved from global render setting to per-light "Jitter" option (disabled by default). Jittered shadows are off in viewport by default for performance.
- **Target:** concepts/shading-rendering.md

### 1.3 Bloom Removed as Render Setting
- **Source:** developer.blender.org/docs/release_notes/4.2/eevee_migration
- **Content:** The Bloom feature and its render pass are removed in EEVEE Next. Replaced by the realtime compositor Glare node (Bloom type). Old files must be manually adjusted: add a Glare node in compositor, enable compositor in Shading popover for viewport preview. Every tutorial showing Render Properties > Bloom is outdated for 4.2+.
- **Target:** concepts/shading-rendering.md, concepts/compositing.md

### 1.4 Material Blend Mode → Render Method
- **Source:** developer.blender.org/docs/release_notes/4.2/eevee_migration
- **Content:** "Blend Mode" (Alpha Clip, Opaque, Alpha Blend) replaced by "Render Method". To replicate old Alpha Clip behavior, add a Greater Than Math node in the shader tree. Simple materials auto-convert; complex node setups with mixed alpha need manual conversion. Shadow Mode replaced by Object > Visibility > Ray Visibility Shadow.
- **Target:** concepts/shading-rendering.md

### 1.5 Screen Space Refraction Broken with Blended Render Method
- **Source:** developer.blender.org/docs/release_notes/4.2/eevee_migration
- **Content:** Screen Space Refraction and Light Probe Planes no longer work with Blended render method (formerly Alpha Blend). The only workaround: switch to Dithered render method and enable Render Settings > Raytracing. This breaks glass/water materials that relied on Alpha Blend + SSR.
- **Target:** concepts/shading-rendering.md

### 1.6 EEVEE Next Performance Regression
- **Source:** projects.blender.org/blender/blender/issues/128253
- **Content:** EEVEE Next at default settings renders slower than old EEVEE. This is expected — the new architecture trades some speed for correctness. Studios maintaining production files need to keep separate EEVEE/EEVEE Next versions of their assets. Shader setups changed between 3.6 → 4.1 → 4.2, meaning potentially three material versions.
- **Target:** concepts/shading-rendering.md

### 1.7 Light Probe Volume Changes
- **Source:** developer.blender.org/docs/release_notes/4.2/eevee_migration
- **Content:** Light Probe Volume sample locations and influence volumes changed. May need manual scale-up to avoid light leaking. New "Surfel Resolution" option may need tweaking for baking older scenes. Baked data is now stored in the probe object itself — requires re-baking with Scene > Light Probes > Bake All. Probe spheres and planes now only record diffuse lighting — all specular/glossy is converted to diffuse (known limitation).
- **Target:** concepts/shading-rendering.md

### 1.8 Translucent BSDF Behavior Change
- **Source:** developer.blender.org/docs/release_notes/4.2/eevee_migration
- **Content:** Translucent BSDF now uses a more accurate approximation when thickness ≠ 0. To get old 4.1 behavior, connect a Value node (value=0) to the Thickness socket of Material Output. Subsurface Translucency is always evaluated now (was previously a toggle). The result depends on the Thickness socket output for inner absorption — and shadow maps can refine it via Material > Settings > Thickness From Shadow.
- **Target:** concepts/shading-rendering.md

---

## Category 2: Expert Workflow Tricks

### 2.1 GeoNodes Performance: Set Position vs Transform Node
- **Source:** blender.stackexchange.com/questions/297620
- **Content:** For entire geometry (all elements), always use the Transform node — it operates on the whole geometry as a single matrix transform. The Set Position node evaluates a field per element. For selective operations (with a selection mask), use Set Position. Wrong choice on 100k+ vertex meshes causes measurable viewport lag.
- **Target:** concepts/geometry-nodes.md

### 2.2 Caustics Faking in EEVEE
- **Source:** blender.stackexchange.com/questions/265789 (community technique)
- **Content:** Create a plane with Geometry Nodes generating many small distorted sub-planes. Material: Transparent BSDF + Glossy BSDF mixed via Light Path "Is Camera Ray" with IOR=1.45. Position the caustic plane 0.001 units above water surface. Only works in EEVEE — breaks in Cycles. This is the standard community workaround for EEVEE's lack of native caustics.
- **Target:** workflows/product-visualization.md or concepts/shading-rendering.md

### 2.3 Texture Baking: Exploded Mesh Technique
- **Source:** polycount.com/discussion/217954 (game art pipeline)
- **Content:** When baking normal maps from high-poly to low-poly with multiple separate mesh elements, move each element far apart ("explode" the mesh) so rays from one element don't hit neighboring elements. This allows higher ray cast distances without cross-element bleeding. Essential for game asset baking where multiple hard-surface parts share a UV atlas.
- **Target:** concepts/sculpting.md or new workflows/game-asset-pipeline.md

### 2.4 Texture Baking: Cage vs Ray Distance
- **Source:** blender.stackexchange.com/questions/267718, blender.stackexchange.com/questions/210570
- **Content:** "Extrude" inflates the low-poly mesh outward to cast rays inward (changing ray origin). "Max Ray Distance" discards hits beyond a threshold (filtering ray results). They serve different purposes — Extrude controls where rays start, Max Ray Distance controls how far they travel. Using only Extrude with no cage causes rays from a uniformly inflated mesh, which fails on concave areas. A manually created cage mesh (same topology, ballooned out) gives much better control for complex shapes. Tip: color cage and high-poly differently to verify no poke-through.
- **Target:** concepts/sculpting.md

### 2.5 FBX Export: Negative Scale Inverts Normals
- **Source:** reddit.com/r/unrealengine (multiple threads)
- **Content:** Objects with negative scale in Blender (e.g., mirrored via S, X, -1) export to FBX with inverted normals. The FBX exporter applies scale on export, flipping the winding order. Fix: apply scale (`Ctrl+A > Scale`) before export, or use Mirror modifier instead of negative scale. This is the single most common "my model looks inside-out in Unreal" issue.
- **Target:** new section in troubleshooting/common-mistakes.md or workflows/game-export.md

### 2.6 FBX Export: Axis Conversion and Unity Rotation -90
- **Source:** reddit.com/r/gamedev, Unity Discussions
- **Content:** Blender uses Z-up; Unity uses Y-up. The FBX exporter adds a -90° X rotation on the root object to compensate. In Unity, this shows as a root transform of (-90, 0, 0). Fix for Unity 2020.1+: disable "Use Space Transform" in Blender's FBX export, then enable "Bake Axis Conversion" in Unity's FBX import settings. For Unreal: apply transforms in Blender before export and use "FBX Unreal" export preset.
- **Target:** troubleshooting/common-mistakes.md or new workflows/game-export.md

### 2.7 Shade Smooth Breaks FBX Normals in Unity
- **Source:** discussions.unity.com/t/shade-smooth-in-blender-breaks-unity-import-of-fbx
- **Content:** Blender's Shade Smooth (especially Auto Smooth in 4.1+) can produce normals that the FBX exporter writes incorrectly for some engines. Fix: triangulate mesh before export (preserves exact shading), or add a Triangulate modifier as the last modifier. Also: clean degenerate faces before export — Unity's "Remove Degenerate" import option can silently delete faces.
- **Target:** troubleshooting/common-mistakes.md

### 2.8 Weight Painting: Shoulder Deformation Requires Twist Bones
- **Source:** blender.stackexchange.com/questions/62735, blenderartists.org/t/shoulder-topology
- **Content:** No amount of weight painting fixes shoulder twist deformation on its own. The problem is anatomical: the shoulder joint needs a twist bone (or twist chain) between the upper arm and the shoulder to distribute rotation. Without twist bones, raising the arm past 90° causes volume loss. Rigify includes twist bones by default. For manual rigs: add a bone between shoulder and upper_arm, constrained with Copy Rotation (Influence 0.5) to split the twist. The topology must also have horizontal edge loops around the armpit — vertical-only loops collapse.
- **Target:** workflows/character-animation.md

### 2.9 Weight Painting: Gradient Tool for Joint Falloff
- **Source:** studio.blender.org/training/weight-painting, CyPaint guides
- **Content:** The Gradient tool in Weight Paint mode creates a linear falloff between two clicked points — far more precise than brush painting for joint transitions. Click on the bone center, drag to the joint boundary. For fingers: use Gradient from knuckle to fingertip with Auto Normalize enabled. For shoulders: Gradient from upper arm to torso. Always test in Pose mode immediately after — Blender's real-time weight paint deformation preview shows problems instantly.
- **Target:** workflows/character-animation.md

---

## Category 3: Geometry Nodes Advanced Patterns

### 3.1 Verlet Integration for Custom Rope/Soft Body Physics
- **Source:** blender.stackexchange.com/questions/289500 (community pattern)
- **Content:** Pure GeoNodes rope simulation using Verlet integration: In Simulation Zone, store previous position as named attribute. In nested Repeat Zone (8-12 iterations): new_pos = current + (current - previous) × 0.98 + gravity × dt². Set previous = current, current = new_pos. Output to Simulation Output. Damping factor 0.98 prevents energy explosion. Add distance constraints in the Repeat Zone for rope rigidity: if distance between consecutive points > rest_length, move both points toward each other.
- **Target:** concepts/geometry-nodes.md

### 3.2 Attribute Transfer: Mesh ↔ Curve
- **Source:** blender.stackexchange.com/questions/280123
- **Content:** To transfer attributes from a mesh to a curve (or vice versa): temporarily convert curve to mesh with "Curve to Mesh" (minimal profile). Use "Sample Nearest" on the temporary mesh to find closest point indices. Use "Sample Index" with those indices to read attributes from the source. Delete the temporary mesh. This two-node pattern (Sample Nearest → Sample Index) is the standard for cross-geometry-type attribute transfer.
- **Target:** concepts/geometry-nodes.md

### 3.3 Geometry to Instance Node for Join Performance
- **Source:** blender.stackexchange.com/questions/296524
- **Content:** When joining large geometries with "Join Geometry", performance degrades linearly with input count. The "Geometry to Instance" node converts each input to a lightweight instance first, then joins — dramatically faster for 50+ inputs. Use this pattern when merging procedurally generated segments (road systems, modular architecture). Warning: the result is instances, not real geometry — further per-vertex operations require Realize Instances.
- **Target:** concepts/geometry-nodes.md

### 3.4 GeoNodes Playback Regression in 4.x
- **Source:** blender.stackexchange.com/questions/331384
- **Content:** Geometry Nodes playback performance is measurably slower in Blender 4.3 compared to 3.6 for complex animated setups. Known issue. Workarounds: bake geometry to avoid per-frame recalculation (Object > Geometry Nodes > Bake), replace objects with bounding boxes in viewport during animation playback, use viewport simplification. If a specific project depends on GeoNodes animation performance, staying on 3.6 LTS or 4.2 LTS may be necessary.
- **Target:** concepts/geometry-nodes.md or troubleshooting/common-mistakes.md

### 3.5 Hidden GeoNodes Still Consume Resources
- **Source:** blender.stackexchange.com/questions/256580
- **Content:** Geometry Nodes modifiers that are disabled in viewport (eye icon off in modifier stack) still consume memory and some CPU during evaluation if they have side effects or if other modifiers reference their output. To truly disable a GeoNodes modifier for performance: either delete it, or bypass it with a Switch node connected to a boolean input exposed on the modifier panel. Simply hiding the object also doesn't prevent GeoNodes evaluation in all cases.
- **Target:** concepts/geometry-nodes.md

### 3.6 Realize Instances in Camera View Performance Bug
- **Source:** projects.blender.org/blender/blender/issues/98257
- **Content:** Cycles rendered viewport with many GeoNodes instances is dramatically slower in camera view than in perspective view. Adding a Realize Instances node before output fixes the camera-view slowdown but increases memory. This is a known Cycles viewport rendering bug related to BVH building for instanced geometry in camera bounds. Workaround: use Realize Instances only for final render, or switch to perspective view during viewport iteration.
- **Target:** concepts/geometry-nodes.md

---

## Category 4: Production Pipeline

### 4.1 Geometry Nodes Instances Don't Export to FBX/glTF Without Realize
- **Source:** blender.stackexchange.com/questions/322491, blenderartists.org
- **Content:** GeoNodes instances are not automatically realized during FBX or glTF export. The export silently produces an empty or incomplete file. Fix: add Realize Instances before the Group Output, OR use `Ctrl+A > Visual Geometry to Mesh` instead of applying the modifier (which fails on curve objects). For curve-based GeoNodes setups, applying the modifier is outright impossible — you must use Visual Geometry to Mesh.
- **Target:** troubleshooting/common-mistakes.md or new file

### 4.2 Realize Instances Loses Material Assignments on Export
- **Source:** blender.stackexchange.com/questions/296927
- **Content:** After Realize Instances, materials assigned per-instance via "Set Material" node may not transfer correctly to glTF/FBX. The attribute domain changes from "Instancer" to "Geometry" — the shader must be updated to read the attribute from the correct domain. For glTF export specifically: materials assigned via GeoNodes attributes are not preserved; you must use Set Material Index node and have actual material slots on the target object.
- **Target:** troubleshooting/common-mistakes.md

---

## Category 5: Sculpting & Retopology

### 5.1 Dyntopo Settings for Hard Surface
- **Source:** blender.stackexchange.com/questions/240123 (community pattern)
- **Content:** For hard-surface concept sculpting with Dyntopo: use Constant Detail mode at 2.0-4.0 (not Relative). Refine method: "Subdivide Edges" only (not Collapse or both). Detail size 3.5px is the community-recommended sweet spot for mechanical parts. Run "Detail Flood Fill" after major strokes to regularize density. Switch to Smooth Shading during sculpting to see hard-surface flow clearly.
- **Target:** concepts/sculpting.md

### 5.2 Retopology Face Flow for Animation
- **Source:** blenderartists.org/t/shoulder-topology, Polycount game art threads
- **Content:** Critical edge loop placement for animated characters: (1) Horizontal loops around the armpit — vertical-only loops collapse when arm raises. (2) Circular loops around the mouth — 3 concentric rings minimum for speech animation. (3) Loops following the nasolabial fold for facial expressions. (4) Loops around the eyes following the orbicularis oculi muscle shape. (5) A loop at the wrist/ankle to provide a clean deformation boundary. The deformation quality of a character mesh is determined at the retopology stage, not the weight painting stage.
- **Target:** concepts/sculpting.md or workflows/character-animation.md

### 5.3 Normal Baking: Selected to Active Split Normals Trap
- **Source:** blender.stackexchange.com/questions/210570, Polycount
- **Content:** When baking normals with Selected to Active, if the low-poly mesh has sharp edges (split normals / custom normals), the baked normal map must account for the split. If the low-poly uses flat shading but the normal map was baked assuming smooth shading, the result has visible seam artifacts at sharp edges. Solution: mark all edges as smooth on the low-poly, bake, then re-apply sharp edges with Auto Smooth. The normal map "encodes" the smoothing, and sharp edges "subtract" it — getting this order wrong doubles the sharpness or cancels it.
- **Target:** concepts/sculpting.md
