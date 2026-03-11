# Decision: Hardware Selection

## The Decision

What hardware should you run Home Assistant on? This determines performance, cost, reliability, and whether you'll hit resource ceilings as your smart home grows.

The decision has three dimensions: **form factor** (what hardware), **storage** (SSD vs SD card), and **resource budget** (how much CPU/RAM you'll actually need).

---

## The Options

### Raspberry Pi 5 (4GB or 8GB)

**Price:** ~$60 (4GB) + SSD + case + PSU = ~$120 total

The current flagship Pi. Significantly faster than Pi 4 with a proper ARM Cortex-A76 quad-core CPU and PCIe support for NVMe SSDs (via HAT).

**Pros:**
- Compact, quiet, low power (~5-8W idle)
- Official HA OS images available
- Large community support
- PCIe HAT supports NVMe SSDs — finally proper SSD speeds for Pi
- Active thermal management (Pi 5 has a power button and improved thermals)

**Cons:**
- More expensive than Pi 4 relative to what you get
- PCIe NVMe HAT adds $20-40
- GPIO hats for external sensors less critical in a HA context

**RAM recommendation:** Get **8GB if you plan to run Frigate** (AI camera NVR) or many add-ons. 4GB is fine for most setups (Zigbee2MQTT, Mosquitto, ESPHome, and the voice stack fit comfortably in 3GB).

**Storage:** Use USB 3.0 SSD (not SD card) or NVMe via Pi 5 HAT. See Storage section below.

---

### Raspberry Pi 4 (4GB or 8GB)

**Price:** ~$40-55 (4GB) + SSD + case + PSU = ~$90-110 total

Still fully capable for most HA setups. Slightly slower than Pi 5 but well-tested and widely available.

**Pros:**
- Cheaper than Pi 5
- Proven stability — most HA Pi tutorials target Pi 4
- Wide accessory ecosystem

**Cons:**
- USB 3.0 SSD (recommended) — no PCIe, so NVMe requires a USB 3.0 adapter
- Gets hot under heavy load — needs a case with cooling

**Best for:** Budget-conscious new builds or if Pi 5 is out of stock.

---

### Raspberry Pi 3 / Zero 2W

**Not recommended for production HA.** The Pi 3B+ has 1GB RAM and a 32-bit CPU. HA now recommends 64-bit only, and 1GB RAM is tight once you add ESPHome, Zigbee2MQTT, and a voice stack.

Use Pi 4 or Pi 5 minimum.

---

### Intel N-series Mini-PC (N100, N5105, N95, N200)

**Price:** $80-150 (used or from AliExpress/Amazon)

The best bang-for-buck option. Intel N-series Celeron/Pentium processors outperform Pi 5 in multi-threaded workloads, support 8-16GB RAM, and include proper NVMe slots and multiple USB ports.

**Examples:** Beelink Mini S12, GMKtec NucBox, Trigkey G5, Minisforum N100 — dozens of similar units from various brands.

**Pros:**
- More CPU headroom for Frigate, Whisper STT, and AI workloads
- 8-16GB RAM — can run Proxmox/VMs plus HA
- Real NVMe SSD slot — fast and reliable
- Multiple USB ports (less USB hub management)
- Runs on 12-20W — still low power, comparable to Pi 5

**Cons:**
- Larger than a Pi (still small — about the size of a thick paperback)
- No HA OS bare-metal image for every model — may need to boot from USB installer
- More research required to confirm HA OS compatibility for specific model

**Best for:** Users who want more headroom, plan to run Frigate with AI cameras, or want to run Proxmox and dedicate a VM to HA.

---

### Intel NUC or Similar (i3/i5/i7)

**Price:** $150-400+ (new), $100-200 (used Gen 8-10 on eBay)

Overkill for a basic HA setup but good if you have one or want to run multiple VMs.

**Pros:**
- Excellent performance — Whisper large-v3 STT, Frigate with GPU, multi-VM
- Reliable hardware from a known manufacturer
- Used Gen 8/10 NUCs are affordable

**Cons:**
- Higher idle power than mini-PC or Pi (15-30W)
- Expensive compared to N-series mini-PCs that match most of the performance

**Best for:** Power users running Proxmox with multiple VMs (HA + Frigate + other services).

---

### Existing NAS (Synology, QNAP, TrueNAS)

**Price:** $0 extra (if you have a NAS)

If you have a NAS with Docker support, running HA as a Container is a natural fit. Synology DS220+/DS920+ and newer models support Docker Manager.

**Pros:**
- No extra hardware
- NAS handles backups natively
- Always-on anyway

**Cons:**
- Container install only — no HA OS add-ons (Zigbee2MQTT, ESPHome must be separate containers)
- NAS performance can suffer when HA runs heavy processing alongside storage workloads
- USB passthrough for Zigbee dongle can be awkward on some NAS models

**Best for:** Users who already have a capable NAS and are comfortable with Docker Compose.

---

### VM (Proxmox, VMware, Hyper-V, VirtualBox)

**Price:** $0 extra (if you have the hardware)

Running HA OS as a VM gives you snapshots, easy migration, and the full HAOS experience on shared hardware.

**Pros:**
- Snapshots before updates — instant rollback
- Easy migration to new hardware
- Full HA OS add-on support
- Run other VMs/containers on the same server

**Cons:**
- USB passthrough for Zigbee dongle requires careful Proxmox/VM configuration
- Hardware cost of the hypervisor host
- More complexity to manage

**Proxmox USB passthrough for Zigbee dongle:**
```
1. Identify USB device: lsusb
2. In Proxmox VM → Hardware → Add USB Device → Choose specific device
3. In HA VM, verify dongle appears: ls /dev/serial/by-id/
```

**Best for:** Homelab users who already run Proxmox or VMware.

---

## Storage: SSD vs SD Card

**This is not optional: use an SSD.**

| Storage Type | Lifespan in HA | Why |
|-------------|---------------|-----|
| SD Card | 6-18 months | HA writes to its SQLite database constantly — SD cards aren't rated for high write endurance and fail unpredictably |
| USB 3.0 SSD | 5+ years | SSDs handle write loads easily; even budget SSDs outlast SD cards by orders of magnitude |
| NVMe SSD (Pi 5 HAT / Mini-PC) | 5-10+ years | Best performance and longevity |

**Recommended SSDs for Pi (USB 3.0):**
- Samsung T7 250GB ($35)
- Crucial X6 500GB ($40)
- Any SSD in a USB 3.0 enclosure (ORICO, Sabrent)

**If your Pi still has only an SD card:** Your HA database is at risk of corruption on every unexpected power loss. Migrate to SSD using the built-in HA backup/restore — back up, install fresh on SSD, restore. Takes 30 minutes and is worth doing immediately.

---

## RAM Requirements by Workload

| Workload | Minimum RAM | Recommended RAM |
|---------|-------------|----------------|
| Basic HA + Zigbee2MQTT + Mosquitto | 2GB | 4GB |
| + ESPHome + 10 add-ons | 2GB | 4GB |
| + Local voice (Whisper tiny/base) | 2GB | 4GB |
| + Local voice (Whisper medium/large) | 4GB | 8GB |
| + Frigate NVR (CPU-only) | 4GB | 8GB |
| + Frigate NVR (with Coral TPU) | 4GB | 8GB |
| + Frigate NVR (with GPU/iGPU) | 8GB | 16GB |
| Proxmox VM with multiple services | 8GB | 16GB+ |

---

## Decision Summary

| If you... | Choose |
|-----------|--------|
| Want the simplest setup, new to HA | Raspberry Pi 5 (4GB) + USB SSD |
| Want best value for a standalone build | Used Intel N100 mini-PC + HA OS |
| Run Proxmox or VMware already | VM with HAOS image |
| Have a Synology NAS | Container on NAS + separate Pi for coordinator |
| Plan heavy AI workloads (Frigate, Whisper large) | NUC i5+ or N100 with 16GB RAM |
| Have a Pi 4 gathering dust | Flash HA OS + USB SSD — works great |

**The most common regret:** Starting on an SD card. Don't. Buy the SSD at the same time as the Pi.

→ See [Phase 1: Planning](../phases/01-planning.md) for the full checklist before you start.
