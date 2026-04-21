---
id: blender-3d/concepts/core-architecture-blend-file
title: "Core Architecture — The .blend File Format"
type: concept
tags:
  - architecture
  - blend-file
  - file-format
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-04-21"
verified_by: agent
supersedes:
  - concepts/core-architecture.md
related:
  - core-architecture-data-blocks.md
---

# Core Architecture — The .blend File Format

---

## Key Properties

The `.blend` file is a binary format containing all data-blocks in the file.

**Self-contained by default:** All meshes, materials, node trees, and scenes are embedded. Images can be embedded (packed) or referenced externally.

**Backward compatible:** Older .blend files can be opened in newer Blender versions with automatic conversion. Forward compatibility (newer files in older versions) is not guaranteed.

**Appendable/Linkable:** Any data-block from any .blend file can be appended (copied) or linked (live reference) into another file. This is the basis for professional asset libraries and production pipelines.

**Compression:** Blender can use LZ4 or Zstandard compression for .blend files. Compressed files are significantly smaller but slightly slower to open.

**Recovery:** Blender auto-saves to a temp file and keeps `quit.blend` (file state when Blender was closed). Accessible via `File → Recover`.

---

## Linked vs Appended Assets

**Append:** Copies the data-block into the current file. The copy is independent — changes to the source file don't update the copy.

**Link:** Creates a live reference to the data-block in another file. Changes to the source file propagate to all linked users. The linked data-block is read-only — you can't edit it directly (use Library Overrides for that).

**Library Overrides:** Allows modifying specific properties of linked data-blocks while keeping the rest live-linked. Used in production pipelines to customize linked characters/environments without breaking the link.

---

## External Data Management

Images and media referenced by path can become broken if files are moved. Key commands:

- `File → External Data → Find Missing Files` — locate and relink missing files
- `File → External Data → Pack Resources` — embed all external files into the .blend
- `File → External Data → Unpack Resources` — extract packed files to disk

**Best practice for projects with many assets:** Use relative paths (`//` prefix) so the .blend file finds assets relative to its own location. Move the whole project folder together, not individual files.
