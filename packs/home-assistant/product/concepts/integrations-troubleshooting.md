---
title: "Integration Reload, Debug, and Monthly Breaks"
type: concept
tags:
  - integrations-guide
  - reload
  - logger
  - breaking-changes
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/integrations-troubleshooting
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - integrations-mqtt-cloud.md
  - integrations-hacs.md
  - integrations-reliability.md
content_hash: sha256:522ada185e320366daf3045c643e9ca476de7b33b3c406d8f32dfbe59a03e5f3
---
# Integration Reload, Debug, and Monthly Breaks

Most integrations reload without restarting HA. Enable per-integration debug logging only while reproducing a bug. HA releases the first Wednesday of each month and breaking changes are normal — read the notes, backup, then update.

## Integration Troubleshooting

### Reload vs Restart

Most integrations support **reloading** without restarting all of HA. This is much faster and avoids disrupting running automations.

```
Settings → Devices & Services → [Integration] → ... → Reload
```

Or via Developer Tools → YAML → [integration section] → Reload

**When to reload vs restart:**
- Config change to existing integration → reload
- Added new integration → reload usually works, restart if entities don't appear
- New HACS custom integration installed → restart required
- HA update → restart required

### Enabling Debug Logging for an Integration

```yaml
# configuration.yaml — temporary, remove after debugging
logger:
  default: warning
  logs:
    homeassistant.components.hue: debug
    custom_components.frigate: debug
    zigpy: debug
```

After adding: reload YAML configuration (Developer Tools → YAML → Reload Logger Settings). Debug logs are verbose — disable after troubleshooting or they'll fill your disk.

### The Monthly Breaking Change Pattern

HA releases on the first Wednesday of each month. Every release includes:
- New features
- Integration improvements
- Deprecation notices
- **Breaking changes** — things that worked last month may not this month

**Safe update workflow:**
1. **Read the release notes** before updating — always at `home-assistant.io/blog`
2. Check if any integrations you use are listed under "Breaking Changes"
3. Take a backup before updating
4. Update HA
5. Check integration pages for any new required configuration

HACS integrations break most often during HA major version bumps. Always check HACS integration issue trackers after major HA updates.

## Related Concepts

- [[integrations-mqtt-cloud.md|integrations mqtt cloud]]
- [[integrations-hacs.md|integrations hacs]]
- [[integrations-reliability.md|integrations reliability]]
