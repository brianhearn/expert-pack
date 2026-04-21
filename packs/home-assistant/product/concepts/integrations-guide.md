---
title: Integrations Guide — Evaluating, Choosing, and Managing HA Integrations
type: concept
tags:
- concepts
- core-architecture
- esphome-fundamentals
- integrations-guide
- protocols
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/integrations-guide
verified_at: "2026-04-21"
verified_by: agent
schema_version: "4.1"
concept_scope: single
---
<!-- context: section=concepts, topic=integrations-guide, related=core-architecture,protocols,esphome-fundamentals -->
---
sources:
  - type: documentation
    url: "https://www.home-assistant.io/integrations/"
    date: "2026-03"
  - type: data
    url: "https://analytics.home-assistant.io/integrations"
    date: "2026-03"
  - type: community
    url: "https://hacs.xyz/docs/"
    date: "2026-03"
  - type: community
    url: "https://community.home-assistant.io/t/hacs-safety-guide/500100"
    date: "2025-10"
---

# Integrations Guide — Evaluating, Choosing, and Managing HA Integrations

> **Lead summary:** Home Assistant has 3,000+ official integrations and thousands more in HACS. Most users never need more than 20-30 integrations. The critical skill isn't knowing all integrations — it's evaluating quality before installing, understanding the IoT class hierarchy (local push beats cloud poll every time), and managing the monthly update cycle that occasionally breaks things. HACS opens the door to powerful community extensions but requires thoughtful security evaluation. This guide gives you a framework for integration decision-making, covers the top integrations by real-world usage, and explains when to go cloud vs local.

## IoT Classes — The Most Important Integration Attribute

Every official HA integration has an **IoT class** — a label describing how it communicates. This is the #1 signal for reliability and independence:

| IoT Class | How It Works | Local Control | Reliability | Example |
|-----------|-------------|---------------|-------------|---------|
| **Local Push** | Device sends data directly to HA, no polling | ✅ Yes | ⭐⭐⭐⭐⭐ | Philips Hue (local), ESPHome, Zigbee |
| **Local Poll** | HA regularly requests data from device on LAN | ✅ Yes | ⭐⭐⭐⭐ | UniFi, some Shelly models |
| **Cloud Push** | Cloud service forwards device data to HA | ❌ Cloud | ⭐⭐⭐ | Nest (cloud API) |
| **Cloud Poll** | HA polls a cloud API for data | ❌ Cloud | ⭐⭐ | Most "smart" WiFi devices |
| **Assumed State** | HA can't confirm device state, assumes it based on last command | N/A | ⭐ | Some RF remotes, IR blasters |

**What this means practically:**
- **Local Push**: instant, always works even without internet, responds in milliseconds
- **Cloud Poll**: depends on manufacturer's server staying up (Tuya shut down in 2023, Wemo shut down their API, etc.), introduces latency (5-30 seconds), stops working if they kill the API
- **Assumed State**: HA "thinks" the light is on but doesn't actually know — if something else changed the state, HA is wrong

**The killer question for any WiFi device:** "If my internet goes down, will this still work?" Local Push = yes. Anything cloud = no.

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

## Top Integrations by Real Usage

Based on analytics.home-assistant.io reporting (integrations with the most active installs):

### Network & Infrastructure

**UniFi Network** (local poll)
The gold standard for WiFi-based device tracking. If you have a UniFi router, this integration provides device presence tracking via DHCP leases + active client tracking. More reliable than phone-based detection. No cloud dependency.

**AdGuard Home** (local poll)
DNS-level ad blocking with HA controls. Toggle filtering, monitor request counts, block specific devices from internet access.

**Pi-hole** — similar to AdGuard, DNS-level blocking

### Climate & Energy

**HACS: Generic Thermostat** is built-in — create a smart thermostat from any temperature sensor + switch.

**Nest** (cloud poll) — Google's smart thermostat. Works but cloud-dependent. If offline = manual thermostat.

**Ecobee** (cloud poll) — popular alternative to Nest. Same cloud caveat.

**Tesla** (cloud poll) — vehicle integration. Check Tesla's history of breaking third-party API access before relying heavily on this.

**Local energy monitoring options:** Shelly EM (local push), Emporia Vue (local API available), PZEM via ESPHome.

### Lighting

**Philips Hue** — operates in two modes:
- *Local API (v2)*: connects to Hue Bridge on LAN — fast, local push, recommended
- *Cloud (older API)*: deprecated, avoid

**LIFX** — cloud or local. The local integration (`lifx` using UDP broadcast) is excellent. Supports all color features locally.

**Zigbee (ZHA / Zigbee2MQTT)** — the ideal: remove the manufacturer's app entirely and control all Zigbee lights via HA.

### Security & Cameras

**Frigate** (local, via MQTT or custom integration)
The most powerful self-hosted NVR with object detection. Runs locally on HA host or separate server. Detects people, cars, animals, packages. Integrates with HA for notifications and automations triggered by detected objects.
→ Install: `custom:frigate-hacs` from HACS, runs as a HA add-on or separate Docker container

**Ring** (cloud push) — doorbell/cameras. Works but cloud-only. Ring has a history of API changes.

**Unifi Protect** (local push) — best local camera system. If you have Unifi hardware, this is the local alternative to Ring/Nest cam.

**Reolink** (local) — budget IP cameras with good local HA support. Notable exception in the budget camera space.

### Media

**Plex** (local/cloud) — works well, discovers media servers on LAN.

**Sonos** (local push) — best-in-class speaker integration. Entity state updates are real-time.

**Spotify** (cloud) — connect and control Spotify playback. Cloud-dependent but Spotify's API has been stable.

**Apple TV** (local push) — control Apple TV, track what's playing, use presence for "TV watching" state.

**Chromecast/Google TV** (local push) — solid integration, works well for media player state.

**Samsung SmartThings TV** (local) — newer Samsung TVs (2018+) support local control via websocket.

### Voice & Assistants

**Assist** (built-in, local) — HA's own voice assistant. Fully local with Whisper (speech-to-text) + Piper (text-to-speech) add-ons. No cloud required.

**Google Assistant / Alexa** — cloud bridges that make HA entities visible to voice assistants. Require Nabu Casa subscription or self-hosted HTTPS endpoint.

### Zigbee & Z-Wave

**ZHA (Zigbee Home Automation)** — built-in, simpler setup, ~2000 device support
**Zigbee2MQTT** — add-on, more complex, ~3500+ device support, more customization

**Z-Wave JS** — the only maintained Z-Wave integration for HA. Works with Z-Wave JS UI add-on for network management.

### Weather & Environment

**Open-Meteo** (cloud poll) — free, no API key, EU-based (GDPR compliant), excellent forecast accuracy.

**OpenWeatherMap** (cloud poll) — free tier with API key, widely used.

**Meteorologisk Institutt (Met.no)** — Norwegian weather service, no API key, good global coverage.

**AccuWeather** — has a free tier (100 calls/day), more detailed forecasts.

### Utility & Automation Helpers

**MQTT** (local push) — the universal protocol bridge. If a device supports MQTT, it can be integrated. Powers Zigbee2MQTT, Tasmota, custom DIY sensors.

**Node-RED** (via HACS integration) — alternative automation engine running as a HA add-on. Visual flow-based programming. Useful for complex automations where HA's automation editor is limiting.

**Home Assistant Cloud (Nabu Casa)** — $6.50/month. Provides: remote access without port forwarding, Google/Alexa bridge, webhook relay. Not required but simplest remote access solution.

## HACS — The Community App Store

HACS (Home Assistant Community Store) is the unofficial extension ecosystem for HA. It provides:
- **Custom integrations** — additional integrations not in official HA (Frigate, car integrations, obscure devices, etc.)
- **Custom frontend cards** — Mushroom, button-card, mini-graph-card, etc.
- **Themes**
- **Python scripts**

### Installing HACS
HACS requires a GitHub account. Install via:
1. Download HACS from `github.com/hacs/integration`
2. Place in `custom_components/hacs/`
3. Add integration in HA: Settings → Integrations → HACS
4. Authenticate with GitHub account

Or use the HACS one-line install script (official, runs in HA terminal).

### Safety Considerations for HACS

HACS components run with the same privileges as HA itself — full access to your HA configuration, your devices, and potentially your network. This is a real security consideration.

**Safe HACS practices:**
- Prefer integrations with large star counts (500+) and active maintenance
- Check when the last commit was — dormant repos for 1+ year are break risk
- Read the code for high-privilege integrations (or trust community security reviews)
- Never install HACS integrations from untrusted sources (not via HACS itself)
- Keep HACS integrations updated — stale custom integrations are a common source of HA update breakage

**Categories of HACS risk:**
- Frontend cards: low risk (UI only, no network/system access)
- Custom integrations: higher risk (can access network, secrets, etc.)
- Unknown authors: higher risk than popular/well-known repos

**The HACS security model:** GitHub Actions runs malware scanning on some repos, but it's community-moderated, not guaranteed. For critical security needs, stick to official integrations.

### When to Use HACS vs Official

| Situation | Recommendation |
|-----------|---------------|
| Integration exists officially | Use official — better tested, stable API |
| Device not officially supported | Check HACS, evaluate activity level |
| Dashboard card functionality missing | HACS frontend cards are low-risk |
| Custom integration from unknown author | Audit code, check community discussion first |
| Feature added to official in recent release | Migrate from HACS to official when stable |

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

## Cloud vs Local — The Replacement Playbook

If your goal is a truly local smart home (no cloud dependencies), here's what to replace:

| Cloud Integration | Local Alternative |
|-------------------|------------------|
| Tuya / Smart Life | Flash with Tasmota/ESPHome (if ESP chip), or buy Zigbee equivalents |
| Wemo | Replace with Shelly (local) or Zigbee plugs |
| Nest Thermostat | Keep (no good open local alternative) OR Ecobee (same caveat) |
| Ring Doorbell | Reolink doorbell (local) or any RTSP-capable camera + Frigate |
| TP-Link Kasa | The official integration supports local API — configure local mode |
| LIFX | Use local LIFX integration, not cloud |
| Philips Hue | Use Hue Bridge v2 local API |
| SmartThings devices | Depends — some support Zigbee/Z-Wave directly |

**Protocol migration strategy:** Don't rip and replace everything at once. As cloud-dependent devices need replacement, replace them with local equivalents (Zigbee/Z-Wave/ESPHome).

## MQTT — The Universal Protocol Bridge

MQTT is a lightweight pub/sub messaging protocol. It's not a product — it's the glue that connects many different systems to HA.

**When to use MQTT:**
- Tasmota-flashed devices (cloud Tuya devices reflashed with open firmware)
- Zigbee2MQTT (Zigbee through MQTT instead of ZHA)
- DIY sensors (custom ESP firmware, Node-RED to HA)
- Industrial sensors and controllers
- Any device that "speaks MQTT"

**Setup:** Install the Mosquitto MQTT Broker add-on (HA add-on store), then install the MQTT integration in HA. Devices publish to topics, HA subscribes.

**Autodiscovery:** Devices that support MQTT Discovery (Tasmota, Zigbee2MQTT, ESPHome MQTT mode) automatically create entities in HA by publishing their configuration to specific MQTT topics. No manual configuration required.

## Related

- [[core-architecture.md|Core Architecture]] — How integrations, devices, and entities relate
- [[protocols.md|Smart Home Protocols]] — Choosing the right protocol for devices
- [[esphome-fundamentals.md|ESPHome Fundamentals]] — Custom sensor integration
- [[diagnostic-guide.md|Troubleshooting]] — Integration debugging

---

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
