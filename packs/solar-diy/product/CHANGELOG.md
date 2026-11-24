# Changelog

All notable changes to the Solar Technology Reference pack.

## [1.0.1] — 2026-11-24

### Added
- `applies_to: residential-solar@2026`.
- Reclassified `freshness.md` from `type: volatile` to `type: reference`. It is a review playbook (W-VOL-01), not a decaying market table; the 2026 specification sheets themselves still need a later data refresh.

### Changed
- Conformance pass for ExpertPack core 4.2 / product schema 4.1.
- `related:` links for previously orphaned FAQs, specifications, and troubleshooting atoms.
- Re-sealed `manifest.yaml` `integrity.pack_digest`.

### Notes
- Glossary, general FAQ, and 2026 specification sheets still exceed the 6,000-character advisory size warning; they were not split in this pass.
