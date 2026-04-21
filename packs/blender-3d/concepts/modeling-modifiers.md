---
id: blender-3d/concepts/modeling-modifiers
title: "Modeling — The Modifier Stack"
type: concept
tags:
  - modeling
  - modifiers
  - subdivision-surface
  - boolean
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-04-21"
verified_by: agent
supersedes:
  - concepts/modeling-fundamentals.md
related:
  - modeling-topology.md
---

# Modeling — The Modifier Stack

Modifiers are non-destructive operations that stack — the output of each modifier feeds into the next. **Order matters enormously.**

---

## Order Examples

- `Mirror → Subdivision Surface` = Mirror first, then subdivide the mirrored result. ✅ Correct
- `Subdivision Surface → Mirror` = Subdivide first, then mirror the dense mesh. Usually wrong.
- `Array → Curve` = Array the object, then deform along the curve. ✅ Correct for fences/chains
- `Boolean → Solidify` = Cut the hole, then add thickness. ✅ Correct for panel cutouts
- `Solidify → Boolean` = Add thickness, then cut. Can leave artifacts.

**Applying modifiers:** Applying bakes the result into the actual mesh and removes the modifier. Cannot be un-done after saving. Don't apply until you're done with that stage.

**Viewport vs Render levels:** Many modifiers (Subdivision Surface, Array) have separate settings for viewport display and final render. Keep viewport subdivision at 1 or 2; render at 2 or 3.

---

## Key Modifiers

### Subdivision Surface
- **Catmull-Clark:** Smooths the mesh — rounds corners. Standard for organic modeling.
- **Simple:** Only subdivides without moving vertices. Used before Displacement modifier.
- **Crease:** In Edit Mode, select edges and `Shift+E` to set a crease value (0–1). Crease = 1 makes an edge resist smoothing (sharp edge without support loops).
- **Order:** Should almost always be last (or near last) in the stack.

### Mirror
- **Merge distance:** How close vertices need to be to the mirror plane to get merged. Too small = gap on seam.
- **Clipping:** When enabled, vertices on the mirror plane cannot move past it. Essential for keeping symmetry tight at seams. **The most-forgotten setting.**
- **Bisect:** Cuts the existing mesh along the mirror plane before mirroring.
- **Mirror Object:** Mirror across another object's origin instead of the object's own.

### Boolean
- **Exact solver:** More reliable, handles edge cases better. Use this by default.
- **Fast solver:** Faster but buggy on coplanar faces or complex geometry.
- **Cleanup after Boolean:** Booleans almost always leave n-gons, tris, and poles. Must clean up manually or accept artifacts.
- **The "boolean cutter" workflow:** Keep the cutter object on a separate hidden collection. Apply all booleans at the end when shape is finalized.

### Solidify
- **Thickness:** How far the new geometry is offset.
- **Offset:** -1 = offset inward, 0 = centered, +1 = offset outward.
- **Complex mode:** Handles non-manifold geometry better than Simple mode. Required for architectural meshes with open edges.
- **Fill Rim:** Fills open edges with cap faces.

### Array
- **Fixed Count:** Duplicate N times.
- **Relative Offset:** 1.0 = array spacing equals the object size. 1.1 = slight gap.
- **Object Offset:** Each array copy is transformed by the difference between two objects' transforms. This is how you create radial/circular arrays — use an empty as the offset object, rotate the empty.
- **Curve Modifier combination:** `Array (Fit Curve)` + `Curve` modifier creates geometry that follows a curve with the correct number of repetitions.

### Bevel
- **Segments:** 1 = sharp chamfer. 3+ = smooth rounding.
- **Profile:** Shape of the bevel. 0.5 = circular arc. 0 = concave. 1 = convex.
- **Limit Method → Angle:** Only bevels edges above a certain angle. Automatically bevels sharp edges while leaving flat areas alone.

### Shrinkwrap
Snaps a mesh's vertices onto the surface of another object. Three modes: Nearest Surface Point, Project, Nearest Vertex.
Essential for: cloth/armor fitting over a body, conforming retopo to a sculpt, layering decals onto curved surfaces.

### Lattice
A deformation cage for another object. Add a Lattice object, size it to encompass your target, add a Lattice modifier to the target pointing to the Lattice. Edit the Lattice's control points to deform the target smoothly.

### Decimate
- **Collapse:** Merges vertices by shortest edge. Ratio controls target percentage.
- **Planar:** Merges coplanar faces. Best for architectural/CAD imports with tons of unnecessary coplanar tris.
- **Preserve Seams/Sharp/Boundaries:** Prevents decimation from crossing UV seams and sharp edges. Enable for game-ready bake meshes.

---

## Hard Surface vs Organic Modeling

**Hard Surface (mechanical objects):**
- Goal: clean, precise shapes with defined sharp edges and smooth panels
- Approach: work at low poly, use subdivision to smooth, use support loops and creases for edge sharpness
- Key modifiers: Mirror, Boolean, Subdivision Surface, Bevel

**Organic (characters, creatures, natural forms):**
- Goal: smooth, flowing surfaces that deform believably under animation
- Approach: edge loops flowing around anatomy/contours, sculpt from reference
- Key tools: sculpting, retopology, subdivision

Most real models combine both — a robot character needs organic-ish geometry at the joints for deformation, and mechanical parts elsewhere.
