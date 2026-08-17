---
title: "YAML Gotchas and Config Validation"
type: concept
tags:
  - yaml-configuration
  - validation
  - ha-core-check
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/yaml-validation
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - yaml-vs-ui.md
  - yaml-templates.md
  - yaml-secrets-env.md
content_hash: sha256:03140372464de6349610dc76d42f613cd7957f800e9d11f69b6b198056bce651
---
# YAML Gotchas and Config Validation

The most common YAML bugs in HA are unquoted `on`/`off` (parsed as booleans), tabs, silent duplicate keys, and mixed indentation. Always run `ha core check` or Developer Tools → Check Configuration before restarting — a bad `configuration.yaml` means HA will not start.

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

## Related Concepts

- [[yaml-vs-ui.md|yaml vs ui]]
- [[yaml-templates.md|yaml templates]]
- [[yaml-secrets-env.md|yaml secrets env]]
