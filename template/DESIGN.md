# Pack Design

Design decisions for this pack. This file is for the pack author (and future
maintainers) — it is not loaded into agent context. Record *why* the pack is
shaped the way it is so the next person (or the next you) doesn't relitigate
settled decisions.

## Purpose

One paragraph: what problem does this pack solve, and for whom? What can an agent
do with this pack loaded that it cannot do from its training weights alone?

## Audience

Who consumes this pack — end users of a product, practitioners of a process, or
agents impersonating a person? What do they already know, and what do they not?

## Scope

What this pack deliberately covers. List the major knowledge areas and the
content types they map to (`concepts/`, `workflows/`, `troubleshooting/`, `faq/`).

## Non-goals

What this pack deliberately does NOT cover, and why. Be explicit — scope creep is
the main way packs dilute their EK ratio. When an area is out of scope, say where
the agent should send the user instead.

## Key decisions

Record the decisions that shaped the structure. For each: the decision, the
alternatives considered, and the reason. Examples:

- **Retrieval strategy defaults** — which content is `standard` vs `atomic` and why.
- **Concept boundaries** — how you decided what earns its own atom vs a Related Term.
- **Freshness policy** — the `refresh_cycle` you chose and what makes content volatile.
- **Provenance sourcing** — where facts come from and how `verified_at` is maintained.

## Open questions

Anything unresolved that affects future hydration — gaps you know exist, areas
that need a subject-matter expert, decisions deferred to a later version.
