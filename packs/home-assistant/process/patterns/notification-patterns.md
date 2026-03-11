---
sources:
  - type: documentation
    url: "https://www.home-assistant.io/integrations/mobile_app/"
    date: "2026-03"
  - type: documentation
    url: "https://companion.home-assistant.io/docs/notifications/notifications-basic"
    date: "2026-03"
  - type: documentation
    url: "https://www.home-assistant.io/integrations/alert/"
    date: "2026-03"
  - type: community
    url: "https://community.home-assistant.io/t/actionable-notifications-guide/360120"
    date: "2025-04"
---

# Smart Notification Patterns — Beyond "Send Me a Message"

> **Lead summary:** The default HA notification experience is "something happened, here's a message." But smart notifications are contextual, actionable, throttled, and routed to the right person. This workflow covers actionable notifications (buttons that trigger automations), critical alerts that bypass DND, throttling to prevent notification storms, rich media (camera snapshots), and persistent alerts that nag until acknowledged. The difference between a useful smart home and an annoying one is notification design.

## The Notification Landscape

Home Assistant has multiple notification paths:

| Method | Best For | Limitations |
|--------|----------|-------------|
| **Companion App** (notify.mobile_app_*) | Primary personal notifications | Requires app installed, platform-specific |
| **Persistent Notifications** | Admin alerts on HA dashboard | Only visible in HA UI, easy to miss |
| **Telegram Bot** | Cross-platform, rich media, actionable | Requires Telegram account + bot setup |
| **Email** (SMTP/Sendgrid) | Detailed alerts, logs, digests | Slow, not real-time |
| **Discord** | Household/group notifications | Requires Discord server |
| **Alexa/Google TTS** | Immediate voice announcements | No persistent record, can be annoying |
| **Alert integration** | Persistent repeating alerts until ack'd | Nags until you deal with it |

## Basic Companion App Notification

```yaml
actions:
  - action: notify.mobile_app_brians_iphone
    data:
      title: "Garage Door Open"
      message: "The garage door has been open for 10 minutes."
```

**Android vs iOS differences that matter:**

- **Android** supports `channel` for notification categorization (different sounds/vibration per channel)
- **iOS** supports `push.sound` for custom sounds, and has stricter background limits
- Both support `data.image` for rich notifications, but URL requirements differ
- **iOS** critical alerts require a one-time permission grant separate from regular notifications

## Actionable Notifications (Buttons)

The killer feature. Send a notification with buttons that trigger automations when tapped.

### iOS Pattern

```yaml
automation:
  - alias: "Garage Door Alert with Actions"
    triggers:
      - trigger: state
        entity_id: cover.garage_door
        to: "open"
        for: "00:10:00"
    actions:
      - action: notify.mobile_app_brians_iphone
        data:
          title: "🚗 Garage Door Open"
          message: "Open for 10 minutes. Close it?"
          data:
            actions:
              - action: "CLOSE_GARAGE"
                title: "Close It"
                destructive: true
              - action: "IGNORE_GARAGE"
                title: "Leave It"

  - alias: "Handle Garage Close Action"
    triggers:
      - trigger: event
        event_type: mobile_app_notification_action
        event_data:
          action: "CLOSE_GARAGE"
    actions:
      - action: cover.close_cover
        target:
          entity_id: cover.garage_door
      - action: notify.mobile_app_brians_iphone
        data:
          message: "✅ Garage door closing."
```

### Android Pattern

```yaml
# Android uses a slightly different structure
actions:
  - action: notify.mobile_app_brians_pixel
    data:
      title: "🚗 Garage Door Open"
      message: "Open for 10 minutes. Close it?"
      data:
        actions:
          - action: "CLOSE_GARAGE"
            title: "Close It"
          - action: "IGNORE_GARAGE"
            title: "Leave It"
```

The response handler automation is identical for both platforms — it listens for the `mobile_app_notification_action` event.

**Key insight:** Action identifiers (like `CLOSE_GARAGE`) must be UPPERCASE on iOS. Android is case-insensitive. Just use UPPERCASE for both.

## Critical Notifications (Bypass DND)

For security alerts, water leaks, smoke detectors — notifications that MUST get through even at 3 AM:

### iOS Critical Alert

```yaml
actions:
  - action: notify.mobile_app_brians_iphone
    data:
      title: "🚨 WATER LEAK DETECTED"
      message: "Water sensor in the basement triggered!"
      data:
        push:
          sound:
            name: "default"
            critical: 1
            volume: 1.0
```

**iOS requirement:** The user must explicitly grant "Critical Alerts" permission for the HA companion app in iOS Settings → Notifications → Home Assistant → Critical Alerts. This is a separate toggle from regular notifications. The app will prompt for it on first critical alert, but it's best to set it up proactively.

### Android High Priority

```yaml
actions:
  - action: notify.mobile_app_brians_pixel
    data:
      title: "🚨 WATER LEAK DETECTED"
      message: "Water sensor in the basement triggered!"
      data:
        priority: high
        channel: "security_alerts"
        importance: high
        vibrationPattern: "100, 1000, 100, 1000, 100"
        ledColor: "red"
```

**Android tip:** Create a dedicated notification channel (e.g., `security_alerts`) with DND override in the Android system notification settings. Then target that channel in your critical notifications.

## Notification Throttling

Without throttling, a flapping sensor can send 50 notifications in an hour. There are several patterns to prevent this:

### Pattern 1: input_datetime Cooldown

```yaml
automation:
  - alias: "Temperature Alert (Throttled)"
    triggers:
      - trigger: numeric_state
        entity_id: sensor.server_room_temperature
        above: 85
    conditions:
      # Only fire if last alert was more than 30 minutes ago
      - condition: template
        value_template: >
          {{ (now() - states('input_datetime.last_temp_alert') | as_datetime).total_seconds() > 1800 }}
    actions:
      - action: notify.mobile_app_brians_iphone
        data:
          title: "🌡️ Server Room Hot"
          message: "Temperature: {{ states('sensor.server_room_temperature') }}°F"
      # Record the alert time
      - action: input_datetime.set_datetime
        target:
          entity_id: input_datetime.last_temp_alert
        data:
          datetime: "{{ now().strftime('%Y-%m-%d %H:%M:%S') }}"
```

### Pattern 2: Timer-Based Suppression

```yaml
automation:
  - alias: "Motion Alert (Timer Throttle)"
    triggers:
      - trigger: state
        entity_id: binary_sensor.backyard_motion
        to: "on"
    conditions:
      # Only alert if the throttle timer isn't running
      - condition: state
        entity_id: timer.motion_alert_cooldown
        state: "idle"
    actions:
      - action: notify.mobile_app_brians_iphone
        data:
          title: "🏃 Backyard Motion"
          message: "Motion detected in the backyard."
      # Start 15-minute cooldown
      - action: timer.start
        target:
          entity_id: timer.motion_alert_cooldown
        data:
          duration: "00:15:00"
```

### Pattern 3: Daily Digest Instead of Real-Time

For non-urgent things (daily energy usage, sensor battery levels), send a single daily digest instead of individual notifications:

```yaml
automation:
  - alias: "Daily Smart Home Digest"
    triggers:
      - trigger: time
        at: "08:00:00"
    actions:
      - action: notify.mobile_app_brians_iphone
        data:
          title: "📊 Daily Smart Home Report"
          message: >
            🔋 Low batteries:
            {% for state in states.sensor
              | selectattr('attributes.device_class', 'defined')
              | selectattr('attributes.device_class', 'eq', 'battery')
              | selectattr('state', 'is_number')
              | rejectattr('state', 'eq', 'unavailable') %}
              {% if state.state | int < 20 %}
            • {{ state.name }}: {{ state.state }}%
              {% endif %}
            {% endfor %}

            🌡️ Climate: {{ states('sensor.outdoor_temperature') }}°F outside
            ⚡ Energy: {{ states('sensor.daily_energy_usage') }} kWh yesterday
```

## Rich Notifications (Camera Snapshots)

Send a camera snapshot with your notification — invaluable for motion alerts:

```yaml
automation:
  - alias: "Front Door Motion with Snapshot"
    triggers:
      - trigger: state
        entity_id: binary_sensor.front_door_motion
        to: "on"
    actions:
      # Capture snapshot
      - action: camera.snapshot
        target:
          entity_id: camera.front_door
        data:
          filename: "/config/www/snapshots/front_door_latest.jpg"
      # Small delay to ensure file is written
      - delay: "00:00:01"
      # Send with image
      - action: notify.mobile_app_brians_iphone
        data:
          title: "🚪 Front Door Motion"
          message: "Someone is at the front door."
          data:
            image: "/local/snapshots/front_door_latest.jpg"
```

**Important:** The image path in the notification uses `/local/` which maps to `/config/www/` on the HA filesystem. The `camera.snapshot` action writes to the filesystem path; the notification references the web-accessible path.

**Tip for Frigate/camera users:** If you use Frigate, you can include the detection snapshot directly via `data.image: "/api/frigate/notifications/{{trigger.payload_json['after']['id']}}/snapshot.jpg"` for real-time object-detection-cropped images.

## Multi-Person Routing

Send notifications to the right person based on context:

```yaml
automation:
  - alias: "Package Delivered - Notify Whoever is Home"
    triggers:
      - trigger: state
        entity_id: binary_sensor.front_door_package
        to: "on"
    actions:
      - choose:
          # Brian is home → notify Brian
          - conditions:
              - condition: state
                entity_id: person.brian
                state: "home"
            sequence:
              - action: notify.mobile_app_brians_iphone
                data:
                  title: "📦 Package Delivered"
                  message: "A package was delivered to the front door."
          # Sarah is home → notify Sarah
          - conditions:
              - condition: state
                entity_id: person.sarah
                state: "home"
            sequence:
              - action: notify.mobile_app_sarahs_phone
                data:
                  title: "📦 Package Delivered"
                  message: "A package was delivered to the front door."
        # Nobody home → notify both
        default:
          - action: notify.notify  # notify group
            data:
              title: "📦 Package Delivered"
              message: "A package was delivered to the front door. Nobody's home!"
```

**Tip:** Create a `notify` group to avoid repeating multi-target logic:

```yaml
# configuration.yaml
notify:
  - name: household
    platform: group
    services:
      - action: mobile_app_brians_iphone
      - action: mobile_app_sarahs_phone
```

Then use `notify.household` to reach everyone at once.

## The Alert Integration — Persistent Nags

For critical issues that need human action (not just awareness), the `alert` integration re-sends notifications at intervals until acknowledged:

```yaml
# configuration.yaml
alert:
  garage_door:
    name: "Garage Door Open"
    entity_id: cover.garage_door
    state: "open"
    repeat:
      - 15    # First reminder after 15 minutes
      - 30    # Then every 30 minutes
      - 60    # Then every hour
    can_acknowledge: true
    skip_first: true  # Don't alert immediately — give time to close it normally
    notifiers:
      - mobile_app_brians_iphone
    title: "🚗 Garage Door Still Open"
    message: "The garage door has been open since {{ states.cover.garage_door.last_changed | as_local }}."

  water_leak:
    name: "Water Leak"
    entity_id: binary_sensor.basement_water_leak
    state: "on"
    repeat: 5  # Every 5 minutes — this is urgent
    can_acknowledge: true
    skip_first: false  # Alert immediately
    notifiers:
      - mobile_app_brians_iphone
      - mobile_app_sarahs_phone
    title: "🚨 WATER LEAK"
    message: "Water detected in the basement! Check immediately."
    data:
      push:
        sound:
          name: "default"
          critical: 1
          volume: 1.0
```

**Key feature:** The alert creates an entity (`alert.garage_door`) that can be acknowledged via automation, dashboard button, or actionable notification — stopping the repeat cycle.

## Voice Announcements (TTS)

For immediate household awareness without requiring phones:

```yaml
automation:
  - alias: "Announce Doorbell"
    triggers:
      - trigger: state
        entity_id: binary_sensor.doorbell
        to: "on"
    conditions:
      # Don't announce late at night
      - condition: time
        after: "08:00:00"
        before: "22:00:00"
    actions:
      - action: tts.speak
        target:
          entity_id: tts.google_en_com
        data:
          media_player_entity_id: media_player.living_room_speaker
          message: "Someone is at the front door."
```

**Combine with visual:** Send a companion app notification with camera snapshot AND do a TTS announcement. The notification persists for later review; the TTS gets immediate attention.

## Notification Design Principles

1. **Title should be scannable.** Use emoji + short description. You should know what it's about without opening it.
2. **Include actionable information.** "Garage open" is less useful than "Garage open for 15 minutes — 42°F outside."
3. **Offer actions when possible.** A "Close It" button beats having to open the app, navigate to the entity, and tap close.
4. **Throttle everything.** If a notification can fire more than once per hour, it needs a cooldown.
5. **Route to the right person.** The person who can act on it, not everyone.
6. **Reserve critical alerts for actual emergencies.** Water leaks, security breaches, smoke detectors. If everything is critical, nothing is.
7. **Batch low-priority info into digests.** Daily battery report > 15 individual "battery low" alerts.

## Related

- [Automation Fundamentals](../concepts/automation-fundamentals.md) — Triggers, conditions, actions
- [Presence Detection](../concepts/presence-detection.md) — Route notifications based on who's home
- [Diagnostic Guide](../troubleshooting/diagnostic-guide.md) — Debugging notification delivery issues
