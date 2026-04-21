---
id: blender-3d/concepts/core-architecture-editors
title: "Core Architecture — Mode System and Editors"
type: concept
tags:
  - architecture
  - editors
  - modes
  - workspaces
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-04-21"
verified_by: agent
supersedes:
  - concepts/core-architecture.md
related:
  - core-architecture-data-blocks.md
  - core-architecture-blend-file.md
---

# Core Architecture — Mode System and Editors

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

**Important rules:**
- You can only enter Edit Mode on the *active* object
- Weight Paint mode requires an Armature modifier AND at least one vertex group
- `Ctrl+Tab` opens a pie menu for mode selection (faster than dropdown)
- You *can* have multiple objects in Edit Mode simultaneously (Blender 2.8+): select multiple objects before pressing `Tab`

---

## Primary Editors

**3D Viewport:** The main 3D working area. Can show Object Mode, Edit Mode, etc. Multiple 3D Viewports can be open simultaneously.

**Outliner:** Hierarchical view of all data in the file. Shows scenes, collections, objects, materials, constraints. The only place to manage certain visibility flags.

**Properties:** Organized into tabs (icons down the side):
- Render Properties (samples, output format)
- Output Properties (file path, frame range)
- View Layer Properties (render passes, AOVs)
- World Properties (environment lighting)
- Object Properties (visibility, display settings)
- Object Modifier Properties (the modifier stack)
- Object Data Properties (mesh/curve-specific settings)
- Material Properties (material slots and surface settings)
- Particles, Physics, Constraints tabs

**Shader Editor:** Node graph for materials. Also accesses the World node tree.

**Geometry Nodes:** Node graph for procedural geometry modifiers.

**Animation editors:**
- Timeline: simple overview, scrubbing
- Dope Sheet: all keyframes across all objects/bones
- Graph Editor: F-Curves with bezier handles for fine animation control
- NLA Editor: Action clips layered as strips

**Compositor:** Node graph for post-processing render output.

**Video Sequence Editor (VSE):** Non-linear video editing. Strips of video, audio, images, effects.

**Text Editor:** Write Python scripts, add-ons, or any text directly in Blender.

---

## Workspaces

Predefined workspace layouts accessible via tabs at the top:
- `Layout` — general 3D work
- `Modeling` — optimized for mesh editing
- `Sculpting` — full-screen sculpt
- `UV Editing` — 3D viewport + UV editor side by side
- `Shading` — 3D viewport + Shader Editor + Image editor
- `Animation` — 3D viewport + Dope Sheet/Graph Editor + Timeline
- `Rendering` — Camera view + Image Editor
- `Compositing` — Compositor + Image Editor
- `Geometry Nodes` — 3D viewport + Geometry Nodes editor
- `Scripting` — Text Editor + Python Console + Info log

These are presets — you can create custom workspaces and rearrange editors freely.

---

## Blender's Python API

Almost everything visible in Blender's UI is accessible and scriptable via Python. The `bpy` module is the entry point.

**Key submodules:**
- `bpy.data` — Access all data-blocks: `bpy.data.objects`, `bpy.data.materials`, `bpy.data.meshes`, etc.
- `bpy.context` — Current state: active object, selected objects, current mode, active view layer
- `bpy.ops` — Call operators (same operations triggered by menu/keyboard)
- `bpy.props` — Register custom properties for add-ons
- `bpy.types` — Extend or register custom types, panels, operators

**The Data API vs the Operator API:**
- `bpy.data` operates directly on data — preferred way to get/set values in scripts
- `bpy.ops` runs operators — have side effects, require context, less predictable in scripts
- Prefer `bpy.data` for reading/setting properties; use `bpy.ops` only when no direct data API equivalent exists

**The Info Log:** Every action you do in Blender's UI generates a Python command that appears in the Info Log. This is the fastest way to learn the Python API for any operation — do it manually, then read the corresponding Python command.
