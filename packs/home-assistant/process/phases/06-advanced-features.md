# Phase 6: Advanced Features

## Goal

Add the three features that transform a basic smart home into something genuinely impressive: **voice control** (local, no cloud required), **energy monitoring** (understand what's drawing power), and **presence detection** (automations that know when people are actually home, not just assumed to be).

## Prerequisites

- Phase 5 complete (stable automations, dashboards built)
- Automations have been running reliably for 2+ weeks
- You're comfortable editing YAML

---

## Feature 1: Voice Assistant (Local Assist)

Home Assistant's built-in voice pipeline (**Assist**) runs entirely locally — no data leaves your home. It can trigger automations, control devices, set timers, and answer questions about your home's state.

### Architecture

```
Wake word → Speech-to-Text (STT) → Natural Language Processing (NLP) → Action → Text-to-Speech (TTS) → Response
```

Each component can be local (preferred) or cloud-based (faster, requires Nabu Casa subscription).

### Option A: Local Wake Word + Local STT (Recommended)

**What you need:**
- An ESP32-S3 dev board with a microphone (e.g., ATOM Echo, M5Stack ATOM Echo S3, or any ESP32 with I2S mic)
- ESPHome installed (Settings → Add-ons → ESPHome)

**Setup:**
1. Install the **Wyoming** integration (Settings → Devices & Services → Add Integration → Wyoming Protocol)
2. Install the **Whisper** add-on for local STT (Settings → Add-ons → Whisper)
3. Install the **openWakeWord** add-on for wake word detection
4. Install the **Piper** add-on for local TTS
5. Flash your ESP32 device with ESPHome's voice assistant config
6. Create an **Assist Pipeline**: Settings → Voice Assistants → Add Assistant
   - STT: Whisper (local)
   - TTS: Piper (local)
   - Wake word: openWakeWord

**Performance note:** Whisper (large-v3 model) is quite accurate but requires ~1.5-2GB RAM and a modern CPU for acceptable latency. On a Pi 4, use the `tiny` or `base` model. On a mini-PC with 8GB RAM, use `medium` or `large`.

### Option B: Cloud Assist (Easiest)

With a **Nabu Casa** subscription ($7/month), you get cloud-based STT/TTS with better accuracy and faster response:
- Settings → Voice Assistants → Add Assistant → Use Cloud
- Works with Google Home speakers and Amazon Alexa via the Nabu Casa cloud

### Testing Voice Commands

Open the Assist dialog (click the microphone icon in HA header) and try:
```
"Turn on the living room lights"
"Set the bedroom temperature to 68 degrees"
"What's the temperature outside?"
"Is the front door locked?"
"Turn off all the lights"
```

If a command doesn't work, check the **Assist debug** view to see how the utterance was interpreted.

### Custom Sentences (Local NLP)

Add custom commands for things Assist doesn't know by default:

```yaml
# config/custom_sentences/en/custom.yaml
language: "en"
intents:
  ActivateScene:
    data:
      - sentences:
          - "activate (movie|cinema) mode"
          - "set up for movie night"
    action:
      scene: scene.movie_mode
```

---

## Feature 2: Energy Monitoring

HA's Energy Dashboard tracks electricity consumption, solar production, battery storage, and gas/water usage in real time and historically.

### What You Need

To see energy data, you need **energy monitoring at some level**:

| Option | Granularity | Cost | Best For |
|--------|------------|------|----------|
| Smart plugs with power monitoring | Per-device | $10-30/plug | Individual appliances |
| Smart circuit breakers (e.g., Emporia Vue 2) | Per-circuit | $130-200 | Whole-home circuit-level |
| Utility smart meter integration (e.g., Sense) | Whole-home | $300+ | Passive monitoring |
| Solar inverter integration (SolarEdge, Enphase, Fronius) | Production + grid | Varies | Solar owners |

**Minimum to get the Energy Dashboard working:**
- One entity with `device_class: energy` and unit `kWh` reporting total consumption
- Emporia Vue 2 + HA integration is the best price/value for circuit-level monitoring

### Setting Up the Energy Dashboard

1. Settings → Energy → Configure
2. Add your energy grid sensor (Consumption from grid)
3. Add solar production sensor (if applicable)
4. Add individual device sensors (smart plugs with energy monitoring)
5. The dashboard populates within an hour

### Template Sensor for Cost Calculation

If your utility uses time-of-use pricing:

```yaml
template:
  - sensor:
      - name: "Electricity Cost Rate"
        unit_of_measurement: "$/kWh"
        state: >
          {% set hour = now().hour %}
          {% if 7 <= hour < 22 %}
            0.18
          {% else %}
            0.09
          {% endif %}
```

---

## Feature 3: Presence Detection

Automations that say "when you come home" are only reliable if presence detection is reliable. The companion app's GPS is a good start but has gaps. The best presence detection uses **multiple signals combined**.

### Detection Methods by Reliability

| Method | Reliability | Latency | False Positives | Setup |
|--------|------------|---------|----------------|-------|
| Phone GPS (companion app) | High | 5-30s | Low | Easy |
| Phone WiFi connection | Medium | 10-60s | Medium | Easy |
| Ping (device IP) | Medium | 30s | High (phone sleeps) | Easy |
| Bluetooth LE (ESPHome proxies) | High | 3-10s | Very low | Medium |
| mmWave radar (e.g., LD2410) | Highest | <1s | Very low | Medium |
| Bayesian probability model | Highest | Varies | Lowest | Hard |

### Strategy 1: Companion App + BLE Proxies (Best Mobile Presence)

ESP32 devices flashed with ESPHome's Bluetooth Proxy firmware detect your phone's Bluetooth LE signal. Multiple proxies placed around the house create a coverage net.

**ESPHome Bluetooth Proxy config:**
```yaml
bluetooth_proxy:
  active: true
```

Add 3-4 proxies ($5-10 ESP32 boards) throughout your home. HA's Bluetooth integration then detects your phone (by MAC address) as a presence signal.

**In automations:**
```yaml
trigger:
  - platform: state
    entity_id: device_tracker.my_phone
    to: "home"
```

### Strategy 2: Bayesian Presence Sensor (Most Accurate)

Combines multiple signals into a probabilistic presence estimate. More setup, but far fewer false "away" states when your phone's GPS lags.

```yaml
binary_sensor:
  - platform: bayesian
    name: "Brian Home"
    prior: 0.7
    probability_threshold: 0.9
    observations:
      - entity_id: device_tracker.brian_phone
        prob_given_true: 0.95
        prob_given_false: 0.1
        platform: state
        to_state: "home"
      - entity_id: binary_sensor.brian_ble_home
        prob_given_true: 0.9
        prob_given_false: 0.15
        platform: state
        to_state: "on"
      - entity_id: binary_sensor.living_room_motion
        prob_given_true: 0.7
        prob_given_false: 0.3
        platform: state
        to_state: "on"
```

### Zones

HA's **Zones** feature creates geographic areas (home, work, school, gym) that device trackers use for presence context.

1. Settings → Areas & Zones → Zones → Add Zone
2. Set a radius (typically 100-200m for home)
3. Your phone shows `home` when within the radius, and the zone name when at the other locations

**Use zones in automations:**
```yaml
# Trigger when leaving work (start preheating home)
trigger:
  - platform: zone
    entity_id: device_tracker.my_phone
    zone: zone.work
    event: leave
```

---

## Checklist

- [ ] Voice assistant configured (local or Nabu Casa)
- [ ] At least 5 basic voice commands working
- [ ] Energy monitoring: at least one whole-home sensor in the Energy Dashboard
- [ ] Individual smart plugs added to energy tracking for high-draw appliances
- [ ] Presence detection using at least two methods per person
- [ ] Bayesian sensor (or equivalent) reduces false "away" states
- [ ] Zones configured for home and at least one other location (work)
- [ ] "Welcome home" automation works reliably 9/10 times

## What's Next

→ [Phase 7: Hardening](07-hardening.md) — Backups, security, remote access, and long-term monitoring
