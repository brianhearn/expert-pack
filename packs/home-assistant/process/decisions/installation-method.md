---
title: 'Decision: Installation Method'
type: decision
tags:
- decisions
- installation-method
pack: home-assistant-process
retrieval_strategy: standard
id: home-assistant/process/decisions/installation-method
verified_at: '2026-04-10'
verified_by: agent
---
# Decision: Installation Method

## The Decision

Which flavor of Home Assistant should you install — HA OS, Supervised, Container, or Core?

This is arguably the most important decision you'll make. It determines what features you can use, how much maintenance work you'll do, and whether you can use the full add-on ecosystem (ESPHome, Zigbee2MQTT, Frigate, etc.).

---

## The Four Installation Methods

### Home Assistant OS (HAOS)

**What it is:** A minimal Linux distribution purpose-built to run Home Assistant. Includes the Supervisor — HA's own operating system management layer — with full add-on support, OTA OS updates, and integrated backup management.

**How it works:** You flash HAOS directly to your storage device (SSD, SD card, or VM disk). HA controls the entire OS. You don't have a general-purpose Linux shell unless you specifically install the SSH add-on.

**Add-on support:** ✅ Full — the Supervisor manages Docker containers on your behalf. All official and community add-ons work.

**Operating system updates:** ✅ Automatic — HA can update its own OS without manual intervention.

**Backups:** ✅ Full — backups include OS configuration, HA config, and add-on data.

**Supports:**
- Raspberry Pi (all models with 64-bit support)
- Generic x86-64 (mini-PCs, NUCs, bare-metal servers)
- ODROID, Khadas, and other supported ARM boards
- VMs on Proxmox, VMware, Hyper-V, and VirtualBox

**Doesn't support:**
- Synology NAS (officially) — use Container instead
- Systems running other full operating systems

**Best for:** Everyone who doesn't have a specific reason to choose a different method. Beginners should always start here.

**Tradeoff:** You don't get a general-purpose Linux shell. If you want to run other software on the same machine, you'll need SSH + Terminal add-on or run HA in a VM alongside other workloads.

---

### Supervised

**What it is:** HA Supervisor + Add-ons running on top of a standard Debian Linux installation. Gives you full add-on support AND a general-purpose Linux system.

**How it works:** You install Debian, then install the HA Supervised installer on top of it. The Supervisor manages HA as if it were HAOS, but you retain access to the underlying OS.

**Add-on support:** ✅ Full — same as HAOS.

**OS requirements (strict):** Only **Debian (latest stable)** with specific package versions. The Supervised installation has strict requirements — other distros (Ubuntu, Raspberry Pi OS) are not supported and will cause the Supervisor to flag your installation as "Unsupported."

**Unsupported state:** If you deviate from the requirements (wrong Docker version, extra packages that modify the network stack, etc.), the Supervisor flags your instance as "Unsupported." You can still run HA, but you won't get support and some Supervisor features may not work.

**Best for:** Linux power users who want full add-on support but also need a general-purpose Debian server on the same hardware. Not for beginners.

**Tradeoff:** More maintenance burden. You own the OS, which means OS security patches, dependency management, and avoiding changes that break the Supervisor's requirements. HA's OS-level updates don't apply — you manage Debian yourself.

---

### Container

**What it is:** Home Assistant Core running in a Docker container. No Supervisor, no add-ons, no integrated backup.

**How it works:** You run the `homeassistant/home-assistant` Docker container yourself, manage the configuration manually, and integrate with any other Docker services through your own compose files.

**Add-on support:** ❌ None — add-ons are Supervisor-managed containers. Without the Supervisor, you must manually run equivalent Docker containers for things like Mosquitto, Zigbee2MQTT, ESPHome, and Frigate. Each needs its own Docker config and you manage the networking between them.

**OS updates:** ❌ Manual — you manage the container lifecycle, pull new images, and restart services yourself.

**Backups:** ❌ No integrated backup — you back up your configuration directory (`~/.homeassistant/` or equivalent volume mount) with your own tooling (rsync, Duplicati, etc.).

**Best for:**
- Synology NAS users running the Container Manager / Docker package
- Users who already run a Docker/Compose homelab and want HA integrated into it
- Users who specifically don't want HAOS to own their server

**Tradeoff:** Significantly more manual work. You're assembling pieces yourself. Zigbee2MQTT, Mosquitto, ESPHome — each is its own Docker container you configure. Not hard once you know Docker, but it's more work and more things to maintain.

---

### Core

**What it is:** HA Core installed directly as a Python application in a virtual environment. No Docker, no Supervisor, no add-ons.

**How it works:** Python venv, manual pip install, run as a systemd service. You manage everything manually.

**Add-on support:** ❌ None.

**Best for:** Python developers who want to contribute to HA, or who need to run HA in a very constrained environment where Docker isn't available.

**Tradeoff:** The most maintenance burden. Not recommended for home use unless you specifically know why you want this.

---

## Comparison Table

| Feature | HA OS | Supervised | Container | Core |
|---------|-------|-----------|-----------|------|
| **Full add-on support** | ✅ | ✅ | ❌ | ❌ |
| **Auto OS updates** | ✅ | ❌ (you manage) | ❌ | ❌ |
| **Integrated backup** | ✅ | ✅ | ❌ | ❌ |
| **General-purpose Linux** | ❌ | ✅ | ✅ (host) | ✅ |
| **NAS / Docker friendly** | ❌ | ❌ | ✅ | ❌ |
| **Setup complexity** | ✅ Easy | ⚠️ Medium | ⚠️ Medium | ❌ Hard |
| **Maintenance burden** | ✅ Low | ⚠️ Medium | ⚠️ Medium | ❌ High |
| **Official support** | ✅ Full | ✅ (on Debian) | ✅ | ✅ |

---

## Recommended Add-Ons (Only Available on HAOS/Supervised)

These add-ons are major reasons to choose HAOS or Supervised. Without them, you're doing equivalent setup manually:

| Add-on | Purpose | Effort Without It |
|--------|---------|------------------|
| **Zigbee2MQTT** | Zigbee coordinator management | Manual Docker container |
| **Mosquitto MQTT** | MQTT broker | Manual Docker container |
| **ESPHome** | ESP32/ESP8266 device management | Separate ESPHome server |
| **Frigate NVR** | AI-powered camera/video monitoring | Complex standalone setup |
| **Node-RED** | Advanced flow-based automation | Standalone Node-RED + integration |
| **Terminal & SSH** | Command line access to HA | Not applicable |
| **Google Drive Backup** | Automated cloud backups | DIY rsync/rclone script |
| **Piper / Whisper** | Local TTS/STT for voice assistant | Standalone Python services |

---

## The Decision for Most People

**Use HA OS.** Unless you have an existing Docker homelab on a NAS (use Container) or you're a Linux admin who specifically wants to run other services on the same bare-metal machine (use Supervised on Debian).

The add-on ecosystem — especially ESPHome, Zigbee2MQTT, Frigate, and the local voice stack — is too valuable to give up without a strong reason.

### Decision Flowchart

```
Do you have an existing Synology/QNAP NAS?
├─ Yes → Use Container (Docker on NAS)
└─ No → Do you want to run other Linux services on the same hardware?
    ├─ Yes, I'm a Debian admin → Use Supervised (on Debian)
    └─ No → Use HA OS
```

→ See [[01-planning.md|Phase 1: Planning]] for hardware recommendations that pair well with HAOS.
