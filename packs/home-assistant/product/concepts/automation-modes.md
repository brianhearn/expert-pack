---
title: "Automation Modes"
type: concept
tags:
  - automation-fundamentals
  - single
  - restart
  - queued
  - parallel
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/automation-modes
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - automation-trigger-action.md
  - automation-templates-blueprints.md
  - presence-sensor-fusion.md
content_hash: sha256:c63d26ce5e30d0beb5e001f5e3e201655a3998b5b899dd0d7091884899e072fe
---
# Automation Modes

Automation mode controls what happens when a trigger fires while the automation is already running. `single` (default) ignores the new trigger; `restart` aborts and starts over — that is the correct mode for motion-activated lights so the off-delay resets.

## Automation Modes

Controls what happens when an automation triggers while it's already running:

| Mode | Behavior | Use Case |
|------|----------|----------|
| **Single** (default) | New trigger is ignored while running | Most automations |
| **Restart** | Stops current run, starts fresh | Motion-activated lights (restart timer on new motion) |
| **Queued** | New runs queue behind the current one | Sequential processing |
| **Parallel** | Multiple instances run simultaneously | Independent per-device logic |

**Most common mistake:** Using `single` mode for motion-activated lights. When motion re-triggers during the "off" delay, the new trigger is ignored and the light turns off anyway. **Use `restart` mode** for motion lights — it resets the off-delay timer on each new motion event.

## Related Concepts

- [[automation-trigger-action.md|automation trigger action]]
- [[automation-templates-blueprints.md|automation templates blueprints]]
- [[presence-sensor-fusion.md|presence sensor fusion]]
