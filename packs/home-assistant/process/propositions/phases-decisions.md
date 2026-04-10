---
title: "Propositions — Process Phases & Decisions"
type: "proposition"
tags: [phases-decisions, propositions]
pack: "home-assistant-process"
retrieval_strategy: "standard"
id: home-assistant/process/propositions/phases-decisions
verified_at: '2026-04-10'
verified_by: agent
---
# Propositions — Process Phases & Decisions

Atomic factual statements extracted from the process phases and decision files.

---

### process/overview.md

- Building a smart home with Home Assistant is a multi-phase journey from bare hardware to a fully automated, reliable home environment.
- A basic HA install with 10-20 devices takes 1-2 weekends; full home coverage and dashboard takes 1-3 months.
- The seven phases build on each other — skipping ahead undermines the foundation the next phase needs.
- Phase 1 (Planning): hardware selection, installation method, network design — 1-3 days.
- Phase 2 (Initial Setup): install HA, first integrations, companion app — 1 weekend.
- Phase 3 (Protocol Setup): Zigbee/Z-Wave coordinator, first devices — 1-2 weeks.
- Phase 4 (Automation Building): first automations, templates, testing — 2-4 weeks.
- Phase 5 (Dashboard Design): Lovelace dashboards, mobile optimization — 1-2 weeks.
- Phase 6 (Advanced Features): voice assistant, energy monitoring, presence detection — 2-4 weeks.
- Phase 7 (Hardening): backups, security, remote access, monitoring — 1 weekend plus ongoing.
- The short version of common gotchas: use HA OS, put it on an SSD not an SD card, set up Zigbee2MQTT early, automate backups on day one.

### phases/01-planning.md

- The three decisions to make before spending money are: which hardware to run HA on, which installation method to use, and how to structure your network.
- The best hardware choice for most new builds is a Raspberry Pi 5 with a 128GB+ USB SSD, or a used Intel N100 mini-PC.
- Raspberry Pi 3 and SD card storage should both be avoided for HA production use.
- The Raspberry Pi 4/5 can boot from USB SSD by updating the bootloader and changing boot order in raspi-config.
- HA OS is the recommended installation method for most users — it provides full add-on support, Supervisor management, and automatic OS updates.
- The HA server should have a static IP assigned via DHCP reservation for reliable access and integration config.
- The HA server should be placed on a UPS (uninterruptible power supply) — power blips cause SD card corruption and HA crashes.
- The USB Zigbee coordinator should be physically near the HA server.
- For security-conscious setups, IoT devices go on VLAN 10 with no internet access; HA server goes on the trusted VLAN.
- Zigbee and Z-Wave devices connect directly to the coordinator (USB dongle) and never touch the IP WiFi network.
- The recommended Zigbee coordinator for new builds is the SMLIGHT SLZB-07 or Sonoff Zigbee 3.0 Dongle Plus-P.

### decisions/protocol-selection.md

- Zigbee is the best starting protocol for most users: local-only, low-power mesh, massive device ecosystem, excellent HA support.
- Zigbee devices typically cost $7-25 each; Z-Wave devices typically cost $30-70 each (2-3x more expensive).
- Z-Wave's key advantage is its 868/912 MHz sub-GHz frequency — no 2.4 GHz congestion, better wall penetration than Zigbee.
- Z-Wave certification is stricter than Zigbee, leading to generally more reliable and better-tested devices.
- WiFi IoT devices should be reserved for high-bandwidth needs (cameras, smart displays) and devices that don't exist in Zigbee/Z-Wave.
- ESPHome (custom ESP32 sensors) is excellent for DIY projects; standard off-the-shelf WiFi devices scale poorly and are typically cloud-dependent.
- Thread/Matter device selection is still smaller than Zigbee in 2026; Zigbee remains more mature and battle-tested.
- The recommended multi-protocol approach: lead with Zigbee, add ESPHome for DIY sensors, use Z-Wave for locks and garage doors, adopt Thread/Matter opportunistically.
- The Nortek HUSBZB-1 ($65) supports both Zigbee and Z-Wave on a single USB stick.
- The Aeotec Z-Stick Gen7 ($55) is the recommended Z-Wave coordinator for US installations.

### decisions/hardware-selection.md (inferred from phases/01-planning.md)

- Intel N100 mini-PCs (~$80-150 used) offer the best price/performance ratio for dedicated HA hardware in 2025-2026.
- NUC or similar Intel small form factor machines ($150-300) are suitable for power users with heavy add-on load (Frigate, many integrations).
- A Synology NAS with Docker can run HA Container; however, no add-on support is available without HA Supervised.
- Proxmox on existing server hardware allows HA to coexist with other services as a VM at no additional hardware cost.

### decisions/installation-method.md (inferred from overview and planning)

- HA OS provides full add-on support, Supervisor, automatic updates, and one-click backup restore.
- HA Supervised requires a strictly maintained Debian environment and is described as "for advanced users."
- HA Container is appropriate only for users who explicitly want to manage all supporting services as Docker containers.
- HA Core (Python venv) is for developers and advanced users only — no add-ons, no Supervisor.

### gotchas/common-mistakes.md

- SD card storage causes database corruption; average failure timeline under HA write load is 6-18 months.
- Using a USB 2.0 extension cable (20-30 cm) to separate the Zigbee dongle from USB 3.0 ports eliminates a major source of Zigbee reliability problems.
- Zigbee2MQTT channel 25 or 26 minimizes interference with WiFi channels 1, 6, and 11.
- Editing `configuration.yaml` without first validating via Settings → System → Check Configuration can leave HA unable to restart.
- `unavailable` is a valid HA state — automations trigger on unavailable→on transitions unless explicitly excluded with `not_from: [unavailable, unknown]`.
- Presence detection based solely on phone GPS fires welcome-home automations 30-90 seconds late and has false departures when GPS is lost indoors.
- Port-forwarding port 8123 directly to the internet exposes HA to constant brute-force attacks; use Nabu Casa, Cloudflare Tunnel, or Tailscale instead.
- Buying Z-Wave devices when Zigbee was sufficient costs 2-3x more without meaningful reliability improvement for most device types.
- Hardcoding motion-off delay values in multiple automations should be replaced with `input_number` helpers configurable from the dashboard.
