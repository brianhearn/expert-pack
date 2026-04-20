/**
 * Plugin config schema + resolver.
 *
 * The plugin config is validated by OpenClaw against the JSON schema declared
 * in openclaw.plugin.json before {@link register} runs, so this module only
 * needs to provide TypeScript types and a small env-substitution helper.
 */

export type EmbeddingTaskType =
  | "RETRIEVAL_QUERY"
  | "RETRIEVAL_DOCUMENT"
  | "SEMANTIC_SIMILARITY"
  | "QUESTION_ANSWERING"
  | "FACT_VERIFICATION"
  | "CODE_RETRIEVAL_QUERY"
  | "CLASSIFICATION"
  | "CLUSTERING";

export type EmbeddingConfig = {
  /** Gemini API key. `${GEMINI_API_KEY}` is resolved from process.env. */
  apiKey: string;
  /** Gemini embedding model. Default: gemini-embedding-001 (3072d). */
  model?: string;
  /** Task type. Default: RETRIEVAL_QUERY (matches EP MCP index build). */
  taskType?: EmbeddingTaskType;
  /** Optional MRL dimension. Unset = full 3072d (matches EP MCP default). */
  outputDimensionality?: number;
};

export type PluginConfig = {
  /** Base URL of the EP MCP server, e.g. https://expertpack.ai/mcp */
  endpoint: string;
  /** Bearer token for the configured pack. */
  apiKey?: string;
  /** Pack slug (must match EP MCP config.yaml). */
  pack: string;
  /** Gemini embedding config. */
  embedding: EmbeddingConfig;
  /** Max results per query (1..50). Default: 10. */
  maxResults?: number;
  /** Minimum score for results (0..1). Default: 0.2. */
  minScore?: number;
  /** Workspace-relative local file paths always resolvable via readFile. */
  includeLocalFiles?: string[];
  /** HTTP timeout in ms. Default: 15000. */
  timeoutMs?: number;
};

export type ResolvedEmbeddingConfig = {
  apiKey: string;
  model: string;
  taskType: EmbeddingTaskType;
  outputDimensionality: number | undefined;
};

export type ResolvedPluginConfig = {
  endpoint: string;
  apiKey: string | undefined;
  pack: string;
  embedding: ResolvedEmbeddingConfig;
  maxResults: number;
  minScore: number;
  includeLocalFiles: string[];
  timeoutMs: number;
};

const ENV_REF = /^\$\{([A-Z0-9_]+)\}$/;

function resolveEnvRef(value: string | undefined): string | undefined {
  if (!value) return value;
  const m = ENV_REF.exec(value.trim());
  if (!m) return value;
  return process.env[m[1]!];
}

export function resolvePluginConfig(raw: PluginConfig): ResolvedPluginConfig {
  const endpoint = raw.endpoint.replace(/\/+$/, "");
  return {
    endpoint,
    apiKey: resolveEnvRef(raw.apiKey),
    pack: raw.pack,
    embedding: {
      apiKey: resolveEnvRef(raw.embedding.apiKey) ?? raw.embedding.apiKey,
      model: raw.embedding.model ?? "gemini-embedding-001",
      taskType: raw.embedding.taskType ?? "RETRIEVAL_QUERY",
      outputDimensionality: raw.embedding.outputDimensionality,
    },
    maxResults: raw.maxResults ?? 10,
    minScore: raw.minScore ?? 0.2,
    includeLocalFiles: raw.includeLocalFiles ?? [],
    timeoutMs: raw.timeoutMs ?? 15_000,
  };
}
