# Pack Tools & Capabilities

Integrator contract for the Solar DIY composite. Not loaded into agent context by default.

## Authority and grounding

Read this composite's `authority_boundary` and each constituent pack's boundary before answering.

- Product pack: residential solar/battery technology, documented NEC requirements, selection, troubleshooting.
- Process pack: site assessment through operations and maintenance.
- Decline investment advice, utility-scale design, and performing or signing off licensed electrical work.
- If product and process disagree, `conflicts.strategy` is `fail_closed` — refuse rather than guess.

## Retrieval

- **Recommended backend:** EP MCP `/search` or OpenClaw RAG over `product/` and `process/`.
- **Consume loop:** search → read the whole atom → expand `requires:` → stop (budget 3 / cap 7).
- **Tiers:** only each pack's `overview.md` is always-loaded. Glossaries are searchable.

## Agent workflows

See `process/phases/` for the install journey and `process/decisions/` for DIY-vs-contractor, topology, and grid-tie choices.
