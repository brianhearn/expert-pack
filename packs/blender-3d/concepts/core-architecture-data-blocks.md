---
id: blender-3d/concepts/core-architecture-data-blocks
title: "Core Architecture — Data-Blocks and Object Data"
type: concept
tags:
  - architecture
  - data-blocks
  - objects
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/core-architecture.md
related:
  - core-architecture-collections-scenes.md
  - core-architecture-blend-file.md
  - core-architecture-modes-editors.md
content_hash: sha256:b6ce41591085c11af72cacc8dd7dad1751f2d88cb905402f3fcf1395458cd3d8
---

# Core Architecture — Data-Blocks and Object Data

Understanding Blender's internal data model is the single most important piece of knowledge for becoming a proficient Blender user. Everything — the behavior of linked duplicates, why deleting an object doesn't delete its mesh, how instancing works — stems from this architecture.

## The Data-Block System

Everything in Blender is a **data-block** — a named, reference-counted container for a specific type of data.

| Data-Block Type | What It Stores |
|----------------|----------------|
| `Object` | Transform (location/rotation/scale), constraints, modifiers |
| `Mesh` | Vertices, edges, faces, UVs, vertex groups |
| `Material` | Shader node tree, surface/volume/displacement settings |
| `Image` | Pixel data (packed or external reference) |
| `Armature` | Bone hierarchy and rest positions |
| `Action` | Keyframe data for an animatable thing |
| `NodeTree` | A node group (shader, geometry nodes, compositor) |
| `Scene` | Everything in a scene (lights, camera, settings) |
| `Collection` | A group of objects |

**Reference counting:** Each data-block has a user count. When you "delete" an object, you decrement its user count. If it reaches zero, the data-block is orphaned — purged on save/reload. This is why you can lose work: delete an object and the mesh disappears on save if nothing else references it.

**Fake User:** The `F` button next to any data-block's name sets a fake user — an artificial +1 to the user count. Use it on materials, node groups, and textures you want to keep even if nothing currently uses them.

**Linked vs copied duplicates:**
- `Shift+D`: New object gets a *copy* of the object data (independent mesh)
- `Alt+D`: Both objects share the *same* mesh data-block. Edit the mesh of one → both update.

---

## Object vs Object Data

This distinction trips up almost everyone initially.

**Object** = scene entity with: Location, Rotation, Scale, Constraints, Modifiers, and a **reference to Object Data**.

**Object Data** = the actual content:
- For a Mesh object: a Mesh data-block (vertices, edges, faces)
- For an Armature: an Armature data-block (bones)
- For a Light: a Light data-block (type, color, intensity)

Multiple Objects can reference the same Object Data. This is efficient instancing — 1000 objects can all point to the same mesh, with each object having its own transform, but the mesh data stored only once.

**Edit Mode operates on Object Data.** When you `Tab` into Edit Mode, you are editing the shared mesh data-block. If two objects share the same mesh (via `Alt+D`) and you edit it, *both objects update*.

To make Object Data independent: in the header where the mesh name is shown, click the number next to the name (the user count) — this "makes single user" and creates a copy.

---

