---
id: blender-3d/concepts/modeling-modifier-stack
title: "Modeling — The Modifier Stack and Order"
type: concept
tags:
  - modeling
  - modifiers
  - modifier-stack
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/modeling-fundamentals.md
related:
  - modeling-key-modifiers.md
  - modeling-shrinkwrap-lattice.md
  - modeling-topology.md
content_hash: sha256:0fc6cefdd3be94545cb716243ef720b9a8549beea9d5e7a8ce0fb5888fe27ec9
---

# Modeling — The Modifier Stack and Order

Modifiers are non-destructive operations that stack — the output of each modifier feeds into the next. **Order matters enormously.** Hard-surface and organic models use different modifier combinations on that stack.

## Order Examples

- `Mirror → Subdivision Surface` = Mirror first, then subdivide the mirrored result. ✅ Correct
- `Subdivision Surface → Mirror` = Subdivide first, then mirror the dense mesh. Usually wrong.
- `Array → Curve` = Array the object, then deform along the curve. ✅ Correct for fences/chains
- `Boolean → Solidify` = Cut the hole, then add thickness. ✅ Correct for panel cutouts
- `Solidify → Boolean` = Add thickness, then cut. Can leave artifacts.

**Applying modifiers:** Applying bakes the result into the actual mesh and removes the modifier. Cannot be un-done after saving. Don't apply until you're done with that stage.

**Viewport vs Render levels:** Many modifiers (Subdivision Surface, Array) have separate settings for viewport display and final render. Keep viewport subdivision at 1 or 2; render at 2 or 3.

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

