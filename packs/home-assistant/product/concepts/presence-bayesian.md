---
title: "Bayesian Presence Sensor"
type: concept
tags:
  - presence-detection
  - bayesian
  - binary-sensor
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/presence-bayesian
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - presence-person-home.md
  - presence-sensor-fusion.md
  - presence-pitfalls.md
content_hash: sha256:546ef8189057e748851cdd831f5df4e9edb1c8e74459376e4127b44ea5f309c1
---
# Bayesian Presence Sensor

The Bayesian binary sensor combines multiple uncertain signals into a probability-based home/away verdict. You set a prior and per-observation `prob_given_true` / `prob_given_false`; the sensor turns `on` when probability crosses the threshold.

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

## Related Concepts

- [[presence-person-home.md|presence person home]]
- [[presence-sensor-fusion.md|presence sensor fusion]]
- [[presence-pitfalls.md|presence pitfalls]]

Sources: [Bayesian integration](https://www.home-assistant.io/integrations/bayesian/).
