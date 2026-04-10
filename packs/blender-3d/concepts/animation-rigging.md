---
title: Animation and Rigging
type: concept
tags:
- animation-rigging
- concepts
pack: blender-3d
retrieval_strategy: standard
id: blender-3d/concepts/animation-rigging
verified_at: '2026-04-10'
verified_by: agent
---

<!-- context: blender-3d/concepts/animation-rigging -->

# Animation and Rigging

> **Lead summary:** Blender's animation system is built around the Action/NLA stack, the Graph Editor for F-curve control, Drivers for property-linking, and the Armature rigging system for skeletal deformation. Understanding the Action/NLA distinction, how bones deform meshes through vertex groups, and where Drivers fit versus Keyframes is the structural knowledge that separates animators who fight the software from those who leverage it.

---

## The Animation Data Model

Before touching keyframes, understand how Blender stores animation data.

**The chain:** Object/Bone property → F-Curve → Action → NLA strip → Final transform

- An **F-Curve** is a single animated property — one curve for X location, one for Y, one for Z, one for bone rotation W quaternion, etc.
- A set of F-Curves grouped together is an **Action** — think of it as a "clip" named and saved
- An object or armature has one **Active Action** at a time (shown in the Action Editor dropdown)
- Actions pushed down to the **NLA Editor** become strips that can be blended, sequenced, and layered

**Critical implication:** If you're recording keyframes in the Graph Editor, you're editing the *active Action*. If you switch the active Action by clicking a different one in the dropdown, your keyframes are in that Action. This surprises people who accidentally create dozens of Actions named "Action.001", "Action.002" by accident.

**Action users:** Actions have user counts like all data-blocks. An Action with no users (not in NLA, not as active Action) will be purged on save. Set Fake User (`F` in the Action dropdown) on Actions you want to keep.

---

## Keyframing Workflow

### Inserting Keyframes

`I` in the 3D Viewport opens the Insert Keyframe menu. Standard choices:

| Option | What It Keys |
|--------|-------------|
| Location | X, Y, Z position |
| Rotation | Rotation (whichever mode the object uses) |
| Scale | X, Y, Z scale |
| Location, Rotation & Scale | All nine channels |
| Visual Location | Actual viewport position (important for constrained objects) |
| Available | Only properties that already have keyframes |

**Visual Keying vs. Regular Keying:** When an object is constrained (e.g., Copy Location or IK), its transform channels reflect the *pre-constraint* values. `Visual Keying` bakes the *visual* position — what you actually see. Use Visual Keying when baking constraint animations, finalizing IK poses to FK, or copying poses.

**Auto-Keying:** Enable with the red dot button in the Timeline header. When active, any change to an object/bone property while the timeline is playing or paused automatically creates a keyframe. Enormously speeds up blocking and hand-crafted animation. Pairs well with the `Replace` mode (only keys properties that already have keyframes) vs `Add & Replace` (keys everything you touch).

### Keyframe Types

Right-click a keyframe in the Dope Sheet or Graph Editor to change type:

| Type | Behavior |
|------|----------|
| Keyframe (Bezier) | Smooth in/out interpolation. Default. |
| Linear | Constant velocity between keys. Good for mechanical motion. |
| Constant | Holds value until the next keyframe, then snaps. Good for on/off switches. |
| Jitter | Noise added on top (not commonly used manually). |

Blender 4.x: You can also set the interpolation mode globally in `Preferences → Animation → Default Interpolation`.

### Dope Sheet

The Dope Sheet shows all keyframes across all channels as dots on a timeline. Think of it as an overview — you can select, move, scale, and delete keyframes but not edit their curves.

**Essential Dope Sheet operations:**
- `G` then `X`: slide keyframes left/right on the timeline
- `S` then `X`: scale selected keyframes in time (stretch or compress timing)
- `Box select`: select all keys in a range
- Filter by object, bone, or property using the search field

**Dope Sheet modes** (dropdown in header):
- `Dope Sheet` — all keyframes in the scene
- `Action Editor` — keyframes in the active Action only
- `Shape Key Editor` — shape key values only
- `Grease Pencil` — Grease Pencil frame timing

---

## Graph Editor — F-Curve Editing

The Graph Editor is where animation lives at the finest level of control. Each property gets its own F-Curve (function curve) — a bezier spline showing value over time.

### Understanding F-Curves

Y axis = property value. X axis = frame number. A flat horizontal line = constant value. A diagonal line = linear change. A bezier S-curve = smooth ease-in/ease-out.

**Handles:** Each keyframe has two bezier handles that control the curve's slope at that point. Handle types:
- `Free` — both handles movable independently
- `Aligned` — both handles stay collinear (default for bezier keys)
- `Vector` — handles point toward adjacent keyframes (linear interpolation approach)
- `Auto` — Blender automatically computes smooth handles
- `Auto Clamped` — Auto, but prevents overshoot beyond keyframe values

Toggle handle types with `V` when handles are selected.

### Extrapolation

What happens outside the keyframe range?

- `Constant` — value holds at the first/last keyframe value (default)
- `Linear` — value continues on the slope of the first/last segment
- `Make Cyclic` — repeats the animation curve (for walk cycles, etc.)

Set via `Channel → Extrapolation Mode` or `Shift+E` on selected curves.

**The Cycle modifier:** Better than extrapolation for most cyclic animation. Add it via `Modifiers → Cycles`. It lets you set how many times to repeat and how to blend at loop points. Essential for walk cycles.

### F-Curve Modifiers

Found in the Sidebar (`N`) when in Graph Editor, under the Modifiers tab for selected curves:

- `Noise` — adds procedural noise (camera shake, organic variation)
- `Cycles` — loops the curve (see above)
- `Generator` — replaces curve with a polynomial function
- `Limits` — clamps output to a min/max range
- `Stepped` — quantizes values to steps (robot motion, pixel art style)

**Camera shake setup:** Select all camera location/rotation curves, add Noise modifier, adjust Scale (timing frequency) and Strength. Result: non-repeating organic camera motion. Combine multiple noise modifiers with different scales for more complex shake.

---

## Drivers — Property-Driven Animation

Drivers link one property to another — or to a Python expression — rather than to time. The property's value is computed every frame based on the driver's target, not stored as keyframes.

### When to Use Drivers (vs Keyframes)

| Use Drivers | Use Keyframes |
|-------------|---------------|
| Shape key controlled by bone rotation | Facial expression keyed by animator |
| Wheel rotation tied to truck movement | Character walk cycle |
| Procedural material intensity linked to object proximity | Light brightness animating over time |
| Custom rig control widgets | General body movement |
| Any "reactive" relationship between properties | Any time-based animation |

### Creating a Driver

1. Right-click any property → `Add Driver`
2. Or: `Ctrl+D` on a property
3. Or: In Graph Editor, switch to Drivers mode (dropdown in header)

**Driver types:**

- `Averaged Value` — average of all variables (most common for single-variable drivers)
- `Sum of Values` — sum all variables
- `Scripted Expression` — arbitrary Python expression (most powerful)
- `Min/Max of Values` — take the min or max from multiple variables

**Variable types:**

- `Single Property` — read any property from any object/bone
- `Rotation Difference` — angle between two bones (excellent for corrective shapes)
- `Distance` — distance between two objects or bones
- `Transform Channel` — a specific transform (loc/rot/scale) from a specific object/bone in a specific space

### Driver Expression Examples

```python
# Remap 0-90 degree bone rotation to 0-1 shape key value
var / 90

# Clamp to 0-1 range
max(0, min(1, var))

# Smooth step (ease in/out) for cleaner transitions
3*var**2 - 2*var**3

# Two variables (var1, var2): bone rotation controls two shape keys
var1 * 0.5 + var2 * 0.3

# Absolute value (useful for bilateral symmetry drivers)
abs(var)

# Check distance and activate above threshold
max(0, var - 0.5) * 2  # activates when var > 0.5
```

**Corrective shape keys via Rotation Difference:** The most common professional driver setup. A knee or elbow bends, the mesh collapses. Create a corrective shape key that fixes the collapse; add a driver with Rotation Difference between the upper and lower limb bones. The shape key activates as the joint bends.

---

## NLA Editor — Non-Linear Animation

The NLA (Non-Linear Animation) Editor treats Actions as clips that can be stacked, blended, and sequenced. It's Blender's equivalent of a video timeline, but for animation actions.

### Workflow

1. Create and finalize an Action in the Graph Editor
2. In the NLA Editor, click the **Push Down** button (down arrow icon) next to the action name in the Action Editor header — this "pushes" the active Action down to an NLA strip, freeing the action slot for a new one
3. The Action now exists as a strip in the NLA track
4. Create a new Action, push it down — repeat
5. NLA strips can be overlapped, scaled, and blended

### NLA Strips

**Strip operations:**
- `Tab` on a strip to enter it and edit the underlying Action
- `G`: slide in time
- `S`: scale (stretch/compress timing)
- `N` panel: strip properties — start/end frame, blend type, influence
- Blend types: Replace (default, override), Add, Subtract, Multiply, Combine

**Blending:** Two overlapping strips can blend using their influence. An idle animation (100% influence) can blend with a "breathing" action (30% influence) — the result is natural layering.

**Tweak Mode:** `Tab` on a selected NLA strip enters Tweak Mode, opening the strip's underlying Action for editing in the Dope Sheet. Exit with `Tab` again.

### NLA for Game Engines

The NLA Editor is the standard workflow for preparing animations for Unity/Unreal export via FBX:
1. All animations are separate named Actions
2. Each Action is pushed down to the NLA as strips
3. Export with `NLA Strips as Clips` or bake all strips to individual actions
4. Game engine imports each Action as a separate animation clip

---

## Armatures — Skeletal Rigging

### Armature Basics

An **Armature** is a Blender object containing bones. Bones form a hierarchy (parent-child). The Armature deforms mesh objects via the **Armature Modifier**.

**Bone anatomy:**
- **Head** — start of the bone (parent connection point)
- **Tail** — end of the bone (where child bones connect from)
- **Roll** — rotation around the bone's Y axis (the bone's "forward" direction)
- **Connected** — when a child bone's head is merged with parent's tail (moving parent moves child's head)
- **Envelope** — a volume around the bone used for automatic weight calculation

**Bone vs. Bone Object Data:** The Armature is the Object; the bones live in the Armature data-block. Edit Mode on an armature lets you edit bone positions/rolls. Pose Mode lets you pose without changing the rest pose.

### Building an Armature

Start in Edit Mode on the Armature object:

- `E` from a bone's tail: extrude a new connected child bone
- `Shift+A`: add a disconnected bone at cursor location
- Select a bone's tip, select another bone's head, `F`: connect them
- `Ctrl+P`: set parent (makes a hierarchy without connecting)
- `Alt+P`: clear parent

**Naming convention:** Use a prefix system — `L_` and `R_` for left/right, `ORG_` for original deform bones, `MCH_` for mechanism bones (no deform), `DEF_` for deform bones. The Rigify system (Blender's built-in auto-rigger) uses a similar scheme.

**Bone layers (4.x: Bone Collections):** Blender 4.0+ replaced the old 32-layer system with named Bone Collections. Organize control bones, deform bones, and helper bones into separate named collections. Toggle visibility per collection.

### Constraints — IK, FK, and More

Bone constraints are evaluated every frame and override (or add to) a bone's transform. They live in the Bone Constraint Properties tab (with bone selected in Pose Mode).

**Key constraints:**

| Constraint | Use |
|------------|-----|
| Copy Location / Rotation / Scale | Makes a bone follow another object/bone's transform |
| Track To | Bone Y+ axis always points at a target |
| Locked Track | Like Track To, but constrains to a single axis |
| Stretch To | Stretches bone toward a target (elastic limbs) |
| IK (Inverse Kinematics) | Solve chain to reach a target (see below) |
| Limit Rotation | Clamp rotation to a range (prevents knee bending backward) |
| Damped Track | Like Track To but smoother for follow-through |
| Child Of | Makes a bone a "child" of another object (weapon pick-up) |
| Action | Drives a specific Action based on a bone's rotation |

### IK vs FK — When to Use Each

**FK (Forward Kinematics):** The default. Rotate the upper arm, the forearm follows. Natural for arcs — swings, reaching up. The animator controls each segment individually. IK must be *removed* to reveal FK (or use IK/FK blend).

**IK (Inverse Kinematics):** Plant the hand in space, the chain (shoulder→elbow→wrist) solves automatically. Natural for:
- Feet on ground (feet stay planted as character moves)
- Hands grabbing a fixed object
- Any time the endpoint needs to be in a specific world position

**IK setup:**
1. Create a control bone at the hand position (no deform, no parent)
2. Add IK constraint to the wrist bone → target = the control bone
3. Set chain length (how many bones the IK solver affects)
4. Create a Pole Target bone to control elbow direction

**IK/FK switching:** Professional rigs have both, with a blend property on the rig. A custom property (0=IK, 1=FK) drives the influence of the IK constraint. This lets animators switch between styles per shot.

**IK Pole Angle:** The pole target tells the IK solver which way the elbow/knee should point. Getting the pole angle right (the offset between the bone's pointing direction and the target) is one of the fussier parts of rigging. Trial and error with the `Pole Angle` value in the IK constraint is normal.

---

## Weight Painting

Weight Paint Mode paints vertex weights — the influence of each bone on each vertex (0.0 to 1.0). Red = full influence, Blue = none.

### Automatic Weights (Starting Point)

With the mesh selected, also select the armature (`Shift+click`), then `Ctrl+P → With Automatic Weights`. Blender calculates weights based on proximity — close vertices get high weights from the nearest bone. This is almost never perfect but gives you a starting point.

**Automatic Weights failure cases:**
- Mesh not enclosed (open boundaries) — solver fails on some bones
- Mesh has non-manifold geometry — gives incorrect results
- Very complex hierarchies or unusual poses — fails unpredictably

If automatic weights fails completely, use `Ctrl+P → Armature Deform` (no automatic weights), then paint all weights manually from scratch.

### Weight Painting Workflow

1. Select the mesh object
2. In Pose Mode, select the bone you want to paint weights for (this sets which vertex group is active)
3. Switch to Weight Paint Mode (or with the mesh selected, `Ctrl+Tab → Weight Paint`)
4. Paint red where you want full influence, blend toward blue at joint areas

**Key brushes:**
- `Draw` (default): paint weight value
- `Blur`: smooth weight transitions between vertices — essential for clean deformation
- `Average`: average weights in the area toward a center value
- `Subtract`: remove weights

**Weight Paint settings:**
- `Strength`: brush opacity
- `Radius`: brush size (`F` to resize interactively)
- `Weight`: value being painted (0–1)
- `Auto Normalize`: keeps total vertex weights summed to 1.0 across all bones — essential for correct deformation. Always enable this.

**Viewing weights:** In Weight Paint Mode, the mesh shows the current vertex group's weights. Switch vertex groups in the Properties → Object Data → Vertex Groups panel.

**Multi-bone influence at joints:** A joint (elbow, knee, shoulder) should have a transition area where both bones have partial influence. The key insight: smooth, natural-looking deformation requires weights that feather across 4–8 vertex loops on each side of the joint.

### Vertex Groups

Vertex Groups are what Weight Paint actually edits. Every bone in an armature that has a deform flag creates an empty vertex group on the mesh with the same name. The Armature Modifier reads these vertex groups to deform the mesh.

You can add/remove vertices from vertex groups in Edit Mode (Select → Assign/Remove in Vertex Groups panel). This is useful for hard assignments (this entire face always follows this bone at weight 1.0).

---

## Shape Keys

Shape Keys store alternative vertex positions as offsets from the Basis (rest) position.

### Setup

In Object Data Properties → Shape Keys:
1. Add the first shape key: `+` button → Name it `Basis` (this is mandatory — the Basis is the neutral/rest position)
2. Add more shape keys for each morph target
3. Select a non-Basis key → go to Edit Mode → move vertices to the target position
4. Exit Edit Mode — the shape key now stores those vertex offsets

**The Value slider** (0.0–1.0) in Object Data → Shape Keys blends between Basis and the shape. Value can also be keyframed or driven.

### Shape Key Order Matters

The Basis key is always the reference. Shape keys are offsets from Basis, not from each other. If you want sequential morphs (mouth opens, then teeth show), you need Drivers to sequence them, not just stacking values.

**Relative vs Absolute:** Relative shape keys (default) are offsets from Basis. Absolute shape keys are evaluated based on an Evaluation Time value rather than individual value sliders — useful for mesh animations (water, cloth approximations).

### Shape Keys for Facial Rigging

The industry-standard facial rig in Blender combines shape keys and bones:
- Shape keys for expressions (smile, brow raise, jaw open)
- Bones as control handles that drive shape key values via Drivers
- Corrective shape keys (driven by Rotation Difference between two bones) fix problem areas where multiple shapes combine badly

**FACS (Facial Action Coding System):** Professional facial rigs use FACS — a standardized set of ~50 Action Units covering all possible face movements. Blender doesn't enforce FACS but professional character rigs follow its vocabulary.

---

## Timeline Controls and Playback

- `Space`: Play/pause (configurable — may be set to search)
- `Shift+Space`: Play/pause (guaranteed shortcut in all workspaces)
- `Left/Right Arrow`: Previous/next frame
- `Up/Down Arrow`: Previous/next keyframe
- `Home/End`: Jump to first/last frame

**Frame range:** Set start/end frames in the Timeline header or in Scene Properties → Frame Range. The render frame range is the same.

**Frame rate:** Set in `Output Properties → Frame Rate`. Standard choices: 24fps (film), 25fps (PAL TV), 30fps (NTSC TV), 60fps (games/web). Blender also supports fractional frame rates.

**Snapping:** With animation, enable `Snap to Keyframes` in the Timeline header for easier frame positioning.

---

## Blender 4.x Animation Changes

**Bone Collections (4.0+):** Replaced the 32-layer system. Bones are now organized into named, nestable collections with toggle visibility. The old `layer` attribute in Python is now `collections`.

**Rotation Mode:** Blender 4.x encourages Quaternion rotation for rigging (no Gimbal lock) and Euler for user-facing controls. Bones default to Quaternion in Pose Mode.

**Bake Action (for export):** Use `Object → Animation → Bake Action` to bake constraint/IK results to pure keyframes. Required before exporting to FBX/GLTF for game engines that don't support Blender constraints.

**Python note:** `bpy.ops.nla.bake()` vs `bpy.ops.object.bake_action()` — these are different operators. `nla.bake()` bakes a range to Action. `object.bake_action()` bakes physics/constraints.
