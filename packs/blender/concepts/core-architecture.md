# Blender Core Architecture

Understanding Blender's internal data model is the single most important piece of knowledge for becoming a proficient Blender user. Everything — the behavior of linked duplicates, why deleting an object doesn't delete its mesh, how instancing works, why modifiers sometimes behave unexpectedly — stems from understanding this architecture.

---

## The Data-Block System

Everything in Blender is a **data-block**. A data-block is a named, reference-counted container for a specific type of data. Examples:

| Data-Block Type | What It Stores |
|----------------|----------------|
| `Object` | Transform (location/rotation/scale), constraints, modifiers |
| `Mesh` | Vertices, edges, faces, UVs, vertex groups |
| `Material` | Shader node tree, surface/volume/displacement settings |
| `Image` | Pixel data (packed or external reference) |
| `Armature` | Bone hierarchy and rest positions |
| `Action` | Keyframe data for an animatable thing |
| `NodeTree` | A node group (shader, geometry nodes, compositor) |
| `Scene` | Everything in a scene (lights, camera, settings) |
| `Collection` | A group of objects |

### Why Data-Blocks Matter

**Reference counting:** Each data-block has a user count. When you "delete" an object, you decrement its user count. If it reaches zero, the data-block is orphaned — it will be purged on save/reload. This is why you can lose work: delete an object, and unless something else references its mesh, the mesh disappears on save.

**Fake User:** The `F` button next to any data-block's name sets a "fake user" — an artificial +1 to the user count. This prevents purging. Use it on materials, node groups, and textures you want to keep even if nothing currently uses them.

**Browsing data-blocks:** In most property panels and fields, you can click the data-block selector to browse all available blocks of that type in the file. This is how you reuse materials, swap meshes, or assign multiple objects to the same Action.

**Practical consequence:** If you duplicate an object with `Shift+D`, the new object gets a *copy* of the object data (mesh). If you duplicate with `Alt+D`, both objects share the *same* mesh data-block. Edit the mesh of one, and both update. This is a linked duplicate / instance.

---

## Object vs Object Data

This distinction trips up almost everyone initially.

**Object** = the scene entity with:
- Location (X, Y, Z in world space)
- Rotation (Euler or Quaternion)
- Scale (X, Y, Z)
- Constraints
- Modifiers
- Object properties (visibility, display settings)
- A reference to Object Data

**Object Data** = the actual content:
- For a Mesh object: a Mesh data-block (vertices, edges, faces)
- For an Armature: an Armature data-block (bones)
- For a Curve: a Curve data-block (spline points, settings)
- For a Light: a Light data-block (type, color, intensity)

Multiple Objects can reference the same Object Data. This is how Blender does efficient instancing — 1000 objects can all point to the same mesh, with each object having its own transform, but the mesh data stored only once.

In the Properties panel, the Object properties (orange square icon) affect the Object; the Object Data properties (green triangle for mesh, curve icon for curves, etc.) affect the underlying data.

**Edit Mode operates on Object Data.** When you `Tab` into Edit Mode, you are editing the shared mesh data-block. If two objects share the same mesh and you edit it in Edit Mode (via either object), *both objects update*. This surprises people who use `Alt+D` without understanding the implication.

To make an Object Data independent (break the link): in the header where the mesh name is shown, click the number next to the name (indicating user count) — this "makes single user" and creates a copy.

---

## Collections

Collections are Blender's organizational hierarchy — the equivalent of "layers" in other software, but more powerful.

**Key properties:**
- Objects can belong to multiple collections simultaneously
- Collections nest inside each other
- Each collection has its own viewport/render visibility toggles
- Collections can have an offset (for instancing)
- Collections appear in the Outliner as a hierarchy

**Viewport visibility toggles** (in Outliner header — enable with the filter icon):
- Eye icon: viewport visibility (doesn't affect render)
- Camera icon: render visibility  
- Select icon: whether objects in the collection can be selected
- Disable in Viewport icon: hides from viewport entirely (performance)

**Collection Instances:** You can create an instance of an entire collection as a single object (`Add → Collection Instance`). This is Blender's equivalent of a "prefab" or "block" in CAD software. The instanced collection's objects appear in the viewport but are not directly selectable — only the empty object representing the instance is. Modifying the original collection updates all instances. Essential for repeated architectural elements, scatter workflows, and linked asset libraries.

**View Layer collection override:** Each View Layer has its own collection visibility settings (Layer Collections). You can render the same Scene with different Collections visible in each View Layer, then composite them together.

---

## Scenes and View Layers

**Scenes** are top-level containers within a .blend file. Each Scene has:
- Its own set of objects (or shared objects via linking)
- Its own Camera and World settings
- Its own render settings
- Its own View Layers
- Its own Timeline

Multiple Scenes are useful for:
- Separate render setups (preview vs final quality settings)
- Multi-camera setups
- The Compositor can combine output from multiple Scenes

**View Layers** subdivide a Scene's render into separate passes. Use cases:
- Character on one View Layer, background on another → composite with separate shadow control
- Effects elements isolated for compositing control
- Render one layer with reflection, another without, blend in compositor

Each View Layer defines which Collections are visible (Layer Collections). This is how professionals break complex scenes into manageable render passes.

---

## The Mode System

Blender is a modal application — different modes expose different tool sets. The current mode is shown in the top-left of the 3D Viewport header.

| Mode | Access | What You Can Do |
|------|--------|----------------|
| Object Mode | `Tab` (from Edit), `Ctrl+Tab` pie menu | Select/transform objects, add/delete objects, manage collections |
| Edit Mode | `Tab` | Edit mesh vertices/edges/faces, curve points, armature bones |
| Sculpt Mode | `Ctrl+Tab` pie | Brush-based mesh deformation, dynamic topology |
| Vertex Paint | `Ctrl+Tab` pie | Paint vertex colors directly on mesh |
| Weight Paint | `Ctrl+Tab` pie | Paint bone influence weights |
| Texture Paint | `Ctrl+Tab` pie | Paint onto UV-mapped image textures |
| Pose Mode | `Ctrl+Tab` pie (on armature) | Pose bones, create animation keyframes |
| Particle Edit | `Ctrl+Tab` pie | Edit particle/hair placement manually |

**Important mode rules:**
- You can only enter Edit Mode on the *active* object
- In Edit Mode, selecting something in the Outliner won't switch your active mesh — you must exit first
- Weight Paint mode requires an Armature modifier AND at least one vertex group
- `Ctrl+Tab` opens a pie menu for mode selection (faster than dropdown)
- You *can* have multiple objects in Edit Mode simultaneously (Blender 2.8+): select multiple objects before pressing `Tab`

---

## The Editor System

Blender's interface is divided into **Editors** — functional workspaces that can be tiled arbitrarily. Any region can display any editor type. There are no fixed panels — it's all configurable. The default screen layout is `Layout` workspace.

### Primary Editors

**3D Viewport:** The main 3D working area. Can show Object Mode, Edit Mode, etc. Multiple 3D Viewports can be open simultaneously with different camera angles.

**Outliner:** Hierarchical view of all data in the file. Shows scenes, collections, objects, materials, constraints. The Outliner is the only place to manage certain visibility flags that aren't in the viewport.

**Properties:** The big panel on the right. Organized into tabs (icons down the side):
- Scene Properties (camera, render engine settings)
- Render Properties (samples, output format)
- Output Properties (file path, frame range)
- View Layer Properties (render passes, AOVs)
- Scene Properties (gravity, audio settings)
- World Properties (environment lighting)
- Object Properties (visibility, display settings)
- Object Modifier Properties (the modifier stack)
- Object Data Properties (mesh/curve-specific settings)
- Material Properties (material slots and surface settings)
- Particles, Physics, Constraints tabs

**Shader Editor:** Node graph for materials. Shows the node tree for the active material. The World node tree (for environment/HDRI lighting) is also accessible here.

**Geometry Nodes:** Node graph for procedural geometry modifiers. Each Geometry Nodes modifier on an object has its own node tree.

**Timeline / Dope Sheet / Graph Editor / NLA Editor:** Animation editors. All show keyframe data at different levels of abstraction:
- Timeline: simple overview, scrubbing
- Dope Sheet: all keyframes across all objects/bones
- Graph Editor: F-Curves with bezier handles for fine animation control
- NLA Editor: Action clips layered as strips

**Image Editor / UV Editor:** Image Editor shows images (rendered output, textures). UV Editor shows UV maps and allows manual UV editing (it's the same editor, just activated in "UV Editing" mode).

**Compositor:** Node graph for post-processing render output. Works on rendered images, video, and render passes.

**Video Sequence Editor (VSE):** Non-linear video editing. Strips of video, audio, images, effects. Blender's least-loved editor but functional for basic editing.

**Text Editor:** Write Python scripts, add-ons, or any text directly in Blender.

### Workspaces

Blender comes with predefined workspace layouts accessible via tabs at the top:
- `Layout` — general 3D work
- `Modeling` — optimized for mesh editing
- `Sculpting` — full-screen sculpt
- `UV Editing` — 3D viewport + UV editor side by side
- `Texture Paint` — 3D viewport + Image editor
- `Shading` — 3D viewport + Shader Editor + Image editor
- `Animation` — 3D viewport + Dope Sheet/Graph Editor + Timeline
- `Rendering` — Camera view + Image Editor (for viewing renders)
- `Compositing` — Compositor + Image Editor
- `Geometry Nodes` — 3D viewport + Geometry Nodes editor
- `Scripting` — Text Editor + Python Console + Info log

These are just presets — you can create custom workspaces and rearrange editors freely.

---

## Blender's Python API

Almost everything visible in Blender's UI is accessible and scriptable via Python. The `bpy` module is the entry point.

**Key submodules:**
- `bpy.data` — Access all data-blocks in the file: `bpy.data.objects`, `bpy.data.materials`, `bpy.data.meshes`, etc.
- `bpy.context` — Access the current state: active object, selected objects, current mode, active view layer
- `bpy.ops` — Call operators (the same operations triggered by menu/keyboard): `bpy.ops.mesh.extrude_region()`, `bpy.ops.object.modifier_add(type='SUBSURF')`
- `bpy.props` — Register custom properties for add-ons
- `bpy.types` — Extend or register custom types, panels, operators

**The Data API vs the Operator API:**
- `bpy.data` operates directly on data — it's the preferred way to get/set values in scripts
- `bpy.ops` runs operators — these have side effects, require context (active object, correct mode), and are less predictable in scripts
- Prefer `bpy.data` for reading/setting properties; use `bpy.ops` only when no direct data API equivalent exists

**Context sensitivity:** Many operators require a specific state (correct mode, something selected, cursor in the right editor). In scripts, use `with bpy.context.temp_override(...)` to set context for operator calls. This replaced the old `override` dict pattern.

**The Info Log:** Every action you do in Blender's UI generates a Python command that appears in the Info Log (Window → Toggle System Console on Windows, or read from the Info editor). This is the fastest way to learn the Python API for any operation — do it manually, then read the corresponding Python command.

---

## The .blend File Format

The `.blend` file is a binary format containing all data-blocks in the file. Understanding its properties:

- **Self-contained by default:** All meshes, materials, node trees, and scenes are embedded. Images can be embedded (packed) or referenced externally.
- **Backward compatible:** Older .blend files can be opened in newer Blender versions with automatic conversion. Forward compatibility (newer files in older versions) is not guaranteed.
- **Appendable/Linkable:** Any data-block from any .blend file can be appended (copied) or linked (live reference) into another file. This is the basis for professional asset libraries and production pipelines.
- **Compression:** Blender can use LZ4 or Zstandard compression for .blend files. Compressed files are significantly smaller but slightly slower to open.
- **Recovery:** Blender auto-saves to a temp file and keeps quit.blend (the file state when Blender was closed). Accessible via File → Recover.
