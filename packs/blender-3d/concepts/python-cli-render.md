---
id: blender-3d/concepts/python-cli-render
title: "Python Scripting — Command-Line Rendering"
type: concept
tags:
  - python
  - command-line
  - headless
  - render
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
  - python-depsgraph.md
content_hash: sha256:bb8b5f387bbe1cf7b66c1419fbaf09dc24bcc5e8fe0872e5b4f091b5cdb0ae40
---

# Python Scripting — Command-Line Rendering

Blender can run headlessly with `--background` (`-b`) to render frames or execute Python without a UI. Frame ranges, output paths, `--python`, and `--python-expr` are the farm-script primitives.

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

