---
title: "Why Phone-Only Presence Fails"
type: concept
tags:
  - presence-detection
  - companion-app
  - waf
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/presence-phone-limits
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - presence-sensor-fusion.md
  - presence-pitfalls.md
  - presence-bayesian.md
content_hash: sha256:51029930b105ea03bebf4e7e24894ca4977a241669cb9a4c10a76b986ff01cd2
---
# Why Phone-Only Presence Fails

Phone-only tracking is unreliable for roughly 40% of households because of battery optimization, OS background limits, GPS drift, and family members who will not run the Companion app. WAF (partner/family acceptance) is the other half of the same problem — the system is only as good as its weakest sensor.

## Why Phone-Based Tracking Alone Fails

The HA Companion app (Android/iOS) is the most common presence sensor — it reports GPS location and can detect home/away transitions. But in practice, it fails more than people expect:

**Android battery optimization** is the #1 killer. Android aggressively kills background apps to save battery, and the HA companion app is frequently killed — especially on Samsung, Xiaomi, Huawei, and OnePlus devices. The phone appears "home" or "away" based on the last reported state before the process was killed, not its actual current location.

**iOS background refresh limits** cause delayed updates. Apple limits apps to ~30-minute background refresh cycles. A person who leaves at 7:15 AM may not appear "away" in HA until 7:45 AM. This means automations that trigger "when person leaves" can fire 30 minutes late.

**GPS drift in urban areas** is a real problem. Apartment buildings, shopping centers, and downtown areas see GPS errors of 50-200 meters. A home zone radius of 100m means false away/home triggers several times per week in dense areas. Increasing zone radius helps but reduces resolution.

**Family members who don't use the companion app.** Partners, teenagers, and elderly relatives rarely maintain the app correctly. Battery saver mode gets toggled on. The app gets force-stopped. Some family members simply refuse to install it.

**Network transitions.** When a phone switches from WiFi to mobile data (walking to the car), some integrations interpret this as "left home" before GPS confirms the departure, causing phantom departures.

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

## Related Concepts

- [[presence-sensor-fusion.md|presence sensor fusion]]
- [[presence-pitfalls.md|presence pitfalls]]
- [[presence-bayesian.md|presence bayesian]]
