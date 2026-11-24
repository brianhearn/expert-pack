---
title: "Changelog"
type: meta
tags:
- changelog
- meta
pack: solar-diy-product
retrieval_strategy: navigation
id: solar-diy-product/meta/changelog
schema_version: "4.1"
verified_at: "2026-11-24"
verified_by: agent
content_hash: sha256:ef74457f1dd3c9b34fc28f23a9eb5be476b2bd56af46cd636cf812ebd0337888
---

# Changelog

All notable changes to the Solar Technology Reference pack.

## [1.0.1] — 2026-11-24

### Added
- Pack content changelog at `meta/changelog.md`.
- Constituent eval suite (`eval/benchmark.yaml`) with `pack_type: product` and eval schema `version: "1.0"`.
- Restored `freshness.md` to `type: "volatile"` (core.md maps `freshness.md` to volatile) with `refresh: P90D`, `fetched_at: "2026-03-10"`, and `expires_at: "2026-06-08"` (last full review plus 90 days). A W-VOL-02 overdue warning is expected until the 2026 market tables are refreshed.
- Folded stray second-block `sources:` into the frontmatter of `specifications/solar-panels-2026.md` and `specifications/battery-systems-2026.md`.

### Changed
- Conformance pass for ExpertPack core 4.3 (tag `core-4.3`, `cd27fa6`) / product schema 4.1.
- `related:` links for previously orphaned FAQs, specifications, and troubleshooting atoms.
- Re-sealed `manifest.yaml` `integrity.pack_digest`.

### Notes
- Glossary, general FAQ, and 2026 specification sheets still exceed the 6,000-character advisory size warning; they were not split in this pass.

