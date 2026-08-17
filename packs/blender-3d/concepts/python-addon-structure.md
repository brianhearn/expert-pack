---
id: blender-3d/concepts/python-addon-structure
title: "Python Scripting — Add-on Structure and Handlers"
type: concept
tags:
  - python
  - addons
  - handlers
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/python-scripting.md
related:
  - python-custom-ui.md
  - python-bpy-data.md
content_hash: sha256:2768946e4de20f4d95c4ec22bafa5fff4e4ea5ad1035e4768ca407e125b0b84c
---

# Python Scripting — Add-on Structure and Handlers

A Blender add-on is a Python package with `bl_info`, `register()`/`unregister()`, and optional `bpy.app.handlers` hooks. Multi-file add-ons split operators and panels; handlers need `@persistent` to survive file load.

## Add-on Structure

```python
# __init__.py
bl_info = {
    "name": "My Blender Add-on",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),         # Minimum Blender version
    "location": "View3D > Sidebar > My Tab",
    "description": "Does useful things",
    "category": "Object",
}

import bpy
from . import operators, panels    # For multi-file add-ons

classes = [
    operators.OBJECT_OT_my_op,
    panels.VIEW3D_PT_my_panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.my_setting = bpy.props.BoolProperty(
        name="My Setting", default=False
    )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.my_setting
```

**Multi-file add-on directory structure:**
```
my_addon/
├── __init__.py      # bl_info + register/unregister
├── operators.py     # Operator classes
├── panels.py        # Panel classes
└── utils.py         # Shared utilities
```

### Installing Add-ons

- Blender 4.2+: `Edit → Preferences → Get Extensions` (official marketplace)
- Legacy: `Edit → Preferences → Add-ons → Install from Disk` (zip the directory)
- Development: symlink into `{blender_config}/scripts/addons/`

---

## Application Handlers

```python
from bpy.app.handlers import persistent

@persistent
def my_frame_change_handler(scene, depsgraph):
    """Called every time the frame changes"""
    frame = scene.frame_current
    if "MyObject" in bpy.data.objects:
        bpy.data.objects["MyObject"].location.z = frame * 0.01

@persistent
def my_load_handler(filepath):
    """Called after a .blend file is loaded"""
    print(f"Loaded: {filepath}")

def register():
    bpy.app.handlers.frame_change_post.append(my_frame_change_handler)
    bpy.app.handlers.load_post.append(my_load_handler)

def unregister():
    bpy.app.handlers.frame_change_post.remove(my_frame_change_handler)
    bpy.app.handlers.load_post.remove(my_load_handler)
```

**Available handlers:** `frame_change_pre/post`, `render_pre/post/complete/cancel`, `load_pre/post`, `save_pre/post`, `undo_pre/post`, `redo_pre/post`, `depsgraph_update_post`, `object_bake_pre/complete/cancel`.

The `@persistent` decorator keeps the handler alive when a new .blend file is loaded.

