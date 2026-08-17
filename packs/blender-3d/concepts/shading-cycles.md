---
id: blender-3d/concepts/shading-cycles
title: "Rendering — Cycles GPU and Performance"
type: concept
tags:
  - rendering
  - cycles
  - gpu
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/shading-rendering.md
related:
  - shading-eevee.md
  - shading-render-settings.md
content_hash: sha256:36b0be58c097036475b094e0e2df698b1f60e9d53127526e47ed3f7d8c357793
---

# Rendering — Cycles GPU and Performance

Cycles is Blender's physically based path tracer. GPU backend (OptiX, CUDA, HIP, Metal), sample count, adaptive sampling, denoising, and light-path clamps are the settings that dominate render time and firefly control.

## Cycles: GPU and Performance

### GPU Rendering

Configure in `Edit → Preferences → System → Cycles Render Devices`:

| GPU Backend | For |
|-------------|-----|
| CUDA | Older NVIDIA (GTX 900 series through RTX 20xx) |
| OptiX | NVIDIA RTX series — hardware ray tracing; significantly faster |
| HIP | AMD GPUs (RX 5000+) |
| Metal | Apple Silicon (M1/M2/M3) and AMD Mac GPUs |

Enable GPU render: `Render Properties → Render Device → GPU Compute`.

### Key Cycles Render Settings

**Samples:**
- Viewport: 32–64 samples for previews
- Render: 256–1024 for most scenes; noisy environments need 1000+
- Adaptive Sampling stops sampling each pixel when it converges — dramatically reduces render times

**Denoising:**
- **OpenImageDenoise (OIDN):** CPU-based, very high quality, works on any machine
- **OptiX Denoiser:** NVIDIA-only, very fast GPU denoising, slightly lower quality
- For animation: temporal denoising in DaVinci Resolve or NeatVideo is better than per-frame Blender denoising

**Light Paths:**
- For most scenes: Total 12, Diffuse 4, Glossy 4, Transmission 12
- For interior scenes or complex glass: increase Transmission and Total bounces
- `Render Properties → Light Paths → Clamp → Indirect Light: 10` — eliminates fireflies at the cost of slight energy loss. Set this early.

---

