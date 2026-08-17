---
id: blender-3d/concepts/python-bpy-ops
title: "Python Scripting — bpy.ops, Gotchas, and the Info Log"
type: concept
tags:
  - python
  - bpy
  - operators
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
  - python-bpy-context.md
content_hash: sha256:2a36057f05b69c430a9007804c4ad6dfb71265066c10dc94ac0129b2367d46b0
---

# Python Scripting — bpy.ops, Gotchas, and the Info Log

`bpy.ops` exposes Blender's UI operators as Python callables — the same actions triggered by menus and shortcuts. Operators require a valid context, return a status set, and are slower and less predictable than the data API for bulk property work.

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

