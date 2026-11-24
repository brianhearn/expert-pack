---
title: "Changelog"
type: meta
tags:
- changelog
- meta
pack: solar-diy
retrieval_strategy: navigation
id: solar-diy/meta/changelog
schema_version: "4.1"
verified_at: "2026-11-24"
verified_by: agent
content_hash: sha256:a6c6a5047711568831f6388801c0e1c287fcf1f5127d8ce15167c318d37ce760
---

# Changelog

All notable changes to the Residential Solar & Battery DIY Guide composite ExpertPack.

## [2.0.1] — 2026-11-24

### Added
- Pack content changelog at `meta/changelog.md`.
- Provenance `id` / `verified_at` on the composite `overview.md`.

### Changed
- Conformance pass for ExpertPack core 4.3 (tag `core-4.3`, `cd27fa6`), product/process schema 4.1, and composite schema 1.2.
- Constituent packs bumped in lockstep: product 1.0.0 → 1.0.1, process 1.0.0 → 1.0.1.
- Composite eval set uses eval schema `version: "1.0"` (no `pack_type: composite`). Most questions are now in-scope, including a `fail_closed` conflict case; constituents have their own `pack_type: product` / `process` suites.
- Re-sealed composite and constituent `integrity.pack_digest` values after the edits.

### Notes
- `integrity_status` remains `unsigned` until a pack signature is added; digests are sealed and should report `digest_verified=true`.

