/**
 * MemorySearchManager implementation backed by EP MCP.
 *
 * This class satisfies OpenClaw's `MemorySearchManager` host interface without
 * any local vector store. Each {@link search} call performs one Gemini embed
 * (3072d by default) and one POST to the EP MCP server with the vector
 * pre-computed. Detail atoms pulled via `requires:` expansion on the server
 * are surfaced to the agent as additional results with the `requires_expanded`
 * flag preserved in the snippet label.
 *
 * The manager is intentionally lightweight: no sync, no index, no embedding
 * probe (the server owns all of that). Local file reads for always-inject
 * files (SOUL.md, IDENTITY.md, etc.) go through the workspace resolver
 * provided by the plugin API.
 */

import { readFile, stat } from "node:fs/promises";
import path from "node:path";

import type { ResolvedPluginConfig } from "./config.js";
import { EpMcpClient, type EpSearchResult } from "./client.js";
import { GeminiEmbedder } from "./embed.js";

/**
 * Narrow structural type matching OpenClaw's MemorySearchManager host
 * interface. We intentionally declare it inline rather than importing from
 * `openclaw` at build time so the plugin has zero compile-time coupling to
 * a specific host version; the plugin SDK types.d.ts drives the real contract
 * at load time.
 */
export interface HostMemorySearchManager {
  search(
    query: string,
    opts?: {
      maxResults?: number;
      minScore?: number;
      sessionKey?: string;
      qmdSearchModeOverride?: "query" | "search" | "vsearch";
      onDebug?: (debug: {
        backend: "builtin" | "qmd";
        configuredMode?: string;
        effectiveMode?: string;
        fallback?: string;
      }) => void;
    },
  ): Promise<
    Array<{
      path: string;
      startLine: number;
      endLine: number;
      score: number;
      snippet: string;
      source: "memory" | "sessions";
      citation?: string;
    }>
  >;
  readFile(params: {
    relPath: string;
    from?: number;
    lines?: number;
  }): Promise<{
    text: string;
    path: string;
    truncated?: boolean;
    from?: number;
    lines?: number;
    nextFrom?: number;
  }>;
  status(): {
    backend: "builtin" | "qmd";
    provider: string;
    model?: string;
    files?: number;
    chunks?: number;
    workspaceDir?: string;
    custom?: Record<string, unknown>;
  };
  sync?(): Promise<void>;
  probeEmbeddingAvailability(): Promise<{ ok: boolean; error?: string }>;
  probeVectorAvailability(): Promise<boolean>;
  close?(): Promise<void>;
}

export type SearchManagerOptions = {
  config: ResolvedPluginConfig;
  workspaceDir: string;
  logger?: {
    info?(message: string): void;
    warn?(message: string): void;
    debug?(message: string): void;
    error?(message: string): void;
  };
};

export class EpMemorySearchManager implements HostMemorySearchManager {
  private readonly cfg: ResolvedPluginConfig;
  private readonly workspaceDir: string;
  private readonly client: EpMcpClient;
  private readonly embedder: GeminiEmbedder;
  private readonly log: SearchManagerOptions["logger"];
  private lastRequestCount = 0;
  private lastEmbedCount = 0;

  constructor(opts: SearchManagerOptions) {
    this.cfg = opts.config;
    this.workspaceDir = opts.workspaceDir;
    this.log = opts.logger;
    this.client = new EpMcpClient({
      endpoint: this.cfg.endpoint,
      apiKey: this.cfg.apiKey,
      timeoutMs: this.cfg.timeoutMs,
      logger: opts.logger,
    });
    this.embedder = new GeminiEmbedder(this.cfg.embedding);
  }

  async search(
    query: string,
    opts: Parameters<HostMemorySearchManager["search"]>[1] = {},
  ): Promise<
    Awaited<ReturnType<HostMemorySearchManager["search"]>>
  > {
    const trimmed = query?.trim();
    if (!trimmed) return [];

    const maxResults = opts.maxResults ?? this.cfg.maxResults;
    const minScore = opts.minScore ?? this.cfg.minScore;
    this.lastRequestCount++;

    opts.onDebug?.({
      backend: "builtin",
      configuredMode: "vsearch",
      effectiveMode: "ep-mcp-remote",
    });

    let vector: number[];
    try {
      vector = await this.embedder.embed(trimmed);
      this.lastEmbedCount++;
    } catch (err) {
      this.log?.warn?.(
        `ep-memory-mcp: embed failed (${(err as Error).message}); ` +
          `falling back to server-side embed`,
      );
      vector = [] as number[];
    }

    let response;
    try {
      response = await this.client.search({
        query: trimmed,
        pack: this.cfg.pack,
        n: maxResults,
        vector: vector.length > 0 ? vector : null,
      });
    } catch (err) {
      this.log?.error?.(
        `ep-memory-mcp: search failed: ${(err as Error).message}`,
      );
      return [];
    }

    return response.results
      .filter((r) => r.score >= minScore)
      .map((r) => this.toHostResult(r));
  }

  private toHostResult(r: EpSearchResult): Awaited<
    ReturnType<HostMemorySearchManager["search"]>
  >[number] {
    const snippet = this.formatSnippet(r);
    const lineCount = Math.max(1, r.text.split("\n").length);
    return {
      path: r.source_file,
      startLine: 1,
      endLine: lineCount,
      score: r.score,
      snippet,
      source: "memory",
      citation: r.source_file,
    };
  }

  private formatSnippet(r: EpSearchResult): string {
    const flags: string[] = [];
    if (r.requires_expanded) flags.push("requires-expanded");
    if (r.graph_expanded) flags.push("graph-expanded");
    const flagLine = flags.length > 0 ? `\n<!-- ${flags.join(", ")} -->` : "";
    // EP MCP already strips frontmatter; preserve the body verbatim.
    return `${r.text}${flagLine}`;
  }

  async readFile(params: {
    relPath: string;
    from?: number;
    lines?: number;
  }): Promise<{
    text: string;
    path: string;
    truncated?: boolean;
    from?: number;
    lines?: number;
    nextFrom?: number;
  }> {
    const { relPath } = params;
    const from = Math.max(1, params.from ?? 1);
    const maxLines = params.lines ?? 400;

    // Only allow reads for files declared in includeLocalFiles, or paths
    // whose basename matches one of those entries. This keeps the plugin
    // from exposing arbitrary workspace files via the memory surface.
    const allowList = this.cfg.includeLocalFiles;
    const normalized = relPath.replace(/^\/+/, "");
    const allowed = allowList.some(
      (entry) => entry === normalized || path.basename(entry) === path.basename(normalized),
    );
    if (!allowed) {
      this.log?.debug?.(
        `ep-memory-mcp: readFile '${normalized}' denied — not in includeLocalFiles`,
      );
      return { text: "", path: relPath, truncated: false, from, lines: 0 };
    }

    const absolute = path.resolve(this.workspaceDir, normalized);
    try {
      await stat(absolute);
    } catch {
      return { text: "", path: relPath, truncated: false, from, lines: 0 };
    }

    const raw = await readFile(absolute, "utf8");
    const allLines = raw.split("\n");
    const slice = allLines.slice(from - 1, from - 1 + maxLines);
    const truncated = from - 1 + slice.length < allLines.length;
    return {
      text: slice.join("\n"),
      path: relPath,
      truncated,
      from,
      lines: slice.length,
      nextFrom: truncated ? from + slice.length : undefined,
    };
  }

  status(): ReturnType<HostMemorySearchManager["status"]> {
    return {
      backend: "builtin",
      provider: "ep-mcp",
      model: this.cfg.embedding.model,
      workspaceDir: this.workspaceDir,
      custom: {
        endpoint: this.cfg.endpoint,
        pack: this.cfg.pack,
        requestCount: this.lastRequestCount,
        embedCount: this.lastEmbedCount,
        includeLocalFiles: this.cfg.includeLocalFiles,
      },
    };
  }

  async sync(): Promise<void> {
    // Indexing is owned by the EP MCP server; nothing to do here.
  }

  async probeEmbeddingAvailability(): Promise<{ ok: boolean; error?: string }> {
    try {
      const vec = await this.embedder.embed("ping");
      if (!Array.isArray(vec) || vec.length === 0) {
        return { ok: false, error: "empty vector" };
      }
      return { ok: true };
    } catch (err) {
      return { ok: false, error: (err as Error).message };
    }
  }

  async probeVectorAvailability(): Promise<boolean> {
    // The EP MCP server is the vector store. If we can embed, we can search.
    const { ok } = await this.probeEmbeddingAvailability();
    return ok;
  }

  async close(): Promise<void> {
    // Stateless HTTP client; no resources to release.
  }
}
