# Home Assistant Smart Home Guide

## What This Is

This is a **composite ExpertPack** — two packs in one:

- **[Product Pack](product/overview.md)** — Deep reference knowledge about the Home Assistant platform itself: its architecture, protocols, automation model, YAML configuration, integrations, dashboards, and troubleshooting.
- **[Process Pack](process/overview.md)** — A phased, practical guide to *building* a smart home with Home Assistant, from initial hardware selection through a fully hardened, automated home.

Together they give you an AI agent that can both *answer technical questions* about Home Assistant and *guide you through the journey* of building and expanding your smart home.

---

## How to Use This Pack

### If you're just starting out
Start with the process pack. Work through the phases in order — they're designed to build on each other without overwhelming you.

→ [Process overview](process/overview.md)  
→ [Phase 1: Planning](process/phases/01-planning.md)

### If you need to make a key decision
The decisions directory distills the major choice points into structured frameworks.

→ [Installation method](process/decisions/installation-method.md) — HA OS vs Container vs Supervised vs Core  
→ [Protocol selection](process/decisions/protocol-selection.md) — Zigbee vs Z-Wave vs WiFi vs Thread/Matter  
→ [Hardware selection](process/decisions/hardware-selection.md) — Pi vs mini-PC vs VM

### If you're troubleshooting or looking up concepts
The product pack is your reference layer. It covers the platform's internals, protocols, automation fundamentals, and common failure modes.

→ [Product overview](product/overview.md)  
→ [Troubleshooting](product/troubleshooting/_index.md)  
→ [Concepts](product/concepts/_index.md)

### If you want proven automation patterns
The process pack includes battle-tested implementation patterns for common automation scenarios.

→ [Motion lighting](process/patterns/motion-lighting.md)  
→ [Climate control](process/patterns/climate-control.md)  
→ [Security monitoring](process/patterns/security-monitoring.md)  
→ [Notification patterns](process/patterns/notification-patterns.md)

---

## Pack Structure

```
home-assistant/            ← this composite
├── product/               ← platform reference
│   ├── concepts/          ← architecture, protocols, automation, YAML, ESPHome, dashboards
│   ├── troubleshooting/   ← diagnostics, common mistakes
│   ├── faq/               ← common questions
│   └── glossary.md        ← terminology
│
└── process/               ← building journey
    ├── phases/            ← 7-phase smart home build (planning → hardening)
    ├── decisions/         ← key decision frameworks
    ├── patterns/          ← proven automation patterns
    └── gotchas/           ← traps to avoid
```
