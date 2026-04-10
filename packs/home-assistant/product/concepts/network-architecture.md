---
title: Network Architecture for Smart Homes
type: concept
tags:
- backup-migration
- concepts
- integrations-guide
- network-architecture
- protocols
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/network-architecture
verified_at: '2026-04-10'
verified_by: agent
---
<!-- context: section=concepts, topic=network-architecture, related=protocols,integrations-guide,backup-migration -->
---
sources:
  - type: documentation
    url: "https://www.home-assistant.io/installation/network/"
    date: "2026-03"
  - type: community
    url: "https://community.home-assistant.io/t/vlan-setup-for-home-assistant-iot-isolation/441253"
    date: "2025-09"
  - type: community
    url: "https://www.reddit.com/r/homeassistant/comments/1b9r3x8/complete_network_guide_for_iot/"
    date: "2025-07"
  - type: reference
    url: "https://www.cisecurity.org/insights/white-papers/iot-security-vulnerabilities"
    date: "2025-01"
---

# Network Architecture for Smart Homes

> **Lead summary:** IoT devices are security liabilities. They ship with outdated firmware, default credentials, phone home to foreign servers, and rarely get security updates. The right architecture isolates them: IoT devices live on a separate VLAN with no internet access (or heavily filtered access), HA lives on your trusted network and bridges between the two, and you access HA remotely only via secured tunnels — never by opening port 8123 to the internet. Getting this right protects your whole network from a compromised light bulb.

## Why Network Design Matters

Smart home security incidents are real and documented:
- Cameras phoning home to Chinese servers with your footage
- Light bulbs used as pivot points to attack other LAN devices
- Cheap sensors exfiltrating WiFi credentials during pairing
- Router exploits via UPnP triggered by IoT devices

Even if your specific devices are from reputable manufacturers, network isolation is defense in depth. A compromised IoT device on an isolated VLAN can't:
- Reach your NAS, desktop, or banking computers
- Port-scan your internal network
- Exfiltrate your credentials to the internet (if you block internet access)
- Persist malware on your main hosts

Home Assistant itself needs to sit on the **trusted VLAN** (or its own HA VLAN), with carefully controlled access to the IoT VLAN for polling devices. It does NOT live on the IoT VLAN.

## The VLAN Approach

VLANs (Virtual LANs) are logical network segments. Devices on separate VLANs can't communicate with each other unless your router/firewall explicitly permits it.

**Recommended VLAN structure:**

| VLAN | Name | Devices | Internet | Intranet |
|------|------|---------|----------|----------|
| 1 | Trusted | Computers, phones, NAS, HA | Yes | Full |
| 10 | IoT | Smart plugs, cameras, sensors | Blocked/limited | HA only |
| 20 | Guest | Guest devices | Yes | Blocked |
| 30 | Cameras | IP cameras, NVR | None | NVR only |

**VLAN 10 (IoT) firewall rules:**
- Deny all outbound internet (or allow only specific update servers per device)
- Allow inbound connections from HA's IP address only
- Deny any access to trusted VLAN
- Allow DNS to Pi-hole/AdGuard on trusted VLAN (for DNS-level blocking)

**VLAN 30 (Cameras) is separate from general IoT:**
Cameras generate enormous bandwidth. Keeping them on a dedicated VLAN prevents them from congesting IoT device traffic and makes bandwidth management easier.

**HA's network position:**
HA (on the trusted VLAN) needs to initiate connections INTO the IoT VLAN to poll devices. Your firewall allows: trusted VLAN → IoT VLAN on specific ports (8080 for Shelly, 1883 for MQTT, etc.). IoT VLAN → trusted VLAN is denied by default.

## mDNS and Multicast: The VLAN Discovery Problem

Here's the problem most people hit when setting up IoT VLANs: discovery breaks.

**mDNS (Multicast DNS)** is how devices announce themselves on the local network — how HA finds your Shelly, Chromecast, ESPHome devices, Sonos, etc. when you click "Add Integration." It uses multicast packets, which do not cross VLAN boundaries by default.

When you put your IoT devices on VLAN 10 and HA on VLAN 1, HA can no longer auto-discover those devices. Integration setup will fail.

**Solutions:**

### Option 1: mDNS Reflector / mDNS Repeater

An mDNS reflector forwards mDNS traffic between VLANs. After reflection, HA can see device announcements from the IoT VLAN as if they were on the same network.

**In UniFi:** Enable "mDNS" in Network Settings → your IoT network. UniFi has a built-in mDNS reflector.

**In pfSense/OPNsense:** Install the `avahi` package. Configure it to reflect mDNS between your IoT and trusted interface.

**In OpenWrt:** Install `avahi-daemon`. Configure bridge between interfaces in `/etc/avahi/avahi-daemon.conf`.

### Option 2: Static IP + Avoid mDNS

Once you have DHCP reservations (you should anyway), you can bypass mDNS entirely:
- Configure integrations using the device's IP address directly instead of hostname
- ESPHome: add via IP address, not discovery
- Shelly: add via known IP, not auto-discovery
- Set `scan_interval` appropriately

This requires knowing all your device IPs, which DHCP reservations handle.

### Option 3: Unicast Integration Where Available

Some integrations don't use mDNS at all:
- MQTT-based devices (ESPHome with MQTT transport, Zigbee2MQTT): the broker is on your trusted network, devices push to it
- Zigbee/Z-Wave: not on IP at all (coordinator is USB to HA)
- Cloud-polled integrations: no LAN discovery needed

For a heavily MQTT-based setup, the mDNS problem largely goes away.

## DHCP Reservations: Make Every IoT Device Have a Stable IP

DHCP assigns IPs randomly unless you reserve them. Without reservations:
- A device reboots and gets a new IP
- HA's integration (configured with the old IP) stops working
- Firewall rules (scoped to the old IP) no longer apply
- You spend 20 minutes debugging why your lights are offline

**Every IoT device should have a DHCP reservation** (also called a static DHCP lease). This assigns the same IP every time based on the device's MAC address.

In most router UIs: find the device in the DHCP client list → click "Reserve" or "Static." The device keeps its IP forever.

**Naming convention for reservations:**
```
10.0.10.10  shelly-kitchen-counter
10.0.10.11  shelly-kitchen-dishwasher
10.0.10.20  esphome-office-sensors
10.0.10.50  esp32-voice-kitchen
10.0.10.100 zigbee2mqtt-broker  (HA host)
```

Consistent naming and IP assignment makes firewall rules, debugging, and log reading dramatically easier.

## DNS for IoT Devices

IoT devices "phone home" — they send telemetry, check for updates, and sometimes exfiltrate data to manufacturer servers. DNS-based blocking is your first line of defense.

### Pi-hole or AdGuard Home

Run a DNS sinkhole on your trusted network. Point your IoT VLAN's DNS (via DHCP option 6) to it. The sinkhole blocks known telemetry and ad domains at the DNS level.

**Recommended blocklists for IoT:**
- StevenBlack Hosts (comprehensive)
- hBlock (aggressive)
- IoT-specific lists: search "iot blocklist adguard"

**Caution:** Some IoT devices need specific domains for firmware updates or cloud features. Test after adding blocklists. The approach is: block aggressively, whitelist what breaks.

### Firewall DNS Interception

Even with a DNS sinkhole, devices with hardcoded DNS servers (Google's 8.8.8.8 is hardcoded in many cheap devices) bypass your sinkhole entirely. Intercept these with a firewall redirect rule:

```
# pfSense/OPNsense rule: IoT VLAN
# Redirect all DNS (port 53) to Pi-hole, regardless of destination
Rule: Proto=UDP, Src=IoT_VLAN, Dst=any, DstPort=53, Redirect to Pi-hole:53
```

This forces all DNS through your sinkhole even for devices that ignore DHCP-assigned DNS.

## WiFi Considerations

### 2.4 GHz is the IoT band

The vast majority of IoT devices (Zigbee, WiFi smart plugs, sensors) use 2.4 GHz only. They don't support 5 GHz or 6 GHz. 2.4 GHz also has superior range and wall penetration compared to 5 GHz — important for devices in basements, garages, and far corners.

**Router configuration recommendations:**
- Keep a 2.4 GHz network dedicated to IoT (or use VLAN-tagged SSIDs)
- If using a separate IoT SSID, name it obviously: `HomeNetwork-IoT` vs `HomeNetwork`
- Disable WiFi features that confuse IoT devices: BSS Transition, fast roaming (802.11r), MU-MIMO aggressive settings on IoT SSIDs
- Some IoT devices choke on WPA3. Use WPA2 or WPA2/WPA3 mixed mode for IoT SSIDs

### Separate SSID vs VLAN+SSID

You can implement IoT isolation with just a separate SSID (no VLAN, just a second WiFi network):
- Simpler: no managed switch needed
- Less effective: traffic still traverses the same switch fabric; firewall rules still required
- Most consumer "guest networks" work this way

VLAN + SSID (with VLAN tagging on the access point) is the proper way but requires a managed switch and a router that supports VLAN-tagged DHCP/firewall rules.

## Zigbee and Z-Wave Network Topology

**Critical understanding:** Zigbee and Z-Wave are NOT on your IP network. They are separate mesh networks with their own addressing, routing, and protocols. The only thing that touches your IP network is the coordinator (USB dongle plugged into HA host).

```
[Zigbee/Z-Wave Mesh Network]           [IP Network]
  Sensor → Router → Router →         USB Coordinator → HA host
  Switch → Router → Coordinator  →  (TCP/IP for HA API)
  Bulb → (directly to coordinator)
```

**Implications:**
- VLANs don't affect Zigbee/Z-Wave at all — they're off-network
- "Zigbee VLAN" is not a thing. Don't try to segment them.
- Security threats to Zigbee are different (RF-based) and managed separately
- IoT isolation of WiFi devices doesn't affect Zigbee/Z-Wave security

### USB Extension Cables: The Most Important Hardware Tip

USB 3.0 ports emit significant RF interference in the 2.4 GHz band — the same band as Zigbee (and some Z-Wave frequencies). A Zigbee coordinator plugged directly into a USB 3.0 port on your HA machine will have dramatically reduced range and reliability.

**Solution:** Use a USB 2.0 extension cable (1-2 meters / 3-6 feet) to move the Zigbee/Z-Wave stick physically away from the USB 3.0 ports and the HA host's RF emissions.

This is one of those tips where the impact is massive and counterintuitive. Reports of range doubling and dropped devices reconnecting are common after adding the extension cable.

### Zigbee Channel Selection

Zigbee uses 2.4 GHz and shares the spectrum with WiFi. WiFi channels 1, 6, and 11 (the standard non-overlapping channels in the US) overlap with certain Zigbee channels.

**Zigbee channels that avoid WiFi overlap:**

| Zigbee Channel | Frequency | Clear of WiFi channels |
|---------------|-----------|----------------------|
| **15** | 2425 MHz | Yes — between WiFi ch 1 and 6 |
| **20** | 2450 MHz | Yes — between WiFi ch 6 and 11 |
| **25** | 2475 MHz | Marginal — near WiFi ch 11 |
| **26** | 2480 MHz | Best interference avoidance |

**Recommended:** Use Zigbee channel 25 or 26 if your WiFi uses channels 1/6/11. Check which channels your WiFi uses with a WiFi analyzer app (WiFi Analyzer on Android, NetSpot on macOS).

In ZHA: Settings → Devices & Services → Zigbee Home Automation → Configure → change channel (requires re-joining devices)

In Zigbee2MQTT: Set `channel` in `configuration.yaml`, restart to apply.

## Remote Access: Ranked by Security

Never expose Home Assistant directly to the internet without a security layer. Here are your options, ranked safest to most dangerous:

### 1. Nabu Casa Cloud (Recommended for Most Users)

Nabu Casa creates a secure outbound-only tunnel from HA to their servers. You access HA via `https://[your-id].ui.nabu.casa`. 

**Security model:** HA never opens an inbound port. All connections originate from inside your network. Even if Nabu Casa's servers were compromised, attackers couldn't tunnel back to your HA.

**Cost:** $75/year (includes voice processing)  
**Setup complexity:** One click  
**Requires port forwarding:** No

### 2. VPN (WireGuard or Tailscale)

Connect to your home network via VPN, then access HA as if you're on your LAN.

**WireGuard:** Low-overhead, fast, built into modern Linux kernels. The HA WireGuard add-on makes setup straightforward. Requires opening one UDP port on your router.

**Tailscale:** Zero-config VPN built on WireGuard. No port forwarding required (uses relay servers as fallback). The Tailscale HA add-on exposes HA on your Tailscale network. Free tier is generous.

**Security model:** Even if your VPN credentials are compromised, the attacker gets network access — not direct HA access. Strong when combined with 2FA on HA.

### 3. Reverse Proxy with SSL (Nginx, Caddy, or Nginx Proxy Manager)

Expose HA via HTTPS with a valid SSL certificate and your own domain. Nginx or Caddy handles TLS termination; traffic is forwarded to HA on port 8123 internally.

**Requirements:** A domain name, a router with port 443 forwarding, DDNS if your IP changes, and the Nginx Proxy Manager or Caddy add-on.

**Security additions to implement:**
- Enable HA's `auth:` component for 2FA (TOTP)
- Add IP allowlisting or fail2ban for brute force protection
- Use Cloudflare as the DNS provider + enable "proxy" to mask your home IP

**Setup complexity:** Medium-high. Many tutorials available.

### 4. NEVER: Port-forward port 8123 directly

Port-forwarding your router's port 8123 (or any port) directly to HA means anyone on the internet can attempt to log in. HA's authentication is good but:
- Brute force attacks happen constantly on port 8123
- If a vulnerability is disclosed in HA, you're exposed until you patch
- No defense in depth

**This is the most common dangerous mistake in HA setups.** If someone in a forum tells you to "just open port 8123 in your router," don't. Use any of options 1-3 instead.

## IP Camera Architecture

Cameras deserve special network treatment:

**Put cameras on a dedicated VLAN (suggested VLAN 30):**
- Cameras generate 1-4 Mbps each continuously. Ten cameras = 10-40 Mbps of constant traffic. Keeping them segregated prevents congestion on other networks.
- No internet access: most cameras don't need internet for local recording. Block it entirely unless firmware updates require it.
- Block access to all VLANs except the NVR's IP.

**Use a local NVR (Network Video Recorder):**
- [Frigate](https://frigate.video) NVR running as a HA add-on or on a separate host
- Record locally, not to the cloud (Nest Cam cloud, Ring, Arlo cloud all have privacy implications)
- Frigate can do object detection with a Coral TPU (~$60) for "person detected" vs "motion detected"

**Don't route camera streams through HA:**
HA can display camera feeds in dashboards, but the video data should stream directly from the camera/NVR to your browser via the `camera_proxy` or `generic` camera integration. Don't process camera video through the HA event loop — it's a Python process not designed for video bandwidth.

## Hardware Recommendations

Getting the right hardware matters enormously for IoT network architecture.

**Router (the most important component):**
- Not your ISP-provided device. ISP routers rarely support VLANs, have poor firewall capability, and get infrequent security updates.
- **UniFi Dream Router / Dream Machine:** Best GUI, excellent VLAN support, integrated WiFi, active development. Community favorite.
- **GL.iNet Flint 2:** OpenWrt-based, more affordable ($80-120), strong VLAN/firewall support.
- **pfSense/OPNsense appliance:** Maximum control, firewall-grade, steeper learning curve.
- **OpenWrt on compatible router:** Free, very capable, large community. Check router support at openwrt.org.

**Managed switch (for VLAN trunking):**
If you have wired devices, a managed switch lets you assign switch ports to specific VLANs. Cheap TP-Link TL-SG108E (~$30) or Netgear GS308E (~$35) handle basic VLAN tagging well.

**Access points (for multi-room WiFi with VLAN-tagged SSIDs):**
UniFi access points are the community standard — they handle VLAN-tagged SSIDs with excellent reliability. The UniFi U6 Lite (~$90) is a reasonable entry point. OpenWrt-capable APs (GL.iNet MT3000) work if you prefer open firmware.

## Related

- [[esphome-fundamentals.md|ESPHome Fundamentals]] — ESP32 sensors that work with MQTT (less mDNS dependency)
- [[integrations-guide.md|Integration Guide]] — Integration-specific network requirements
- [[backup-migration.md|Backup & Migration]] — Keeping your HA config safe during network changes
