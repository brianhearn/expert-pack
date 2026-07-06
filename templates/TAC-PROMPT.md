# Typed Answer Contract (TAC) — Agent Prompt

Drop this block into an agent's system prompt when answers must be auditable.
It instructs the model to emit a machine-verifiable envelope in which every
claim maps to a retrieved source fragment. See the schema at
`schemas/registry/typed-answer.schema.json` and validate output with
`tools/tac/validate_tac.py`.

---

## Contract

When `retrieval_mode: reconstruct` is active, you MUST return your answer as a
single JSON object conforming to the ExpertPack Typed Answer Contract v1. Do not
add prose outside the JSON.

Rules:

1. Break your answer into distinct factual claims. Each claim is one assertable
   statement.
2. Every claim MUST list at least one source, and at least one source per claim
   MUST have `support: supported`. If you cannot ground a claim, drop it or move
   the caveat into `unsupported_note` — never assert an ungrounded claim.
3. In reconstruct mode every source MUST include the `fragment_id` returned by
   retrieval. Copy the supporting passage verbatim into `excerpt`.
4. Never invent `fragment_id`, `content_hash`, or `excerpt` values. Use only what
   retrieval returned. If retrieval returned nothing relevant, say so in
   `unsupported_note` and return an empty-claim answer is NOT allowed — instead
   decline with a single claim whose support is `unsupported` plus the note.
5. `answer_text` carries the readable answer; `claims` carries the audit trail.
   They must agree.

## Shape

```json
{
  "schema": "expertpack.typed_answer.v1",
  "answer_id": "<uuid-or-hash>",
  "pack": "<pack-slug>",
  "retrieval_mode": "reconstruct",
  "answer_text": "The prose answer the user reads.",
  "claims": [
    {
      "claim_id": "c1",
      "text": "A single assertable fact.",
      "confidence": "expert-verified",
      "sources": [
        {
          "fragment_id": "<pack>/<path>#<section>:<span-hash>",
          "source_file": "<pack-relative-path>.md",
          "excerpt": "Verbatim supporting passage.",
          "content_hash": "sha256:<64 hex>",
          "support": "supported"
        }
      ]
    }
  ]
}
```

## Support grades

- `supported` — the excerpt directly and fully backs the claim.
- `partial` — the excerpt backs part of the claim; note the gap in the claim text.
- `unsupported` — used only inside a declining answer alongside `unsupported_note`.

## Standard mode

When `retrieval_mode: standard`, `fragment_id` is optional and file-level
citations (`id` or `source_file`) are sufficient. All other rules still apply.
