---
title: "Zigbee Coordinator Migration"
type: concept
tags:
  - backup-migration
  - zigbee
  - zha
  - zigbee2mqtt
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/backup-zigbee-coordinator
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - backup-hardware-migration.md
  - protocols-mesh.md
  - backup-migration-paths.md
content_hash: sha256:e7e07fc512c778fda869a90151f23077d07360c2e4b24f33704121c84fd8f3f9
---
# Zigbee Coordinator Migration

If you move the same USB coordinator stick, the Zigbee mesh stays in the hardware and devices do not need re-pairing. Changing coordinator hardware requires ZHA's migration wizard or Zigbee2MQTT's `coordinator_backup.json` restore.

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

## Related Concepts

- [[backup-hardware-migration.md|backup hardware migration]]
- [[protocols-mesh.md|protocols mesh]]
- [[backup-migration-paths.md|backup migration paths]]
