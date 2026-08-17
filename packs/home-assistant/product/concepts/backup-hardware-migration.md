---
title: "Migrating Home Assistant to New Hardware"
type: concept
tags:
  - backup-migration
  - restore
  - usb-path
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/backup-hardware-migration
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - backup-zigbee-coordinator.md
  - backup-migration-paths.md
  - backup-builtin.md
content_hash: sha256:1e618df58159645bc40b5eb4bc7e4fd01d772c674edb4da60dc3529a425047e8
---
# Migrating Home Assistant to New Hardware

Migrating HA to new hardware is backup → flash HA OS → restore → move USB coordinators. YAML, automations, dashboards, add-ons, HACS, and history transfer. What needs attention is the coordinator device path, IP/URL, and SSL certs.

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

## Related Concepts

- [[backup-zigbee-coordinator.md|backup zigbee coordinator]]
- [[backup-migration-paths.md|backup migration paths]]
- [[backup-builtin.md|backup builtin]]
