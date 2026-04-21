---
title: Common Mistakes in Home Assistant
type: gotcha
tags:
- common-mistakes
- gotchas
pack: home-assistant-process
retrieval_strategy: atomic
id: home-assistant/process/gotchas/common-mistakes
verified_at: "2026-04-21"
verified_by: agent
schema_version: "4.1"
---
# Common Mistakes in Home Assistant

These are the mistakes that cost people the most time and frustration. Learn them before you start.

---

## Mistake 1: SD Card Storage

**What happens:** Your HA installation corrupts after a power blip or fails silently after 6-12 months. You lose your configuration, automations, and device pairing database.

**Why it happens:** Home Assistant writes constantly to its SQLite database (every state change, every logbook entry). SD cards are not designed for this write load and fail unpredictably.

**The fix:** Always use an SSD. USB 3.0 SSD on a Pi ($35-40), or NVMe on a mini-PC or Pi 5 with HAT. If you're already on an SD card:
1. Create a full backup (Settings → System → Backup)
2. Flash HA OS to a USB SSD
3. Restore from backup

→ See [Hardware Selection](../decisions/hardware-selection.md#storage-ssd-vs-sd-card)

---

## Mistake 2: Using Wi-Fi for Everything

**What happens:** Router degrades under 30+ IoT devices. Devices randomly go offline. Automations become unreliable. Most cloud-dependent Wi-Fi devices stop working when the manufacturer shuts down their servers.

**Why it happens:** Wi-Fi devices are marketed as "no hub required" which sounds simpler. Short-term, it is. Long-term, it's a mess.

**The fix:** Use Zigbee or Z-Wave for sensors, switches, plugs, and bulbs. Reserve Wi-Fi for devices that must be Wi-Fi (cameras, smart displays, appliances). A $25 Zigbee coordinator handles 100+ devices without impacting your router.

→ See [[protocol-selection.md|Protocol Selection]]

---

## Mistake 3: Zigbee Coordinator Too Close to USB 3.0 Ports

**What happens:** Zigbee devices pair fine but randomly drop offline. LQI values are low. Devices that should be in range aren't reaching the coordinator.

**Why it happens:** USB 3.0 ports emit RF noise in the 2.4GHz band that Zigbee uses. Plugging the dongle directly into a USB 3.0 port on a Pi or mini-PC causes interference.

**The fix:** Use a short (20-30cm) **USB 2.0** extension cable to physically separate the dongle from the USB 3.0 port. Also: in Zigbee2MQTT, change the Zigbee channel to 25 or 26 (these overlap least with common Wi-Fi channels).

---

## Mistake 4: Wrong Automation Mode for Motion Lights

**What happens:** Motion-activated lights turn off while you're still in the room. Moving again doesn't reset the timer.

**Why it happens:** The default automation mode is `single` — if the automation is already running (waiting for the off-delay), new triggers are ignored.

**The fix:** Set `mode: restart` on motion-lighting automations so each new motion event resets the off-delay timer:

```yaml
automation:
  mode: restart
  trigger:
    - platform: state
      entity_id: binary_sensor.kitchen_motion
      to: "on"
  action:
    - service: light.turn_on
      entity_id: light.kitchen
    - delay: "00:05:00"
    - service: light.turn_off
      entity_id: light.kitchen
```

→ See [[motion-lighting.md|Motion Lighting Pattern]]

---

## Mistake 5: Not Setting Up Backups on Day One

**What happens:** HA crashes or hardware fails six months in. You lose your entire configuration.

**Why it happens:** Backups are boring and don't seem urgent until they're needed.

**The fix:** Install the Google Drive Backup (or Samba Backup) add-on during Phase 2 setup. Set it to run at 3am daily. You'll never think about it again until the day you need it.

→ See [Phase 7: Hardening](../phases/07-hardening.md#part-1-backups)

---

## Mistake 6: Editing `configuration.yaml` Without Validating

**What happens:** HA fails to restart after a YAML edit. You're left with an inaccessible HA instance and no obvious error message.

**Why it happens:** YAML is whitespace-sensitive and easy to break with an incorrect indent. A broken `configuration.yaml` prevents HA from starting.

**The fix:**
1. Always run **Settings → System → Check Configuration** before restarting
2. Use the HA file editor add-on (it shows YAML syntax errors)
3. If HA won't start: access the host via SSH, navigate to the config directory, and find the error in the logs: `ha core logs`

---

## Mistake 7: Using Unavailable Entities in Automations

**What happens:** Automations fire on `unavailable` states as if they were valid state changes. Lights turn on/off randomly. Presence automations trigger when a phone loses connectivity briefly.

**Why it happens:** `unavailable` is a valid state in HA. `state: "on"` → `state: "unavailable"` triggers any automation watching for state changes.

**The fix:** Add a condition to check the state isn't `unavailable`, or use the `not` state in triggers:

```yaml
trigger:
  - platform: state
    entity_id: binary_sensor.front_door
    to: "on"
    not_from:
      - "unavailable"
      - "unknown"
```

Or in conditions:
```yaml
condition:
  - condition: not
    conditions:
      - condition: state
        entity_id: binary_sensor.front_door
        state: "unavailable"
```

---

## Mistake 8: Presence Detection Based Only on Phone GPS

**What happens:** "Welcome home" automations fire late (phone GPS takes 30-90 seconds to update after you arrive). "Goodbye" automations misfire when your phone's GPS connection is lost indoors.

**Why it happens:** Phone GPS polling intervals and network availability create gaps in presence accuracy.

**The fix:** Use multiple presence signals combined:
- Phone GPS (companion app) — broad net
- BLE (ESPHome Bluetooth proxies around the home) — fast, accurate near-home detection
- WiFi connection to your router — secondary confirmation

Combine them with a Bayesian sensor for highest accuracy.

→ See [Phase 6: Advanced Features — Presence Detection](../phases/06-advanced-features.md#feature-3-presence-detection)

---

## Mistake 9: Exposing HA Directly to the Internet

**What happens:** Your HA instance gets hit by brute-force login attempts. If using a weak password, it gets compromised.

**Why it happens:** Port-forwarding 8123 directly to the internet is the naive way to enable remote access. Port scanners find open ports within hours.

**The fix:**
- Use **Nabu Casa** (the official $7/month remote access — properly secured and easiest)
- Or **Cloudflare Tunnel** (free, self-hosted, no port forwarding needed)
- Always enable **2FA** on your HA admin account
- Never expose port 8123 directly to the internet

→ See [Phase 7: Hardening — Remote Access](../phases/07-hardening.md#part-2-remote-access)

---

## Mistake 10: Buying Cheap Z-Wave Devices When Zigbee Was Sufficient

**What happens:** You spend 2-3x more on Z-Wave devices when Zigbee devices would have worked fine and been equally reliable.

**Why it happens:** Z-Wave's reputation for reliability makes it sound like the "serious" choice for everything.

**The fix:** Use Zigbee for most devices. Use Z-Wave specifically where sub-GHz range matters (thick walls, long distances) or for door locks and garage door openers where the higher certification bar matters. Don't default to Z-Wave for everything.

→ See [[protocol-selection.md|Protocol Selection]]

---

## Mistake 11: Naming Entities Poorly From the Start

**What happens:** After 50 devices, your automation list looks like: `binary_sensor.0x00158d0003498a7d`, `light.tradfri_bulb_e27_ws_806lm_6` — impossible to read or maintain.

**Why it happens:** HA auto-generates entity IDs from device names, and device names come from the integration (often ugly). Early users don't realize how permanent these become.

**The fix:** Rename devices and entities as you add them. Use a consistent naming convention from day one:

```
{room}_{device_type}_{qualifier}
# Examples:
sensor.kitchen_temperature
binary_sensor.front_door_contact
light.bedroom_ceiling
switch.office_plug_monitor
```

Rename entities: Settings → Devices → click the device → click the entity → rename.

---

## Mistake 12: Not Using Helpers for Shared Configuration

**What happens:** You have the motion-off delay hardcoded to 5 minutes in 15 different automations. You want to change it to 3 minutes and have to edit all 15 automations.

**Why it happens:** Beginners hardcode values that should be configurable.

**The fix:** Create an `input_number` helper for thresholds that appear in multiple automations:

```yaml
# Settings → Helpers → Add Helper → Number
input_number:
  motion_off_delay:
    name: "Motion Off Delay"
    min: 1
    max: 30
    step: 1
    initial: 5
    unit_of_measurement: minutes
    icon: mdi:timer
```

Then in automations:
```yaml
delay: "00:{{ states('input_number.motion_off_delay') | int }}:00"
```

Now you adjust the delay from one place — the dashboard — and all automations use it.

---

## Community-Sourced Process Pitfalls

> Added from community mining, 2026-03-12.
> Sources: r/homeassistant, community.home-assistant.io, GitHub issues.

### Never Update HA Without a Snapshot

**The pattern:** Users update HA → HACS integration breaks → they have no rollback path → spend 4+ hours debugging.

**The rule:** Before every HA update, take a snapshot (Settings → System → Backup → Create Backup). HA OS allows one-click rollback to the previous version from the backup. This is the #1 piece of advice from experienced users. Source: [Reddit r/homeassistant](https://www.reddit.com/r/homeassistant/comments/1i61v5c/how_to_deal_with_breaking_integrations_on_every/), Jan 2025.

### Read the Breaking Changes List Before Every Update

HA publishes a "Breaking Changes" section in every monthly release blog post at `home-assistant.io/blog`. Before updating, scan the list for:
- Integrations you use
- YAML keys you use (e.g., `service:` → `action:`, `trigger:` → `triggers:`)
- Device-specific entity renames (happens frequently with Zigbee2MQTT updates)

Source: [home-assistant.io release blog](https://www.home-assistant.io/blog/), monthly.

### Don't Update Z2M and HA at the Same Time

Updating Zigbee2MQTT and Home Assistant Core in the same maintenance window doubles the number of potential breaking changes and makes it impossible to isolate which update caused a problem. Best practice: update Z2M first, validate devices work, then update HA core separately. Source: community consensus, r/homeassistant.

### Put Your Config in Git

The most consistently recommended advanced practice across r/homeassistant, community.home-assistant.io, and HN. With git:
- `git diff` before/after shows exactly what changed during a breaking update
- You can roll back specific files without a full restore
- You can share automations and get help debugging

Minimum: `cd /config && git init && git add automations.yaml scripts.yaml configuration.yaml && git commit -m "initial"`. Source: [Hacker News](https://news.ycombinator.com/item?id=42813513), Jan 2025.

### Don't Buy Cloud-Only Devices for Critical Functions

Vendors can revoke API access at any time. Known cases:
- **Chamberlain/MyQ** (2023): revoked HA API access, integration removed
- **Mazda** (2023): DMCA takedown of third-party API tool
- **Generic Tuya cloud**: randomly requires re-authentication, tokens expire

For anything controlling physical security (locks, garage doors, alarms), use local-only protocols: Z-Wave, Zigbee, Thread/Matter, ESPHome, or LocalTuya with cloud blocked at the firewall. Source: [Hacker News](https://news.ycombinator.com/item?id=42813513), Jan 2025; [home-assistant.io/blog/2023/11/06/removal-of-myq-integration/](https://www.home-assistant.io/blog/2023/11/06/removal-of-myq-integration/).

### Don't Start With ZHA if You Have Aqara or "Picky" Zigbee Devices

ZHA is the built-in Zigbee integration but has worse device compatibility than Zigbee2MQTT for certain brands (Aqara in particular). The community first-line advice when ZHA devices randomly drop off: migrate to Z2M. However, migration requires re-pairing every device (the Zigbee mesh does not transfer between integrations). Starting with Z2M avoids this painful migration. Source: [XDA Developers](https://www.xda-developers.com/things-wish-knew-before-going-all-in-home-assistant/), Aug 2025; [Reddit community consensus](https://www.reddit.com/r/homeassistant/comments/1fpdp25/).

### Template Sensors Need `unique_id` for Stability

Template sensors in `configuration.yaml` without `unique_id:` will have unstable entity IDs — if a naming conflict occurs, HA appends `_2`, `_3`, etc., silently breaking automations. Always add a `unique_id:` (any unique string) to every template sensor. Source: [community.home-assistant.io](https://community.home-assistant.io/t/unique-id-for-template-sensor/596594), Jul 2023.

### Zigbee2MQTT 2.0 Migration Checklist

Before upgrading from Z2M 1.x to 2.0, add these to your `configuration.yaml` to minimize breaking changes:

```yaml
advanced:
  homeassistant_legacy_entity_attributes: false
  homeassistant_legacy_triggers: false
  legacy_api: false
  legacy_availability_payload: false
device_options:
  legacy: false
```

Also explicitly set `serial: { adapter: ezsp }` (or your adapter type). Missing the explicit adapter type causes "No valid USB adapter found" on first start. Source: [Z2M Discussion #24198](https://github.com/Koenkk/zigbee2mqtt/discussions/24198), Jan 2025.
