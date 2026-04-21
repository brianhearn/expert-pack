---
id: blender-3d/concepts/video-editing-render
title: "Video Editing — Rendering, Audio, and VSE Limitations"
type: concept
tags:
  - video-editing
  - rendering
  - audio
  - ffmpeg
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-04-21"
verified_by: agent
supersedes:
  - concepts/video-editing.md
related:
  - video-editing-vse.md
---

# Video Editing — Rendering, Audio, and VSE Limitations

---

## Rendering from the VSE

### Output Settings (`Output Properties`)

- **Resolution:** Set X, Y, % scale
- **Frame Rate:** Must match your footage (24, 25, 29.97, 30, 60fps)
- **Output Path:** Where to save rendered frames or video
- **File Format:** Image sequence or video

### Video File Formats (FFmpeg encoding)

`Output → File Format → FFmpeg Video`

**Container format:**

| Container | Use |
|-----------|-----|
| MP4 | Web delivery, sharing. Universal compatibility. |
| MKV | High-quality archival. Container-level error recovery. |
| MOV | Apple ecosystem, Final Cut Pro compatibility. |
| WebM | Web HTML5 video. |

**Video codec (within container):**

| Codec | Use |
|-------|-----|
| H.264 | Standard web/sharing. Good compression, universal playback. |
| H.265 (HEVC) | Better compression than H.264. Some devices still lack native support. |
| AV1 | Next-gen codec, excellent quality. Slow encoding. |
| ProRes | Apple. High quality, large files. For post-production deliverables. |
| DNxHD/DNxHR | Avid. Professional post-production format. |

**Constant Rate Factor (CRF) vs Bitrate:**
- CRF mode: Set quality level (0=lossless, 18=high quality web, 23=default, 28=low quality). Bitrate varies.
- Bitrate mode: Specify exact bitrate. Set 8–20 Mbps for 1080p/H.264 web delivery.

### Rendering Render Image Sequences to Video

The most common VSE task:

```
1. Import rendered PNG sequence as Image Strip
2. Set Resolution to match renders (e.g., 1920×1080)
3. Set Frame Range to match sequence
4. Set File Format → FFmpeg Video → H.264 in MP4
5. Set output path
6. F12 to render (or Ctrl+F12 for animation)
```

The VSE respects the Frame Range set in the timeline. Make sure `Use Preview Range` is off.

---

## Audio

**Audio waveform display:** Enable in Sound strip's properties → Waveform checkbox.

**Audio settings (strip properties):**
- `Volume`: 0–2+ multiplier (1.0 = original)
- `Pitch`: Adjust pitch without affecting speed (Blender 4.x)
- `Pan`: Left/right stereo panning (-1 to +1)
- `Mute`: Silence without deleting

**Scene audio settings (`Render Properties → Audio`):**
- `Sample Rate`: 44100 Hz (standard), 48000 Hz (video standard)
- `Format`: Mono, Stereo, 5.1

**Mixdown:** `Scene Properties → Audio → Mixdown` bakes all audio tracks to a single file for checking sync or exporting audio separately.

### Audio Encoding

In `Encoding → Audio`:
- `AAC` (with MP4/MOV) for web
- `PCM` (uncompressed WAV) for archival quality
- Bitrate: 192kbps (standard web), 320kbps (high quality web)

---

## Stamps and Metadata Overlay

`Output Properties → Metadata` allows rendering with burn-in metadata:
- Filename, date, time, frame number
- Camera, lens, render time
- Note field (custom text)

Useful for review cuts, WIP exports, and dailies.

---

## VSE vs External Editors

| Feature | Blender VSE | DaVinci Resolve | Premiere Pro |
|---------|-------------|-----------------|--------------|
| Multi-cam editing | No | Yes | Yes |
| Professional color grading | Basic | Excellent | Good |
| Audio mixing | Basic | DaVinci Fairlight | Adobe Audition |
| Plugin ecosystem | Minimal | Extensive | Extensive |
| Performance with 4K+ | Moderate | Excellent (GPU) | Good |
| Blender render integration | Native | Via file export | Via file export |

**The practical workflow:**
- **Use Blender VSE for:** Assembling renders for quick-turnaround projects, basic color corrections and text for personal work, when you need to stay inside one app.
- **Use DaVinci Resolve for:** Any professional delivery requiring proper color science, multi-source multi-camera editing, when audio mixing matters.

The VSE is not Blender's strongest feature. For hobbyist and quick professional work it's adequate. For broadcast or film, export sequences and use a dedicated editor.
