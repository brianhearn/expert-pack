---
title: "Testing Home Assistant Backups"
type: concept
tags:
  - backup-migration
  - restore
  - backup-test
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/backup-testing
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - backup-builtin.md
  - backup-disaster-recovery.md
  - backup-automated.md
content_hash: sha256:cae3990a90d4bf3479f253af31f8b9656e7d7de9f39452f2c583664aead1b7b9
---
# Testing Home Assistant Backups

The only backup test that matters is actually restoring one. Periodic restore onto a spare Pi or Proxmox VM is how you discover missing OAuth re-auth, wrong URLs, or incomplete archives before disaster.

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

## Related Concepts

- [[backup-builtin.md|backup builtin]]
- [[backup-disaster-recovery.md|backup disaster recovery]]
- [[backup-automated.md|backup automated]]
