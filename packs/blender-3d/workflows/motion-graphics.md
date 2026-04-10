---
title: Motion Graphics Workflow
type: workflow
tags:
- motion-graphics
- workflows
pack: blender-3d
retrieval_strategy: atomic
id: blender-3d/workflows/motion-graphics
verified_at: '2026-04-10'
verified_by: agent
---

<!-- context: blender-3d/workflows/motion-graphics -->

# Motion Graphics Workflow

> **Lead summary:** Motion graphics in Blender combines three systems: **Geometry Nodes** for procedural animation without keyframes, **shader-driven animation** (animated shader properties via drivers or baked textures), and **camera animation** with controlled easing for a professional MoGraph feel. The key insight is that Geometry Nodes operates on geometry at render time — you can animate node parameters and get fully procedural motion with no bone rigs or shape keys. Combine this with EEVEE's real-time feedback and you have a fast iteration loop for motion design work.

---

## Geometry Nodes for Procedural Motion

### The Core Pattern: Animate a Node Input

Any Geometry Nodes input socket can be driven by an animated value. The simplest form:

1. Add a **Value** or **Integer** node inside the Geometry Nodes tree
2. Right-click the output socket → `Add Driver` or hover over the value field and press `I` to keyframe it
3. The parameter changes over time drive the entire procedural result

```
Example: Animated scatter count
[Random Value] → [Point Distribute: Count] 
Connect Count to a [Math: Floor] node driven by a scene time expression.
As frame increases, more instances appear — no keyframes on the instances themselves.
```

### Time-Based Expressions

The `Scene Time` node is the MoGraph workhorse — it exposes the current frame and elapsed time in seconds as node outputs:

```
Node: Scene Time
  Outputs:
    Seconds — time in seconds (0.0 at frame 1, 1.0 at frame 25 for 25fps)
    Frame   — current frame as a float
```

Combine with math nodes for procedural animation:

```
Scene Time (Seconds) → Math (Sine) → Scale (element-wise)
Result: All instances scale up and down in a sinusoidal pattern over time — loopable with no keyframes

Scene Time (Seconds) → Math (Multiply: 0.5) → Math (Sine) → Map Range (–1 to 1 → 0 to 1)
Result: normalized oscillation, 0–1 range
```

### Instance Array with Staggered Timing

A core MoGraph pattern — N objects, each animating on a delay based on their index:

```
Nodes:
[Mesh Line (Count: 20)] → [Instance on Points]
                              ↑
                         Instance: [Cube mesh]

For staggered scale:
[Index] → [Math: Divide by 20] → stagger_factor
[Scene Time: Seconds] → [Math: Subtract stagger_factor] → time_offset
[Math: Clamp 0–1] → [Math: Smoothstep] → scale_value
[Scale Instances: scale_value]
```

This gives a "falling dominoes" effect where each instance scales up after its neighbor, with smooth easing via the Smoothstep function.

### Staggered Animation Formula

The `Smoothstep` node (or Math → Smooth Min) provides S-curve easing without keyframes:

```
Smoothstep equation: x = clamp((t - edge0) / (edge1 - edge0), 0, 1)
                     result = x * x * (3 - 2*x)

In nodes:
Input time (0–1 range) → Map Range (Type: Smooth Step, From: 0→1, To: 0→1)
This gives ease-in/ease-out on any procedural value.

For each instance:
local_time = global_time - (index * delay_per_item)
clamped = clamp(local_time, 0, 1)
scaled_value = smoothstep(clamped)
```

### Geometry Nodes Wave/Ripple Effect

```
Nodes setup for a vertex wave:
[Position] → separate XYZ → X component
X → [Math: Multiply (frequency 2.0)] → [Math: Add (Scene Time × speed)] → [Math: Sine]
Sine output → [Math: Multiply (amplitude)] → Z offset
Combine XYZ (X, Y, Z+offset) → [Set Position]

Control parameters:
- frequency: how many wave crests per unit
- speed: how fast the wave moves (multiply with Scene Time)
- amplitude: wave height
```

This creates an animated vertex displacement wave across any geometry without any keyframes — purely procedural and infinitely adjustable.

### Procedural Text Animation (Blender 4.x)

Geometry Nodes can operate on text strings in Blender 4.x:

```
[String to Curves] → [Fill Curve] → [Realize Instances]
                ↑
         animated string input

For typewriter effect:
[String Info: Length] → [Math: Multiply (Frame/10)] → [Math: Floor]
→ [Slice String: from 0 to animated_count]
→ [String to Curves]
```

---

## Shader-Driven Animation

### Animating Shader Properties Directly

Any shader node value can be keyframed:

1. In the **Shader Editor**, hover over a value field
2. Press `I` to insert a keyframe (value turns orange when keyed)
3. The material changes over time are visible in viewport with Rendered or LookDev mode

**Example: Animated emission for a light-up effect:**
```
Emission shader → Strength: keyframe 0 at frame 1, keyframe 20 at frame 30
Add easing in Graph Editor (F-Curve → T → Smooth)
```

### Using Drivers in Shaders

Connect a custom object property to a shader value:

1. Add a custom property to the object: `Properties → Object → Custom Properties → New`
2. In Shader Editor, right-click a value → `Add Driver`
3. Set driver to use the object's custom property
4. Animating the custom property drives the shader

**Example: Reveal effect via gradient:**
```
Custom property: reveal_progress (0.0 to 1.0)

Shader nodes:
[Texture Coordinate: Generated] → [Separate XYZ: Z] 
→ [Math: Greater Than (threshold=reveal_progress)]
→ [Mix Shader: factor] (fully transparent vs actual material)

Animate reveal_progress from 0 to 1:
Object reveals from bottom to top without modifiers
```

### Animated Noise for Organic Motion

Noise Texture with time input creates organic-looking procedural motion:

```
Shader node setup for animated noise displacement:
[Texture Coordinate: Object] → [Mapping] → [Noise Texture]
                                               ↑
                                    W input: Scene Time (Seconds) × speed_factor

Noise Texture → [Displacement] → Material Output (Displacement slot)

Scale: 3.0 (frequency)
Detail: 6.0
Roughness: 0.5
W (time): drives the noise evolution over time
```

This makes surfaces "breathe" or look like they have living texture, using only the material — no rig, no shape keys.

---

## Camera Animation

### Camera Setup for MoGraph

For motion graphics work, set up the camera before animating:

```
Camera Settings for a clean MoGraph look:
Focal Length: 50mm (neutral, minimal distortion)
Sensor Size: 36mm (Full Frame equivalent)
Clip Start: 0.01m
Clip End: 1000m

Resolution: 1920×1080 (16:9) — or 1080×1080 for Instagram square
Frame Rate: 24fps (film feel) or 30fps (broadcast/digital)
```

### Smooth Camera Moves

**The wrong way:** Keyframe camera position at A and B, play it back → linear movement, mechanical feel.

**The right way:**

1. Keyframe at start and end
2. Open **Graph Editor** → select camera location F-curves
3. `T → Smooth` (Bezier interpolation with auto handles)
4. Adjust bezier handles to control acceleration into and out of the move

**Or use a Camera Rig:**
- Add an **Empty** at the target point, add **Track To** constraint on the camera targeting the Empty
- Animate the Empty's position (camera always looks at it, even as it moves)
- Animate the camera separately on a separate path
- This decouples look-at behavior from camera movement — much easier to control

**Follow Path camera:**
```
1. Draw a Bezier curve for the camera path
2. Camera → Add Constraint → Follow Path → select the curve
3. Animate the Offset value (0% to 100% = full path traversal)
4. Add Track To constraint → target an Empty placed at the scene center
5. Adjust path handles to control velocity (bunched handles = slow, spread = fast)
```

### Easing and Timing

**Graph Editor easing types (`T` key):**
- `Ease In` — starts slow, ends fast (good for camera push-in revealing something)
- `Ease Out` — starts fast, ends slow (good for settling into a final position)
- `Ease In Out` — slow-fast-slow (most natural for camera moves)
- `Linear` — constant velocity (mechanical, use for conveyor/machine aesthetics)
- `Bounce` — bounces at end (cartoon feel)
- `Back` — overshoots then settles (springy MoGraph feel)

**Overshoot for snappy MoGraph feel:**
In the Graph Editor, pull the bezier handle past the final value:
```
Final position: Z = 5.0
Overshoot handle: Z = 5.8 at frame 18, then settle to Z = 5.0 at frame 25
This creates a springy, confident landing
```

### Camera Shake

Procedural camera shake without keyframes using a Noise modifier on F-curves:

1. Select the camera
2. Insert keyframes on Location and Rotation at start and end
3. In Graph Editor, select all F-curves → `Channel → Add Modifier → Noise`
4. Settings:
   ```
   Scale: 15 (frequency — lower = slower shake)
   Strength: 0.05 (subtlety — 0.01 for barely perceptible, 0.2 for action cam)
   Depth: 2 (octaves of noise)
   Offset: different value per axis to prevent sync between X/Y/Z
   ```
5. Mute the modifier on any axis you don't want to shake (e.g., keep Z locked)

---

## Lighting for Motion Graphics

### Flat, Stylized Lighting

Motion graphics often prefers flat, controlled lighting rather than photorealistic studio setups:

```
World: solid color background (#1a1a1a for dark, #f0f0f0 for light)
World strength: 0.0 (no ambient from world)

Key light: Area, 100W, white
Rim light: Area, 150W, accent color (#4488ff, #ff6644, etc.)
No fill light (embrace shadow for graphic punch)
```

### Rim-Heavy Lighting for Dark Backgrounds

Popular MoGraph look: dark background, strong rim lights defining object edges:

```
3 area lights at 120° intervals around the subject
All positioned behind/beside, angled to hit only the silhouette edges
Colors: main accent, complementary, neutral white
Strength: high enough to blow out the edge to pure white
```

### EEVEE Bloom for Neon/Glow Effects

```
Render Properties → EEVEE → Bloom:
  Threshold: 0.8 (only the brightest areas glow)
  Knee: 0.5
  Radius: 6
  Color: (1, 1, 1) or tint the bloom
  Intensity: 0.05–0.2

Material setup for glowing objects:
  Emission shader → Color: accent color, Strength: 3–10
  Mix with Principled BSDF (Mix Shader, factor: 0.5–1.0)
```

---

## Loop-Ready Animations

For seamless loops (social media, broadcast holds):

### The Loop Setup

```
Frame range: 1–120 (5 seconds at 24fps, or 4 seconds at 30fps)

F-Curve requirement for loop:
- Start value = End value (keyframe at frame 1 and frame 121 must match)
- OR: use Cycles F-Curve modifier (adds no keyframes, just cycles automatically)

In Graph Editor:
Select all F-curves → Channel → Add Modifier → Cycles
Mode: Repeat (values loop continuously)
```

### Geometry Nodes Loop

For Geometry Nodes animations, use Scene Time (Seconds) with a modulo operation:

```
[Scene Time: Seconds] → [Math: Modulo (loop_duration)] → normalized_time
→ [Math: Divide by loop_duration] → 0 to 1 range over one loop

This gives a value that goes 0→1, then resets to 0 — infinite loop,
no keyframes needed, renders at any frame range seamlessly.
```

### Checking Loop Integrity

1. Render frame 1 and the frame *after* the last frame
2. Overlay them in an image editor — they should be identical
3. In the VSE: `V` to scrub at the loop point, watching for any pop or jump

---

## MoGraph Efficiency Tips

**Use Group Nodes:** Encapsulate repeated Geometry Nodes logic into Group nodes (`Ctrl+G` to group selected nodes). This makes the node graph readable and allows reuse across multiple objects.

**Object Info node for per-instance variation:** When using Instance on Points, the `Object Info` node inside a node group outputs the index and random value per instance — use these to vary size, rotation, color, or timing per instance.

**Bake Geometry Nodes when done:** `Object → Geometry Nodes → Bake` — caches the simulation to disk, enabling scrubbing without recomputation. Essential for complex simulations before final render.

**Separate layers for compositing:** Use `Object Properties → Visibility → Render Visibility` by View Layer to separate background, foreground, and motion elements into separate render passes for compositing flexibility.

**Restrict renders to EEVEE during iteration:** EEVEE renders at 10–100× the speed of Cycles. Build and iterate the animation in EEVEE, then switch to Cycles only for final frames. Many MoGraph pieces use EEVEE for final output anyway.
