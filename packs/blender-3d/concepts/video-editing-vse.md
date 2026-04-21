---
id: blender-3d/concepts/video-editing-vse
title: "Video Editing — VSE Interface, Strips, and Workflow"
type: concept
tags:
  - video-editing
  - vse
  - strips
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-04-21"
verified_by: agent
supersedes:
  - concepts/video-editing.md
related:
  - video-editing-render.md
---

# Video Editing — VSE Interface, Strips, and Workflow

The VSE (Video Sequence Editor) is Blender's built-in non-linear video editor. It excels at assembling Blender renders, basic color grading, and exporting final deliverables — all without leaving Blender. It's not competitive with DaVinci Resolve or Premiere for professional multi-camera or complex color work.

---

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

## Working with Strips

### Adding Strips

`Shift+A` opens the Add menu. Strip starts at the current frame.

**Import rendered image sequences:**
1. `Shift+A → Image/Sequence`
2. Navigate to folder of rendered frames
3. Select all files (`A`), click `Add Image Strip`
4. Set Start Frame and length to match frame count

### Strip Properties (N Panel)

**Strip tab:**
- `Channel`: Which layer it's on
- `Start Frame / Duration`: Position and length
- `Strip Offset Start/End`: Trim points (don't change file, just hide frames)
- `Hold Offset Start/End`: Extend the first/last frame

**Modifiers tab:** Non-destructive modifiers per strip — Color Balance, Curves, Hue Correct, Brightness/Contrast, Mask, White Balance.

### Cutting and Trimming

- `K` or `Ctrl+K`: Cut (razor) all strips at the current frame
- `K` with a specific strip selected: Cut only that strip
- `Shift+K`: Soft cut — cuts but keeps both halves
- Drag strip handles (left/right edges) to trim in/out points
- `S`: Slip edit (Blender 4.x) — slides the source clip within the strip handles without changing strip length

### Ripple Edit

Blender doesn't have a true "ripple delete." Workaround:
1. Select strip and delete (`X`)
2. Select all strips to the right
3. `G` + `X` to slide them left to fill the gap

---

## Proxies for Performance

Working with high-resolution video (4K, 6K, RAW) in the VSE is slow. Proxies are lower-resolution copies used during editing, swapped for full-res at render time.

### Setting Up Proxies

1. Select the Movie strip
2. Strip Properties → Proxy/Timecode tab: enable `Use Proxy`
3. Set proxy resolution: 25%, 50%, 75%, or 100%
4. Click `Set Selected Strip Proxies` → then `Rebuild Proxy and Timecode Indices`
5. Blender creates `BL_proxy` folder next to the source file

**Active proxy level:** In the VSE header, set `Proxy Render Size` to the proxy size you built. At render time, set `Proxy Render Size` to `Full`.

---

## Speed Control — Slow Motion and Time Remapping

### Simple Slow Motion

1. Select the Movie strip
2. `Shift+A → Effect Strip → Speed Control`
3. Set `Speed Factor` = 0.5 for 50% speed

**Source frame rate matters:** If source is 60fps and sequence is 24fps, a speed factor of 0.4 gives you 24fps. If source is 24fps, slowing to 0.5 gives you 12fps effective (choppy). Always film slow-motion clips at high FPS.

### Variable Speed

1. Add Speed Control strip
2. Enable `Use as Speed` or `Use Frame Number`
3. Keyframe the `Speed Factor` property
4. Use Graph Editor to add easing to keyframes for smooth speed ramps

---

## Text and Titles in VSE

`Shift+A → Text` adds a text strip. Properties: Font, size, color, shadow, position (X, Y as percentage of frame), blend mode, opacity.

**Better option for complex titles:** Create titles in Blender's 3D viewport (Text object or Geometry Nodes title card), render as PNG sequences, import into VSE. This gives you full 3D capabilities.
