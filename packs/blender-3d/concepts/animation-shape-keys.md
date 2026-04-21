---
id: blender-3d/concepts/animation-shape-keys
title: "Animation — Shape Keys"
type: concept
tags:
  - animation
  - shape-keys
  - facial-rigging
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-04-21"
verified_by: agent
supersedes:
  - concepts/animation-rigging.md
related:
  - rigging-armatures.md
  - animation-nla-drivers.md
---

# Animation — Shape Keys

Shape Keys store alternative vertex positions as offsets from the Basis (rest) position.

---

## Setup

In Object Data Properties → Shape Keys:
1. Add the first shape key: `+` button → Name it `Basis` (mandatory — the neutral/rest position)
2. Add more shape keys for each morph target
3. Select a non-Basis key → go to Edit Mode → move vertices to the target position
4. Exit Edit Mode — the shape key stores those vertex offsets

**The Value slider** (0.0–1.0) blends between Basis and the shape. Value can be keyframed or driven.

---

## Key Rules

**Shape keys are offsets from Basis, not from each other.** If you want sequential morphs (mouth opens, then teeth show), you need Drivers to sequence them, not just stacking values.

**Relative vs Absolute:**
- Relative shape keys (default): offsets from Basis
- Absolute shape keys: evaluated based on an Evaluation Time value — useful for mesh animations (water, cloth approximations)

---

## Shape Keys for Facial Rigging

The industry-standard facial rig in Blender combines shape keys and bones:
- Shape keys for expressions (smile, brow raise, jaw open)
- Bones as control handles that drive shape key values via Drivers
- Corrective shape keys (driven by Rotation Difference between two bones) fix problem areas where multiple shapes combine badly

**FACS (Facial Action Coding System):** Professional facial rigs use FACS — a standardized set of ~50 Action Units covering all possible face movements. Blender doesn't enforce FACS but professional character rigs follow its vocabulary.

**Order matters:** Combine multiple shape keys with Drivers to control sequencing. For example, a jaw-open shape key driven by a jaw bone rotation Driver, with a corrective shape key for the chin area also driven by the same bone at higher rotation values.
