---
id: blender-3d/concepts/python-bpy-api
title: "Python Scripting — bpy Module, Data API, and Operators"
type: concept
tags:
  - python
  - bpy
  - scripting
  - api
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-04-21"
verified_by: agent
supersedes:
  - concepts/python-scripting.md
related:
  - python-addons.md
  - python-batch-scripting.md
---

# Python Scripting — bpy Module, Data API, and Operators

Blender exposes virtually its entire feature set through the `bpy` Python module. The mental model that unlocks scripting is understanding the difference between the **data API** (`bpy.data` — direct property access, always works) and the **operator API** (`bpy.ops` — replicates UI actions, requires context).

---

## The bpy Module Structure

```python
import bpy

bpy.data      # All data-blocks in the .blend file
bpy.context   # Current selection, active object, mode, scene
bpy.ops       # Operators — UI actions exposed as Python callables
bpy.types     # Blender's type system — for registering custom classes
bpy.props     # Property types for custom properties on panels/operators
bpy.utils     # Utility functions (register_class, unregister_class, etc.)
bpy.app       # Application state (version, handlers, translations)
bpy.path      # File path utilities
```

---

## bpy.data — Direct Data Access

`bpy.data` is a collection of ID data-blocks organized by type:

```python
bpy.data.objects      # All objects
bpy.data.meshes       # All mesh data-blocks
bpy.data.materials    # All materials
bpy.data.images       # All images
bpy.data.armatures    # All armature data-blocks
bpy.data.collections  # All collections
bpy.data.scenes       # All scenes
bpy.data.actions      # All animation actions
bpy.data.node_groups  # All node groups
```

### Accessing and Modifying Data

```python
obj = bpy.data.objects["Cube"]
obj.location = (1.0, 0.0, 0.0)
obj.rotation_euler = (0, 0, 1.5708)   # radians
obj.scale = (2.0, 2.0, 2.0)

# Read a material's base color
mat = bpy.data.materials["Metal"]
nodes = mat.node_tree.nodes
principled = nodes.get("Principled BSDF")
if principled:
    color = principled.inputs["Base Color"].default_value
```

### Creating New Data-Blocks

```python
mesh = bpy.data.meshes.new("MyMesh")
obj = bpy.data.objects.new("MyObject", mesh)
bpy.context.collection.objects.link(obj)

# Use bmesh for constructing geometry
import bmesh
bm = bmesh.new()
bmesh.ops.create_cube(bm, size=2.0)
bm.to_mesh(mesh)
bm.free()
```

### The bmesh Module

`bmesh` is the in-memory mesh editing API — faster and lower-level than operators:

```python
import bmesh

if obj.mode == 'EDIT':
    bm = bmesh.from_edit_mesh(obj.data)
    # do stuff
    bmesh.update_edit_mesh(obj.data)
else:
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    # do stuff
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
```

---

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

## bpy.ops — Operators

```python
# Object operators
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
bpy.ops.object.duplicate_move()
bpy.ops.object.join()
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# Mesh operators (require EDIT mode)
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.delete(type='VERT')
bpy.ops.mesh.subdivide(number_cuts=2)
bpy.ops.mesh.remove_doubles(threshold=0.001)

# Mode switching
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.object.mode_set(mode='OBJECT')

# Rendering
bpy.ops.render.render(write_still=True)
bpy.ops.render.render(animation=True)
```

**Operator return values:**
```python
result = bpy.ops.object.delete()
# Returns: {'FINISHED'}, {'CANCELLED'}, {'RUNNING_MODAL'}, {'PASS_THROUGH'}
```

### When to Use Operators vs Data API

| Use Data API (`bpy.data`) | Use Operators (`bpy.ops`) |
|--------------------------|--------------------------|
| Reading/setting properties | Performing complex operations (Boolean, Remesh) |
| Creating data-blocks | Need undo history entry |
| Bulk property changes | Replicating exact UI behavior |
| Performance-critical loops | Context is available and correct |

The data API is generally faster and more reliable in scripts.

---

## Scripting Gotchas

**Mode Requirements:**
```python
# Fails if no active object:
bpy.ops.object.mode_set(mode='EDIT')  # ERROR: poll() failed
# Always ensure an active object first
if bpy.context.active_object:
    bpy.ops.object.mode_set(mode='EDIT')
```

**Safe access:**
```python
obj = bpy.data.objects.get("MyObject")  # Returns None if not found (vs KeyError)
```

**Data-Block Lifetime:** Creating a data-block without linking it gives it zero users — it will be purged on save. Fix: link it or set `mesh.use_fake_user = True`.

**Update Propagation:**
```python
obj.data.update()              # For mesh data
bpy.context.view_layer.update()  # For transform/visibility changes
```

---

## The Info Log

Every action you do in Blender's UI generates a Python command that appears in the Info Log (`Window → Toggle System Console` on Windows, or read from the Info editor). This is the fastest way to learn the Python API for any operation — do it manually, then read the corresponding Python command.
