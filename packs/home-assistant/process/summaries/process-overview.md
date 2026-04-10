---
title: Summary — Process Pack Overview
type: summary
tags:
- process-overview
- summaries
pack: home-assistant-process
retrieval_strategy: standard
id: home-assistant/process/summaries/process-overview
verified_at: '2026-04-10'
verified_by: agent
---
# Summary — Process Pack Overview

This summary covers the 7-phase smart home build process and key decision frameworks. For detailed guidance, follow the links to source files.

---

## The Seven-Phase Journey

Building a smart home with Home Assistant takes 3-6 months to do well. Each phase creates the foundation for the next.

| Phase | Goal | Time |
|-------|------|------|
| [[01-planning.md|1. Planning]] | Hardware, install method, network design | 1-3 days |
| [[02-initial-setup.md|2. Initial Setup]] | Flash HA, first integrations, companion app | 1 weekend |
| [[03-protocol-setup.md|3. Protocol Setup]] | Zigbee/Z-Wave coordinator, pair first devices | 1-2 weeks |
| [[04-automation-building.md|4. Automation Building]] | First automations, templates, testing | 2-4 weeks |
| [[05-dashboard-design.md|5. Dashboard Design]] | Lovelace dashboards, mobile optimization | 1-2 weeks |
| [[06-advanced-features.md|6. Advanced Features]] | Voice, energy monitoring, presence detection | 2-4 weeks |
| [[07-hardening.md|7. Hardening]] | Backups, security, remote access | 1 weekend + ongoing |

→ Source: [[overview.md|process overview]]

---

## Key Decisions Before You Buy Hardware

Three decisions shape everything downstream. Make these first:

**1. Hardware:** Raspberry Pi 5 + USB SSD (~$120) or used Intel N100 mini-PC ($80-150). Avoid Pi 3, avoid SD card storage. A UPS is strongly recommended.

**2. Installation method:** HA OS for most users (full add-on support, Supervisor, built-in backups). HA Container only if you're a Docker power user who doesn't need add-ons. Never expose port 8123 to the internet.

**3. Protocol:** Lead with Zigbee (local, cheap, mature, massive device selection). Add ESPHome for DIY sensors. Use Z-Wave for locks and thick walls. Adopt Thread/Matter opportunistically.

→ Source: [[protocol-selection.md|decisions/protocol-selection.md]] | [[01-planning.md|phases/01-planning.md]]

---

## Common Gotchas (Read Before Starting)

The mistakes that cost people the most time:

- **SD card:** Don't run HA on an SD card. They fail within 6-18 months. Use an SSD.
- **WiFi overload:** Don't buy 40 WiFi devices. Use Zigbee for sensors/plugs/bulbs; WiFi only for cameras.
- **USB 3.0 interference:** Use a USB 2.0 extension cable (20-30 cm) to move the Zigbee dongle away from USB 3.0 ports.
- **Motion lights mode:** Set `mode: restart` on motion-lighting automations. The default `single` mode ignores new motion events while the timer runs.
- **No backups:** Set up Google Drive Backup or Samba Backup on day one. You will need it.
- **YAML without validation:** Always run Settings → System → Check Configuration before restarting after YAML edits.
- **Port 8123 exposed:** Never port-forward 8123 to the internet. Use Nabu Casa, Tailscale, or Cloudflare Tunnel.
- **Naming:** Rename every entity when you add a device. `light.kitchen_ceiling` is useful; `light.0x00158d0003` is not.

→ Source: [[common-mistakes.md|gotchas/common-mistakes.md]]

---

## Proven Automation Patterns

These patterns work well across thousands of HA installations:

- **[[motion-lighting.md|Motion Lighting]]:** `mode: restart` + 5-minute off-delay. Triggers on motion sensor, turns on light, waits for clear, turns off after delay.
- **[[climate-control.md|Climate Control]]:** Presence-based HVAC — heat/cool only when home, use setback when away. Use generic thermostat with temperature sensor + switch.
- **[[security-monitoring.md|Security Monitoring]]:** Door/window contact sensors + cameras + Frigate object detection + push notifications. Keep cameras on dedicated VLAN.
- **[[notification-patterns.md|Notification Patterns]]:** HA Companion app push notifications with actionable buttons. Alert only for things that require action.

---

## What Makes a Smart Home Actually Work for Families

The technical system is only half the challenge. The other half is family acceptance:

- Automations should be invisible — lights that turn on/off without anyone pressing anything.
- Physical switches must always work regardless of HA state.
- Start small — prove one automation works reliably before expanding.
- Use presence-based automations (HVAC, security) as the highest ROI starting point.
- Don't require family members to open an app for daily tasks.

→ Source: [[common-mistakes.md|process/faq and gotchas]]
