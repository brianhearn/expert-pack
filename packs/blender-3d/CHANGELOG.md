# Changelog

All notable changes to the Blender 3D ExpertPack.

## [1.0.1] — 2026-11-24

### Added
- Pack CHANGELOG for release tracking.

### Changed
- Conformance pass for ExpertPack core 4.2 / product schema 4.1 (spec `da51888`).
- Reciprocal `related:` links for previously unidirectional concept links, orphaned FAQs, and workflows.
- Set `concept_scope: multi` on `concepts/geometry-nodes-flow-creation.md` (W-HUB-01).
- Re-sealed `manifest.yaml` `integrity.pack_digest` after the edits.

### Notes
- `integrity_status` remains `unsigned` until a pack signature is added; the digest itself is sealed and should report `digest_verified=true`.
- Glossary and `_community-mining-2026-03-13.md` still exceed the 6,000-character advisory size warning; they were not split in this pass.
