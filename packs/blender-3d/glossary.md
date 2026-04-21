---
title: Blender Glossary
type: glossary
tags: []
pack: blender-3d
retrieval_strategy: standard
id: blender-3d/glossary
verified_at: "2026-04-21"
verified_by: agent
schema_version: "4.1"
---

# Blender Glossary

Key terminology that confuses newcomers and intermediate users alike. Terms are grouped thematically rather than alphabetically for easier learning.

---

## Modes and Context

### Object Mode
The default mode when you open Blender. You can select, move, rotate, and scale entire objects. You cannot edit the geometry of a mesh — only the object's transform. Press `Tab` to toggle between Object Mode and Edit Mode. Most modifiers are visible and can be applied in Object Mode.

### Edit Mode
The mode for editing the actual geometry of a mesh, curve, or surface. Press `Tab` to enter/exit (when a mesh object is selected). In Edit Mode you see vertices, edges, and faces. Important: Edit Mode operates on the *object data* (the mesh), not the object itself — transforms in Edit Mode move vertices relative to the object's origin, not the object in the world.

### Sculpt Mode
A brush-based mode for organic deformation. Works on actual mesh geometry. Dyntopo (Dynamic Topology) can add/remove geometry on the fly. Multi-resolution sculpting lets you work at different subdivision levels non-destructively. `Ctrl+Tab` (in the viewport) opens the mode pie menu.

### Pose Mode
Exclusive to Armature objects. Allows you to pose bones and create animation keyframes. Pose Mode operates on the pose of the armature, not its rest position (which is edited in Edit Mode on the armature).

### Weight Paint Mode
Used to paint vertex weights — the influence each bone has on each vertex. Essential for rigging. Red = full influence (1.0), Blue = no influence (0.0). You must have an armature modifier and at least one vertex group to use this meaningfully.

### Vertex Paint / Texture Paint
Vertex Paint bakes colors directly to vertices (cheap, low resolution). Texture Paint paints onto UV-mapped image textures using brushes. These are different tools for different purposes.

---

## Geometry Types

### Mesh
The most common Blender object type. A collection of vertices, edges, and faces. Everything in 3D games and most rendering pipelines is ultimately a mesh. Blender's modeling, sculpting, and modifiers all operate on meshes.

### Curve
Bezier or NURBS path objects. Mathematically smooth — not made of polygons. Can be 2D or 3D. Used for: spline paths for animation, extrusion profiles, hair/fur curves, text outlines. Converting a Curve to a Mesh (`Alt+C` or Object → Convert) bakes the resolution into polygons.

### Surface
NURBS surface patches. Less commonly used than Meshes or Curves in modern Blender workflows. Useful for CAD-adjacent work and smooth surface construction.

### Armature
The skeleton object used for rigging. Contains bones organized in a hierarchy. Armatures deform mesh objects via the Armature Modifier. The rest position (T-pose or A-pose) is set in Edit Mode; poses are created in Pose Mode.

### Grease Pencil
A unique Blender object type that draws 2D strokes in 3D space. Each stroke is a curve with fill and stroke materials. Grease Pencil objects can be animated, use modifiers, and participate in 3D scenes alongside regular meshes. Used for 2D animation, storyboarding, and stylized illustration in 3D.

---

## Render Engines

### Cycles
Blender's physically-based path tracer. Traces rays of light through the scene, simulating real physics. Produces photorealistic results. Much slower than EEVEE but far more accurate — handles caustics, global illumination, realistic glass, subsurface scattering, and more. Supports CPU and GPU rendering. The GPU path (CUDA/OptiX for NVIDIA, HIP for AMD, Metal for Mac) is significantly faster.

### EEVEE
Blender's real-time rasterization engine. Uses the same node-based materials as Cycles but approximates lighting rather than simulating it. Dramatically faster than Cycles — renders in seconds to minutes vs minutes to hours. EEVEE Next (introduced in Blender 4.2) is a major rewrite with improved accuracy.

### EEVEE Next
The rebuilt version of EEVEE introduced in Blender 4.2. Adds ray-traced shadows, improved reflections, better subsurface scattering, and GPU-accelerated rendering. Still an approximation (not a path tracer), but significantly more accurate than classic EEVEE. Some features require newer GPUs.

### Workbench
Not really a "render engine" in the production sense — it's the solid viewport display mode. Fast but flat. Used for modeling and layout work, not final renders. Useful for checking proportions, testing rigs, or quick playblasts.

---

## Materials and Shading

### Shader Nodes
The node-based material system in Blender. Every material is a network of nodes that describes how light interacts with a surface. The Shader Editor workspace shows these nodes. Cycles and EEVEE share the same node system, though some nodes only work in Cycles.

### Principled BSDF
The all-in-one shader node that handles most real-world materials. A "kitchen sink" shader implementing Disney's PBR model. Key parameters: Base Color, Metallic (0=dielectric, 1=metal), Roughness (0=mirror, 1=fully rough), Normal (for normal maps), Specular (Fresnel effect), Emission. For 90% of materials, this is the only shader you need.

### PBR (Physically Based Rendering)
A rendering approach where material parameters correspond to real physical properties. PBR materials (Metallic/Roughness workflow) are portable — the same values look correct under any lighting. Base Color, Roughness, and Metallic are the core PBR parameters.

### HDRI (High Dynamic Range Image)
A 360° panoramic photo used as environment lighting. Contains actual light intensity data (not just color), so it creates realistic, complex lighting from a single image. Set in the World shader via an Environment Texture node. Free HDRIs available at Poly Haven (polyhaven.com).

### UV Map
A 2D coordinate system that maps 3D surface points to positions in a 2D texture image. "Unwrapping" a mesh means cutting it along seams and flattening it into UV space. Every vertex gets UV coordinates (U,V) from 0 to 1. Multiple UV maps can exist on one mesh — useful for lightmaps, decals, etc.

### Normal Map
A texture that encodes surface normal directions as RGB colors (blue-ish images). Fakes small-scale surface detail (bumps, scratches, pores) without adding actual geometry. Dramatically cheaper than real geometry. Must be connected to the Normal input of a shader node via a Normal Map node — never connect directly to a color input.

### Displacement
Actual geometry movement based on a texture. Unlike Normal Maps (which are an illusion), displacement physically moves vertices up or down. Requires sufficient geometry subdivision to look good. Cycles supports true micropolygon displacement; EEVEE uses a less accurate approximation.

---

## Scene Organization

### Data-Block
The fundamental building unit of Blender's internal data model. Everything is a data-block: meshes, materials, textures, node trees, armatures, images, scenes, objects, and more. Each has a name, a user count, and can be linked or appended from other .blend files. If a data-block has zero users, it is marked for deletion on save (unless "fake user" is set).

### Collection
Blender's organizational hierarchy. Collections hold objects (and other collections). Equivalent to layers in other software, but more flexible — objects can be in multiple collections simultaneously. Collections can be instanced as "Collection Instances" (essentially prefabs). Render visibility can be controlled per-collection.

### Object
A scene entity with a location, rotation, and scale (the "transform"). An Object references Object Data (a mesh, curve, armature, etc.) — the Object is just a container. Multiple Objects can share the same Object Data (instancing). This distinction is crucial for understanding linked duplicates (`Alt+D`) vs independent duplicates (`Shift+D`).

### Scene
A complete 3D environment within a .blend file. One .blend file can have multiple Scenes, each with their own objects, camera, and render settings. Scenes can share data via linking.

### View Layer
A sub-set of a Scene for rendering. Used to separate objects into render passes (foreground, background, effects) that can be composited together. One Scene can have multiple View Layers, each rendering different Collections.

---

## Modifier System

### Modifier
A non-destructive operation applied to an object that changes its appearance without permanently altering the underlying mesh. Modifiers stack — order matters. Common examples: Subdivision Surface, Mirror, Array, Bevel, Boolean, Solidify, Shrinkwrap, Armature, Lattice.

### Subdivision Surface
A modifier (and workflow) that smooths a mesh by subdividing it into smaller polygons following Catmull-Clark or Simple rules. Catmull-Clark rounds everything (organic look). Simple just subdivides without moving vertices (preserves shape). Level 2 in viewport, Level 3-4 for rendering is typical.

### Boolean
A modifier that performs Constructive Solid Geometry (CSG) operations: Union, Difference, Intersect. Used to cut holes, merge shapes, and create complex forms. Blender has two solvers: Fast (buggy, for simple cases) and Exact (slower, more reliable). Both can leave messy topology that needs cleanup.

### Solidify
Adds thickness to a thin mesh by extruding along normals. Essential for architectural elements, fabric, cards, thin objects. Has complex and simple modes; complex mode handles non-manifold geometry better.

### Array
Duplicates an object along an axis, along a curve, or at a fixed offset. Pairs beautifully with a Curve modifier to create chains, tracks, fences, rails.

### Bevel
Adds a chamfer/bevel to edges or vertices, creating smooth transitions. Can be weight-controlled (Bevel Weight per edge). In interactive mode: `Ctrl+B` for edge bevel, `Ctrl+Shift+B` for vertex bevel. The modifier version is non-destructive.

### Decimate
Reduces polygon count automatically. Useful for LOD generation, simplifying sculpts for rigging, or shrinking file size. Three modes: Collapse (merge nearby vertices), Un-Subdivide, Planar (merge coplanar faces).

---

## Animation

### Keyframe
A stored value at a specific frame. Blender interpolates between keyframes to create smooth motion. Press `I` in the viewport to insert keyframes for selected properties. Types: BEZIER (smooth), LINEAR, CONSTANT (stepped).

### Driver
A special keyframe mechanism that sets a property's value based on *another* property or a mathematical expression, rather than based on time/frame. Example: bone rotation drives a shape key blend factor. Drivers are Python expressions evaluated every frame.

### Shape Key
Stored vertex positions that can be blended between. Used for facial expressions, morphs, corrective shapes. Basis shape key is the neutral position; all others are offsets from it. Driven by drivers or keyframed via value slider.

### NLA Editor (Non-Linear Animation)
An editor for mixing, sequencing, and layering animation clips (called "Actions"). Allows non-destructive reuse of animations — push an Action down to the NLA, create strips, blend them together. Essential for game animation pipelines and complex character animation.

### Action
A named set of keyframes for an object or armature. A single armature can have multiple Actions (walk, run, jump), which are managed in the NLA Editor.

### Constraint
A rule that controls an object's or bone's transformation based on another object or target. Examples: Copy Location, Track To, IK (Inverse Kinematics), Follow Path, Stretch To. Constraints are non-destructive and evaluated every frame.

---

## Advanced Concepts

### Geometry Nodes
A visual, node-based system for creating and modifying geometry procedurally. Added to Blender in 2.92 and dramatically expanded in subsequent releases. Think of it as a programming language for 3D geometry, expressed as a node graph. Operates on a new data paradigm (geometry sockets, attributes, fields) distinct from the shader node system.

### Compositor
Blender's built-in node-based post-processing system. Operates on render output (and video input). Used for color grading, glare, depth-of-field, combining render passes (diffuse, specular, shadow), adding lens effects. The Compositor uses render passes from View Layers.

### Linked / Appended
Two ways to bring data from one .blend file into another. **Append** copies the data-block into the current file — it becomes independent. **Link** creates a live reference to the external file — the data can only be viewed/overridden, not directly edited. Linking is used in large production pipelines (assets in separate files, linked into shot files).

### Fake User
A flag (`F` toggle in data blocks) that keeps a data-block alive even when it has no actual users in the scene. Without a fake user, materials, textures, and node groups with zero users are purged on save. Always set fake user on materials or node groups you want to preserve.

### Pack / Unpack
Blender can embed (pack) external image files and other assets directly into the .blend file, making it self-contained. Use File → External Data → Pack Resources. Unpacking extracts them back to disk. Packed files make .blend files larger but portable.

### Origin
The pivot point of an object — the orange dot. Location, rotation, and scale all operate relative to the origin. The origin does NOT have to be at the center of the geometry. Moving the origin (`Right-click → Set Origin`) vs moving the geometry are different operations. Most modifiers (Mirror, Array, Screw) use the origin as their reference point.

### N Panel (Properties Panel)
The side panel in the 3D Viewport accessed by pressing `N`. Contains tabs for Item (object transform), Tool (tool settings), View (viewport settings), and any add-on panels. Calling something the "N Panel" is standard Blender community shorthand.

### T Panel (Toolbar)
The left toolbar in the 3D Viewport, accessed by pressing `T`. Contains tool buttons for the active mode.

### F-Curve (Function Curve)
The mathematical curve representing how an animated property changes over time. Viewable in the Graph Editor. Bezier handles let you control easing. F-Curves can be modified with modifiers (Cycles, Noise, etc.) for procedural animation variation.
