---
title: Summary — Home Assistant ExpertPack (Composite)
type: summary
tags:
- pack-overview
- summaries
pack: home-assistant
retrieval_strategy: standard
---
# Summary — Home Assistant ExpertPack (Composite)

This is a composite ExpertPack combining a **product pack** (reference knowledge about the HA platform) and a **process pack** (practical 7-phase guide to building a smart home).

## Quick Navigation

**Just starting?** → [[overview.md|Process overview]] → [[01-planning.md|Phase 1: Planning]]

**Need a decision framework?** → [[installation-method.md|Installation method]] | [[protocol-selection.md|Protocol selection]] | [[hardware-selection.md|Hardware selection]]

**Looking up how HA works?** → [[overview.md|Product overview]] → [[_index.md|Concepts]]

**Troubleshooting?** → [[diagnostic-guide.md|Diagnostic guide]] | [[top-ha-mistakes.md|Common mistakes]]

**Automation patterns?** → [[motion-lighting.md|Motion lighting]] | [[climate-control.md|Climate control]] | [[presence-detection.md|Presence detection]]

## Product Pack Summary

→ [[concepts-overview.md|Full product concepts summary]]

The product pack covers HA's internals: the integration→device→entity→state hierarchy (core-architecture), the trigger→condition→action automation model (automation-fundamentals), protocol selection (protocols), YAML configuration patterns (yaml-configuration), integration evaluation (integrations-guide), dashboard design (dashboard-design), DIY sensor building (esphome-fundamentals), network security (network-architecture), backup/migration (backup-migration), presence detection (presence-detection), voice assistant (voice-assistant), and energy management (energy-management).

## Process Pack Summary

→ [[process-overview.md|Full process summary]]

The process pack provides a structured path through 7 phases (planning → hardening), 3 pre-purchase decision frameworks, 4 proven automation patterns, and a gotchas guide covering the mistakes that cost the most time.

## Key Facts

- HA is local-first, open-source, and integrates 3,000+ devices without cloud dependency.
- **Best default protocol:** Zigbee — local, cheap ($7-25/device), massive device selection, proven.
- **Best hardware (2025-2026):** Intel N100 mini-PC (~$130-180) or Raspberry Pi 5 + USB SSD.
- **Never use an SD card** — they fail in 6-18 months under HA's write load.
- **Automate backups on day one** — Google Drive Backup add-on, or Samba to NAS.
- **Never port-forward port 8123** — use Nabu Casa, Tailscale, or a reverse proxy.
