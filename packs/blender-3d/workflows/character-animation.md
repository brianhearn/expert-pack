---
title: Character Animation Workflow
type: workflow
tags:
- character-animation
- workflows
pack: blender-3d
retrieval_strategy: atomic
id: blender-3d/workflows/character-animation
verified_at: "2026-04-21"
verified_by: agent
schema_version: "4.1"
---

<!-- context: blender-3d/workflows/character-animation -->

# Character Animation Workflow

> **Lead summary:** Character animation in Blender flows through four integrated systems: Armature rigging (bone hierarchy, IK chains, constraints), Shape Keys (facial animation, blend shapes), the Action Editor (clip-based animation authoring), and the NLA Editor (layering and mixing clips for final output). The workflow decision that matters most early is FK vs IK — knowing when each gives you control vs fighting you. A clean rig with well-named bones, correct pole vectors, and working IK/FK switching saves hundreds of hours on complex projects.

---

## Phase 1 — Rigging the Character

### Armature Setup

Start in Object Mode. `Shift+A → Armature` to create the first bone. The workflow:

1. Enter **Edit Mode** on the armature (`Tab`)
2. Build the bone hierarchy by extruding (`E`) from existing bones
3. Set bone rolls (the local Y axis rotation) with `Ctrl+N → Recalculate Roll`
4. Name every bone descriptively: `spine.001`, `spine.002`, `thigh.L`, `shin.L`, `foot.L`, `toe.L`

**Naming convention:** Blender automatically mirrors `.L`/`.R` suffixes in the symmetry tools. Use `.L` and `.R` (not `_Left` or `Left_`) to get Mirror X and Symmetrize to work correctly.

**Bone roll:** The roll determines which direction a bone's local X axis points. Inconsistent rolls cause twisted deformation and IK flipping. `Alt+N` in bone Edit Mode to set roll from the active face or custom direction.

### Rigify vs Manual Rigging

**Rigify** (included add-on) generates a production-ready control rig from a meta-rig:
- Enable: `Edit → Preferences → Add-ons → Rigging: Rigify`
- Add meta-rig: `Shift+A → Armature → Human (Meta-Rig)`
- Position the meta-rig bones to match your character
- Click `Generate Rig` — creates a full FK/IK rig with switching
- Rigify rigs are complex but animator-ready immediately

**Manual rigging** gives full control but requires deeper knowledge. Use manual rigging when:
- The character anatomy doesn't match Rigify's assumptions (non-humanoid, stylized proportions)
- You need custom control shapes that Rigify doesn't support
- Pipeline requires a specific rig structure for game engines or other DCC tools

### Inverse Kinematics Setup

IK chains solve bone rotations automatically — you move the foot, the leg bends to reach it.

```
Bone chain: thigh → shin → foot (IK target)
IK target: empty or bone outside the chain
Pole target: controls which direction the knee bends
```

To add IK to the shin bone:
1. **Pose Mode** → select the shin bone
2. **Properties → Bone Constraints → Add Constraint → Inverse Kinematics**
3. Set **Target**: the armature object, **Bone**: the IK target bone
4. Set **Chain Length**: 2 (shin + thigh)
5. Set **Pole Target** and **Pole Angle** (usually -90° for front-facing knee)

**Pole target placement:** The pole target (an empty or bone) controls where the knee points. Place it forward of the character for legs, backward for elbows. If the knee flips when you move the foot, the pole target position or angle is wrong — adjust the pole angle in 90° increments.

### FK/IK Switching

The cleanest approach uses a custom property on a control bone to blend between FK and IK:

```python
# In a driver expression on the IK constraint's "influence" property:
# Bone: shin.L, Constraint: IK, Channel: Influence
# Driver variable: ik_fk_switch (custom prop on rig root bone)
# Expression: 1 - var   (so 0 = FK, 1 = IK)
```

Rigify handles this automatically with its IK/FK sliders. For manual rigs, add a custom property (`Properties → Object Properties → Custom Properties`) and wire it to the IK constraint influence via a driver.

### Binding the Mesh — Armature Modifier

1. Select the **mesh** first, then `Shift+click` the **armature** (armature is active)
2. `Ctrl+P → With Automatic Weights` — Blender calculates vertex weights based on proximity to bones
3. Automatic weights are a starting point, not a finish line

**After automatic weights:**
- Enter **Weight Paint Mode** on the mesh
- Select a bone in Pose Mode (the weight for that bone shows as color)
- Paint corrections: red (1.0 = full influence), blue (0.0 = no influence)
- Use `Subtract`, `Add`, `Smooth` brush modes

**Common weight painting fixes:**
- **Gradient bleeding:** A knee bone affecting vertices on the hip — paint those vertices to 0 on the knee bone, restore them to the hip/thigh bone
- **Pinching at joints:** Paint the joint area with smooth falloff across 2–3 bones
- **Rigidity:** Hard-surface elements (armor plates, glasses) should be fully weighted (1.0) to a single bone with no gradient

### Advanced Weight Painting Techniques

**The Gradient Tool (massively underused):**
The Gradient tool in Weight Paint mode creates a linear weight falloff between two click points — far more precise than brush painting for joint transitions. Click on the bone center, drag to the joint boundary. For fingers: Gradient from knuckle to fingertip. For shoulders: Gradient from upper arm center to torso edge. Always use with Auto Normalize enabled (Header → Weights → Auto Normalize) to keep all bone weights summing to 1.0 per vertex.

**Shoulder Deformation — Why Weight Painting Alone Can't Fix It:**
No amount of weight painting fixes shoulder twist deformation. The problem is anatomical: a single bone from shoulder to elbow can't represent the complex twist distribution of a real shoulder joint. The fix is **twist bones** — a bone chain between shoulder and upper_arm that distributes rotation:
- Add a bone between the shoulder and upper_arm joints
- Constrain it with `Copy Rotation` from the upper arm bone at Influence 0.5
- This splits the twist across two bones instead of concentrating it at the shoulder
- Rigify includes twist bones by default — this is a manual-rig-only problem

The mesh topology also matters: the armpit must have **horizontal edge loops** (wrapping around the arm like rings). Vertical-only loops collapse when the arm raises past 90°.

**Corrective Shape Keys for Volume Preservation:**
Even with twist bones and good weights, extreme poses (arm raised overhead, deep knee bend) lose volume. The fix:
1. Create a Shape Key for the problem pose
2. Add a Rotation Difference driver (measures angle between two bones)
3. As the joint bends, the corrective shape key automatically activates, restoring volume

### Retopology Edge Loop Placement for Animation

The deformation quality of a character mesh is determined at the retopology stage, not the weight painting stage. Critical loop placements:

1. **Armpit:** Horizontal loops wrapping around the arm — at least 2 rings. Vertical-only loops collapse on arm raise.
2. **Mouth:** 3 concentric circular loops minimum around the mouth opening for speech animation (M/B/P, OOH, EE shapes).
3. **Nasolabial fold:** Loops following the crease from nose to mouth corner — required for smile/sneer expressions.
4. **Eyes:** Loops following the orbicularis oculi (circular muscle around the eye) — at minimum 2 concentric rings for blink and squint.
5. **Wrist/Ankle:** A clean loop at each joint boundary provides a sharp deformation edge between hand/forearm, foot/shin.
6. **Elbow/Knee front:** Extra loop density on the crease side (front of elbow, back of knee) where the skin bunches.

A model with correct loop placement and automatic weights will deform better than a model with bad topology and hours of weight painting.

---

## Phase 2 — Walk Cycle

A walk cycle is an 8–16 frame looping animation of a full stride. The standard approach for a 24fps cycle at normal walking pace:

### Frame Layout (8-frame cycle, 24fps)

| Frame | Pose Name | Description |
|-------|-----------|-------------|
| 1 | Contact | Left heel hits ground, right toe pushes off |
| 3 | Down | Body at lowest point, weight fully on left leg |
| 5 | Passing | Right leg swings through, body at highest point |
| 7 | Contact | Right heel hits ground, left toe pushes off |
| (9 = 1) | Loop | Back to start |

### Walk Cycle Construction

**Step 1 — Block the contacts first:**
```
Frame 1:  L foot forward, R foot back (Contact L)
Frame 5:  R foot forward, L foot back (Contact R)  
Frame 9:  Copy pose from Frame 1 (loop point)
```

**Step 2 — Add the extremes (down/up):**
- Frame 3: Body drops, L knee bends, R leg trails behind
- Frame 7: Body drops, R knee bends, L leg trails behind

**Step 3 — Add passing poses:**
- Frame 5 (already done as contact)
- The "up" phase happens naturally between contact and passing

**Step 4 — Body and hip motion:**
- Hips rotate left-right (left hip forward when left leg is forward): ~5–10° rotation
- Hips translate up-down: ~2–4cm bobbing (down on contact frames, up on passing)
- Hips sway side to side: slight lean over the weight-bearing leg

**Step 5 — Upper body counteraction:**
- Shoulders counter-rotate opposite to hips: left shoulder forward when right leg is forward
- Head stays relatively stable — slight bounce but always leads the body
- Arms swing opposite to legs: left arm forward with right leg

**Step 6 — Feet and ankle:**
- Heel strike on contact (foot angled down slightly before it lands)
- Foot flattens on down pose
- Toe roll on push-off (just before the foot leaves ground)

### Making It Loop

1. Copy keyframe at frame 1 → paste at frame 9 (for 8-frame cycle)
2. In the **Graph Editor**: select all F-curves → `W → Make Cyclic (Extrapolation)` or use `Channel → Extrapolation Mode → Cyclic`
3. Set **Cycles modifier** in the F-Curve modifiers panel for each F-curve

**Cycle modifier:**
```
N panel → Active F-Curve → Modifiers → Add Modifier → Cycles
Mode: Repeat with Offset (for root motion) or Repeat (for in-place)
```

### In-Place vs Root Motion

**In-place cycle:** The character walks in place, the world moves (or the camera moves). Easiest to set up, compatible with game engines.

**Root motion:** The root bone actually moves forward each cycle. Controlled by keying the root bone's Y translation. Each cycle advances by one stride length.

For root motion, use a **Cycles modifier** with `Repeat with Offset` so the root bone offsets correctly on each repeat.

---

## Phase 3 — Lip Sync

Lip sync uses **Shape Keys** (blend shapes) driven by phoneme timing.

### Setting Up Phoneme Shape Keys

In **Edit Mode** on the head mesh, create shape keys for each phoneme group:

1. **Properties → Object Data → Shape Keys → `+`** to add a Basis shape key
2. Add additional shape keys for each mouth shape:
   - `M/B/P` — lips closed, pressed together
   - `OOH` — lips rounded, pushed forward
   - `EE/I` — lips spread wide
   - `AH/AA` — mouth open, jaw dropped
   - `F/V` — lower lip touching upper teeth
   - `TH` — tongue between teeth
   - `L/D/N` — mouth slightly open, tongue up
   - `rest` — neutral mouth shape

3. For each shape key, switch to Edit Mode (with that shape key selected), deform the mesh to the target shape, return to Object Mode

### Animating Shape Keys

Shape keys are animated directly in the timeline:

1. **Properties → Object Data → Shape Keys** — select the shape key
2. Hover over the **Value** slider, press `I` to insert a keyframe
3. Or right-click the value → `Insert Keyframe`

**In the Dope Sheet → Shape Key Editor** mode, you see all shape key values on the timeline. Phoneme timing workflow:
1. Listen to the audio track in the VSE or load it as a sequence strip
2. Scrub through the timeline to find phoneme timings
3. Set shape key values to 0 on the frame before a phoneme, ramp to 1.0 at the peak, ramp back to 0 after

**Typical timing:**
- Anticipation: set shape key to 0 two frames before the sound
- Peak: set to 0.8–1.0 at the frame the phoneme hits
- Release: set back toward 0 over 2–4 frames (blending into the next phoneme)

### Audio Track Setup

1. **VSE (Video Sequence Editor):** Add audio strip → position under dialogue
2. Or: **Properties → Scene → Audio** — attach audio file directly to scene
3. Enable **AV Sync** in the Timeline header (`Playback → AV Sync`) for audio playback in sync

### Auto Lip Sync Options

For production lip sync, dedicated tools integrate better:

- **Papagayo-NG:** External tool that generates phoneme timing from audio; export timing data and apply to shape keys via script
- **Rhubarb Lip Sync:** Command-line tool that analyzes audio and outputs phoneme timings; Python script can apply to Blender shape keys automatically
- **FACEIT add-on:** Paid but comprehensive facial rigging and expression system for Blender with auto lip sync support

---

## Phase 4 — NLA Workflow

The NLA (Non-Linear Animation) Editor layers multiple Actions together. This enables mixing animations that were created independently:

### Pushing Actions to the NLA

1. Animate the character using the Action Editor — create individual clips: `walk`, `wave`, `idle`, `jump`
2. With an Action active, click the **Push Down** button (↓ arrow) in the Action Editor header
3. The Action becomes an NLA strip on a new NLA track
4. The Action Editor now shows `[No Action]` — you're in NLA mode

### NLA Strip Controls

In the NLA Editor, strips can be:
- **Repositioned:** `G` to slide strips on the timeline
- **Scaled:** `S` to stretch/compress timing
- **Blended:** `N` panel → Strip properties → Blend In/Out (frames to crossfade)
- **Muted:** `H` to temporarily disable a strip
- **Repeated:** Set Repeat count to loop a clip multiple times

```
Strip blend types (dropdown in N panel):
- Replace: Strip replaces the base pose (most common)
- Combine: Additive — adds on top of other strips
- Add: Arithmetically add values (useful for oscillation layers)
- Multiply: Multiply values
- Subtract: Subtract from base
```

### Additive Layers for Secondary Animation

The NLA shine: a `breathing` action can be created with just the chest bones expanding, then layered as an additive track on top of the main animation:

1. Create a `breathing` Action with only the chest bones moving
2. Push down to NLA → set track blend mode to `Add` or `Combine`
3. The breathing track adds on top of whatever the character is doing
4. Similarly: `blink` (eyes only), `hair_flow` (hair bones oscillating), `idle_sway` (gentle body rocking)

### NLA for Complex Sequences

For a cutscene where a character walks to a door and opens it:

```
Track 3: [facial_dialogue         ][smile     ]
Track 2: [arm_swing][hand_reaching         ]
Track 1: [walk_cycle][walk_slow][idle                ]
```

- Track 1 handles locomotion
- Track 2 overrides arm motion during the reaching sequence (blend type: Combine, with Blend In/Out)
- Track 3 facial overlay (additive)

### Baking NLA to Final Action

Before export (especially for game engines), bake NLA down to a single Action:

1. Select the armature
2. `Object → Animation → Bake Action`
3. Settings: `Frame Range: Start=1, End=250`, `Only Selected Bones: off`, `Visual Keying: on`, `Clear Constraints: depends on pipeline`
4. This creates a new Action with all NLA contributions baked in — safe for FBX/GLTF export

---

## Quality Checklist

Before calling a character animation done:

- [ ] **Squash and stretch** on organic forms (especially cartoony characters) — bodies squash on landing, stretch on anticipation
- [ ] **Anticipation** before every major action — weight shifts before a jump, inhale before a shout
- [ ] **Follow-through** — hair, clothing, secondary appendages continue moving after the primary action stops
- [ ] **Ease in / ease out** — check F-curves in the Graph Editor; mechanical motion has linear curves, organic motion has bezier easing
- [ ] **Overlap** — different body parts move on different timing; hips lead, chest follows 2 frames later, head follows 4 frames later
- [ ] **IK/FK integrity** — no joint flipping, pole targets working at extremes of motion range
- [ ] **Viewport playback at 24fps** — use `Viewport Shading: Solid` for playback speed; switch to rendered only for final review
- [ ] **NLA loops seamlessly** — check cycle boundaries in the Graph Editor at high magnification
