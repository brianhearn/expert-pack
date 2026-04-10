---
title: Video Editing — Video Sequence Editor (VSE)
type: concept
tags:
- concepts
- video-editing
pack: blender-3d
retrieval_strategy: standard
id: blender-3d/concepts/video-editing
verified_at: '2026-04-10'
verified_by: agent
---

<!-- context: blender-3d/concepts/video-editing -->

# Video Editing — Video Sequence Editor (VSE)

> **Lead summary:** The VSE (Video Sequence Editor) is Blender's built-in non-linear video editor. It's functional for assembling, basic color grading, and audio mixing — particularly for post-processing Blender's own renders. It's not competitive with DaVinci Resolve or Premiere for professional multi-camera, complex color work, or large multi-layer projects. The VSE excels at: rendering Blender animation passes to video, basic cuts and assembly, adding effects to renders, and exporting final deliverables — all without leaving Blender.

---

## VSE Interface Overview

Open via `Video Editing` workspace or set any editor to `Video Sequence Editor`.

The VSE has two main areas:
- **Sequence strips (timeline):** The horizontal strip view where you arrange media
- **Preview:** The rendered preview of the current frame's output

**Header controls:**
- `Start / End`: Frame range for the sequence
- `FPS`: Frame rate (inherits from Output Properties)
- Playback controls: Play, Step Frame, Jump to Start/End

**Navigation:**
- `Scroll`: Pan timeline left/right
- `Ctrl+Scroll`: Zoom in/out on timeline
- `Numpad 0`: Zoom to fit all strips
- `Home`: View all strips

---

## Strip Types

Strips are the fundamental units in the VSE — each is a clip, effect, or audio in the timeline.

### Media Strips

**Movie Strip (`Shift+A → Movie`):** Video file (MP4, MOV, MKV, AVI). Supports most codecs that FFmpeg handles. Key properties: Start Frame, Channel, Strip Offset Start/End (trim in/out points).

**Image Strip (`Shift+A → Image`):** A sequence of image files. Import entire folder of rendered frames (PNG, EXR). This is how you bring in Blender animation render sequences. Set `Start Frame` and `Length` to match the image sequence.

**Sound Strip (`Shift+A → Sound`):** Audio file (WAV, MP3, FLAC, AAC). Appears at the bottom of the timeline. Volume, Pitch, and Pan controls in strip properties.

**Scene Strip (`Shift+A → Scene`):** Renders a Blender Scene directly into the VSE. Use this to composite multiple 3D scenes together without pre-rendering. Slower than pre-rendered image sequences but allows late-breaking changes.

### Effect Strips

Effect strips work on the strips below them (channel stacking). Select one or two strips before adding an effect.

**Color Balance:** Non-destructive color grading on a strip. Lift/Gamma/Gain controls. Equivalent to applying a Color Balance compositor node, but in the VSE.

**Transform:** Scale, rotate, and position a strip without changing the source clip.

**Speed Control:** Changes the playback speed of a strip. Critical for:
- Slow motion: Set speed factor < 1.0 (requires high-FPS source footage)
- Time remapping: Variable speed with keyframed `Speed Factor`
- Freeze frame: Speed = 0

**Glow:** Adds bloom effect to bright areas. Fast but lower quality than the Compositor Glare node.

**Blur:** Simple blur effect.

**Multiply, Add, Subtract, Divide:** Mathematical blend modes between two strips (select both, then add effect). Multiply is useful for combining a color strip over footage as a color wash.

**Wipe:** Animated transition — line/iris/double sweeps from one strip to the next. Old-fashioned but functional.

**Gaussian Blur:** Blurs a strip (much better than the basic Blur).

### Transitions

Blender VSE doesn't have a native "drag a crossfade" transition system like Premiere. Instead:

1. Overlap two strips on adjacent channels
2. Select both
3. `Shift+A → Gamma Cross` — creates a color-correct crossfade between them

`Gamma Cross` is better than `Cross` because it corrects for gamma during the blend, avoiding the "midpoint dip" artifact that uncorrected linear blending produces.

**The Cross effect** is the standard fade/dissolve. Gamma Cross should be the default choice.

---

## Working with Strips

### Adding Strips

`Shift+A` opens the Add menu. The strip starts at the current frame. After adding, you can reposition it.

**Import rendered image sequences:**
1. `Shift+A → Image/Sequence`
2. Navigate to the folder of rendered frames
3. Select all files (`A`), click `Add Image Strip`
4. Set Start Frame and length to match frame count

### Strip Properties (N Panel)

With a strip selected, `N` opens the properties panel showing:

**Strip tab:**
- `Name`: Rename the strip
- `Channel`: Which layer it's on
- `Start Frame / Duration`: Position and length
- `Strip Offset Start/End`: Trim points (don't change file, just hide frames)
- `Hold Offset Start/End`: Additional held frames (extend the first/last frame)

**Modifiers tab:** Non-destructive modifiers stacked per strip — Color Balance, Curves, Hue Correct, Brightness/Contrast, Mask, White Balance. These stack on each individual strip, not globally.

**Source tab:** File path and other source-specific settings.

### Cutting and Trimming

- `K` or `Ctrl+K`: Cut (razor) all strips at the current frame
- `K` with a specific strip selected: Cut only that strip
- `Shift+K`: Soft cut — cuts but keeps both halves
- Drag strip handles (left/right edges) to trim in/out points

**Slip:** `S` with strip selected (Blender 4.x) — slides the source clip within the strip handles without changing strip length. Like sliding a window over the source material.

### Ripple Edit

Blender doesn't have a true "ripple delete" that automatically closes gaps. Workaround:
1. Select strip and delete (`X`)
2. Select all strips to the right
3. `G` + `X` to slide them left to fill the gap

Or use the `Snap` feature: enable `Snap to Current Frame` and slide strips to butt against each other.

---

## Proxies for Performance

Working with high-resolution video (4K, 6K, RAW) in the VSE is slow. Proxies are lower-resolution copies used during editing, swapped for full-res at render time.

### Setting Up Proxies

1. Select the Movie strip
2. In Strip Properties → Proxy/Timecode tab: enable `Use Proxy`
3. Set proxy resolution: 25%, 50%, 75%, or 100%
4. Click `Set Selected Strip Proxies` → then `Rebuild Proxy and Timecode Indices`
5. Blender creates `BL_proxy` folder next to the source file with proxy files

**Active proxy level:** In the VSE header, set `Proxy Render Size` to the proxy size you built (25%, 50%, etc.). The timeline now plays back at proxy resolution — fast.

**At render time:** Set `Proxy Render Size` to `Full` — Blender uses original full-resolution files.

**Proxy codec:** Proxies are built with a fast-decode codec (by default, MPEG-4). For smoother playback, consider building DNxHD or ProRes proxies using FFmpeg externally.

---

## Audio

The VSE handles multi-track audio. Sound strips appear on lower channels (typically).

**Audio waveform display:** Enable in the Sound strip's properties → Waveform checkbox. Shows the waveform in the strip for easier sync.

**Audio settings (strip properties):**
- `Volume`: 0–2+ multiplier (1.0 = original)
- `Pitch`: Adjust pitch without affecting speed (Blender 4.x)
- `Pan`: Left/right stereo panning (-1 to +1)
- `Mute`: Silence without deleting

**Scene audio settings (`Render Properties → Audio`):**
- `Bitrate`: Audio quality (128kbps, 192kbps, 320kbps for MP3; 1411kbps for WAV)
- `Sample Rate`: 44100 Hz (standard), 48000 Hz (video standard)
- `Format`: Mono, Stereo, 5.1

**Mixdown for preview:** `Scene Properties → Audio → Mixdown` bakes all audio tracks to a single file. Useful for checking sync or exporting audio separately.

---

## Speed Control — Slow Motion and Time Remapping

### Simple Slow Motion

1. Select the Movie strip
2. `Shift+A → Effect Strip → Speed Control`
3. In the Speed Control strip properties: `Speed Factor` = 0.5 for 50% speed (slow motion)

**Source frame rate matters:** If source is 60fps and sequence is 24fps, a speed factor of 0.4 gives you 24fps in the edit. If source is 24fps, slowing to 0.5 gives you 12fps effective frame rate (choppy). Always film slow-motion clips at high FPS (60, 120, 240).

### Variable Speed (Time Remapping)

1. Add Speed Control strip
2. Enable `Use as Speed` or `Use Frame Number`
3. Keyframe the `Speed Factor` property
4. The strip now plays at different speeds depending on the keyframe values

For smooth speed ramps, use the Graph Editor to add easing to the Speed Factor keyframes.

### Frame Rate Conversion

When source footage is at a different frame rate than your sequence, the VSE can handle it:
- `Render Properties → Frame Rate` sets the output frame rate
- Movie strips that are a different FPS play back at the correct speed automatically (the strip is just longer or shorter)
- Force a specific interpretation: Strip properties → Use Custom Frame Rate → set the source FPS

---

## Rendering from the VSE

### Output Settings (`Output Properties`)

- **Resolution:** Set X, Y, % scale
- **Frame Rate:** Must match your footage (24, 25, 29.97, 30, 60fps)
- **Output Path:** Where to save rendered frames or video
- **File Format:** Image sequence or video

### Video File Formats (FFmpeg encoding)

`Output → File Format → FFmpeg Video`

Then in `Encoding` section:

**Container format:**

| Container | Use |
|-----------|-----|
| MP4 | Web delivery, sharing. Universal compatibility. |
| MKV | High-quality archival. Container-level error recovery. |
| MOV | Apple ecosystem, Final Cut Pro compatibility. |
| AVI | Windows compatibility (less common now). |
| WebM | Web HTML5 video. |

**Video codec (within container):**

| Codec | Use |
|-------|-----|
| H.264 | Standard web/sharing. Good compression, universal playback. |
| H.265 (HEVC) | Better compression than H.264. Some devices still don't support natively. |
| AV1 | Next-gen codec, excellent quality. Slow encoding. |
| ProRes | Apple. High quality, large files. For post-production deliverables. |
| DNxHD/DNxHR | Avid. Professional post-production format. |
| VP9 | Google's web codec. Good quality. |

**Constant Rate Factor (CRF) vs Bitrate:**
- CRF mode: Set quality level (0=lossless, 18=high quality web, 23=default, 28=low quality). Bitrate varies.
- Bitrate mode: Specify exact bitrate (Mbps). Set 8–20 Mbps for 1080p/H.264 web delivery.

### Audio Encoding

In `Encoding → Audio`:
- `AAC` (with MP4/MOV) for web
- `PCM` (uncompressed WAV) for archival quality
- Set bitrate: 192kbps (standard web), 320kbps (high quality web)

### Rendering Render Image Sequences to Video

The most common VSE task: take 500 frames of PNG renders and output a final video.

```
1. Import rendered PNG sequence as Image Strip
2. Set Resolution to match renders (e.g., 1920×1080)
3. Set Frame Range to 1–500 (or whatever range)
4. Set File Format → FFmpeg Video → H.264 in MP4
5. Set output path
6. F12 to render (or Ctrl+F12 for animation)
```

The VSE respects the Frame Range set in the timeline. Make sure `Use Preview Range` is off.

---

## VSE vs External Editors

The VSE's limitations are important to understand:

| Feature | Blender VSE | DaVinci Resolve | Premiere Pro |
|---------|-------------|-----------------|--------------|
| Multi-cam editing | No | Yes | Yes |
| Professional color grading | Basic | Excellent (Fusion + Color) | Good |
| Audio mixing | Basic | DaVinci Fairlight | Adobe Audition |
| Plugin ecosystem | Minimal | Extensive | Extensive |
| Performance with 4K+ | Moderate | Excellent (GPU-accelerated) | Good |
| Blender render integration | Native | Via file export | Via file export |

**The practical workflow:** Use Blender VSE for:
- Assembling renders from Blender for quick-turnaround projects
- Adding basic color corrections and text to personal work
- When you need to stay inside one app

Use DaVinci Resolve for:
- Any professional delivery requiring proper color science
- Multi-source multi-camera editing
- When audio mixing matters

The VSE is not Blender's strongest feature. For hobbyist and quick professional work it's adequate. For broadcast or film, export sequences and use a dedicated editor.

---

## Text and Titles in VSE

`Shift+A → Text` adds a text strip. In the strip properties:
- Font, size, color, shadow
- Position (X, Y) as percentage of frame
- Blend mode and opacity

Text strips are rendered every frame with the specified content. Animate position/opacity by keyframing the strip properties.

**Better option for complex titles:** Create titles in Blender's 3D viewport (Text object or Geometry Nodes title card), render those as PNG sequences, import into VSE. This gives you full 3D capabilities for title cards.

---

## Stamps and Metadata Overlay

`Output Properties → Metadata` allows rendering with burn-in metadata:
- Filename, date, time, frame number
- Camera, lens, render time
- Note field (custom text)

Enable specific stamp types and adjust position/size. Useful for review cuts, WIP exports, and dailies.
