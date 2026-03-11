# Common Blender Mistakes

A field guide to the most common confusing behaviors, mistakes, and gotchas in Blender — organized by how often they trip up users and how hard they are to diagnose.

---

## Transform Issues

### Unapplied Scale (The #1 Source of Weird Behavior)

**Symptoms:**
- Subdivision Surface creates uneven smoothing (one direction more subdivided than others)
- Physics simulation behaves incorrectly (object appears the wrong size to the physics engine)
- Textures scale unevenly across a mesh
- Mirror modifier has the center in the wrong place
- Armature deformation looks wrong
- Normal maps appear stretched in one direction

**Cause:** You scaled an object in Object Mode (`S` to scale), which changes the object's *scale factor* (shown in the N panel as Scale X/Y/Z). The mesh vertices didn't actually move — only the object's scale changed. When modifiers and physics read geometry, they see the unscaled mesh *plus* the scale factor, which causes inconsistencies.

**Fix:** `Ctrl+A → Scale` (applies scale), or `Ctrl+A → All Transforms` (applies location + rotation + scale). After applying scale, the N panel shows Scale X/Y/Z = 1.000.

**Prevention:** Apply scale immediately after doing any significant scaling in Object Mode. Especially before:
- Adding an Armature modifier
- Adding physics
- Adding texture coordinates
- Mirroring

**Edge case:** Armature objects should have scale applied too. Parent bones to the armature, not the armature to the mesh, when scale is involved.

---

### Object Origin Problems

**Symptoms:**
- Mirror modifier mirrors around the wrong point
- Array modifier offsets from an unexpected position
- Rotation/scale happens around an unexpected pivot
- Bone targeting seems offset from where it should be

**Cause:** The origin (orange dot) is not where you expect it. The origin is the reference point for transforms, modifiers, and parenting.

**Fix options:**
- `Right-click → Set Origin → Origin to Geometry` — moves origin to center of mass of the mesh
- `Right-click → Set Origin → Origin to 3D Cursor` — moves origin to wherever the 3D cursor is
- `Right-click → Set Origin → Geometry to Origin` — moves the mesh so the origin is at the current origin position (moves the geometry, not the origin)

**Important distinction:** "Set Origin → Origin to Geometry" moves the origin dot without moving the mesh. "Geometry to Origin" moves the mesh without moving the origin. These do opposite things. Read carefully.

---

## Visibility and Selection Issues

### The Hidden Object / Geometry Problem

**Symptom:** Something that was visible is gone. Or: you can see it in the Outliner but not the viewport.

**Cause (objects):** Multiple hiding mechanisms in Blender that work independently:
- `H` key: hides in viewport (but NOT in render by default). `Alt+H` to unhide all hidden objects.
- Eye icon in Outliner: toggles viewport visibility
- Camera icon in Outliner: toggles render visibility
- Monitor icon in Outliner: "Disable in Viewports" — turns off completely (not just hidden)
- Collection visibility: parent collection is hidden

**Cause (geometry):** In Edit Mode, `H` hides selected geometry. `Alt+H` unhides. This is Edit Mode only.

**The trick:** If an object seems to have disappeared, first try `Alt+H` in Object Mode (unhide all). Then check the Outliner — look for the eye icon state. Then check if it's on a hidden collection.

---

### Can't Select Anything

**Symptom:** Clicking in the viewport selects nothing, or the wrong things.

**Cause checklist:**
1. **Wrong selection mode:** In Edit Mode, you might be in Face select trying to click a vertex. Press `1/2/3` to switch.
2. **Overlapping objects:** A larger object is catching the click before the intended target. Try clicking in an area where only the target is visible, or use the Outliner to select.
3. **Objects not selectable:** In the Outliner, there's a "Restrict Select" icon (arrow/cursor icon) per object. If disabled, the object cannot be selected in the viewport.
4. **Wrong mode:** You might be in Edit Mode for one object — you can only select geometry of that specific object. Objects in the background cannot be selected while in Edit Mode.
5. **Clipping:** Object might be outside the viewport's clipping range (see below).
6. **Layer/Collection issue:** Object is in a collection that's excluded from the current View Layer.

---

### The Proportional Editing "Blue Circle of Death"

**Symptom:** You grab one vertex and the entire mesh moves with it (or a huge area deforms unexpectedly).

**Cause:** Proportional Editing is enabled (`O` toggles it). The falloff radius is large, affecting everything within that circle.

**Fix:** Press `O` to toggle off Proportional Editing. Or scroll the wheel while transforming to reduce the radius.

**How to spot it:** When active, you'll see a large circle around your cursor when you start a grab/scale/rotate. If this circle is very large, it will affect geometry far from your selection.

---

## Render and Material Issues

### Pink Textures / Missing Images

**Symptom:** Objects appear bright pink/magenta in Lookdev or Material Preview mode.

**Cause:** Blender cannot find the image file(s) referenced by the material. The image was moved, renamed, or was never saved to disk (for rendered images).

**Fix options:**
1. `File → External Data → Find Missing Files` — point Blender to the directory containing the missing files
2. `File → External Data → Reload Images` — forces a reload if files exist but weren't loaded
3. `File → External Data → Pack Resources` — embeds all external files into the .blend file (makes it self-contained but larger)
4. In the Image node, click the folder icon to manually browse for the file

**Prevention:** Use `File → External Data → Pack Resources` when sharing files or moving projects. Or: keep all textures in a `/textures/` subdirectory relative to the .blend file and use relative paths (`//textures/file.png`).

---

### Dark or Black Render

**Symptom:** Rendered output is unexpectedly dark or completely black.

**Cause checklist:**
1. **No World lighting:** No HDRI set, and no lights in the scene. Add at minimum an HDRI to the World shader.
2. **Lights on a hidden collection:** Lights exist but are hidden from render (camera icon in Outliner).
3. **Clipping distance:** Lights or objects are outside the camera's clip range.
4. **Camera sensor size / exposure:** Camera exposure settings or scene exposure set very low.
5. **Wrong render engine:** EEVEE requires light probe baking for indirect illumination. If you added a light but didn't bake probes, there may be no indirect light.
6. **Material set to fully black:** Check material Base Color — it might be black.
7. **Compositor fully black:** If you have a compositor setup, a node might be outputting black. Disconnect the compositor temporarily to test.

---

### Render Takes Forever

**Symptom:** Cycles render estimated at hours when it should be minutes.

**Cause checklist (in order of impact):**
1. **Too many samples:** 4096 samples for a still image is almost always overkill with denoising. Try 256–512 with denoising.
2. **Denoising not enabled:** Without denoising, you need 4–8x more samples for the same quality. Enable OIDN or OptiX denoiser.
3. **CPU rendering when GPU is available:** Check Render Properties → Device. Set to GPU Compute.
4. **Max Bounces too high:** More than 12 total bounces rarely improves quality. Set Total: 12, Diffuse: 4, Glossy: 4, Transmission: 12.
5. **No adaptive sampling:** Adaptive sampling stops early when pixels converge. It's enabled by default — check it's on.
6. **Dense geometry:** Millions of polygons slow ray tracing. Check if you can reduce with Decimate or avoid realizing instances.
7. **Volume in the scene:** Volumes (smoke, fire, fog) are extremely expensive to render. Reduce step rate or simplify.
8. **Caustics:** If enabled in EEVEE, can be slow. In Cycles, caustics via glass require many more samples.

---

### EEVEE and Cycles Look Completely Different

**Symptom:** A material looks correct in Cycles but wrong in EEVEE (or vice versa).

**This is expected** — they use fundamentally different rendering approaches. Specific differences:

**Transmission (glass/liquid):**
- In EEVEE, set `Material → Blend Mode → Alpha Hashed` or `Screen Space Refraction` must be enabled in Render settings
- IOR-based refraction may be incorrect or absent in EEVEE

**Reflections:**
- EEVEE uses Screen Space Reflections (SSR) — only reflects what's visible on screen. Cycles reflects everything accurately.

**Subsurface scattering:**
- EEVEE Next has improved SSS but it's still an approximation; Cycles is physically accurate

**Solution:** Design materials for one renderer or the other. If you need both, check your materials in both renderers and use material-specific adjustments. Some studios maintain separate material libraries for EEVEE and Cycles.

---

## Viewport Issues

### Objects Disappear at Distance / Clipping Problems

**Symptom:** Objects disappear when the camera gets too far away. Or: objects become invisible when zooming in very close.

**Cause:** Viewport or camera clipping plane settings.

**Fix:**
- In the 3D Viewport, press `N` to open the N Panel → `View` tab → `Clip Start` and `Clip End`
- For very large scenes: increase `Clip End` (e.g., 10000m or 1000000m)
- For very small objects: decrease `Clip Start` (e.g., 0.001m)
- The camera also has separate Clip Start/End in Object Data Properties (Camera)
- **The zooming-in problem:** If Clip Start is too large (e.g., 1m) and you zoom into a small object, the viewport clips through the surface. Reduce Clip Start.

**Scene scale issue:** If your objects are at an extreme scale (either very large or very small) relative to Blender's default unit scale, you'll constantly fight clipping. Set up your scene in appropriate units from the start: `Scene Properties → Units`.

---

### Viewport Empty / Can't Find Objects

**Symptom:** The viewport appears empty, or you can see objects in the Outliner but not in the viewport.

**Quick fixes to try in order:**
1. `Home` key — shows all objects in the scene (fits viewport to scene content)
2. `Numpad .` — focuses on the selected object
3. `Numpad 5` — toggles perspective/orthographic. You may have accidentally switched to an extreme orthographic view where nothing is visible.
4. `Numpad 1/3/7` — front/right/top views. Try cycling through these to see if objects appear.
5. Check that you're not looking at an empty collection — expand all collections in Outliner.

---

### Snapping Behaves Oddly

**Symptom:** Snap to vertex seems to snap to the wrong vertex. Or snap doesn't work at all.

**Cause checklist:**
1. **Snap not enabled:** `Shift+Tab` toggles snapping. Check the magnet icon in the header is active (highlighted).
2. **Wrong snap target:** The header shows what you're snapping to (Vertex, Edge, Face, etc.). Check it's set to what you expect.
3. **Snap base point:** "Closest Point" snaps the closest selected point to the target. "Active Element" snaps the active (last-selected) element. "Center of Bounding Box" snaps the center of the selection. This matters when multiple elements are selected.
4. **Face snapping: no individual projection:** When snap target is Face, the selected geometry will collapse onto a single face. Enable `Project Individual Elements` to project each vertex independently onto the surface.
5. **Snap to occluded geometry:** By default, snap can target hidden/backfacing geometry. Disable `Snap to Back Faces` for surface-only snapping.

---

## Edit Mode Gotchas

### Accidentally Working in Wrong Mesh

**Symptom:** You're editing vertices and the wrong object is being modified. Or: you select multiple objects and expect to edit all of them but only one responds.

**Cause:** Edit Mode edits the *active* object's mesh. If multiple objects are selected when entering Edit Mode, you can edit all of them (Blender 2.8+ supports multi-object Edit Mode). But the active object (brighter highlight) determines which mesh is the primary edit target for some operations.

**Fix:** Exit Edit Mode, reselect the correct object as active (click it last), then enter Edit Mode.

---

### Modifiers Not Applying As Expected

**Symptom:** Applied a modifier but the result looks different than the viewport preview showed.

**Common causes:**
1. **Viewport vs Render level different:** Subdivision Surface might show Level 1 in viewport but apply at Level 1 anyway. Check both fields.
2. **Modifier above another modifier:** The stacking order affects the result. Rearrange if needed.
3. **Object data used by multiple objects:** If two objects share the same mesh data (Alt+D duplicate), applying a modifier on one may behave unexpectedly.
4. **Scale not applied:** See the unapplied scale issue above — this causes many modifier anomalies.

---

### Geometry Disappeared After Delete

**Symptom:** You deleted some geometry in Edit Mode and unexpected faces/edges/vertices also disappeared.

**Cause:** Using `X → Vertices` deletes the vertices AND all connected edges and faces. This can collapse more geometry than expected.

**Alternatives:**
- `X → Dissolve Vertices` — removes the vertex but attempts to preserve the surrounding topology
- `X → Limited Dissolve` — dissolves geometry below a flatness threshold, preserving shape
- `Ctrl+X` — quick-dissolve the selection

**Rule:** When in doubt, use Dissolve instead of Delete for topology editing. Delete is for removing sections of a mesh; Dissolve is for topology cleanup.

---

## File and Data Management

### Lost Work — Object "Disappeared"

**Symptom:** Object was there, now it's gone. Can't undo back to it.

**Recovery options:**
1. `File → Recover → Last Session` — opens the autosaved file from when Blender last closed normally
2. `File → Recover → Auto Save` — opens the most recent autosave (default every 2 minutes)
3. Check the Outliner — object might be hidden (see visibility issues above)
4. `Orphan Data Purge` might have removed it: `File → Clean Up → Purge All` shows all orphaned data-blocks — if the mesh is there without a user, it was purged

**Prevention:** Save frequently. `Ctrl+S`. Enable incremental saves (`File → Save Incremental` creates numbered versions). Increase autosave frequency in `Preferences → Save & Load → Auto Save`.

---

### Missing Data After Opening File

**Symptom:** Opened a .blend file and materials, textures, or objects are missing or broken.

**Cause:** External file references are broken (see pink textures above). Or: linked library files are missing.

**For linked files:** `File → External Data → Report Missing Files` shows what's missing. Broken links appear orange in the Outliner.

**Prevention:** Use `File → External Data → Pack Resources` before archiving or sharing files. For linked libraries, maintain consistent directory structures and use relative paths.
