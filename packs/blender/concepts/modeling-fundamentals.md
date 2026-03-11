# Modeling Fundamentals

Blender's modeling toolkit is vast. This file focuses on the underlying principles and the non-obvious knowledge that separates good models from bad ones — topology theory, modifier strategy, and common failure modes.

---

## Why Topology Matters

"Topology" refers to the arrangement of vertices, edges, and faces in a mesh. It sounds abstract but has direct, concrete consequences:

**For subdivision:** Subdivision Surface works by averaging neighboring vertices. If your topology has triangles (tris) or poles (vertices with 5+ edges), the subdivision creates pinching, lumps, and artifacts. Quads subdivide predictably; triangles and n-gons don't.

**For deformation/animation:** When a character bends at the elbow, the geometry on the inside must compress and the outside must stretch. This only looks good if edges flow *around* the joint in loops — like wrist watches, not radial spokes. Bad edge flow at joints causes collapsing, pinching, and "candy wrapper" twists.

**For shading:** Blender calculates face normals to determine how light reflects. Non-planar quads (four vertices not on the same plane) cause shading inconsistencies. N-gons (5+ sided faces) are interpreted differently by different renderers. Tris on curved surfaces cause hard shading edges.

**For UV mapping:** Dense poles (6+ edges meeting at a vertex) stretch UV maps badly. Good topology gives UV unwrappers predictable, distortion-free results.

**The rule:** Aim for **all quads**, arranged in **edge loops** that follow the natural contours of the surface. Every other consideration is secondary.

### Poles

A pole is any vertex where the number of connected edges is not 4.

- **3-pole (E-pole):** Where three edges meet. Common at corners, topology transitions. Acceptable in most locations.
- **5-pole (N-pole):** Where five edges meet. Creates a subtle pinch under Subdivision Surface. Acceptable away from curved surfaces and deformation zones; problematic on faces, joints, and smooth areas.
- **6+-pole:** Highly problematic. Avoid almost everywhere.

The art of topology is routing edge loops so that poles end up in "safe" locations — flat areas, hidden areas, areas that don't deform.

---

## Edit Mode Essentials

### Selection Modes
`1` = Vertex select, `2` = Edge select, `3` = Face select. Hold `Shift` to combine modes (e.g., Vertex + Edge simultaneously). This is the source of "I can't select any faces" — you're in vertex select mode.

### Core Operations and Shortcuts

| Operation | Shortcut | Notes |
|-----------|----------|-------|
| Extrude | `E` | Extrudes selection along normals. `Alt+E` for extrude menu (Extrude Along Normals, Individual Faces, etc.) |
| Extrude Along Normals | `Alt+E → Along Normals` | Each face/vertex extrudes in its own normal direction — for complex surfaces |
| Inset | `I` | Creates an inset face inside selected face(s). `I` again while insetting to per-face mode |
| Bevel | `Ctrl+B` | Bevels selected edges. Scroll wheel controls segment count. `V` while bevel is active for vertex bevel. `P` for profile shape |
| Loop Cut | `Ctrl+R` | Adds an edge loop. Scroll before clicking to add multiple loops. Slide with mouse to position |
| Knife | `K` | Free-cut polygons. `Z` for cut-through. `C` for 45° constraint. `Enter` to confirm |
| Bridge Edge Loops | `Ctrl+E → Bridge Edge Loops` | Connects two selected edge loops with new faces |
| Fill | `F` | Creates a face from selected vertices/edges. `Alt+F` for fill using triangulation |
| Merge | `M` | Merges selected vertices (at center, at cursor, at first/last, by distance) |
| Dissolve | `Ctrl+X` | Removes vertices/edges while preserving surrounding topology (unlike Delete which leaves holes) |
| Separate | `P` | Separates selected geometry into a new object |
| Split | `Y` | Splits selection from the rest of the mesh (disconnects but stays as one object) |
| Mirror Selection | `Ctrl+Shift+M` | Selects the mirrored counterpart of the current selection (requires symmetry to be set) |

### Proportional Editing
`O` toggles proportional editing. When active, edits fall off gradually to surrounding vertices based on a radius (the blue circle). Scroll wheel changes radius. Falloff types (pie via `Shift+O`): Smooth, Sphere, Root, Inverse Square, Sharp, Linear, Constant, Random. **The #1 source of "why did my whole mesh move?"** — users forget proportional editing is on.

### Pivot Points
The center around which transformations rotate and scale.

`Period (.)` key opens the pivot point menu:
- **Bounding Box Center:** Geometric center of the selection bounding box
- **3D Cursor:** The red/white circle (position it first with `Shift+RMB`)
- **Individual Origins:** Each selected element transforms around its own center — critical for scaling multiple faces independently
- **Median Point:** Average position of all selected elements (default)
- **Active Element:** The last-selected element (highlighted brighter)

### Snapping
`Shift+Tab` toggles snapping. In the header, configure snap to: Vertex, Edge, Face, Volume, Edge Center, Edge Perpendicular, Increment. The **snap base point** (what part of the selected mesh snaps to the target) matters: Active Vertex, Closest Point, Center of Bounding Box, Median.

**Practical snap workflow:** Move a vertex to snap to another vertex → turn on snap to Vertex, set snap base to Active Vertex, then select the vertex you want to move and `G` to grab. The active vertex snaps to any surface.

---

## The Modifier Stack

Modifiers are non-destructive operations that appear to change the mesh but don't permanently alter the underlying data. They stack — the output of each modifier feeds into the next.

**Order matters enormously.** The mesh goes through modifiers from top to bottom in the Properties stack. Examples:

- `Mirror → Subdivision Surface` = Mirror first, then subdivide the mirrored result. Correct for most workflows.
- `Subdivision Surface → Mirror` = Subdivide first, then mirror the dense mesh. Usually wrong — wastes memory, may not join correctly.
- `Array → Curve` = Array the object, then deform along the curve. Correct for fences/chains.
- `Curve → Array` = Deform first (weird), then array. Usually wrong.
- `Boolean → Solidify` = Cut the hole, then add thickness. Correct for panel cutouts.
- `Solidify → Boolean` = Add thickness, then cut. Can leave artifacts.

**Applying modifiers:** Applying a modifier bakes its result into the actual mesh and removes the modifier. Once applied, it cannot be un-done (except with Ctrl+Z before saving). Don't apply modifiers until you're absolutely sure you're done with that stage of the model.

**Viewport vs Render levels:** Many modifiers (Subdivision Surface, Array) have separate settings for viewport display and final render. Keep viewport subdivision at 1 or 2; render at 2 or 3. High viewport subdivision kills performance.

---

## Key Modifier Deep Dives

### Subdivision Surface
- **Catmull-Clark:** Smooths the mesh — every subdivision adds loops and rounds corners. The standard for organic modeling.
- **Simple:** Only subdivides without moving vertices. Used for increasing mesh density on flat/angular surfaces without changing shape. Also useful before Displacement modifier.
- **Levels:** Each level multiplies face count by 4. Level 3 = 64x the original faces. Level 4 = 256x. Be conservative.
- **Crease:** In Edit Mode, select edges and `Shift+E` to set a crease value (0–1). Crease = 1 makes an edge resist smoothing, creating a sharp edge without support loops. Faster to work with than support loops, but gives slightly different results.
- **Modifier order:** Should almost always be last (or near last) in the stack. Mirror before it, Boolean before it.

### Mirror
- **Merge distance:** Sets how close vertices need to be to the mirror plane to get merged. Too small = gap on seam. Too large = merges far vertices.
- **Clipping:** When enabled, vertices on the mirror plane cannot move past it. Essential for keeping symmetry tight at seams. The most-forgotten setting.
- **Bisect:** Cuts the existing mesh along the mirror plane before mirroring. Useful when you started modeling non-symmetrically.
- **Mirror Object:** Can mirror across another object's origin instead of the object's own origin. Useful for off-center symmetry.

### Boolean
- **Exact solver:** More reliable, handles edge cases better. Use this by default.
- **Fast solver:** Faster but buggy on coplanar faces, complex geometry, or meshes with holes.
- **Collection Boolean:** Can use a collection as the cutter, applying the operation to all objects in the collection simultaneously.
- **Cleanup after Boolean:** Booleans almost always leave n-gons, tris, and poles. You must clean up the resulting topology manually or accept the artifacts. This is the biggest bottleneck of the Boolean workflow.
- **The "boolean cutter" workflow:** Keep the cutter object on a separate collection, hidden from render. Use it for multiple booleans. Apply all booleans at the end when shape is finalized.

### Solidify
- **Thickness:** How far the new geometry is offset. Can be negative.
- **Offset:** -1 = offset inward, 0 = offset centered, +1 = offset outward.
- **Complex mode:** Handles non-manifold geometry (open meshes, holes) better than Simple mode. Required for architectural meshes with open edges.
- **Fill Rim:** Fills the open edges with cap faces. Usually what you want.

### Array
- **Fixed Count:** Duplicate N times.
- **Fixed Length:** Fill a specific distance with as many duplicates as fit.
- **Fit Curve:** Match a curve object's length.
- **Relative Offset:** 1.0 = array spacing equals the object size (edge-to-edge touching). 1.1 = slight gap. 0.9 = slight overlap.
- **Object Offset:** Each array copy is transformed by the difference between two objects' transforms. This is how you create radial/circular arrays — use an empty as the offset object, rotate the empty.
- **Curve Modifier combination:** `Array (Fit Curve)` + `Curve` modifier on the same object creates geometry that follows a curve with the correct number of repetitions.

### Bevel
- **Width:** Physical size of the bevel. Can be percentage of edge length or absolute units.
- **Segments:** Number of edge loops in the bevel. 1 = sharp chamfer. 3+ = smooth rounding.
- **Profile:** Shape of the bevel between segments. 0.5 = circular arc. 0 = concave. 1 = convex/sharp. The custom profile option gives full bezier control.
- **Limit Method:** Which edges get beveled. "Angle" (only edges above a certain angle) is the most useful — automatically bevels sharp edges while leaving flat areas alone.
- **Bevel Weight:** In Edit Mode, assign per-edge weights (`Ctrl+Shift+B` doesn't do this — you need the "Mean Bevel Weight" edge property in Item panel). Then set the modifier to use Weight limit method.

### Shrinkwrap
Snaps a mesh's vertices onto the surface of another object. Three modes: Nearest Surface Point, Project (along axis), Nearest Vertex. Essential for: cloth/armor fitting over a body, conforming retopo to a sculpt, layering decals onto curved surfaces.

### Lattice
A deformation cage for another object. Add a Lattice object, size it to encompass your target, add a Lattice modifier to the target pointing to the Lattice. Edit the Lattice's control points in Edit Mode to deform the target object smoothly. Faster than Proportional Editing for large-scale smooth deformations.

### Decimate
- **Collapse:** Merges vertices by shortest edge. Ratio controls target percentage.
- **Un-Subdivide:** Reverses subdivision — only works on meshes that were subdivided uniformly.
- **Planar:** Merges faces that are coplanar (same angle). Best for architectural/CAD imports with tons of unnecessary coplanar tris.
- **Preserve Seams/Sharp/Boundaries:** Prevents decimation from crossing UV seams, sharp edges, and object boundaries. Enable these for game-ready bake meshes.

---

## Hard Surface vs Organic Modeling

These are two fundamentally different philosophies:

**Hard Surface (mechanical objects):**
- Goal: clean, precise shapes with defined sharp edges and smooth panels
- Approach: work at low poly, use subdivision to smooth, use support loops and creases to control edge sharpness
- Key modifiers: Mirror, Boolean, Subdivision Surface, Bevel
- Reference: industrial design, vehicles, robots, weapons, props

**Organic (characters, creatures, natural forms):**
- Goal: smooth, flowing surfaces that deform believably under animation
- Approach: work with edge loops flowing around anatomy/contours, sculpt from reference
- Key tools: sculpting (Dyntopo for initial shape, Multi-Res for detail), retopology, subdivision
- Reference: human/animal anatomy, cloth, organic architecture

Most real models combine both — a robot character needs organic-ish geometry at the joints for deformation, and mechanical parts elsewhere.

---

## Common Mistakes in Modeling

### Unapplied Scale (The #1 Gotcha)
**Symptom:** Subdivision Surface creates uneven smoothing, physics simulation behaves oddly, textures scale inconsistently.
**Cause:** You scaled the object in Object Mode, which changes the *object's* scale factor without changing the underlying mesh dimensions. Modifiers and physics use the object's scale to interpret geometry — a scale of (1, 1, 3) means the physics engine thinks your object is 3x taller than it looks.
**Fix:** `Ctrl+A → Scale` (or All Transforms) to apply the scale, baking it into the mesh. Do this before applying modifiers or setting up physics.

### N-Gons Under Subdivision Surface
N-gons (5+ sided faces) create unpredictable smoothing under Subdivision Surface. They sometimes look fine in small areas, but can create pinching or flat spots. Use `Overlay → Face Orientation` to check, or use Mesh Analysis (Overlay → Mesh Analysis → N-Gons).

### Overlapping Vertices
Vertices at the exact same position create zero-length edges, non-manifold geometry, and rendering artifacts. Fix with `Mesh → Merge by Distance` (previously "Remove Doubles") — select all in Edit Mode and run it. Set the merge distance appropriately for your scale.

### Non-Manifold Geometry
A manifold mesh is one where every edge is shared by exactly 2 faces — a closed surface with no holes, no intersections, no internal faces. Non-manifold geometry causes issues with:
- Solidify modifier (can't figure out inside/outside)
- 3D printing
- Boolean operations
- Physics simulation
Check for non-manifold edges: `Select → Select All by Trait → Non-Manifold`. 3D-Print Toolbox add-on (built-in) has automated checks.

---

## Retopology

Retopology is the process of creating new, clean topology over existing high-resolution geometry (usually a sculpt). The sculpt captures the shape; the retopo creates a mesh suitable for deformation, subdivision, or real-time use.

**When you need retopology:**
- After sculpting a character (sculpt mesh = millions of tris, useless for animation)
- After importing CAD or scan data (non-quads, excessive density)
- When fixing topology that's gotten too messy to work with

**Manual retopo workflow in Blender:**
1. Import or sculpt your high-res reference mesh
2. Add a new empty mesh object on top of it
3. Enable `Snap to Face` with `Project Individual Elements` — your new geometry will snap to the surface
4. Use `LoopTools` add-on (built-in) for evenly-spaced loops
5. Draw quad-by-quad with `F` (face creation)
6. Use `Shrinkwrap` modifier (with Nearest Surface mode) for real-time snapping of the retopo mesh to the sculpt

**Automated retopo:**
- **QuadriFlow** (built-in, `Mesh → Remesh → QuadriFlow`) — Creates an all-quad mesh. Good for organic shapes. Results vary; usually needs manual cleanup.
- **Instant Meshes** (external free tool) — Feed it your high-res mesh, get a clean quad mesh back. Often better results than QuadriFlow for complex shapes.
- **Remesh modifier** (Voxel mode) — Not retopo exactly, but creates uniform density mesh for further sculpting.

**After retopology:** Bake normal maps from the high-res sculpt onto the low-res retopo mesh using Blender's bake system (or Marmoset Toolbag/Substance Painter for better quality bakes).
