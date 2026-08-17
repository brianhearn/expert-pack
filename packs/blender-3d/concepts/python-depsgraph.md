---
id: blender-3d/concepts/python-depsgraph
title: "Python Scripting — Depsgraph and Evaluated Data"
type: concept
tags:
  - python
  - depsgraph
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
  - python-batch-scripting.md
  - python-bpy-data.md
content_hash: sha256:a7d6b060bffe1687af6e6a248325c6e45208c3f412bf0c21245f0c90ca2aad86
---

# Python Scripting — Depsgraph and Evaluated Data

The dependency graph (depsgraph) is Blender's evaluated view of objects after modifiers, constraints, and drivers. Use `evaluated_depsgraph_get()` and `evaluated_get()` when you need the deformed mesh, not the base data-block.

## Depsgraph — Evaluated Data

The **dependency graph** (depsgraph) tracks all dependencies between objects, modifiers, constraints, and drivers. Use it when you need the *actual* evaluated geometry (after modifiers):

```python
depsgraph = bpy.context.evaluated_depsgraph_get()
obj = bpy.data.objects["MyObject"]
obj_eval = obj.evaluated_get(depsgraph)  # The evaluated version

# Access evaluated mesh (with all modifiers applied)
mesh_eval = obj_eval.to_mesh()
print(f"Evaluated vertices: {len(mesh_eval.vertices)}")

# Important: free the evaluated mesh when done
obj_eval.to_mesh_clear()
```

**When to use evaluated data:** When iterating geometry after modifiers, when getting particle positions, or when you need the final deformed mesh for export.

