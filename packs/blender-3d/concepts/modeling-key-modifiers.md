---
id: blender-3d/concepts/modeling-key-modifiers
title: "Modeling — Key Modifiers"
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
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/modeling-fundamentals.md
related:
  - modeling-modifier-stack.md
  - modeling-shrinkwrap-lattice.md
  - modeling-topology.md
content_hash: sha256:d736b06e645329a2e50dfbf36842d353edc98a6d3e4f1cbf826b96715975258d
---

# Modeling — Key Modifiers

Subdivision Surface, Mirror, Boolean, Solidify, Array, and Bevel are the non-destructive modifiers used in most hard-surface and organic stacks. Each has a few settings that determine whether the result is clean or artifact-ridden.

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

