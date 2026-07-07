# RFC-003: Fragment Provenance and Reconstruct Mode

- **Status:** Accepted (spec + in-repo consumer contract; EP MCP runtime shipped 2026-07-06)
- **Author:** Brian Hearn (with EasyBot)
- **Created:** 2026-07-06
- **Target:** Schema 4.1 (additive — no breaking changes)
- **Companion:** `schemas/core.md` § "Fragment Provenance and Reconstruct Mode"

---

## Summary

Extend the file-level Citation Response Contract with a **span-level fragment
provenance** envelope so a retriever can prove *which part* of a file it
returned and that the span was not modified. This is the retrieval-layer
contract behind "Reconstruct Mode": discovery is done by vectors, but
verification is done by `source_file` + `line_range` + a content-addressed span
hash.

This directly attacks the dominant RAG failure mode. The problem is rarely
ranking quality — it is provenance. Vector-only retrieval returns plausible text
with no verifiable link to an exact source span, so downstream answers "sound
right" but cannot be traced or audited.

## Motivation

The existing Citation Response Contract returns `file`, `id`, `content_hash`,
`verified_at`, and an `excerpt`. That is enough to cite a *file*, but not enough
to:

1. Point a human at the exact lines that grounded a claim.
2. Prove the cited span is byte-for-byte what was indexed (not paraphrased or
   drifted).
3. Detect when a previously cited fragment has gone stale because its source
   changed.

ExpertPack already ships the ingredients: per-file `content_hash` (Schema 3.0),
the AKS export with `source_span_uri` and `source_checksum`, and header-boundary
chunking in EP MCP. What was missing is a stable, content-addressed **fragment
identity** and a response envelope that carries it end to end.

## Design

### Fragment ID

```
{id}#{section-slug}:{sha256-prefix}
```

- `id` — the source atom's stable frontmatter id (e.g. `blender-3d/concepts/modeling-topology`).
- `section-slug` — kebab-cased nearest `##`/`###` heading above the span, or
  `opening` for the lead paragraph (the retrieval anchor).
- `sha256-prefix` — first 12 hex characters of the SHA-256 of the exact span
  text.

Example:

```
blender-3d/concepts/modeling-topology#why-topology-matters:a3f1c0d29e4b
```

The ID is stable across re-indexes while the span text is unchanged. Any edit to
the span changes its hash and therefore its fragment ID — which is precisely the
staleness signal. This mirrors the file-level `content_hash` semantics one level
down, at the chunk.

### Response envelope

Returned per result when Reconstruct Mode is requested (see `schemas/core.md`
for the field list): `fragment_id`, `source_file`, `id`, `line_range`,
optional `byte_offset`, span `content_hash`, `verified_at`, `excerpt`,
`original_markdown` (host-rendered with the match highlighted), and a `stale`
flag set when the span hash no longer matches the file's frontmatter
`content_hash`.

### Verification

A consumer verifies a citation without trusting the retriever:

1. Open `source_file`, read `line_range`.
2. Recompute the SHA-256 of that span.
3. Compare the prefix to the `sha256-prefix` in `fragment_id` and to the file's
   frontmatter `content_hash`.

If they match, the citation is proven. If not, the fragment is stale or
tampered.

### Opt-in

Reconstruct Mode is behind a flag (`reconstruct=true`) because returning
`original_markdown` costs tokens. Normal retrieval keeps returning compact
results; Reconstruct Mode is used when auditability matters more than token cost.

## Scope and repository boundary

| Layer | Where | This RFC |
|-------|-------|----------|
| Spec / contract | `schemas/core.md`, this RFC | Defined here |
| Consumer types | `tools/openclaw-memory-plugin` (`EpSearchResult`, `reconstruct` request flag) | Wired here |
| AKS projection | `schemas/registry/agent-knowledge.spec.yaml` (`fragment_id`, `line_range`, `span_hash`) | Extended here |
| Runtime span offsets, hashing, highlighting | EP MCP (`/search?reconstruct=true`) | External milestone |

The authoring repo defines the contract and the consumer-side plumbing so EP MCP
has a stable target to implement against. The runtime that stores per-chunk line
offsets, verifies span hashes at query time, and renders highlighted markdown
lives in EP MCP.

## Interaction with existing schema

- **RFC-001 atomic model:** For a whole-file atom the fragment collapses to the
  file (`section-slug = opening`, span = body), so file-level and fragment-level
  provenance agree. Fragments matter for oversized/reference files that split at
  `##`/`###` boundaries — see RFC-004 chunk sidecars for how those boundaries
  and offsets are recorded.
- **`content_hash`:** unchanged; the fragment span hash is a narrower sibling.
- **AKS:** `source_span_uri` remains file-level; fragment fields are additive.

## EP MCP runtime implementation checklist (handoff)

The authoring repo owns the contract; EP MCP owns the runtime. To close the
loop, the EP MCP server needs to:

1. **Index-time:** when chunking a file (header-boundary split per RFC-001, or a
   RFC-004 chunk sidecar when present), store per-chunk `line_range`, optional
   `byte_offset`, the `section-slug`, and the span SHA-256 alongside the vector.
2. **Query-time:** accept `reconstruct: true` in the POST `/search` body
   (already forwarded by the in-repo OpenClaw plugin) and, for each hit, return
   the fragment envelope defined in `schemas/core.md`: `fragment_id`,
   `source_file`, `id`, `line_range`, optional `byte_offset`, span
   `content_hash`, `verified_at`, `excerpt`, `original_markdown`, and `stale`.
3. **Fragment ID:** compose `{id}#{section-slug}:{sha256-prefix}` where the
   prefix is the first 12 hex chars of the span hash.
4. **Staleness:** recompute the span hash from the current source at query time
   and set `stale: true` when it differs from the indexed hash (or from the
   file's frontmatter `content_hash`).
5. **Back-compat:** when `reconstruct` is false or unset, return the existing
   compact result shape unchanged.

The in-repo consumer (`tools/openclaw-memory-plugin`) already sends the flag and
renders the returned fields. EP MCP shipped this runtime on 2026-07-06
(`ep-mcp` commit `a9d1639`). Remaining operational step: reindex packs that
gained `.chunks.yaml` sidecars so `line_range` / `span_hash` are populated.

## Open questions

- Whether to persist fragment IDs in the AKS export or compute them at query
  time only (leaning: compute at query time, persist chunk boundaries via the
  RFC-004 sidecar).
- Highlight rendering is host-dependent; the contract only guarantees the span
  coordinates and hash, not a specific rendering.
