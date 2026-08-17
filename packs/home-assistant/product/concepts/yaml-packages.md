---
title: "YAML Packages"
type: concept
tags:
  - yaml-configuration
  - packages
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/yaml-packages
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - yaml-includes.md
  - yaml-vs-ui.md
  - yaml-templates.md
content_hash: sha256:6e40176297800c1b6354da5bb69423a698ee421ebd6aa308d192ca6a3cdea2dc
---
# YAML Packages

A package bundles all YAML for one feature — automations, sensors, helpers, scripts — into a single file. Add or remove a feature by adding or removing one file. Enable with `homeassistant.packages: !include_dir_named packages/`.

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

## Related Concepts

- [[yaml-includes.md|yaml includes]]
- [[yaml-vs-ui.md|yaml vs ui]]
- [[yaml-templates.md|yaml templates]]

Sources: [Packages](https://www.home-assistant.io/docs/configuration/packages/).
