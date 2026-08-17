---
title: "DHCP Reservations and IoT DNS"
type: concept
tags:
  - network-architecture
  - dhcp
  - pihole
  - adguard
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/network-dhcp-dns
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - network-vlan.md
  - network-mdns.md
  - network-wifi.md
content_hash: sha256:9dc916a4f4a0e30900e0b5a0e3f1ccf11aab585e0832e926ddaa3970868829fa
---
# DHCP Reservations and IoT DNS

Every IoT device should have a DHCP reservation so IPs, firewall rules, and HA integrations stay stable. Point the IoT VLAN at Pi-hole or AdGuard and intercept hardcoded DNS (8.8.8.8) at the firewall so devices cannot bypass the sinkhole.

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

## Related Concepts

- [[network-vlan.md|network vlan]]
- [[network-mdns.md|network mdns]]
- [[network-wifi.md|network wifi]]
