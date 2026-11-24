---
title: "Changelog"
type: meta
tags:
- changelog
- meta
pack: home-assistant-process
retrieval_strategy: navigation
id: home-assistant-process/meta/changelog
schema_version: "4.1"
verified_at: "2026-11-24"
verified_by: agent
content_hash: sha256:7a7ce6a951c320519d6d661033afe6038c97ef0b7e44d2fe4775fcef90e2f3a3
---

# Changelog

All notable changes to the Building a Smart Home with Home Assistant process pack.

## [1.0.1] — 2026-11-24

### Added
- Pack content changelog at `meta/changelog.md`.
- Constituent eval suite (`eval/benchmark.yaml`) with `pack_type: process` and eval schema `version: "1.0"`.
- Folded stray second-block `sources:` into the frontmatter of `patterns/climate-control.md`, `motion-lighting.md`, `notification-patterns.md`, and `security-monitoring.md`.

### Changed
- Conformance pass for ExpertPack core 4.3 (tag `core-4.3`, `cd27fa6`) / process schema 4.1.
- Re-sealed `manifest.yaml` `integrity.pack_digest`.

### Notes
- Several decision and pattern files still exceed the 6,000-character advisory size warning; they are long-form decision/pattern atoms and were not split in this pass.

