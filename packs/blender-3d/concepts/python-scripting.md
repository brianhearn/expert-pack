---
title: Python Scripting (bpy)
type: concept
tags:
- concepts
- python-scripting
pack: blender-3d
retrieval_strategy: standard
id: blender-3d/concepts/python-scripting
verified_at: '2026-04-10'
verified_by: agent
---

<!-- context: blender-3d/concepts/python-scripting -->

# Python Scripting (bpy)

> **Lead summary:** Blender exposes virtually its entire feature set through the `bpy` Python module — data-blocks, operators, context, UI registration, and render pipeline hooks. The mental model that unlocks scripting is understanding the difference between the **data API** (`bpy.data` — direct property access, always works) and the **operator API** (`bpy.ops` — replicates UI actions, requires context). Add-ons are just Python modules that register panels, operators, and menus against Blender's type system. Command-line rendering and batch processing via `blender --background` make Blender scriptable as a headless render engine.

---

## The bpy Module Structure

```python
import bpy

bpy.data      # All data-blocks in the .blend file (meshes, objects, materials, etc.)
bpy.context   # Current selection, active object, mode, scene — context-dependent
bpy.ops       # Operators — UI actions exposed as Python callables
bpy.types     # Blender's type system — for registering custom classes
bpy.props     # Property types for custom properties on panels/operators
bpy.utils     # Utility functions (register_class, unregister_class, etc.)
bpy.app       # Application state (version, handlers, translations)
bpy.path      # File path utilities
```

The **critical distinction**: `bpy.data` accesses the internal data model directly, with no context requirements. `bpy.ops` simulates UI button presses and requires the correct context (mode, selection state, active editor type). When something works in the UI but fails in a script, the operator likely needs a context override.

---

## bpy.data — Direct Data Access

`bpy.data` is a collection of ID data-blocks organized by type:

```python
bpy.data.objects      # All objects in the blend file
bpy.data.meshes       # All mesh data-blocks
bpy.data.materials    # All materials
bpy.data.images       # All images
bpy.data.armatures    # All armature data-blocks
bpy.data.collections  # All collections
bpy.data.scenes       # All scenes
bpy.data.actions      # All animation actions
bpy.data.node_groups  # All node groups (geometry nodes, shader groups)
```

### Accessing and Modifying Data

```python
# Get an object by name
obj = bpy.data.objects["Cube"]

# Access mesh data
mesh = bpy.data.meshes["Cube"]
print(f"Vertices: {len(mesh.vertices)}")
print(f"Polygons: {len(mesh.polygons)}")

# Access object properties
obj.location = (1.0, 0.0, 0.0)
obj.rotation_euler = (0, 0, 1.5708)   # radians
obj.scale = (2.0, 2.0, 2.0)

# Read a material's base color
mat = bpy.data.materials["Metal"]
# Navigate the node tree to find Principled BSDF
nodes = mat.node_tree.nodes
principled = nodes.get("Principled BSDF")
if principled:
    color = principled.inputs["Base Color"].default_value
    print(f"Base Color: {list(color)}")
```

### Creating New Data-Blocks

```python
# Create a new mesh and object
mesh = bpy.data.meshes.new("MyMesh")
obj = bpy.data.objects.new("MyObject", mesh)

# Link to current scene collection
bpy.context.collection.objects.link(obj)

# Create a new material
mat = bpy.data.materials.new("MyMaterial")
mat.use_nodes = True

# Use bmesh for constructing geometry
import bmesh
bm = bmesh.new()
bmesh.ops.create_cube(bm, size=2.0)
bm.to_mesh(mesh)
bm.free()
```

### The bmesh Module

`bmesh` is the in-memory mesh editing API — faster and lower-level than using operators:

```python
import bpy
import bmesh

obj = bpy.context.active_object

# Edit mode bmesh (linked to actual mesh, changes are live)
if obj.mode == 'EDIT':
    bm = bmesh.from_edit_mesh(obj.data)
    # ... do stuff ...
    bmesh.update_edit_mesh(obj.data)
else:
    # Object mode bmesh (copy — must write back)
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    # ... do stuff ...
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()

# Select vertices by position
for vert in bm.verts:
    if vert.co.z > 0:
        vert.select = True
```

---

## bpy.context — The Context System

`bpy.context` reflects the *current state* of the UI — what's selected, what mode you're in, what editor is active. It's read from the running Blender session:

```python
bpy.context.active_object          # The active (highlighted orange) object
bpy.context.selected_objects       # All selected objects (list)
bpy.context.scene                  # Current scene
bpy.context.view_layer             # Current view layer
bpy.context.mode                   # 'OBJECT', 'EDIT_MESH', 'POSE', 'SCULPT', etc.
bpy.context.space_data             # Current editor (depends on where script runs)
bpy.context.region                 # Current viewport region
bpy.context.tool_settings          # Tool settings for current mode
bpy.context.object                 # Same as active_object in most contexts
bpy.context.collection             # Active collection
```

### Context-Dependent Properties

Many properties are only available in specific modes:

```python
# Only available in POSE mode:
bpy.context.active_pose_bone       # The active bone in Pose Mode
bpy.context.selected_pose_bones    # All selected pose bones

# Only in EDIT mode:
bpy.context.edit_object            # The object being edited

# Only when timeline is available:
bpy.context.scene.frame_current    # Current frame number
```

### Context Override (Older API)

Before Blender 3.2, context overrides were done with a dict:

```python
# Old method (still works in 3.x, deprecated in 4.x)
ctx = bpy.context.copy()
ctx['area'] = target_area
ctx['region'] = target_region
bpy.ops.view3d.some_operator(ctx)
```

### Context Override (Modern API — Blender 3.2+)

```python
# Modern: use context manager
with bpy.context.temp_override(active_object=my_object):
    bpy.ops.object.shade_smooth()

# Override area type (e.g., run a View3D operator from a script)
for window in bpy.context.window_manager.windows:
    for area in window.screen.areas:
        if area.type == 'VIEW_3D':
            with bpy.context.temp_override(window=window, area=area):
                bpy.ops.view3d.camera_to_view()
            break
```

**Key rule:** If an operator crashes with `context is incorrect`, you need a `temp_override`. The operator's `poll()` method determines what context it requires — readable in the operator's tooltip (`Ctrl+Alt+click`) or Python documentation.

---

## bpy.ops — Operators

Operators are Blender's command system — each UI button ultimately calls an operator. They're accessible via Python:

```python
# Object operators
bpy.ops.object.select_all(action='SELECT')   # Select all objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.delete()                       # Delete selected objects
bpy.ops.object.duplicate_move()
bpy.ops.object.join()                         # Join selected into active
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# Mesh operators (require EDIT mode)
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.delete(type='VERT')
bpy.ops.mesh.extrude_region_move()
bpy.ops.mesh.subdivide(number_cuts=2)
bpy.ops.mesh.remove_doubles(threshold=0.001)  # Merge by distance

# Mode switching
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.mode_set(mode='POSE')
bpy.ops.object.mode_set(mode='SCULPT')

# Rendering
bpy.ops.render.render(write_still=True)
bpy.ops.render.render(animation=True)
```

### Operator Return Values

Operators return a set indicating success or failure:

```python
result = bpy.ops.object.delete()
# Returns: {'FINISHED'}, {'CANCELLED'}, {'RUNNING_MODAL'}, {'PASS_THROUGH'}

if 'FINISHED' in result:
    print("Operator succeeded")
elif 'CANCELLED' in result:
    print("Operator cancelled (nothing to delete, wrong mode, etc.)")
```

### When to Use Operators vs Data API

| Use Data API (`bpy.data`) when | Use Operators (`bpy.ops`) when |
|-------------------------------|-------------------------------|
| Reading/setting properties | Performing complex operations (Boolean, Remesh) |
| Creating data-blocks | Need undo history entry |
| Bulk property changes | Replicating exact UI behavior |
| Performance-critical loops | You need the modal feedback |
| No UI context available | Context is available and correct |

The data API is generally faster and more reliable in scripts. Operators add undo steps and require context. When possible, use the data API.

---

## Custom Operators

Custom operators are Python classes that integrate into Blender's operator system — they get undo support, can be run from the UI, and can receive properties:

```python
import bpy

class OBJECT_OT_rename_selected(bpy.types.Operator):
    """Rename all selected objects with a prefix"""
    bl_idname = "object.rename_selected"    # Internal ID: category.name
    bl_label = "Rename Selected Objects"    # Shown in UI
    bl_options = {'REGISTER', 'UNDO'}       # Undo support

    # Properties shown in the operator redo panel (F9)
    prefix: bpy.props.StringProperty(
        name="Prefix",
        default="Asset_",
        description="Prefix to add to each object name"
    )

    @classmethod
    def poll(cls, context):
        """Return True when operator is available"""
        return context.selected_objects is not None

    def execute(self, context):
        for obj in context.selected_objects:
            obj.name = self.prefix + obj.name
        self.report({'INFO'}, f"Renamed {len(context.selected_objects)} objects")
        return {'FINISHED'}

    def invoke(self, context, event):
        """Called when operator is first triggered — open dialog"""
        return context.window_manager.invoke_props_dialog(self)


def register():
    bpy.utils.register_class(OBJECT_OT_rename_selected)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_rename_selected)

# Run from text editor:
if __name__ == "__main__":
    register()
    bpy.ops.object.rename_selected('INVOKE_DEFAULT')
```

### Naming Conventions

Blender enforces a `CATEGORY_OT_name` pattern for operators, `CATEGORY_PT_name` for panels, `CATEGORY_MT_name` for menus:

| Class Type | Prefix Pattern | Base Class |
|-----------|---------------|------------|
| Operator | `OBJECT_OT_`, `MESH_OT_`, `VIEW3D_OT_` | `bpy.types.Operator` |
| Panel | `VIEW3D_PT_`, `PROPERTIES_PT_` | `bpy.types.Panel` |
| Menu | `TOPBAR_MT_`, `VIEW3D_MT_` | `bpy.types.Menu` |
| Node Tree | `CustomNodeTree` | `bpy.types.NodeTree` |
| Preferences | `AddonPreferences` | `bpy.types.AddonPreferences` |

---

## Custom Panels

Panels add UI to Blender's sidebars, properties editors, and tool shelves:

```python
import bpy

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

        # Basic label
        layout.label(text=f"Active: {obj.name}")

        # Property field
        layout.prop(obj, "name", text="Name")

        # Button (calls an operator)
        layout.operator("object.rename_selected", text="Rename Selected")

        # Row of buttons
        row = layout.row(align=True)
        row.operator("object.select_all", text="Select All").action = 'SELECT'
        row.operator("object.select_all", text="Deselect All").action = 'DESELECT'

        # Box (grouped section)
        box = layout.box()
        box.label(text="Transform", icon='ORIENTATION_GLOBAL')
        box.prop(obj, "location")
        box.prop(obj, "rotation_euler", text="Rotation")

        # Collapsible section
        col = layout.column()
        row = col.row()
        row.prop(context.scene, "my_addon_expanded",
                 icon='TRIA_DOWN' if context.scene.get("my_addon_expanded") else 'TRIA_RIGHT',
                 icon_only=True, emboss=False)
        row.label(text="Advanced Settings")
```

---

## Add-on Structure

A complete add-on is a Python module (single `.py` file or a directory with `__init__.py`) with specific metadata:

```python
# __init__.py (or single .py file for simple add-ons)
bl_info = {
    "name": "My Blender Add-on",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),         # Minimum Blender version
    "location": "View3D > Sidebar > My Tab",
    "description": "Does useful things",
    "doc_url": "https://example.com/docs",
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
    # Register custom properties on existing types
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
├── utils.py         # Shared utilities
└── presets/         # Preset files if needed
```

### Installing Add-ons

- Blender 4.2+: `Edit → Preferences → Get Extensions` (official marketplace)  
- Legacy: `Edit → Preferences → Add-ons → Install from Disk` (zip the directory)
- Development: `Edit → Preferences → Add-ons → Install from Disk` or symlink into `{blender_config}/scripts/addons/`

---

## Application Handlers

Handlers let your code respond to Blender events:

```python
import bpy
from bpy.app.handlers import persistent

@persistent
def my_frame_change_handler(scene, depsgraph):
    """Called every time the frame changes"""
    frame = scene.frame_current
    # Update something based on current frame
    if "MyObject" in bpy.data.objects:
        obj = bpy.data.objects["MyObject"]
        obj.location.z = frame * 0.01

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

The `@persistent` decorator keeps the handler alive when a new .blend file is loaded (otherwise handlers are cleared on file load).

---

## Batch Scripting Patterns

### Batch Rename with Pattern

```python
import bpy
import re

def batch_rename(pattern: str, replacement: str):
    """Rename objects matching a regex pattern"""
    for obj in bpy.data.objects:
        new_name = re.sub(pattern, replacement, obj.name)
        if new_name != obj.name:
            print(f"Renaming: {obj.name} → {new_name}")
            obj.name = new_name

batch_rename(r"_v\d+$", "")  # Strip version suffixes like _v01, _v02
```

### Batch Export

```python
import bpy
import os

def export_all_objects_as_fbx(output_dir: str):
    """Export each object as its own FBX file"""
    os.makedirs(output_dir, exist_ok=True)

    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue

        # Deselect all, select only this object
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        filepath = os.path.join(output_dir, f"{obj.name}.fbx")
        bpy.ops.export_scene.fbx(
            filepath=filepath,
            use_selection=True,
            apply_unit_scale=True,
            apply_scale_options='FBX_SCALE_NONE',
            bake_anim=False,
        )
        print(f"Exported: {filepath}")
```

### Batch Material Assignment

```python
import bpy

def assign_material_by_name(name_keyword: str, material_name: str):
    """Assign a material to all objects whose name contains a keyword"""
    mat = bpy.data.materials.get(material_name)
    if mat is None:
        print(f"Material '{material_name}' not found")
        return

    for obj in bpy.data.objects:
        if obj.type == 'MESH' and name_keyword.lower() in obj.name.lower():
            if len(obj.data.materials) == 0:
                obj.data.materials.append(mat)
            else:
                obj.data.materials[0] = mat
            print(f"Assigned {material_name} to {obj.name}")

assign_material_by_name("wall", "Concrete_Grey")
```

### Iterating Frames and Capturing Data

```python
import bpy

scene = bpy.context.scene
obj = bpy.data.objects["MyObject"]
data = []

for frame in range(scene.frame_start, scene.frame_end + 1):
    scene.frame_set(frame)
    # Force dependency graph evaluation
    depsgraph = bpy.context.evaluated_depsgraph_get()
    obj_eval = obj.evaluated_get(depsgraph)
    data.append({
        'frame': frame,
        'location': list(obj_eval.location),
        'rotation': list(obj_eval.rotation_euler),
    })

import json
with open("/tmp/animation_data.json", "w") as f:
    json.dump(data, f, indent=2)
```

---

## Command-Line Rendering

Blender can be run headlessly from the terminal using `--background` (or `-b`):

### Basic Rendering

```bash
# Render a single frame
blender -b my_scene.blend -o /output/frame_##### -f 42

# Render an animation range (uses scene settings)
blender -b my_scene.blend -o /output/frame_##### -a

# Render a specific range, overriding scene settings
blender -b my_scene.blend -o /output/frame_##### -s 1 -e 250 -a

# Render to a specific format
blender -b my_scene.blend -o /output/frame_#### -F PNG -f 1
```

### Running a Script Headlessly

```bash
# Run a Python script on a .blend file
blender -b my_scene.blend --python my_script.py

# Run a Python expression directly
blender -b my_scene.blend --python-expr "import bpy; bpy.context.scene.render.samples = 512; bpy.ops.render.render(write_still=True)"

# Pass arguments to your script (access via sys.argv after --)
blender -b my_scene.blend --python my_script.py -- --output /renders/ --frame 1
```

```python
# In my_script.py, access custom arguments:
import sys
import bpy

argv = sys.argv
argv = argv[argv.index("--") + 1:]  # Get arguments after "--"
# argv is now ["--output", "/renders/", "--frame", "1"]

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--output", required=True)
parser.add_argument("--frame", type=int, default=1)
args = parser.parse_args(argv)

bpy.context.scene.render.filepath = args.output
bpy.context.scene.frame_set(args.frame)
bpy.ops.render.render(write_still=True)
```

### Render Farm Script Pattern

```bash
#!/bin/bash
# render_farm.sh — render one frame per invocation (parallelizable)
BLEND_FILE=$1
FRAME=$2
OUTPUT_DIR=$3

blender -b "$BLEND_FILE" \
    -o "${OUTPUT_DIR}/frame_####" \
    -F OPEN_EXR_MULTILAYER \
    -f "$FRAME" \
    --python-expr "
import bpy
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 256
scene.cycles.use_denoising = True
"
```

---

## Depsgraph — Evaluated Data

The **dependency graph** (depsgraph) tracks all dependencies between objects, modifiers, constraints, and drivers. When you need the *actual* evaluated geometry (after modifiers), use the depsgraph:

```python
import bpy

depsgraph = bpy.context.evaluated_depsgraph_get()

obj = bpy.data.objects["MyObject"]
obj_eval = obj.evaluated_get(depsgraph)  # The evaluated version

# Access evaluated mesh (with all modifiers applied)
mesh_eval = obj_eval.to_mesh()
print(f"Evaluated vertices: {len(mesh_eval.vertices)}")

# Important: free the evaluated mesh when done
obj_eval.to_mesh_clear()
```

**When to use evaluated data:** When iterating geometry after modifiers (Subdivision Surface, Array, etc.), when getting particle positions, or when you need the final deformed mesh for export.

---

## Scripting Gotchas

### Mode Requirements
Many operators require a specific mode. Switching modes in a script requires an active object:

```python
# This fails if no active object:
bpy.ops.object.mode_set(mode='EDIT')  # ERROR: poll() failed

# Always ensure an active object first:
if bpy.context.active_object:
    bpy.ops.object.mode_set(mode='EDIT')
```

### String vs Reference Access
`bpy.data.objects["Name"]` raises `KeyError` if not found. Use `.get()` for safe access:

```python
obj = bpy.data.objects.get("MyObject")  # Returns None if not found
if obj is None:
    print("Object not found")
```

### Data-Block Lifetime
Creating a data-block without linking it to a scene object gives it zero users — it will be purged on save:

```python
mesh = bpy.data.meshes.new("TempMesh")
# If never linked to an object: will be deleted on save
# Fix: either link it or set fake user
mesh.use_fake_user = True
```

### Update Propagation
After changing properties via the data API, sometimes the viewport doesn't update immediately. Force it:

```python
obj.data.update()              # For mesh data
bpy.context.view_layer.update()  # For transform/visibility changes
```
