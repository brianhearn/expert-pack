# Obsidian Setup for ExpertPack

This `.obsidian/` folder makes any ExpertPack a native Obsidian vault.

## First-Time Setup

1. Open Obsidian → **Open folder as vault** → select any pack directory (e.g. `packs/blender-3d/`) or the repo root
2. Go to **Settings → Community plugins → Browse** and install:
   - **Dataview** — live queries over pack content
   - **Templater** *(optional)* — for creating new content with EP-schema frontmatter
3. Enable both plugins

## Key Settings (pre-configured)

- **Link format:** Relative path (not wikilinks) — preserves GitHub compatibility
- **Markdown links:** Enabled — standard `[text](file.md)` syntax throughout
- **New link format:** Relative to file
- **Graph view filter:** `_index.md` files excluded by default — reveals concept topology without hub-spoke noise. To see index nodes: open Graph View → Filters → clear the search field.

## Useful Dataview Queries

Paste these into any note to create live dashboards:

### All concepts in a pack
```dataview
TABLE title, tags
FROM "concepts"
WHERE type = "concept"
SORT title ASC
```

### High-EK content (where ek_score is set)
```dataview
TABLE title, ek_score, type
FROM ""
WHERE ek_score >= 0.7
SORT ek_score DESC
```

### Atomic files (workflows + troubleshooting)
```dataview
TABLE title, type
FROM ""
WHERE retrieval_strategy = "atomic"
SORT type ASC
```

### Volatile files needing refresh
```dataview
TABLE title, file.mtime
FROM ""
WHERE type = "volatile"
SORT file.mtime ASC
```

### All files by type
```dataview
TABLE rows.file.link as Files
FROM ""
WHERE type != null
GROUP BY type
```

## Notes

- The `.obsidian/` folder is checked into the EP repo as a reference configuration
- Copy it into any EP pack directory to make that pack Obsidian-ready
- Graph view excludes `_index.md` by default — shows concept relationships, not navigation hubs
- Add `related:` frontmatter to content files for richer graph cross-links between sections
- ExpertPack content is fully readable/editable without Obsidian — plain `.md` files always
