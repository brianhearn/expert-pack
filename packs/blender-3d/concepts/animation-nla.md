---
id: blender-3d/concepts/animation-nla
title: "Animation — NLA Editor"
type: concept
tags:
  - animation
  - nla
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/animation-rigging.md
related:
  - animation-data-model.md
  - animation-drivers.md
content_hash: sha256:01a809429a75d58ebd52b1af287c16821c2d869d1d9516c7e6cd790d441bbc5a
---

# Animation — NLA Editor

The NLA (Non-Linear Animation) Editor treats Actions as strips you can stack, scale, blend, and sequence. Push Down converts the active Action into a strip; overlapping strips mix with influence. Game exports typically ship each Action as a clip.

## NLA Editor — Non-Linear Animation

The NLA (Non-Linear Animation) Editor treats Actions as clips that can be stacked, blended, and sequenced.

### Workflow

1. Create and finalize an Action in the Graph Editor
2. In the NLA Editor, click **Push Down** (down arrow icon) next to the action name — this pushes the active Action down to an NLA strip
3. The Action now exists as a strip in the NLA track
4. Create a new Action, push it down — repeat
5. NLA strips can be overlapped, scaled, and blended

### NLA Strips

**Strip operations:**
- `Tab` on a strip: enter it and edit the underlying Action
- `G`: slide in time
- `S`: scale (stretch/compress timing)
- `N` panel: strip properties — start/end frame, blend type, influence

**Blend types:** Replace (default, override), Add, Subtract, Multiply, Combine

**Blending:** Two overlapping strips can blend using their influence. An idle animation (100% influence) + "breathing" action (30% influence) = natural layering.

**Tweak Mode:** `Tab` on a selected NLA strip enters Tweak Mode, opening the strip's underlying Action for editing. Exit with `Tab` again.

### NLA for Game Engines

Standard workflow for preparing animations for Unity/Unreal export via FBX:
1. All animations are separate named Actions
2. Each Action is pushed down to the NLA as strips
3. Export with `NLA Strips as Clips` or bake all strips to individual actions
4. Game engine imports each Action as a separate animation clip

---

