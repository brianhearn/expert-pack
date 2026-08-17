---
title: "Reusable Jinja2 Templates"
type: concept
tags:
  - yaml-configuration
  - jinja2
  - custom-templates
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/yaml-templates
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - yaml-template-extensions.md
  - yaml-validation.md
  - automation-templates-blueprints.md
content_hash: sha256:db7bae8c78873793647aa4d5c053f59a45fdfbc96878039d1a6fe82c8863755b
---
# Reusable Jinja2 Templates

HA can load `/config/custom_templates/*.jinja` as macro libraries you import into any template. Always use `states()` not `states.domain.entity.state`, cast before comparing, and test in Developer Tools → Template.

## Reusable Jinja2 Templates

### Custom Templates Folder

Create `/config/custom_templates/` and place `.jinja` files there. These are macro libraries importable into any template in HA.

```jinja2
{# /config/custom_templates/helpers.jinja #}

{% macro format_duration(seconds) %}
  {% if seconds < 60 %}
    {{ seconds }}s
  {% elif seconds < 3600 %}
    {{ (seconds / 60) | int }}m
  {% else %}
    {{ (seconds / 3600) | round(1) }}h
  {% endif %}
{% endmacro %}

{% macro is_night() %}
  {{ now().hour >= 22 or now().hour < 6 }}
{% endmacro %}
```

Import and use in automations:
```jinja2
{% from 'helpers.jinja' import format_duration, is_night %}

{% if is_night() %}
  The {{ trigger.entity_id }} has been on for {{ format_duration(60) }}
{% endif %}
```

**The `as_function` filter** (HA 2024.4+) enables macros to return values cleanly:
```jinja2
{% macro brightness_for_time() %}
  {% if now().hour >= 22 or now().hour < 6 %}
    10
  {% elif now().hour >= 18 %}
    60
  {% else %}
    100
  {% endif %}
{% endmacro %}

{# Call it as a function #}
{{ brightness_for_time() | as_function }}
```

## Template Best Practices

### Always use `states()`, never `states.domain.entity.state`
```jinja2
{# WRONG — breaks if entity doesn't exist #}
{{ states.sensor.outdoor_temp.state }}

{# CORRECT — returns 'unknown' if entity doesn't exist #}
{{ states('sensor.outdoor_temp') }}
```

### Always cast types before comparison
States are always strings. Numeric comparison without casting silently compares strings:
```jinja2
{# WRONG — '15' > '9' is False (string comparison) #}
{{ states('sensor.temp') > 9 }}

{# CORRECT #}
{{ states('sensor.temp') | float > 9 }}
{{ states('sensor.count') | int >= 3 }}
```

### Use `has_value()` for availability checks
```jinja2
{# Check that entity exists AND has a real value (not unknown/unavailable) #}
{% if has_value('sensor.outdoor_temp') %}
  {{ states('sensor.outdoor_temp') | float }}
{% else %}
  N/A
{% endif %}
```

### Test everything in Developer Tools → Template
Before adding a template to an automation, test it live. Developer Tools → Template (text editor + result pane) gives immediate feedback with the live system state.

## Related Concepts

- [[yaml-template-extensions.md|yaml template extensions]]
- [[yaml-validation.md|yaml validation]]
- [[automation-templates-blueprints.md|automation templates blueprints]]

Sources: [Templating](https://www.home-assistant.io/docs/configuration/templating/).
