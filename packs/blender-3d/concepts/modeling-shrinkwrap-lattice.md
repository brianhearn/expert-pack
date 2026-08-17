---
id: blender-3d/concepts/modeling-shrinkwrap-lattice
title: "Modeling — Shrinkwrap, Lattice, and Decimate"
type: concept
tags:
  - modeling
  - modifiers
  - shrinkwrap
  - lattice
  - decimate
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/modeling-fundamentals.md
related:
  - modeling-key-modifiers.md
  - modeling-modifier-stack.md
  - modeling-retopology.md
content_hash: sha256:3cf97963b86e830cabcd06f128c28a71034d2eab8cba939ebfddccb37048db7c
---

# Modeling — Shrinkwrap, Lattice, and Decimate

Shrinkwrap and Lattice deform a mesh toward another object or a cage; Decimate reduces density. These modifiers sit beside the core stack (Mirror, Boolean, Subdivision Surface) when you fit armor, reshape a model, or prepare a bake mesh.

## Shrinkwrap

Snaps a mesh's vertices onto the surface of another object. Three modes: Nearest Surface Point, Project, Nearest Vertex.
Essential for: cloth/armor fitting over a body, conforming retopo to a sculpt, layering decals onto curved surfaces.

## Lattice

A deformation cage for another object. Add a Lattice object, size it to encompass your target, add a Lattice modifier to the target pointing to the Lattice. Edit the Lattice's control points to deform the target smoothly.

## Decimate

- **Collapse:** Merges vertices by shortest edge. Ratio controls target percentage.
- **Planar:** Merges coplanar faces. Best for architectural/CAD imports with tons of unnecessary coplanar tris.
- **Preserve Seams/Sharp/Boundaries:** Prevents decimation from crossing UV seams and sharp edges. Enable for game-ready bake meshes.
