---
title: Community-Sourced Gotchas and Practitioner Knowledge
type: gotcha
tags: [gotcha, community, practitioner-knowledge, home-assistant-product, troubleshooting]
pack: home-assistant-product
retrieval_strategy: atomic
description: High-EK gotchas extracted from r/homeassistant, community.home-assistant.io, and GitHub issues. These are real-world surprises that contradict docs or aren't mentioned in official guides.
mined: 2026-03-12
sources:
  - https://github.com/Koenkk/zigbee2mqtt/discussions/24198
  - https://community.home-assistant.io/t/psa-2024-7-recorder-problems/746428
  - https://github.com/hacs/integration/issues/4314
  - https://www.reddit.com/r/homeassistant/comments/1hu5h8s/
  - https://github.com/home-assistant/core/issues/130582
  - https://news.ycombinator.com/item?id=42813513
  - https://www.xda-developers.com/things-wish-knew-before-going-all-in-home-assistant/
  - https://edvoncken.net/2025/01/reduce-homeassistant-database/
id: home-assistant/product/troubleshooting/common-mistakes/community-gotchas
verified_at: '2026-04-10'
verified_by: agent
---
# Community-Sourced Gotchas and Practitioner Knowledge

> These are things that tripped up real users and are NOT obvious from docs.

---

## Zigbee / Zigbee2MQTT

- **Zigbee2MQTT 2.0 (Jan 2025): `sensor.*_action` entities disabled by default.** After upgrading from Z2M 1.x to 2.0, all your button/remote automations that used `sensor.devicename_action` will silently break — the sensor entities are disabled, not deleted. The new approach is MQTT device triggers. To restore old behavior: add `homeassistant: { legacy_action_sensor: true }` to your Z2M `configuration.yaml`. Source: [GitHub Z2M Discussion #24198](https://github.com/Koenkk/zigbee2mqtt/discussions/24198), Jan 2025.

- **Zigbee2MQTT 2.0: `sensor.*_click` entities removed entirely** (not just disabled). Any automation using `*_click` entities must be rewritten to use MQTT device triggers. This is not backward-compatible — there is no legacy flag for `_click`. Source: [Z2M #24198](https://github.com/Koenkk/zigbee2mqtt/discussions/24198), Jan 2025.

- **Zigbee2MQTT 2.0: Status topic changed from `hass/status` to `homeassistant/status`.** If you upgraded Z2M 1.x → 2.0 and your devices go unavailable after HA restart, the MQTT birth topic mismatch is likely the cause. Fix: In HA → Settings → Devices & Services → MQTT → Configure → Re-configure MQTT → Next: ensure Birth message topic is `homeassistant/status`. Source: [Z2M #24198](https://github.com/Koenkk/zigbee2mqtt/discussions/24198), Jan 2025.

- **Zigbee2MQTT 2.0: `illuminance_lux` entity renamed to `illuminance`.** This affects dozens of Aqara, IKEA, Philips Hue, Tuya, and other devices. Any automation or template referencing `sensor.X_illuminance_lux` will break silently (entity becomes unknown). Must manually update entity names. Source: [Z2M #24198](https://github.com/Koenkk/zigbee2mqtt/discussions/24198), Jan 2025.

- **Zigbee2MQTT 2.0: entity attributes removed from device state.** Z2M used to expose rich attributes on entities (e.g. `states.binary_sensor.my_sensor.attributes`). These are gone in 2.0. Any template or automation using `entity.attributes` from a Z2M device must be rewritten to use separate entities. Source: [Z2M #24198](https://github.com/Koenkk/zigbee2mqtt/discussions/24198), Jan 2025.

- **Zigbee2MQTT 2.0: external converters no longer use `external_converters:` in config.** They auto-load from `data/external_converters/` directory. Also, extensions load from `data/external_extensions/` (previously `data/extension/`). Bare-metal Git installs must rename directories manually. Source: [Z2M #24198](https://github.com/Koenkk/zigbee2mqtt/discussions/24198), Jan 2025.

- **Zigbee2MQTT 2.0: bare-metal Git installs use `pnpm` not `npm`.** Running the old `npm install` after `git pull` will fail. Must first run `npm install -g pnpm` then re-run your update script. Source: [Z2M #24198](https://github.com/Koenkk/zigbee2mqtt/discussions/24198), Jan 2025.

- **ZHA + Aqara devices drop off SiLabs coordinators (Yellow/SkyConnect/ZBT-1) but work on TI CC2652 (Sonoff 3.0).** The SiLabs-based coordinators do NOT auto-update firmware. You must manually flash the latest coordinator firmware to get Aqara Zigbee devices to pair and stay connected. Sonoff Zigbee 3.0 USB Dongle Plus (TI CC2652) is unaffected. Fix: manually upgrade Nabu Casa Yellow/ZBT-1/SkyConnect firmware via the HA OS add-on. Source: [community.home-assistant.io](https://community.home-assistant.io/t/aqara-zha-zbt-1-fails-aqara-zha-sonoff-works-fix-how-to-upgrade-nabu-casa-yellow-zbt1-skyconnect-zigbee-firmware-for-aqara/844159), Feb 2025.

- **ZHA has worse Zigbee device compatibility than Zigbee2MQTT.** ZHA commonly drops Aqara and other "picky" Zigbee devices; Z2M handles them fine. Community consensus: if a device reports disconnects or "unavailable" with ZHA, try Z2M first before debugging hardware. Migrating from ZHA to Z2M requires re-pairing all devices (the mesh does not transfer). Source: [XDA Developers](https://www.xda-developers.com/things-wish-knew-before-going-all-in-home-assistant/), Aug 2025; [Reddit r/homeassistant](https://www.reddit.com/r/homeassistant/comments/1fpdp25/).

---

## HACS (Home Assistant Community Store)

- **HACS broke on HA 2025.1.0 due to deprecated `config_flow` API.** After upgrading to 2025.1, HACS fails to start with: `custom integration 'hacs' sets option flow config_entry explicitly, which is deprecated`. Workaround: update HACS to 2.0.x first, OR update HA after HACS update. Source: [GitHub hacs/integration #4314](https://github.com/hacs/integration/issues/4314), Jan 2025.

- **HACS 2.0.1 failed to set up after 2025.1 upgrade** with error `The repo id for music-assistant/hass-music-assistant is already set`. Fix: delete HACS data file and restart, or re-download custom integrations via HACS → 3-dot menu → Re-download. Source: [GitHub hacs/integration #4325](https://github.com/hacs/integration/issues/4325), Jan 2025.

- **After HA 2025.x update, HACS integrations show "unavailable update" status even when up-to-date.** Fix: go to HACS menu → select each integration → 3-dot menu → Re-download. Source: [Reddit r/homeassistant](https://www.reddit.com/r/homeassistant/comments/1hxbihz/hacs_is_inconsistent_since_updating_to_2025/), Jan 2025.

- **HACS disappears from sidebar after HA restart (without any HA update).** Fix: Settings → Devices & Services → HACS → Configure → enable "AppDaemon apps discovery & tracking" → save. HACS reappears immediately. Source: [Reddit r/homeassistant](https://www.reddit.com/r/homeassistant/comments/1htm6kq/hacs_broke_not_sure_how_to_fix_this/), Jan 2025.

- **Every HA update risks breaking HACS custom integrations.** HACS integrations are not tested by the HA team and use internal APIs that can change without notice. Real-world pattern: HACS integrations break 2–4 times per year, often requiring a version hold or manual patch. Mitigation: take a snapshot before every HA update; keep HACS integrations to a minimum. Source: [Reddit r/homeassistant](https://www.reddit.com/r/homeassistant/comments/1i61v5c/how_to_deal_with_breaking_integrations_on_every_update/), Jan 2025.

---

## Recorder / Database

- **HA 2024.7 recorder bug: after purge, recorder stops writing to DB until HA restarts.** Affects installations with old legacy foreign keys in the `states` table (common when upgrading from very old HA versions or with certain HACS integrations). Fix: upgrade to 2024.7.2 (patched) or 2024.8.1+ if disk space ran out during table rebuild. Source: [community.home-assistant.io PSA: 2024.7 recorder problems](https://community.home-assistant.io/t/psa-2024-7-recorder-problems/746428), July 2024.

- **Recorder database grows to 7GB+ without any configuration.** By default, HA records every state change for every entity. High-frequency entities (radar presence sensors, IKEA sensors, BLE distance) can produce millions of records. Fix: use SQLite Web add-on to run `SELECT m.entity_id, COUNT(*) as count FROM states AS S INNER JOIN states_meta AS M ON M.metadata_id = s.metadata_id GROUP BY m.entity_id ORDER BY count DESC LIMIT 20;` — exclude top offenders in `recorder:` config. Source: [edvoncken.net](https://edvoncken.net/2025/01/reduce-homeassistant-database/), Jan 2025.

- **`recorder: commit_interval: 10` (default is 5) reduces SD card wear** by flushing to disk less often. On systems with hundreds of entities, the default 5-second interval causes many unnecessary writes. Increasing to 10–30 is safe for most setups. Source: [edvoncken.net](https://edvoncken.net/2025/01/reduce-homeassistant-database/), Jan 2025.

- **Recorder Purge + Repack must be manually triggered after adding exclude rules.** Adding `exclude:` to `recorder:` only stops NEW data. Old high-frequency data stays until you call `Recorder: Purge` action with `repack: true` and `apply_filter: true` in Developer Tools → Actions. Source: [edvoncken.net](https://edvoncken.net/2025/01/reduce-homeassistant-database/), Jan 2025.

---

## Z-Wave JS

- **Z-Wave devices go "unavailable" after updating Z-Wave JS add-on.** Confirmed bug pattern across multiple Z-Wave JS versions (13.3.1, 2025.3.4, UI 4.7.0). Fix: re-interview each device one by one (slow but effective). Reverting to previous add-on backup does NOT fix it — the issue is in the node state cache. Source: [GitHub home-assistant/core #126235](https://github.com/home-assistant/core/issues/126235), Sep 2024; [community.home-assistant.io](https://community.home-assistant.io/t/devices-become-unavailable-after-every-z-wave-js-update/882601), Apr 2025.

- **Z-Wave devices disappeared entirely after HA 2025.3.4 upgrade.** Only one device remained registered. Affects SiLabs 700/800 series USB sticks running firmware 7.21.5. Not directly caused by the Z-Wave JS add-on update but by the HA core update itself. Source: [community.home-assistant.io](https://community.home-assistant.io/t/z-wave-devices-have-disappeared-after-update-to-ha-2025-3-4/868880), Mar 2025.

---

## YAML / Automation Breaking Changes

- **HA 2024.8: `service:` renamed to `action:` in YAML automations.** Old `service:` key still works (backward compatible) but causes automations to show as "Unknown" in the GUI and require YAML editing. If your automations display as "Unknown" after 2024.8, the fix is replacing `service:` with `action:` in `automations.yaml`. Source: [Reddit r/homeassistant](https://www.reddit.com/r/homeassistant/comments/1f1t06z/), Aug 2024.

- **HA 2024.10: automation YAML syntax changed plural keys.** `trigger:` became `triggers:`, `condition:` became `conditions:`, `action:` became `actions:` (plural). Old singular forms still work but the UI generates the new plural forms. Mixing old and new in the same file is valid YAML but confusing. Source: [home-assistant.io blog 2024.10](https://www.home-assistant.io/blog/2024/10/02/release-202410/), Oct 2024.

- **HA 2025.11: Person entity state changed for custom zones.** `person` entity state now uses the zone's friendly name instead of object ID when companion app sends zone-only data. Any automation triggering on `person.X = 'zone_object_id'` breaks silently. Source: [home-assistant.io blog 2025.11](https://rc.home-assistant.io/blog/2025/10/02/release-202511/), Oct 2025.

---

## Companion App / Notifications

- **iOS standard notifications delayed ~10 seconds; critical notifications are instant.** Confirmed bug in HA 2024.11.1 with iOS 18.1. Affects WiFi and cellular. Workaround: use `push: { sound: { name: default, critical: 1, volume: 1.0 } }` in your notification data to make time-sensitive alerts critical. Source: [GitHub home-assistant/core #130582](https://github.com/home-assistant/core/issues/130582), Nov 2024.

- **iOS critical notifications require explicit `push.sound` YAML block**, not just `data: { push: { sound: default } }`. The full required structure is:
  ```yaml
  data:
    push:
      sound:
        name: default
        critical: 1
        volume: 1.0
  ```
  Omitting the nested structure silently sends a non-critical notification with no delay override. Source: [Reddit r/homeassistant](https://www.reddit.com/r/homeassistant/comments/1huziju/making_a_notification_to_an_ios_device_come/), Jan 2025.

- **`notify.mobile_app_<device>` action doesn't exist until HA restarts after first companion app setup.** Installing the app and granting permissions is not enough — HA must be restarted before the notify action appears in Developer Tools. Source: [companion.home-assistant.io troubleshooting](https://companion.home-assistant.io/docs/troubleshooting/faqs/).

---

## Tuya / LocalTuya

- **LocalTuya breaks on HA 2024.12.5 with traceback in `config_entries.py`.** All Tuya WiFi sockets become unreachable. Caused by API changes in HA core that LocalTuya (HACS) hadn't caught up to. Fix: wait for LocalTuya update, or temporarily downgrade HA. Source: [community.home-assistant.io](https://community.home-assistant.io/t/tuya-local-broke-with-update-core-2024-12-5-supervisor-2024-12-0-operating-system-14-1-frontend-20241127-8/814415), Dec 2024.

- **Tuya (cloud) integration loses control ~once/day and requires integration restart.** Error codes 104 / -999999 in logs. Workaround: create an automation to restart the Tuya integration on a schedule (e.g., daily at 3 AM) using `homeassistant.reload_config_entry`. LocalTuya is more reliable for local devices. Source: [community.home-assistant.io](https://community.home-assistant.io/t/tuya-integration-issues-network-errors-104-999999-localtuya/820361), Jan 2025.

- **LocalTuya goes "unavailable" for 7 minutes once or twice daily.** This is a known issue where Tuya's local protocol performs periodic cloud token refresh checks. Devices with IoT firewall rules blocking Tuya cloud traffic are most affected. Source: [community.home-assistant.io](https://community.home-assistant.io/t/local-tuya-smart-plug-goes-unavailable-for-7min-once-or-twice-a-day/490519).

---

## Matter / Thread

- **Matter device pairing via HA Companion App fails if Thread credentials aren't synced.** Fix: Settings → Companion App → Troubleshooting → tap "Sync Thread Credentials" twice. Second sync should say "Home Assistant and this device use the same network." Source: [Reddit r/homeassistant](https://www.reddit.com/r/homeassistant/comments/1dis8hc/help_unable_to_add_matter_devices/), June 2024.

- **Matter in HA Docker Container requires host networking for mDNS.** Without `network_mode: host`, Matter (and most mDNS-dependent integrations like Cast, HomeKit, Sonos) fail to discover devices. Even with host networking, users frequently report issues. Community consensus: run HAOS in a VM instead of Docker Container for reliable mDNS. Source: [XDA Developers](https://www.xda-developers.com/things-wish-knew-before-going-all-in-home-assistant/), Aug 2025.

---

## Installation / Installation Method Gotchas

- **HA Container (Docker) cannot use official add-ons.** Official add-ons (ESPHome, Zigbee2MQTT, MQTT Broker, Whisper, Piper, etc.) require the Supervisor (HAOS or Supervised). Container users must manually run equivalent Docker containers and link them. This is non-obvious from the docs and surprises many first-time installers. Source: [XDA Developers](https://www.xda-developers.com/things-wish-knew-before-going-all-in-home-assistant/), Aug 2025.

- **HA Container + mDNS: services discovered via Bonjour/mDNS don't work unless host networking is enabled.** Cast, HomeKit, DLNA, Sonos, and other mDNS-dependent integrations require `network_mode: host` in Docker compose. Many integrations silently fail to discover devices without this. Source: [XDA Developers](https://www.xda-developers.com/things-wish-knew-before-going-all-in-home-assistant/), Aug 2025.

- **HA OS running in Proxmox VM: the VM should get its own IP from DHCP.** Do NOT run HA in a container on Proxmox for a production install — run it in a VM with bridged networking so it appears as its own node on your LAN. This fixes mDNS, Bluetooth dongles via USB passthrough, and many other integration issues. Source: [XDA Developers](https://www.xda-developers.com/things-wish-knew-before-going-all-in-home-assistant/), Aug 2025.

---

## Template / Entity Gotchas

- **Template sensors defined in YAML cannot be assigned to a device** (the `device_id:` property is not available in `configuration.yaml` template sensors as of 2025). To associate a template sensor with a device, you must use the UI-based template editor, which supports device association. Source: [community.home-assistant.io](https://community.home-assistant.io/t/how-can-you-associate-a-template-sensor-with-an-existing-device/918795), Aug 2025.

- **Template sensors without `unique_id:` cannot be customized in the UI** and their entity_id can change on reload/restart if another entity with the same name gets created. Always add `unique_id:` to template sensors to stabilize their entity_id. Source: [community.home-assistant.io](https://community.home-assistant.io/t/unique-id-for-template-sensor/596594), Jul 2023.

---

## General Practitioner Tips (from power users)

- **Add automations.yaml to git.** This is the most-recommended advanced practice on Reddit and HN. Every breaking HA update is more manageable when you can `git diff` your config before and after. Source: [Hacker News](https://news.ycombinator.com/item?id=42813513), Jan 2025.

- **Use Automation Traces for debugging.** The trace viewer (top-right of the automation editor) shows exactly what happened at every step, what variables changed, and where it failed. It's the #1 debugging tool for automation issues and is underused by beginners. Source: [XDA Developers](https://www.xda-developers.com/things-wish-knew-before-going-all-in-home-assistant/), Aug 2025.

- **Don't buy products that require cloud to function.** Cloud integrations (Tuya cloud, Chamberlain/MyQ, Mazda, etc.) can be revoked by the vendor at any time with zero notice. HA has had multiple integrations forcibly removed due to vendor C&D. Check the integration's "class" (Local Push, Local Polling, Cloud Push, etc.) on the HA integrations page before buying. Source: [Hacker News](https://news.ycombinator.com/item?id=42813513), Jan 2025.

- **50+ IoT WiFi devices cause issues on some Unifi U7 series APs.** Community reports of degraded WiFi stability with Unifi U7 series when running 50+ IoT devices. Workaround: use a dedicated VLAN/SSID for IoT devices on a different AP or consider switching high-density IoT to Zigbee/Thread. Source: [Hacker News](https://news.ycombinator.com/item?id=42813513), Jan 2025.

- **Smart bulbs + smart switches conflict: smart switches physically cut power to smart bulbs, breaking them.** To use both, set smart switches to "detached mode" (supported by Shelly, Inovelli, Zooz) — the switch sends a Z-Wave/Zigbee command to HA instead of cutting power. OR use Matter/Thread bindings (Inovelli + Nanoleaf Thread) to bind switches to bulbs at the protocol level, keeping control even when HA is offline. Source: [Hacker News](https://news.ycombinator.com/item?id=42813513), Jan 2025.
