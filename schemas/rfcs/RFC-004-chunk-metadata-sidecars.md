# RFC-004: Chunk Metadata Sidecars

- **Status:** Accepted (authoring format + tool + validator rules; EP MCP consumption tracked separately)
- **Author:** Brian Hearn (with EasyBot)
- **Created:** 2026-07-06
- **Target:** Schema 4.1 (additive)
- **Companion:** `tools/chunker/ep-chunk-annotate.py`, `schemas/registry/chunk-sidecar.spec.yaml`

---

## Summary

For files that legitimately exceed the one-atom size ceiling, record semantic
chunk boundaries in a **git-tracked YAML sidecar** next to the Markdown file
rather than in the file's frontmatter. This keeps chunk metadata out of the
embeddable body (avoiding the frontmatter-dilution problem) while giving the
indexer deterministic, semantic boundaries to split on and reassemble from.

## Motivation

Fixed-size chunking splits claims from their evidence and breaks section
structure, which measurably degrades retrieval. The atomic model (RFC-001) is
the primary answer — one concept, one file — but three cases still produce files
larger than a single retrieval unit:

- a `standard` file that has grown past the ~1,000-token ceiling,
- a multi-section reference file (`concept_scope: reference`),
- an oversized legacy file that has not yet been split during migration.

For these, we want header-aware chunking, not fixed windows. And we learned in
April that putting provenance/metadata *inside* the file that gets embedded
pulls the embedding off-axis. So chunk metadata belongs beside the file, not in
its frontmatter.

## Why a sidecar (not frontmatter)

A `chunks:` array in frontmatter would either be embedded (diluting the vector)
or require every indexer to strip it. A sidecar sidesteps both: `ep-strip-frontmatter`
already removes frontmatter for indexing, and the sidecar is read separately by
the chunker for boundaries. The only frontmatter addition is an optional pointer:
`chunks_sidecar: <name>.chunks.yaml`.

## Format

File pair:

```
concepts/modeling-topology.md
concepts/modeling-topology.chunks.yaml   # generated, git-tracked
```

Sidecar:

```yaml
schema_version: "1.0"
source_id: blender-3d/concepts/modeling-topology
content_hash: sha256:...        # of the frontmatter-stripped body; matches the .md
generated_by: ep-chunk-annotate
chunks:
  - chunk_id: modeling-topology--opening
    chunk_order: 0
    section: null                # null for the opening/lead chunk
    line_range: [23, 45]         # 1-indexed inclusive, in the source .md
    tokenizer_tokens: 312        # estimate
    embedding_version: text-embedding-004
    chunk_summary: "One-sentence retrieval anchor."
  - chunk_id: modeling-topology--why-topology-matters
    chunk_order: 1
    section: "Why Topology Matters"
    line_range: [47, 78]
    tokenizer_tokens: 401
    embedding_version: text-embedding-004
    chunk_summary: "Topology determines deformation, shading, and boolean quality."
```

- `chunk_id` = `{file-stem}--{section-slug}` (`opening` for chunk 0). Unique
  within the sidecar.
- `chunk_order` is 0-based and contiguous — this is what the indexer sorts by to
  reassemble the complete logical unit.
- `line_range` lines are in the source `.md` (including its frontmatter offset)
  so they line up with RFC-003 fragment provenance.
- `content_hash` matches the `.md` body hash, so the validator can detect drift
  between a file and its sidecar.

## Boundaries

Chunk 0 is the opening: the H1 and lead paragraph, which is the retrieval anchor.
Subsequent chunks start at each `##`/`###` heading and run to the next one.
Headings inside fenced code blocks are ignored. This matches the header-boundary
rule EP MCP already uses, so a pack chunks the same way with or without a
sidecar; the sidecar simply makes the split explicit, reviewable, and
deterministic.

## Tooling

`tools/chunker/ep-chunk-annotate.py` generates and checks sidecars:

- default (dry-run): print the chunk plan;
- `--apply`: write `<name>.chunks.yaml`;
- `--check`: regenerate and diff against disk (nonzero exit on drift) — for CI;
- `--min-tokens N`: only annotate files over the threshold (default 1000);
- `--all`: annotate every content file regardless of size.

## Validator rules

`ep-validate` adds (WARN by default):

- `W-CHUNK-01` — a file over the token ceiling (concept/reference, non-atomic)
  has no sidecar.
- `W-CHUNK-02` — sidecar `content_hash` does not match the file body.
- `W-CHUNK-03` — `chunk_order` has gaps/duplicates or `chunk_id` is duplicated.

These stay warnings so the sidecar remains opt-in; a pack that prefers to split
oversized files into true atoms (the RFC-001 default) never needs a sidecar.

## Repository boundary

The authoring repo owns the format, the generator, and the validator rules. EP
MCP consumes the sidecar at index time (boundaries + offsets) and reassembles by
`chunk_order`; when no sidecar is present it falls back to its built-in
header-boundary split. That runtime alignment is tracked as a separate EP MCP
milestone.
