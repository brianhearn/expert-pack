---
id: blender-3d/concepts/geometry-nodes-fields
title: "Geometry Nodes — Fields"
type: concept
tags:
  - geometry-nodes
  - fields
  - procedural
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/geometry-nodes.md
related:
  - geometry-nodes-core.md
  - geometry-nodes-instances-attributes.md
content_hash: sha256:ff20b0aeac5b86f28bf73c17189e5280b64738477ed389520196f9ccb7f631a6
---

# Geometry Nodes — Fields

A field is a per-element recipe for computing a value, not a single constant. Connecting Position or Random Value passes that recipe so every vertex, face, or point evaluates independently — purple sockets accept fields.

## Fields: The Most Important Concept

**A field is NOT a single value. A field is a recipe for computing a value per element.**

When you connect a `Position` node to another node, you are not passing the position of some object. You are passing a *field* that says "evaluate to the position of whatever element is being processed."

Think of a field like a function `f(element)` rather than a constant value.

**Why this matters:**

`Random Value` node → you don't get one random number. You get a *field* that evaluates to a different random number for each element. Every vertex, face, or point gets its own random value.

`Position` node connected to `Set Position → Offset` → offsets each element by *its own* position (which scales everything outward from the origin).

**The mental model:**
- Most numeric values in Geometry Nodes are fields (per-element recipes)
- A constant value (like `0.5`) is a trivially constant field — same for every element
- A `Position` or `Index` or `Normal` field is different for each element

**Practical example:** `Distribute Points on Faces` — the `Density` input is a *field*. Connect a noise texture to make some areas denser. The noise is evaluated *per-face* during distribution.

**Where fields appear:** Look for the purple tint on socket inputs — those accept fields (per-element values). White/gray sockets typically require single values.

