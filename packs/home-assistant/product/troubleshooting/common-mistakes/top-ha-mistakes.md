---
title: Top Home Assistant Mistakes
type: troubleshooting
tags:
- automation-fundamentals
- backup-migration
- protocols
- top-ha-mistakes
- troubleshooting
pack: home-assistant-product
retrieval_strategy: atomic
---
<!-- context: section=troubleshooting, topic=top-ha-mistakes, related=protocols,automation-fundamentals,backup-migration -->
# Top Home Assistant Mistakes

## 1. Using WiFi for Everything

### Symptom
Devices randomly go offline, automations are unreliable, router struggles under load.

### The Mistake
Buying 40+ WiFi smart devices because "they don't need a hub." WiFi IoT devices congest your network, most depend on cloud servers, and they consume more power than mesh alternatives.

### The Fix
Transition critical devices to Zigbee or Z-Wave. Keep WiFi only for high-bandwidth devices (cameras) and devices that don't exist in other protocols. A Zigbee coordinator (USB dongle) costs $20-30.

### How to Avoid
Start with Zigbee as your default protocol. See [[protocols.md|Protocols]].

---

## 2. Wrong Automation Mode for Motion Lights

### Symptom
Motion-activated lights turn off while you're still in the room. The timer runs out even though you moved again.

### The Mistake
Using the default `single` automation mode. When the automation is running (waiting for the off-delay timer), new motion triggers are ignored.

### The Fix
Change the automation mode to `restart`. Every new motion event restarts the off-delay timer from zero.

```yaml
automation:
  mode: restart
  triggers:
    - trigger: state
      entity_id: binary_sensor.motion_living_room
      to: "on"
  actions:
    - action: light.turn_on
      target:
        entity_id: light.living_room
    - delay: "00:05:00"
    - action: light.turn_off
      target:
        entity_id: light.living_room
```

### How to Avoid
Always ask: "What should happen if this automation triggers while it's already running?" Choose the mode deliberately. See [Automation Fundamentals](../../concepts/automation-fundamentals.md#automation-modes).

---

## 3. Using device_id Instead of entity_id

### Symptom
Automation breaks after re-pairing a device, replacing hardware, or migrating Zigbee coordinators. The device_id (a hash) no longer matches.

### The Mistake
Creating automations via the UI's device trigger picker, which inserts opaque device_id references.

### The Fix
Edit the automation YAML and replace `device_id` references with `entity_id` references. Entity IDs are human-readable and stable.

### How to Avoid
After creating automations via the UI, check the YAML view and convert device_id to entity_id. Name your entities deliberately and consistently.

---

## 4. Not Setting Up Backups

### Symptom
SD card corrupts (common with Raspberry Pi), system update breaks something, or you accidentally delete a critical automation. Everything is lost.

### The Mistake
Running HA for months without configuring backups.

### The Fix
- HA OS/Supervised: Settings → System → Backups → Create Backup
- Set up automatic backups (weekly minimum)
- Store backups OFF the HA device (Google Drive add-on, Samba share, etc.)

### How to Avoid
Set up automated backups in the first week. The Google Drive Backup add-on is free and handles it automatically.

---

## 5. Overcomplicating YAML When the UI Works

### Symptom
Spending hours writing YAML for something the UI handles in clicks. YAML typos cause HA to fail to start.

### The Mistake
Assumption that "real" HA users do everything in YAML. The UI has improved dramatically — most automations, scenes, and integrations are easier to set up via the UI.

### The Fix
Use the UI for standard automations and integrations. Reserve YAML for: template sensors, complex automations that need direct YAML editing, packages for organizing large configs, and integrations that require YAML.

### How to Avoid
Try the UI first. Drop to YAML when you hit the UI's limitations, not before.

---

## 6. Running HA on an SD Card Long-Term

### Symptom
System corruption, database errors, HA becoming unresponsive. SD cards have limited write cycles and HA writes constantly (state changes, database, logs).

### The Mistake
Running HA OS on a Raspberry Pi with an SD card as the only storage.

### The Fix
- Best: Move to an SSD (USB boot on Pi 4/5, or use a mini-PC like N100)
- Acceptable: Move the database and logs to a USB drive or NAS, keep the SD card for OS only
- Minimum: Use a high-endurance SD card (Samsung PRO Endurance)

### How to Avoid
If starting fresh, use a mini-PC (Intel N100-based are popular — silent, low power, SSD) or a Raspberry Pi with USB-attached SSD.

---

## 7. Ignoring Entity Naming Conventions

### Symptom
As your system grows, you can't find anything. Entity IDs are a mess of manufacturer defaults like `light.0x00158d0001a2b3c4_light` or duplicates.

### The Mistake
Accepting default entity names from integrations without renaming them.

### The Fix
Rename entities consistently. Common pattern: `domain.area_function`
- `light.kitchen_ceiling`
- `sensor.bedroom_temperature`
- `binary_sensor.front_door_contact`
- `switch.garage_opener`

### How to Avoid
Rename every entity when you first add a device. Establish your naming convention before you have 200 entities. Include the area and the function. Be consistent.

---

## 8. Not Using Areas and Labels

### Symptom
Dashboard is a flat list of entities. Automations target entities one by one instead of by room. Voice commands don't work well because HA can't map "turn off the bedroom lights" to the right entities.

### The Mistake
Never assigning devices to Areas. This blocks: area-based dashboard cards, area targets in automations/scripts, natural voice control, and floor plan views.

### The Fix
Go to Settings → Areas → create areas for every room/zone. Assign every device to its area. Then you can target areas in automations:

```yaml
actions:
  - action: light.turn_off
    target:
      area_id: bedroom
```

### How to Avoid
Create areas and assign devices from day one. It takes minutes and saves hours later.
