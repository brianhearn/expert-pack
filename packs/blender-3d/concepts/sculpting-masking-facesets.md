---
id: blender-3d/concepts/sculpting-masking-facesets
title: "Sculpting — Face Sets, Masking, Filters, and Performance"
type: concept
tags:
  - sculpting
  - masking
  - face-sets
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/sculpting.md
related:
  - sculpting-brushes.md
  - sculpting-multires-remesh.md
content_hash: sha256:1977dd143dc8100db7106178c1cf603be239e1a6d82b29d56a04b25f5214db20
---

# Sculpting — Face Sets, Masking, Filters, and Performance

Face sets and masks restrict which vertices a sculpt brush can affect. Face sets are persistent per-face regions; masks are per-vertex and gradient-capable. Filters and display or undo settings keep heavy Multires sessions usable.

## Face Sets

Face Sets are colored regions that act as isolation masks. Persistent per-face (vs vertex-based masks).

**Operations:**
- `Ctrl+W`: paint a new face set under the cursor
- `W → Extract Face Set`: Creates a new object from the selected region
- `Alt+H` on a face set: hides everything except that set

**Face set automasking:** Toggle in header — brushes only affect the face set under the cursor.

**Workflow:** Segment a character into logical face sets (head, torso, left arm, right arm, etc.) at the start of the session. Toggle visibility freely to work in isolation.

---

## Masking

Masks prevent brush strokes from affecting masked areas. Per-vertex (gradient capable), different from Face Sets (per-face, binary).

- `M`: toggle mask view
- `Ctrl+click` with any brush: paint a mask
- `Alt+M`: invert mask
- `W → Mask → Mask from Cavity`: auto-generates mask in recessed areas — useful for adding dirt/detail to only crevices
- `B`, `L`: box/lasso mask painting

### Automask

Per-brush masking that automatically restricts strokes:

| Automask Type | Effect |
|---------------|--------|
| Topology | Only affects connected geometry |
| Face Sets | Only affects the face set under the cursor |
| Cavity | Only affects protruding areas |
| Normal Limit | Only affects faces within an angle threshold |
| View Normal | Only affects faces pointing toward the camera |

"Topology + Normal Limit" is a popular combination for detailing without stroke bleed-through.

---

## Mesh Filters

Applied via `Ctrl+T` — brush-like effects across the entire mesh without a stroke:

| Filter | Effect |
|--------|--------|
| Smooth | Global smooth |
| Surface Smooth | Projects smoothing onto the surface plane |
| Inflate | Uniform inflate/deflate |
| Relax | Relaxes topology toward even distribution |
| Sharpen | Enhances existing high-frequency details |
| Random | Adds noise (sculpt-level jitter) |

**Surface Smooth** is particularly useful after remeshing — smooths without significantly altering surface position.

---

## Performance Tuning

**Multires display optimization:**
- Keep `Preview` level 2–3 lower than your Sculpt level
- Disable face overlays during heavy sculpting

**Memory:** A level-6 Multires on a 5000-vertex mesh = ~20 million vertices in memory. Blender needs ~4× this in actual RAM (undo history, attributes). 32GB RAM is comfortable; 16GB will struggle.

**Undo:** Sculpt undo is expensive — each stroke is a separate undo step. Reduce undo steps in `Preferences → System → Memory & Limits → Undo Steps` if running out of RAM.

