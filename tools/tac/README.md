# TAC — Typed Answer Contract tooling

The Typed Answer Contract (TAC) is a machine-verifiable response envelope: every
claim an agent makes maps to one or more retrieved source fragments, each graded
`supported`, `partial`, or `unsupported`. TAC is the response layer that sits on
top of the Fragment Provenance retrieval layer ([RFC-003](../../schemas/rfcs/RFC-003-fragment-provenance-reconstruct-mode.md)).

- Spec: [`schemas/registry/typed-answer.spec.yaml`](../../schemas/registry/typed-answer.spec.yaml)
- JSON Schema (draft 2020-12): [`schemas/registry/typed-answer.schema.json`](../../schemas/registry/typed-answer.schema.json)
- Agent prompt contract: [`templates/TAC-PROMPT.md`](../../templates/TAC-PROMPT.md)
- TypeScript types: [`tools/openclaw-memory-plugin/src/tac-types.ts`](../openclaw-memory-plugin/src/tac-types.ts)

## validate_tac.py

Validates a TAC JSON envelope against the schema plus the semantic rules a plain
JSON Schema cannot express (every claim grounded, `reconstruct` requires
`fragment_id`, well-formed `content_hash`). Uses `jsonschema` for full 2020-12
validation when installed; otherwise the built-in structural checks run alone.

```bash
python tools/tac/validate_tac.py answer.json           # human-readable
python tools/tac/validate_tac.py answer.json --json     # JSON report
type answer.json | python tools/tac/validate_tac.py -   # stdin (Windows)
```

Exit code is non-zero on any contract violation, so it can gate CI.

## Eval scoring

`claim_verifier.py` scores a TAC envelope: structural validity, self-declared
coverage, and (with `--pack` + `OPENROUTER_API_KEY`) an independent LLM check
that re-grounds each claim against the pack.

```bash
python tools/eval-runner/claim_verifier.py --tac answer.json
python tools/eval-runner/claim_verifier.py --tac answer.json --pack packs/blender-3d
```

`example-tac.json` is a minimal valid envelope for reference and smoke tests.
