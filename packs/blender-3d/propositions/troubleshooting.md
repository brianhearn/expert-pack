---
title: Propositions — Troubleshooting
type: proposition
tags:
- propositions
- troubleshooting
pack: blender-3d
retrieval_strategy: standard
id: blender-3d/propositions/troubleshooting
verified_at: '2026-04-10'
verified_by: agent
---

# Propositions — Troubleshooting

Atomic factual statements extracted from troubleshooting/common-mistakes.md.

---

### common-mistakes.md

- Unapplied scale (object scaled in Object Mode without Ctrl+A → Scale) is the #1 source of weird Blender behavior.
- Unapplied scale causes: uneven Subdivision Surface smoothing, incorrect physics simulation, inconsistent texture scaling, mirror modifier centered at wrong point, and wrong armature deformation.
- Fix unapplied scale with `Ctrl+A → Scale` or `Ctrl+A → All Transforms`; after applying, the N panel shows Scale X/Y/Z = 1.000.
- Apply scale before: adding an Armature modifier, setting up physics, adding texture coordinates, or mirroring.
- "Set Origin → Origin to Geometry" moves the origin dot without moving the mesh; "Geometry to Origin" moves the mesh without moving the origin — these do opposite things.
- There are multiple independent hiding mechanisms in Blender: `H` key (viewport only), Eye icon in Outliner, Camera icon (render), Monitor icon (disable completely), and Collection visibility.
- `Alt+H` in Object Mode unhides all objects hidden with `H`; in Edit Mode, `Alt+H` unhides hidden geometry within the mesh.
- Proportional Editing (`O`) is the most common cause of "why did my whole mesh move?" — visible as a large circle around the cursor when transforming.
- Pink/magenta textures mean Blender cannot find the image file; fix with `File → External Data → Find Missing Files` or `Pack Resources`.
- A dark or black render is caused by: no World lighting, lights on a hidden collection, clipping distance issues, very low exposure, wrong render engine, all-black material, or a Compositor node outputting black.
- Fireflies (bright pixel artifacts) in Cycles are fixed by clamping Indirect Light to 10–15 in `Render Properties → Light Paths → Clamp`.
- Noisy Cycles renders are fixed by: increasing samples, enabling adaptive sampling, enabling denoising, making lights larger, or checking light path bounce settings.
- EEVEE and Cycles intentionally look different — EEVEE glass requires Screen Space Refraction enabled and Blend Mode set to Alpha Hashed; SSS quality differs; some shader nodes don't work in EEVEE.
- Viewport clipping is fixed by adjusting `N Panel → View → Clip Start` and `Clip End`; the camera has separate Clip Start/End in Object Data Properties.
- `Home` key fits all objects in the viewport; `Numpad .` focuses on the selected object; `Numpad 5` toggles perspective/orthographic.
- Snapping issues: check that snapping is enabled (`Shift+Tab`), verify the snap target type in the header, and verify the snap base point (Closest Point, Active Element, Center of Bounding Box).
- Edit Mode edits only the active object's mesh; if multiple objects are selected before pressing Tab, all can be edited simultaneously (Blender 2.8+).
- Accidental Action proliferation (Action.001, Action.002, etc.) is caused by pressing `I` to keyframe with no active Action — always set a named Action in the Action Editor before keyframing.
- Actions with zero users (asterisk `*` prefix in Action Editor) will be purged on save; use Fake User (`F`) to preserve Actions not currently assigned to any object.
- IK pole target flipping is fixed by: placing the pole target farther from the limb (3–5 bone lengths), trying Pole Angle values of 0°, 90°, -90°, 180°, and testing at the full motion range before animating.
- NLA strip conflicts are diagnosed by using the Solo button (star icon) on a track to isolate it, or muting (`H`) individual tracks.
- Dyntopo destroys UV maps, vertex groups, and shape keys in sculpted areas — it is for starting from rough forms, not refining existing topology.
- Applying a modifier below the Multiresolution modifier collapses the base mesh and discards all high-level sculpt detail; always apply other modifiers BEFORE adding Multires.
- Physics cache location problems on render farms are caused by absolute cache paths; fix by setting relative paths (`//cache/sim_name/`) and using shared storage, or export to Alembic.
- Cloth passing through colliders is fixed by: increasing Cloth Collision Quality to 10–15, ensuring collider objects have the Collision physics property enabled, increasing cloth mesh resolution at problem areas, and reducing Collision Distance.
- `X → Dissolve Vertices` removes a vertex while preserving surrounding topology; `X → Vertices` (Delete) also removes all connected edges and faces, often collapsing more than intended.
- Lost objects can be recovered via `File → Recover → Last Session` (last normal close) or `File → Recover → Auto Save` (most recent autosave, default every 2 minutes).
- Broken links in `.blend` files are shown as orange in the Outliner; fix with `File → External Data → Report Missing Files` and then re-link.

### Game Engine Export (common-mistakes.md)

- Objects with negative scale (mirrored via S, X, -1) export to FBX with inverted normals because the exporter applies scale and flips face winding order; fix by applying scale (`Ctrl+A → Scale`) before export.
- Blender's Z-up to Unity's Y-up FBX conversion adds a -90° X rotation on the root; fix in Unity 2020.1+ by disabling "Use Space Transform" in Blender and enabling "Bake Axis Conversion" in Unity.
- Blender's Auto Smooth normals (especially the modifier-based system in 4.1+) can produce custom normals that the FBX exporter writes incorrectly; triangulating the mesh before export freezes shading and prevents the game engine from retriangulating differently.
- Geometry Nodes instances are not automatically realized during FBX or glTF export, producing empty or incomplete files; fix with Realize Instances before Group Output or `Ctrl+A → Visual Geometry to Mesh`.
- After Realize Instances, materials assigned per-instance via Set Material node may not transfer to glTF/FBX because the attribute domain changes from "Instancer" to "Geometry"; use Set Material Index with actual material slots on the object.
- When baking normals with Selected to Active, if the low-poly has sharp edges, mark all edges smooth before baking, then re-apply sharp edges with Auto Smooth afterward — the normal map encodes smoothing direction and sharp edges subtract from it.
- The "exploded mesh" technique for multi-part normal map baking moves each mesh element far apart so rays from one element don't hit neighbors, allowing higher ray cast distances without cross-element bleeding.
- "Extrude" in texture baking sets where rays originate (inflates the low-poly outward); "Max Ray Distance" filters how far rays travel — they serve different purposes, and a manually created cage mesh gives better control than Extrude alone for complex shapes.
