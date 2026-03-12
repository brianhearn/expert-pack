---
title: "Zigbee2MQTT 2.0 Migration: What Broke and How to Fix It"
description: Comprehensive community-sourced guide to Z2M 1.x → 2.0 migration gotchas and fixes.
mined: 2026-03-12
sources:
  - https://github.com/Koenkk/zigbee2mqtt/discussions/24198
  - https://www.reddit.com/r/homeassistant/comments/1hu5h8s/
  - https://github.com/Koenkk/zigbee2mqtt/issues/25461
  - https://community.home-assistant.io/t/action-entity-missing-for-zigbee-switches-zigbee2mqtt/630468
---

# Zigbee2MQTT 2.0 Migration Guide

> Zigbee2MQTT 2.0.0 was released January 2025. It contains significant breaking changes for HA users.
> This guide covers the most common post-migration failures and fixes.

---

## Pre-Migration Checklist

Add these to your Z2M `configuration.yaml` **before** updating, to minimize breakage:

```yaml
advanced:
  homeassistant_legacy_entity_attributes: false
  homeassistant_legacy_triggers: false
  legacy_api: false
  legacy_availability_payload: false
device_options:
  legacy: false
# Explicitly set your adapter type to avoid "No valid USB adapter found":
serial:
  adapter: ezsp        # for SiLabs (Nabu Casa Yellow, SkyConnect, ZBT-1)
  # adapter: zstack    # for TI CC2652 (Sonoff Zigbee 3.0 Dongle Plus)
  # adapter: deconz    # for ConBee/RaspBee
```

Source: [Z2M Discussion #24198](https://github.com/Koenkk/zigbee2mqtt/discussions/24198), Jan 2025.

---

## Breaking Change #1: Action Sensor Entities Disabled

**Symptom:** Button/remote automations stop working. `sensor.devicename_action` is missing or unavailable.

**Cause:** In Z2M 2.0, `sensor.*_action` entities are **disabled by default**. They still exist but are disabled in HA.

**Fix Option A (quick):** Re-enable in Z2M config:
```yaml
homeassistant:
  legacy_action_sensor: true
```
Then restart Z2M.

**Fix Option B (recommended):** Migrate to MQTT device triggers:
1. In HA, go to automations that use `sensor.X_action`
2. Replace state trigger on the sensor with a Device trigger (select device → action → button press type)
3. This is more reliable and won't break again in future Z2M updates

---

## Breaking Change #2: `sensor.*_click` Entities Removed

**Symptom:** Automations using `sensor.devicename_click` fail with "entity not found."

**Cause:** `*_click` entities are **removed entirely** (not just disabled). There is no legacy flag.

**Fix:** Must migrate to MQTT device triggers. No workaround exists to restore `_click` entities.

---

## Breaking Change #3: MQTT Status Topic Changed

**Symptom:** After HA restart, all Z2M devices go "unavailable" even though Z2M is running.

**Cause:** Z2M 2.0 changed default status topic from `hass/status` to `homeassistant/status`. HA may still be configured for the old topic.

**Fix:**
1. HA → Settings → Devices & Services → MQTT → Configure → Re-configure MQTT → Next
2. Ensure "Birth message topic" is `homeassistant/status`
3. Restart HA

---

## Breaking Change #4: `illuminance_lux` → `illuminance`

**Symptom:** Templates/automations referencing `sensor.X_illuminance_lux` break. Entity shows as "unknown."

**Cause:** Dozens of devices (Aqara, IKEA, Philips, Tuya, and others) had `illuminance_lux` renamed to `illuminance`. The `lux` value now requires enabling a separate option in Z2M 2.1.0+.

**Fix:** Find and replace `_illuminance_lux` with `_illuminance` in your automations and templates. Use Developer Tools → Template editor to test.

---

## Breaking Change #5: Entity Attributes Removed

**Symptom:** `{{ states.sensor.X.attributes.Y }}` returns empty/error for Z2M devices.

**Cause:** Z2M no longer exposes device data as HA entity attributes. Each value is now a separate entity.

**Fix:** Find the corresponding standalone entity (e.g., `sensor.X_battery`, `sensor.X_voltage`) and use `states('sensor.X_voltage')` in templates.

---

## Breaking Change #6: Child Lock Now `switch` Not `lock`

**Symptom:** Automations targeting `lock.*_child_lock` break.

**Cause:** All child lock entities changed from `lock` domain to `switch` domain.

**Fix:** Replace `lock.X_child_lock` with `switch.X_child_lock` in automations.

---

## Breaking Change #7: USB Adapter Discovery Fails

**Symptom:** Z2M fails to start with "USB adapter discovery error (No valid USB adapter found)."

**Cause:** Z2M 2.0 improved adapter discovery but changed which adapters are auto-detected. Some adapters (especially older ones) need explicit configuration.

**Fix:** Add to `configuration.yaml`:
```yaml
serial:
  adapter: ezsp    # or zstack, deconz, zigate, ember — see Z2M docs for your device
  port: /dev/ttyUSB0   # your USB port
```

---

## Breaking Change #8: External Converters and Extensions Moved

**Symptom:** Custom converters not loading after Z2M 2.0 update.

**Cause:**
- External converters: moved from `external_converters:` config key → auto-loaded from `data/external_converters/` directory
- External extensions: moved from `data/extension/` → `data/external_extensions/`

**Fix:**
1. Move files to the new directories
2. Remove `external_converters:` from `configuration.yaml`

---

## Bare-Metal / Git Install Special Steps

If you run Z2M from Git (not Docker/add-on):

```bash
# Before updating:
git checkout data/configuration.example.yaml
cp data/configuration.yaml data/configuration.yaml.bak

# Switch from npm to pnpm:
npm install -g pnpm

# Update:
git pull --no-rebase
pnpm install

# If missing files error:
pnpm run clean
# then restart Z2M
```

---

## Verification After Migration

1. Check Z2M logs for errors (`zigbee2mqtt/add-on logs` or `data/log/`)
2. Open HA Developer Tools → States → filter for your device names — check entity names changed
3. Test each button/remote manually and verify device triggers fire
4. Check HA → Settings → Devices → your Z2M devices → verify expected entities are there
5. Run one automation manually with trace to verify trigger paths work

---

## Related

- [Community Gotchas](../troubleshooting/common-mistakes/community-gotchas.md) — All Z2M gotchas in one place
- [Protocol Selection](../../process/decisions/protocol-selection.md) — ZHA vs Z2M decision
- [Zigbee Concepts](../concepts/protocols.md) — Zigbee protocol fundamentals
