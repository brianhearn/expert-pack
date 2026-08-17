---
id: blender-3d/concepts/geometry-nodes-flow-creation
title: "Geometry Nodes — Flow Control, Creation, and Modification"
type: concept
tags:
  - geometry-nodes
  - nodes
pack: blender-3d
retrieval_strategy: standard
concept_scope: single
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
supersedes:
  - concepts/geometry-nodes.md
related:
  - geometry-nodes-instances-attributes.md
  - geometry-nodes-core.md
content_hash: sha256:c103cbb26bf82f1f0e9004e841d404af24b3637e43ec6f9e862b1adba6cab9ce
---

# Geometry Nodes — Flow Control, Creation, and Modification

Geometry Nodes graphs start at Group Input, create or modify geometry, and end at Group Output. Flow-control, primitive-creation, and mesh-modification nodes are the backbone before instancing and attributes.

## Flow Control

| Node | Purpose |
|------|---------|
| Group Input | Inputs to your node group (exposed as modifier parameters) |
| Group Output | Final geometry output |
| Join Geometry | Combines multiple geometry streams into one |

---

## Creation

| Node | Purpose |
|------|---------|
| Mesh Primitives (Cube, Cylinder, etc.) | Create basic mesh shapes procedurally |
| Mesh Line | Create a line of vertices |
| Mesh Grid | Create a grid mesh |
| Curve Primitives | Create curves procedurally |
| Points | Create a point cloud |

---

## Modification

| Node | Purpose |
|------|---------|
| Set Position | Move geometry — the fundamental deformation node |
| Transform Geometry | Apply a full transform (location/rotation/scale) to geometry |
| Merge by Distance | Weld nearby vertices (equivalent to "Remove Doubles") |
| Subdivide Mesh | Subdivide within the node graph |
| Extrude Mesh | Extrude faces/edges/vertices |
| Flip Faces | Flip face normals |

---

