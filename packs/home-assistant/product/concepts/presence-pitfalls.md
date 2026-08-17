---
title: "Presence Detection Pitfalls"
type: concept
tags:
  - presence-detection
  - gotchas
  - mac-randomization
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/presence-pitfalls
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - presence-phone-limits.md
  - presence-bayesian.md
  - presence-sensor-fusion.md
content_hash: sha256:daeb2d660f63ee5e4a03587924ca2e20cc99a161b7e6d4c78d329504fd5679a5
---
# Presence Detection Pitfalls

Most presence failures are the same handful of mistakes: Android battery optimization, iOS background refresh off, MAC randomization, a single tracker with no `delay_off`, and mmWave sensitivity set too high or too low. Community reports add nmap ghost-aways and the 2025.11 person-zone name change.

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

## Community-Sourced Presence Detection Gotchas

> Appended from community mining, 2026-03-12. Sources: r/homeassistant, community.home-assistant.io.

- **WiFi-only presence detection is fundamentally unreliable.** Modern phones randomize MAC addresses (especially iPhones on iOS 14+) which breaks all router-based and nmap-based tracking unless you: (a) use the HA Companion App which can report consistent MAC in HA settings, or (b) configure your router to assign static IPs based on device hostname. MAC randomization is on by default on Android 10+ and iOS 14+. Source: [Reddit r/homeassistant](https://www.reddit.com/r/homeassistant/comments/13sfzns/), May 2023.

- **nmap tracker marks phones "away" as soon as they drop WiFi ping** — which happens frequently when a phone's screen is off (power-saving suppresses WiFi activity). This creates "ghost away" events. Use nmap ONLY as one signal in a Bayesian/multi-source fusion model, never as the sole trigger for security or HVAC automations. Source: [Reddit r/homeassistant](https://www.reddit.com/r/homeassistant/comments/gbenma/), May 2020.

- **HA 2025.11 breaking change: person entity state now uses zone friendly name instead of zone object ID.** Automations that trigger on `state: 'zone_object_id'` silently break. Update automations to use zone friendly name (e.g., `state: 'Home'` instead of `state: 'home'`). Source: [home-assistant.io blog 2025.11](https://rc.home-assistant.io/blog/2025/10/02/release-202511/), Oct 2025.

- **Companion app presence stops updating on Android after phone restart** if battery optimization is re-enabled by Android itself (common after OS updates). Fix: check Settings → Apps → Home Assistant → Battery → set to "Unrestricted" after every major Android update. Source: community.home-assistant.io, recurring thread.

## Related Concepts

- [[presence-phone-limits.md|presence phone limits]]
- [[presence-bayesian.md|presence bayesian]]
- [[presence-sensor-fusion.md|presence sensor fusion]]
