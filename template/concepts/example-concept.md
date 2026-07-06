---
id: your-pack-slug/concepts/example-concept
title: "Example Concept"
type: concept
tags: [example-concept, your-domain]
pack: your-pack-slug
retrieval_strategy: standard
schema_version: "4.1"
verified_at: "2026-07-06"
verified_by: agent
requires:
  # - prerequisite-concept.md   # declare only when this atom is unintelligible without another
related:
  - example-workflow.md
content_hash: sha256:d16c439165dcb9e44b3aa9a577cad68bb58ab18ec019b497b6fb9e742a80a47c
---

# Example Concept

An example concept is a self-contained unit of knowledge in an ExpertPack — it carries its definition, body, FAQs, and related terms in a single retrieval-ready file. This opening paragraph IS the summary: retriever-anchored, reader-useful, no throat-clearing. Write it to answer the most likely query about this concept directly.

## How It Works

Explain the concept clearly. Assume the reader knows the domain but not the specifics. Target 500–800 tokens for the whole file; hard ceiling 1,000 (schema v4.1). Use `##` section headers at natural topic breaks.

## Why It Matters

What does understanding this concept unlock? What mistakes does it prevent? This is often where esoteric knowledge (EK) lives — the things a general-purpose LLM gets wrong without the pack.

## Frequently Asked

### How is this concept different from [sibling-concept]?
Phrase questions the way users actually ask them. Each H3 becomes its own sub-chunk with a strong natural-language match surface.

### When should I use this concept vs. [alternative]?
Keep answers tight and directly applicable. FAQ answers should not re-explain the whole concept — assume the reader has the opening paragraph.

## Related Terms

- **Relative term 1:** Definition that only makes sense in context of this concept. If a term has its own definition, properties, and relationships, it earns its own atom instead — don't embed it here.
- **Relative term 2:** Short, concrete, 1–2 sentences.

## Related Concepts

- [[example-workflow]]
