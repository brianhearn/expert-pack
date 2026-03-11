# Phase 1: Planning

## Goal

Make three key decisions before spending money: **what hardware to run HA on**, **which installation method to use**, and **how to structure your network**. These choices shape everything downstream.

## Prerequisites

None — this is the starting point.

## Outputs

- Hardware selected and ordered (or repurposed)
- Installation method chosen
- Network plan sketched (VLANs, IP reservations, where the hub will live)

---

## Step 1: Choose Your Hardware

Your HA server needs to run 24/7. It needs enough CPU and RAM to handle integrations, automations, and add-ons without lag. It also needs reliable storage — SD cards fail; SSDs don't.

### Quick Guide

| Option | Cost | Best For |
|--------|------|----------|
| Raspberry Pi 5 (4GB) + SSD | ~$120 | Clean new builds, physically small |
| Used mini-PC (Intel N-series) | $80-150 | Best price/performance, easy SSD upgrade |
| NUC or similar Intel small form factor | $150-300 | Power users, heavy add-on load |
| Synology NAS (existing) | $0 extra | NAS owners who want Docker/Container install |
| VM (Proxmox, VMware, Hyper-V) | $0 if hardware exists | Server homelab users |

**Best choice for most new builds:** Raspberry Pi 5 with a 128GB+ SSD via USB3, or a used Intel N100 mini-PC from Amazon. Both support HA OS natively.

**What to avoid:**
- Raspberry Pi 3 or earlier — too slow for modern HA with add-ons
- SD card storage on any Pi — they fail within 6-18 months under HA's write load
- 32-bit ARM boards — limited add-on support
- Shared servers running other production workloads

→ See [Hardware Selection Decision](../decisions/hardware-selection.md) for full comparison and buying advice.

---

## Step 2: Choose Your Installation Method

Home Assistant comes in four flavors. The differences are significant.

| Method | Full Add-on Support | HA OS Updates | Supervisor | Best For |
|--------|--------------------:|:-------------:|:----------:|----------|
| **HA OS** | ✅ Yes | ✅ Yes | ✅ Yes | Most users |
| **Supervised** | ✅ Yes | ❌ Manual | ✅ Yes | Linux power users (strict reqs) |
| **Container** | ❌ Limited | ❌ Manual | ❌ No | Docker users, NAS |
| **Core** | ❌ None | ❌ Manual | ❌ No | Python devs, advanced only |

**Recommendation:** Choose **HA OS** unless you have a specific reason not to. It's the only method where you get full add-on support (ESPHome, Zigbee2MQTT, Frigate, etc.), automatic OS-level updates, and official Supervisor support. The tradeoff — you don't have general OS access — is rarely a problem in practice.

→ See [Installation Method Decision](../decisions/installation-method.md) for detailed tradeoffs.

---

## Step 3: Plan Your Network

A smart home adds dozens of devices to your network. Doing this thoughtlessly causes security risks and troubleshooting nightmares.

### IP Address Reservations

Your HA server should have a **static IP** (either assigned via DHCP reservation or configured statically). You'll be accessing it constantly — a changing IP is painful.

**How:** Log into your router, find the HA server's MAC address (once it's running), and assign it a fixed IP. Common choices: `192.168.1.100` or `192.168.1.50`.

### VLAN Segmentation (Optional but Recommended)

For security-conscious setups, consider putting IoT devices on a separate VLAN:

- **VLAN 1 (Trusted):** PCs, phones, HA server
- **VLAN 10 (IoT):** Wi-Fi smart devices (plugs, bulbs, cameras)
- **Firewall rule:** IoT devices can't initiate connections to trusted VLAN; HA server can reach IoT VLAN

This matters most for Wi-Fi devices from unknown manufacturers. Zigbee and Z-Wave devices connect directly to your coordinator (plugged into HA), so they never touch your Wi-Fi at all — that's one reason Zigbee is preferred.

### Where to Place the HA Server

The Zigbee/Z-Wave coordinator (a USB dongle) needs to be physically near the HA server. Place the server:

- Centrally in the home if possible (better Zigbee mesh coverage)
- Away from 2.4GHz Wi-Fi access points (interference with Zigbee)
- On a UPS (uninterruptible power supply) — power blips cause SD card corruption and HA crashes

### Ports to Know

| Purpose | Port | Notes |
|---------|------|-------|
| HA Web UI | 8123 | Default; accessed from your LAN |
| ESPHome devices | 6052 | ESPHome Dashboard add-on |
| MQTT broker | 1883 | Mosquitto add-on (unencrypted) |
| MQTT TLS | 8883 | For external clients |

---

## Step 4: Protocol Selection

While planning, decide which smart home protocol you'll lead with. This determines which coordinator USB dongle you need before you can buy devices.

**TL;DR for most people:** Start with **Zigbee**. It's cheap, local, mature, and has the largest device ecosystem.

→ See [Protocol Selection Decision](../decisions/protocol-selection.md) for full Zigbee vs Z-Wave vs Wi-Fi vs Thread/Matter comparison.

---

## Checklist

- [ ] Hardware selected (or existing hardware identified)
- [ ] SSD ordered (if using a Pi or Pi-sized board)
- [ ] USB Zigbee coordinator ordered (e.g., SMLIGHT SLZB-07, Sonoff Dongle Plus-P, or Aeotec Z-Stick 7 for Z-Wave)
- [ ] Installation method chosen (recommend: HA OS)
- [ ] HA server will have a static IP
- [ ] UPS ordered or planned for server
- [ ] Physical location for server identified

## What's Next

→ [Phase 2: Initial Setup](02-initial-setup.md) — Install HA OS and configure your first integrations
