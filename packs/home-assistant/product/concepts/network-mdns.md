---
title: "mDNS and Multicast Across VLANs"
type: concept
tags:
  - network-architecture
  - mdns
  - avahi
  - discovery
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/network-mdns
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - network-vlan.md
  - network-dhcp-dns.md
  - esphome-what.md
content_hash: sha256:807095fcc63f24be7c45545e6aac3b391dcdf6c329681c7b80ca2a7bc4024dfc
---
# mDNS and Multicast Across VLANs

mDNS is how HA discovers Shelly, Chromecast, ESPHome, and Sonos. Multicast does not cross VLAN boundaries, so putting IoT on VLAN 10 and HA on VLAN 1 breaks Add Integration until you add an mDNS reflector, use static IPs, or go MQTT/Zigbee.

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

## Related Concepts

- [[network-vlan.md|network vlan]]
- [[network-dhcp-dns.md|network dhcp dns]]
- [[esphome-what.md|esphome what]]
