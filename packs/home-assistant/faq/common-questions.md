---
sources:
  - type: documentation
    url: "https://www.home-assistant.io/docs/configuration/"
    date: "2026-03"
  - type: community
    url: "https://community.home-assistant.io/t/frequently-asked-questions-faq/676432"
    date: "2025-12"
  - type: community
    url: "https://www.reddit.com/r/homeassistant/wiki/index"
    date: "2026-01"
  - type: community
    url: "https://community.home-assistant.io/t/new-to-ha-read-this-first/537148"
    date: "2025-10"
---

# Frequently Asked Questions

> **Lead summary:** These are the questions that come up repeatedly in r/homeassistant, the HA Community forum, and Discord. Each answer here represents the community consensus in 2026 — not theoretical best practices, but what experienced practitioners actually recommend based on running real HA setups for real people. Where there's genuine debate, the tradeoffs are laid out honestly.

---

## "Should I use the UI (visual editor) or YAML?"

**Short answer:** UI for most things. YAML for complex logic and anything you want in version control.

**Longer answer:**

The trend in HA is strongly toward UI-first. As of 2024-2025, you can create most automations, scripts, helpers, and integrations entirely through the UI without touching YAML. The visual automation editor is significantly improved — it handles most real-world scenarios.

**Use the UI (visual editor) for:**
- Standard automations with straightforward triggers/conditions/actions
- Integration setup and configuration
- Dashboard creation (Sections layout is UI-only)
- Helper creation (input_boolean, input_number, schedule, etc.)
- Device and entity management
- Quick iterations when you want to see results immediately

**Use YAML for:**
- Template sensors (`template:` platform) — these can only be defined in YAML
- Complex Jinja2 template logic in automations
- `packages:` — splitting config into logical files
- Anything you want under version control (git)
- Automations with complex multiline templates (readable in a text editor, not a text box)
- When the visual editor doesn't expose a parameter you need

**The practical hybrid approach** most experienced users settle on:
- Integrations: UI
- Helpers: UI  
- Simple automations (80% of them): UI
- Complex automations with template conditions: UI editor + switch to YAML view for the complex parts
- Template sensors, packages: YAML files edited in VS Code + File Editor add-on

**Version control note:** Automations created in the UI are stored in `.storage/core.automation` (JSON format). Automations in `automations.yaml` are stored as YAML. Both work fine; YAML-in-files is better for git diffs.

---

## "Zigbee2MQTT or ZHA — which should I choose?"

**Short answer:** ZHA if you want simplicity. Zigbee2MQTT if you want power and flexibility.

**Detailed comparison:**

| Aspect | ZHA | Zigbee2MQTT |
|--------|-----|-------------|
| Setup complexity | Easy (built into HA) | Medium (requires MQTT broker) |
| UI configuration | Yes, fully in HA | Yes, via Z2MQTT web UI |
| Device support | Good (~3,000 devices) | Excellent (~4,500+ devices) |
| MQTT independence | No (uses HA core) | Yes — works without HA frontend |
| Coordinator migration | OK | Better tooling |
| Community size | Large | Larger |
| Custom device quirks | Possible but harder | Active developer community, fast quirk additions |
| Multiple coordinators | Not supported | Supported (multi-instance) |

**Choose ZHA if:**
- You're new to HA and want minimum complexity
- Your specific devices are confirmed ZHA-compatible
- You don't run (or don't want to run) MQTT for other things
- You want everything under the HA umbrella without separate add-ons

**Choose Zigbee2MQTT if:**
- You have devices that work in Z2MQTT but not ZHA (check the Z2MQTT device list)
- You want the coordinator to survive independently of HA (sensors keep working if HA reboots)
- You want the best migration tooling when upgrading coordinator hardware
- You already use MQTT for other integrations
- You want multi-coordinator support (large home, 100+ devices)

**Migration between them:** Possible but tedious. All Zigbee devices need to be re-paired to the new stack. Don't switch unless you have a compelling reason — both work well. The switching cost is proportional to your device count.

---

## "How often should I update Home Assistant?"

**Short answer:** Monthly, with a 3-5 day delay after release, and always after reading release notes.

**The practical update rhythm:**

HA releases monthly (typically the first Wednesday of the month). The release notes are detailed and flag breaking changes explicitly.

**Recommended cadence:**
1. **New release drops.** Don't update immediately.
2. **Wait 3-5 days.** Bug fix releases (2024.X.1, 2024.X.2) typically follow within a week if there are critical issues.
3. **Read the release notes.** Check for deprecation warnings and breaking changes that affect your setup. Pay attention if you use custom integrations — HACS might need updates too.
4. **Always backup before updating.** Takes 2 minutes. Non-negotiable.
5. **Update.** If something breaks, restore from backup.

**When to skip a month:** If the release notes don't affect your setup and you're not chasing new features, it's fine to skip. Running 2-3 months behind is reasonable. Running 12+ months behind means you'll have more breaking changes to deal with when you do update, and security patches pile up.

**What actually breaks on updates:** Usually one of:
- A custom integration (HACS) that hasn't been updated for a HA core change
- A deprecated YAML key that's been removed
- An integration that changed its entity naming convention

The release notes call these out. Five minutes of reading saves hours of debugging.

---

## "How many entities is too many? My HA feels slow."

**Short answer:** Entity count is rarely the real problem. It's almost always the recorder database.

**HA handles 1,000+ entities fine on modest hardware.** The HA event loop and state machine are efficient. Having 2,000 entities doesn't meaningfully slow down automations or the dashboard.

**What actually causes performance issues:**

**1. Recorder logging everything:**
If you have sensors updating every 5 seconds (energy monitoring, high-frequency temperature sensors, ESPHome with default intervals), the recorder writes thousands of state changes per minute. This:
- Makes the database grow rapidly (gigabytes per month)
- Adds I/O load to your storage
- Slows the UI when rendering history

**Fix:** Be selective about what gets recorded:
```yaml
# configuration.yaml
recorder:
  purge_keep_days: 14    # Keep only 14 days of history
  exclude:
    entity_globs:
      - sensor.*_power_w          # High-frequency power sensors
      - sensor.*_signal_strength  # WiFi RSSI (changes constantly)
      - sensor.*_linkquality      # Zigbee link quality
    domains:
      - weather                   # External weather (rarely useful in history)
```

**2. Dashboards with too many live-updating cards:**
A dashboard with 50 entity cards, all live-updating, hitting the HA API every second = significant WebSocket load. Use template cards sparingly and check how many active dashboard sessions you have.

**3. Overly complex template sensors:**
Template sensors that do expensive operations (expanding groups, iterating over many entities) and update on every state change can introduce lag. Profile them with the Template Developer Tools.

**4. Database growing beyond SSD capacity:**
If your `/config` partition is nearly full, the recorder starts dropping writes and HA slows down. Check with `df -h` in the SSH terminal.

---

## "Should I use Docker (HA Container) or HA OS?"

**Short answer:** HA OS for 90% of users. Docker only if you already manage Docker infrastructure and explicitly don't need add-ons.

**The three main installation types:**

| Type | Add-ons | Supervisor | Backups | Best For |
|------|---------|-----------|---------|---------|
| **HA OS** | ✅ Full | ✅ Yes | ✅ Built-in | Most users, dedicated hardware |
| **HA Container** | ❌ No | ❌ No | Manual only | Docker-native power users |
| **HA Supervised** | ✅ Full | ✅ Yes | ✅ Built-in | Debian power users on existing server |

**HA OS (recommended for most):**
- Boots directly into HA OS (Linux-based, managed by the HA team)
- Full add-on store (Mosquitto, Nginx, Zigbee2MQTT, Frigate, etc. — all one-click installs)
- Built-in backup system
- Supervisor manages updates, add-ons, OS
- Works on Pi, N100 mini-PCs, x86_64, HA Green/Yellow

**HA Container (Docker):**
- Runs HA as a Docker container alongside other containers you manage
- No add-on store — you manage all services (MQTT broker, NVR, etc.) as separate Docker containers
- No built-in backup (you manage your own)
- Appropriate if you're already managing Docker-Compose stacks and want HA as one more container
- Does NOT support Zigbee2MQTT as an add-on — it's just a separate container you manage

**HA Supervised:**
- Full HA (with Supervisor and add-ons) running on a Debian Linux machine you manage
- Most complex to set up, most control
- The OS must meet strict requirements (specific Debian version, Docker version, no conflicting packages)
- Officially supported but described as "for advanced users"

**The real question:** Do you want add-ons? If yes, use HA OS. The add-on ecosystem (Mosquitto, Z2MQTT, Frigate, Google Drive Backup, Nginx, etc.) is a major productivity multiplier.

---

## "Can I run Home Assistant in a virtual machine?"

**Short answer:** Yes, very well. Proxmox + HA OS VM is a popular and well-supported setup.

**Why run HA in a VM:**
- Run other services on the same hardware (NAS, media server, Pi-hole)
- Take VM snapshots before risky updates (instant rollback)
- Allocate resources (CPU, RAM) dynamically
- No dedicated hardware needed

**Proxmox is the community-standard hypervisor** for HA home labs. It's free, open source, and HA publishes an official import script:

```bash
# On Proxmox, run the community helper script:
bash -c "$(wget -qLO - https://github.com/tteck/Proxmox/raw/main/vm/haos-vm.sh)"
```

This creates a HA OS VM with appropriate settings automatically.

**USB passthrough for Zigbee/Z-Wave coordinators:**
The coordinator must be passed through to the HA VM (not shared with the Proxmox host):

```bash
# In Proxmox VM config file (/etc/pve/qemu-server/XXX.conf):
usb0: host=10c4:ea60    # Pass through by vendor:product ID (most stable)
```

Or in the Proxmox UI: VM → Hardware → Add → USB Device → select your coordinator.

**Resource allocation for HA VM:**
- CPU: 2 cores minimum, 4 recommended if running Frigate or other add-ons
- RAM: 2GB minimum, 4-8GB if running Frigate with ML
- Storage: 32GB minimum, 64GB+ recommended (recorder database grows)

---

## "How do I get my family to actually use it?"

**Short answer:** Make it invisible. The best automation doesn't require anyone to touch a phone.

**The golden rule:** Automations should be invisible infrastructure, not features people need to learn.

**What works:**
- **Motion-activated lights** in hallways, bathrooms, entry points — nobody has to do anything
- **Automatic good morning/good night routines** triggered by first person up / last person to bed
- **Presence-based HVAC** — just works, no interaction needed
- **Automatic locking** after door closes and 5 minutes pass

**What doesn't work:**
- "Open the HA app and tap this card to turn off the lights"
- Voice commands that require specific phrasing family members won't remember
- Automations that occasionally break and make people distrust the system

**Physical switches must always work.** If someone flips a physical switch and nothing happens because HA is between states, that's a trust-destroying failure. Use smart switches (not smart bulbs in dumb-switch setups) so the physical switch always does what it says.

**Voice control lowers the barrier** — "Hey Google, turn off the living room lights" is accessible to most people and doesn't require learning a UI.

**Dashboard is for monitoring, not daily interaction.** Show status (who's home, is the door locked, current temperatures). Don't design a dashboard that requires daily navigation.

**Start small.** Add one automation that makes a real quality-of-life improvement. Prove the system is reliable before expanding. A system that works reliably for one thing earns trust to be given more.

---

## "My automation isn't firing. How do I debug?"

**Systematic debugging approach — check in this order:**

**Step 1: Automation Traces**
Settings → Automations → [your automation] → Traces → last N runs

The trace shows exactly which step ran, which didn't, why conditions failed, and what values were present at each step. This is the most valuable debugging tool. Check it first.

**Step 2: Check entity states in Developer Tools**
Developer Tools → States → search for relevant entities

Verify the entity is in the state you expect. If your trigger is `binary_sensor.motion to 'on'` and the sensor is showing as `unavailable`, that's your problem.

**Step 3: Test the trigger manually**
Developer Tools → Events → fire an event to simulate the trigger, or:
- For time-based triggers: temporarily change the time to "now"
- For state triggers: change the entity state in Dev Tools → States (set state)
- For template conditions: test your template in Developer Tools → Template

**Step 4: Check for template errors**
If your automation has template conditions or actions, paste the template into Developer Tools → Template. Template syntax errors cause silent failures.

**Step 5: Check HA logs**
Settings → System → Logs → filter by `automation` or the specific integration name

Look for warnings or errors around the time the automation should have fired.

**Step 6: Check automation mode**
If your automation mode is `single` and it was already running, the new trigger is silently ignored. Change to `restart` or `queued` depending on desired behavior.

**Common root causes:**
- Template condition evaluates to `False` (check the trace — it shows the evaluated value)
- Entity in `unavailable` or `unknown` state (the trigger or condition can't evaluate)
- `for:` duration not met (trigger fires but condition waits haven't elapsed)
- Wrong entity ID (typo, entity was renamed)
- Automation disabled (the toggle in the automations list)

---

## "Matter vs Zigbee — what should I buy in 2026?"

**Short answer:** Zigbee is proven and mature. Matter is promising but still maturing. Buy what's best for each specific device.

**Zigbee in 2026:**
- Massive device selection (4,500+ confirmed Z2MQTT devices, more in ZHA)
- Mature ecosystem — most quirks and edge cases are solved
- Stable: your Zigbee network from 2020 still works fine
- Local-only by nature
- Cheap: Zigbee devices are often $10-30, especially from Sonoff, IKEA, Aqara
- No IP network integration needed — separate RF mesh

**Matter in 2026:**
- Growing device selection, but still limited vs Zigbee
- Works across ecosystems (Apple HomeKit, Google Home, Amazon, HA) — one device, all platforms
- Local-first when used Thread-based (no hub needed with Thread)
- IP-based: Thread devices join your IPv6 network directly
- Generally more expensive than equivalent Zigbee devices
- Still seeing interoperability issues between platforms in practice
- HA Matter integration is solid but the broader ecosystem has rough edges

**The practical guidance:**
- Don't replace working Zigbee devices with Matter equivalents — pointless churn
- Buy Matter when it's genuinely the best option for that specific device (some Matter devices have features not available in Zigbee equivalents)
- For new sensors and basic devices: Zigbee is still the better choice (cheaper, more options)
- For switches/outlets that might need to work with non-HA systems too: Matter is worth considering
- For EV chargers, major appliances, and devices with rich UIs: Matter is often better supported

**Thread vs WiFi Matter:**
Thread-based Matter devices (battery-powered sensors, smart home devices) form a mesh and are more efficient than WiFi Matter devices. WiFi Matter is for mains-powered devices (bulbs, outlets) and works fine but doesn't mesh. Both work in HA via the Matter integration.

---

## "Is Nabu Casa / Home Assistant Cloud worth it?"

**Short answer:** Yes, for most users. $75/year is reasonable for what you get.

**What you get with Nabu Casa:**

| Feature | Value |
|---------|-------|
| Secure remote access | No port forwarding, no VPN setup, just works |
| Cloud STT for Assist | Good speech recognition without local compute |
| Cloud TTS for Assist | High-quality voices without local inference |
| HA development support | You're funding the project |

**Secure remote access alone is worth it for many users.** The alternative (WireGuard VPN, Tailscale, or a reverse proxy) requires setup and maintenance. Nabu Casa just works, and it's secure.

**When Nabu Casa is NOT necessary:**
- You already have Tailscale or WireGuard set up and it works
- You run fully local voice (Whisper + Piper)
- You don't need remote access at all (home-only use)
- You're on a budget and prefer self-hosting everything

**What continues to work without Nabu Casa:**
Everything. HA is fully functional locally without any subscription. All local automations, integrations, dashboards, and voice (with local STT/TTS) work independently. Nabu Casa is a convenience service and a way to support the project, not a requirement.

---

## Related

- [Core Architecture](../concepts/core-architecture.md) — Understanding what HA is and how it works
- [Backup & Migration](../concepts/backup-migration.md) — HA OS vs Docker migration considerations
- [Voice Assistant](../concepts/voice-assistant.md) — Nabu Casa voice vs local Whisper/Piper
- [Smart Home Protocols](../concepts/protocols.md) — Zigbee vs Matter vs Thread deep dive
