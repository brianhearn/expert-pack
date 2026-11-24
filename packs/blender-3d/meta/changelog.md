---
title: "Changelog"
type: meta
tags:
- changelog
- meta
pack: blender-3d
retrieval_strategy: navigation
id: blender-3d/meta/changelog
schema_version: "4.1"
verified_at: "2026-11-24"
verified_by: agent
content_hash: sha256:7a310afbcd0d43124cc40791c4435e04250915817fc4115aaa7982341d869171
---

# Changelog

All notable changes to the Blender 3D ExpertPack.

## [1.0.1] — 2026-11-24

### Added
- Pack content changelog at `meta/changelog.md` (core.md Content Changelog).

### Changed
- Conformance pass for ExpertPack core 4.3 (tag `core-4.3`, `cd27fa6`) / product schema 4.1.
- Reciprocal `related:` links for previously unidirectional concept links, orphaned FAQs, and workflows.
- Set `concept_scope: multi` on `concepts/geometry-nodes-flow-creation.md` (W-HUB-01).
- Re-sealed `manifest.yaml` `integrity.pack_digest` after the edits.

### Notes
- `integrity_status` remains `unsigned` until a pack signature is added; the digest itself is sealed and should report `digest_verified=true`.
- Glossary and `_community-mining-2026-03-13.md` still exceed the 6,000-character advisory size warning; they were not split in this pass.

