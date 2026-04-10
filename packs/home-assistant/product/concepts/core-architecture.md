---
title: Core Architecture — The HA Mental Model
type: concept
tags:
- automation-fundamentals
- concepts
- core-architecture
- integrations-guide
- protocols
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/core-architecture
verified_at: '2026-04-10'
verified_by: agent
---
<!-- context: section=concepts, topic=core-architecture, related=automation-fundamentals,protocols,integrations-guide -->
---
sources:
  - type: documentation
    url: "https://www.home-assistant.io/getting-started/concepts-terminology/"
    date: "2026-03"
---

# Core Architecture — The HA Mental Model

> **Lead summary:** Home Assistant is a state machine. Everything revolves around **entities** (the atomic unit — a sensor, switch, light, etc.), which belong to **devices** (physical or logical groupings), which connect through **integrations** (the software bridges to hardware and services). Entities have states that change over time. Automations react to state changes. Dashboards display states. Understanding this hierarchy — integration → device → entity → state — is the single most important concept in HA.

## The Hierarchy

```
Integration (software bridge)
  └── Device (physical or logical unit)
        └── Entity (sensor, switch, light, etc.)
              └── State (on/off, 72°F, detected, etc.)
                    └── Attributes (brightness, color, battery %)
```

### Integrations

An integration is a piece of software that connects Home Assistant to an external system — hardware, cloud service, protocol, or platform. Examples: Philips Hue integration talks to the Hue Bridge. MQTT integration connects to an MQTT broker. Weather integration pulls forecast data from an API.

**Key facts:**
- Over 2000 official integrations exist
- Most are configured via the UI (Settings → Devices & Services → Add Integration)
- Some require YAML configuration in `configuration.yaml`
- Custom integrations (via HACS) extend beyond official support
- Integrations can be cloud-dependent (marked with ☁️ icon) or fully local

### Devices

A device is a logical grouping of related entities. One physical device typically creates one HA device with multiple entities. Example: a Zigbee motion sensor (one device) creates entities for motion detection, temperature, light level, and battery percentage.

**Key facts:**
- Devices are created automatically by integrations — you don't create them manually
- A device can belong to one Area (room/zone)
- Device info includes manufacturer, model, firmware version
- Some "devices" are logical, not physical (weather service creates a device with forecast entities)

### Entities

The atomic unit of HA. An entity represents one measurable or controllable thing. Every entity has:
- **Entity ID** — unique identifier (format: `domain.name`, e.g., `light.living_room`, `sensor.outdoor_temp`)
- **State** — current value (`on`, `off`, `72.5`, `home`, `detected`)
- **Attributes** — additional data beyond the state (brightness, color_temp, battery, friendly_name)
- **Domain** — what type of entity it is (light, switch, sensor, binary_sensor, climate, etc.)

**Key facts:**
- Entity IDs are permanent once created — renaming requires care (automations reference them)
- States are always strings internally (even numbers)
- The state + attributes together describe everything HA knows about that entity right now
- Entity history is recorded in the database (configurable retention)

### Areas

Organizational grouping for devices and entities by physical location (room, floor, zone). Areas are optional but highly recommended — they enable floor plans, area-based automations ("turn off all lights in the bedroom"), and dashboard organization.

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

## Services (Actions)

Services are the verbs of HA — the things you can ask entities to do. Examples:
- `light.turn_on` — turn on a light (with optional brightness, color)
- `climate.set_temperature` — set thermostat target temperature
- `notify.mobile_app` — send a push notification

**Key facts:**
- Services are called with a target (which entity/device/area) and optional data (parameters)
- The UI calls them "Actions" (renamed from "Services" in recent versions)
- You can test services in Developer Tools → Services
- Custom integrations can register their own services

## Installation Types

HA can be installed four ways, with significant differences:

| Type | What It Is | Supervisor | Add-ons | Best For |
|------|-----------|------------|---------|----------|
| **HA Operating System** | Dedicated OS on bare metal or VM | ✅ | ✅ | Most users — recommended default |
| **HA Container** | Docker container (just Core) | ❌ | ❌ | Users comfortable with Docker |
| **HA Core** | Python venv installation | ❌ | ❌ | Developers, advanced users |
| **HA Supervised** | HA + Supervisor on existing Linux | ✅ | ✅ | Advanced users wanting add-ons on existing OS |

The **Supervisor** provides: add-on store (like Mosquitto MQTT broker, Node-RED, file editors), backup management, snapshot/restore, and update management. Without it, you manage all supporting services yourself.

## Related

- [[protocols.md|Smart Home Protocols]] — How devices actually communicate with HA
- [[automation-fundamentals.md|Automation Fundamentals]] — Using the state machine for automation
