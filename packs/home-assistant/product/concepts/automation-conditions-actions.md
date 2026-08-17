---
title: "Automation Conditions and Actions"
type: concept
tags:
  - automation-fundamentals
  - conditions
  - actions
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/automation-conditions-actions
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - automation-trigger-action.md
  - automation-modes.md
  - automation-templates-blueprints.md
content_hash: sha256:e1fda6bc2be429e75ff89aeae097698bc515848d8d8cba77d9ff9f137b3e2904
---
# Automation Conditions and Actions

Conditions are optional gates evaluated after a trigger fires and before actions run. All conditions must be true (AND by default). If a condition fails, the automation stops — it does not wait. Actions then execute sequentially: call a service, delay, wait, choose, repeat, or fire an event.

### 2. Conditions — "Only if..."

Conditions are optional gates evaluated AFTER a trigger fires but BEFORE actions execute. All conditions must be true (AND logic by default).

**Common condition types:**

| Condition | What It Checks | Example |
|-----------|---------------|---------|
| **State** | Entity is in a specific state | `input_boolean.vacation_mode` is `on` |
| **Numeric State** | Entity value within range | Temperature between 65-80 |
| **Time** | Current time within window | Between 10 PM and 6 AM |
| **Sun** | Before/after sunrise/sunset | After sunset |
| **Zone** | Person is in a zone | Person is home |
| **Template** | Jinja2 template evaluates to true | Custom complex logic |
| **And/Or/Not** | Combine conditions | (A AND B) OR C |

**Critical distinction:** Triggers START the automation. Conditions GATE whether it continues. A trigger fires once when the event occurs. A condition is checked at that moment. If the condition fails, the automation silently stops — it doesn't wait for the condition to become true.
### 3. Actions — "Then do this..."

Actions are what the automation actually does. They execute sequentially (top to bottom).

**Common actions:**

| Action | What It Does | Example |
|--------|-------------|---------|
| **Call service** | Invoke an HA service | `light.turn_on`, `notify.mobile_app` |
| **Delay** | Wait before continuing | Wait 5 seconds |
| **Wait for trigger** | Pause until a condition is met | Wait until door closes |
| **Choose** | Conditional branching (if/else) | If daytime → bright; if night → dim |
| **Repeat** | Loop actions | Check every 30 seconds until done |
| **Fire event** | Trigger a custom event | Notify other automations |
| **Set variable** | Store a value for later use | Remember the triggering entity |

## Related Concepts

- [[automation-trigger-action.md|automation trigger action]]
- [[automation-modes.md|automation modes]]
- [[automation-templates-blueprints.md|automation templates blueprints]]
