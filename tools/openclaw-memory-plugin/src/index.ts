/**
 * OpenClaw memory plugin — ExpertPack MCP backend.
 *
 * Replaces the local LanceDB / builtin file vector store with a single
 * POST /search call to an EP MCP server. The agent gets the same
 * MemorySearchManager surface, but the index, embeddings, and reranker
 * all live on the remote EP MCP deployment.
 *
 * Selection:
 *   plugins.slots.memory = "ep-memory-mcp"
 *   plugins.entries.ep-memory-mcp = { enabled: true, config: {...} }
 *
 * See ./openclaw.plugin.json for the config schema.
 */

import { definePluginEntry } from "./openclaw-types.js";
import type { OpenClawPluginApi } from "./openclaw-types.js";

import {
  resolvePluginConfig,
  type PluginConfig,
  type ResolvedPluginConfig,
} from "./config.js";
import {
  EpMemorySearchManager,
  type HostMemorySearchManager,
} from "./search-manager.js";

const PLUGIN_ID = "ep-memory-mcp";

/**
 * Build the single MemorySearchManager instance for this plugin.
 * Cached per `api` reference so repeated getMemorySearchManager calls
 * don't keep rebuilding the client.
 */
type ManagerCacheEntry = {
  manager: HostMemorySearchManager;
  config: ResolvedPluginConfig;
};

export default definePluginEntry({
  id: PLUGIN_ID,
  name: "Memory (EP MCP)",
  description:
    "OpenClaw memory plugin that proxies search to an ExpertPack MCP " +
    "server. One Gemini embed, one remote /search; no local vector store.",
  kind: "memory",
  register(api: OpenClawPluginApi): void {
    let cached: ManagerCacheEntry | null = null;

    function getManager(): HostMemorySearchManager {
      if (cached) return cached.manager;
      const raw = api.pluginConfig as unknown as PluginConfig;
      const resolved = resolvePluginConfig(raw);
      const workspaceDir = resolveWorkspaceDir(api);
      const manager = new EpMemorySearchManager({
        config: resolved,
        workspaceDir,
        logger: {
          info: (m) => api.logger.info?.(m),
          warn: (m) => api.logger.warn?.(m),
          debug: (m) => api.logger.debug?.(m),
          error: (m) => api.logger.error?.(m),
        },
      });
      cached = { manager, config: resolved };
      api.logger.info?.(
        `ep-memory-mcp: registered (endpoint=${resolved.endpoint}, ` +
          `pack=${resolved.pack}, model=${resolved.embedding.model})`,
      );
      return manager;
    }

    api.registerMemoryCapability({
      runtime: {
        async getMemorySearchManager() {
          try {
            return { manager: getManager() };
          } catch (err) {
            return {
              manager: null,
              error: `ep-memory-mcp init failed: ${(err as Error).message}`,
            };
          }
        },
        resolveMemoryBackendConfig() {
          // EP MCP is an external HTTP service, not qmd; the host should
          // treat us as a builtin backend for flow purposes.
          return { backend: "builtin" };
        },
        async closeAllMemorySearchManagers() {
          if (cached?.manager?.close) {
            await cached.manager.close();
          }
          cached = null;
        },
      },
    });

    api.registerService({
      id: PLUGIN_ID,
      start: () => {
        api.logger.info?.(
          `${PLUGIN_ID}: service started (lazy init on first memory call)`,
        );
      },
      stop: async () => {
        if (cached?.manager?.close) {
          await cached.manager.close();
        }
        cached = null;
      },
    });
  },
});

function resolveWorkspaceDir(api: OpenClawPluginApi): string {
  // The host API exposes resolvePath for workspace-relative resolution.
  // We treat "." as the workspace root.
  try {
    return api.resolvePath(".");
  } catch {
    return process.cwd();
  }
}
