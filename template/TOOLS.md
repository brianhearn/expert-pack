# Pack Tools & Capabilities

What an agent can *do* with this pack, beyond reading it. If the pack is meant to
be consumed through an MCP server, custom retrieval, or a specific agent workflow,
document that contract here. This file is for integrators; it is not loaded into
agent context by default.

## Retrieval

How this pack is meant to be searched.

- **Recommended backend:** e.g. EP MCP (`/search`), OpenClaw RAG, or a plain vector store.
- **Chunking:** files are authored at 400–800 tokens; point any chunker at ~1,000 tokens so files pass through intact. Oversized `atomic`/`reference` files carry `.chunks.yaml` sidecars (RFC-004).
- **Reconstruct Mode:** whether consumers should request span-level provenance (RFC-003) and emit Typed Answer Contracts (`templates/TAC-PROMPT.md`).

## MCP tools exposed

If this pack ships with or expects specific MCP tools, list them. For each: the
tool name, what it does, its inputs, and what it returns.

| Tool | Purpose | Inputs | Returns |
|------|---------|--------|---------|
| `memory_search` | Retrieve pack fragments for a query | `query`, `n` | Ranked fragments (+ provenance in reconstruct mode) |
| `memory_get` | Fetch a specific fragment/file by id | `id` | File body + frontmatter |

## Agent workflows

The multi-step tasks this pack is designed to support. Point at the relevant
`workflows/` files rather than restating them here.

- **Workflow name** → see `workflows/<file>.md`. One line on when to invoke it.

## Integration checklist

- [ ] Pack passes `expertpack validate --strict`.
- [ ] `content_hash` backfilled (`expertpack checksum --apply`).
- [ ] Sidecars generated for oversized atomic/reference files (`expertpack chunk-annotate --apply`).
- [ ] Retrieval backend pointed at the pack directory.
- [ ] Consumers configured for Reconstruct Mode / TAC if auditable answers are required.
