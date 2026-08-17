---
id: blender-3d/concepts/python-batch-scripting
title: "Python Scripting — Batch Scripting Patterns"
type: concept
tags:
  - python
  - batch-scripting
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/python-scripting.md
related:
  - python-cli-render.md
  - python-depsgraph.md
  - python-bpy-data.md
content_hash: sha256:efb75300091b635fe0264897d80e5559f83871a7695bd6870fca013550a7a5cd
---

# Python Scripting — Batch Scripting Patterns

Batch scripting loops `bpy.data` to rename, export, or sample many objects or frames in one run. These patterns are the in-session half of pipeline automation; headless CLI rendering is the other half.

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
            obj.name = new_name

batch_rename(r"_v\d+$", "")  # Strip version suffixes like _v01, _v02
```

### Batch Export

```python
import bpy, os

def export_all_objects_as_fbx(output_dir: str):
    """Export each object as its own FBX file"""
    os.makedirs(output_dir, exist_ok=True)
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        filepath = os.path.join(output_dir, f"{obj.name}.fbx")
        bpy.ops.export_scene.fbx(
            filepath=filepath,
            use_selection=True,
            apply_unit_scale=True,
            bake_anim=False,
        )
```

### Iterating Frames and Capturing Data

```python
import bpy, json

scene = bpy.context.scene
obj = bpy.data.objects["MyObject"]
data = []

for frame in range(scene.frame_start, scene.frame_end + 1):
    scene.frame_set(frame)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    obj_eval = obj.evaluated_get(depsgraph)
    data.append({
        'frame': frame,
        'location': list(obj_eval.location),
        'rotation': list(obj_eval.rotation_euler),
    })

with open("/tmp/animation_data.json", "w") as f:
    json.dump(data, f, indent=2)
```

---

