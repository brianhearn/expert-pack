# Session Handoff — 2026-07-06 (final)

*Context for the next agent session. Plan file was NOT edited: `.cursor/plans/expertpack_top_5_improvements_bb28fa4e.plan.md`*

---

## Git state (after push)

| Item | Value |
|------|--------|
| **Commits (this workstream)** | `355257b` — enforcement + onboarding gates; follow-up — doc sync |
| **Branch** | `main` — pushed to `origin/main` |
| **Untracked (local only)** | `expert-pack.code-workspace` — IDE workspace; exclude from commits |
| **Working tree** | Clean |

---

## What was accomplished (two commits)

### 1. Top 5 implementation (`355257b`)

All plan todos complete. Phases: strict validation + CI, RFC-003 Reconstruct Mode, RFC-004 chunk sidecars, TAC v1, unified CLI + onboarding templates.

### 2. Documentation sync (follow-up commit)

Framework docs brought in line with implementation. Schema family remains **4.1** (additive extensions only — user declined 4.2 bump).

| Doc | What changed |
|-----|--------------|
| `schemas/core.md` | Sidecars, TAC, `--strict` gate, registry cross-refs, provenance table, footer 2026-07-06 |
| `schemas/schema-index.yaml` | frontmatter, chunk-sidecar, typed-answer registry entries |
| `ARCHITECTURE.md` | Tools tree, onboarding, RFC-003/004, TAC, ingest gate, evaluation |
| `AXIOMS.md` | Operational contracts (axioms 6 & 13) |
| `README.md` | Implementation status, axioms 11–13, regenerated schema table |
| `CHANGELOG.md` | `[Unreleased]` Top-5 + doc sync entries |
| `tools/update-schema-readme.py` | UTF-8 read/write; ORDER includes new registry specs |

Regenerate README schema table after future schema changes:

```powershell
python tools/update-schema-readme.py
```

---

## Key design decisions (carry forward)

1. **Schema 4.1, not 4.2** — Top 5 is additive (RFCs, registry, tooling). Strict mode enforces existing 4.1 fields; it is a gate, not a new authoring model.
2. **EP MCP is external** — Reconstruct Mode runtime and sidecar consumption live in [ep-mcp](https://github.com/brianhearn/ep-mcp). In-repo contracts + OpenClaw plugin are done; RFC checklists define MCP exit criteria.
3. **CI backlog ignore** — Demo packs use `--ignore W-V41-01` for oversized standard concepts. Template job uses `--strict` only (not `--fail-on-warn`).
4. **Do not edit the plan file** — user instruction throughout session.
5. **Broken wikilink fix** — consolidated into `ep-doctor --fix links` (never shipped standalone script).

---

## Verification commands (Windows)

```powershell
python tools/validate-all.py --ignore W-V41-01
python tools/validator/ep-validate.py template --strict
python tools/chunker/ep-chunk-annotate.py packs/blender-3d --check --embedding-version gemini-embedding-001
python tools/tac/validate_tac.py tools/tac/example-tac.json
python tools/eval-runner/claim_verifier.py --tac tools/tac/example-tac.json
python tools/cli/expertpack.py init my-pack --type product --output $env:TEMP\ep-test
```

All passed before implementation commit.

---

## External repo dependencies (ep-mcp)

1. **RFC-003:** `/search?reconstruct=true`, span storage, hash verification, `stale` flag
2. **RFC-004:** chunker consumes `.chunks.yaml` for deterministic re-assembly

Do not mark end-to-end exit criteria done until EP MCP ships.

---

## Known backlog (non-blocking)

- **W-V41-01:** oversized `standard` concept files in demo packs
- **pip install -e .:** needs modern pip/setuptools/wheel on Windows dev box; direct `python tools/cli/expertpack.py` works
- **Plan file todos:** still show `pending` in YAML — work is complete; plan intentionally not edited

---

## Likely next-session work

- EP MCP integration against RFC-003/004 checklists
- Trim demo-pack oversized concepts to drop `W-V41-01` ignore
- Release tagging / changelog `[Unreleased]` → versioned section when ready
- Core **4.2** only if user explicitly requests a schema bump

---

## Key file index

```
.github/workflows/validate.yml
.pre-commit-config.yaml
tools/validate-all.py
tools/ingest-gate.py
tools/validator/ep-validate.py
tools/validator/ep-doctor.py
tools/chunker/ep-chunk-annotate.py
tools/cli/expertpack.py
tools/tac/validate_tac.py
tools/eval-runner/claim_verifier.py
schemas/core.md
schemas/schema-index.yaml
schemas/rfcs/RFC-003-*.md
schemas/rfcs/RFC-004-*.md
schemas/registry/frontmatter.*
schemas/registry/chunk-sidecar.spec.yaml
schemas/registry/typed-answer.*
templates/TAC-PROMPT.md
template/DESIGN.md
template/TOOLS.md
ARCHITECTURE.md
AXIOMS.md
README.md
CHANGELOG.md
ROADMAP.md
```

---

*End handoff.*
