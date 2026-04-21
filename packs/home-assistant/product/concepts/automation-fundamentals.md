---
title: Automation Fundamentals
type: concept
tags:
- automation-fundamentals
- concepts
- core-architecture
- protocols
- yaml-configuration
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/automation-fundamentals
verified_at: "2026-04-21"
verified_by: agent
schema_version: "4.1"
concept_scope: single
---
<!-- context: section=concepts, topic=automation-fundamentals, related=core-architecture,yaml-configuration,protocols -->
---
sources:
  - type: documentation
    url: "https://www.home-assistant.io/docs/automation/"
    date: "2026-03"
  - type: documentation
    url: "https://www.home-assistant.io/docs/automation/trigger/"
    date: "2026-03"
  - type: documentation
    url: "https://www.home-assistant.io/docs/automation/templating/"
    date: "2026-03"
---

# Automation Fundamentals

> **Lead summary:** Every HA automation has three parts: **triggers** (what starts it), **conditions** (optional gates that must be true), and **actions** (what happens). Triggers fire on state changes, time events, or other signals. Conditions filter when the automation should actually run. Actions execute services (turn on lights, send notifications, etc.). Understanding this trigger → condition → action flow, plus automation modes and the Jinja2 template system, is essential for building reliable automations.

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

## Automation Modes

Controls what happens when an automation triggers while it's already running:

| Mode | Behavior | Use Case |
|------|----------|----------|
| **Single** (default) | New trigger is ignored while running | Most automations |
| **Restart** | Stops current run, starts fresh | Motion-activated lights (restart timer on new motion) |
| **Queued** | New runs queue behind the current one | Sequential processing |
| **Parallel** | Multiple instances run simultaneously | Independent per-device logic |

**Most common mistake:** Using `single` mode for motion-activated lights. When motion re-triggers during the "off" delay, the new trigger is ignored and the light turns off anyway. **Use `restart` mode** for motion lights — it resets the off-delay timer on each new motion event.

## Templates (Jinja2)

HA uses Jinja2 templates for dynamic values in automations, scripts, and sensors. Templates are powerful but also the most common source of confusion.

### When to Use Templates

- **Dynamic service data:** Set brightness based on time of day
- **Complex conditions:** Logic that can't be expressed with built-in conditions
- **Message formatting:** Dynamic notification text
- **Template sensors:** Calculated values from other entities

### Essential Template Patterns

**Get an entity's state:**
```jinja2
{{ states('sensor.outdoor_temperature') }}
```

**Get an attribute:**
```jinja2
{{ state_attr('light.living_room', 'brightness') }}
```

**Numeric comparison (states are always strings — cast them):**
```jinja2
{{ states('sensor.outdoor_temperature') | float > 80 }}
```

**Trigger variable (which entity triggered the automation):**
```jinja2
{{ trigger.entity_id }}
{{ trigger.to_state.state }}
{{ trigger.from_state.state }}
```

**Time-based logic:**
```jinja2
{{ now().hour >= 22 or now().hour < 6 }}
```

**Count entities in a state:**
```jinja2
{{ states.light | selectattr('state', 'eq', 'on') | list | count }}
```

### Template Anti-Patterns

- **Don't use templates where built-in conditions work.** A template condition checking `states('light.x') == 'on'` should just be a state condition. Templates are slower and harder to debug.
- **Always cast types.** `states()` returns strings. Use `| float`, `| int`, `| bool` for comparisons.
- **Use `states('entity_id')` not `states.sensor.name.state`.** The latter breaks if the entity doesn't exist. The former returns `'unknown'`.
- **Test in Developer Tools → Template.** Always test your templates before putting them in automations.

## Blueprints

Pre-made automations shared by the community. You configure the inputs (which entities, what times, etc.) without writing YAML. Found in Settings → Automations → Blueprints, or import from the community blueprint exchange.

**Good for:** Standard patterns (motion lights, humidity fan, low battery alerts). **Limited when:** You need custom logic or complex conditions beyond what the blueprint exposes.

## Best Practice: Entity ID vs Device ID

**Always use entity_id in automations, not device_id.**

- Entity IDs are human-readable and stable (`light.kitchen_ceiling`)
- Device IDs are opaque hashes that can change if you re-pair a device
- If you create an automation via the UI device trigger, it may insert device_id — convert to entity_id for reliability

## Related

- [[core-architecture.md|Core Architecture]] — Understanding entities and the state machine
- [[protocols.md|Protocols]] — How devices connect and communicate
