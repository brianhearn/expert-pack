---
title: Presence Detection — The Hardest Problem in Home Automation
type: concept
tags:
- automation-fundamentals
- concepts
- esphome-fundamentals
- presence-detection
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/presence-detection
verified_at: "2026-04-21"
verified_by: agent
schema_version: "4.1"
concept_scope: single
---
<!-- context: section=concepts, topic=presence-detection, related=esphome-fundamentals,automation-fundamentals -->
---
sources:
  - type: documentation
    url: "https://www.home-assistant.io/integrations/bayesian/"
    date: "2026-03"
  - type: documentation
    url: "https://www.home-assistant.io/integrations/bluetooth/"
    date: "2026-03"
  - type: community
    url: "https://community.home-assistant.io/t/presence-detection-megathread/580060"
    date: "2025-12"
  - type: community
    url: "https://www.reddit.com/r/homeassistant/comments/1b2z8w9/presence_detection_the_definitive_guide/"
    date: "2025-08"
---

# Presence Detection — The Hardest Problem in Home Automation

> **Lead summary:** Presence detection is the single most impactful capability in home automation — and the one most systems get wrong. A system that knows who's home and who isn't can automatically arm/disarm security, adjust HVAC, control lighting, and gate hundreds of other automations. Phone-only tracking is unreliable for roughly 40% of households due to battery optimization, OS restrictions, and non-technical family members. The winning strategy is **multi-sensor fusion**: combine phone tracking + WiFi router detection + Bluetooth proximity + mmWave radar at the room level + door sensor logic into a unified presence model that degrades gracefully when individual sensors fail.

## Why Phone-Based Tracking Alone Fails

The HA Companion app (Android/iOS) is the most common presence sensor — it reports GPS location and can detect home/away transitions. But in practice, it fails more than people expect:

**Android battery optimization** is the #1 killer. Android aggressively kills background apps to save battery, and the HA companion app is frequently killed — especially on Samsung, Xiaomi, Huawei, and OnePlus devices. The phone appears "home" or "away" based on the last reported state before the process was killed, not its actual current location.

**iOS background refresh limits** cause delayed updates. Apple limits apps to ~30-minute background refresh cycles. A person who leaves at 7:15 AM may not appear "away" in HA until 7:45 AM. This means automations that trigger "when person leaves" can fire 30 minutes late.

**GPS drift in urban areas** is a real problem. Apartment buildings, shopping centers, and downtown areas see GPS errors of 50-200 meters. A home zone radius of 100m means false away/home triggers several times per week in dense areas. Increasing zone radius helps but reduces resolution.

**Family members who don't use the companion app.** Partners, teenagers, and elderly relatives rarely maintain the app correctly. Battery saver mode gets toggled on. The app gets force-stopped. Some family members simply refuse to install it.

**Network transitions.** When a phone switches from WiFi to mobile data (walking to the car), some integrations interpret this as "left home" before GPS confirms the departure, causing phantom departures.

## The Multi-Sensor Fusion Strategy

The reliable pattern is not "better phone tracking" — it's **defense in depth**: multiple independent sensors that each contribute evidence for or against presence, fused into a single confident verdict.

```
┌─────────────────────────────────────────────────────┐
│              Person: "Brian Home?" State             │
├──────────────┬──────────────┬───────────────────────┤
│  Phone GPS   │ WiFi Device  │  Bluetooth Proxy      │
│  (coarse,    │  Tracker     │  (room-level,         │
│   delayed)   │  (fast, LAN) │   requires BLE)       │
├──────────────┴──────────────┴───────────────────────┤
│    mmWave Radar (room-level, no false negatives)     │
│    Door Contact Sensors (edge detection)             │
└─────────────────────────────────────────────────────┘
```

Each layer has different strengths and failure modes. Combined, the false negative/positive rate drops dramatically.

### Layer 1: Companion App (Phone GPS + WiFi)

Still valuable as a layer, especially for the "definitely left home" signal. Works best when:
- User has disabled battery optimization for the HA app (see below)
- Zone radius is set to 250-500m to compensate for GPS drift
- "WiFi router integration" augments it (below)

**Android: Disable battery optimization for HA Companion:**
Settings → Apps → Home Assistant → Battery → Unrestricted (not "Optimized")
This step is mandatory on Samsung/Xiaomi/OnePlus. Otherwise the app will be killed within 30-60 minutes.

**iOS: Background App Refresh:**
Settings → Home Assistant → Background App Refresh: ON
Also: Settings → Privacy → Location Services → Home Assistant → Always (not "While Using")

### Layer 2: WiFi Router Device Tracking

Most modern routers (and dedicated integrations like UniFi, FritzBox, eero, GL.iNet) can report which devices are connected to the network. If your phone's MAC address is on the WiFi network, you're home. If it drops off, you've likely left.

**Advantages:**
- Faster than GPS (responds in seconds, not minutes)
- Works for family members who have the WiFi password but not the companion app
- Doesn't depend on app being awake

**Disadvantages:**
- MAC randomization (iOS 14+, Android 10+) rotates MAC addresses, making tracking unreliable unless you reserve a static MAC in the companion app or router
- Brief WiFi disconnections (elevator, moving room to room) cause false "away" signals

**Fix for MAC randomization:** The HA companion app can be configured to report a consistent network identifier. Alternatively, use ping-based detection (device_tracker.ping) against the DHCP reservation IP.

### Layer 3: Bluetooth Proximity via ESPHome BLE Proxy

This is the most underutilized layer and one of the most powerful for room-level presence. ESP32 devices running ESPHome can act as BLE (Bluetooth Low Energy) scanners, detecting the BLE advertisements from phones and BLE tags.

**Setup:**
1. Flash ESP32 with ESPHome (one per room or area)
2. Enable `bluetooth_proxy` component in ESPHome YAML
3. In HA, the ESP32 appears as a Bluetooth proxy — it extends BLE range throughout the house
4. Use the `bluetooth_tracker` integration or the `iBeacon` integration to track BLE-enabled devices

```yaml
# ESPHome BLE proxy configuration
bluetooth_proxy:
  active: true

esp32_ble_tracker:
  scan_parameters:
    active: true
    interval: 1100ms
    window: 1100ms
```

**Practical reality:** Phone BLE is not always discoverable (screen off, power save). Works better with dedicated BLE tags (like Nut mini, Tile, or Apple AirTags via OpenHAB... no — use ESPresense for this pattern). **ESPresense** is a purpose-built firmware for ESP32 that specializes in BLE room-level detection. It tracks specific BLE devices (phone, watch, earbuds) per room.

### Layer 4: mmWave Radar (Room-Level, Foolproof)

mmWave sensors detect micro-motion — breathing, heartbeat, even stillness — making them impervious to the "person sitting still watching TV" false negative that defeats PIR sensors. They are the ground truth at room level.

**2025-2026 mmWave Recommendations:**

| Sensor | Price | Connection | Range | Best For |
|--------|-------|-----------|-------|----------|
| **Apollo MSR-1 / AIR-1** | ~$25-30 | ESPHome (USB-C) | 5-6m | Wired, DIY, best customization |
| **Apollo R PRO-1** | ~$35 | ESPHome (USB-C) | 8m | Best wired option, LD2450 chip for zone detection |
| **Aqara FP300** | ~$35-45 | Zigbee | 5m | Best battery-powered option, official Zigbee |
| **Aqara FP2** | ~$50 | WiFi (HomeKit/HA) | 5m | Reliable, multi-zone (5 zones), well-supported |
| **Sonoff SNZB-06P** | ~$12-15 | Zigbee | 4m | Best budget option, simple binary detection |
| **Tuya mmWave sensors** | ~$10 | WiFi/Zigbee | 4-5m | Inconsistent quality — verify model before buying |

**Apollo series (Apollo Automation)** are popular because they run ESPHome natively and the community firmware exposes all LD2410/LD2450 parameters directly in HA. You can tune sensitivity zones, detection angles, and timeouts from the HA UI.

**Aqara FP300** (released 2024-2025) is the best option for rental situations or anywhere you can't run wiring — USB-C battery-powered, Zigbee, and surprisingly accurate. The main limitation is battery life (~2-3 months depending on activity).

**Sonoff SNZB-06P** is the budget king — $12-15, Zigbee, works with ZHA and Zigbee2MQTT, provides reliable binary occupied/clear detection (not zone-level). For rooms where you just need "occupied or not", this is excellent value.

### Layer 5: Door Contact Sensors as Edge Detectors

Door sensors don't track presence directly, but they provide hard evidence: if the front door opened and no one was detected inside, someone left. If it opened and phone GPS went from "away" to "home" coordinates, someone arrived. Door sensors catch arrivals/departures faster than any other method.

**Pattern:** Use door sensor state change + tracker state as a cross-check:
```yaml
# If front door opens AND all person trackers are "not_home" → someone arrived
trigger:
  - trigger: state
    entity_id: binary_sensor.front_door_contact
    to: "on"
condition:
  - condition: state
    entity_id: person.brian
    state: "not_home"
action:
  - action: input_boolean.turn_on
    target:
      entity_id: input_boolean.possible_arrival_brian
```

## The Bayesian Binary Sensor — Probabilistic Presence Fusion

The **Bayesian binary sensor** (`binary_sensor` platform) is HA's built-in way to combine multiple uncertain signals into a probability-based verdict. It uses Bayes' theorem to update a probability estimate as each piece of evidence arrives.

**How it works:**
- You define a prior probability (how likely is the person home at baseline?)
- Each observation updates the probability upward (evidence for presence) or downward (evidence against)
- The sensor outputs `on` (home) when probability exceeds a configurable threshold

**Worked example — Brian's home presence:**

```yaml
binary_sensor:
  - platform: bayesian
    name: "Brian Home"
    unique_id: bayesian_brian_home
    prior: 0.6  # Brian is home 60% of the time on average
    probability_threshold: 0.9  # Require 90% confidence before "home"
    observations:
      # Strong evidence FOR home: phone on home WiFi
      - platform: state
        entity_id: device_tracker.brians_phone_wifi
        to_state: "home"
        prob_given_true: 0.95   # If Brian is home, 95% chance phone is on WiFi
        prob_given_false: 0.05  # If Brian is NOT home, 5% chance phone still on WiFi
      
      # Strong evidence FOR home: companion app says home
      - platform: state
        entity_id: person.brian
        to_state: "home"
        prob_given_true: 0.92
        prob_given_false: 0.04
      
      # Medium evidence FOR home: mmWave detected in living room
      - platform: state
        entity_id: binary_sensor.living_room_mmwave_occupancy
        to_state: "on"
        prob_given_true: 0.8
        prob_given_false: 0.1   # Pet could trigger this too
      
      # Weak evidence FOR home: Bluetooth proximity detected
      - platform: state
        entity_id: device_tracker.brians_phone_ble
        to_state: "home"
        prob_given_true: 0.75
        prob_given_false: 0.15
      
      # Evidence AGAINST home: door sensor opened, GPS shows away
      - platform: state
        entity_id: binary_sensor.front_door_contact
        to_state: "off"
        prob_given_true: 0.05   # If Brian IS home, front door is closed most of the time
        prob_given_false: 0.85
```

**Tuning the Bayesian sensor:**

The `probability_threshold` is your confidence requirement. At 0.9, the sensor requires very strong evidence before declaring someone home — fewer false positives but slower to detect arrivals. At 0.7, you'll get faster arrival detection but more false positives.

`prob_given_true` / `prob_given_false` require observation and calibration. Start with conservative estimates, then check the sensor's probability attribute over time to understand how it's behaving:

```yaml
# Check in Developer Tools → States:
# binary_sensor.brian_home attributes includes 'probability' — monitor this value
```

## Home-Level vs Room-Level Presence

These are two different problems with different solutions:

| | Home-Level | Room-Level |
|---|---|---|
| **Question** | Is anyone home? Is Brian home? | Which room is Brian in? |
| **Sensors** | Phone GPS, WiFi, door sensors | mmWave, BLE proximity, PIR |
| **Complexity** | Medium | High |
| **Use case** | HVAC, security, welcome automations | Motion lighting, TV automation, specific room scenes |
| **Reliability needed** | High (seconds matter) | High (false positives annoying) |

**Most HA users should solve home-level presence first**, then add room-level only for specific automations where it adds real value (like adjusting lighting when moving between rooms).

**Room-level approach:** One mmWave per room (for high-value automations) + ESPresense BLE proxies (ESP32 per room) for identity-aware room tracking. The combination lets you answer: "Brian is in the living room right now."

## The WAF Problem

WAF (Wife/Partner/Family Acceptance Factor) is real. Your presence detection system is only as good as its weakest sensor — and if family members:
- Disable Bluetooth because it drains battery
- Turn off WiFi tracking because "it's creepy"
- Remove the companion app after a phone restart
- Use battery saver mode that kills background apps

...your system will continuously mark them as "not home" and automate against them.

**Practical solutions:**

1. **Don't make "all home" automations depend on all-family tracking.** A system that needs 100% tracker reliability is fragile. Design automations that degrade gracefully.

2. **Use mmWave for "anyone home" detection.** If a mmWave sensor is running in the main living area, you know *someone* is home — even without knowing who. Use this as a fallback.

3. **Input boolean manual override.** Create a `guest mode` or `occupied` input boolean that family members can toggle manually. Show it prominently on the dashboard.

4. **For family members who won't cooperate:** Set their person entity to require only one signal (WiFi presence is the most passive — they don't have to do anything, just have their phone connected to home WiFi).

## Template Sensor: Unified "Person Home" State

Combine multiple imperfect trackers into one reliable sensor:

```yaml
template:
  - binary_sensor:
      - name: "Brian Home Reliable"
        unique_id: brian_home_reliable
        device_class: presence
        delay_off: "00:05:00"  # Don't flip to 'away' until 5 minutes of no evidence
        state: >
          {% set phone_home = is_state('person.brian', 'home') %}
          {% set wifi_home = is_state('device_tracker.brians_phone_wifi', 'home') %}
          {% set ble_home = is_state('device_tracker.brians_phone_ble', 'home') %}
          {% set mmwave_active = is_state('binary_sensor.living_room_mmwave', 'on') %}
          
          {# Require at least 2 of 4 signals, OR Bayesian is high confidence #}
          {% set signal_count = [phone_home, wifi_home, ble_home, mmwave_active] | select('true') | list | count %}
          {% set bayesian_home = is_state('binary_sensor.brian_home_bayesian', 'on') %}
          
          {{ signal_count >= 2 or bayesian_home }}
        availability: >
          {{ not is_unavailable('person.brian') }}
```

**Key detail:** The `delay_off` attribute on the template binary_sensor means the sensor stays "on" (home) for 5 minutes after the conditions stop being true. This prevents the lights going off just because your phone briefly dropped WiFi when walking from the living room to the kitchen.

## Common Pitfalls Summary

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Android battery optimization | Person stays "home" all day | Set HA app to Unrestricted battery mode |
| iOS Background Refresh off | Delayed arrival/departure (30+ min) | Enable Background App Refresh + Always location |
| MAC randomization | WiFi tracker stops working | Reserve static DHCP / enable consistent MAC in companion app |
| Single tracker dependency | Too many false away triggers | Implement multi-sensor fusion + delay_off |
| mmWave sensitivity too low | Occupied room shows clear | Increase sensitivity in ESPHome / Zigbee2MQTT config |
| mmWave sensitivity too high | Empty room shows occupied | Reduce far-zone sensitivity, check for air vents |
| No delay_off on template sensor | Lights flash off mid-room | Add `delay_off: "00:05:00"` to template sensor |
| Bayesian threshold too high | Slow arrival detection | Lower threshold to 0.75-0.85 |

## Related

- [[esphome-fundamentals.md|ESPHome Fundamentals]] — Building BLE proxies and mmWave sensors with ESP32
- [[automation-fundamentals.md|Automation Fundamentals]] — Using presence in triggers and conditions
- Motion Lighting Workflow — Room-level presence applied to lighting

---

## Community-Sourced Presence Detection Gotchas

> Appended from community mining, 2026-03-12. Sources: r/homeassistant, community.home-assistant.io.

- **WiFi-only presence detection is fundamentally unreliable.** Modern phones randomize MAC addresses (especially iPhones on iOS 14+) which breaks all router-based and nmap-based tracking unless you: (a) use the HA Companion App which can report consistent MAC in HA settings, or (b) configure your router to assign static IPs based on device hostname. MAC randomization is on by default on Android 10+ and iOS 14+. Source: [Reddit r/homeassistant](https://www.reddit.com/r/homeassistant/comments/13sfzns/), May 2023.

- **nmap tracker marks phones "away" as soon as they drop WiFi ping** — which happens frequently when a phone's screen is off (power-saving suppresses WiFi activity). This creates "ghost away" events. Use nmap ONLY as one signal in a Bayesian/multi-source fusion model, never as the sole trigger for security or HVAC automations. Source: [Reddit r/homeassistant](https://www.reddit.com/r/homeassistant/comments/gbenma/), May 2020.

- **HA 2025.11 breaking change: person entity state now uses zone friendly name instead of zone object ID.** Automations that trigger on `state: 'zone_object_id'` silently break. Update automations to use zone friendly name (e.g., `state: 'Home'` instead of `state: 'home'`). Source: [home-assistant.io blog 2025.11](https://rc.home-assistant.io/blog/2025/10/02/release-202511/), Oct 2025.

- **Companion app presence stops updating on Android after phone restart** if battery optimization is re-enabled by Android itself (common after OS updates). Fix: check Settings → Apps → Home Assistant → Battery → set to "Unrestricted" after every major Android update. Source: community.home-assistant.io, recurring thread.
