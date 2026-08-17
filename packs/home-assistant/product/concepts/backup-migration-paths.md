---
title: "Common HA Hardware Upgrade Paths"
type: concept
tags:
  - backup-migration
  - n100
  - proxmox
  - ha-green
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/backup-migration-paths
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - backup-hardware-migration.md
  - backup-sd-card.md
  - core-services-install.md
content_hash: sha256:1d1cf05c11ab5bff0d217dae5ee2cdba320de5b5a3ea8fdc8d17775dccbb2235
---
# Common HA Hardware Upgrade Paths

The common 2025–2026 upgrade paths are Pi SD → Pi SSD, Pi → Intel N100 mini-PC, and bare metal → Proxmox VM. An N100 is the community sweet spot for a dedicated HA machine; HA Green and Yellow are the official appliances.

## Common Migration Paths

### Pi SD Card → Pi SSD (USB Boot)

**Best for:** Current Pi users who want to stay on Pi but gain reliability.

Process:
1. Full backup via HA UI
2. Enable USB boot on Pi (update bootloader, change boot order)
3. Flash SSD with HA OS
4. Restore backup to SSD
5. Move coordinator USB stick

Total time: ~1 hour. Zero Zigbee repairing.

### Raspberry Pi → Intel N100 Mini-PC

**Best for:** Users who want significantly better performance, more storage, and USB 3.0 SSDs built in.

N100 mini-PCs (~$100-200) offer:
- 4-8x the single-core performance of Pi 4
- 8-16GB RAM (Pi 4 max: 8GB)
- Built-in eMMC or M.2 SSD (no SD card problems)
- Multiple USB ports (no competition between SSD and coordinator)

Process: standard migration (backup → flash → restore → move coordinator).

**Recommended N100 devices (2025-2026):**
- Beelink EQ12 / EQ12 Pro (~$150-180)
- MINISFORUM UM350 (for HA + other services)
- Trigkey G4 (~$120, confirmed HA OS compatible)

Note: N100 mini-PCs use x86_64 architecture. All HA OS features work identically to Pi.

### Raspberry Pi / Bare Metal → Proxmox VM

**Best for:** Power users who want to run other services alongside HA (NAS, media server, Z2MQTT as a separate container, etc.).

Process:
1. Install Proxmox on mini-PC or NUC
2. Import HA OS as a VM (Proxmox provides an official HA OS OVA import script)
3. Pass through USB coordinator: Proxmox → VM → Hardware → Add → USB Device → select coordinator
4. Restore backup from file upload in HA onboarding

**USB passthrough in Proxmox:**
```bash
# In Proxmox VM config, add:
usb0: host=10c4:ea60  # Vendor:product ID of your coordinator
# Or pass through by port:
usb0: host=1-1.4      # USB bus-port path (stable if nothing changes)
```

## Hardware Upgrade Recommendations (2025-2026)

| Option | Price | Best For | Notes |
|--------|-------|----------|-------|
| **Intel N100 mini-PC** | ~$130-180 | Most users upgrading from Pi | Best performance/$ ratio |
| **HA Green** | ~$100 | Plug-and-play, official | eMMC storage (no SD), officially supported |
| **HA Yellow** | ~$130 (board) | Zigbee built-in, CM4 | Needs Raspberry Pi CM4 module, built-in ZHA coordinator |
| **Raspberry Pi 5 + SSD** | ~$120-150 | Pi ecosystem loyalty | 3x faster than Pi 4, but N100 still beats it for HA |
| **Proxmox on existing hardware** | $0 | Running other services too | Repurpose an old PC or laptop |

The N100 recommendation is consistent across the community in 2025-2026: it's the sweet spot for a dedicated HA machine at home. If you're buying new hardware specifically for HA, an N100 mini-PC is the answer.

## Related Concepts

- [[backup-hardware-migration.md|backup hardware migration]]
- [[backup-sd-card.md|backup sd card]]
- [[core-services-install.md|core services install]]
