---
title: "Splitting configuration.yaml with Includes"
type: concept
tags:
  - yaml-configuration
  - include
  - splitting
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/yaml-includes
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - yaml-packages.md
  - yaml-vs-ui.md
  - yaml-secrets-env.md
content_hash: sha256:464a898574d1c23c52b9943adeb3030d1c2eb12b6f12399fa7c88553f3fb838c
---
# Splitting configuration.yaml with Includes

When `configuration.yaml` grows past a few hundred lines, split it with `!include`, `!include_dir_list`, `!include_dir_named`, `!include_dir_merge_list`, and `!include_dir_merge_named`. `!include_dir_merge_list` is the recommended pattern for hand-written automations.

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

## Related Concepts

- [[yaml-packages.md|yaml packages]]
- [[yaml-vs-ui.md|yaml vs ui]]
- [[yaml-secrets-env.md|yaml secrets env]]

Sources: [Splitting configuration](https://www.home-assistant.io/docs/configuration/splitting_configuration/).
