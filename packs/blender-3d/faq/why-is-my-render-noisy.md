<!-- context: section=faq, topic=render-noise, related=shading-rendering,compositing,troubleshooting/common-mistakes -->

# Why Is My Render Noisy?

> **Lead summary:** Cycles noise is caused by insufficient samples, difficult lighting (small lights, complex indirect paths, glass/caustics), or missing denoising. The fastest fix is enabling denoising (OIDN or OptiX) and using Adaptive Sampling — together these let you render at 256–512 samples with results equivalent to thousands of raw samples. For persistent fireflies (bright pixel artifacts), clamp Indirect Light to 10–15.

---

## The Short Answer

Cycles is a path tracer — noise is the natural output of the algorithm. More samples = less noise. But raw sample count is the *slowest* fix. The fast fixes are:

1. **Enable denoising** (if you haven't already)
2. **Enable Adaptive Sampling** (on by default — check it's not disabled)
3. **Clamp Indirect Light** to fix fireflies

---

## Step 1: Enable Denoising

`Render Properties → Sampling → Denoiser`

| Denoiser | Quality | Speed | Requirement |
|----------|---------|-------|-------------|
| OpenImageDenoise (OIDN) | Excellent | Moderate (CPU) | Any machine |
| OptiX | Very good | Fast (GPU) | NVIDIA RTX |
| NLM | Poor | Slow | Any (avoid) |

**For still images:** Use OIDN. In the compositor, connect Denoising Albedo and Denoising Normal passes to the Denoise node for best results:
```
Enable in View Layer → Passes → Data:
  Denoising Albedo ✓
  Denoising Normal ✓

Compositor Denoise node:
  Image ← Render Layers (Image)
  Normal ← Render Layers (Denoising Normal)
  Albedo ← Render Layers (Denoising Albedo)
  Prefilter: Accurate (for stills)
```

**For animation:** Per-frame denoising causes temporal flickering ("swimming" fine details). Options:
- Use OptiX Temporal denoising if you have an NVIDIA GPU
- Post-process with DaVinci Resolve's Temporal Noise Reduction or NeatVideo (better results)
- Render more samples per frame to minimize the denoiser's work

---

## Step 2: Check Adaptive Sampling

`Render Properties → Sampling → Adaptive Sampling` (should be ON by default)

Adaptive Sampling stops sampling each pixel when it converges — areas that resolve quickly (smooth diffuse surfaces) stop early; complex areas (caustics, glass, fine indirect lighting) continue. This makes a 256-sample render equivalent to a much higher raw count.

**Settings:**
- `Noise Threshold: 0.01` — lower = less noise, more samples
- `Min Samples: 32` — always do at least this many before adaptive kicks in

---

## Step 3: Identify the Noisy Parts

Not all noise is the same:

**Uniform grain across the whole image:**
→ Not enough samples. Increase Render Samples or reduce Noise Threshold.

**Fireflies (single bright speckles):**
→ High-variance indirect paths (caustics, small lights, sharp reflections on glass).
→ Fix: `Render Properties → Light Paths → Clamp → Indirect Light: 10` (try 5–15; lower = fewer fireflies but more energy loss).
→ Also check: any Emission materials with very high Strength values — reduce them and compensate with light intensity instead.

**Noisy specific areas (glass, shadows, indirect light):**
→ Those areas require more bounces or larger lights.

**Noise only in volume/smoke/fire:**
→ Volume rendering is expensive. Reduce `Volume Render Step Rate` in Render Properties, or use EEVEE for the volume element.

---

## Step 4: Make Your Lights Larger

**This is counterintuitive but important:** Larger lights converge faster in path tracing. A small area light (5cm) creates high-variance samples in the renderer — most rays miss it, occasionally a ray hits it and creates a bright sample → fireflies and noise.

A larger area light (50cm) is hit more often, variance drops, convergence is faster.

**Rule of thumb:** If a scene is noisy, try doubling the size of your lights and halving the strength to maintain the same total light output. Render should be cleaner with fewer samples.

---

## Step 5: Increase Samples (As a Last Resort)

If denoising and adaptive sampling are on and the render still looks bad:

| Scene Type | Recommended Samples |
|------------|---------------------|
| Simple diffuse scene, daylight HDRI | 128–256 |
| Interior scene, indirect lighting | 512–1024 |
| Night scene, artificial lights | 1024–2048 |
| Heavy glass, caustics | 1024–4096 |
| Complex volumes | 512–2048 |

**The relationship:** noise reduction ≈ `sqrt(samples)`. Going from 256 to 1024 (4× more samples) gives 2× better noise, not 4×. This is why denoising is almost always the better investment.

---

## EEVEE Alternative

If your scene doesn't require Cycles' physical accuracy, switch to EEVEE:
- Viewport renders are near-instant
- Final renders are seconds, not minutes
- No path-tracing noise at all

EEVEE is appropriate for: product visualization (many studios), motion graphics, stylized art, Grease Pencil work.

→ See: [shading-rendering.md](../concepts/shading-rendering.md) for EEVEE vs Cycles decision guide.
