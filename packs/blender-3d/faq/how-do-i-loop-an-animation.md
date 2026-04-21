---
title: How Do I Loop an Animation?
type: faq
tags:
- animation-looping
- animation-rigging
- character-animation
- faq
- motion-graphics
pack: blender-3d
retrieval_strategy: standard
id: blender-3d/faq/how-do-i-loop-an-animation
verified_at: "2026-04-21"
verified_by: agent
schema_version: "4.1"
---
<!-- context: section=faq, topic=animation-looping, related=animation-rigging,character-animation,motion-graphics -->

# How Do I Loop an Animation?

> **Lead summary:** Loop animations by setting keyframe extrapolation mode to "Make Cyclic" in the Graph Editor (Channel → Extrapolation Mode → Make Cyclic), ensuring the first and last keyframes match, and using the Cycles modifier for fine control. For NLA strips, set the Action Clip repeat count.

## Quick Method: Make Cyclic

1. Open the **Graph Editor** (Shift+F6 or split a panel)
2. Select the channels you want to loop (A to select all)
3. Go to **Channel → Extrapolation Mode → Make Cyclic (F-Modifier)**
4. This adds a Cycles modifier that repeats the curve infinitely

**Important:** Your first and last keyframes should have the **same value** for a seamless loop. If frame 1 has rotation 0° and frame 24 has rotation 350°, the loop will "pop" at the seam.

## Seamless Loop Tips

- **Match first/last keyframes exactly** — select the first keyframe, note its value, set the last keyframe to the same value.
- **Remove duplicate frame** — if your animation is 24 frames (1-24) and frame 1 = frame 24, set your playback range to frames 1-23. Otherwise you'll hold the same pose for 2 frames at the seam.
- **Use Linear interpolation at loop points** — in the Graph Editor, select the seam keyframes and press T → Linear. This prevents easing that creates visible hitches.

## NLA Strip Looping

For character animations or reusable loops:
1. Push the action down to an **NLA Strip** (Stash or Push Down in the Action Editor)
2. In the NLA Editor, select the strip
3. In the sidebar (N), set **Repeat** to the number of loops
4. Or enable **Cyclic Strip Time** under Strip → Action Clip for infinite looping

## Cycles Modifier (Fine Control)

In the Graph Editor → Sidebar → Modifiers tab:
- **Before/After Mode:** `Repeat with Offset` (accumulates — good for walk cycles moving forward) or `Repeat` (exact loop — good for idle animations)
- **Before/After Cycles:** 0 = infinite, or set a specific count

## Walk Cycle Specific

For a walk cycle that moves forward:
- Animate the walk in-place (no root translation)
- Use the NLA Editor to combine the walk strip with a separate linear movement strip
- Or use `Repeat with Offset` on the root bone's Y translation channel

## Related

- [[animation-data-model.md|Animation & Rigging]]
- [[character-animation.md|Character Animation Workflow]]
- [[motion-graphics.md|Motion Graphics Workflow]]
