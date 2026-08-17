---
title: "Automation Triggers, Conditions, and Actions"
type: concept
tags:
  - automation-fundamentals
  - triggers
  - conditions
  - actions
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/automation-trigger-action
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - automation-conditions-actions.md
  - automation-modes.md
  - core-state-machine.md
content_hash: sha256:ce5681258b219029482f6b9abe38f4f7e173fee87d1a0b0c20a8e4d49b77ac21
---
# Automation Triggers, Conditions, and Actions

Every HA automation has three parts: triggers (what starts it), conditions (optional gates), and actions (what happens). A trigger starts the run — multiple triggers are OR. The `for` duration on a trigger ignores brief blips (motion clear for 5 minutes before lights off).

## The Three Parts

### 1. Triggers — "When this happens..."

A trigger starts the automation. Multiple triggers can be combined (OR logic — any one fires the automation).

**Common trigger types:**

| Trigger | What It Does | Example |
|---------|-------------|---------|
| **State** | Entity state changes | Motion sensor changes to `detected` |
| **Numeric State** | Entity crosses a threshold | Temperature goes above 80°F |
| **Time** | Specific time of day | Every day at 7:00 AM |
| **Time Pattern** | Recurring interval | Every 5 minutes |
| **Sun** | Sunrise/sunset (with offset) | 30 minutes before sunset |
| **Zone** | Person enters/leaves a zone | Person arrives home |
| **Device** | Device-specific trigger | Button pressed, motion detected |
| **Webhook** | External HTTP request received | IFTTT, external service calls HA |
| **MQTT** | MQTT message received | Sensor publishes to topic |
| **Event** | HA event fired | Tag scanned, automation triggered |
| **Template** | Template evaluates to true | Custom complex condition becomes true |

**Key concept: `for` parameter.** Many triggers support a `for` duration — "entity has been in this state for X time." This prevents false triggers from brief state changes. Example: "motion sensor has been `clear` for 5 minutes" before turning off lights.

## Related Concepts

- [[automation-conditions-actions.md|automation conditions actions]]
- [[automation-modes.md|automation modes]]
- [[core-state-machine.md|core state machine]]

Sources: [Automations](https://www.home-assistant.io/docs/automation/), [Triggers](https://www.home-assistant.io/docs/automation/trigger/).
