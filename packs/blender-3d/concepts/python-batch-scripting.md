---
id: blender-3d/concepts/python-batch-scripting
title: "Python Scripting — Batch Scripting and Command-Line Rendering"
type: concept
tags:
  - python
  - batch-scripting
  - command-line
  - headless
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
  - python-addons.md
---

# Python Scripting — Batch Scripting and Command-Line Rendering

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

## Command-Line Rendering

Blender can be run headlessly from the terminal using `--background` (or `-b`):

### Basic Rendering

```bash
# Render a single frame
blender -b my_scene.blend -o /output/frame_##### -f 42

# Render an animation range (uses scene settings)
blender -b my_scene.blend -o /output/frame_##### -a

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
import sys, argparse, bpy

argv = sys.argv
argv = argv[argv.index("--") + 1:]  # Get arguments after "--"

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
