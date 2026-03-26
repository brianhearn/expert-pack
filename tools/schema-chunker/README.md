# Schema-Aware Chunker

Pre-processes ExpertPack `.md` files into optimally-sized chunk files for [OpenClaw](https://openclaw.ai)'s RAG indexer.

## The Problem

OpenClaw's built-in chunker splits files by character count — it doesn't understand markdown structure. It will happily slice a lead summary in half, split a proposition from its header, or orphan a `<!-- refresh -->` metadata block. The result: degraded retrieval quality despite carefully structured content.

## The Solution

The schema-aware chunker understands ExpertPack conventions and produces one `.md` file per semantic chunk, each sized to fit within OpenClaw's token budget. OpenClaw's chunker then passes each file through as a single chunk — no splitting, no lost context.

**What it respects:**
- `##` headers as semantic boundaries (never splits mid-section)
- Lead summaries stay with their `# Title`
- Proposition groups (`### source.md` + bullet list) stay intact
- `<!-- refresh -->` metadata stays attached to its content
- YAML frontmatter stays with the first chunk
- Glossary category tables stay together
- `_index.md` files chunked as single units when possible
- **Atomic vs. sectioned strategies** — workflows and troubleshooting files are emitted as single chunks (never split); reference content is split on `##` headers
- **Per-file overrides** via `retrieval.strategy` frontmatter
- **Sequence metadata** in source comments for sectioned splits (`part X of Y`, glob pattern)

## Quick Start

```bash
# Basic usage
python3 chunk.py --pack ./packs/my-pack --output ./packs/my-pack/.chunks

# With custom chunk size
python3 chunk.py --pack ./packs/my-pack --output ./packs/my-pack/.chunks --max-chars 2400

# Read token budget from OpenClaw config
python3 chunk.py --pack ./packs/my-pack --output ./packs/my-pack/.chunks --config ~/.openclaw/openclaw.json

# Verbose output (shows per-file details)
python3 chunk.py --pack ./packs/my-pack --output ./packs/my-pack/.chunks --verbose
```

## OpenClaw Integration

After chunking, update your OpenClaw config to index `.chunks/` instead of the raw pack:

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "extraPaths": [
          "path/to/pack/.chunks"
        ]
      }
    }
  }
}
```

**Recommended OpenClaw query settings for chunked packs:**

```json
{
  "memorySearch": {
    "chunking": { "tokens": 500, "overlap": 0 },
    "query": {
      "hybrid": {
        "enabled": true,
        "mmr": { "enabled": true, "lambda": 0.7 },
        "temporalDecay": { "enabled": false }
      }
    }
  }
}
```

- **Overlap 0** — chunks are already semantically complete; overlap would just duplicate content
- **MMR enabled** — prevents near-duplicate proposition/summary/content chunks from crowding results
- **Temporal decay off** — pack knowledge doesn't expire based on file modification time

## CLI Reference

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--pack` | Yes | — | Path to ExpertPack directory |
| `--output` | Yes | — | Output directory (created if needed, cleared on each run) |
| `--max-chars` | No | 2000 | Max characters per chunk file (~500 tokens) |
| `--config` | No | — | Path to `openclaw.json` — reads `chunking.tokens` × 4 |
| `--verbose` | No | — | Print per-file chunking details |

## Chunking Strategies

*(Schema 2.4+)*

The chunker applies one of two strategies per file:

| Strategy | Behavior | Default For |
|----------|----------|-------------|
| **atomic** | Emit the entire file as a single chunk. Never split. | `workflows/`, `troubleshooting/errors/`, `troubleshooting/diagnostics/`, `troubleshooting/common-mistakes/` |
| **sectioned** | Split on `##` headers, then `###` if oversized, then paragraphs. | `concepts/`, `interfaces/`, `faq/`, `propositions/`, `summaries/`, `commercial/`, all others |

**Why it matters:** Workflows and troubleshooting files are step-by-step procedures or symptom → cause → fix units. Splitting them produces hallucinated instructions — the model fills gaps with fabricated content. These files must be retrieved whole or not at all.

### Precedence

1. **Frontmatter override** — `retrieval.strategy: atomic` or `sectioned` in YAML frontmatter
2. **Directory default** — based on ExpertPack directory conventions (table above)
3. **Fallback** — `sectioned`

Override example:

```yaml
---
retrieval:
  strategy: atomic
---
```

### Sectioned Split Hierarchy

For sectioned files, splitting is tried in order (falls back to next):

1. **`##` headers** — each section becomes a candidate chunk
2. **`###` headers** — if a section is still too large
3. **Paragraph boundaries** — double newlines
4. **Line boundaries** — single newlines (never splits mid-line)

### Source Comments

**Each chunk file includes a source comment:**

```markdown
<!-- source: concepts/routing-optimizer.md | section: How It Works | tier: 2 -->
The TSP optimizer uses a genetic algorithm with population size 32...
```

For sectioned splits, chunks include sequence metadata:

```markdown
<!-- source: concepts/territories.md | section: How It Works (part 3 of 7) | sequence: concepts--territories--*.md -->
```

The `part X of Y` tells the consuming agent this is a fragment. The `sequence` glob tells it where to find the full set.

This metadata aids embedding quality and enables source citations.

### Filename Convention

Standard: `{dir}--{file}--{section-slug}.md`

```
concepts--routing-optimizer--how-it-works.md
propositions--concepts.md
glossary--territory-terms.md
troubleshooting--upload-failures--lead.md
```

Atomic files that exceed size limits produce `{name}--summary.md` and `{name}--full.md`.

## Output

The tool produces:

1. **`.chunks/*.md`** — one file per semantic chunk
2. **`.chunks/_manifest.json`** — metadata about the chunking run:

```json
{
  "generated": "2026-03-13T13:35:00Z",
  "pack": "my-pack",
  "source_files": 45,
  "chunks_produced": 120,
  "max_chars": 2000,
  "avg_chunk_chars": 1200,
  "coverage": {
    "included": ["concepts/routing.md", "..."],
    "skipped": ["manifest.yaml", "eval/..."]
  }
}
```

3. **Console summary:**

```
Schema Chunker — my-pack
────────────────────────────────────────
Source files:    45
Chunks produced: 120
Avg chunk size:  1,200 chars
Max chunk budget: 2,000 chars
Files skipped:   8
Coverage: 100% of content files
Output:   ./packs/my-pack/.chunks/
```

## What Gets Skipped

- `manifest.yaml` — pack identity, not search content
- `eval/` — test data, not knowledge
- `meta/changelog.md` — maintenance metadata
- `.chunks/` — won't re-chunk its own output
- Hidden files/dirs (`.git`, etc.)
- Non-`.md` files

## Dependencies

Python 3.10+ standard library only. No pip installs required.

(Uses PyYAML if available for `manifest.yaml` parsing, falls back to built-in parser.)

## License

Apache 2.0 — part of the [ExpertPack](https://github.com/brianhearn/ExpertPack) framework.
