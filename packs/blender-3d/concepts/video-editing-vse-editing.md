---
id: blender-3d/concepts/video-editing-vse-editing
title: "Video Editing — Working with Strips, Proxies, Speed, and Text"
type: concept
tags:
  - video-editing
  - vse
  - proxies
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/video-editing.md
related:
  - video-editing-vse-interface.md
  - video-editing-render.md
content_hash: sha256:04da6551b9d69c65fb7606841846100b40b9cfbbe841554f87c451b673c71faf
---

# Video Editing — Working with Strips, Proxies, Speed, and Text

VSE editing is strip-based: you add, trim, slip, and stack media, then add proxies, speed control, and text as needed. Blender has no true ripple delete; proxies keep 4K editable; complex titles are often better as rendered PNG sequences.

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

