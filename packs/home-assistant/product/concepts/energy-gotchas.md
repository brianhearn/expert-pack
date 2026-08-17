---
title: "Energy Dashboard Gotchas"
type: concept
tags:
  - energy-management
  - statistics
  - recorder
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/energy-gotchas
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - energy-dashboard.md
  - energy-automations.md
  - energy-riemann-utility.md
content_hash: sha256:960cd95791d1af9ecbd0178e8eaaa1a0958df65d782e83a55a76f36aee9979fc
---
# Energy Dashboard Gotchas

Energy gotchas are sensor resets, the one-hour statistics delay, no retroactive history for newly added sources, high-frequency power sensors bloating the recorder, and orphaned statistics after an entity ID change on migration.

## Common Gotchas

### Sensor resets to zero on device reboot

`state_class: total_increasing` handles this. When the new value is less than the last recorded value, HA treats it as a reset and continues accumulating from the new baseline. As long as the drop is large (>10% decrease), HA will detect it correctly. Small decreases (<10%) might be misinterpreted as actual negative energy use — this is rare but can happen with some integrations.

### Statistics require at least 1 hour of data

The Energy Dashboard won't show meaningful data until HA has at least an hour of statistics. When you first set up a sensor, the dashboard may show zeros or gaps. This is normal — let it run for a few hours.

### Adding sources retroactively

If you add a new sensor to the Energy Dashboard after running for weeks, the historical data **before** that sensor was added will not appear. HA can only retroactively import statistics for specific integrations (like SolarEdge) that support historical data import. For most sensors, you only have data from when you first configured them.

**Practical implication:** Set up Energy Dashboard sensors as early as possible in your HA journey. The data you don't capture now is gone forever.

### High-frequency sensor updates slow down the recorder

A smart plug that reports power every 5 seconds generates 17,280 state changes per day — just for one device. Multiply by 20 devices and your recorder database grows rapidly.

**Solutions:**
- Set `scan_interval` or reporting threshold in the integration/device settings
- Use `filter` integration to debounce rapid sensor updates
- Exclude raw power sensors from recorder if you only need the derived energy sensor:

```yaml
recorder:
  exclude:
    entity_globs:
      - sensor.*_power_w  # Exclude raw W sensors, keep kWh sensors
```

### Energy Dashboard shows incorrect totals after migration

If you migrate HA to new hardware or restore from backup, the long-term statistics database comes with the backup. If a sensor's entity ID changed during migration, HA can't connect the historical statistics to the new entity. Use Developer Tools → Statistics to manually associate old statistics with the new entity ID.

## Related Concepts

- [[energy-dashboard.md|energy dashboard]]
- [[energy-automations.md|energy automations]]
- [[energy-riemann-utility.md|energy riemann utility]]
