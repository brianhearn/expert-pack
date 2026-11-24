---
title: "Changelog"
type: meta
tags:
- changelog
- meta
pack: home-assistant-product
retrieval_strategy: navigation
id: home-assistant-product/meta/changelog
schema_version: "4.1"
verified_at: "2026-11-24"
verified_by: agent
content_hash: sha256:f51c395bbb743c34f02e544238c711431fe9df3e9229f4b1dc67fdd3063eb646
---

# Changelog

All notable changes to the Home Assistant Platform Reference pack.

## [2.0.1] — 2026-11-24

### Added
- Pack content changelog at `meta/changelog.md`.
- Constituent eval suite (`eval/benchmark.yaml`) with `pack_type: product` and eval schema `version: "1.0"`.

### Changed
- Conformance pass for ExpertPack core 4.3 (tag `core-4.3`, `cd27fa6`) / product schema 4.1.
- Reciprocal `related:` links for previously unidirectional concept links and orphaned FAQs.
- Re-sealed `manifest.yaml` `integrity.pack_digest`.

### Notes
- `faq/common-questions.md` and `faq/zigbee2mqtt-2-migration.md` still exceed the 6,000-character advisory size warning; they were not split in this pass.

