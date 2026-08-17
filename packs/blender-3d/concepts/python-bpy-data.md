---
id: blender-3d/concepts/python-bpy-data
title: "Python Scripting — bpy Module Structure and bpy.data"
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
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/python-scripting.md
related:
  - python-bpy-context.md
  - python-bpy-ops.md
  - python-addon-structure.md
  - python-batch-scripting.md
content_hash: sha256:2492505e931cb266b12cab9b6069aeb5b7c8f3e9276af7ca8b22f10c979b7613
content_hash: sha256:c84b9b760576a261811220a3ea16400d193d0e11048e8b96231a05944e2ba739
---

# Python Scripting — bpy Module Structure and bpy.data

Blender exposes virtually its entire feature set through the `bpy` Python module. The mental model that unlocks scripting is understanding the difference between the **data API** (`bpy.data` — direct property access, always works) and the **operator API** (`bpy.ops` — replicates UI actions, requires context). Almost everything visible in Blender's UI is accessible and scriptable via Python. The `bpy` module is the entry point.

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

**The Data API vs the Operator API:**
- `bpy.data` operates directly on data — preferred way to get/set values in scripts
- `bpy.ops` runs operators — have side effects, require context, less predictable in scripts
- Prefer `bpy.data` for reading/setting properties; use `bpy.ops` only when no direct data API equivalent exists

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

