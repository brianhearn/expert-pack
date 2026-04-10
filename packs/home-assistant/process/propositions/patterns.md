---
title: "Propositions — Process Patterns"
type: "proposition"
tags: [patterns, propositions]
pack: "home-assistant-process"
retrieval_strategy: "standard"
id: home-assistant/process/propositions/patterns
verified_at: '2026-04-10'
verified_by: agent
---
# Propositions — Process Patterns

Atomic factual statements extracted from the process patterns files.

---

### patterns/motion-lighting.md (inferred from top-ha-mistakes and common-mistakes)

- Motion-activated lights require `mode: restart` so each new motion event resets the off-delay timer.
- The `single` automation mode (the default) ignores new triggers while the automation is running, causing motion lights to turn off despite continued motion.
- Using a 5-minute `delay` after motion clears is the standard off-delay pattern for motion-activated lights.
- A motion-lighting automation has three parts: turn on when motion detected, wait for motion to clear, turn off after delay.

### patterns/security-monitoring.md (inferred from concepts)

- Security monitoring automations should notify via multiple channels (push notification + optional alarm) for redundancy.
- Door contact sensors are the fastest presence edge-detector — they catch arrivals/departures faster than GPS or WiFi tracking.
- Cameras should be on a dedicated VLAN with no internet access for both security and bandwidth reasons.
- Frigate NVR provides local AI object detection (person, car, package) for security cameras without cloud dependency.

### patterns/climate-control.md (inferred from concepts)

- Presence-based HVAC control is one of the highest-ROI automations — no human interaction needed, immediate energy savings.
- A generic thermostat can be created from any temperature sensor plus a heating/cooling switch using HA's built-in generic thermostat.

### patterns/notification-patterns.md (inferred from concepts)

- The HA Companion app sends push notifications to phones; `notify.mobile_app_<device>` is the service call.
- Notifications should be actionable when possible — include relevant context (which door opened, current state, quick-action buttons).
