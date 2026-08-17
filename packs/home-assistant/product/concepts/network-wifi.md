---
title: "IoT WiFi — 2.4 GHz and SSIDs"
type: concept
tags:
  - network-architecture
  - wifi
  - 2.4ghz
  - wpa2
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/network-wifi
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - network-vlan.md
  - network-zigbee-zwave.md
  - network-dhcp-dns.md
content_hash: sha256:c0efb76e5118f0ab535ca5227a0a98fa624eb322fedce82788c095dd1ae16b1a
---
# IoT WiFi — 2.4 GHz and SSIDs

Almost all IoT WiFi is 2.4 GHz only. Use a dedicated IoT SSID (or VLAN-tagged SSID), disable aggressive roaming features that confuse cheap devices, and prefer WPA2 or mixed WPA2/WPA3 — some gadgets choke on WPA3-only.

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

## Related Concepts

- [[network-vlan.md|network vlan]]
- [[network-zigbee-zwave.md|network zigbee zwave]]
- [[network-dhcp-dns.md|network dhcp dns]]
