---
id: blender-3d/concepts/video-editing-vse-interface
title: "Video Editing — VSE Interface and Strip Types"
type: concept
tags:
  - video-editing
  - vse
  - strips
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/video-editing.md
related:
  - video-editing-vse-editing.md
  - video-editing-render.md
content_hash: sha256:5625108154f8a8bba1602ae8802aa153a956516118995a4553d9165bb51d8a77
---

# Video Editing — VSE Interface and Strip Types

The VSE (Video Sequence Editor) is Blender's built-in non-linear video editor. It excels at assembling Blender renders, basic color grading, and exporting final deliverables — all without leaving Blender. It's not competitive with DaVinci Resolve or Premiere for professional multi-camera or complex color work.

## VSE Interface Overview

Open via `Video Editing` workspace or set any editor to `Video Sequence Editor`.

**Main areas:**
- **Sequence strips (timeline):** Where you arrange media
- **Preview:** The rendered preview of the current frame's output

**Navigation:**
- `Scroll`: Pan timeline left/right
- `Ctrl+Scroll`: Zoom in/out on timeline
- `Numpad 0`: Zoom to fit all strips
- `Home`: View all strips

---

## Strip Types

### Media Strips

**Movie Strip (`Shift+A → Movie`):** Video file (MP4, MOV, MKV, AVI).

**Image Strip (`Shift+A → Image`):** A sequence of image files. Import entire folder of rendered frames (PNG, EXR). Set `Start Frame` and `Length` to match the image sequence.

**Sound Strip (`Shift+A → Sound`):** Audio file. Volume, Pitch, Pan controls in strip properties.

**Scene Strip (`Shift+A → Scene`):** Renders a Blender Scene directly into the VSE. Allows late-breaking changes without pre-rendering. Slower than pre-rendered image sequences.

### Effect Strips

**Color Balance:** Non-destructive color grading on a strip. Lift/Gamma/Gain controls.

**Transform:** Scale, rotate, and position a strip without changing the source clip.

**Speed Control:** Changes playback speed. Speed factor < 1.0 = slow motion; > 1.0 = fast forward.

**Glow:** Adds bloom effect to bright areas (lower quality than Compositor Glare node).

**Gaussian Blur:** Blurs a strip.

**Multiply, Add, Subtract, Divide:** Mathematical blend modes between two strips.

**Wipe:** Animated transition — line/iris/double sweeps from one strip to the next.

### Transitions

Blender VSE doesn't have a native "drag a crossfade" system. Instead:

1. Overlap two strips on adjacent channels
2. Select both
3. `Shift+A → Gamma Cross` — creates a color-correct crossfade

**Gamma Cross** is better than `Cross` because it corrects for gamma during the blend, avoiding the "midpoint dip" artifact that uncorrected linear blending produces.

---

