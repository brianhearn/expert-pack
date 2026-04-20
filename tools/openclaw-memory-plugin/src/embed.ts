/**
 * Minimal Gemini embedding client.
 *
 * Calls the REST `models.embedContent` endpoint directly. No SDK dependency,
 * no bundled transitive HTTP stack — just `fetch`. The caller is responsible
 * for handling rate limits and retries; this module keeps a single failing
 * attempt simple so the host logger gets a clean error message.
 */

import type { ResolvedEmbeddingConfig } from "./config.js";

export type GeminiEmbedOptions = {
  signal?: AbortSignal;
};

export class GeminiEmbedder {
  constructor(private readonly cfg: ResolvedEmbeddingConfig) {
    if (!cfg.apiKey) {
      throw new Error("ep-memory-mcp: embedding.apiKey is required");
    }
  }

  async embed(query: string, opts: GeminiEmbedOptions = {}): Promise<number[]> {
    const url =
      `https://generativelanguage.googleapis.com/v1beta/models/` +
      `${encodeURIComponent(this.cfg.model)}:embedContent?key=` +
      `${encodeURIComponent(this.cfg.apiKey)}`;

    const body: Record<string, unknown> = {
      model: `models/${this.cfg.model}`,
      content: { parts: [{ text: query }] },
      taskType: this.cfg.taskType,
    };
    if (this.cfg.outputDimensionality) {
      body.outputDimensionality = this.cfg.outputDimensionality;
    }

    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal: opts.signal,
    });

    if (!response.ok) {
      const text = await response.text().catch(() => "<unreadable>");
      throw new Error(
        `Gemini embed failed (${response.status}): ${text.slice(0, 300)}`,
      );
    }

    const data = (await response.json()) as {
      embedding?: { values?: number[] };
    };
    const values = data?.embedding?.values;
    if (!Array.isArray(values) || values.length === 0) {
      throw new Error("Gemini embed: empty response");
    }
    return values;
  }
}
