---
title: "Home Assistant State Machine"
type: concept
tags:
  - core-architecture
  - state-machine
  - events
  - state-changed
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/core-state-machine
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - core-architecture.md
  - automation-trigger-action.md
  - core-services-install.md
content_hash: sha256:ac5ea1611caba039bcecd6a1d72be60eae40fbd0bd5d88166aa2e15969b9303e
---
# Home Assistant State Machine

Home Assistant is a state machine: it stores the current state of every entity and fires `state_changed` when an integration reports a new value. Automations, dashboards, and templates all read or write those states through the event loop.

## The State Machine

HA is fundamentally a **state machine** — it tracks the current state of every entity and reacts when states change.

**The event loop:**
1. An integration reports a state change (sensor reads new temperature, light is turned on)
2. HA records the new state in its database
3. The state change fires a `state_changed` event
4. Any automation with a matching trigger evaluates its conditions
5. If conditions pass, the automation executes its actions
6. Actions may change other entity states, which fire more events

This is why understanding entities and states is foundational — every automation, dashboard card, and template ultimately reads or writes entity states.

## Related Concepts

- [[core-architecture.md|core architecture]]
- [[automation-trigger-action.md|automation trigger action]]
- [[core-services-install.md|core services install]]
