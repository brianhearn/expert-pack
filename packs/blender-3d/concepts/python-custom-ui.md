---
id: blender-3d/concepts/python-custom-ui
title: "Python Scripting — Custom Operators and Panels"
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
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/python-scripting.md
related:
  - python-addon-structure.md
  - python-bpy-ops.md
content_hash: sha256:f7b8efc32c1c929dba54020a220cbfe21afd1e32c6ab708ef0d12cf81cd8f498
---

# Python Scripting — Custom Operators and Panels

Custom operators (`bpy.types.Operator`) and panels (`bpy.types.Panel`) are how add-ons add actions and UI. Operators use the `CATEGORY_OT_name` pattern with `poll`/`execute`; panels draw into an editor region and call those operators.

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

