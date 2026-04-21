---
title: "Home Assistant — Glossary"
type: "glossary"
tags: []
pack: "home-assistant-product"
retrieval_strategy: "standard"
id: home-assistant/product/glossary
verified_at: "2026-04-21"
verified_by: agent
schema_version: "4.1"
concept_scope: single
---
# Home Assistant — Glossary

Quick-reference definitions mapping HA terminology to plain language.

## Core Concepts

| Term | Definition | Common User Language |
|------|-----------|---------------------|
| **Entity** | The atomic unit of HA — a single sensor, switch, light, or other controllable/measurable thing. Has a state and attributes. | "a thing in HA", "sensor", "device" (incorrectly) |
| **Device** | Logical grouping of related entities. One physical device = one HA device with multiple entities. | "my sensor", "my light" |
| **Integration** | Software bridge connecting HA to hardware, services, or platforms. | "plugin", "connector", "how HA talks to my stuff" |
| **State** | Current value of an entity (on/off, 72.5, home, detected). Always stored as a string internally. | "is it on?", "what's the temperature?" |
| **Attribute** | Additional data beyond the state — brightness, color, battery %, friendly name. | "other info about the thing" |
| **Service / Action** | A command you can call on entities (turn_on, set_temperature, send notification). Recently renamed from "service" to "action" in the UI. | "do something", "tell it to turn on" |
| **Area** | Organizational grouping by physical location (room, floor, zone). | "room", "where the device is" |
| **Domain** | Entity type prefix (light, switch, sensor, binary_sensor, climate, etc.). | "what kind of thing it is" |

## Automation

| Term | Definition | Common User Language |
|------|-----------|---------------------|
| **Trigger** | The event that starts an automation. | "when this happens" |
| **Condition** | Optional gate checked after trigger — must be true for actions to run. | "only if" |
| **Action** | What the automation does when triggered and conditions pass. | "then do this" |
| **Automation mode** | Controls behavior when an automation triggers while already running: single, restart, queued, parallel. | "what happens if it fires twice" |
| **Blueprint** | Pre-made automation template by the community — configure inputs, no YAML needed. | "ready-made automation", "template" |
| **Script** | Reusable sequence of actions — like an automation without triggers. Called by automations or manually. | "macro", "reusable action list" |
| **Scene** | Snapshot of entity states — apply to set multiple entities at once. | "preset", "mood", "setting" |

## Protocols & Networking

| Term | Definition | Common User Language |
|------|-----------|---------------------|
| **Zigbee** | Open-standard, low-power 2.4 GHz mesh protocol. Most recommended for HA. | "the mesh network", "what Aqara/IKEA uses" |
| **Z-Wave** | Proprietary low-power mesh protocol on 868/912 MHz. Less interference than Zigbee. | "the other mesh protocol" |
| **Thread** | IP-based mesh protocol. Low-power, used as transport for Matter. | "the new mesh thing" |
| **Matter** | Unification standard for smart home interoperability across ecosystems. | "the universal standard", "what's supposed to make everything work together" |
| **ESPHome** | Platform for programming ESP32/ESP8266 microcontrollers via YAML. Direct HA integration. | "DIY sensors", "custom sensors" |
| **Coordinator** | The USB dongle or bridge that manages a Zigbee or Z-Wave network. | "the Zigbee stick", "USB dongle" |
| **Router device** | Mains-powered mesh device that relays messages and extends network coverage. | "repeater", "range extender" |
| **End device** | Battery-powered mesh device that connects to routers but doesn't relay. | "sensor", "battery device" |
| **MQTT** | Message Queuing Telemetry Transport — lightweight messaging protocol. Used by Zigbee2MQTT, many IoT devices. | "the message system" |
| **ZHA** | Zigbee Home Automation — HA's built-in Zigbee integration. | "built-in Zigbee" |
| **Zigbee2MQTT** | Alternative Zigbee integration running through an MQTT broker. More devices supported. | "the other Zigbee option" |

## Configuration

| Term | Definition | Common User Language |
|------|-----------|---------------------|
| **configuration.yaml** | Main config file for HA. Some integrations require entries here. | "the config file", "the YAML file" |
| **Jinja2** | Template engine used in HA for dynamic values. Python-based syntax. | "templates", "the curly brace stuff" |
| **HACS** | Home Assistant Community Store — custom integration/card/theme marketplace. | "the community store", "custom stuff" |
| **Add-on** | Supplementary application running alongside HA (requires Supervisor). Examples: Mosquitto, Node-RED, File Editor. | "plugin", "extra app" |
| **Supervisor** | Component that manages add-ons, backups, and updates. Available in HA OS and HA Supervised. | "the manager", "what runs add-ons" |
| **Lovelace** | Legacy name for HA's dashboard system. Now just called "Dashboards." | "the dashboard", "the UI" |
| **Helper** | UI-created entities for storing values: input_boolean, input_number, input_select, input_text, timer, counter. | "virtual switch", "variable", "toggle" |
| **Package** | YAML organization method — group related config (automations, sensors, scripts) into a single file by topic instead of by type. | "organized config", "config per room" |
