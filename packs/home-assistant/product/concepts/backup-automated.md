---
title: "Automated Off-Device Backups"
type: concept
tags:
  - backup-migration
  - google-drive
  - nas
  - 3-2-1
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/backup-automated
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - backup-builtin.md
  - backup-testing.md
  - backup-sd-card.md
content_hash: sha256:ef71f648e82b098d4ee4bcd7ad9bbdbf23795583941ddde27dee87c533d9b315
---
# Automated Off-Device Backups

Manual backups are forgotten. Automate them, and store copies off the HA host — a backup that dies with the SD card is not a backup. Follow 3-2-1: one local, one on a NAS, one offsite.

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

## Related Concepts

- [[backup-builtin.md|backup builtin]]
- [[backup-testing.md|backup testing]]
- [[backup-sd-card.md|backup sd card]]
