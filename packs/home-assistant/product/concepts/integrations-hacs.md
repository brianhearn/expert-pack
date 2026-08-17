---
title: "HACS Community Store"
type: concept
tags:
  - integrations-guide
  - hacs
  - custom-integrations
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/integrations-hacs
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - integrations-iot-class.md
  - dashboard-mushroom.md
  - integrations-reliability.md
content_hash: sha256:ada03494aa413bbc496ddb61c010f7fe598bfbd1fa23442088d3105a8f22fec7
---
# HACS Community Store

HACS is the unofficial extension ecosystem for custom integrations, frontend cards, and themes. Components run with the same privileges as HA, so prefer well-starred maintained repos, never install from outside HACS, and treat custom integrations as the first thing that breaks on a monthly HA update.

## HACS — The Community App Store

HACS (Home Assistant Community Store) is the unofficial extension ecosystem for HA. It provides:
- **Custom integrations** — additional integrations not in official HA (Frigate, car integrations, obscure devices, etc.)
- **Custom frontend cards** — Mushroom, button-card, mini-graph-card, etc.
- **Themes**
- **Python scripts**

### Installing HACS
HACS requires a GitHub account. Install via:
1. Download HACS from `github.com/hacs/integration`
2. Place in `custom_components/hacs/`
3. Add integration in HA: Settings → Integrations → HACS
4. Authenticate with GitHub account

Or use the HACS one-line install script (official, runs in HA terminal).

### Safety Considerations for HACS

HACS components run with the same privileges as HA itself — full access to your HA configuration, your devices, and potentially your network. This is a real security consideration.

**Safe HACS practices:**
- Prefer integrations with large star counts (500+) and active maintenance
- Check when the last commit was — dormant repos for 1+ year are break risk
- Read the code for high-privilege integrations (or trust community security reviews)
- Never install HACS integrations from untrusted sources (not via HACS itself)
- Keep HACS integrations updated — stale custom integrations are a common source of HA update breakage

**Categories of HACS risk:**
- Frontend cards: low risk (UI only, no network/system access)
- Custom integrations: higher risk (can access network, secrets, etc.)
- Unknown authors: higher risk than popular/well-known repos

**The HACS security model:** GitHub Actions runs malware scanning on some repos, but it's community-moderated, not guaranteed. For critical security needs, stick to official integrations.

### When to Use HACS vs Official

| Situation | Recommendation |
|-----------|---------------|
| Integration exists officially | Use official — better tested, stable API |
| Device not officially supported | Check HACS, evaluate activity level |
| Dashboard card functionality missing | HACS frontend cards are low-risk |
| Custom integration from unknown author | Audit code, check community discussion first |
| Feature added to official in recent release | Migrate from HACS to official when stable |

## Related Concepts

- [[integrations-iot-class.md|integrations iot class]]
- [[dashboard-mushroom.md|dashboard mushroom]]
- [[integrations-reliability.md|integrations reliability]]

Sources: [HACS docs](https://hacs.xyz/docs/).
