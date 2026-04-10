---
title: "Research Coverage — Home Assistant Ecosystem"
type: "source"
tags: [-coverage, sources]
pack: "home-assistant-product"
retrieval_strategy: "standard"
id: home-assistant/product/sources/_coverage
verified_at: '2026-04-10'
verified_by: agent
---
# Research Coverage — Home Assistant Ecosystem

Pack version: (not yet built)
Initial research: 2026-03-10 (source discovery only)
Last deepened: —
Estimated knowledge coverage: **not started** — Phase 0 (source discovery) complete. No content extracted yet.

## Source Inventory

### Official Documentation
| Source | Status | Value | Notes |
|--------|--------|-------|-------|
| home-assistant.io/docs | ⬜ Identified | Critical | Official docs — installation, configuration, YAML reference, integrations. The primary source. |
| home-assistant.io/integrations | ⬜ Identified | Critical | 2000+ integration pages. Each has config options, known issues, entity types. |
| home-assistant.io/blog | ⬜ Identified | High | Release notes, feature announcements, architecture decisions. Monthly release cycle. |
| developers.home-assistant.io | ⬜ Identified | High | Developer docs — custom integrations, API reference, architecture internals. |
| companion.home-assistant.io | ⬜ Identified | Medium | Mobile app docs, troubleshooting, notification setup. |
| analytics.home-assistant.io/integrations | ⬜ Identified | High | Real usage data — which integrations are most popular. Verified source for prioritizing coverage. |

### Forums & Communities
| Source | Status | Value | Notes |
|--------|--------|-------|-------|
| community.home-assistant.io | ⬜ Identified | Critical | Official Discourse forum. Massive archive of troubleshooting, config examples, integration-specific issues. |
| r/homeassistant (~475K members) | ⬜ Identified | Very High | One of the largest home automation subreddits. Beginner guides, troubleshooting, project showcases, product recommendations. |
| r/homeautomation | ⬜ Identified | Medium | Broader home automation community, HA frequently discussed. |
| Home Assistant Discord | ⬜ Identified | High | Real-time support channel. Harder to mine but fast-moving troubleshooting. |
| Home Assistant Facebook group | ⬜ Identified | Medium | Additional community, less technical than Reddit/Discord. |

### Video Content
| Source | Status | Value | Notes |
|--------|--------|-------|-------|
| @home_assistant (official YouTube) | ⬜ Identified | High | Official videos + livestreams. Release showcases, feature walkthroughs. |
| Everything Smart Home (YouTube) | ⬜ Identified | Very High | Community-recommended HA-focused channel. Hardware reviews, integration guides, ESPHome projects. |
| Smart Home Junkie (YouTube) | ⬜ Identified | Very High | Community-recommended. Step-by-step HA tutorials, automation blueprints. |
| JuanMTech (YouTube) | ⬜ Identified | High | HA guides, dashboard design, device reviews. |
| HomeTechHacker (blog + YouTube) | ⬜ Identified | High | HA integration guides, ESPHome projects, device reviews. |
| The Hook Up (YouTube) | ⬜ Identified | High | Zigbee/Z-Wave/Thread deep dives, protocol comparisons. |
| SmartHomeScene.com (blog) | ⬜ Identified | High | HA-focused smart home blog. Device reviews, integration guides, news. |
| HASSCASTS (YouTube) | ⬜ Identified | Medium | HA tutorials, growing channel. GUI-focused automation guides. |

### Protocol & Hardware Documentation
| Source | Status | Value | Notes |
|--------|--------|-------|-------|
| Zigbee2MQTT docs | ⬜ Identified | High | Alternative Zigbee integration, device compatibility database, coordinator support. |
| ZHA (Zigbee Home Automation) docs | ⬜ Identified | High | Built-in Zigbee integration docs. Device quirks, coordinator compatibility. |
| Z-Wave JS docs | ⬜ Identified | High | Z-Wave integration, device database, network management. |
| Matter/Thread documentation | ⬜ Identified | High | New protocol — rapidly evolving. HA has Matter certification (CSA-certified). |
| ESPHome docs (esphome.io) | ⬜ Identified | High | Component library, YAML configs, device templates. Tightly coupled with HA. |

### Third-Party Integration Ecosystems
| Source | Status | Value | Notes |
|--------|--------|-------|-------|
| HACS (Home Assistant Community Store) | ⬜ Identified | Very High | Custom integrations, custom cards, custom themes. The unofficial "app store." |
| Mushroom Cards docs | ⬜ Identified | High | Most popular custom dashboard card set. |
| Node-RED HA nodes | ⬜ Identified | Medium | Alternative automation engine, popular with complex flows. |
| AppDaemon docs | ⬜ Identified | Medium | Python-based automation framework for HA. |

### Books & Courses
| Source | Status | Value | Notes |
|--------|--------|-------|-------|
| "Home Assistant" by Udo Brandes (German, 2024) | ⬜ Identified | Low | Only known book. Community notes it was "outdated before first character was printed" — HA moves too fast for books. |
| No official certification program exists | — | — | HA is community-driven. No formal certification. The docs ARE the training material. |

**Key finding:** The community explicitly says books are useless for HA because it evolves monthly. This validates the ExpertPack approach — a structured, updatable knowledge pack is exactly what's needed here.

### News & Release Tracking
| Source | Status | Value | Notes |
|--------|--------|-------|-------|
| home-assistant.io/blog (monthly releases) | ⬜ Identified | High | Each monthly release adds features, changes integrations, deprecates things. |
| The Verge / Ars Technica HA coverage | ⬜ Identified | Low | Mainstream tech press, surface-level coverage. |
| @home_assistant on X/Twitter | ⬜ Identified | Medium | Announcements, community highlights. |

## Known Gaps (Pre-Build)
- **No content extracted yet** — this is Phase 0 only
- Integration coverage will need prioritization — 2000+ integrations means we MUST scope. Use analytics.home-assistant.io to identify top 50-100 by usage.
- Protocol comparison knowledge (Zigbee vs Z-Wave vs Thread/Matter vs WiFi vs Bluetooth) is critical practitioner knowledge that LLMs handle poorly
- YAML configuration patterns, templating (Jinja2), and automation logic are the core "agent value" areas
- Dashboard design (Lovelace/modern dashboards, custom cards) is a major user pain point
- Hardware recommendations (coordinators, hosts, sticks) change frequently — volatile appendix territory

## Priority Sources for Phase 1 Build
1. **home-assistant.io/docs** — Core concepts, architecture, YAML reference (durable)
2. **r/homeassistant top threads** — Common pain points, beginner mistakes, protocol advice (durable)
3. **analytics.home-assistant.io** — Integration popularity data to scope coverage (current)
4. **community.home-assistant.io** — Troubleshooting patterns, integration-specific issues (durable)
5. **Protocol docs** (Zigbee2MQTT, ZHA, Z-Wave JS, Matter) — Comparison and selection guidance (durable)

## Scoping Decision Needed
A full Home Assistant pack covering all 2000+ integrations is impossible. Proposed scope for v1.0:
- **Core concepts** — Architecture, installation methods, YAML vs UI config, entities/devices/areas model
- **Protocol guide** — Zigbee vs Z-Wave vs WiFi vs Thread/Matter decision framework (high agent value, very durable)
- **Top 20-30 integrations** — Based on analytics popularity data, with config patterns and common issues
- **Automation patterns** — Triggers, conditions, actions, templates (Jinja2), blueprints (very durable, very high agent value)
- **Dashboard fundamentals** — Lovelace/modern dashboard, key card types, common layouts
- **Troubleshooting** — Common errors, diagnostic approaches, safe mode, log reading
- **Hardware selection** — Coordinator/host recommendations (volatile appendix with refresh metadata)
