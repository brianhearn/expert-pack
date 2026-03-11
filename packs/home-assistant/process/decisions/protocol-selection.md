# Decision: Smart Home Protocol Selection

## The Decision

Which wireless protocol should you use for smart home devices — Zigbee, Z-Wave, Wi-Fi, or Thread/Matter?

This decision determines which devices you can buy, which coordinator hardware you need, and how your system will behave over time. Getting this wrong is expensive (you're buying new hardware) and time-consuming (re-pairing dozens of devices).

---

## Protocol Overview

### Zigbee

**What it is:** IEEE 802.15.4-based mesh network operating at 2.4GHz. The most widely used protocol in HA deployments.

**Mesh behavior:** Mains-powered Zigbee devices (plugs, bulbs) act as repeaters, extending range for battery-powered devices. A 30-device network with 10+ mains devices covers a typical 2,500 sq ft home easily.

**Strengths:**
- Huge device ecosystem — thousands of compatible devices from hundreds of manufacturers
- Cheap devices ($7-15 for sensors, $15-25 for plugs)
- Excellent HA support via Zigbee2MQTT or ZHA
- Fully local — no cloud, no account, no subscription
- Low power consumption for battery devices (years of battery life)

**Weaknesses:**
- 2.4GHz band shared with Wi-Fi — can cause interference (use a USB extension cable, choose Zigbee channel 25/26 to avoid WiFi overlap)
- Not all Zigbee devices work with all coordinators — check compatibility before buying
- No native IP routing — requires the coordinator as the hub

**Best coordinator:** SMLIGHT SLZB-07 (USB), Sonoff Zigbee 3.0 Dongle Plus-P (USB or Ethernet)  
**Best integration:** Zigbee2MQTT (more device support) or ZHA (built-in, easier)

**Verdict: Best starting protocol for most users.**

---

### Z-Wave

**What it is:** Proprietary 900MHz mesh network. Requires a licensed Z-Wave chipset.

**Frequency advantage:** Z-Wave operates on sub-GHz frequencies (868MHz in EU, 908MHz in US). No 2.4GHz interference. Better wall/floor penetration than Zigbee.

**Strengths:**
- No interference with 2.4GHz Wi-Fi
- Better range per hop than Zigbee
- Stricter certification — Z-Wave devices are generally more reliable and better-tested
- Good for thick-walled homes (concrete, stone, brick)

**Weaknesses:**
- **Expensive** — Z-Wave devices typically cost 2-3x Zigbee equivalents ($30-70 for sensors)
- Smaller device ecosystem than Zigbee
- Requires a Z-Wave controller (Aeotec Z-Stick Gen7, Nortek HUSBZB-1)
- Z-Wave Long Range (ZWLR) adds even more range but requires newer devices

**Best for:** Homes with thick walls, users who prioritize device reliability over price, security-focused deployments.

**Verdict: Premium alternative to Zigbee. Worth it for specific scenarios, not for budget-conscious builds.**

---

### Wi-Fi (ESPHome / Tasmota / Tuya)

**What it is:** Devices connect directly to your 2.4GHz or 5GHz Wi-Fi network.

**Subtypes:**
- **ESPHome devices** — ESP32/ESP8266-based, flashed with open firmware you control. Highly customizable.
- **Tasmota** — Open firmware for commodity Tuya/Sonoff hardware. Removes cloud dependency.
- **Cloud Wi-Fi** (Tuya, TP-Link Kasa, Meross) — Work through manufacturer's cloud but often have local polling APIs in HA.

**Strengths:**
- ESPHome integration in HA is excellent — OTA updates, config managed in HA
- DIY sensors cheaply ($5-15 per ESP32 board)
- 5GHz available for higher-bandwidth devices (cameras, video doorbells)
- No separate coordinator hardware

**Weaknesses:**
- **Doesn't scale well** — 50+ Wi-Fi IoT devices degrades router performance and adds AP load
- Most cheap Wi-Fi devices depend on manufacturer's cloud (privacy/reliability risk)
- Higher power consumption — Wi-Fi kills battery-powered devices within days
- Each device consumes an IP address (DHCP table limits apply)

**Best for:**
- Custom ESPHome sensors (temperature, CO2, mmWave presence, DIY projects)
- Devices that don't exist in Zigbee/Z-Wave (smart appliances, specific sensors)
- Situations where you're already invested in a Wi-Fi ecosystem (Kasa, Meross)

**Verdict: Excellent for custom/DIY sensors (ESPHome). Poor choice for volume deployments of off-the-shelf devices.**

---

### Thread / Matter

**What it is:** Thread is an IPv6 mesh protocol (based on 802.15.4 at 2.4GHz). Matter is an application-layer standard running over Thread (or Wi-Fi). Designed to unify smart home ecosystems.

**Current state (2026):** Matter has broad manufacturer adoption but is still maturing. HA support is solid via the Thread and Matter integrations.

**Strengths:**
- IP-based — no proprietary coordinator; any Thread Border Router works (Apple TV, Google Nest Hub, HA with USB dongle)
- Cross-ecosystem — a Matter device works with HA, HomeKit, Google Home, and Alexa simultaneously
- Designed for interoperability, not lock-in
- Local control — Matter devices don't require cloud after initial setup

**Weaknesses:**
- Device ecosystem still smaller than Zigbee
- More complex network setup (Thread Border Routers, commissioning process)
- Mixed quality — some Matter devices are excellent, some have firmware bugs
- Matter over Wi-Fi (not Thread) doesn't solve the Wi-Fi scale problem
- Not all Matter devices support all features in all ecosystems (feature parity is inconsistent)

**Best for:**
- New builds where you want ecosystem flexibility
- Users who also use Apple HomeKit or Google Home alongside HA
- Smart TVs, appliances, and devices that use Matter over Wi-Fi

**Verdict: Promising long-term direction, but Zigbee is more mature and battle-tested today. Consider Thread/Matter for new devices, keep Zigbee for the bulk of your sensors.**

---

## Decision Matrix

| Criterion | Zigbee | Z-Wave | Wi-Fi (ESPHome) | Thread/Matter |
|-----------|--------|--------|-----------------|---------------|
| **Device cost** | ✅ Low | ❌ High | ✅ Low (DIY) | ⚠️ Medium |
| **Device variety** | ✅ Huge | ⚠️ Medium | ✅ DIY unlimited | ⚠️ Growing |
| **Local control** | ✅ Yes | ✅ Yes | ✅ ESPHome yes; others vary | ✅ Yes (post-setup) |
| **Interference** | ⚠️ 2.4GHz | ✅ 900MHz | ⚠️ 2.4GHz | ⚠️ 2.4GHz |
| **Battery life** | ✅ Years | ✅ Years | ❌ Hours-days | ✅ Years (Thread) |
| **HA support** | ✅ Excellent | ✅ Excellent | ✅ Excellent (ESP) | ⚠️ Good, improving |
| **Coordinator needed** | ✅ ~$25 USB dongle | ✅ ~$50 USB stick | ❌ None | ✅ Thread Border Router |
| **Ecosystem maturity** | ✅ Very mature | ✅ Mature | ✅ ESPHome: mature | ⚠️ Maturing |

---

## Recommended Approach

**For most people building a new smart home:**

1. **Lead with Zigbee** for sensors, switches, plugs, and bulbs — widest device selection, lowest cost, excellent HA support.
2. **Add ESPHome** for custom sensors (DIY mmWave presence, temperature arrays, CO2 monitors) that don't exist as Zigbee devices.
3. **Consider Z-Wave** for door locks and garage openers — these are safety-critical devices where Z-Wave's higher reliability and better wall penetration justifies the cost.
4. **Adopt Thread/Matter** opportunistically — if a device you want comes in Matter, use it; don't throw out working Zigbee devices to migrate.

**Coordinator hardware to buy:**

- Zigbee: SMLIGHT SLZB-07 ($25) or Sonoff Dongle Plus-P ($20)
- Z-Wave: Aeotec Z-Stick Gen7 ($55)
- Both: Nortek HUSBZB-1 ($65) supports both protocols on one stick

→ See [Phase 3: Protocol Setup](../phases/03-protocol-setup.md) for installation and pairing instructions.
