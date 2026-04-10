---
title: "Propositions — Product Concepts"
type: "proposition"
tags: [concepts, propositions]
pack: "home-assistant-product"
retrieval_strategy: "standard"
id: home-assistant/product/propositions/concepts
verified_at: '2026-04-10'
verified_by: agent
---
# Propositions — Product Concepts

Atomic factual statements extracted from the product concepts files.

---

### core-architecture.md

- Home Assistant is fundamentally a state machine that tracks the current state of every entity and reacts when states change.
- The core hierarchy is: Integration → Device → Entity → State → Attributes.
- An integration is a software bridge connecting HA to external hardware, cloud services, protocols, or platforms.
- Over 2,000 official integrations exist for Home Assistant as of 2026.
- A device is a logical grouping of related entities; one physical device typically creates one HA device with multiple entities.
- An entity is the atomic unit of HA — it represents one measurable or controllable thing.
- Every entity has an entity ID in the format `domain.name` (e.g., `light.living_room`, `sensor.outdoor_temp`).
- Entity states are always stored as strings internally, even when they represent numbers.
- The entity ID is permanent once created; renaming it requires care because automations reference it by ID.
- Areas are optional organizational groupings for devices and entities by physical location (room, floor, zone).
- Services (also called Actions) are the verbs of HA — the things you can ask entities to do.
- HA OS (Home Assistant Operating System) is the recommended installation method for most users.
- HA OS provides full add-on support and Supervisor management; HA Container does not.
- HA Container is a Docker-only install without the Supervisor or add-on store.
- HA Supervised runs the full HA stack (with Supervisor and add-ons) on an existing Debian Linux machine.
- When an entity state changes, a `state_changed` event fires and all matching automation triggers evaluate.

### automation-fundamentals.md

- Every HA automation has three parts: triggers (when), conditions (only if), and actions (then do).
- Multiple triggers in one automation use OR logic — any one of them fires the automation.
- Conditions use AND logic by default — all conditions must be true for the automation to proceed.
- A trigger fires the automation; a condition gates whether it continues — if a condition fails, the automation stops silently.
- The `for` parameter on a trigger requires an entity to remain in a state for a specified duration before the trigger fires.
- The default automation mode is `single` — new triggers are ignored while the automation is already running.
- Motion-activated lights must use `restart` mode so new motion events reset the off-delay timer.
- The `restart` automation mode stops the current run and starts fresh when triggered again.
- HA uses Jinja2 templates for dynamic values in automations, scripts, and sensors.
- Entity states are always strings in templates — use `| float`, `| int`, or `| bool` to cast before numeric comparisons.
- `states('entity_id')` returns `'unknown'` if the entity doesn't exist; `states.domain.entity.state` breaks if the entity is missing.
- Blueprints are pre-made automations from the community that require only configuration inputs, not YAML writing.
- Always use entity_id in automations, not device_id — entity IDs are human-readable and stable; device IDs are opaque hashes.
- Automation traces (Settings → Automations → Traces) show exactly which trigger fired, which conditions passed/failed, and which actions ran.

### protocols.md

- For most Home Assistant users in 2025-2026, Zigbee is the best default protocol — local-only, low-power mesh, massive device selection, proven reliability.
- Zigbee operates at 2.4 GHz and supports mesh networking where mains-powered devices relay messages for battery devices.
- Z-Wave operates at 868/912 MHz (sub-GHz), avoiding 2.4 GHz congestion from WiFi — this is its key advantage over Zigbee.
- WiFi IoT devices are often cloud-dependent and do not scale well beyond 50 devices due to router capacity limits.
- Thread is a 2.4 GHz IPv6 mesh protocol; Matter is an application-layer standard that runs over Thread, WiFi, or Ethernet.
- In 2025-2026, Matter device selection is still limited compared to Zigbee and Z-Wave; adoption is recommended cautiously.
- ESPHome is the recommended approach for DIY sensors — ESP32 microcontrollers programmed via YAML, connecting directly to HA via a native local API.
- Mains-powered Zigbee/Z-Wave devices act as mesh routers; battery-powered devices are end devices that do not relay messages.
- A Zigbee/Z-Wave coordinator USB dongle should be moved away from USB 3.0 ports using a USB 2.0 extension cable to avoid 2.4 GHz RF interference.
- Zigbee channels 25 and 26 have the least overlap with WiFi channels 1, 6, and 11 and are recommended for Zigbee deployments.
- ZHA (Zigbee Home Automation) is the built-in HA Zigbee integration; Zigbee2MQTT is a more powerful alternative requiring a separate MQTT broker.
- ZHA supports approximately 2,000-3,000 devices; Zigbee2MQTT supports approximately 3,500+ devices.
- Most good HA setups use 2-3 protocols simultaneously (e.g., Zigbee + ESPHome + selective WiFi).

### yaml-configuration.md

- Most HA users can accomplish 90% of setup through the UI; YAML is reserved for template sensors, complex automations, packages, and secrets management.
- The `configuration.yaml` file is HA's main config file; integrations added via UI are stored in `.storage/` (JSON), not in this file.
- `!include` includes a single YAML file; `!include_dir_merge_list` merges all YAML files in a directory into one list (recommended for automations).
- Packages bundle all YAML for one feature (automations, sensors, helpers) into a single file under `homeassistant: packages:`.
- `secrets.yaml` stores sensitive values (API keys, passwords) referenced with `!secret key_name`; it does not encrypt them.
- YAML does not allow tabs for indentation — use spaces only; tabs cause cryptic startup errors.
- `'on'` and `'off'` must be quoted in YAML; unquoted, they are parsed as boolean `true`/`false` by the YAML parser.
- Running `ha core check` or using Developer Tools → YAML → Check Configuration validates the config before a restart.
- The `state_class: total_increasing` attribute is required for cumulative sensor entities used in the Energy Dashboard.
- HA adds non-standard Jinja2 functions including `iif()`, `expand()`, `area_entities()`, `label_entities()`, and time helpers like `today_at()`.
- Always use `states('entity_id')` rather than `states.domain.entity.state` — the former safely returns `'unknown'` if the entity is missing.

### integrations-guide.md

- Every official HA integration has an IoT class that describes how it communicates: Local Push, Local Poll, Cloud Push, or Cloud Poll.
- Local Push integrations are the most reliable — the device pushes state updates instantly to HA without polling, no internet required.
- Cloud Poll integrations depend on the manufacturer's server and stop working if the manufacturer shuts down the API (e.g., Tuya 2023, Wemo).
- The integration quality scale rates integrations Platinum, Gold, Silver, or Bronze; Platinum Local Push integrations are the most reliable.
- HACS (Home Assistant Community Store) provides custom integrations and frontend cards not in the official HA integration library.
- HACS custom integrations run with the same privileges as HA itself — full access to configuration, devices, and potentially the network.
- Frontend HACS cards (Mushroom, mini-graph-card) are lower risk than HACS custom integrations.
- Most integrations support reloading without a full HA restart (Settings → Devices & Services → Integration → Reload).
- HA releases on the first Wednesday of each month; always read the release notes before updating for breaking changes.
- Zigbee2MQTT and ZHA are the two main ways to run Zigbee in HA; ZHA is built-in and simpler, Z2MQTT supports more devices.
- MQTT (Mosquitto broker add-on) is the universal protocol bridge — it connects Tasmota devices, Zigbee2MQTT, DIY sensors, and more.
- The Frigate NVR integration provides local AI-based object detection for cameras (people, cars, packages) and integrates with HA for notifications.

### dashboard-design.md

- Sections layout (default since HA 2024.4) is the recommended dashboard layout — it's responsive and adapts from mobile to desktop.
- Masonry layout is legacy; it causes cards to shift unpredictably across screen sizes and is not recommended for new dashboards.
- The majority of HA daily use is on phones — design dashboards for 375px wide screens first.
- Mushroom Cards are the most widely-used HACS custom card set (2 million+ active installs) and provide a clean, mobile-first visual language.
- The `mushroom-chips-card` creates a compact status bar of small indicator chips showing multiple entity states at once.
- `button-card` is the most flexible custom card — fully template-driven with custom styles, colors, and text — but has a steeper learning curve than Mushroom.
- Conditional cards show or hide based on entity state — use them to build adaptive dashboards without cluttering the view.
- Tap action, hold action, and double-tap action are configurable per card; common pattern is tap=toggle, hold=more-info.
- The "Useful in 3 Seconds" rule: any household member should understand status and take action within 3 seconds of viewing a dashboard.
- Build purpose-specific dashboards (Overview, Room, Security, Energy) rather than one giant dashboard with all entities.
- Never add every entity to a dashboard — 200 entities on one view is unusable; be ruthless about only showing actionable information.

### esphome-fundamentals.md

- ESPHome is a framework that generates C++ firmware for ESP microcontrollers from YAML configuration files — no C++ knowledge needed.
- ESP32 microcontroller dev boards cost $5-12; sensors cost $2-20; total ESPHome sensor cost is $10-35 vs $50-150 for commercial equivalents.
- ESPHome devices connect to Home Assistant via an encrypted native API — fully local, zero cloud dependency, instant state updates.
- The ESP32 should always be chosen over the ESP8266 for new projects — it has Bluetooth, more RAM, more GPIO pins, and better hardware encryption.
- ESPHome is maintained by Nabu Casa (the Home Assistant company) and ships as an official add-on in HA OS.
- The first flash of an ESPHome device requires a USB cable; all subsequent updates are over-the-air (OTA).
- The LD2410 mmWave sensor detects micro-motion including breathing and stillness, making it immune to the "sitting still" false negative of PIR sensors.
- The SCD41 CO2 sensor costs $20-30 and is the gold standard for DIY air quality monitoring; commercial CO2 monitors with HA integration cost $100+.
- BLE proxy (enabling `bluetooth_proxy` in ESPHome) turns any ESP32 into a Bluetooth antenna, extending HA's BLE device range throughout the home.
- ESPHome devices auto-discover in HA via mDNS — accepting the integration creates entities for all sensors/switches defined in the YAML config.
- Entity IDs for ESPHome follow the pattern: `domain.device_name_entity_name`.
- Use `disabled_by_default: true` in ESPHome component YAML to keep diagnostic entities from cluttering HA until explicitly enabled.

### network-architecture.md

- IoT devices should be placed on a separate VLAN with no internet access (or heavily filtered access) to isolate security threats.
- Home Assistant lives on the trusted network and bridges to the IoT VLAN — it does NOT live on the IoT VLAN itself.
- mDNS (Multicast DNS) does not cross VLAN boundaries by default — devices on an IoT VLAN cannot be auto-discovered by HA without an mDNS reflector.
- UniFi routers have a built-in mDNS reflector; pfSense/OPNsense requires the Avahi package for cross-VLAN mDNS.
- Every IoT device should have a DHCP reservation (static DHCP lease by MAC address) so its IP never changes.
- DNS-based blocking (Pi-hole, AdGuard Home) on the IoT VLAN blocks telemetry and manufacturer call-home domains.
- Some IoT devices have hardcoded DNS servers (like 8.8.8.8) — use a firewall DNS interception rule to force all DNS through the sinkhole.
- Zigbee and Z-Wave are NOT on the IP network — they are separate RF mesh networks; VLANs do not affect them at all.
- USB 3.0 ports emit RF interference in the 2.4 GHz band — always use a USB 2.0 extension cable (1-2 meters) to move the Zigbee coordinator away.
- Nabu Casa Cloud remote access is the safest remote access option — it uses an outbound-only tunnel; no inbound ports are opened.
- Never port-forward port 8123 directly to the internet — brute force attacks occur constantly on this port and there is no defense in depth.
- Tailscale is a zero-config VPN (WireGuard-based) that requires no port forwarding and provides safe remote access to HA.
- Zigbee channel 26 (2480 MHz) provides the best interference avoidance from WiFi channels 1/6/11.
- Cameras should be on a dedicated VLAN (separate from general IoT) due to their high bandwidth (1-4 Mbps per camera continuously).

### backup-migration.md

- A full HA backup includes: all YAML configuration, add-ons and their data, the recorder database, HACS custom integrations, and SSH keys.
- HA backup files are `.tar` archives containing `.tar.gz` archives that can be manually extracted to recover config files.
- Moving the same USB coordinator stick to new hardware requires zero Zigbee device repairing — the mesh is stored in the coordinator hardware.
- SD cards have a typical lifespan of 1-3 years under HA's constant write load; symptoms include slow UI, I/O errors in logs, and HA failing to start.
- USB-connected SSDs have far higher write endurance than SD cards (150-600 TBW rated vs 3,000-10,000 write cycles per cell for SD).
- Raspberry Pi 4 can boot from USB SSD by updating the bootloader and changing boot order — the SD card slot can then be left empty.
- Intel N100 mini-PCs (~$130-180) offer 4-8x single-core performance vs Raspberry Pi 4 at similar cost and are the community sweet spot for dedicated HA hardware.
- HA backup/restore to new hardware takes under 30 minutes and transfers all configuration, integrations, add-ons, and Zigbee mesh data.
- The Google Drive Backup HACS add-on automatically uploads backups to Google Drive with configurable retention.
- If the recorder database (`home-assistant_v2.db`) corrupts, deleting it and restarting HA creates a fresh empty database; automations and configuration are unaffected.
- The only useful backup test is actually restoring the backup — verify it works on spare hardware or a VM before a real emergency.
- Proxmox + HA OS VM is a popular and well-supported setup for running HA alongside other services on the same hardware.

### presence-detection.md

- Presence detection is the single most impactful capability in home automation and the one most systems get wrong.
- Phone-only tracking fails for roughly 40% of households due to Android battery optimization, iOS background refresh limits, GPS drift, and non-technical family members.
- Android battery optimization must be disabled for the HA Companion app (set to "Unrestricted") on Samsung, Xiaomi, Huawei, and OnePlus devices.
- iOS background refresh limits cause delayed presence updates of up to 30 minutes — "person leaves at 7:15 AM" may not appear in HA until 7:45 AM.
- The winning presence strategy is multi-sensor fusion: phone GPS + WiFi router tracking + BLE proximity + mmWave radar + door sensors combined.
- MAC randomization (iOS 14+, Android 10+) breaks WiFi-based device tracking unless the HA Companion app is configured to report a consistent identifier.
- The Bayesian binary sensor combines multiple uncertain presence signals into a probability-based verdict using Bayes' theorem.
- The `delay_off` attribute on template binary sensors prevents false "away" flips from brief signal gaps (e.g., phone briefly drops WiFi).
- mmWave sensors detect micro-motion including breathing, making them immune to the "sitting still" false negative that defeats PIR sensors.
- ESPresense is a purpose-built ESP32 firmware for BLE room-level presence detection, tracking specific devices per room.
- The Aqara FP2 mmWave sensor supports up to 5 detection zones and connects via WiFi/HomeKit/HA integration.
- The Sonoff SNZB-06P is the budget mmWave option ($12-15, Zigbee) providing reliable binary occupied/clear detection.
- The Apollo Automation MSR-1 and AIR-1 sensors run ESPHome natively and expose all LD2410 parameters directly in HA.
- Solve home-level presence (is anyone home?) before adding room-level presence (which room is Brian in?).

### voice-assistant.md

- Home Assistant Assist is HA's built-in voice assistant — fully local, no subscriptions, no cloud required.
- The Assist pipeline is modular: Wake Word → STT (speech-to-text) → Intent Recognition → TTS (text-to-speech) → response.
- Each pipeline stage is independently configurable — you can mix local and cloud components per stage.
- The Wyoming protocol is HA's open standard for connecting voice processing services (STT, TTS, wake word) to HA via local network streaming.
- Faster Whisper is the standard local STT engine for HA in 2026 — it runs OpenAI's Whisper model 4x faster using CTranslate2.
- On a Raspberry Pi 4, only the `tiny` Whisper model is practical (3-8 second latency); an Intel N100 handles the `small` model (1-3 second latency).
- Piper is the standard local TTS engine for HA — it produces high-quality speech in real-time even on CPU hardware.
- OpenWakeWord is the primary local wake word engine; it detects words like "Hey Jarvis", "Hey Nabu", and "Alexa" locally on CPU.
- MicroWakeWord runs on the ESP32-S3 itself — wake word detection happens on the satellite device, so audio only leaves the device after wake word detection.
- Only expose entities you actually want to control by voice — each query sends the full exposed entity list to the intent engine or LLM.
- Entity naming for voice control: use `[Area] + [Descriptor] + [Domain]` format (e.g., "Kitchen ceiling light", "Living room floor lamp").
- Aliases on entities let Assist recognize alternative names ("TV", "telly", "the TV" for the same entity).
- All devices must be assigned to Areas for area-targeted voice commands to work ("turn off the bedroom lights").
- The ESP32-S3-BOX-3 (~$50) is the officially recommended voice satellite — it has a dual-mic array, speaker, and screen with maintained firmware.
- In 2026, Assist does not support multi-turn conversation — each command is stateless.

### energy-management.md

- The HA Energy Dashboard tracks grid consumption, solar production, return-to-grid, battery storage, gas, water, and individual device usage.
- The Energy Dashboard requires sensors reporting cumulative energy in kWh with `state_class: total_increasing` — not instantaneous power in watts.
- Power (watts) measures the rate of consumption right now; energy (kWh) measures total consumption over time — the dashboard needs energy sensors.
- `state_class: total_increasing` tells HA the sensor is a cumulative counter; HA handles resets to zero (device reboots) without data loss.
- The Riemann sum `integration` platform converts a power sensor (W) to a cumulative energy sensor (kWh) using trapezoidal or left/right integration.
- The `trapezoidal` Riemann sum method is most accurate for loads that ramp up and down (HVAC, EV charger).
- Long-term energy statistics persist in the HA database independently of state history and survive database purges.
- The `utility_meter` integration creates cycle-based consumption tracking (daily/monthly/yearly) from a cumulative sensor with optional tariff support.
- Energy data is only captured from the time sensors are configured — retroactive import is only possible for specific integrations (e.g., SolarEdge).
- The Shelly EM clamp-style energy monitor is the recommended solution for 240V high-draw circuits (HVAC, EV charger) — do not use smart plugs for these.
- Excluding high-frequency raw power sensors from the recorder (`entity_globs: sensor.*_power_w`) reduces database growth by 30-50%.
- Forecast.Solar provides free solar production forecasts using panel tilt, azimuth, and total wattage; Solcast is more accurate using satellite weather data.
