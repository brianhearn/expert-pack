---
title: "The SD Card Problem"
type: concept
tags:
  - backup-migration
  - sd-card
  - ssd
  - raspberry-pi
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/backup-sd-card
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - backup-hardware-migration.md
  - backup-automated.md
  - core-services-install.md
content_hash: sha256:890e953d04b755026de24f71ef87fb518184b875d95e5733cfc38027023e0dbb
---
# The SD Card Problem

SD cards are the single biggest reliability issue for Raspberry Pi HA installs. Constant recorder writes exhaust NAND in 1–3 years. Move to USB SSD (or eMMC/NVMe) early — do not wait for I/O errors.

## The SD Card Problem

SD cards are the single biggest reliability issue for Raspberry Pi-based HA installations.

### Why SD Cards Fail

SD cards use NAND flash memory that has a limited write endurance — typically 3,000 to 10,000 write cycles per cell. Home Assistant writes constantly: the recorder database logs state changes (potentially thousands per hour), logs rotate, temporary files are written.

**Average HA SD card lifespan in real-world usage: 1-3 years.** After that, cells begin to fail.

### Signs Your SD Card Is Dying

- **Slow UI:** Dashboard takes 30+ seconds to load, especially after a fresh reboot
- **I/O errors in logs:** `read-only file system`, `EXT4-fs error`, `Buffer I/O error on dev`
- **Automations stopping mid-run:** Unexplained failures in traces
- **HA can't start cleanly:** Gets stuck on "Preparing Home Assistant" indefinitely
- **Filesystem corruption:** After a power outage that would normally be fine

By the time you see these symptoms, the card is already in the failure window. Don't wait — migrate immediately.

### Prevention: Move to SSD

A USB-connected SSD has two key advantages over SD cards:
1. **Higher write endurance:** TLC SSDs are rated for 150-600 TBW (terabytes written). At HA's write rate, that's 50+ years.
2. **Better error correction:** SSDs handle write failures more gracefully.

**Recommended SSDs for HA (2025-2026):**
- Samsung T7 or Crucial X6 (external USB SSD, ~$40-60) — plug into Pi USB 3.0 port
- Any 2.5" SATA SSD in a USB 3.0 enclosure ($20 SSD + $10 enclosure)
- For Pi 5: NVMe HAT is available, much faster than USB

**Boot from USB SSD on Pi 4:**
1. Update Pi OS bootloader: `sudo rpi-eeprom-update -a` on Pi OS (boot Pi from SD card first)
2. Change boot order to USB first: `sudo raspi-config` → Advanced → Boot Order → USB first
3. Flash HA OS to SSD using Balena Etcher or Raspberry Pi Imager
4. Remove SD card, plug in SSD, boot

For most Pi 4 users, "USB boot with SSD" is the correct operating mode. The SD card slot should be empty.

## Related Concepts

- [[backup-hardware-migration.md|backup hardware migration]]
- [[backup-automated.md|backup automated]]
- [[core-services-install.md|core services install]]

Sources: [SD/SSD community guide](https://www.reddit.com/r/homeassistant/comments/1dzs9x7/the_definitive_sd_card_ssd_guide_for_ha/).
