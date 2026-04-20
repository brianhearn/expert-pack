# @expertpack/openclaw-memory-plugin

> **Status: 0.1.0-alpha** — drop-in folder, not yet published to npm / ClawHub.

An [OpenClaw](https://openclaw.ai) memory plugin that replaces the built-in
vector store with a single remote `/search` call to an
[ExpertPack MCP](https://github.com/brianhearn/ep-mcp) (EP MCP) server.

## Why

OpenClaw's bundled memory plugins (`memory-core`, `memory-lancedb`) maintain
a local index and perform a local vector search on every query. For agents
whose "memory" is really an ExpertPack knowledge pack served by EP MCP, this
means **two independent vector stores** (local LanceDB + EP MCP's SQLite-vec),
**two embedding pipelines**, and a full round-trip to Gemini on every query.

This plugin collapses the stack:

- **One Gemini embed call per search** (3072d by default)
- **One POST /search call** to EP MCP with the vector pre-computed
- **No local index, no local vector store**
- The server-side `requires:` expansion, cross-encoder reranker, graph
  widening, BM25 fallback, and query-embed cache all still apply

Typical warm query latency: ~1–2 seconds end-to-end (embed + network + server
pipeline), single-digit ms if the query embed cache hits on the server.

## Requirements

- OpenClaw `>= 2026.4.15-beta.1`
- An EP MCP server running **ep-mcp `>= 0.5`** (introduces POST /search with
  caller-supplied `vector`)
- A Gemini API key (`gemini-embedding-001` by default; must match the
  embedding provider configured on the EP MCP server)
- A configured pack slug on the EP MCP server, with API key auth enabled

## Install (drop-in)

```bash
cd /path/to/your/host/plugins
git clone <this repo>  # or copy the tools/openclaw-memory-plugin folder
cd openclaw-memory-plugin
npm install            # builds ./dist automatically via `prepare`
```

Then in `~/.openclaw/openclaw.json`:

```json5
{
  "plugins": {
    "load": {
      "paths": [
        "/absolute/path/to/openclaw-memory-plugin"
      ]
    },
    "slots": {
      "memory": "ep-memory-mcp"
    },
    "entries": {
      "ep-memory-mcp": {
        "enabled": true,
        "config": {
          "endpoint": "https://expertpack.ai/mcp",
          "apiKey": "<EP MCP bearer token>",
          "pack": "ezt-designer",
          "embedding": {
            "apiKey": "${GEMINI_API_KEY}",
            "model": "gemini-embedding-001",
            "taskType": "RETRIEVAL_QUERY"
          },
          "maxResults": 10,
          "minScore": 0.2,
          "includeLocalFiles": ["SOUL.md", "IDENTITY.md"],
          "timeoutMs": 15000
        }
      }
    }
  }
}
```

Restart the OpenClaw gateway. `memory_search` now queries EP MCP directly.

## Config reference

| Field | Required | Default | Notes |
|---|---|---|---|
| `endpoint` | yes | — | Base URL, no trailing slash |
| `apiKey` | no | — | Bearer token. `${ENV_VAR}` references are resolved |
| `pack` | yes | — | Pack slug (must match EP MCP `config.yaml`) |
| `embedding.apiKey` | yes | — | Gemini API key (or `${GEMINI_API_KEY}`) |
| `embedding.model` | no | `gemini-embedding-001` | Must match server index |
| `embedding.taskType` | no | `RETRIEVAL_QUERY` | Keep unless you know why |
| `embedding.outputDimensionality` | no | — | MRL dim; unset = full 3072d |
| `maxResults` | no | `10` | 1..50 |
| `minScore` | no | `0.2` | Applied client-side after server returns |
| `includeLocalFiles` | no | `[]` | Workspace-relative paths readable via `readFile` |
| `timeoutMs` | no | `15000` | Per-request HTTP timeout |

## Behavior

- **`search`**: embeds the query once with Gemini, then POSTs to
  `<endpoint>/search` with the vector. If the embed call fails, falls back to
  server-side embedding automatically. Filters by `minScore` client-side.
  Results flagged `requires_expanded` / `graph_expanded` on the server get a
  trailing HTML comment in the snippet so the agent can see the provenance.
- **`readFile`**: only permits reads for paths explicitly listed in
  `includeLocalFiles` (or matching by basename). This keeps the plugin from
  exposing arbitrary workspace files.
- **`status`**: reports backend `builtin`, provider `ep-mcp`, and a
  `custom` block with endpoint/pack/requestCount/embedCount for debugging.
- **`sync` / `probeVectorAvailability`**: indexing and vector storage live
  on the EP MCP server. `sync` is a no-op. `probeVectorAvailability` just
  checks that the embedder is reachable.
- **`close`**: stateless HTTP client; no-op.

## Limitations

- **Remote-only.** No local fallback if the EP MCP server is down. For local
  agent sessions that should survive network failures, combine with
  `memory-core` in a multi-provider setup (not yet supported by OpenClaw's
  single-slot memory system — tracked upstream).
- **No session transcripts.** The plugin does not index or search previous
  agent transcripts. Use `memory-core` or `memory-lancedb` for that.
- **Single pack per plugin instance.** If you need multiple packs, run
  multiple plugin instances or build a composite backend.
- **Gemini-only embedding provider (for now).** OpenAI and other providers
  can be added behind the same `GeminiEmbedder` interface; PRs welcome.

## Development

```bash
npm install     # installs devDeps, builds via `prepare`
npm run build   # rebuild
node test-smoke.mjs   # smoke test (requires GEMINI_API_KEY + EP MCP access)
```

## License

Apache-2.0, matching the parent ExpertPack repo.
