---
title: Propositions — Concepts
type: proposition
tags:
- concepts
- propositions
pack: blender-3d
retrieval_strategy: standard
id: blender-3d/propositions/concepts
verified_at: '2026-04-10'
verified_by: agent
---

# Propositions — Concepts

Atomic factual statements extracted from the concepts files.

---

### core-architecture.md

- Everything in Blender is a data-block — a named, reference-counted container for a specific type of data.
- Every data-block has a user count; when the count reaches zero, the data-block is orphaned and purged on save/reload.
- The Fake User (`F` button) sets an artificial +1 to a data-block's user count, preventing it from being purged.
- `Shift+D` duplicates an object and gives the new object a *copy* of the mesh data; `Alt+D` creates a linked duplicate that shares the *same* mesh data-block.
- In Edit Mode on a linked duplicate, editing the mesh updates all objects that share that mesh.
- An Object stores location, rotation, scale, constraints, and modifiers — plus a reference to Object Data.
- Object Data (Mesh, Armature, Curve, etc.) is a separate data-block that multiple Objects can reference, enabling efficient instancing.
- Edit Mode operates on Object Data; if two objects share a mesh, editing one's mesh in Edit Mode updates both.
- Collections are Blender's organizational hierarchy; objects can belong to multiple collections simultaneously.
- A Collection Instance (`Add → Collection Instance`) is Blender's equivalent of a "prefab" — an instanced copy of an entire collection updated automatically when the original changes.
- Each View Layer defines which Collections are visible, enabling separate render passes from the same Scene.
- `bpy.data` accesses all data-blocks directly; `bpy.context` accesses current selection and mode state; `bpy.ops` calls operators.
- `bpy.data` is preferred for scripts; `bpy.ops` requires correct context (mode, selection) to work.
- The Info Log records every UI action as a Python command — the fastest way to learn the Python API for any operation.
- `.blend` files are binary archives; images can be embedded (packed) or referenced externally.
- Any data-block from any `.blend` file can be appended (copied) or linked (live reference) into another file.
- `Ctrl+Tab` opens a pie menu for mode selection; modes include Object, Edit, Sculpt, Weight Paint, Pose, and Particle Edit.
- Multiple objects can be in Edit Mode simultaneously (Blender 2.8+) by selecting all before pressing Tab.

---

### modeling-fundamentals.md

- Topology refers to the arrangement of vertices, edges, and faces; bad topology causes artifacts under Subdivision Surface, deformation problems in animation, and UV stretching.
- All-quad topology arranged in edge loops produces the most predictable subdivision, deformation, and UV results.
- A pole is any vertex where the number of connected edges is not 4; 5-poles cause pinching under Subdivision Surface and should be kept away from curved or deforming areas.
- Proportional Editing (`O`) causes edits to fall off gradually to surrounding vertices — the most common cause of "why did my whole mesh move?"
- `Dissolve (Ctrl+X)` removes geometry while preserving surrounding topology; `Delete` removes geometry and leaves holes.
- Modifier order in the stack matters enormously: Mirror before Subdivision Surface, Boolean before Solidify, Array before Curve.
- The Subdivision Surface modifier has separate Viewport and Render level settings — keep viewport at 1–2, render at 2–3.
- Crease (`Shift+E` in Edit Mode) sets a 0–1 value on edges; Crease=1 makes an edge resist Subdivision Surface smoothing without adding support loops.
- The Mirror modifier's Clipping option prevents vertices from crossing the mirror plane — essential for keeping seams tight.
- The Boolean modifier has Exact (reliable, slower) and Fast (buggy on edge cases) solvers; Exact is the default choice.
- Boolean operations almost always leave n-gons, tris, and poles that require manual topology cleanup.
- Non-manifold geometry (edges shared by more or fewer than 2 faces) causes problems with Solidify, 3D printing, Booleans, and physics.
- Unapplied scale (object scaled in Object Mode without `Ctrl+A → Scale`) causes inconsistent Subdivision Surface, wrong physics behavior, and texture scaling issues.
- QuadriFlow (built-in) and Instant Meshes (external free) are automated retopology tools that produce all-quad meshes from high-res geometry.
- After retopology, bake normal maps from the high-res sculpt onto the low-res retopo mesh to transfer surface detail.
- Smart UV Project (`U → Smart UV Project`) is fast but produces many small islands; seam-based Unwrap gives higher-quality results for textured objects.
- UV stretching is visible in the UV Editor with the Stretching overlay enabled; blue = compressed, red = stretched, green = no distortion.

---

### shading-rendering.md

- EEVEE is a rasterization renderer: fast, real-time, good for product viz, motion graphics, stylized output, and Grease Pencil.
- Cycles is a path-tracing renderer: physically correct for photorealism, transparent/refractive materials, caustics, and complex indirect lighting.
- EEVEE Next (Blender 4.2+) requires a GPU; CPU-only machines cannot use it.
- EEVEE screen-space reflections miss objects that are offscreen or behind the camera; Cycles handles all reflections physically.
- The Principled BSDF implements Disney's PBR model and handles ~90% of real-world materials.
- Metallic should be 0 (dielectric: plastic, wood, skin) or 1 (metal); values between are physically incorrect for photorealism.
- Base Color, Emission image textures must be set to sRGB color space; Roughness, Metallic, Normal, and AO maps must be set to Non-Color.
- Connecting a Normal Map image directly to the Normal input of Principled BSDF is wrong — it requires the Normal Map node to convert tangent-space colors to actual normal vectors.
- Adaptive Sampling stops sampling each pixel when it converges; it is enabled by default in modern Blender and dramatically reduces render times.
- OpenImageDenoise (OIDN) is CPU-based, high quality, and works on any machine; OptiX denoiser is NVIDIA-only, faster, and slightly lower quality.
- Per-frame animation denoising can produce temporal flickering; temporal denoising in DaVinci Resolve or NeatVideo produces better results.
- The Indirect Light Clamp setting (`Render Properties → Light Paths → Clamp → Indirect Light: 10–15`) eliminates fireflies at the cost of slight energy loss.
- Never render animation directly to a video file; render image sequences first, then compile to video — a crash won't lose all frames.
- True displacement (Cycles only) requires enabling Displacement in Material Settings and sufficient geometry (use Adaptive Subdivision).
- Poly Haven (polyhaven.com) provides free CC0 HDRIs up to 16K resolution and is the definitive free HDRI source.
- AgX (Blender 4.0+) is the recommended view transform; it has better chromatic accuracy in highlights than Filmic.
- Film Transparent (`Render Properties → Film → Transparent`) renders an alpha channel, required for compositing over other footage.

#### EEVEE Next Migration (4.2+)

- EEVEE Next world volume shaders completely block distant light (sun lights and world lights); old scenes with world volume + sun will render dark — convert the volume to a physical mesh object via the Help menu conversion operator.
- EEVEE Next shadow system replaces per-light shadow resolution with a "Resolution Limit" setting; old files with low shadow resolution may trigger "Shadow buffer full" errors or massive performance drops.
- Contact Shadows are removed in EEVEE Next — the new shadow maps are accurate enough; scenes relying on Contact Shadows may need Resolution Limit lowered to prevent light leaking.
- Bloom is removed as a render setting in EEVEE Next (4.2+) and replaced by the realtime compositor Glare node with Bloom type; any tutorial showing Render Properties > Bloom is outdated.
- Material "Blend Mode" is replaced by "Render Method" in EEVEE Next; reproducing Alpha Clip behavior requires adding a Greater Than Math node in the shader tree.
- Screen Space Refraction and Light Probe Planes no longer work with Blended render method in EEVEE Next; the only workaround is switching to Dithered render method + enabling Raytracing.
- EEVEE Next at default settings renders slower than old EEVEE — the architecture trades speed for correctness; studios may need separate material versions for 3.6, 4.1, and 4.2+.
- Translucent BSDF behavior changed in EEVEE Next: to reproduce 4.1 results, connect a Value node (value=0) to the Thickness socket of Material Output.
- Light Probe Volumes in EEVEE Next only record diffuse lighting — all specular/glossy is converted to diffuse (known limitation); baked data is now stored in the probe object and requires re-baking.

---

### animation-rigging.md

- An F-Curve is a single animated property; a set of F-Curves grouped together is an Action, which functions as an animation clip.
- An Action has a user count; Actions with no users are purged on save unless given a Fake User (`F` in the Action dropdown).
- Visual Keying captures the object's actual viewport position (after constraints/IK), not the raw pre-constraint channel values.
- Auto-Keying automatically creates keyframes for any changed property while playing or paused; pair with `Replace` mode to only key properties that already have keyframes.
- Extrapolation mode `Make Cyclic` repeats an F-Curve for looping; the Cycles modifier is more flexible for walk cycles, allowing Repeat with Offset for root motion.
- F-Curve Noise modifier adds procedural noise (camera shake, organic variation) to any animated channel without keyframes.
- Drivers link one property to another via a Python expression rather than to time; they are evaluated every frame.
- Use Drivers (not keyframes) for: shape keys controlled by bone rotation, wheel rotation tied to movement, reactive material properties.
- The Rotation Difference variable type in Drivers returns the angle between two bones — the standard way to drive corrective shape keys.
- IK (Inverse Kinematics) automatically solves a bone chain to reach a target; use IK for feet on ground, hands grabbing fixed objects, and any endpoint that must hit a specific world position.
- FK (Forward Kinematics) gives direct control over each bone; use for arcs, swings, and any motion where the endpoint position is a result, not a goal.
- The IK Pole Angle parameter offsets the pole target direction — adjust in 90° increments until the knee/elbow points correctly.
- Automatic Weights (`Ctrl+P → With Automatic Weights`) is a starting point for mesh binding; always refine with Weight Paint.
- Auto Normalize in Weight Paint keeps all vertex weights summed to 1.0 across all bones — always enable this for correct deformation.
- NLA strips can be layered using blend types: Replace (default), Add, Subtract, Multiply, Combine.
- Additive NLA tracks allow independent actions (breathing, blinking) to layer on top of primary animations.
- Shape Keys store vertex position offsets from the Basis shape; the Basis is mandatory and is always the neutral/rest position.
- Corrective shape keys (driven by Rotation Difference) fix mesh collapse at joints when the character bends.
- Before FBX/GLTF export for game engines, bake constraint/IK results to pure keyframes using `Object → Animation → Bake Action`.

---

### physics-simulation.md

- Always bake physics simulations to disk before rendering — simulations are not deterministic if re-run per frame during render.
- Blender's Rigid Body system is built on the Bullet physics library.
- Use Convex Hull collision shape for active rigid body objects — Mesh shape is 100× slower and often unstable for active objects.
- Rigid body bakes to object keyframes (visible in Dope Sheet), unlike Cloth and Fluid which bake to point cache files on disk.
- Rigid Body World Substeps per Frame (default 10) should be increased to 20–40 for fast-moving objects; Solver Iterations should be increased to 20–60 for stacked/piled objects.
- Soft Body simulates volumetric elastic deformation; Cloth simulates surface fabric — use Soft Body for jelly/rubber, Cloth for fabric/flags.
- Cloth pinning uses a vertex group: vertices with weight 1.0 are pinned (don't move), vertices with weight 0.0 are fully simulated.
- Cloth self-collision must be enabled for fabric that bunches up on itself; collision objects need a Collision physics property with appropriate Thickness.
- Mantaflow (integrated in Blender 2.82) is the current fluid and gas simulation engine.
- Fluid simulation Resolution Divisions (voxel count): 32 = very low/testing, 128–256 = production; a 200-frame 128-resolution bake can take 30 minutes to several hours.
- Smoke fire is configured by setting Flow object Fuel > 0; the `Flame` attribute (0–1) is automatically available in the domain material.
- Particle Object rendering creates one instance of a specified object per particle — 100,000 object instances is manageable due to GPU instancing.
- Hair particles in Blender 4.x have been largely superseded by the dedicated Curves object type, which integrates with Geometry Nodes and has dedicated sculpt brushes.
- Force fields (Wind, Vortex, Turbulence, etc.) affect particles and soft/rigid bodies; combine Wind + Turbulence for natural fire buoyancy.
- The Geometry Nodes Simulation Zone (Blender 4.0+) enables stateful per-frame simulation within the Geometry Nodes editor.
- Blender's physics assume real-world scale: 1 Blender unit = 1 meter; physics that behave wrongly are often caused by objects at incorrect scale.
- Physics caches grow large: a 200-frame 128-resolution fluid simulation can be 5–50GB.

---

### geometry-nodes.md

- Geometry Nodes is a modifier type that processes geometry through a user-defined node graph — a visual functional programming environment for 3D geometry.
- Geometry Nodes was introduced in Blender 2.92 (2021) and is one of the fastest-evolving parts of Blender.
- A field in Geometry Nodes is NOT a single value — it is a recipe for computing a value per element (vertex, face, point); connecting `Position` passes a per-element position, not a constant.
- The `Distribute Points on Faces` node accepts a density field, enabling per-face density variation driven by textures or attributes.
- `Instance on Points` places lightweight instances at each point — 10,000 tree instances consume only 1 tree's worth of geometry memory.
- `Realize Instances` converts instances to actual geometry — potentially freezing the viewport and creating enormous mesh data; avoid unless editing individual instance elements is required.
- The `Simulation Zone` (Blender 3.6+) uses Simulation Input and Simulation Output nodes to create a stateful loop that runs once per frame, enabling custom particle systems and physics.
- Simulation Zone must be evaluated sequentially from frame 1; jumping to frame 100 requires computing frames 1–99. Always bake before rendering animation.
- Use Group Nodes (`Ctrl+G`) to encapsulate repeated Geometry Nodes logic into reusable, labeled sub-graphs.
- Geometry Nodes is excellent for: scatter/distribution workflows, procedural/parametric shapes, simulation, and motion graphics.
- Geometry Nodes is NOT efficient for: detailed hand-crafted organic modeling, character rigging, material setup, or post-processing.
- The Viewer node (`Shift+Ctrl+click` any output) previews intermediate geometry values without full evaluation of the graph.
- Custom attributes stored via `Store Named Attribute` persist through the Geometry Nodes stack and can be read/written by any node.
- Attribute domains: Point (per vertex/point), Edge, Face, Face Corner (for UV seams), Instance (per instance in a collection).
- Built-in geometry attributes include: `position` (Vector), `normal` (Vector), `index` (Integer), `material_index` (Integer).

#### Advanced Patterns (community-sourced)

- Verlet integration in a Simulation Zone with nested Repeat Zone (8-12 iterations) enables custom rope/soft body physics: new_pos = current + (current - previous) × 0.98 + gravity × dt², with distance constraints solving in the repeat loop for rigidity.
- The two-node pattern for cross-geometry attribute transfer is Sample Nearest → Sample Index: Sample Nearest finds the closest point index on the target, Sample Index reads the value at that index — required for transferring attributes between mesh and curve types.
- The Transform node operates on entire geometry as a single matrix transform; Set Position evaluates a field per element — using Set Position for a uniform translation on 100k+ vertex meshes is measurably slower than Transform.
- The Geometry to Instance node converts each input to a lightweight instance before Join Geometry, dramatically improving performance when merging 50+ procedural segments (road systems, modular architecture).
- Disabling a Geometry Nodes modifier in the viewport (eye icon off) does not fully stop evaluation if other modifiers reference its output; use a Switch node connected to an exposed boolean input to truly bypass computation.
- Geometry Nodes animation playback is measurably slower in Blender 4.3 compared to 3.6 for complex setups — a known regression; baking geometry or using viewport simplification are the current workarounds.
- Cycles rendered viewport with many GeoNodes instances is dramatically slower in camera view than perspective view due to BVH rebuilding for instanced geometry within camera bounds.

---

### python-scripting.md

- `bpy.data` accesses the internal data model directly with no context requirements; `bpy.ops` simulates UI actions and requires correct context (mode, selection state, active editor).
- Prefer `bpy.data` for reading/setting properties in scripts; use `bpy.ops` only when no direct data API equivalent exists.
- `bpy.data.objects.get("Name")` returns None if not found (safe); `bpy.data.objects["Name"]` raises KeyError.
- `bmesh` is the in-memory mesh editing API — faster and lower-level than operators; in Edit Mode use `bmesh.from_edit_mesh()`, in Object Mode use `bmesh.new()` then write back with `bm.to_mesh()`.
- `bpy.context.temp_override()` (Blender 3.2+) is the modern way to set context for operator calls that require a specific area or mode.
- Custom operators inherit from `bpy.types.Operator` with `bl_idname` (CATEGORY_OT_name), `bl_label`, `bl_options = {'REGISTER', 'UNDO'}`.
- The `@persistent` decorator on app handlers keeps them alive when a new `.blend` file is loaded; without it, handlers are cleared on file load.
- The depsgraph (`bpy.context.evaluated_depsgraph_get()`) provides evaluated geometry after all modifiers; access via `obj.evaluated_get(depsgraph)`.
- Blender can run headlessly with `blender --background` (or `-b`), enabling scripted batch rendering and processing.
- Pass custom arguments to a headless script using `--` separator: `blender -b scene.blend --python script.py -- --arg value`.
- Creating a data-block without linking it to a scene object gives it zero users — it will be purged on save; use `use_fake_user = True` to prevent this.
- After changing mesh properties via the data API, call `obj.data.update()` to force viewport refresh.
- Multi-file add-on structure: `__init__.py` (bl_info + register/unregister), separate modules for operators, panels, and utilities.
- Application handlers include: `frame_change_pre/post`, `render_pre/post/complete`, `load_pre/post`, `save_pre/post`, `depsgraph_update_post`.

---

### sculpting.md

- Blender sculpting has three paradigms: Dyntopo (dynamic mesh generation), Multi-Resolution (subdivision levels), and Remeshing (voxel/quad cleanup).
- Dyntopo dynamically adds and removes triangles under the brush; it destroys UV maps, vertex groups, and shape keys in sculpted areas.
- Dyntopo is best for freeform concept sculpting and exploration from a rough base; NOT for final production sculpting or after retopology.
- For hard-surface Dyntopo sculpting, use Constant Detail mode at 2.0–4.0, Refine method "Subdivide Edges" only, detail size 3.5px for mechanical parts, and run Detail Flood Fill after major strokes to regularize density.
- Multi-Resolution (Multires) preserves the base mesh topology while enabling sculpting at multiple subdivision levels independently.
- Multires sculpting follows a macro-to-micro funnel: levels 1–2 for major forms, 3–4 for secondary forms (muscle groups), 5–6 for fine detail (pores, wrinkles).
- Voxel Remesh (`Ctrl+R` in Sculpt Mode) creates a watertight all-quad mesh from a voxel representation; it loses UV maps and vertex groups.
- Quad Remesh (4.x) uses the instant-meshes algorithm to generate quad-dominant retopology from a sculpt — good starting point, usually needs cleanup.
- MatCap shading (Viewport Shading → MatCap) removes material rendering overhead and shows surface detail clearly; recommended during sculpting.
- Face Sets (Blender 2.91+) are colored per-face regions for isolating brushes to specific areas; `Alt+H` hides everything except the face set under the cursor.
- Automask options (Topology, Face Sets, Normal Limit) restrict brush strokes automatically based on topology or angle, preventing unintended bleed-through.
- The Smooth brush is available by holding `Shift` with any brush active.
- Multires level 6 on a 5000-vertex base mesh = ~20 million vertices in memory; 32GB RAM is comfortable, 16GB will struggle.
- For manual retopology in Blender, enable `Face Snap` with `Project Individual Elements` and use a Shrinkwrap modifier set to Nearest Surface Point.
- Baking normals: select the low-poly retopo mesh, `Shift+select` the high-poly sculpt, enable `Selected to Active`, and bake with type Normal.

---

### compositing.md

- Blender's Compositor is a node-based post-processing system operating on render output, render passes, and imported images/video.
- The Viewport Compositor (Blender 4.0+) runs in real-time in the 3D Viewport for preview color grading; it is not a replacement for the full Compositor.
- The Render Layers node is the primary compositor input; enable specific render passes in View Layer Properties → Passes before rendering.
- Denoising passes (Denoising Albedo and Denoising Normal) must be enabled in View Layer → Passes for the Denoise node to achieve best quality.
- OIDN v2 (Blender 4.x) is significantly better than older OIDN versions; the Prefilter: Accurate setting gives highest quality for stills.
- Per-frame Cycles denoising produces temporal flickering in animation ("swimming" fine details); DaVinci Resolve or NeatVideo temporal denoising eliminates this.
- AgX (Blender 4.0+) is the recommended view transform; it maintains color hue in bright highlights better than Filmic.
- Cryptomatte (View Layer → Passes → Cryptomatte Object/Material) generates edge-antialiased per-object isolation masks — superior to the old Object Index workflow.
- Multi-pass compositing separates Diffuse Direct, Diffuse Indirect, Specular, Emission, Shadow, and AO passes for independent per-pass adjustment.
- The Shadow pass shows shadow contribution as a dark value; reroute through Color Balance to change shadow color or tint.
- Glare node types: Bloom (soft glow), Ghosts (aperture lens flares), Streaks (star-burst), Fog Glow (diffuse spread); set Threshold > 1.0 to only affect genuinely bright lights.
- OpenEXR Multilayer stores multiple render passes in a single file with 32-bit floating point precision; the professional standard for any project requiring re-compositing.
- GPU compositing (Blender 4.0+, enabled in Preferences → System → GPU Compositing) provides 5–20× speedup for supported nodes.
- The `Is Camera Ray` output of the Light Path node allows showing a solid color background while using an HDRI for lighting.

---

### video-editing.md

- The VSE (Video Sequence Editor) is Blender's built-in non-linear video editor; it is functional for assembly, basic color grading, and audio mixing but is not competitive with DaVinci Resolve or Premiere for professional work.
- Scene Strips (`Shift+A → Scene`) render a Blender Scene directly into the VSE, allowing late-breaking changes without pre-rendering.
- Gamma Cross crossfade corrects for gamma during blending, avoiding the "midpoint dip" of uncorrected linear blending — always prefer Gamma Cross over Cross for dissolves.
- `K` (razor cut) cuts all strips at the current frame; `Shift+K` is a soft cut that keeps both halves.
- Proxies (lower-resolution copies of footage) are essential for editing 4K+ footage smoothly; built via Strip Properties → Proxy/Timecode → Rebuild Proxy.
- Speed Control strips with speed factor < 1.0 create slow motion; slow motion requires high-FPS source footage (60, 120, or 240fps).
- For web video delivery, H.264 in MP4 is the standard codec; for professional post-production deliverables, ProRes (Apple) or DNxHD (Avid) are appropriate.
- Never render VSE output to video directly for long animations — render image sequences, then compile to video to protect against crash data loss.
- Stamp metadata (Output Properties → Metadata) burns filename, date, frame number, and custom text into rendered images — useful for review cuts and dailies.
- VSE text strips are functional but limited; complex title cards are better created as 3D objects/Geometry Nodes in the viewport and rendered as PNG sequences.
- DaVinci Resolve is recommended over the VSE for: multi-camera editing, professional color science, significant audio mixing, and broadcast/film delivery.
