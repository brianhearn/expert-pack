# Pack Tools & Capabilities

Integrator contract for the Home Assistant composite. Not loaded into agent context by default.

## Authority and grounding

Read this composite's `authority_boundary` and each constituent pack's boundary before answering.

- Product pack: platform architecture, protocols, automations, dashboards, troubleshooting.
- Process pack: phased install, decisions, patterns, hardening.
- Decline other smart-home platforms, licensed electrical/construction work, and legal/medical/financial advice.
- If product and process disagree, `conflicts.strategy` is `fail_closed` — refuse rather than guess.

## Retrieval

- **Recommended backend:** EP MCP `/search` or OpenClaw RAG over `product/` and `process/`.
- **Consume loop:** search → read the whole atom → expand `requires:` → stop (budget 3 / cap 7).
- **Tiers:** only each pack's `overview.md` is always-loaded. Glossaries are searchable.

## Agent workflows

See `process/phases/` for the install journey and `process/patterns/` for battle-tested automations.
