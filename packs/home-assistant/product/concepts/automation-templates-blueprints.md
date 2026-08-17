---
title: "Automation Templates, Blueprints, and Entity IDs"
type: concept
tags:
  - automation-fundamentals
  - jinja2
  - blueprints
  - entity-id
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/automation-templates-blueprints
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - automation-trigger-action.md
  - automation-conditions-actions.md
  - yaml-templates.md
content_hash: sha256:8c54ead80ffec10dffb8d68d257ca32e6d924d1544fc7a20f13caabbb9aa3668
---
# Automation Templates, Blueprints, and Entity IDs

Jinja2 templates supply dynamic values in automations; blueprints are community-shared automations you configure with inputs. Always target `entity_id` (`light.kitchen_ceiling`), not opaque `device_id` hashes that change when you re-pair.

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

## Related Concepts

- [[automation-trigger-action.md|automation trigger action]]
- [[automation-conditions-actions.md|automation conditions actions]]
- [[yaml-templates.md|yaml templates]]

Sources: [Automation templating](https://www.home-assistant.io/docs/automation/templating/).
