/**
 * Typed Answer Contract (TAC) v1 types.
 *
 * Mirrors schemas/registry/typed-answer.schema.json. TAC is the response layer
 * that sits on top of the Fragment Provenance retrieval layer (RFC-003): every
 * claim an agent makes maps to one or more retrieved source fragments, so
 * answers can be audited and machine-verified.
 *
 * These are types only — validation lives in tools/tac/validate_tac.py. Use
 * isTypedAnswer() for a cheap runtime shape guard before trusting an envelope.
 */

export type TacRetrievalMode = 'standard' | 'reconstruct';
export type TacSupport = 'supported' | 'partial' | 'unsupported';
export type TacConfidence = 'expert-verified' | 'crawled' | 'inferred';

export type TacSource = {
  /** RFC-003 fragment ID. Required when retrieval_mode is 'reconstruct'. */
  fragment_id?: string;
  /** Source atom frontmatter id (file-level citation). */
  id?: string;
  /** Pack-relative source path. */
  source_file?: string;
  /** Supporting passage copied from the source. */
  excerpt?: string;
  /** Hash of the cited span/file at answer time, `sha256:<64 hex>`. */
  content_hash?: string;
  /** How strongly this source backs the claim. */
  support: TacSupport;
};

export type TacClaim = {
  claim_id: string;
  text: string;
  confidence?: TacConfidence;
  sources: TacSource[];
};

export type TypedAnswer = {
  schema: 'expertpack.typed_answer.v1';
  answer_id: string;
  pack: string;
  retrieval_mode: TacRetrievalMode;
  answer_text?: string;
  generated_at?: string;
  model?: string;
  unsupported_note?: string;
  claims: TacClaim[];
};

/**
 * Cheap runtime shape guard. This is NOT the full contract check — use
 * tools/tac/validate_tac.py for the authoritative structural + semantic
 * validation. This only confirms the envelope is safe to read as a TypedAnswer.
 */
export function isTypedAnswer(value: unknown): value is TypedAnswer {
  if (typeof value !== 'object' || value === null) return false;
  const v = value as Record<string, unknown>;
  return (
    v.schema === 'expertpack.typed_answer.v1' &&
    typeof v.answer_id === 'string' &&
    typeof v.pack === 'string' &&
    (v.retrieval_mode === 'standard' || v.retrieval_mode === 'reconstruct') &&
    Array.isArray(v.claims)
  );
}
