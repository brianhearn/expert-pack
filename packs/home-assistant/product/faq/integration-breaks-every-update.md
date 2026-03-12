---
title: "Why does my integration break every update?"
description: Real-world patterns for HA update-induced integration failures and how to survive them.
mined: 2026-03-12
sources:
  - https://www.reddit.com/r/homeassistant/comments/1i61v5c/how_to_deal_with_breaking_integrations_on_every/
  - https://github.com/hacs/integration/issues/4314
  - https://github.com/home-assistant/core/issues/126235
  - https://news.ycombinator.com/item?id=42813513
---

# Why Does My Integration Break Every Update?

This is one of the most common complaints from experienced HA users. Here's what's really happening and how to handle it.

---

## Why HA Updates Break Integrations

Home Assistant releases monthly (every first Wednesday of the month). Each release can include:
- **Internal API changes** that HACS integrations depend on without being officially supported
- **Entity/state renames** that break automations (e.g., `illuminance_lux` → `illuminance` in Z2M 2.0)
- **YAML key renames** that change behavior (e.g., `service:` → `action:` in 2024.8)
- **Integration-specific breaking changes** listed in the release notes

Official integrations (built-in to HA) get migration paths. HACS custom integrations frequently do not.

---

## Most Frequently Broken Integrations (Community Reports)

| Integration | Breakage Pattern | Fix Pattern |
|-------------|-----------------|-------------|
| HACS itself | HA API deprecations | Update HACS first, before updating HA |
| Zigbee2MQTT (Z2M) | Major version changes (1.x → 2.0) | Read Z2M breaking changes before updating |
| LocalTuya | HA core API changes | Wait for LocalTuya HACS update, or downgrade HA |
| Z-Wave JS | Add-on version changes | Re-interview devices after update |
| Any HACS integration | Random HA internal API changes | Always snapshot before updating |

---

## The Correct Process for HA Updates

1. **Create a backup** (Settings → System → Backup → Create) — do this EVERY time
2. **Read the breaking changes** in the [HA release blog](https://www.home-assistant.io/blog/)
3. **Check Z2M release notes** if you use Zigbee2MQTT
4. **Update add-ons first**, then HA core
5. **Test critical devices/automations** before considering the update done
6. **If something breaks**: restore the backup, open a GitHub issue for the HACS integration

---

## HACS Integrations Have No Stability Guarantees

This is documented but underappreciated: HACS integrations exist in HACS precisely because they don't meet HA quality standards or weren't accepted as built-in. They:
- Use internal HA APIs that change without notice
- May be abandoned at any time
- Are tested by maintainers, not the HA team

**Community rule of thumb**: Limit HACS integrations to devices/services with no official HA alternative. The fewer HACS integrations, the more stable your system.

---

## After a Broken Update: Decision Tree

```
Integration broken after HA update?
├── Is it a HACS integration?
│   ├── Yes → Check GitHub for open issues, wait for maintainer update
│   │         Workaround: restore backup, hold HA version, or remove integration
│   └── No  → File a GitHub issue at home-assistant/core with logs
│
├── Is it Z-Wave devices showing "unavailable"?
│   └── Re-interview each device one by one (see diagnostic-guide.md)
│
└── Is HACS itself broken?
    ├── Missing from sidebar → Settings → HACS → Configure → enable AppDaemon discovery
    └── Won't start → Update HACS via terminal: wget -O - https://get.hacs.xyz | bash -
```

---

## Related

- [Community Gotchas](common-mistakes/community-gotchas.md) — Specific version-by-version breakage
- [Diagnostic Guide](../troubleshooting/diagnostic-guide.md) — How to read logs and traces
- [Process Gotchas](../../process/gotchas/common-mistakes.md) — Update process best practices
