---
title: "IP Cameras and IoT Network Hardware"
type: concept
tags:
  - network-architecture
  - frigate
  - unifi
  - cameras
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/network-cameras-hardware
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - network-remote-access.md
  - network-vlan.md
  - integrations-top-used.md
content_hash: sha256:5946d011cf8c710257dd4417d87991d4bb2475557b12c6a992897d6470d4d7d9
---
# IP Cameras and IoT Network Hardware

Cameras belong on their own VLAN with no internet and a local NVR (Frigate). Do not push video through HA's Python event loop. The router is the most important network component — UniFi, GL.iNet Flint 2, or pfSense/OPNsense, not the ISP gateway.

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

## Related Concepts

- [[network-remote-access.md|network remote access]]
- [[network-vlan.md|network vlan]]
- [[integrations-top-used.md|integrations top used]]
