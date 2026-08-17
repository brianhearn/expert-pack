---
id: blender-3d/concepts/core-architecture-modes-editors
title: "Core Architecture — Modes and Primary Editors"
type: concept
tags:
  - architecture
  - editors
  - modes
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/core-architecture.md
related:
  - core-architecture-workspaces.md
  - core-architecture-data-blocks.md
  - python-bpy-data.md
content_hash: sha256:11af6effe4834f41d3115d09340d980aa678b27e8da991efbd56113f6c2aa0c7
---

# Core Architecture — Modes and Primary Editors

Blender is modal: Object, Edit, Sculpt, Pose, and paint modes expose different tools on the same object. Editors (3D Viewport, Outliner, Properties, node editors, animation editors) are the panes that make up a workspace.

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

