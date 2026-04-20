/**
 * Minimal vendored types from the OpenClaw plugin SDK.
 *
 * We vendor a narrow subset of the `openclaw/plugin-sdk/core` surface area
 * rather than depending on `openclaw` at build time, because the OpenClaw
 * npm package pulls thousands of transitive dependencies (channel plugins,
 * provider SDKs, etc.) that this plugin does not need and that routinely
 * fail to resolve under `npm install` on clean hosts.
 *
 * These types are structural: they match the shape that OpenClaw will pass
 * us at load time. If the upstream SDK drifts, the `definePluginEntry`
 * import below simply points at a different default export — the host
 * loader only cares that the exported object has `id`, `name`, `kind`, and
 * `register`.
 *
 * Source: /usr/lib/node_modules/openclaw/dist/plugin-sdk/src/plugins/types.d.ts
 *         /usr/lib/node_modules/openclaw/dist/plugin-sdk/src/plugin-sdk/plugin-entry.d.ts
 *         /usr/lib/node_modules/openclaw/dist/plugin-sdk/src/plugins/memory-state.d.ts
 *         /usr/lib/node_modules/openclaw/dist/plugin-sdk/src/memory-host-sdk/host/types.d.ts
 */

/* eslint-disable @typescript-eslint/no-explicit-any */

export interface PluginLogger {
  info?(message: string): void;
  warn?(message: string): void;
  debug?(message: string): void;
  error?(message: string): void;
}

export interface OpenClawPluginService {
  id: string;
  start?: () => void | Promise<void>;
  stop?: () => void | Promise<void>;
}

export interface MemoryPluginRuntime {
  getMemorySearchManager(params: {
    cfg: unknown;
    agentId: string;
    purpose?: "default" | "status";
  }): Promise<{ manager: unknown; error?: string }>;
  resolveMemoryBackendConfig(params: {
    cfg: unknown;
    agentId: string;
  }): { backend: "builtin" | "qmd"; [k: string]: unknown };
  closeAllMemorySearchManagers?(): Promise<void>;
}

export interface MemoryPluginCapability {
  runtime?: MemoryPluginRuntime;
  promptBuilder?: unknown;
  flushPlanResolver?: unknown;
  publicArtifacts?: unknown;
}

export interface OpenClawPluginApi {
  logger: PluginLogger;
  pluginConfig?: Record<string, unknown>;
  resolvePath: (input: string) => string;
  registerTool: (...args: unknown[]) => void;
  registerService: (service: OpenClawPluginService) => void;
  registerMemoryCapability: (capability: MemoryPluginCapability) => void;
  // Other members exist on the real api (channels, providers, commands, etc.)
  // but are not needed here. Index access is permitted for forward-compat.
  [k: string]: any;
}

export interface DefinePluginEntryOptions {
  id: string;
  name: string;
  description: string;
  kind?: "memory" | "channel" | "provider" | "tool" | "service" | "context-engine" | string;
  configSchema?: unknown;
  register: (api: OpenClawPluginApi) => void;
}

export interface DefinedPluginEntry extends DefinePluginEntryOptions {
  configSchema: unknown;
}

/**
 * Pure identity/normalizer matching the runtime behavior of
 * `openclaw/plugin-sdk/core#definePluginEntry`. The host loader inspects
 * the exported shape directly; the real SDK's `definePluginEntry` is
 * itself a normalizer (see dist/plugin-entry-*.js), so a local copy is
 * sufficient and avoids a heavy runtime dependency on `openclaw`.
 */
export function definePluginEntry(
  opts: DefinePluginEntryOptions,
): DefinedPluginEntry {
  return {
    configSchema: opts.configSchema,
    ...opts,
  };
}
