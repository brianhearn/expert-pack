---
title: Backup, Migration, and Hardware Upgrades
type: concept
tags:
- backup-migration
- concepts
- core-architecture
- network-architecture
pack: home-assistant-product
retrieval_strategy: standard
---
<!-- context: section=concepts, topic=backup-migration, related=core-architecture,network-architecture -->
---
sources:
  - type: documentation
    url: "https://www.home-assistant.io/common-tasks/os/#backups"
    date: "2026-03"
  - type: documentation
    url: "https://www.home-assistant.io/installation/raspberrypi/"
    date: "2026-03"
  - type: community
    url: "https://community.home-assistant.io/t/migration-from-pi-to-new-hardware-guide/541821"
    date: "2025-11"
  - type: community
    url: "https://www.reddit.com/r/homeassistant/comments/1dzs9x7/the_definitive_sd_card_ssd_guide_for_ha/"
    date: "2025-08"
---

# Backup, Migration, and Hardware Upgrades

> **Lead summary:** Home Assistant's backup system is remarkably good — a full system backup (including add-ons, configuration, and database) can be restored to completely new hardware in under 30 minutes, with your Zigbee/Z-Wave mesh intact as long as you migrate the coordinator USB stick. The most common failure mode isn't backup complexity; it's people running on SD cards that die without warning. The solution is simple: move to SSD early, automate off-device backups, and test your backups by restoring them before you actually need to. All three together make HA a resilient foundation rather than a fragile one.

## The Built-In Backup System

Home Assistant OS has a built-in backup system (Settings → System → Backups). No extra software required.

### What's Included in a Full Backup

A full backup contains everything:
- **Configuration** (`/config` directory) — all YAML files, `configuration.yaml`, automations, scripts, dashboards, secrets
- **Add-ons** — the add-on data for each installed add-on (Mosquitto, Z2MQTT, Nginx, etc.)
- **Database** — the recorder database (`home-assistant_v2.db`) — state history, energy statistics, logbook
- **Home Assistant core** — the HA version itself (allows version pinning on restore)
- **Custom components** (HACS and manual installs in `custom_components/`)
- **Media** — if you store media in HA's media folder
- **SSH keys** and other security material

### Full vs Partial Backups

**Full backup:** Everything. Recommended for scheduled backups.

**Partial backup:** You select which components to include. Use cases:
- Quick backup before making a risky config change (just config, no add-ons)
- Smaller backup when the database is large and you only need the config
- Faster backup when storage is limited

**Backup size reality:** A full HA backup with history database can be 500MB-5GB depending on how long you've been running and how many entities you track. Excluding the database dramatically reduces size and backup time — but you lose historical data on restore.

### Backup from CLI (for scripting)

```bash
# Via HA supervisor CLI (in SSH add-on terminal)
ha backups new --name "pre-update-backup" --type full

# Or via HA REST API
curl -X POST http://localhost:8123/api/backup \
  -H "Authorization: Bearer YOUR_LONG_LIVED_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "weekly-backup"}'
```

## Automated Backup Strategies

Manual backups are forgotten. Automate them.

### Built-in Backup Automation (HA 2024.6+)

Settings → System → Backups → Configure Automatic Backups:
- Schedule: daily/weekly (weekly minimum for most setups)
- Retention: keep last N backups
- Location: local storage (the HA `/backup` folder)

This is the minimum viable backup setup. The issue: it's still on-device. If your storage dies, the backups die with it.

### Off-Device Storage (Critical)

Your backup is only useful if it survives the failure you're recovering from. Store backups off the HA host.

**Option 1: Google Drive (Google Drive Backup add-on)**

The community [Google Drive Backup](https://github.com/sabeechen/hassio-google-drive-backup) add-on (available in HACS add-ons) is the most popular off-device backup solution:
- Automatically uploads backups to Google Drive
- Configurable retention (delete old backups automatically)
- Dashboard UI for backup status
- Free (uses your Google Drive storage)

Setup: Install add-on → authenticate with Google → configure schedule and retention.

**Option 2: Network Share (Samba)**

If you have a NAS or another machine on your network, configure HA to write backups there:

Settings → System → Storage → Add Network Storage → type: Backup

The storage appears as a backup location in the backup UI. Works with Samba (SMB) shares on Synology, TrueNAS, Windows, etc.

**Option 3: Automation + File Copy**

```yaml
automation:
  - alias: "Weekly Backup to NAS"
    trigger:
      - trigger: time
        at: "03:00:00"
    condition:
      - condition: time
        weekday: [sun]
    action:
      # Create the backup
      - action: backup.create
        data:
          name: >
            weekly-{{ now().strftime('%Y-%m-%d') }}
      # Wait for backup to complete (the service call returns before it's done)
      - delay: "00:05:00"
      # Optionally: use shell command to rsync to NAS
      - action: shell_command.rsync_backup_to_nas
```

**Rule of thumb:** Follow the 3-2-1 backup rule — 3 copies, 2 different media, 1 offsite. For home labs this usually means: 1 local backup on HA host + 1 on NAS + 1 in cloud.

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

## Migration to New Hardware

The process for migrating to new hardware is simpler than people expect.

### Standard Migration Process

1. **Create a full backup** of your current system (Settings → Backups → Create Backup)
2. Download the backup file to your computer (or confirm it's in off-device storage)
3. **Flash new hardware** with HA OS using Balena Etcher or the HA installer
4. Start the new hardware and complete the initial onboarding (just enough to get to the UI)
5. **Restore from backup:** In the onboarding flow, choose "Restore from backup" → upload your file
6. HA restores everything — config, add-ons, dashboards, integrations, database
7. **Move USB devices** (Zigbee/Z-Wave coordinator sticks) to the new host
8. HA recognizes the coordinator at its expected USB path

That's it. Your automations work, your history is intact, your HACS integrations are there.

### What Transfers Seamlessly

- All YAML configuration
- All automations, scripts, scenes
- Dashboards (Lovelace config)
- All integration configs and credentials (stored encrypted in `.storage/`)
- Add-ons (Mosquitto, Z2MQTT, Nginx, Frigate, etc.) and their configurations
- HACS and custom integrations
- Long-term statistics and recorder history
- User accounts and permissions

### What Needs Attention

**USB coordinator path:**
After migration, your Zigbee/Z-Wave coordinator usually gets a different USB device path (`/dev/ttyUSB0` vs `/dev/ttyACM0`). Check the add-on configuration (ZHA, Zigbee2MQTT) and update the device path if needed. Better: use the device's ID path (`/dev/serial/by-id/usb-XXXX`) which is stable across reboots and hardware changes.

```yaml
# Zigbee2MQTT configuration.yaml — use stable device path
serial:
  port: /dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller-if00-port0
```

**IP address:**
If your HA host gets a different IP on the new hardware, update any hardcoded IPs in your config files, scripts, or external integrations. Better: use a DNS hostname (`homeassistant.local` or a reserved DHCP IP).

**SSL certificates:**
If you had custom SSL certs, re-issue or recopy them. Let's Encrypt certs in the Nginx/Caddy add-on will auto-renew after migration.

**HA URL setting:**
Settings → System → General → Internal URL / External URL may need updating after IP changes.

## Zigbee Coordinator Migration

The coordinator migration is the part people worry about most. The reality is straightforward:

### Same Coordinator Stick → Zero Work

If you move the same USB coordinator stick (ConBee II, Sonoff Zigbee 3.0, HUSBZB-1, etc.) from old hardware to new hardware:
- The Zigbee mesh is stored in the coordinator hardware
- All paired devices remember the coordinator
- All they need is for the coordinator to come back online — which it does, on the new host
- **Zero repairing of Zigbee devices**

This is why coordinator selection matters: pick a stick you can easily move between hosts.

### Different Coordinator → Migration Required

If you're changing coordinator hardware (e.g., ConBee II → Sonoff Zigbee 3.0, or upgrading from USB to network coordinator):

**ZHA migration:**
1. ZHA has a built-in coordinator migration wizard (Settings → Devices & Services → ZHA → Migrate coordinator)
2. It exports the network key and attempts to migrate to the new stick
3. Results vary — simpler devices usually migrate; some devices may need re-pairing

**Zigbee2MQTT migration:**
Z2MQTT stores the Zigbee network configuration in `coordinator_backup.json` and `coordinator_backup_yaml`. The migration process:
1. Create a backup in Z2MQTT UI → Zigbee → Create backup
2. Swap coordinator
3. In Z2MQTT config, set the new port
4. On first start, Z2MQTT will attempt to restore the network backup to the new coordinator

Z2MQTT's migration is generally more reliable than ZHA's due to better backup/restore tooling.

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

## Disaster Recovery

When the normal restore process fails, here's the recovery ladder:

### Level 1: Restore Fails — Config Extraction

If HA won't boot and you can't restore from backup, you can manually extract config files from the backup archive:

```bash
# HA backup files are .tar archives containing .tar.gz archives
tar xf backup-file.tar
# Inside: homeassistant.tar.gz
tar xzf homeassistant.tar.gz
# Inside: /data/config/ — all your YAML files
# Inside: /data/storage/ — integration credentials, entity registry
```

You can then manually restore by:
1. Starting fresh HA install
2. Copying extracted config files to `/config/`
3. Recreating integrations (credentials are in `.storage/core.config_entries`)

### Level 2: Corrupted Database

The recorder database (`home-assistant_v2.db`) is the most common corruption point. If HA can't start because of database corruption:

1. SSH into the HA host (or use Terminal add-on)
2. Stop HA: `ha core stop`
3. Rename the database: `mv /config/home-assistant_v2.db /config/home-assistant_v2.db.corrupt`
4. Start HA: `ha core start` — HA creates a fresh empty database
5. Your history is gone, but automations, dashboards, and entities return immediately

Losing history is painful but far better than a completely dead HA. Your automations never cared about historical data anyway.

### Level 3: Filesystem Corruption (SD Card Death)

If the underlying storage is corrupted (SD card failure):
1. Flash new storage with fresh HA OS
2. Complete initial onboarding
3. Restore from your off-device backup

This is why off-device backups are non-negotiable. Local-only backups on a dying SD card may be inaccessible when you need them.

## Testing Backups

**The only test that matters: actually restoring the backup.**

Many people set up automated backups, feel good about it, and never discover until disaster strikes that the backups are incomplete, corrupted, or missing critical pieces.

**Test your backups periodically:**

1. **Use Proxmox or a spare Pi:** Spin up a fresh HA instance, restore your latest backup, verify everything works
2. **Document what actually restores:** Note any post-restore steps (IP changes, re-authenticating integrations, etc.)
3. **Check backup completion in logs:** The Google Drive Backup add-on shows backup status; verify backups are actually uploading

**Restoration checklist after test restore:**
- [ ] Dashboard loads and shows correct entities
- [ ] A few automations fire correctly (test manually via Developer Tools)
- [ ] Add-ons started (Z2MQTT, Mosquitto, etc.)
- [ ] Integrations authenticated (OAuth integrations like Google, Nest, etc. may need re-auth)
- [ ] Coordinator recognized and devices online

Most people who test this process for the first time discover one OAuth integration that needs re-authentication after restore. Better to discover this in a test than in a real emergency.

## Related

- [[core-architecture.md|Core Architecture]] — What each component of HA stores and where
- [[network-architecture.md|Network Architecture]] — Remote access options (needed after migration to new IP)
- [[protocols.md|Smart Home Protocols]] — Zigbee coordinator hardware selection
