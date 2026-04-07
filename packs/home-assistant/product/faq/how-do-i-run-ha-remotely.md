---
title: How Do I Access Home Assistant Remotely?
type: faq
tags:
- backup-migration
- faq
- network-architecture
- remote-access
pack: home-assistant-product
retrieval_strategy: standard
---
<!-- context: section=faq, topic=remote-access, related=network-architecture,backup-migration -->

# How Do I Access Home Assistant Remotely?

> **Lead summary:** There are three safe ways to access HA remotely: Nabu Casa Cloud (easiest, $75/year, outbound-only tunnel — no port forwarding), Tailscale (free, zero-config VPN, no port forwarding), or a reverse proxy with SSL (self-hosted, requires a domain and some setup). **Never port-forward port 8123 directly to the internet** — it receives constant brute-force attacks. All three safe options protect HA behind authentication layers without exposing the raw HA port.

## Option 1: Nabu Casa Cloud (Recommended for Most Users)

Nabu Casa is the official remote access service from the Home Assistant team ($75/year).

**How it works:**
- HA establishes an outbound-only encrypted tunnel to Nabu Casa's servers
- You access HA via `https://[your-id].ui.nabu.casa`
- No port forwarding required — nothing is opened inbound on your router
- Even if Nabu Casa's servers were compromised, attackers cannot tunnel back to your HA

**Setup:** Settings → Home Assistant Cloud → Sign in or create account

**Also includes:** Cloud speech processing for Assist (voice commands), Google Assistant and Alexa bridge

**When to choose this:** You want remote access that "just works" and don't want to manage infrastructure. Also supports the HA development team.

## Option 2: Tailscale (Free, Zero-Config VPN)

Tailscale is a WireGuard-based VPN that requires no port forwarding and is free for personal use.

**How it works:**
- Install Tailscale on your HA host (Settings → Add-ons → Tailscale) and on your phone/laptop
- Tailscale creates an encrypted peer-to-peer connection between your devices
- HA appears at `http://homeassistant` or its Tailscale IP on any connected device
- Falls back to Tailscale relay servers if direct connection isn't possible

**Setup:**
1. Install Tailscale add-on in HA OS
2. Create a free Tailscale account at tailscale.com
3. Install Tailscale on your phone and laptop
4. All devices can now reach HA on the Tailscale network

**When to choose this:** You want a free, secure option with no subscription. Works excellently for technical users comfortable with VPN concepts.

## Option 3: Reverse Proxy with SSL (Self-Hosted)

Use Nginx, Caddy, or the Nginx Proxy Manager add-on to expose HA via HTTPS on your own domain.

**Requirements:**
- A domain name ($10-15/year from Namecheap, Cloudflare, etc.)
- Router that supports port 443 forwarding
- DDNS service if your IP changes (DuckDNS is free)
- Nginx Proxy Manager or Caddy add-on

**Security additions required:**
- Enable HA 2FA (Settings → Profile → Multi-factor Authentication)
- Use Cloudflare as DNS proxy (hides your home IP, adds DDoS protection)
- Consider IP allowlisting if you only access from known locations

**When to choose this:** You want full control, are comfortable with web server concepts, and want to self-host your access infrastructure.

## Option 4: NEVER — Port-Forward Port 8123 Directly

Directly forwarding port 8123 (or any port) on your router to HA means anyone on the internet can attempt to log in. 

**Why this is dangerous:**
- Automated bots scan all internet IPs for port 8123 within hours of it being opened
- Brute force attacks occur constantly
- If a HA vulnerability is disclosed, you're exposed until you patch
- No defense in depth — if your password is weak or a HA bug exists, you're compromised

This is the single most common dangerous mistake in HA setups. If a forum post tells you to "just open port 8123," don't.

## Quick Decision Guide

| Your Situation | Recommended Option |
|---------------|-------------------|
| Non-technical, want simple | Nabu Casa |
| Want free, ok with VPN concept | Tailscale |
| Already use Cloudflare, have domain | Reverse proxy |
| Want to support HA development | Nabu Casa |
| Just want to try something | Tailscale (easy rollback) |

→ See [[network-architecture.md]] for full security discussion
