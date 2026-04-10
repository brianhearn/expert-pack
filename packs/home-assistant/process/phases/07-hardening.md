---
title: "Phase 7: Hardening"
type: "phase"
tags: [07-hardening, phases]
pack: "home-assistant-process"
retrieval_strategy: "atomic"
id: home-assistant/process/phases/07-hardening
verified_at: '2026-04-10'
verified_by: agent
---
# Phase 7: Hardening

## Goal

Make your smart home **resilient, secure, and maintainable**. This phase ensures that when something breaks (and something will), you can recover quickly. It also closes security gaps that could expose your home network to the internet.

This phase is never fully "done" — it's an ongoing practice. But the checklist below gets you to a solid baseline.

## Prerequisites

- Phases 1-6 complete (running, stable, feature-complete)
- At least a few weeks of daily use (you know what breaks and what doesn't)

---

## Part 1: Backups

Your HA configuration is months of work. Losing it means starting over. Automated backups take 10 minutes to configure and could save you days.

### What's in an HA Backup

HA backups include:
- All configuration files (`configuration.yaml`, automations, scripts, scenes)
- Add-on data (Zigbee2MQTT database, MQTT broker settings, ESPHome device configs)
- Integrations and their authentication tokens
- HA database (history, logbook data)
- Custom components and Lovelace dashboards

Backups do **not** include external hardware state (Zigbee device pairing is in the Z2M database, which IS backed up; the devices themselves obviously aren't).

### Option A: Automatic Google Drive/OneDrive Backup (Easiest)

Install the **Samba Backup** or **Google Drive Backup** add-on:

1. **Settings → Add-ons → Add-on Store → Google Drive Backup** (search: "Google Drive Backup")
2. Install and configure:
   ```yaml
   max_backups_in_ha: 3       # Keep 3 local copies
   max_backups_in_google_drive: 30  # Keep 30 in the cloud
   backup_time_of_day: "03:00"      # Run at 3am daily
   ```
3. Authenticate with Google and authorize the folder
4. Verify: the add-on creates a test backup within 5 minutes

### Option B: NAS/Network Share Backup

If you have a Synology or other NAS:

1. Install the **Samba Backup** add-on
2. Point it at your NAS share
3. Configure daily schedule and retention

### Manual Backup Before Changes

**Always create a manual backup before:**
- HA version upgrades
- Major YAML edits
- Add-on updates
- Hardware changes

```
Settings → System → Backup → Create Backup
```

Label it with the reason: `2026-03-11 before upgrade to 2026.3`

### Test Your Backups

A backup is worthless if you can't restore from it. Once a quarter:
1. Download a backup file to your laptop
2. Verify the file is not corrupted (it's a tar file — you can open it)
3. Optionally, do a full test restore on a VM

---

## Part 2: Remote Access

Accessing HA from outside your home without opening ports is the safe approach. Two main options:

### Option A: Nabu Casa (Recommended for Most)

$7/month gets you:
- Encrypted remote access with no port forwarding
- Google Home and Alexa integration
- Nabu Casa cloud for voice assistant STT/TTS

Setup: Settings → Home Assistant Cloud → Sign In

**Pros:** Dead simple, no network config, officially supported, encrypted.  
**Cons:** Paid, depends on Nabu Casa's infrastructure.

### Option B: Cloudflare Tunnel (Free Self-Hosted)

For users who don't want a subscription:

1. Create a free Cloudflare account and add your domain
2. Install the **Cloudflare Tunnel** add-on in HA
3. Configure the tunnel to point at `http://homeassistant.local:8123`
4. Set `trusted_proxies` in `configuration.yaml`:
   ```yaml
   http:
     use_x_forwarded_for: true
     trusted_proxies:
       - 172.30.33.0/24  # HA internal network
   ```
5. Enable 2FA on your HA account (required when exposing to internet)

### ⚠️ What Not to Do

- **Don't forward port 8123 directly to the internet.** HA's web UI exposed directly is a security risk. Brute-force attacks on HA instances are common.
- **Don't disable authentication** even on your local network for convenience.
- **Don't use plain HTTP for remote access** — always HTTPS.

---

## Part 3: Security Hardening

### Strong Authentication

1. **Enable 2FA for all admin accounts:**  
   Profile → Security → Enable multi-factor authentication → TOTP (Google Authenticator, Authy)
   
2. **Create separate accounts for family members** — never share the admin account. Regular users can control devices but can't change settings.

3. **Restrict admin access via network:** In `configuration.yaml`:
   ```yaml
   homeassistant:
     auth_providers:
       - type: homeassistant
   ```

### User Account Roles

| Role | Can Do | Can't Do |
|------|--------|----------|
| Owner | Everything | N/A |
| Administrator | Manage settings, users, add-ons | Remove owner |
| User | Control devices, view dashboards | Change settings, add devices |

Create user accounts for household members: Settings → People → Add Person → Create Login

### IoT Network Isolation

If you haven't already (from Phase 1 planning):
- Put Wi-Fi smart devices (plugs, cameras, bulbs with proprietary apps) on an IoT VLAN
- Zigbee and Z-Wave devices don't need network isolation — they connect to your coordinator, not the internet
- Block IoT VLAN devices from accessing your trusted VLAN except via HA

### Disable Unused Integrations

Each integration is an attack surface. If you added something to try it and don't use it:
Settings → Devices & Services → [Integration] → Delete

---

## Part 4: System Health Monitoring

Set up automations that tell you when something is wrong.

### Low Battery Alert

```yaml
- alias: "Alert — Low Battery Devices"
  trigger:
    - platform: numeric_state
      entity_id: sensor.low_battery_count  # Template sensor from Phase 5
      above: 0
  condition:
    - condition: time
      after: "09:00:00"
      before: "20:00:00"
  action:
    - service: notify.mobile_app_my_phone
      data:
        title: "Low Battery"
        message: "{{ states('sensor.low_battery_count') }} device(s) need new batteries"
```

### Unavailable Device Alert

```yaml
- alias: "Alert — Devices Unavailable"
  trigger:
    - platform: state
      entity_id:
        - binary_sensor.front_door
        - binary_sensor.back_door
        - binary_sensor.garage_door
      to: "unavailable"
      for:
        minutes: 10
  action:
    - service: notify.mobile_app_my_phone
      data:
        title: "Device Offline"
        message: "{{ trigger.to_state.name }} is unavailable for 10+ minutes"
```

### HA Update Available

```yaml
- alias: "Alert — HA Update Available"
  trigger:
    - platform: state
      entity_id: update.home_assistant_core_update
      to: "on"
  action:
    - service: notify.mobile_app_my_phone
      data:
        title: "HA Update Available"
        message: "Home Assistant {{ state_attr('update.home_assistant_core_update', 'latest_version') }} is ready to install"
```

---

## Part 5: Maintenance Routine

The "set it and forget it" smart home is a myth. Schedule regular maintenance:

| Frequency | Task |
|-----------|------|
| **Daily** (automated) | Automated backup runs at 3am |
| **Weekly** | Check logbook for unusual state changes or errors |
| **Monthly** | Install HA updates (after reading release notes) |
| **Monthly** | Check device battery levels |
| **Quarterly** | Review and clean up unused automations |
| **Quarterly** | Test backup restore |
| **Yearly** | Review access — revoke unused API tokens, update passwords |

---

## Hardening Checklist

- [ ] Automated daily backups to cloud or NAS
- [ ] Manual backup tested (can actually restore from it)
- [ ] Remote access via Nabu Casa or Cloudflare Tunnel — NOT direct port forwarding
- [ ] HTTPS enforced for all remote access
- [ ] 2FA enabled on owner account
- [ ] Separate user accounts for each household member
- [ ] Admin access restricted (no shared admin password)
- [ ] Low battery alert automation running
- [ ] Unavailable device alert for critical sensors
- [ ] HA update available notification configured
- [ ] Monthly update schedule in calendar

## You're Done (For Now)

Completing Phase 7 means you have a smart home that:
- ✅ Runs locally without cloud dependencies
- ✅ Backs itself up automatically
- ✅ Notifies you when something goes wrong
- ✅ Recovers from a hardware failure within an hour
- ✅ Is accessible remotely without exposing your network
- ✅ Has proper user separation

The journey doesn't end here — the HA community is constantly expanding what's possible. But you now have the solid foundation to explore safely.
