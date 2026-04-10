---
title: Home Security Monitoring with Home Assistant
type: pattern
tags:
- pattern
- security
- monitoring
- automation
- home-assistant-process
pack: home-assistant-process
retrieval_strategy: standard
id: home-assistant/process/patterns/security-monitoring
verified_at: '2026-04-10'
verified_by: agent
---
---
sources:
  - type: documentation
    url: "https://www.home-assistant.io/integrations/alarmo/"
    date: "2026-03"
  - type: documentation
    url: "https://frigate.video/docs/"
    date: "2026-03"
  - type: community
    url: "https://community.home-assistant.io/t/frigate-nvr-complete-guide/553204"
    date: "2025-11"
  - type: community
    url: "https://community.home-assistant.io/t/alarmo-custom-alarm-system-megathread/424789"
    date: "2025-09"
---

# Home Security Monitoring with Home Assistant

> **Lead summary:** Home Assistant can serve as a legitimate home security system — not just notifications when things happen, but a full alarm system with zones, delays, arming modes, and siren control. The key components are Alarmo (custom alarm panel), Frigate (local AI camera NVR), and a solid sensor strategy. The advantage over commercial systems is total local control, no monthly fees, and deep integration with the rest of your automations. The tradeoff is setup complexity and self-managed reliability — if you're on vacation and HA goes down, so does your monitoring.

## Alarmo: A Full Alarm System in HA

[Alarmo](https://github.com/nielsfaber/alarmo) (HACS custom integration) implements a proper alarm panel directly in Home Assistant. It adds:

- Multiple arming modes: **Away** (full security), **Home** (perimeter only), **Night** (partial), **Custom** (user-defined)
- **Entry delay:** 30-60 seconds to disarm before the alarm triggers (siren sounds)
- **Exit delay:** Time to leave after arming before sensors become active
- **Zones:** Group sensors logically — perimeter zone (instant trigger), interior zone (delayed trigger)
- **Sensor bypass:** Temporarily ignore a specific sensor (leave bedroom window open on a hot night without triggering the alarm)
- **Siren control:** Trigger a switch/siren entity when alarm activates
- **Code input:** Require a PIN to arm/disarm from the dashboard or keypad
- **NFC tag support:** Tap a tag at the door to arm/disarm
- **Notifications:** Push alerts at every state change

### Setting Up Alarmo

Install via HACS → Alarmo → configure through the Alarmo panel (appears in your sidebar).

**Basic sensor configuration:**
```
Alarm sensors to add:
  - binary_sensor.front_door_contact          → Entry/Exit zone
  - binary_sensor.back_door_contact           → Entry/Exit zone  
  - binary_sensor.living_room_window_left     → Perimeter zone (instant)
  - binary_sensor.living_room_window_right    → Perimeter zone (instant)
  - binary_sensor.living_room_motion          → Interior zone (only in Away mode)
  - binary_sensor.kitchen_motion              → Interior zone (only in Away mode)
```

**Recommended zone strategy:**
- **Perimeter sensors** (doors/windows): Active in all arming modes. Trigger immediately.
- **Interior sensors** (motion): Only active in Away mode (you'd trigger them yourself if home). Set a 30-second entry delay on doors so you can disarm before interior sensors fire.
- **Smoke/CO sensors:** Always active regardless of arming mode.

### Automation Triggers from Alarmo

The `alarmo_event` custom event fires on every Alarmo state change:

```yaml
automation:
  - alias: "Alarm Triggered - Lights On + Notify"
    triggers:
      - trigger: state
        entity_id: alarm_control_panel.alarmo
        to: "triggered"
    actions:
      # Flash all lights to alert mode
      - action: light.turn_on
        target:
          entity_id: all
        data:
          brightness_pct: 100
          color_name: red
          flash: short
      # Send critical alert (bypasses phone silent mode)
      - action: notify.mobile_app_brians_phone
        data:
          title: "🚨 ALARM TRIGGERED"
          message: "Home alarm activated — check cameras"
          data:
            push:
              sound: default
              interruption-level: critical  # iOS critical alert
            tag: alarm_triggered
            channel: alarm        # Android high-priority channel
```

### NFC Tag Arm/Disarm

Place NFC stickers near your door. Tap to arm when leaving, tap to disarm when arriving:

```yaml
automation:
  - alias: "NFC Tag - Front Door Arm/Disarm"
    triggers:
      - trigger: tag
        tag_id: "nfc-front-door-keypad"  # Get tag ID from Developer Tools → Events after first scan
    actions:
      - choose:
          # If armed → disarm
          - conditions:
              - condition: not
                conditions:
                  - condition: state
                    entity_id: alarm_control_panel.alarmo
                    state: "disarmed"
            sequence:
              - action: alarmo.disarm
                data:
                  entity_id: alarm_control_panel.alarmo
                  code: !secret alarm_code
          # If disarmed → arm away
          - conditions:
              - condition: state
                entity_id: alarm_control_panel.alarmo
                state: "disarmed"
            sequence:
              - action: alarmo.arm
                data:
                  entity_id: alarm_control_panel.alarmo
                  mode: away
                  code: !secret alarm_code
```

## Door and Window Sensor Patterns

### Front Door Left Open Alert

```yaml
automation:
  - alias: "Front Door Left Open"
    mode: single
    triggers:
      - trigger: state
        entity_id: binary_sensor.front_door_contact
        to: "on"     # Open
        for: "00:05:00"  # 5 minutes
    actions:
      - action: notify.mobile_app_brians_phone
        data:
          title: "🚪 Front door left open"
          message: "Front door has been open for 5 minutes"
          data:
            tag: front_door_open
            actions:
              - action: DISMISS_DOOR_ALERT
                title: "OK, I know"

  # Cancel notification when door closes
  - alias: "Front Door Closed - Dismiss Alert"
    triggers:
      - trigger: state
        entity_id: binary_sensor.front_door_contact
        to: "off"
    actions:
      - action: notify.mobile_app_brians_phone
        data:
          message: clear_notification
          data:
            tag: front_door_open
```

### Dashboard: Open Windows/Doors Summary

Instead of individual notifications for each sensor, a template binary_sensor summarizes all open sensors:

```yaml
template:
  - binary_sensor:
      - name: "Any Window Open"
        unique_id: any_window_open
        device_class: window
        state: >
          {{ expand('group.window_sensors') 
             | selectattr('state', 'eq', 'on') 
             | list | count > 0 }}
        attributes:
          open_windows: >
            {{ expand('group.window_sensors') 
               | selectattr('state', 'eq', 'on') 
               | map(attribute='name') 
               | list | join(', ') }}
```

Add this to your dashboard as a conditional card — visible only when windows are open, showing which ones.

## Frigate: Local AI Camera NVR

[Frigate](https://frigate.video) is a locally-running NVR (Network Video Recorder) with real-time object detection. It's the standard for serious HA camera integration.

**What Frigate does:**
- Stores camera streams locally (to your HA SSD or NAS)
- Performs AI-based object detection (person, car, dog, cat, bicycle, package)
- Defines configurable zones per camera ("if person detected in driveway zone, trigger")
- Exposes binary sensors, image snapshots, and video clips to HA
- Motion-triggered recording (saves storage vs continuous recording)
- Sub-stream support (record high-res, detect on low-res stream simultaneously)

**Hardware requirements for Frigate:**
- Processing camera streams is CPU-intensive. An N100 mini-PC handles ~4-8 cameras with object detection on CPU.
- **Google Coral TPU** (~$60, USB Accelerator version): offloads ML inference entirely. With a Coral, an N100 handles 20+ cameras. This is the recommended setup.
- **Intel iGPU (QSV):** Frigate 0.14+ supports Intel Quick Sync for hardware video decoding. Dramatically reduces CPU load for stream processing.
- Pi 4: can handle 1-2 cameras without a Coral, but struggles with more. With Coral USB: 4-6 cameras.

### Frigate Configuration

```yaml
# frigate.yml (Frigate add-on config)
mqtt:
  host: 192.168.1.10  # Your MQTT broker
  
cameras:
  front_door:
    ffmpeg:
      inputs:
        - path: rtsp://admin:password@192.168.30.10:554/stream1   # High-res for recording
          roles:
            - record
        - path: rtsp://admin:password@192.168.30.10:554/stream2   # Low-res for detection
          roles:
            - detect
    detect:
      width: 1280
      height: 720
      fps: 5          # 5fps is enough for detection, saves CPU
    record:
      enabled: true
      retain:
        days: 7       # Keep recordings 7 days
      events:
        retain:
          default: 14  # Keep event clips 14 days
    snapshots:
      enabled: true
      bounding_box: true  # Draw box around detected objects
    zones:
      driveway:
        coordinates: 50,450,730,450,730,720,50,720  # Polygon coordinates
      front_path:
        coordinates: 730,350,1280,350,1280,720,730,720
    
detectors:
  coral:
    type: edgetpu
    device: usb  # USB Coral TPU

objects:
  track:
    - person
    - car
    - dog
    - cat
    - package
  filters:
    person:
      min_area: 5000      # Filter out tiny detections (birds, etc.)
      min_score: 0.7      # 70% confidence minimum
```

### Frigate HA Integration

The [Frigate HA integration](https://github.com/blakeblackshear/frigate-hass-integration) (HACS) adds:
- `binary_sensor.front_door_motion` — motion detected
- `binary_sensor.front_door_person` — person detected
- `image.front_door_person` — latest person snapshot
- `sensor.front_door_person_count` — current person count in frame
- Camera entities for each stream

### Notification with Camera Snapshot

```yaml
automation:
  - alias: "Person at Front Door — Notify with Snapshot"
    mode: single
    triggers:
      - trigger: state
        entity_id: binary_sensor.front_door_person
        to: "on"
    conditions:
      # Only notify when not home (or use for all detections in away mode)
      - condition: state
        entity_id: binary_sensor.anyone_home
        state: "off"
    actions:
      # Wait briefly for Frigate to process a good snapshot
      - delay:
          seconds: 2
      - action: notify.mobile_app_brians_phone
        data:
          title: "👤 Person detected — Front Door"
          message: "Motion at {{ now().strftime('%I:%M %p') }}"
          data:
            image: /api/frigate/notifications/{{ trigger.id }}/snapshot.jpg
            # Or use local Frigate URL:
            # image: "http://frigate.local:5000/api/front_door/latest.jpg"
            tag: frigate_front_door
            actions:
              - action: URI
                title: "View Camera"
                uri: /lovelace/cameras
```

## Escalating Notification Pattern

Simple motion alerts suffer from alert fatigue. An escalating pattern sends a notification only when multiple conditions align:

```yaml
automation:
  - alias: "Motion Escalation Pattern"
    mode: restart
    triggers:
      - trigger: state
        entity_id: binary_sensor.driveway_person
        to: "on"
    actions:
      # Step 1: Log the detection (no notification yet)
      - variables:
          detection_time: "{{ now() }}"
      
      # Wait 30 seconds — if someone recognized arrives, cancel
      - wait_for_trigger:
          - trigger: state
            entity_id: binary_sensor.anyone_home
            to: "on"
        timeout: "00:00:30"
      
      # If someone arrived home → was expected, skip notification
      - condition: template
        value_template: "{{ wait.trigger is none }}"  # No arrival during wait
      
      # Check if motion is still active (not just a brief passing car)
      - condition: state
        entity_id: binary_sensor.driveway_person
        state: "on"
      
      # Nobody home, still motion → this is suspicious
      - action: notify.mobile_app_brians_phone
        data:
          title: "⚠️ Unrecognized person in driveway"
          message: "No family member arrived, but person still detected"
          data:
            image: "http://frigate.local:5000/api/front_door/latest.jpg"
            push:
              sound: default
              interruption-level: time-sensitive
```

## Lighting as Security Deterrent

When away, random light patterns discourage burglars better than lights-always-on (which looks obviously automated):

```yaml
automation:
  - alias: "Away Mode Occupancy Simulation"
    mode: restart
    triggers:
      - trigger: state
        entity_id: alarm_control_panel.alarmo
        to: "armed_away"
    actions:
      - repeat:
          while:
            - condition: state
              entity_id: alarm_control_panel.alarmo
              state: "armed_away"
          sequence:
            # Randomize which light and for how long
            - variables:
                random_light: >
                  {% set lights = ['light.living_room', 'light.kitchen', 'light.bedroom'] %}
                  {{ lights | random }}
                random_duration: "{{ range(10, 45) | random }}"  # 10-45 minutes
            - action: light.turn_on
              target:
                entity_id: "{{ random_light }}"
              data:
                brightness_pct: "{{ range(30, 80) | random }}"
                color_temp_kelvin: "{{ range(2700, 4000) | random }}"
            - delay:
                minutes: "{{ random_duration }}"
            - action: light.turn_off
              target:
                entity_id: "{{ random_light }}"
            - delay:
                minutes: "{{ range(5, 20) | random }}"
```

Only run during evening hours (sunset to midnight) — a light turning on at 3 AM is itself suspicious.

## Smart Locks: Auto-Lock and Guest Codes

Zigbee and Z-Wave locks integrate fully with HA for auto-lock, code management, and access logs.

**Popular lock integrations:**
- **Schlage BE469 / BE489 (Z-Wave):** Best-in-class Z-Wave locks. Full code management via HA.
- **Yale Assure / August Smart Lock:** WiFi or Z-Wave. August has a native HA integration.
- **Ultraloq U-Bolt (Z-Wave):** Good fingerprint + Z-Wave combo. Well-supported.
- **Nuki Smart Lock:** Zigbee or WiFi, European market, excellent HA integration.

### Auto-Lock After Timeout

```yaml
automation:
  - alias: "Auto-Lock Front Door"
    mode: single
    triggers:
      - trigger: state
        entity_id: lock.front_door
        to: "unlocked"
        for: "00:05:00"  # Unlocked for 5 minutes
    conditions:
      # Don't lock if the door is still open
      - condition: state
        entity_id: binary_sensor.front_door_contact
        state: "off"  # Door is closed
    actions:
      - action: lock.lock
        target:
          entity_id: lock.front_door
```

### Lock Jammed / Battery Low Alerts

```yaml
automation:
  - alias: "Front Door Lock Battery Low"
    triggers:
      - trigger: numeric_state
        entity_id: sensor.front_door_lock_battery
        below: 20
    actions:
      - action: notify.mobile_app_brians_phone
        data:
          title: "🔋 Front door lock battery low"
          message: "Battery at {{ states('sensor.front_door_lock_battery') }}% — replace soon"
```

## Privacy Considerations

A home security setup should protect privacy as rigorously as it provides security.

### Don't Record When Family Is Home

Interior cameras should not record when family members are home — it's surveillance of your own household:

```yaml
automation:
  - alias: "Disable Interior Cameras When Home"
    triggers:
      - trigger: state
        entity_id: binary_sensor.anyone_home
        to: "on"
    actions:
      - action: switch.turn_off
        target:
          entity_id:
            - switch.frigate_living_room_recording
            - switch.frigate_hallway_recording
  
  - alias: "Enable Interior Cameras When Away"
    triggers:
      - trigger: state
        entity_id: binary_sensor.anyone_home
        to: "off"
        for: "00:05:00"
    actions:
      - action: switch.turn_on
        target:
          entity_id:
            - switch.frigate_living_room_recording
            - switch.frigate_hallway_recording
```

**In Frigate:** You can toggle recording per camera via MQTT or the Frigate API. The Frigate HA integration exposes these as switches.

### Exterior Cameras Only by Default

The best practice for privacy: exterior cameras (driveway, front door, backyard) can record continuously. Interior cameras (if you install them at all) should be on the "enabled in away mode only" pattern above.

**Consider:** Do you actually need interior cameras? Door/window sensors + exterior cameras + Alarmo cover 90% of security scenarios without interior surveillance.

### Data Retention

Define explicit retention policies in Frigate:
```yaml
record:
  retain:
    days: 7       # General recordings: 7 days then deleted
  events:
    retain:
      default: 14  # Event clips: 14 days
      objects:
        person: 30  # Person events kept 30 days
```

Don't keep years of footage unless you have specific reasons — it's storage burden and a data liability.

## Related

- Presence Detection — The "anyone home" signal that drives security mode
- [[notification-patterns.md|Notification Patterns]] — Advanced notification delivery with camera snapshots and action buttons
- Network Architecture — Camera VLAN, NVR placement, no cloud routing
