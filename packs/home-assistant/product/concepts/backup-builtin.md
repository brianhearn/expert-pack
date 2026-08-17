---
title: "Built-In Home Assistant Backups"
type: concept
tags:
  - backup-migration
  - backups
  - restore
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/backup-builtin
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - backup-automated.md
  - backup-testing.md
  - backup-disaster-recovery.md
content_hash: sha256:77940b39bf87a786b846d96751a23705113dcf76c1a4b536f5cb08d82f165a07
---
# Built-In Home Assistant Backups

Home Assistant OS has a built-in backup system at Settings → System → Backups. A full backup includes configuration, add-ons, the recorder database, custom components, and media — enough to restore onto new hardware in under 30 minutes if the coordinator stick moves with you.

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

## Related Concepts

- [[backup-automated.md|backup automated]]
- [[backup-testing.md|backup testing]]
- [[backup-disaster-recovery.md|backup disaster recovery]]

Sources: [HA OS backups](https://www.home-assistant.io/common-tasks/os/#backups).
