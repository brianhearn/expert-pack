// Smoke test: load the built plugin, verify shape, run a real /search.
// Run with: node test-smoke.mjs

import plugin from "./dist/index.js";
import { EpMemorySearchManager } from "./dist/search-manager.js";
import { resolvePluginConfig } from "./dist/config.js";

// 1. Verify exported plugin entry shape.
console.log("=== Plugin entry shape ===");
console.log("id:", plugin.id);
console.log("name:", plugin.name);
console.log("kind:", plugin.kind);
console.log("has register:", typeof plugin.register === "function");
console.log();

// 2. Build a manager directly and run a real query.
console.log("=== Running real /search against expertpack.ai/mcp ===");

// Config pulled entirely from env. Set before running:
//   GEMINI_API_KEY=...        (required)
//   EP_MCP_API_KEY=...        (required, bearer token for the pack)
//   EP_MCP_ENDPOINT=...       (optional, default https://expertpack.ai/mcp)
//   EP_MCP_PACK=...           (optional, default ezt-designer)
if (!process.env.GEMINI_API_KEY) {
  console.error("GEMINI_API_KEY not set");
  process.exit(1);
}
if (!process.env.EP_MCP_API_KEY) {
  console.error("EP_MCP_API_KEY not set");
  process.exit(1);
}

const config = resolvePluginConfig({
  endpoint: process.env.EP_MCP_ENDPOINT ?? "https://expertpack.ai/mcp",
  apiKey: process.env.EP_MCP_API_KEY,
  pack: process.env.EP_MCP_PACK ?? "ezt-designer",
  embedding: {
    apiKey: "${GEMINI_API_KEY}",
    model: "gemini-embedding-001",
    taskType: "RETRIEVAL_QUERY",
  },
  maxResults: 5,
  minScore: 0.2,
  includeLocalFiles: ["SOUL.md", "IDENTITY.md"],
});

const manager = new EpMemorySearchManager({
  config,
  workspaceDir: "/root/.openclaw/workspace",
  logger: {
    info: (m) => console.log("  [info]", m),
    warn: (m) => console.log("  [warn]", m),
    error: (m) => console.log("  [error]", m),
    debug: (m) => console.log("  [debug]", m),
  },
});

const start = Date.now();
const results = await manager.search("what is a territory");
const elapsed = Date.now() - start;

console.log(`\nGot ${results.length} results in ${elapsed}ms:`);
for (const r of results) {
  console.log(`  ${r.score.toFixed(4)}  ${r.path}  (${r.endLine - r.startLine + 1} lines)`);
}

console.log("\n=== Status ===");
console.log(JSON.stringify(manager.status(), null, 2));

console.log("\n=== readFile (allowed: SOUL.md) ===");
const soul = await manager.readFile({ relPath: "SOUL.md", lines: 5 });
console.log(`  lines=${soul.lines} truncated=${soul.truncated}`);
console.log(`  first line: "${soul.text.split("\n")[0]}"`);

console.log("\n=== readFile (denied: MEMORY.md) ===");
const denied = await manager.readFile({ relPath: "MEMORY.md" });
console.log(`  lines=${denied.lines}  (should be 0 — not in allowlist)`);

console.log("\n=== probeEmbeddingAvailability ===");
const probe = await manager.probeEmbeddingAvailability();
console.log("  ok:", probe.ok, probe.error ? `(${probe.error})` : "");

console.log("\n✅ Smoke test complete");
