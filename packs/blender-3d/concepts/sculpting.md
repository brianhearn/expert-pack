---
title: Sculpting
type: concept
tags:
- concepts
- sculpting
pack: blender-3d
retrieval_strategy: standard
id: blender-3d/concepts/sculpting
verified_at: '2026-04-10'
verified_by: agent
---

<!-- context: blender-3d/concepts/sculpting -->

# Sculpting

> **Lead summary:** Blender's sculpt system operates in three distinct paradigms — Dyntopo (dynamic mesh generation, for freeform exploration), Multi-resolution (subdivision-based layers, for production characters), and remeshed static topology (for clean retopo targets). Each has different performance characteristics, undo behavior, and compatibility with the rest of the pipeline. Choosing the wrong paradigm for the task is the most common sculpting mistake.

---

## Three Sculpting Paradigms

### Dyntopo (Dynamic Topology)

Dyntopo dynamically adds and removes triangles under the brush as you sculpt. The mesh isn't subdivided in advance — topology grows where you need it.

**When to use:**
- Concept sculpting and exploration (fast iteration)
- Adding major forms from a low-poly base
- Any time you need geometry where the base mesh doesn't have it

**When NOT to use:**
- When you have clean topology you want to preserve
- Final production sculpting (use Multires instead)
- After retopology

**Enable:** Sculpt Mode → Header → Dyntopo checkbox, or `Ctrl+D`

**Dyntopo settings:**

| Setting | Effect |
|---------|--------|
| Detail Size | Controls triangle size (smaller = more polygons). Constant Detail uses world-space units; Relative Detail uses screen-space. |
| Detail Type | `Relative` (adapts to distance), `Constant` (fixed world size), `Brush` (detail follows brush size). |
| Refine Method | `Subdivide Edges` (only adds), `Collapse Edges` (only removes), `Subdivide Collapse` (both — best for most work). |
| Smooth Shading | Applies smooth shading to new geometry automatically |

**Performance:** Dyntopo at high detail counts (5M+ triangles) gets slow. Keep your sculpt under 2M triangles during exploration. For detail work, switch to Multires.

**Warning:** Dyntopo destroys UV maps, vertex groups, shape keys, and any attribute data it touches. Once you enable Dyntopo on a mesh with UVs, the UVs in the sculpted area are gone. This is intentional — Dyntopo isn't meant for final production meshes.

**Dyntopo for hard-surface concept sculpting (expert settings):**
For mechanical parts and hard-surface concepts, Dyntopo requires specific configuration that differs from organic sculpting defaults:
- Use **Constant Detail** mode (not Relative) at size 2.0–4.0
- Refine method: **Subdivide Edges only** (not Collapse or both) — preserves sharp transitions
- Detail size **3.5px** is the community-recommended sweet spot for mechanical parts
- Run `Detail Flood Fill` after major strokes to regularize triangle density across the surface
- Enable Smooth Shading during sculpting to see hard-surface flow clearly
- This gives you a fast concept sculpt that can be retopologized — don't try to get final topology from Dyntopo

### Multi-Resolution (Multires)

Multires is the professional sculpting workflow. It subdivides a mesh into multiple levels (like Subdivision Surface) and lets you sculpt on each level independently.

**Key principle:** The base mesh topology is preserved. You sculpt high-frequency detail at high levels, major forms at lower levels.

**Setup:**
1. Start with a clean, retopologized mesh (or block-out)
2. In Object Mode, add Multires modifier (`Properties → Modifiers → Multires`)
3. Add subdivisions with `Subdivide` button — 6 levels is common (base → 64x polygon count)
4. Enter Sculpt Mode — you can sculpt at any level

**Level selector:** The three level controls in the Multires modifier:
- `Preview` — current level displayed in viewport (sculpt at this level)
- `Sculpt` — which level your brush strokes land on
- `Render` — which level is used at render time

Best practice: Sculpt at the highest level you need for detail, preview at a level that keeps viewport responsive.

**Multires Reshape:** Apply a mesh from another source onto the Multires base cage — useful for baking back external sculpt details.

**Sculpt levels workflow:**
- Level 1–2: Block out major forms, proportions
- Level 3–4: Secondary forms (muscle groups, major surface features)
- Level 5–6: Fine detail (skin pores, wrinkles, fabric weave)

This "funnel" approach — macro to micro — produces the best results.

### Remeshing (Voxel and Quad)

Remeshing converts any mesh into a clean, uniform topology. Used to:
- Reset after Dyntopo exploration
- Prepare for Multires sculpting
- Generate retopo-like mesh from a sculpt (Quad Remesh)

**Voxel Remesh:** `Ctrl+R` in Sculpt Mode (or via header). Creates a watertight mesh from voxel representation. The Voxel Size controls resolution (smaller = more polygons = more detail preserved). Good for:
- Combining multiple objects into one clean mesh
- Resetting Dyntopo mess before Multires
- Creating a closed volume from an open mesh

After voxel remesh, you lose UV maps and vertex groups (same as Dyntopo) but the new mesh is all-quad and uniform — ready for Multires.

**Quad Remesh (4.x):** Accessible via `Object → Remesh → QuadRemesh`. Uses the instant-meshes algorithm to generate quad-dominant retopology. Settings:
- `Target Quads`: how many quads to target
- `Edge Length`: use edge length mode instead of quad count
- `Use Vertex Color for Density`: paint density guides with vertex colors
- `Preserve Sharp Edges`: keep hard features in the remesh

Quad Remesh result is near-production-quality retopology — not perfect, but an excellent starting point. Better than manual retopology for simple objects; needs cleanup for complex ones.

---

## Sculpt Mode Interface

### Viewport Shading for Sculpting

Turn off overlays (viewport overlay button or `Alt+Z`). Use MatCap shading:

- `Z` → Solid display
- In viewport shading dropdown → MatCap → Choose a high-contrast clay-like matcap

Good clay matcaps: `clay_brown`, `jade`, `metal_shiny_hair`. Matcap shading removes material rendering overhead and shows surface detail clearly.

**X-Ray mode (`Alt+Z`):** Useful for selecting through the mesh but turns off MatCap — toggle off before sculpting.

### Symmetry

`X`, `Y`, `Z` symmetry toggles in the header. For character work:
- `X` symmetry handles bilateral symmetry (left=right face, body)
- Radial symmetry (set radial count) for patterns like spokes, petals

**Topology Mirror:** When enabled, Blender looks for mirror-paired vertices (same position on opposite sides) and applies strokes to both. Only works if the topology is already symmetrical. Without Topology Mirror, X symmetry mirrors strokes across the X axis regardless of topology.

---

## Brushes — The Core Toolkit

Blender 4.x ships with a greatly expanded brush library. The most important brushes:

### Form and Mass Brushes

**Draw (`X`):** The default. Pushes geometry outward (or inward with `Ctrl`). The workhorse for adding volume and shape. Falloff controls the brush profile.

**Clay (`C`):** Accumulates flat layers of "clay" — stops at a plane perpendicular to the stroke direction. More predictable than Draw for building up volume evenly.

**Clay Strips:** Like Clay, but uses a square falloff — better for building sharp ridges or flat planes. Very popular for hard-surface-informed organic work.

**Blob:** Inflates and "grows" the mesh. Good for fleshy protrusions, tumors, muscle bulges. The "Magnify" checkbox makes it less prone to spiky artifacts.

**Inflate (`I`):** Moves vertices along their normals — inflates the whole surface outward uniformly. Good for adding thickness or puffiness. `Ctrl` deflates.

**Smooth (`Shift`):** Available by holding `Shift` with any brush active. Relaxes vertices toward their average neighbors. Use constantly to clean up stroke artifacts.

### Carving and Detail Brushes

**Crease (`Shift+C`):** Pinches edges together — creates sharp creases, wrinkles, skin folds. Move across the mesh to draw a sharp groove.

**Pinch (`P`):** Pulls vertices toward the stroke center — creates sharp ridges and edges without actually removing geometry. Essential for:
- Ear helix details
- Eyelid creases
- Hard crease lines in stylized work

**Scrape:** Flattens a surface below a plane (scrapes off bumps). The opposite of Clay. Good for flat panels, planes, flattening the forehead or cheeks.

**Flatten/Contrast:** Averages the surface to a plane. Stronger than Smooth. Good for polishing after rough shaping.

**Grab (`G`):** Moves a cluster of geometry as a unit. No surface effect — just relocates vertices. Key for adjusting proportions without re-sculpting.

**Snake Hook (`K`):** Stretches and creates tubes of geometry from the surface. Used for horns, spikes, tentacles. Works best with Dyntopo enabled (adds geometry as it pulls).

**Multires Displacement Eraser:** Removes displacement from specific Multires levels without affecting other levels. Only works with Multires.

### Texture-Driven Brushes

Any brush can have a texture applied to its stroke. This is how skin pores, scales, and fabric are sculpted:

1. Open a tileable detail texture (grayscale, high contrast)
2. In the Brush Settings → Texture section, assign the texture
3. Set Mapping to `Area Plane` (most common for fabric/skin — tiles across the surface)
4. Adjust texture angle, scale, and strength

**Alpha textures** for custom brush shapes: A grayscale PNG (white = effect, black = none) defines the brush shape. Invaluable for damage detailing, logos, stamps.

---

## Face Sets

Face Sets are colored regions painted on the sculpt that act as isolation masks. Introduced in Blender 2.91.

**Why they're powerful:** You can restrict any brush to only its face set — equivalent to masking but stored per-face rather than per-vertex, so they're cleaner and persistent.

**Operations:**
- `Ctrl+W`: paint a new face set under the cursor
- `W` → `Extract Face Set` → Creates a new object from the selected face set region
- `W` → `Face Set from Visible` → Creates a face set from currently visible geometry
- In the header, toggle `Face Set Automasking` — brushes only affect the face set under the cursor

**Face set visibility:** `Alt+H` on a face set hides everything except that set. Use this to isolate body parts for detailed sculpting without accidentally affecting adjacent geometry.

**Workflow:** Segment a character into logical face sets (head, torso, left arm, right arm, etc.) at the start of the session. Toggle visibility freely to work in isolation.

---

## Masking

Masks prevent brush strokes from affecting masked areas. Different from Face Sets — masks are per-vertex (gradient capable) while face sets are per-face (binary).

**Paint mask:** In Sculpt Mode, `M` toggles the mask view. `Ctrl+click` with any brush paints a mask. `Alt+M` inverts mask. `Ctrl+I` inverts from the mask menu.

**Mask from Cavity:** `W → Mask → Mask from Cavity` — auto-generates a mask in the recessed areas of the mesh. Very useful for adding dirt/detail to only the crevices.

**Mask from Face Set:** `W → Mask → Mask from Face Set` — converts a face set to a mask.

**Box/Lasso mask (`B`, `L`):** Quick rectangular or freehand mask painting.

### Automask

Automask is a per-brush masking system that automatically restricts strokes based on topology or angle. Found in the brush settings (N panel while in Sculpt Mode):

| Automask Type | Effect |
|---------------|--------|
| Topology | Only affects connected geometry (no crossing gaps) |
| Face Sets | Only affects the face set under the cursor |
| Boundary Edges | Avoids mesh boundary edges |
| Cavity | Only affects protruding areas (inverse cavity) |
| Normal Limit | Only affects faces within an angle threshold of the brush angle |
| View Normal | Only affects faces pointing toward the camera |

Combine multiple automask types. "Topology + Normal Limit" is a popular combination for detailing that prevents stroke bleed-through.

---

## Sculpting Workflow — Character Head Example

A typical production-quality head sculpt workflow:

1. **Base mesh:** Start with a simple sphere (`Shift+A → Mesh → UV Sphere`, 32×32). Or use a more refined basemesh with eye sockets, lips, and ears blocked in as quads.

2. **Rough form (Dyntopo ON, ~20px detail):** Grab, Snake Hook, and Clay to establish the major volumes — cranium, cheekbones, jaw. Don't add small detail. Work at detail size ~10px.

3. **Voxel remesh:** Once the major form is good, voxel remesh at a size that gives you ~200–500k triangles (depends on character scale). This cleans up Dyntopo topology.

4. **Add Multires modifier** (6 subdivisions). Sculpt at level 2–3 for secondary forms.

5. **Secondary forms (level 3):** Define muscle groups, orbital rims, nasolabial folds, ear helix shape. Use Clay, Crease, Scrape.

6. **Detail pass (level 5–6):** Pores (texture brush with skin alpha), wrinkles (Crease brush), sub-dermal fat bumps. This is where you spend most time.

7. **Polish:** Smooth, Flatten, Polish brushes to clean up transitions and overworked areas.

8. **Retopology:** Quad Remesh for base, then refine manually. Or manual retopo using Shrinkwrap and a retopo overlay mesh.

---

## Mesh Filters

Mesh Filters (Sculpt Mode header → filter icon, or `Ctrl+T`) apply a brush-like effect across the entire mesh without a stroke:

| Filter | Effect |
|--------|--------|
| Smooth | Global smooth (like pressing Shift everywhere) |
| Surface Smooth | Projects smoothing onto the surface plane |
| Inflate | Uniform inflate/deflate entire mesh |
| Relax | Relaxes topology toward even distribution |
| Sharpen | Enhances existing high-frequency details |
| Enhance Details | Like Sharpen but more localized |
| Erase Displacement | For Multires, removes displacement at current level |
| Random | Adds noise (sculpt-level jitter) |

**Surface Smooth** is particularly useful after remeshing — it smooths without actually moving the surface position significantly, unlike regular Smooth which can alter forms.

---

## Performance Tuning

High-polygon sculpting requires careful configuration:

**GPU acceleration:** In `Preferences → System`, enable Metal (Mac), CUDA, or HIP GPU acceleration. Sculpting uses the GPU for display but mostly CPU for calculation.

**Multires display optimization:**
- Keep the `Preview` level 2–3 lower than your Sculpt level
- Use `Sculpt Mask → View Mask` to see mask without full detail overlay
- Disable face overlays (Overlay menu) during heavy sculpting

**Memory:** Each Multires level roughly multiplies vertex count by 4. A level-6 Multires on a 5000-vertex mesh = ~5000 × 4^6 = ~20 million vertices in memory. Blender needs ~4× this in actual RAM (undo history, attributes). 32GB RAM is comfortable for this; 16GB will struggle.

**Undo:** Sculpt undo is expensive — each stroke is a separate undo step. Reduce undo steps in Preferences if running out of RAM. `Preferences → System → Memory & Limits → Undo Steps`.

---

## Retopology After Sculpting

Sculpts need retopology for animation — the high-poly sculpt becomes the "target" for a new, clean low-poly mesh.

**RetopoFlow (add-on):** The most capable retopology add-on for Blender. Available on Blender Market (~$80) and on GitHub (free for Blender contributors). Provides specialized tools: Contours (edge loops around limbs), Strokes (polystrip chains), Patches (fill areas with a quad patch).

**Manual retopology workflow:**
1. Make the sculpt non-selectable in the Outliner (click the mouse cursor icon)
2. Add a new empty mesh object
3. In Edit Mode, enable `Face Snap` (snap to surface) and `Project Individual Elements`
4. Use the Shrinkwrap modifier with `Nearest Surface Point` to keep the retopo mesh on the sculpt
5. Draw edge loops following the sculpt's surface using the Snap cursor and `F` (fill)

**Shrinkwrap in Edit Mode approach:** Add a Shrinkwrap modifier to the retopo object targeting the sculpt. Enable `Adjust Edit Cage to Modifier Result` in the modifier. Now Edit Mode shows the retopo mesh projected onto the sculpt in real-time.

**Baking normals:** Once you have low-poly retopo, bake the high-poly sculpt's normals onto it. `Properties → Render → Bake`. Set type to `Normal`. Select the low-poly, then `Shift+select` the high-poly, enable `Selected to Active`, and bake. The result is a Normal Map that makes the low-poly look like the high-poly.
