---
id: blender-3d/concepts/core-architecture-collections-scenes
title: "Core Architecture — Collections, Scenes, and View Layers"
type: concept
tags:
  - architecture
  - collections
  - scenes
  - view-layers
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/core-architecture.md
related:
  - core-architecture-data-blocks.md
  - core-architecture-modes-editors.md
content_hash: sha256:46183c6775485bd9629e807ffa5ed1ddcd5907727df40866f1fa395f25e3eece
---

# Core Architecture — Collections, Scenes, and View Layers

Collections group objects for visibility, selection, and instancing; an object can belong to more than one collection. Scenes are top-level containers with their own camera, world, and render settings; View Layers split a scene's render into isolated passes.

## Collections

Collections are Blender's organizational hierarchy — more powerful than traditional layers.

**Key properties:**
- Objects can belong to multiple collections simultaneously
- Collections nest inside each other
- Each collection has its own viewport/render visibility toggles
- Collections can have an offset (for instancing)

**Viewport visibility toggles** (enable in Outliner header with filter icon):
- Eye icon: viewport visibility (doesn't affect render)
- Camera icon: render visibility
- Select icon: whether objects in the collection can be selected
- Disable in Viewport: hides entirely (performance)

**Collection Instances:** `Add → Collection Instance` creates an instance of an entire collection as a single object — Blender's equivalent of a "prefab." The instanced collection's objects appear in the viewport but are not directly selectable. Modifying the original collection updates all instances. Essential for repeated architectural elements, scatter workflows, and linked asset libraries.

---

## Scenes and View Layers

**Scenes** are top-level containers within a .blend file — each has its own objects, Camera, World settings, render settings, and View Layers.

Multiple Scenes are useful for:
- Separate render setups (preview vs final quality)
- Multi-camera setups
- The Compositor can combine output from multiple Scenes

**View Layers** subdivide a Scene's render into separate passes:
- Character on one View Layer, background on another → composite with separate shadow control
- Effects elements isolated for compositing control
- Each View Layer defines which Collections are visible (Layer Collections)

