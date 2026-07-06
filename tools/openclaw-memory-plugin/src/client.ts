/**
 * EP MCP HTTP client.
 *
 * Wraps the POST /search endpoint introduced in ep-mcp v0.5 (caller-supplied
 * vector). GET /search is not used here because passing a 3072-element vector
 * in a URL is both impractical and, on some proxies, over the limit.
 *
 * The client is intentionally small: one endpoint, bearer auth, JSON in/out,
 * AbortSignal support. All tuning knobs live in PluginConfig; this module
 * just marshals the request.
 */

export type EpSearchResult = {
  source_file: string;
  title?: string | null;
  text: string;
  score: number;
  type?: string | null;
  tags?: string[];
  graph_expanded?: boolean;
  requires_expanded?: boolean;
  // Fragment provenance (RFC-003 Reconstruct Mode). Present when the request
  // sets reconstruct=true and the server supports it.
  fragment_id?: string | null;
  id?: string | null;
  line_range?: [number, number] | null;
  byte_offset?: [number, number] | null;
  content_hash?: string | null;
  verified_at?: string | null;
  original_markdown?: string | null;
  stale?: boolean;
};

export type EpSearchResponse = {
  query: string;
  pack: string;
  vector_supplied?: boolean;
  results: EpSearchResult[];
};

export type EpSearchRequest = {
  query: string;
  pack: string;
  n?: number;
  type?: string | null;
  tags?: string[] | null;
  vector?: number[] | null;
  /** Ask the server for span-level provenance envelopes (RFC-003). */
  reconstruct?: boolean;
};

export type EpClientOptions = {
  endpoint: string;
  apiKey?: string;
  timeoutMs: number;
  /** Optional logger — host plugin logger, falls back to no-op. */
  logger?: {
    warn?(message: string): void;
    debug?(message: string): void;
  };
};

export class EpMcpClient {
  private readonly endpoint: string;
  private readonly apiKey: string | undefined;
  private readonly timeoutMs: number;
  private readonly log: EpClientOptions["logger"];

  constructor(opts: EpClientOptions) {
    this.endpoint = opts.endpoint.replace(/\/+$/, "");
    this.apiKey = opts.apiKey;
    this.timeoutMs = opts.timeoutMs;
    this.log = opts.logger;
  }

  async search(
    req: EpSearchRequest,
    signal?: AbortSignal,
  ): Promise<EpSearchResponse> {
    const url = `${this.endpoint}/search`;
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    };
    if (this.apiKey) {
      headers.Authorization = `Bearer ${this.apiKey}`;
    }

    // Link caller signal + local timeout into one controller.
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeoutMs);
    const onExternalAbort = () => controller.abort();
    if (signal) {
      if (signal.aborted) controller.abort();
      else signal.addEventListener("abort", onExternalAbort, { once: true });
    }

    try {
      const response = await fetch(url, {
        method: "POST",
        headers,
        body: JSON.stringify({
          query: req.query,
          pack: req.pack,
          n: req.n ?? 10,
          type: req.type ?? null,
          tags: req.tags ?? null,
          vector: req.vector ?? null,
          reconstruct: req.reconstruct ?? false,
        }),
        signal: controller.signal,
      });

      if (!response.ok) {
        const text = await response.text().catch(() => "<unreadable>");
        throw new Error(
          `EP MCP /search failed (${response.status}): ${text.slice(0, 300)}`,
        );
      }

      const data = (await response.json()) as EpSearchResponse;
      if (!Array.isArray(data?.results)) {
        throw new Error("EP MCP /search: malformed response (missing results)");
      }
      this.log?.debug?.(
        `ep-memory-mcp: /search returned ${data.results.length} results ` +
          `(vector_supplied=${Boolean(data.vector_supplied)})`,
      );
      return data;
    } finally {
      clearTimeout(timer);
      if (signal) signal.removeEventListener("abort", onExternalAbort);
    }
  }
}
