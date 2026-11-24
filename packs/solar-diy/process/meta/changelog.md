---
title: "Changelog"
type: meta
tags:
- changelog
- meta
pack: solar-diy-process
retrieval_strategy: navigation
id: solar-diy-process/meta/changelog
schema_version: "4.1"
verified_at: "2026-11-24"
verified_by: agent
content_hash: sha256:15d520dcc54649c22c3a7eb9583bbb2d22c12f824d180c1b867b22f12b4ef098
---

# Changelog

All notable changes to the Residential Solar Installation Process pack.

## [1.0.1] — 2026-11-24

### Added
- Pack content changelog at `meta/changelog.md`.
- Constituent eval suite (`eval/benchmark.yaml`) with `pack_type: process` and eval schema `version: "1.0"`.
- Phase-chain and decision `related:` links so process atoms are no longer orphaned.

### Changed
- Conformance pass for ExpertPack core 4.3 (tag `core-4.3`, `cd27fa6`) / process schema 4.1.
- Re-sealed `manifest.yaml` `integrity.pack_digest`.

### Notes
- Three decision files still exceed the 6,000-character advisory size warning; they are long-form decision atoms and were not split in this pass.

