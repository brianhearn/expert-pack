---
title: Why Is My Automation Not Firing?
type: faq
tags:
- automation-debugging
- automation-fundamentals
- diagnostic-guide
- faq
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/faq/why-is-my-automation-not-firing
verified_at: "2026-04-21"
verified_by: agent
schema_version: "4.1"
concept_scope: single
---
<!-- context: section=faq, topic=automation-debugging, related=automation-fundamentals,diagnostic-guide -->

# Why Is My Automation Not Firing?

> **Lead summary:** Most automation failures have one of five causes: the trigger didn't fire (entity in wrong state or wrong trigger type), a condition silently failed (check the trace — it shows which condition and why), the automation is in `single` mode and was already running, there's a template error causing silent failure, or the entity is `unavailable`/`unknown`. Start with the Automation Trace — it shows exactly what happened at every step and is the fastest path to the root cause.

## Step 1: Check the Automation Trace First

Settings → Automations → [your automation] → Traces (clock icon in top right)

The trace shows the last 5-10 runs. For each run:
- Which trigger fired
- Which conditions were evaluated and whether they passed or failed
- The actual value at each condition evaluation ("entity state was 'off', expected 'on' — condition failed")
- Template rendered values
- Which actions ran

**Most problems are diagnosed here in under a minute.** A condition that failed silently is the #1 cause of "automation doesn't fire."

## Step 2: Check Entity State in Developer Tools

Developer Tools → States → search for the entity in your trigger

Verify:
- Is the entity in the state you expect?
- Is it showing `unavailable` or `unknown`? These prevent triggers from firing correctly.
- Has the state changed recently? (check the "last changed" timestamp)

## Step 3: Check Automation Mode

If your automation mode is `single` (the default) and it was already running when the trigger occurred, the new trigger is silently ignored.

**Symptom:** Motion-activated lights turn off even though you're still moving. New motion doesn't reset the timer.

**Fix:** Change mode to `restart` for motion-activated lights.

```yaml
automation:
  mode: restart  # ← Add this
  trigger:
    - platform: state
      entity_id: binary_sensor.motion_sensor
      to: "on"
```

Other modes: `queued` (runs sequentially), `parallel` (multiple simultaneous instances).

## Step 4: Test Your Template

If your trigger or condition uses a Jinja2 template, open Developer Tools → Template and paste your template there. Template errors cause silent failures in automations.

**Common template bugs:**
- Comparing strings to numbers: `states('sensor.temp') > 20` fails (string vs int comparison)
- Fix: `states('sensor.temp') | float > 20`
- Using `states.sensor.name.state` instead of `states('sensor.name')` — breaks if entity doesn't exist

## Step 5: Check for `unavailable` Triggers

HA fires state change events when an entity becomes `unavailable`. If your trigger is watching for `to: "on"` and the entity briefly goes `unavailable → on`, the trigger DOES fire. But if you're seeing unwanted triggers when devices go offline, you need to exclude unavailable states:

```yaml
trigger:
  - platform: state
    entity_id: binary_sensor.motion_sensor
    to: "on"
    not_from:
      - "unavailable"
      - "unknown"
```

## Step 6: Check HA Logs

Settings → System → Logs → filter by "automation"

Look for WARNING or ERROR entries around the time the automation should have fired. Common log messages:
- "Service not found" — wrong service name or entity not available
- "Template render error" — template syntax error
- "Condition not met" — echoes the trace information

## Common Root Causes Summary

| Symptom | Most Likely Cause | Fix |
|---------|-----------------|-----|
| Never fires | Trigger entity state is wrong | Check entity state in Dev Tools → States |
| Sometimes fires, not always | Condition failing silently | Check trace — look at condition results |
| Fires but does nothing | Action error (unavailable entity, wrong service) | Check trace → action section |
| Lights turn off despite motion | `single` mode ignoring re-triggers | Change to `mode: restart` |
| Fires too many times | Template trigger oscillating | Add `for:` duration to stabilize |
| Fires on device going offline | `unavailable` state triggering | Add `not_from: [unavailable, unknown]` |

→ See [[automation-fundamentals.md]] for trigger/condition/action reference
→ See [[diagnostic-guide.md]] for deeper troubleshooting
