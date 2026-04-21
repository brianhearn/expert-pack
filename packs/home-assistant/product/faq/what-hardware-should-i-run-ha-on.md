---
title: What Hardware Should I Run Home Assistant On?
type: faq
tags:
- backup-migration
- faq
- hardware-selection
- network-architecture
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/faq/what-hardware-should-i-run-ha-on
verified_at: "2026-04-21"
verified_by: agent
schema_version: "4.1"
concept_scope: single
---
<!-- context: section=faq, topic=hardware-selection, related=backup-migration,network-architecture -->

# What Hardware Should I Run Home Assistant On?

> **Lead summary:** For most new builds in 2025-2026, an **Intel N100 mini-PC** ($130-180) is the sweet spot — it offers 4-8x the performance of a Raspberry Pi 4, runs HA OS natively, has a built-in SSD slot (no SD card problems), and is whisper-quiet. Raspberry Pi 5 with a USB SSD is the alternative for those in the Pi ecosystem. Whatever you choose: **use an SSD, not an SD card** — SD cards fail within 6-18 months under HA's constant write load.

## The Short Answer

| Hardware | Cost | Best For |
|----------|------|----------|
| **Intel N100 mini-PC** | $130-180 | Most users — best value in 2025-2026 |
| **Raspberry Pi 5 (4GB) + USB SSD** | ~$120 | Clean new Pi-based builds |
| **HA Green (official)** | ~$100 | Plug-and-play official hardware |
| **Used mini-PC (Intel N-series)** | $80-150 | Budget performance |
| **Proxmox VM on existing server** | $0 | Running HA alongside other services |

## Why N100 Mini-PC is the Community Recommendation

- **Performance:** Intel N100 handles Frigate (NVR with AI object detection), many add-ons, and large automations without breaking a sweat. Raspberry Pi 4 struggles with Frigate + full add-on stack.
- **Storage:** Built-in M.2 or 2.5" SATA slot — no external SSD needed, no SD card issues.
- **Quiet:** Fanless or near-silent at HA's idle power draw.
- **Price:** $130-180 new (or $80-120 used) buys significantly more headroom than a Pi 4.
- **Architecture:** x86_64 — all HA features, add-ons, and Docker images are fully supported.

**Recommended N100 models:** Beelink EQ12, Trigkey G4, MINISFORUM UM350.

## Why You Should Avoid SD Cards

Home Assistant writes to its SQLite database every time any entity changes state. This can be thousands of writes per hour. SD cards are rated for 3,000-10,000 write cycles per cell — under HA's load, they fail in 6-18 months.

**Signs of a dying SD card:**
- HA dashboard takes 30+ seconds to load after reboot
- I/O errors in the logs: `EXT4-fs error`, `Buffer I/O error`
- HA gets stuck on "Preparing Home Assistant" at startup
- Filesystem corruption after power outages

**The fix:** Run HA from a USB-attached SSD (on Pi 4) or from an internal SSD (on mini-PC or Pi 5 with NVMe HAT).

**Pi 4 USB boot setup:**
1. Update bootloader: `sudo rpi-eeprom-update -a` (boot from SD card first)
2. Change boot order: `sudo raspi-config` → Advanced → Boot Order → USB first
3. Flash HA OS to USB SSD using Balena Etcher
4. Remove SD card, boot from SSD

## Raspberry Pi 5 — Still a Good Choice

The Pi 5 is approximately 3x faster than Pi 4 for single-core workloads. It supports:
- NVMe SSDs via the official M.2 HAT (~$12)
- USB boot (no bootloader change needed, unlike Pi 4)
- Better thermal management

Still slower than an N100 mini-PC for Frigate ML inference, but handles everything else well.

## Official HA Hardware (HA Green / HA Yellow)

- **HA Green (~$100):** Compact, officially supported, eMMC storage (no SD card). Good plug-and-play option. Lower ceiling than N100 for heavy workloads.
- **HA Yellow (~$130 board):** Requires a Raspberry Pi CM4 module (sold separately). Has built-in Zigbee/Matter coordinator (ZBT-1 chip). Solid for Zigbee-heavy setups.

## Proxmox VM — For Those Running Other Services

If you want to run HA alongside a NAS, media server, or other services on the same hardware:

1. Install Proxmox on an x86 machine
2. Create HA OS VM using the tteck community helper script
3. Pass through USB Zigbee/Z-Wave coordinator to the VM
4. Allocate 2+ cores and 4+ GB RAM to HA

USB passthrough in Proxmox: VM → Hardware → Add → USB Device → select coordinator by vendor:product ID.

→ See [[backup-migration.md]] for migration details and hardware upgrade paths
