---
title: "Integration Reliability Patterns"
type: concept
tags:
  - integrations-guide
  - myq
  - tuya
  - hacs
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/integrations-reliability
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - integrations-iot-class.md
  - integrations-hacs.md
  - integrations-mqtt-cloud.md
content_hash: sha256:8bdbd5455996d896d9fd12a36e56c729b442ee32db16a4575adc5daa35434166
---
# Integration Reliability Patterns

IoT class is a strong predictor of real-world reliability: local push almost never breaks; cloud polling breaks when vendors change APIs. Chamberlain/MyQ and Mazda already killed third-party access. HACS integrations break 2–4 times a year on HA updates.

## Community Reality Check: Integration Reliability Patterns

> Appended from community mining, 2026-03-12.
> Sources: r/homeassistant, community.home-assistant.io, GitHub issues, Hacker News.

### Cloud vs. Local: Real-World Reliability

The integration quality classification (Local Push, Local Polling, Cloud Push, Cloud Polling) on each HA integration page is a strong predictor of reliability:

| Class | Reliability | Breaks when | Examples |
|-------|-------------|-------------|---------|
| Local Push | Highest | Rarely (only HA API changes) | ESPHome, Zigbee2MQTT, Z-Wave JS |
| Local Polling | High | When device firmware changes | LocalTuya, some Shelly |
| Cloud Push | Medium | When vendor changes API | Nest, Ecobee |
| Cloud Polling | Low | Regularly (rate limits, auth changes) | Tuya cloud, generic cloud APIs |

**Community rule**: for anything critical (security, HVAC, alarms), use Local Push only.

### Integrations Vendors Have Killed or Threatened

- **Chamberlain/MyQ** (Nov 2023): API access revoked. HA integration removed. See [HA blog post](https://www.home-assistant.io/blog/2023/11/06/removal-of-myq-integration/).
- **Mazda** (Oct 2023): DMCA takedown of third-party API tool. Source: [Ars Technica](https://arstechnica.com/cars/2023/10/mazdas-dmca-takedown-kills-a-hobbyists-smart-car-api-tool/).
- **Generic Tuya cloud**: randomly requires re-authentication every few weeks; cloud controls sometimes lag 2–5 seconds. LocalTuya + network block is the workaround.

### HACS Custom Integration Reality

HACS integrations break on HA updates 2–4 times per year on average. They use internal HA APIs that change without notice. The community pattern:
1. Update HA
2. HACS integration breaks
3. Wait 1–7 days for maintainer to push a fix
4. Update HACS integration

**Mitigation**: keep a HA snapshot before every update. Minimize HACS integrations to what has no official alternative.

## Related Concepts

- [[integrations-iot-class.md|integrations iot class]]
- [[integrations-hacs.md|integrations hacs]]
- [[integrations-mqtt-cloud.md|integrations mqtt cloud]]
