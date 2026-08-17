---
id: blender-3d/concepts/python-bpy-context
title: "Python Scripting — bpy.context"
type: concept
tags:
  - python
  - bpy
  - context
  - scripting
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/python-scripting.md
related:
  - python-bpy-data.md
  - python-bpy-ops.md
content_hash: sha256:e9fe26d4eb1994f26e1d30c68a56f9d38930945069d2fba1ae379a104c15680b
---

# Python Scripting — bpy.context

`bpy.context` is Blender's live UI state — the active object, selection, mode, and scene that operators and scripts read at call time. Context is why the same operator succeeds in one editor and fails with `context is incorrect` in another.

## bpy.context — The Context System

`bpy.context` reflects the *current state* of the UI:

```python
bpy.context.active_object          # The active (highlighted orange) object
bpy.context.selected_objects       # All selected objects
bpy.context.scene                  # Current scene
bpy.context.mode                   # 'OBJECT', 'EDIT_MESH', 'POSE', 'SCULPT', etc.
bpy.context.active_pose_bone       # Active bone in Pose Mode (only in POSE mode)
bpy.context.edit_object            # Object being edited (only in EDIT mode)
```

### Context Override (Modern API — Blender 3.2+)

```python
with bpy.context.temp_override(active_object=my_object):
    bpy.ops.object.shade_smooth()

# Override area type for View3D operators
for window in bpy.context.window_manager.windows:
    for area in window.screen.areas:
        if area.type == 'VIEW_3D':
            with bpy.context.temp_override(window=window, area=area):
                bpy.ops.view3d.camera_to_view()
            break
```

**Key rule:** If an operator crashes with `context is incorrect`, you need a `temp_override`.

---

