---
title: "YAML vs UI Configuration"
type: concept
tags:
  - yaml-configuration
  - configuration-yaml
  - ui
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/yaml-vs-ui
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - yaml-includes.md
  - yaml-packages.md
  - yaml-validation.md
content_hash: sha256:5231a892d86a9a8555f9b4a7085e7da568c9537fc8f5025de6382e5128a9ae0e
---
# YAML vs UI Configuration

Most HA users can do 90% of setup in the UI. Reserve YAML for template sensors, packages, secrets, integrations that still require it, and automations that hit the UI's limits. Mixing UI and YAML is fine — UI items live in `.storage/`, YAML items in `configuration.yaml` and includes.

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

## Related Concepts

- [[yaml-includes.md|yaml includes]]
- [[yaml-packages.md|yaml packages]]
- [[yaml-validation.md|yaml validation]]

Sources: [HA configuration](https://www.home-assistant.io/docs/configuration/).
