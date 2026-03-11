# Hard Surface Modeling Workflow

Hard surface modeling refers to creating mechanical, manufactured, or architectural objects — things with defined sharp edges, smooth flat panels, precise geometry, and no organic deformation. Think robots, vehicles, weapons, machinery, architecture, consumer electronics.

This is one of the most common modeling domains in Blender, and one where technique diverges sharply from organic modeling.

---

## The Core Philosophy

Hard surface modeling in Blender revolves around one central workflow: **build a clean, low-poly control cage, then use the Subdivision Surface modifier to generate smoothness.** The control cage defines shape; edge density and support loops control sharpness.

This is the "subdiv workflow" and it produces:
- Clean, predictable geometry
- Easy editability at any stage
- Smooth renders with accurate normal-based shading
- Geometry that holds up at any subdivision level

The alternative — modeling everything at full density — is harder to edit and more error-prone. The Subdivision Surface modifier is your best tool for hard surface work.

---

## The Subdivision Surface Workflow

### Step 1: Build the Control Cage

Model the rough shape at low resolution. A complex mechanical component might start as 50–200 polygons. Don't add detail yet — get the proportions and major forms right first.

**Rules at this stage:**
- All quads — no triangles, no n-gons
- Clean topology that flows naturally around major forms
- Keep face count as low as possible while maintaining the shape
- Apply scale (`Ctrl+A → Scale`) before adding the Subdivision Surface modifier

### Step 2: Add Subdivision Surface Modifier

`Properties → Modifier → Add Modifier → Subdivision Surface`
- Viewport: Level 1 or 2 (preview shape)
- Render: Level 2 or 3

Toggle it on/off with the eye icon in the modifier stack to compare with/without subdivision.

### Step 3: Add Support Loops / Holding Edges

The Subdivision Surface rounds *everything* — which is what you want for smooth surfaces, but you need to control where sharp edges appear.

A **support loop** (or holding edge) is an edge loop placed close to the edge you want to remain sharp. The subdivision surface sees the tight loop and cannot smooth as aggressively — resulting in a crisper edge.

**Adding support loops:**
- `Ctrl+R` to add a Loop Cut
- Position it close to the edge you want to sharpen
- For symmetric sharpening: add one loop on each side of the target edge

**The 2-edge rule:** Most sharp edges in subdiv modeling need 2 support loops (one on each side). This creates a "pinching" effect that holds the edge crisp.

**Crease alternative:** Select an edge in Edit Mode, press `Shift+E` to set crease weight (0–1). Crease=1 gives a hard edge without support loops. Faster, but less predictable and doesn't interact as well with adjacent curvature. Use for edges deep inside the model or on truly flat panels.

### The "Level 2 Rule"

Your model should look correct at Subdivision Level 2. If it doesn't — if there are lumps, pinching, or shading artifacts at Level 2 — your topology needs work. Don't increase to Level 3 to hide topology problems; fix the topology instead.

Level 3 is for render quality only, not for hiding Level 2 problems.

---

## Shading Artifacts and How to Fix Them

Shading artifacts — dark splotches, creases, uneven gradients on smooth surfaces — are the enemy of hard surface work. They come from bad topology, not render settings.

**Common causes:**

**N-gons:** Five or more sided faces create unpredictable subdivision behavior. Find them with `Overlay → Statistics` or `Mesh Analysis → N-Gons`. Cut them into quads.

**Non-planar quads:** Four vertices that aren't coplanar create a twisted face that subdivides oddly. Usually from mesh operations that moved one vertex out of the face's plane. Fix by selecting the face and using `Face → Flatten Faces` or retopologizing.

**Poles in curved areas:** A vertex where 5 edges meet on a curved or subdivided surface creates a star artifact. Move poles to flat areas or outside the visible part of the model.

**Smooth shading required:** Add Subdivision Surface, then right-click → `Shade Smooth`. Hard surface models need smooth shading to work correctly with the subdiv modifier. Use `Shade Auto Smooth` (new in 4.1+) for automatic smooth/sharp edge detection.

**Incorrect normals:** Faces pointing the wrong direction appear dark (black) even with proper lighting. Check with `Overlay → Face Orientation` (blue = correct outward, red = inverted). Fix with `Mesh → Normals → Recalculate Outside` (`Shift+N` in Edit Mode).

---

## Boolean Workflow

Booleans are unavoidable for hard surface work — drilling holes, cutting complex shapes, making panel separations. Use them strategically.

### The Boolean Approach

**Fast workflow (destructive):**
1. Overlap the cutter object with the target object
2. Select target, add Boolean modifier → Difference
3. Choose the cutter object
4. Apply the modifier
5. Delete the cutter
6. Clean up resulting topology

**Non-destructive (recommended for complex work):**
1. Keep cutter objects on a dedicated "Cutters" collection, hidden from render
2. Boolean modifier stays live — you can adjust the cutter's position/shape
3. Apply all booleans only when the design is finalized

### Boolean Solver Choice

- **Exact:** Use by default. Handles complex intersections reliably. Slower but worth it.
- **Fast:** Use only for very simple operations where exact is overkill. Prone to failures on coplanar geometry.

### Boolean Cleanup

The most time-consuming part. After a Boolean, you'll typically have:
- N-gons where the cut intersects quads
- Triangles in odd places
- Poles where new loops emerge

**Cleanup workflow:**
1. Select all in Edit Mode after applying boolean
2. `Merge by Distance` to weld any floating vertices from the operation
3. `Select → Select All by Trait → Non-Manifold` to find problem areas
4. Manually route new edge loops from the cut to create clean quad flow
5. The key operation: `Knife (K)` to add connecting edges through n-gons
6. `Dissolve Edges (Ctrl+X)` to remove unnecessary edge loops

**The boolean "float" technique (Ian Hubert style):** For very complex booleans, don't clean up at all — just let the messy topology sit, apply smooth shading with auto-smooth edges, and accept the imperfection. The shading artifacts are often invisible at camera distance. This sacrifices topology quality for speed. Valid for background objects, game assets, and any situation where the mesh won't be subdivided.

---

## Key Tools Reference

### Bevel (`Ctrl+B`)

The single most important hard surface tool. Bevels selected edges.

**Keyboard modifiers while beveling:**
- Scroll wheel: change segment count (more segments = rounder bevel)
- `S`: toggle shape (controls profile — sharp vs round)
- `P`: profile curve (interactive profile shape)
- `V`: switch to vertex bevel (`Ctrl+Shift+B` also works)
- `C`: enable clamp overlap (prevents bevel going past adjacent geometry)
- `F`: specify vertex only
- `M`: miter type (affects corners)

**Bevel width types** (accessible via header after confirming):
- Offset: absolute distance from original edge
- Width: width of the bevel band
- Depth: depth from the original surface
- Percent: percentage of adjacent edge length

**Bevel workflow tip:** For a clean hard surface bevel, select the edges you want to bevel (typically: angle-based selection — `Select → Select Sharp Edges`), apply bevel with 2–3 segments, then clean up corners.

### Loop Cut (`Ctrl+R`)

Adds edge loops to the mesh.

- Move mouse before clicking to position the loop
- Scroll wheel before clicking to add multiple parallel loops
- After clicking: slide to position, `Right Click` to center, `Enter` to confirm
- `Alt+Double Click` on an edge to select the entire edge loop (not adding, just selecting)

**Loop cut for support loops:** Add loop cuts flanking your target edge, position them close to the edge for sharpness.

### Inset (`I`)

Creates an inset face inside selected faces.

- `I` for uniform inset across all selected faces
- `I` then `I` again for per-face mode (each face gets its own island inset, not connected)
- `B`: boundary (inset stays inside the face boundaries even if they share edges)
- `O`: offset even (compensates for non-square faces)

**Usage:** Essential for panel lines, screw holes, recessed details. Select the face(s) you want to detail, inset to create a frame, then extrude inward or bevel the inner edge.

### Knife (`K`)

Free-form cutting of the mesh. Click to start, click to add vertices, `Enter` to confirm.

- `Z`: cut-through mode (cuts visible and occluded faces)
- `C`: constrain to 45°/90° angles
- `A`: new cut (start a new cut without confirming the current one)
- `E`: start a new cut from the last vertex

**Best use:** Adding a single edge across an n-gon, connecting two vertices across a complex surface, or creating custom cuts that Loop Cut can't handle.

### Bridge Edge Loops

Select two (or more) edge loops and `Ctrl+E → Bridge Edge Loops`. Creates faces spanning the gap between them.

- Works on two separate open edge loops on one object
- Works across holes in a mesh (making the grid to fill between)
- Number of cuts (subdivisions) between the loops is adjustable in the operator panel

---

## Modifier Stack Patterns

### Classic Hard Surface Stack
```
Mirror
  ↓
Bevel (angle-based, 2 segments)
  ↓
Subdivision Surface (Catmull-Clark)
```

Order is critical: Mirror first (work on half the mesh), Bevel adds support loops for crispness, Subdivision subdivides the result. If you put Subdivision *before* Bevel, you'd be beveling the dense subdivided mesh — slow and messy.

### Hard Surface with Boolean
```
Boolean (Difference)
  ↓
Bevel (angle-based)
  ↓
Subdivision Surface
```

Boolean creates the cutout, Bevel adds support loops around the cut edges (for sharpness), Subdivision smooths.

### Mechanical Object with Array
```
Mirror
  ↓
Array (for repeated elements like bolts/vents)
  ↓
Subdivision Surface
```

Or for a curved array:
```
Array (Fixed Count or Fit Curve)
  ↓
Curve (deform along path)
  ↓
(apply both before subdivision if needed)
```

---

## Common Hard Surface Problems

### Problem: Subdivision Causes Ballooning
**Symptom:** Your low-poly box looks correct, but after subdivision it's huge and round.
**Cause:** Too few support loops — the subdivision is rounding all edges.
**Fix:** Add support loops near every edge you want to remain reasonably sharp.

### Problem: Bumpy Surface After Boolean
**Symptom:** After a boolean cut, the surrounding surface has shading artifacts.
**Cause:** The boolean created n-gons and non-planar faces.
**Fix:** Add edge loops bridging from the boolean cut to restore quad flow in the surrounding area.

### Problem: Bevel Creates Overlapping/Weird Geometry
**Symptom:** Bevel produces strange faces that overlap or fold.
**Cause:** Two selected edges are too close together, or the mesh has overlapping vertices.
**Fix:** Run `Merge by Distance` first. Enable `Clamp Overlap` in the bevel operation. Reduce bevel width.

### Problem: Mirror Seam Visible
**Symptom:** A visible seam or gap at the mirror center line.
**Cause:** Vertices near the center not being merged across the mirror plane, OR clipping not enabled.
**Fix:** In the Mirror modifier, enable `Clipping` (prevents vertices from passing the mirror plane). Increase `Merge Distance` if vertices still aren't connecting.

### Problem: Hard Edge After Shade Smooth
**Symptom:** A sharp crease appears on an edge that should be smooth after applying Shade Smooth.
**Cause:** That edge has a crease weight, or it's marked as a Sharp edge, or the Auto Smooth angle threshold is exceeded.
**Fix:** In Edit Mode, select the problem edge, `Edge Properties → Crease: 0`, `Edge Properties → Sharp: Disabled`. Or adjust Auto Smooth angle in Object Data Properties.
