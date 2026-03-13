# ExpertPack Framework — TODO

## Guides

- [x] **Hydration guide** (`guides/hydration.md`) — DONE (2026-03-13). Complete hydration lifecycle: planning → population (8 methods) → EK triage → retrieval layer building (schema-aware chunking, summaries, propositions, lead summaries, glossary) → validation → maintenance. Replaces and subsumes `population-methods.md`.

- [x] **Consumption guide** (`guides/consumption.md`) — DONE (2026-03-13). Platform integration, chunking strategy, RAG configuration, context tier loading, model selection, agent training (SOUL.md), eval-driven improvement loop. Grounded in 6 real experiments on EZT Designer help bot.

- [ ] **Research: optimal models for pack consumption** — Survey OpenRouter models suited for agent-style pack consumption. Goals: fast, inexpensive, good at structured document reasoning and instruction-following. Opus 4.6 is overkill for a deployed consumer agent. Evaluate candidates on: cost/token, speed, context window, instruction adherence, structured output quality. Consider separate recommendations for different consumption patterns (simple Q&A vs. multi-step troubleshooting vs. workflow guidance). *Note: consumption.md now includes model selection guidance based on our EZT experiments. This TODO is for a more comprehensive survey.*

## Population

- [x] **Population methods guide** — DONE (2026-02-28). Consolidated into `guides/hydration.md` (2026-03-13). Original `population-methods.md` archived.
