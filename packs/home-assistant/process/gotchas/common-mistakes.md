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

→ See [Protocol Selection](../decisions/protocol-selection.md)

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

→ See [Motion Lighting Pattern](../patterns/motion-lighting.md)

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

→ See [Protocol Selection](../decisions/protocol-selection.md)

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
