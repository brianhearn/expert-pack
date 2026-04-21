---
id: blender-3d/concepts/python-addons
title: "Python Scripting — Custom Operators, Panels, and Add-ons"
type: concept
tags:
  - python
  - addons
  - operators
  - panels
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-04-21"
verified_by: agent
supersedes:
  - concepts/python-scripting.md
related:
  - python-bpy-api.md
  - python-batch-scripting.md
---

# Python Scripting — Custom Operators, Panels, and Add-ons

---

## Custom Operators

```python
import bpy

class OBJECT_OT_rename_selected(bpy.types.Operator):
    """Rename all selected objects with a prefix"""
    bl_idname = "object.rename_selected"    # Internal ID: category.name
    bl_label = "Rename Selected Objects"    # Shown in UI
    bl_options = {'REGISTER', 'UNDO'}       # Undo support

    prefix: bpy.props.StringProperty(
        name="Prefix",
        default="Asset_",
        description="Prefix to add to each object name"
    )

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):
        for obj in context.selected_objects:
            obj.name = self.prefix + obj.name
        self.report({'INFO'}, f"Renamed {len(context.selected_objects)} objects")
        return {'FINISHED'}

    def invoke(self, context, event):
        """Called when operator is first triggered — open dialog"""
        return context.window_manager.invoke_props_dialog(self)
```

### Naming Conventions

Blender enforces a `CATEGORY_OT_name` pattern for operators, `CATEGORY_PT_name` for panels:

| Class Type | Prefix Pattern | Base Class |
|-----------|---------------|------------|
| Operator | `OBJECT_OT_`, `MESH_OT_`, `VIEW3D_OT_` | `bpy.types.Operator` |
| Panel | `VIEW3D_PT_`, `PROPERTIES_PT_` | `bpy.types.Panel` |
| Menu | `TOPBAR_MT_`, `VIEW3D_MT_` | `bpy.types.Menu` |

---

## Custom Panels

```python
class VIEW3D_PT_my_tools(bpy.types.Panel):
    bl_label = "My Tools"
    bl_idname = "VIEW3D_PT_my_tools"
    bl_space_type = 'VIEW_3D'      # Which editor
    bl_region_type = 'UI'          # Sidebar ('UI'), Tool Shelf ('TOOLS'), Header ('HEADER')
    bl_category = "My Tab"         # Tab name in the N panel sidebar

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        layout.label(text=f"Active: {obj.name}")
        layout.prop(obj, "name", text="Name")
        layout.operator("object.rename_selected", text="Rename Selected")

        row = layout.row(align=True)
        row.operator("object.select_all", text="Select All").action = 'SELECT'
        row.operator("object.select_all", text="Deselect All").action = 'DESELECT'

        box = layout.box()
        box.label(text="Transform", icon='ORIENTATION_GLOBAL')
        box.prop(obj, "location")
```

---

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
