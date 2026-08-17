---
title: "Integration Quality Scale and Pre-Install Checks"
type: concept
tags:
  - integrations-guide
  - quality-scale
  - evaluation
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/integrations-quality-eval
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - integrations-iot-class.md
  - integrations-hacs.md
  - integrations-reliability.md
content_hash: sha256:7e6b73023453fdf8057705fd4b7d025a18936a8a4ac33fae7ca9ea19612cc4c6
---
# Integration Quality Scale and Pre-Install Checks

Official integrations are rated Platinum through Bronze (or unlabeled). Quality scale plus IoT class tells you what to expect. Before installing, read Known Limitations, scan GitHub issues, check the forum, and look at the last two or three release notes for breaking changes.

## Integration Quality Scale

HA's official integrations are rated on a quality scale. Check the integration's documentation page:

| Level | Meaning |
|-------|---------|
| **Platinum** | Implements all best practices, auto-discovered, fully featured, actively maintained |
| **Gold** | Implements most best practices, good device support |
| **Silver** | Solid integration, may be missing some advanced features |
| **Bronze** | Basic functionality, may have limitations |
| *(unlabeled)* | Older integrations awaiting quality review |

Quality scale + IoT class together tell you what to expect. A Platinum Local Push integration (Zigbee, ESPHome) is rock solid. A Bronze Cloud Poll integration is one API change away from breaking.

## Evaluating an Integration Before Installing

Checklist:
1. **Check IoT class** on the integration documentation page
2. **Check quality scale** 
3. **Read the "Known Limitations" section** — every honest integration has one
4. **Check GitHub issues** — search the HA repository (`github.com/home-assistant/core/issues?q=<integration_name>`) for open bugs
5. **Check community forum** — search `community.home-assistant.io` for the integration name + recent issues
6. **Check release notes** — scan the last 2-3 monthly release notes for breaking changes

For HACS custom integrations, additionally check:
- GitHub stars and recent commit activity (is it still maintained?)
- Number of open issues vs closed
- When the last release was (unmaintained = future breakage risk)

## Related Concepts

- [[integrations-iot-class.md|integrations iot class]]
- [[integrations-hacs.md|integrations hacs]]
- [[integrations-reliability.md|integrations reliability]]
