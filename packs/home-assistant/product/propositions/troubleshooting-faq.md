---
title: "Propositions — Troubleshooting & FAQ"
type: "proposition"
tags: [propositions, troubleshooting-faq]
pack: "home-assistant-product"
retrieval_strategy: "standard"
id: home-assistant/product/propositions/troubleshooting-faq
verified_at: '2026-04-10'
verified_by: agent
---
# Propositions — Troubleshooting & FAQ

Atomic factual statements extracted from the troubleshooting and FAQ files.

---

### diagnostic-guide.md

- Developer Tools → States shows every entity's current state and attributes — if an entity shows `unavailable`, the integration has lost connection.
- Developer Tools → Template allows live testing of Jinja2 templates against the current system state before embedding them in automations.
- Developer Tools → Events shows all events fired on the HA event bus in real time — useful for understanding what events a device generates.
- Settings → System → Repairs is HA's self-diagnostic system listing known integration issues, deprecated configurations, and required actions.
- Safe mode boots HA with no HACS custom integrations, no custom frontend resources, and no running automations — used for recovery when HA won't start.
- Entering safe mode: Settings → System → Restart → Safe Mode, or via SSH: `ha core restart --safe-mode`.
- HA log entries include the component identifier in brackets — `homeassistant.components.hue` or `custom_components.frigate` — to identify which integration is failing.
- Debug logging is enabled per-integration in `configuration.yaml` under `logger: logs:` and reloaded via Developer Tools → YAML → Reload Logger Settings.
- A corrupt recorder database (`home-assistant_v2.db`) can be recovered by stopping HA, deleting the database file, and restarting — all configuration and automations are preserved.
- Automation traces (Settings → Automations → Traces) show per-run: which trigger fired, which conditions passed/failed, template rendered values, and timing.
- The `single` automation mode silently ignores new triggers while the automation is running — a common cause of "automation doesn't fire sometimes."
- Zigbee channel conflicts with WiFi are a major source of intermittent Zigbee problems — channels 25 and 26 are the safest choices.
- Z-Wave ghost nodes (dead nodes in the Z-Wave JS node list) consume network resources and cause routing issues — remove them via "Remove Failed Node."
- Running `ha core check` or Developer Tools → YAML → Check Configuration validates the config before applying a restart.
- SQLite database performance degrades significantly above 5-10 GB; consider migrating to MariaDB for large installations (1,000+ entities, 30+ day history).
- Excluding high-frequency sensors (time, signal strength, link quality) from the recorder can reduce database writes by 30-50%.

### top-ha-mistakes.md (process gotchas)

- Using WiFi for all smart home devices leads to random dropouts, router congestion, and cloud-dependent failure when manufacturer servers shut down.
- The default `single` automation mode for motion lights causes lights to turn off mid-occupancy because new motion triggers are ignored while the delay timer runs.
- Motion-lighting automations must use `mode: restart` so each new motion event resets the off-delay timer from zero.
- Automations created via the UI device trigger picker insert opaque `device_id` references — convert to `entity_id` for stability.
- Not setting up backups on day one is the most common cause of catastrophic configuration loss when SD cards die or hardware fails.
- Running HA on an SD card long-term causes database corruption; average SD card lifespan under HA write load is 1-3 years.
- HA OS should be run on an SSD (USB-attached on Pi 4, NVMe on Pi 5 or mini-PC) — not on an SD card.
- Accepting default entity names from integrations results in unreadable IDs like `light.tradfri_bulb_e27_ws_806lm_6` — rename entities immediately on device add.
- A consistent entity naming convention is `domain.area_function` (e.g., `light.kitchen_ceiling`, `sensor.bedroom_temperature`).
- Not assigning devices to Areas blocks area-targeted automations, voice commands, and dashboard area targeting.
- Hardcoding values like motion-off delay in 15 automations instead of using an `input_number` helper creates future maintenance burden.
- Never expose port 8123 directly to the internet — brute force attacks occur constantly; use Nabu Casa, Tailscale, or a reverse proxy instead.

### common-questions.md

- The trend in HA is strongly toward UI-first configuration; as of 2024-2025, most automations can be created entirely through the UI.
- Template sensors (`template:` platform) can only be defined in YAML — this is the primary reason to use YAML over the UI.
- ZHA is the built-in Zigbee integration (simpler, less setup); Zigbee2MQTT requires a separate MQTT broker but supports more devices and has better migration tooling.
- ZHA supports approximately 3,000 devices; Zigbee2MQTT supports approximately 4,500+ devices.
- Switching between ZHA and Zigbee2MQTT requires re-pairing all Zigbee devices — do not switch without a compelling reason.
- The recommended HA update cadence is monthly, with a 3-5 day delay after release to let bug fix patches land.
- Always create a full backup before applying any HA update.
- HA entity count rarely causes performance issues; the recorder database logging high-frequency sensors is the primary cause of slowdowns.
- Excluding sensors like `sensor.time`, `sensor.*_signal_strength`, and `sensor.*_linkquality` from the recorder improves performance and reduces database size.
- HA OS is recommended over HA Container for 90% of users — it provides the full add-on ecosystem, built-in backups, and Supervisor management.
- HA Container (Docker) does not include the Supervisor or the add-on store — users must manage all supporting services (MQTT, Zigbee2MQTT) as separate containers.
- Proxmox + HA OS VM is a popular community-standard setup using the official tteck helper script for automated VM creation.
- Nabu Casa Cloud remote access ($75/year) is the easiest and safest remote access option — it uses an outbound-only tunnel with no port forwarding.
- All HA functionality works locally without a Nabu Casa subscription — it is a convenience service and project funding mechanism, not a requirement.
- In 2026, Zigbee has a larger and more mature device ecosystem than Matter; Matter adoption is recommended on a per-device basis, not as a wholesale replacement.
- Matter over Thread (mesh) is more efficient than Matter over WiFi; Thread devices are better for battery-powered sensors.
- Physical switches must always work regardless of HA state — use smart switches (not smart bulbs in dumb-switch setups) so the switch always does something.
- Automations should be invisible infrastructure that doesn't require family members to learn any UI or new habits.
