---
title: "Home Assistant Disaster Recovery"
type: concept
tags:
  - backup-migration
  - corruption
  - restore
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/backup-disaster-recovery
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - backup-testing.md
  - backup-builtin.md
  - backup-sd-card.md
content_hash: sha256:927eb43d12d2d488f5397da5a4fc4a442be08c552158fe1868f2cbdfca5305ab
---
# Home Assistant Disaster Recovery

When a normal restore fails, work the recovery ladder: extract config from the `.tar` backup, rename a corrupt `home-assistant_v2.db` so HA starts empty, or flash fresh storage and restore from the off-device copy. Off-device backups are non-negotiable for SD-card death.

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

## Related Concepts

- [[backup-testing.md|backup testing]]
- [[backup-builtin.md|backup builtin]]
- [[backup-sd-card.md|backup sd card]]
