---
title: "Remote Access Ranked by Security"
type: concept
tags:
  - network-architecture
  - nabu-casa
  - wireguard
  - tailscale
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/network-remote-access
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - network-cameras-hardware.md
  - network-vlan.md
  - backup-hardware-migration.md
content_hash: sha256:451f44c6c9eebcea4c7044a0477d1ddf712ec5073062ae4a59e3c60f5b59d02e
---
# Remote Access Ranked by Security

Never expose port 8123 to the internet. Ranked safest to most dangerous: Nabu Casa outbound tunnel, WireGuard/Tailscale VPN, then a reverse proxy with SSL and 2FA. Port-forwarding 8123 is the most common dangerous HA mistake.

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

## Related Concepts

- [[network-cameras-hardware.md|network cameras hardware]]
- [[network-vlan.md|network vlan]]
- [[backup-hardware-migration.md|backup hardware migration]]
