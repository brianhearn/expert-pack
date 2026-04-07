---
title: 'Phase 2: Initial Setup'
type: phase
tags:
- 02-initial-setup
- phases
pack: home-assistant-process
retrieval_strategy: atomic
---
# Phase 2: Initial Setup

## Goal

Get Home Assistant running, connected to your network, and handling its first integrations. By the end of this phase you'll have a working HA instance, the companion app on your phone, and 2-3 non-critical integrations configured.

## Prerequisites

- Hardware ready (from Phase 1)
- USB Zigbee/Z-Wave coordinator on hand
- Static IP planned for HA server
- 30-60 minutes of uninterrupted time for the initial setup

---

## Step 1: Flash and Boot HA OS

### For Raspberry Pi or Mini-PC with HA OS

1. Download the HA OS image from [home-assistant.io/installation](https://www.home-assistant.io/installation/)
   - For Pi: choose the `.img.xz` file for your Pi model
   - For x86-64 mini-PC: choose the `.img.xz` for generic x86-64
2. Flash to your SSD using **Balena Etcher** (free, works on Windows/Mac/Linux)
   - If using a Pi with USB SSD: flash directly to the SSD, then connect SSD to Pi
   - If using a mini-PC: flash to a USB stick, boot from it, install to the internal SSD via the installer
3. Connect ethernet (not Wi-Fi for initial setup — more reliable)
4. Power on and wait 5-10 minutes for first boot
5. Access at `http://homeassistant.local:8123` — if that doesn't work, use the IP address directly

### For Proxmox/VM

1. Download the HAOS `.vmdk` or `.qcow2` image
2. Create a new VM (minimum: 2 cores, 2GB RAM, 32GB disk)
3. Import the disk image and boot
4. Access at the VM's IP on port 8123

---

## Step 2: Onboarding Wizard

The first-run wizard takes about 5 minutes:

1. **Create your owner account** — this is the admin account; use a strong password
2. **Name your home** — shown throughout the UI
3. **Set your location** — used for sunrise/sunset automations and weather
4. **Set your timezone** — critical for scheduled automations
5. **Auto-discovered devices** — HA will show devices it found on your network; you can add them now or skip
6. **Allow telemetry** — optional; sends anonymous usage stats to the HA project

> ⚠️ **Don't rush through location and timezone** — incorrect settings cause automation failures that are frustrating to debug later.

---

## Step 3: Configure Your First Integrations

After onboarding, go to **Settings → Devices & Services → Add Integration**.

### Recommended First Integrations

**Start with what you already have on the network:**

| Integration | What It Does | Priority |
|-------------|--------------|----------|
| **Google Cast** | Control Google/Chromecast speakers | High |
| **Philips Hue** (if you have it) | Hue bridge integration | High |
| **HACS** (Home Assistant Community Store) | Enables 3rd-party integrations and cards | High |
| **Mobile App** | Companion app for phone sensors/notifications | High |
| **Meteorologisk institutt / OpenWeatherMap** | Local weather | Medium |
| **CO2 Signal** | Grid carbon intensity (for energy monitoring) | Low |

### Installing HACS

HACS (Home Assistant Community Store) unlocks hundreds of custom integrations and Lovelace cards not in the official store. Install it early.

1. Go to **Settings → Add-ons → Add-on Store**
2. Install the **Terminal & SSH** add-on (needed for HACS install)
3. Open the Terminal and run:
   ```bash
   wget -O - https://get.hacs.xyz | bash -
   ```
4. Restart HA when prompted
5. Go to **Settings → Devices & Services → Add Integration → HACS**
6. Authenticate with GitHub (requires a free GitHub account)

> HACS integrations are not officially supported by the HA team. They're community-maintained. This is fine — most popular ones are well-maintained.

---

## Step 4: Install the Companion App

The HA Companion App turns your phone into a smart home sensor. Install it early — it's your primary control interface.

1. Install **Home Assistant** from the App Store (iOS) or Play Store (Android)
2. Open the app and it will auto-discover your HA instance on the local network
3. Log in with your owner credentials
4. **Grant all permissions** when prompted — each permission enables a sensor type:
   - Location → presence detection
   - Motion/activity → activity sensors
   - Battery → battery status sensor
   - Notifications → HA can push alerts to your phone

After setup, your phone appears in HA as a device with 20-40 sensors (battery level, GPS location, WiFi SSID, call state, step count, etc.).

---

## Step 5: First Configuration Check

Before adding more devices, verify the basics work:

1. **Restart works:** Settings → System → Restart. Confirm HA comes back up in ~60 seconds.
2. **Check config is valid:** Settings → System → Check Configuration. Should show "Configuration valid."
3. **Backup works:** Settings → System → Backup → Create Backup. Verify it completes.
4. **Update HA:** Settings → System → Updates. Install any pending updates before going further.

---

## Step 6: Enable Advanced Mode (Recommended)

HA hides some advanced settings by default. Enable them now:

1. Click your user profile (bottom left)
2. Scroll down to **Advanced Mode** and toggle it on

This unlocks the YAML editor for automations, template testing, and other power-user features you'll need later.

---

## Checklist

- [ ] HA OS installed and accessible at a static IP
- [ ] Onboarding completed (location, timezone, account)
- [ ] HACS installed
- [ ] Companion app installed and connected on your main phone
- [ ] First backup created
- [ ] HA updated to latest version
- [ ] Advanced Mode enabled
- [ ] 2-3 existing devices integrated (start easy — things already on your network)

## What's Next

→ [[03-protocol-setup.md|Phase 3: Protocol Setup]] — Add your Zigbee/Z-Wave coordinator and start pairing smart devices
