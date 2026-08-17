---
title: "Home Assistant Template Extensions"
type: concept
tags:
  - yaml-configuration
  - jinja2
  - iif
  - expand
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/yaml-template-extensions
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - yaml-templates.md
  - automation-templates-blueprints.md
  - yaml-validation.md
content_hash: sha256:85072be6f2333f7f0ea3d0891e88f66e747f6df4df235cb653ed2d8a3608617a
---
# Home Assistant Template Extensions

HA adds non-standard Jinja2 functions that general-purpose LLMs often get wrong: `iif()`, `state_translated()`, `expand()`, `area_entities()`, `integration_entities()`, `floor_areas()`, `label_entities()`, and the time helpers (`now()`, `today_at()`, `timedelta`).

## HA-Specific Template Extensions

HA adds many non-standard Jinja2 functions. These are frequently wrong in AI-generated templates:

### `iif()` — Inline if (ternary operator)
```jinja2
{{ iif(condition, if_true, if_false) }}
{{ iif(is_state('light.kitchen', 'on'), 'Kitchen is ON', 'Kitchen is OFF') }}
```

### `state_translated()` — Human-friendly state strings
```jinja2
{# Returns localized string instead of raw 'on'/'off' #}
{{ state_translated('binary_sensor.motion') }}
{# Returns "Detected" or "Clear" in user's language #}
```

### `expand()` — Expand groups/areas to entity lists
```jinja2
{# Get all entities in a group #}
{% for entity in expand('group.all_lights') %}
  {{ entity.entity_id }}: {{ entity.state }}
{% endfor %}

{# Also works with area_id #}
{% for entity in expand(area_entities('bedroom')) %}
  {{ entity.entity_id }}
{% endfor %}
```

### `area_entities()`, `area_devices()`, `area_name()`
```jinja2
{# All entity IDs in an area #}
{{ area_entities('bedroom') }}

{# Name of the area an entity belongs to #}
{{ area_name('light.kitchen_ceiling') }}
```

### `integration_entities()` — All entities from an integration
```jinja2
{# All entities from the hue integration #}
{{ integration_entities('hue') | list }}
```

### `floor_areas()`, `label_entities()` (HA 2024.4+)
```jinja2
{# All areas on a given floor #}
{{ floor_areas('ground_floor') }}

{# All entities with a specific label #}
{{ label_entities('important') }}
```

### Time helpers
```jinja2
{{ now() }}                        {# Current datetime #}
{{ today_at("07:00") }}            {# Today at 7 AM #}
{{ as_timestamp(now()) }}          {# Unix timestamp #}
{{ timedelta(hours=2) }}           {# Duration object #}
{{ (now() - states.sensor.x.last_changed).total_seconds() | int }}
```

## Related Concepts

- [[yaml-templates.md|yaml templates]]
- [[automation-templates-blueprints.md|automation templates blueprints]]
- [[yaml-validation.md|yaml validation]]
