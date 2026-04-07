---
title: Diagnostic Guide — Systematic Home Assistant Troubleshooting
type: troubleshooting
tags:
- core-architecture
- diagnostic-guide
- integrations-guide
- troubleshooting
- yaml-configuration
pack: home-assistant-product
retrieval_strategy: atomic
---
<!-- context: section=troubleshooting, topic=diagnostic-guide, related=core-architecture,yaml-configuration,integrations-guide -->
---
sources:
  - type: documentation
    url: "https://www.home-assistant.io/docs/troubleshooting/"
    date: "2026-03"
  - type: documentation
    url: "https://www.home-assistant.io/docs/tools/dev-tools/"
    date: "2026-03"
  - type: documentation
    url: "https://www.home-assistant.io/docs/backend/database/"
    date: "2026-03"
  - type: community
    url: "https://community.home-assistant.io/t/complete-guide-to-home-assistant-diagnostics/490200"
    date: "2025-09"
  - type: community
    url: "https://community.home-assistant.io/t/zigbee-troubleshooting-megathread/550032"
    date: "2025-11"
---

# Diagnostic Guide — Systematic Home Assistant Troubleshooting

> **Lead summary:** Most HA problems follow predictable patterns. The key is systematic diagnosis: start with the logs (they usually tell you exactly what's wrong), use Developer Tools to interrogate entity state in real time, and know when to reload vs restart vs use safe mode. Zigbee mesh problems, database corruption, and automation logic errors each have distinct diagnostic signatures. This guide gives you the toolkit and decision tree for resolving 90% of HA issues methodically rather than randomly.

## The Diagnostic Toolkit

### Developer Tools — Your First Stop

Developer Tools (the wrench icon, or `/developer-tools`) is where diagnosis starts:

**States tab:** View every entity's current state and attributes. Filter by entity ID or domain. This is the live view of the HA state machine. If an entity shows `unavailable` here, the integration has lost connection. If it shows an unexpected value, the integration is reporting something wrong.

**Services/Actions tab:** Call any service with custom parameters. Essential for testing automations: call `light.turn_on` directly to verify the service works before troubleshooting the automation.

**Template tab:** Live Jinja2 template editor. Type a template, see the evaluated result immediately. Invaluable for debugging template errors before they're embedded in automations.

**Events tab:** Monitor the event bus in real time. Start listening, then perform an action — you can see every event fired. Useful for understanding what events a device generates (especially when debugging triggers).

**Statistics tab:** View long-term statistics for sensor entities. Shows if statistics are being recorded correctly.

### Log Viewer

Settings → System → Logs. This is where integration errors, startup failures, and automation errors appear.

**Log structure:**
```
2026-03-11 14:23:01.234 WARNING (MainThread) [homeassistant.components.hue] Error connecting to Hue Bridge: timeout
2026-03-11 14:23:15.789 ERROR (MainThread) [custom_components.frigate] Failed to connect: connection refused
```

The bracketed component identifier tells you exactly which integration is generating the log. Use this to filter:
- Official integrations: `homeassistant.components.<name>`
- Custom (HACS) integrations: `custom_components.<name>`

**Filtering:** Use the filter box to show only logs from a specific integration: type `hue` to see only Hue-related logs.

**Log levels:**
- **ERROR**: Something failed. Always investigate.
- **WARNING**: Potential problem or deprecation notice.
- **INFO**: Normal operational messages.
- **DEBUG**: Verbose diagnostic output (only enabled explicitly).

### System Information

Settings → System → Hardware (or System) — shows HA version, Python version, host information, memory, disk usage. Check this first when performance is degrading.

`Settings → System → Repairs` — HA's self-diagnostic system. Lists known issues with integrations, deprecated configurations, and actions needed. Check this after every HA update.

## Reading Logs Effectively

### Setting Per-Integration Log Levels

Enable debug logging for a specific integration without drowning in all-system debug output:

```yaml
# configuration.yaml — add temporarily, remove when done
logger:
  default: warning
  logs:
    homeassistant.components.zha: debug
    homeassistant.components.recorder: debug
    zigpy: debug
    bellows: debug  # ZHA's Zigbee stack for EZSP (Silicon Labs) coordinators
    zigpy_znp: debug  # ZHA's Zigbee stack for ZNP (Texas Instruments) coordinators
```

After adding: Developer Tools → YAML → Reload Logger Settings (no restart needed).

**After debugging:** Remove the debug overrides. Debug logging generates MB of data per hour and degrades performance.

### Integration Identifier Reference

| Integration | Logger Identifier |
|------------|------------------|
| ZHA | `homeassistant.components.zha`, `zigpy`, `bellows`, `zigpy_znp` |
| Zigbee2MQTT | The add-on has its own log — check in add-on page |
| Z-Wave JS | `homeassistant.components.zwave_js`, `zwave_js_server` |
| ESPHome | `homeassistant.components.esphome` |
| Recorder/Database | `homeassistant.components.recorder` |
| Automations | `homeassistant.components.automation` |
| Hue | `homeassistant.components.hue` |

## Safe Mode — When HA Won't Start

Safe mode boots HA with no custom integrations (HACS), no custom frontend resources (custom cards), and no automations running. It's your recovery tool when a bad update, corrupted custom component, or YAML error prevents normal startup.

**How to enter safe mode:**

Option 1 (if HA is running): Settings → System → Restart → Safe Mode

Option 2 (if HA won't start): Hold the Home Assistant button on Raspberry Pi while it boots (if HA OS). Alternatively, SSH into the host and run:
```bash
ha core restart --safe-mode
```

**What safe mode disables:**
- All HACS custom integrations
- All frontend custom cards/themes
- All automations (won't run but aren't deleted)

**What safe mode keeps running:**
- All official integrations
- Core functionality
- Access to Settings, Developer Tools, Logs

**Typical safe mode workflow:**
1. HA won't start after update → enter safe mode → access UI
2. Check Settings → Repairs for known issues
3. Check logs for the actual error
4. Identify which custom component is causing the problem
5. Disable or remove the offending component
6. Restart normally

## Database Issues

HA stores entity history and statistics in an SQLite database (`home-assistant_v2.db`). Over time this can become problematic.

### Database Corruption

Symptoms: HA starts slowly, errors like `SQLITE_CORRUPT`, database-related errors in logs, history not loading.

**Cause:** SD card write failures (very common on Raspberry Pi), power cuts during writes, running out of disk space.

**Fix — Purge and rebuild:**
```yaml
# In Developer Tools → Services:
# Call: recorder.purge_entities
# Or nuclear option: stop HA, delete the database, restart

# Stop HA first:
ha core stop

# Delete the database (SSH or terminal):
rm /config/home-assistant_v2.db
rm /config/home-assistant_v2.db-wal
rm /config/home-assistant_v2.db-shm

# Restart HA — it creates a fresh database
ha core start
```

**Note:** Deleting the database loses all entity history. This is usually acceptable — configuration and automations are fine.

### Moving to External Database (PostgreSQL/MariaDB)

For large installs (1000+ entities, 30+ day history), SQLite becomes a performance bottleneck. Moving to PostgreSQL or MariaDB improves:
- Query performance
- Concurrent access
- Reliability under load
- Backup options

**MariaDB setup (easiest via HA OS):**
1. Install MariaDB add-on
2. Configure a database and user
3. Add to `configuration.yaml`:
```yaml
recorder:
  db_url: mysql://recorder_user:password@core-mariadb/homeassistant?charset=utf8mb4
```
4. Stop HA, migrate data (optional — or start fresh), start HA

**Practical threshold:** Switch from SQLite when you notice:
- HA UI is slow to load history graphs
- Database file exceeds 5-10 GB
- Recorder errors appearing in logs under load

### Recorder Configuration Optimization

Before moving to external DB, optimize the recorder config to reduce write load:

```yaml
recorder:
  purge_keep_days: 14           # Keep 14 days of history (default is 10)
  commit_interval: 5            # Write batch every 5 seconds instead of 1
  exclude:
    domains:
      - weather                  # Weather history is rarely useful
      - sun
    entities:
      - sensor.time
      - sensor.date
      - sensor.last_boot
      - sensor.uptime
    entity_globs:
      - sensor.*_signal_strength # Skip WiFi signal for every device
      - sensor.*_link_quality_indicator
```

Excluding high-frequency sensors (time, signal strength, LQI) can reduce database writes by 30-50%.

## Network Diagnostics

### mDNS Issues

HA discovers many devices via mDNS (`.local` hostnames). Problems arise in:
- **VLAN setups:** mDNS doesn't cross VLAN boundaries by default. Devices on an IoT VLAN can't be discovered by HA on the main VLAN without mDNS reflection (Avahi proxy, Unifi mDNS proxy).
- **Docker networking:** HA Container installs may have mDNS issues depending on Docker network mode. Use `--network=host` or configure mDNS proxy.

**Test mDNS resolution:**
```bash
# From HA host terminal:
avahi-browse -a  # List all mDNS-advertised services
ping homeassistant.local
```

### DHCP Reservations for IoT Devices

**Every IoT device should have a DHCP reservation** (fixed IP via MAC address). Reasons:
1. Device tracking: IP-based tracking breaks if the IP changes
2. Firewall rules: VLAN rules targeting specific IPs need stable IPs
3. Integration config: some integrations store the IP — changing IPs breaks them

Set reservations in your router/DHCP server. After adding a reservation, devices may need to renew their lease.

### VLAN Considerations for HA

A common advanced setup: IoT devices on an isolated VLAN (no internet access) with HA either on the main network or a dedicated HA VLAN.

**What needs to work across VLANs:**
- HA → IoT devices: UDP/TCP to device IPs (allow in firewall)
- IoT devices → HA API (port 8123): needed for ESPHome devices to connect back
- mDNS: needs mDNS reflection configured
- MQTT: broker must be reachable from IoT VLAN (if using Zigbee2MQTT/Tasmota)

**Simpler alternative:** Put HA on the IoT VLAN with internet access controlled via firewall policy. Less overhead, HA can reach all devices.

## Zigbee Troubleshooting

### Understanding Zigbee Mesh Health

A healthy Zigbee mesh has:
- Multiple router devices per area (mains-powered plugs, switches, lights)
- No battery devices relying on just one router
- LQI (Link Quality Indicator) > 100 on all routes (255 = perfect, 0 = no connection)

**Visualize the mesh:** ZHA: Settings → Zigbee Home Automation → Visualization (shows mesh topology as graph)
Zigbee2MQTT: has a built-in map that shows all devices and their connections.

### Coordinator Firmware Updates

The Zigbee coordinator dongle has firmware that occasionally needs updating. Outdated coordinator firmware causes:
- Pairing failures with new devices
- Dropped connections
- Random device unavailability

**Check current firmware:**
- ZHA: Settings → ZHA → Coordinator info shows firmware version
- Compare to latest release on coordinator manufacturer's GitHub

**Popular coordinator firmware sources:**
- Sonoff ZBDongle-P (CC2652P): `github.com/Koenkk/Z-Stack-firmware`
- Home Assistant Connect ZBT-1 (EFR32): HA update mechanism

### WiFi Channel Conflicts

Zigbee runs on 2.4 GHz and shares spectrum with WiFi. Zigbee channels 11-24 overlap with WiFi channels 1-11. This is a major source of intermittent Zigbee problems.

**Non-overlapping channels:**
- Zigbee 15, 20, 25, 26 are clear of WiFi channels 1, 6, 11 (use one of these)
- Zigbee 11 conflicts heavily with WiFi channel 1

**Check your WiFi channels** in your router admin. Set Zigbee to a channel that doesn't overlap. In ZHA: Settings → ZHA → Configure → Channel migration. **This requires re-pairing all devices** — schedule it.

### Device Won't Pair

1. **Distance:** Pair the device within 2 meters of the coordinator, then move it
2. **Channel issue:** Wrong channel won't pair at all
3. **Firmware:** Old coordinator firmware may not support newer Zigbee 3.0 devices
4. **Reset:** Factory reset the device first — previous pairing state can prevent re-pairing
5. **Permit join:** Ensure "permit join" is active in ZHA/Zigbee2MQTT during pairing

## Z-Wave Troubleshooting

### Ghost Nodes

Z-Wave ghost nodes are entries in the node list that refer to devices that no longer exist or can no longer be reached. They consume network resources and can cause routing issues.

**Identify:** In Z-Wave JS UI, ghost nodes show as "dead" with no communication for extended periods.

**Remove ghost nodes:**
1. Z-Wave JS UI → Nodes → [ghost node] → Remove Failed Node
2. If that fails: Heal network, then retry
3. Last resort: exclude the node manually (put controller in exclusion mode, press button on nothing — sometimes clears ghost entries)

### Network Heal

The Z-Wave network heal rebuilds routing tables — all devices recalculate optimal paths. Run this after:
- Adding new devices (especially routers/powered devices)
- Moving devices
- Removing devices
- After a ghost node removal

**Trigger:** Z-Wave JS UI → Controller → Heal Network
**Time:** 30 seconds to 5 minutes depending on network size. Run overnight for large networks.

### S2 Security Pairing Issues

Z-Wave devices with S2 (Secure Mode 2) security require a DSK (Device Specific Key) or QR code for secure inclusion. If pairing fails:

1. Check that Z-Wave JS is up to date
2. Have the DSK (on device label) ready before starting inclusion
3. S2 Unauthenticated pairing (without DSK) is a fallback — less secure but works
4. Some older controllers don't support S2 — verify coordinator firmware

## Automation Debugging — The Trace View

When an automation doesn't behave as expected, the **trace view** is the most powerful debugging tool.

**Access trace:** Settings → Automations → [automation] → Traces button (clock icon)

The trace view shows:
- Every run of the automation (last 5-10 stored)
- For each run: which trigger fired, which conditions were evaluated (passed/failed), which actions executed
- For conditions: the actual values evaluated ("entity state was 'off', expected 'on' — condition failed")
- For templates: the rendered result of each template
- Timing: how long each step took

**Common trace diagnoses:**

*"Trigger fired but nothing happened"* → Check conditions section — one likely failed silently

*"Automation triggered too many times"* → Trigger is firing repeatedly (e.g., template trigger oscillates)

*"Wait for trigger timed out"* → Expected state never occurred within timeout window

*"Action failed"* → Service call errored — check entity availability

**Template debugging in trace:**
Click on any template step to see: the template source, rendered values of variables, and the final output. This catches type mismatch errors ("'72.5' > 70" where both sides are strings).

## Performance Optimization

### Entity Count Impact

HA runs well up to approximately 2,000 entities. After that, startup time and memory usage grow noticeably. At 5,000+ entities, performance degradation is significant.

**Reduce entity count:**
- Use `disabled_by_default: true` in ESPHome for diagnostic entities you don't need in HA
- Disable unused entities in Settings → Entities (filter by integration)
- Consider whether you need every attribute of every device exposed as an entity

### Recorder Pressure

The database recorder writes every state change. High-frequency sensors (time, sun angle, signal strength) write thousands of times per day.

**Check database size:**
```bash
# SSH to HA host
ls -lh /config/home-assistant_v2.db
```

A database over 3-4 GB on an SD card suggests misconfigured recorder includes. See recorder exclusion config above.

## The Nuclear Option — When to Start Fresh

Sometimes the correct answer is a clean install. Triggers:

- **Corrupted database AND configuration** — data is gone, config is broken
- **Deep HACS custom component conflicts** — 5+ custom integrations all breaking after HA update
- **Migration from old HA version (3+ major versions behind)** — too many breaking changes accumulated
- **Migration to new hardware** — take a backup, restore to new hardware is actually cleaner than in-place upgrade

**What to preserve before starting fresh:**
1. `configuration.yaml` and all YAML configs (version control is ideal)
2. List of integrations (screenshot Settings → Integrations)
3. List of HACS components
4. Automations export (YAML view)
5. Any `.storage/` files for integrations not configurable via YAML

**What you lose:** Entity history, statistics, long-term tracking data. Decide if that's acceptable.

**The verdict:** If you've spent more than 4 hours debugging a problem and still haven't found it, a clean install + backup restore is often faster and results in a healthier system.

## Related

- [[core-architecture.md|Core Architecture]] — Understanding what you're troubleshooting
- [[yaml-configuration.md|YAML Configuration]] — Config validation workflow
- [[top-ha-mistakes.md|Top HA Mistakes]] — Avoid the most common problems
- [[integrations-guide.md|Integrations Guide]] — Integration-specific troubleshooting

---

## Community-Sourced Diagnostic Tips

> Appended from community mining, 2026-03-12.
> Sources: r/homeassistant, community.home-assistant.io, GitHub issues, Hacker News.

### Finding What's Bloating Your Recorder Database

Install the **SQLite Web add-on** (HAOS only) and run this query to find the top 20 entities filling your database. This is the #1 community-recommended first step for "HA is slow" complaints:

```sql
SELECT m.entity_id, COUNT(*) as count
FROM states AS S
INNER JOIN states_meta AS M ON M.metadata_id = s.metadata_id
GROUP BY m.entity_id
ORDER BY count DESC
LIMIT 20;
```

Typical offenders: radar presence sensors (`sensor.*_last_seen`, `sensor.*_linkquality`), BLE distance sensors, IKEA Fornuftig air quality, any sensor with sub-second state changes. Exclude them in `recorder:` config, then run `Recorder: Purge` with `repack: true` and `apply_filter: true`. Source: [edvoncken.net](https://edvoncken.net/2025/01/reduce-homeassistant-database/), Jan 2025.

### Diagnosing Z-Wave "Unavailable" After Add-on Update

After every Z-Wave JS add-on update, devices may appear "unavailable" even after restart. Standard workaround:
1. Go to Developer Tools → States, filter for Z-Wave devices showing "unavailable"
2. For each device: Settings → Devices → device → Z-Wave JS → Re-interview device
3. If "Re-interview" does nothing (modal stays open, no error), restart the Z-Wave JS add-on then retry
4. Reverting to an older add-on backup does NOT fix this — the state cache must be rebuilt

Source: [GitHub home-assistant/core #126235](https://github.com/home-assistant/core/issues/126235), Sep 2024.

### Diagnosing Zigbee2MQTT Action Sensor Breakage

If button/remote automations stopped working after Z2M update to 2.0+:
1. Check if `sensor.devicename_action` entities still exist (they may be disabled, not deleted)
2. In HA, go to Settings → Devices → find the device → check "Disabled entities"
3. Either enable the sensor entities AND add `homeassistant: { legacy_action_sensor: true }` to Z2M config
4. OR migrate automations to use MQTT device triggers (recommended long-term)
5. Also verify: Settings → Devices & Services → MQTT → Configure → Birth message topic = `homeassistant/status`

Source: [Z2M Discussion #24198](https://github.com/Koenkk/zigbee2mqtt/discussions/24198), [Reddit r/homeassistant](https://www.reddit.com/r/homeassistant/comments/1hu5h8s/), Jan 2025.

### Automation Trace — Most Underused Debug Tool

The **Traces** button (top-right corner of the automation editor) is the fastest way to debug automation failures. It shows:
- Which trigger fired (or didn't fire)
- Variable values at each step
- Which condition failed and why
- Which action errored, and the exact error

Use this before reading logs. Most automation "why isn't this firing?" questions can be answered in 30 seconds with traces. Source: [XDA Developers](https://www.xda-developers.com/things-wish-knew-before-going-all-in-home-assistant/), Aug 2025.

### Diagnosing HACS After HA Updates

If HACS disappears from sidebar or shows all integrations as broken after an HA update:
1. Settings → Devices & Services → HACS → Configure → enable "AppDaemon apps discovery & tracking" → save (fixes disappearing sidebar)
2. If integrations show stale "unavailable update" status: HACS → select integration → 3-dot menu → Re-download
3. If HACS itself fails to load (critical error in logs): update HACS via terminal using `wget -O - https://get.hacs.xyz | bash -` and restart HA

Source: [GitHub hacs/integration #4314](https://github.com/hacs/integration/issues/4314), [Reddit r/homeassistant](https://www.reddit.com/r/homeassistant/comments/1htm6kq/), Jan 2025.
