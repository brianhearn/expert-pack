# Gotchas Index

Common mistakes and traps in Home Assistant setups. Reading this before you start saves hours of debugging.

| File | Contents |
|------|----------|
| [common-mistakes.md](common-mistakes.md) | The 12 most costly mistakes in HA setups — SD cards, protocol choices, automation modes, backups, security, and entity naming |

**Top 5 by cost (time or money):**

1. **SD card storage** — corrupts and fails; use SSD from day one
2. **No automated backups** — set up Google Drive Backup in Phase 2, not Phase 7
3. **Wi-Fi for all devices** — use Zigbee; 50 Wi-Fi IoT devices degrades everything
4. **Wrong automation mode** — motion lights need `mode: restart`
5. **Exposing port 8123 to the internet** — use Nabu Casa or Cloudflare Tunnel instead

→ For diagnostic help when things go wrong, see the [product troubleshooting guide](../../product/troubleshooting/_index.md).
