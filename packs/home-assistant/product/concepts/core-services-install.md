---
title: "Services, Actions, and Installation Types"
type: concept
tags:
  - core-architecture
  - services
  - actions
  - ha-os
  - supervisor
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/core-services-install
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - core-architecture.md
  - core-state-machine.md
  - backup-migration-paths.md
content_hash: sha256:1e27bdfb2957af81d8c2b8054a5ce46a0494ad54fed400033f1e1e8722bb91d5
---
# Services, Actions, and Installation Types

Services (the UI now says Actions) are the verbs — `light.turn_on`, `climate.set_temperature`, `notify.mobile_app`. HA installs four ways: OS (recommended, has Supervisor and add-ons), Container, Core, and Supervised. Without Supervisor you run Mosquitto, backups, and updates yourself.

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

## Related Concepts

- [[core-architecture.md|core architecture]]
- [[core-state-machine.md|core state machine]]
- [[backup-migration-paths.md|backup migration paths]]
