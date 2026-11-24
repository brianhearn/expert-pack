# Changelog

All notable changes to the Home Assistant Smart Home Guide composite ExpertPack.

## [2.0.1] — 2026-11-24

### Added
- Pack CHANGELOG for release tracking.
- Provenance `id` / `verified_at` on the composite `overview.md`.

### Changed
- Conformance pass for ExpertPack core 4.2, product/process schema 4.1, and composite schema 1.2 (spec `da51888`).
- Constituent packs bumped in lockstep: product 2.0.0 → 2.0.1, process 1.0.0 → 1.0.1.
- Eval benchmark upgraded to the v4.1 field set (`pack_slug`, `pack_version`, `expected_answer`) so `run_eval.py --dry-run` succeeds.
- Re-sealed composite and constituent `integrity.pack_digest` values after the edits.

### Notes
- `integrity_status` remains `unsigned` until a pack signature is added; digests are sealed and should report `digest_verified=true`.
