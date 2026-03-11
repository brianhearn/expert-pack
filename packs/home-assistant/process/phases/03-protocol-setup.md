# Phase 3: Protocol Setup

## Goal

Get your Zigbee (or Z-Wave) coordinator running, pair your first batch of devices, and verify they're stable before building automations on top of them. Unstable devices make everything downstream unreliable.

## Prerequisites

- Phase 2 complete (HA running with companion app)
- USB coordinator dongle on hand
- At least 4-6 smart devices to pair (bulbs, plugs, or sensors)
- (Optional) USB extension cable — keeps dongle away from Pi USB 3.0 ports

---

## Step 1: Position Your Coordinator

The Zigbee/Z-Wave coordinator is a USB dongle plugged into your HA server. Where and how you plug it in matters.

**Always use a USB 2.0 extension cable (20-30cm):** The USB 3.0 ports on a Raspberry Pi or mini-PC emit RF interference on the 2.4GHz band that Zigbee uses. A short USB 2.0 extension cable physically separates the dongle from the interference source. This is one of the most common "why is my Zigbee flaky?" gotchas.

**Position the dongle centrally:** The coordinator is the root of your Zigbee mesh. More central placement means better initial reach. As you add mains-powered devices (bulbs, plugs), they become mesh repeaters and coverage expands.

---

## Step 2: Install Zigbee2MQTT (Recommended)

There are two ways to manage Zigbee in HA:
- **ZHA (Zigbee Home Automation)** — built-in, easier setup, good for beginners
- **Zigbee2MQTT** — more powerful, broader device support, more control

**Recommendation: Zigbee2MQTT** — it supports more devices, gives you more diagnostic information, and is the community standard. The extra setup time is worth it.

### Install Mosquitto (MQTT Broker) First

Zigbee2MQTT communicates via MQTT. Install the Mosquitto broker add-on first:

1. **Settings → Add-ons → Add-on Store → Mosquitto broker**
2. Install, then start it
3. Go to **Settings → Devices & Services** — Mosquitto will auto-create an MQTT integration
4. The integration auto-configures using your HA user credentials

### Install Zigbee2MQTT

1. In the Add-on Store, search for **Zigbee2MQTT** (may need HACS or the third-party repository)
   - Add the Zigbee2MQTT repository: `https://github.com/zigbee2mqtt/hassio-zigbee2mqtt`
2. Install the add-on
3. Before starting: configure the serial port in the add-on configuration
   ```yaml
   serial:
     port: /dev/ttyUSB0  # or /dev/ttyACM0 — check which appears when dongle is connected
   ```
4. Start the add-on and open the Web UI
5. You should see "Zigbee2MQTT started" in the logs

**Finding your dongle's serial port:**

```bash
# In the HA Terminal add-on:
ls /dev/ttyUSB* /dev/ttyACM*
```

Typical values:
- SONOFF Dongle Plus (CH340): `/dev/ttyUSB0`
- SMLIGHT SLZB-07 (CP2102): `/dev/ttyUSB0`
- Aeotec Z-Stick 7: `/dev/ttyACM0`

---

## Step 3: Pair Your First Devices

### Pairing Mode in Zigbee2MQTT

1. Open the Zigbee2MQTT web UI
2. Click **Permit join (All)** — this opens a 255-second pairing window
3. Put your device in pairing mode (varies by device — usually hold the reset button or cycle power 3x)
4. Watch the Z2M log — you should see the device join and be identified
5. The device appears in HA within 30 seconds

### Pairing Order Matters for Mesh

Add mains-powered devices (plugs, bulbs) before battery-powered sensors. Mains devices act as mesh repeaters — the more you have, the better your coverage for battery devices.

**Good pairing order:**
1. Smart plugs (2-4) — establish the mesh backbone
2. Smart bulbs (if any) — more mesh nodes
3. Door/window sensors
4. Motion sensors
5. Temperature/humidity sensors

### Device Naming Strategy

Name devices systematically from the start — renaming later is painful when automations reference the old names.

**Good naming convention:**
```
{room}_{device_type}_{qualifier?}
# Examples:
living_room_motion
bedroom_temperature
kitchen_plug_kettle
front_door_contact
```

In HA, go to the device page and rename both the device and all its entities using this convention.

---

## Step 4: Verify Stability

Before building automations, let your devices run for 24-48 hours and check stability.

### What to Check

**In Zigbee2MQTT Dashboard:**
- All devices show "Online" status
- LQI (Link Quality Indicator) > 100 for most devices (200+ is excellent; < 50 means check placement)
- No devices showing frequent offline/online transitions (a sign of weak signal or interference)

**In HA:**
- Go to **Settings → Devices & Services → Zigbee2MQTT** and verify all entities have recent state updates
- Check **Settings → System → Logs** for Zigbee-related errors

### Common Stability Issues

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Device pairs but immediately goes offline | Out of Zigbee range | Move device closer or add a repeater plug between it and the coordinator |
| Device shows "unavailable" in HA | MQTT connection issue | Check Mosquitto add-on is running; check Z2M logs |
| Coordinator not found | Wrong serial port | Check `/dev/ttyUSB*` — port number can change on reboot |
| Devices flaky after HA restart | Serial port changed | Set `port: /dev/serial/by-id/{your-dongle-id}` in Z2M config for stable identification |

**Set a stable serial port by-id:**

```bash
ls -la /dev/serial/by-id/
```

This shows persistent device IDs like `usb-ITead_Sonoff_Zigbee_3.0_USB_Dongle_Plus_...`. Use this path in Z2M config — it won't change across reboots.

---

## Step 5: Organize into Areas

HA's **Areas** feature groups devices by room, which makes dashboards and automations much cleaner.

1. Go to **Settings → Areas & Zones → Add Area** for each room
2. Go to each device and assign it to an area
3. Set the area on the device itself (not just the entity) — it propagates to all entities

Areas unlock:
- "Turn off all lights in the bedroom" in automations
- Room-based dashboards
- Voice commands like "Hey Google, turn off the kitchen"

---

## Checklist

- [ ] Coordinator dongle plugged in with USB extension cable
- [ ] Zigbee2MQTT (or ZHA) installed and running
- [ ] Mosquitto MQTT broker installed and running
- [ ] First 6+ devices paired and named
- [ ] All devices online and stable for 24+ hours
- [ ] Serial port set to `/dev/serial/by-id/...` for stability
- [ ] Devices assigned to Areas
- [ ] LQI checked for battery-powered sensors (>100)

## What's Next

→ [Phase 4: Automation Building](04-automation-building.md) — Build your first automations on a stable device foundation
