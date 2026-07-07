# Session Handoff — 2026-07-07

*Context for the next agent session. Top-5 implementation complete in-repo (2026-07-06); EP MCP runtime verified and doc-synced (2026-07-07). Plan file was NOT edited: `.cursor/plans/expertpack_top_5_improvements_bb28fa4e.plan.md`*

---

## Git state (after push)

| Item | Value |
|------|--------|
| **Top-5 commits** | `355257b` — enforcement + onboarding; `ede5d2c` — framework doc sync |
| **Doc sync commit** | (this session) — README/ROADMAP/CHANGELOG/RFC status reflect ep-mcp shipped |
| **Branch** | `main` — pushed to `origin/main` |
| **Untracked (local only)** | `expert-pack.code-workspace` — exclude from commits |
| **Deploy** | **Not done** — production MCP host not updated this session |

---

## End-to-end status (verified 2026-07-07)

| Layer | Repo | Status |
|-------|------|--------|
| Specs + tooling (RFC-003/004, TAC, strict gate, sidecars) | expert-pack | ✅ Complete |
| OpenClaw `reconstruct` consumer | expert-pack | ✅ Complete |
| EP MCP runtime (sidecar consumption + reconstruct envelope) | ep-mcp `a9d1639` | ✅ Complete |
| Production reindex + live smoke | — | ⏳ **Next session** |

RFC-003/004 exit criteria are **code-complete**. Remaining work is operational: deploy ep-mcp, reindex sidecar packs, smoke `reconstruct=true` on expertpack.ai/mcp.

---

## What was accomplished (2026-07-06 — two commits)

### 1. Top 5 implementation (`355257b`)

Strict validation + CI, RFC-003 Reconstruct Mode spec, RFC-004 chunk sidecars, TAC v1, unified CLI + onboarding templates. All plan todos complete.

### 2. Documentation sync (`ede5d2c`)

`ARCHITECTURE.md`, `AXIOMS.md`, `README.md`, `schemas/core.md`, `schemas/schema-index.yaml`, `CHANGELOG.md`. Schema family remains **4.1** (additive only).

---

## What was accomplished (2026-07-07 — verification + doc sync)

Verified ep-mcp `a9d1639` against RFC-003/004 checklists (tests pass, blender-3d sidecar smoke OK). Updated framework docs that still said "EP MCP external":

| Doc | Change |
|-----|--------|
| `README.md` | Implementation status: RFC-003/004 → ✅ Full |
| `ROADMAP.md` | Top-5 bullets reference ep-mcp `a9d1639` |
| `CHANGELOG.md` | EP MCP runtime alignment entry |
| `schemas/rfcs/RFC-003-*.md` | Status shipped; checklist notes reindex step |
| `schemas/rfcs/RFC-004-*.md` | Status shipped |
| ep-mcp `ARCHITECTURE.md` §5.9 | RFC-003 field list (cross-repo doc sync) |

**FastMCP:** `mcp` **1.28.1** is latest PyPI; ep-mcp uses `from mcp.server.fastmcp import FastMCP`.

---

## Key design decisions (carry forward)

1. **Schema 4.1, not 4.2** — Top 5 is additive. Strict mode is a gate, not a new authoring model.
2. **EP MCP runtime shipped** — [ep-mcp](https://github.com/brianhearn/ep-mcp) `a9d1639` (2026-07-06). Reindex required for accurate `fragment_id`.
3. **CI backlog ignore** — Demo packs use `--ignore W-V41-01` for oversized standard concepts.
4. **Do not edit the plan file** — user instruction; todos in YAML still show `pending`.
5. **Do not deploy without explicit user request** — deferred 2026-07-07.

---

## Verification commands (Windows)

```powershell
cd C:\Users\BrianHearn\source\repos\expert-pack
python tools/validate-all.py --ignore W-V41-01
python tools/validator/ep-validate.py template --strict
python tools/chunker/ep-chunk-annotate.py packs/blender-3d --check --embedding-version gemini-embedding-001
python tools/tac/validate_tac.py tools/tac/example-tac.json

cd C:\Users\BrianHearn\source\repos\ep-mcp
py -3.12 -m pytest tests/unit/test_sidecar.py tests/unit/test_reconstruct.py -v
```

---

## External repo (ep-mcp) — shipped

1. **RFC-003:** reconstruct envelope, span storage, `stale` — ✅ `a9d1639`
2. **RFC-004:** `.chunks.yaml` consumption at index time — ✅ `a9d1639`

**Production exit criteria (not done):** deploy → reindex sidecar packs → smoke `reconstruct=true` on live host.

---

## Known backlog (non-blocking)

- **W-V41-01:** oversized `standard` concept files in demo packs
- **Windows loader path keys** (ep-mcp): 8 unit test failures on Windows; pre-existing
- **Plan file todos:** still `pending` in YAML — work complete; plan intentionally not edited
- **pip install -e .** on Windows may need modern pip/setuptools; `python tools/cli/expertpack.py` works directly

---

## Likely next-session work

1. Deploy ep-mcp + reindex + live reconstruct smoke (user deferred)
2. Trim demo-pack oversized concepts to drop `W-V41-01` ignore
3. Version tag + `[Unreleased]` → versioned CHANGELOG (both repos)
4. Core **4.2** only if user explicitly requests schema bump

---

## Key file index

```
.github/workflows/validate.yml
tools/validate-all.py
tools/ingest-gate.py
tools/validator/ep-validate.py
tools/chunker/ep-chunk-annotate.py
tools/cli/expertpack.py
tools/tac/validate_tac.py
schemas/core.md
schemas/rfcs/RFC-003-*.md
schemas/rfcs/RFC-004-*.md
schemas/registry/chunk-sidecar.spec.yaml
schemas/registry/typed-answer.*
ARCHITECTURE.md
README.md
ROADMAP.md
CHANGELOG.md
```

---

## Related repos

| Repo | Path | Role |
|------|------|------|
| expert-pack | `C:\Users\BrianHearn\source\repos\expert-pack` | Authoring framework, specs, validation, sidecar tooling |
| ep-mcp | `C:\Users\BrianHearn\source\repos\ep-mcp` | MCP runtime — hybrid retrieval, sidecars, reconstruct |

---

*End handoff.*
