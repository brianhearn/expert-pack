---
title: "IoT VLANs and Why Network Design Matters"
type: concept
tags:
  - network-architecture
  - vlan
  - iot-security
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/network-vlan
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - network-mdns.md
  - network-dhcp-dns.md
  - network-wifi.md
content_hash: sha256:6fd1c7381bcb861a0409bbfb15da348f2927e0fbfa830f07c88edf7b335a6f82
---
# IoT VLANs and Why Network Design Matters

IoT devices are security liabilities — outdated firmware, default credentials, and phone-home telemetry. Put them on a separate VLAN with no (or filtered) internet, keep HA on the trusted network, and allow only HA to initiate into the IoT VLAN.

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

## Related Concepts

- [[network-mdns.md|network mdns]]
- [[network-dhcp-dns.md|network dhcp dns]]
- [[network-wifi.md|network wifi]]

Sources: [HA network](https://www.home-assistant.io/installation/network/).
