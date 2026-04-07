---
title: Home Assistant Smart Home Guide
type: overview
tags: []
pack: home-assistant
retrieval_strategy: standard
---
# Home Assistant Smart Home Guide

## What This Is

This is a **composite ExpertPack** — two packs in one:

- **[[overview.md|Product Pack]]** — Deep reference knowledge about the Home Assistant platform itself: its architecture, protocols, automation model, YAML configuration, integrations, dashboards, and troubleshooting.
- **[[overview.md|Process Pack]]** — A phased, practical guide to *building* a smart home with Home Assistant, from initial hardware selection through a fully hardened, automated home.

Together they give you an AI agent that can both *answer technical questions* about Home Assistant and *guide you through the journey* of building and expanding your smart home.

---

## How to Use This Pack

### If you're just starting out
Start with the process pack. Work through the phases in order — they're designed to build on each other without overwhelming you.

→ [[overview.md|Process overview]]  
→ [[01-planning.md|Phase 1: Planning]]

### If you need to make a key decision
The decisions directory distills the major choice points into structured frameworks.

→ [[installation-method.md|Installation method]] — HA OS vs Container vs Supervised vs Core  
→ [[protocol-selection.md|Protocol selection]] — Zigbee vs Z-Wave vs WiFi vs Thread/Matter  
→ [[hardware-selection.md|Hardware selection]] — Pi vs mini-PC vs VM

### If you're troubleshooting or looking up concepts
The product pack is your reference layer. It covers the platform's internals, protocols, automation fundamentals, and common failure modes.

→ [[overview.md|Product overview]]  
→ [[_index.md|Troubleshooting]]  
→ [[_index.md|Concepts]]

### If you want proven automation patterns
The process pack includes battle-tested implementation patterns for common automation scenarios.

→ [[motion-lighting.md|Motion lighting]]  
→ [[climate-control.md|Climate control]]  
→ [[security-monitoring.md|Security monitoring]]  
→ [[notification-patterns.md|Notification patterns]]

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
