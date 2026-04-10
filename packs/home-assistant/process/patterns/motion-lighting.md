---
title: Motion-Activated Lighting — The Definitive Pattern
type: pattern
tags:
- pattern
- motion-lighting
- automation
- home-assistant-process
pack: home-assistant-process
retrieval_strategy: standard
id: home-assistant/process/patterns/motion-lighting
verified_at: '2026-04-10'
verified_by: agent
---
---
sources:
  - type: documentation
    url: "https://www.home-assistant.io/docs/automation/"
    date: "2026-03"
  - type: community
    url: "https://community.home-assistant.io/t/motion-activated-lighting-done-right/450032"
    date: "2025-06"
  - type: community
    url: "https://www.reddit.com/r/homeassistant/comments/1dgdpxe/tips_you_wished_you_knew/"
    date: "2024-06"
---

# Motion-Activated Lighting — The Definitive Pattern

> **Lead summary:** Motion-activated lighting is the first automation most people build and the one most people get wrong. The default `single` automation mode ignores re-triggers during the off-delay, so lights turn off while you're still in the room. The fix — `restart` mode — is simple, but real-world scenarios quickly get more complex: time-based brightness, occupied rooms without motion (TV watching), multi-sensor zones, pet filtering, and night mode. This workflow covers the complete pattern from basic to advanced.

## Why This Automation Breaks

The #1 beginner mistake with motion lighting is using the default automation mode. Here's what happens:

1. Motion detected → automation fires → light turns on → 5-minute delay starts → light turns off
2. During that 5-minute delay, you move again. The automation **tries to fire again**.
3. In `single` mode (the default), the new trigger is **silently ignored** because the automation is already running.
4. The original 5-minute timer expires. Light turns off. You're still in the room. You wave your arms.

**The fix:** Change automation mode to `restart`. Every new motion event restarts the entire automation from the top, resetting the off-delay timer.

## The Basic Pattern

```yaml
automation:
  - alias: "Living Room Motion Lights"
    mode: restart
    triggers:
      - trigger: state
        entity_id: binary_sensor.living_room_motion
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

This works for simple cases. But real homes need more.

## Time-Based Brightness (Adaptive Lighting)

You don't want 100% brightness at 2 AM when you stumble to the kitchen. Use a `choose` action to set brightness based on time of day:

```yaml
automation:
  - alias: "Kitchen Motion Lights - Adaptive"
    mode: restart
    triggers:
      - trigger: state
        entity_id: binary_sensor.kitchen_motion
        to: "on"
    actions:
      - choose:
          # Daytime: full brightness, cool white
          - conditions:
              - condition: time
                after: "07:00:00"
                before: "21:00:00"
            sequence:
              - action: light.turn_on
                target:
                  entity_id: light.kitchen
                data:
                  brightness_pct: 100
                  color_temp_kelvin: 4000
          # Evening: medium brightness, warm
          - conditions:
              - condition: time
                after: "21:00:00"
                before: "23:00:00"
            sequence:
              - action: light.turn_on
                target:
                  entity_id: light.kitchen
                data:
                  brightness_pct: 50
                  color_temp_kelvin: 2700
          # Night: minimal brightness, very warm
          - conditions:
              - condition: time
                after: "23:00:00"
                before: "07:00:00"
            sequence:
              - action: light.turn_on
                target:
                  entity_id: light.kitchen
                data:
                  brightness_pct: 10
                  color_temp_kelvin: 2200
      - delay: "00:05:00"
      - action: light.turn_off
        target:
          entity_id: light.kitchen
```

### The Adaptive Lighting Integration (Alternative)

The [Adaptive Lighting](https://github.com/basnijholt/adaptive-lighting) custom integration (HACS) handles this automatically — it adjusts brightness and color temperature throughout the day following your circadian rhythm. If you use it, your motion automation just calls `light.turn_on` without brightness/color data and Adaptive Lighting handles the rest.

## The "TV Watching" Problem

Scenario: You're watching TV in the living room. You stop moving. The motion sensor clears. The light turns off. You're sitting still in the dark.

**Solutions, ranked by reliability:**

### 1. Use mmWave presence sensor instead of (or alongside) PIR

mmWave sensors detect **static presence** — a person sitting still, breathing. PIR only detects movement. If you use an mmWave sensor as the trigger, it stays `on` as long as someone is in the room, even if perfectly still.

```yaml
triggers:
  - trigger: state
    entity_id: binary_sensor.living_room_presence  # mmWave sensor
    to: "on"
```

The off-delay is now handled by the mmWave sensor's own timeout (configurable, typically 30s-2min after the last detected presence), and your automation's delay stacks on top.

### 2. Check media player state as a condition

If the TV/media player is actively playing, don't turn off the light (or keep it at a dim level):

```yaml
automation:
  - alias: "Living Room Motion Lights - TV Aware"
    mode: restart
    triggers:
      - trigger: state
        entity_id: binary_sensor.living_room_motion
        to: "on"
    actions:
      - action: light.turn_on
        target:
          entity_id: light.living_room
      - delay: "00:05:00"
      # Don't turn off if TV is playing
      - condition: not
        conditions:
          - condition: state
            entity_id: media_player.living_room_tv
            state: "playing"
      - action: light.turn_off
        target:
          entity_id: light.living_room
```

### 3. Use an input_boolean as manual override

A toggle helper that lets someone press a button (physical or dashboard) to say "I'm still here, don't turn off the lights":

```yaml
automation:
  - alias: "Living Room Motion Lights - Override Aware"
    mode: restart
    triggers:
      - trigger: state
        entity_id: binary_sensor.living_room_motion
        to: "on"
    conditions:
      - condition: state
        entity_id: input_boolean.living_room_override
        state: "off"
    actions:
      - action: light.turn_on
        target:
          entity_id: light.living_room
      - delay: "00:10:00"
      - action: light.turn_off
        target:
          entity_id: light.living_room
```

## Multi-Sensor Rooms (PIR + mmWave)

The ideal combo: **PIR for fast initial detection** + **mmWave for sustained presence hold**.

PIR sensors trigger in <100ms (instant). mmWave sensors can take 1-3 seconds for initial detection. But mmWave holds presence while someone is sitting still. Combine them:

```yaml
automation:
  - alias: "Office Motion Lights - Dual Sensor"
    mode: restart
    triggers:
      # PIR for instant trigger
      - trigger: state
        entity_id: binary_sensor.office_pir_motion
        to: "on"
      # mmWave for sustained presence re-trigger
      - trigger: state
        entity_id: binary_sensor.office_mmwave_presence
        to: "on"
    actions:
      - action: light.turn_on
        target:
          entity_id: light.office
      - wait_for_trigger:
          # Wait until BOTH sensors are clear
          - trigger: template
            value_template: >
              {{ is_state('binary_sensor.office_pir_motion', 'off') and
                 is_state('binary_sensor.office_mmwave_presence', 'off') }}
        timeout: "01:00:00"
        continue_on_timeout: true
      - delay: "00:02:00"
      - action: light.turn_off
        target:
          entity_id: light.office
```

## Dealing with Pets

Pets trigger PIR sensors. Solutions:

**Sensor placement:** Mount PIR sensors at 6-7 feet (1.8-2.1m) angled downward. Most pets don't trigger sensors mounted above waist height. Ceiling-mounted PIR sensors are terrible for pet avoidance — they see everything.

**mmWave sensitivity tuning:** Some mmWave sensors (LD2410-based, Apollo) let you adjust sensitivity per distance gate. Reduce sensitivity at the lowest gates (0-1m from ground) to filter pets.

**Zone-based mmWave:** Sensors like the Aqara FP2 support detection zones. Create a zone that starts at 1m height to exclude floor-level movement.

**Realistic expectation:** No solution is perfect. A large dog on a couch will trigger any presence sensor. The goal is reducing false triggers from pets walking through, not eliminating all pet detection.

## Night Mode Pattern

For bathrooms and hallways at night — you want light, but minimal:

```yaml
automation:
  - alias: "Hallway Night Light"
    mode: restart
    triggers:
      - trigger: state
        entity_id: binary_sensor.hallway_motion
        to: "on"
    conditions:
      - condition: time
        after: "22:00:00"
        before: "06:00:00"
    actions:
      - action: light.turn_on
        target:
          entity_id: light.hallway
        data:
          brightness_pct: 5
          color_temp_kelvin: 2000  # Very warm, red-shifted
      - delay: "00:02:00"
      - action: light.turn_off
        target:
          entity_id: light.hallway
        data:
          transition: 5  # Gentle fade-out
```

**Pro tip:** Use `transition` on turn_off to fade out gradually. A sudden blackout at 3 AM is jarring; a 5-second fade is not.

## The "Someone Already Turned It On" Problem

If someone manually turned on the light (wall switch, voice command, dashboard), should the motion automation turn it off when motion clears? Usually **no** — that's infuriating.

**Pattern:** Only turn off lights that the automation turned on. Use a `trigger` variable or an `input_boolean` flag:

```yaml
automation:
  - alias: "Bedroom Motion Lights - Respect Manual"
    mode: restart
    triggers:
      - trigger: state
        entity_id: binary_sensor.bedroom_motion
        to: "on"
    conditions:
      # Only auto-turn-on if light is currently off
      - condition: state
        entity_id: light.bedroom
        state: "off"
    actions:
      # Flag that we turned it on
      - action: input_boolean.turn_on
        target:
          entity_id: input_boolean.bedroom_auto_light
      - action: light.turn_on
        target:
          entity_id: light.bedroom
      - delay: "00:10:00"
      # Only turn off if we were the ones who turned it on
      - condition: state
        entity_id: input_boolean.bedroom_auto_light
        state: "on"
      - action: light.turn_off
        target:
          entity_id: light.living_room
      - action: input_boolean.turn_off
        target:
          entity_id: input_boolean.bedroom_auto_light
```

## Blueprint Recommendations

If you don't want to write YAML, community blueprints handle most of these patterns:

- **[Motion-activated Light](https://community.home-assistant.io/t/wasp-in-a-box/)** — "Wasp in a Box" blueprint, the community gold standard for motion lighting with occupancy awareness
- **[Adaptive Lighting + Motion](https://github.com/basnijholt/adaptive-lighting)** — Pairs with the Adaptive Lighting integration
- Built-in blueprints: Settings → Automations → Blueprints → Import from community

<!-- refresh
  decay: slow-moving
  as_of: 2026-Q1
  fields: [blueprint_names, blueprint_urls]
  source: https://community.home-assistant.io/c/blueprints-exchange/53
  method: "Blueprint popularity shifts. Check the Blueprints Exchange category on the HA community forum."
-->

## Related

- Automation Fundamentals — Triggers, conditions, actions, modes
- Presence Detection — Multi-sensor presence for room-level awareness
- Dashboard Design — Creating override toggles and status indicators
