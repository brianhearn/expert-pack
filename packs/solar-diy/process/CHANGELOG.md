# Changelog

All notable changes to the Residential Solar Installation Process pack.

## [1.0.1] — 2026-11-24

### Added
- `applies_to: residential-solar@2026`.
- Phase-chain and decision `related:` links so process atoms are no longer orphaned.

### Changed
- Conformance pass for ExpertPack core 4.2 / process schema 4.1.
- Re-sealed `manifest.yaml` `integrity.pack_digest`.

### Notes
- Three decision files still exceed the 6,000-character advisory size warning; they are long-form decision atoms and were not split in this pass.
