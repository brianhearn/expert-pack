---
title: YAML Configuration — The Definitive Practitioner Guide
type: concept
tags:
- automation-fundamentals
- concepts
- core-architecture
- yaml-configuration
pack: home-assistant-product
retrieval_strategy: standard
---
<!-- context: section=concepts, topic=yaml-configuration, related=core-architecture,automation-fundamentals -->
---
sources:
  - type: documentation
    url: "https://www.home-assistant.io/docs/configuration/"
    date: "2026-03"
  - type: documentation
    url: "https://www.home-assistant.io/docs/configuration/splitting_configuration/"
    date: "2026-03"
  - type: documentation
    url: "https://www.home-assistant.io/docs/configuration/packages/"
    date: "2026-03"
  - type: documentation
    url: "https://www.home-assistant.io/docs/configuration/templating/"
    date: "2026-03"
  - type: community
    url: "https://community.home-assistant.io/t/configuration-yaml-best-practices/350080"
    date: "2025-11"
---

# YAML Configuration — The Definitive Practitioner Guide

> **Lead summary:** Most HA users today can accomplish 90% of their setup through the UI. But YAML remains essential for: template sensors, complex automations, packages, secrets management, and anything the UI can't express. The pitfall is learning YAML the hard way (cryptic startup errors). This guide covers when to use YAML vs UI, the include system for splitting large configs, the packages pattern for feature-based organization, and the Jinja2 template system — including HA's non-standard template extensions that LLMs often get wrong.

## When to Use YAML vs UI

The UI has improved dramatically since HA's early days. Use the UI for:
- Adding integrations (Settings → Devices & Services)
- Creating standard automations (80% of automation needs)
- Creating scripts
- Creating scenes
- Dashboard configuration

Reserve YAML for:
- **Template sensors** — `template:` platform sensors derived from other entity states
- **`input_*` helpers** if you want them in packages (you can also do these in UI)
- **Complex automations** that hit the UI's limits (nested choose, complex templates)
- **Packages** — organizing related config into feature files
- **Integrations that require YAML** (some older integrations, `command_line`, etc.)
- **Customizations** (friendly names, icons for edge cases)

**The golden rule:** If the UI can do it, use the UI. Drop to YAML only when you need to. Mixing UI and YAML is fine — HA handles both simultaneously.

## The `configuration.yaml` Structure

The main config file. For a new HA OS install, it starts nearly empty. Every integration you add via UI is stored in `.storage/` (JSON), NOT in `configuration.yaml`. What goes in `configuration.yaml`:

```yaml
# Standard configuration.yaml sections
homeassistant:
  name: "My Home"
  latitude: 30.4518
  longitude: -84.2807
  elevation: 57
  unit_system: imperial
  time_zone: "America/New_York"
  currency: USD
  country: US

# HTTP settings (rarely needed unless customizing)
http:
  # ip_ban_enabled: true
  # login_attempts_threshold: 5

# The recorder — controls what's stored in the database
recorder:
  purge_keep_days: 14
  exclude:
    entities:
      - sensor.time        # High-frequency, low-value
      - sensor.date
    domains:
      - weather             # Don't record weather history

# Logbook — which entity changes show in history view
logbook:
  exclude:
    entities:
      - sensor.time

# History — what shows in the History graph
history:

# Template sensors/binary sensors
template:
  - sensor:
      - name: "Kitchen Temperature Rounded"
        state: "{{ states('sensor.kitchen_temp') | float | round(1) }}"

# Automations loaded from file(s)
automation: !include automations.yaml
# Or split: automation: !include_dir_merge_list automations/

# Scripts
script: !include scripts.yaml

# Scenes
scene: !include scenes.yaml
```

**Note:** The `automation:`, `script:`, and `scene:` keys in `configuration.yaml` coexist with UI-created automations/scripts/scenes. UI-created ones live in `.storage/`. YAML-defined ones in `configuration.yaml` (or includes) are separate and identified by their `id:` field.

## Splitting Configuration with Includes

When `configuration.yaml` becomes unwieldy (500+ lines), split it. HA provides several include directives:

### `!include` — Single file
```yaml
# In configuration.yaml:
sensor: !include sensors.yaml

# In sensors.yaml:
- platform: template
  sensors:
    my_sensor:
      value_template: "{{ ... }}"
```

### `!include_dir_list` — All YAML files in a directory as a list
```yaml
# Each file in the sensors/ directory becomes a list item
sensor: !include_dir_list sensors/
```
Files must contain a single item or list. Good for sensors, switches — things that are sequences.

### `!include_dir_named` — Files as a dictionary, keyed by filename
```yaml
# Each filename becomes a key, file content becomes the value
group: !include_dir_named groups/
```
Each file contains the content for one group. The key is the filename (without `.yaml`).

### `!include_dir_merge_list` — Merge all files into one list
```yaml
# Combines all YAML list files in automations/ into one list
automation: !include_dir_merge_list automations/
```
Each file can be a list of automations. All are merged. **This is the recommended pattern for automations.**

### `!include_dir_merge_named` — Merge all files into one dict
```yaml
# Merges all key:value yaml files into one dict
script: !include_dir_merge_named scripts/
```

### Practical split structure for a mature HA install:
```
config/
├── configuration.yaml       # Minimal top-level file
├── automations.yaml         # UI-managed (don't hand-edit)
├── scripts.yaml             # UI-managed
├── scenes.yaml              # UI-managed
├── automations/             # Hand-written automations
│   ├── presence.yaml
│   ├── lighting.yaml
│   └── climate.yaml
├── templates/               # Template sensors/binary sensors
│   ├── presence.yaml
│   └── derived_sensors.yaml
├── packages/                # Feature-based bundles (see below)
│   ├── motion_lighting.yaml
│   └── security.yaml
└── secrets.yaml             # API keys, passwords
```

## Packages — The Best Practice for Feature Organization

Packages are the most underutilized feature of HA YAML configuration. A package bundles ALL the YAML for one "feature" — automations, sensors, input booleans, scripts — into a single file. This keeps related things together instead of scattered across automation.yaml, sensors.yaml, etc.

```yaml
# In configuration.yaml:
homeassistant:
  packages: !include_dir_named packages/
```

```yaml
# packages/guest_mode.yaml — Everything for "guest mode" in one file
# Package name: guest_mode (the filename)

input_boolean:
  guest_mode:
    name: "Guest Mode"
    icon: mdi:account-multiple

automation:
  - alias: "Guest Mode — Turn on when guests arrive"
    id: "guest_mode_auto_on"
    trigger:
      - trigger: state
        entity_id: binary_sensor.guest_bedroom_mmwave
        to: "on"
        for: "00:10:00"
    action:
      - action: input_boolean.turn_on
        target:
          entity_id: input_boolean.guest_mode

  - alias: "Guest Mode — Turn off 24h after last motion"
    id: "guest_mode_auto_off"
    trigger:
      - trigger: state
        entity_id: binary_sensor.guest_bedroom_mmwave
        to: "off"
        for: "24:00:00"
    action:
      - action: input_boolean.turn_off
        target:
          entity_id: input_boolean.guest_mode

template:
  - binary_sensor:
      - name: "Guest Room Occupied"
        device_class: occupancy
        state: "{{ is_state('input_boolean.guest_mode', 'on') }}"
```

**Why packages are powerful:**
- Feature-complete: add or remove an entire feature by adding/removing one file
- Clear ownership: the automation and its supporting entities live together
- Easier code review: a collaborator can review one package file
- Portable: copy a package file to a new HA instance and it works

**Package limitation:** You cannot use the same top-level key twice. If two packages both define `input_boolean:`, HA merges them (deduplicated by key). But if both define `sensor: platform: template`, each needs a unique list structure. Use the `template:` syntax (under `homeassistant:`) not the old `sensor: platform: template` style.

## secrets.yaml

Store sensitive values (API keys, passwords, coordinates) here instead of inline in `configuration.yaml`:

```yaml
# secrets.yaml
google_api_key: "AIzaSyBXXXXXXXXXXXXXXXXXXXX"
mqtt_password: "super-secret-password"
latitude: 30.4518
longitude: -84.2807
home_alarm_code: "1234"
```

Reference in `configuration.yaml`:
```yaml
homeassistant:
  latitude: !secret latitude
  longitude: !secret longitude
```

**What secrets.yaml does NOT do:** It doesn't encrypt values. The file is plaintext. Its purpose is to prevent secrets appearing in code/version control, not to encrypt them. If you use git for your config, ensure `secrets.yaml` is in `.gitignore`.

**Debug mode gotcha:** When running `ha core check` or checking config, secret values are masked in output. This is intentional.

## Common YAML Gotchas

These mistakes cause silent failures or startup errors:

### 1. Tabs vs Spaces
YAML does not allow tabs for indentation. Use spaces only. Most text editors can convert, but copy-pasting from websites often introduces tabs. `ha core check` will report a "while scanning..." error if tabs exist.

### 2. Boolean Quoting — `'on'` and `'off'` MUST be quoted
```yaml
# WRONG — YAML parses 'on' and 'off' as booleans true/false
state: on     # YAML sees: true
to_state: off # YAML sees: false

# CORRECT — quote boolean-like strings
state: "on"
to_state: "off"
```
This is the most common YAML bug in HA. `state: on` becomes `state: True` and the condition never matches `"on"`.

Also quote: `yes`, `no`, `true`, `false`, `null`, `~`

### 3. Duplicate Keys — Last Value Wins Silently
```yaml
# WRONG — duplicate 'name' key
light:
  name: Kitchen
  name: Living Room  # This silently overwrites 'Kitchen'
```
YAML parsers accept duplicate keys and take the last value. HA will not warn you. This is especially problematic when merging includes.

### 4. Indentation Inconsistency
```yaml
# WRONG — mixing 2-space and 4-space indentation
sensor:
  - platform: template
      sensors:          # 6-space indent here breaks parsing
        my_sensor: ...
```
Pick 2 spaces (most common) or 4 spaces and be consistent. The HA config editor enforces this.

### 5. Case Sensitivity
Entity IDs, service names, and configuration keys are case-sensitive. `Light.Kitchen_Ceiling` ≠ `light.kitchen_ceiling`. Domain names are always lowercase.

### 6. String vs Number
```yaml
# 'value_template' expects a string expression
value_template: "{{ states('sensor.temp') | float }}"

# But template result for numeric sensors should be a number, not a string
# Use 'state_class: measurement' and 'unit_of_measurement' to hint the type
```

## The `!env_var` Directive (HA Core Only)

Available in HA Core (Python venv) installs only — NOT in HA OS/Supervised. Reads environment variables:

```yaml
# configuration.yaml (Core install only)
http:
  server_host: !env_var SERVER_HOST "0.0.0.0"
  server_port: !env_var SERVER_PORT 8123
```

This enables Docker/container deployments to inject values without editing YAML files. Not applicable to most HA OS users.

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

## Config Validation Workflow

**Always validate before restarting.** A bad `configuration.yaml` means HA won't start.

```bash
# In HA OS terminal / SSH:
ha core check

# If using the File Editor or Studio Code Server add-on, use their built-in check
# In the UI: Developer Tools → YAML → Check Configuration
```

Workflow:
1. Make YAML edits
2. `ha core check` (or Developer Tools → Check Configuration)
3. If OK → `ha core restart` (or restart from UI)
4. If error → read the error message carefully, it includes the file and line number
5. Fix the error → repeat from step 2

**Safe restart vs full restart:**
- `ha core restart` — restarts the HA Core (most changes)
- `ha homeassistant restart` — equivalent via CLI
- **Some changes don't require restart:** Template sensor changes, dashboard changes, most UI-managed things. Use "reload" where available (Developer Tools → YAML → Reload All YAML / specific sections).

## Related

- [[core-architecture.md|Core Architecture]] — Entities, devices, integrations model
- [[automation-fundamentals.md|Automation Fundamentals]] — Templates in automations
- [[diagnostic-guide.md|Troubleshooting]] — Debugging config errors
