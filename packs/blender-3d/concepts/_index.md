---
title: Concepts
type: index
tags:
- concepts
pack: blender-3d
retrieval_strategy: navigation
id: blender-3d/concepts/_index
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
---

# Concepts

Core knowledge concepts for Blender — the underlying principles and mental models required to work effectively with the software.

## Core Architecture
- `core-architecture-data-blocks.md` — Data-blocks, objects, and object data
- `core-architecture-collections-scenes.md` — Collections, scenes, and view layers
- `core-architecture-blend-file.md` — The .blend file format, linking, appending, and asset management
- `core-architecture-modes-editors.md` — Mode system and primary editors
- `core-architecture-workspaces.md` — Workspace layouts

## Modeling
- `modeling-topology.md` — Topology theory and Edit Mode tools
- `modeling-retopology.md` — Retopology and common modeling mistakes
- `modeling-modifier-stack.md` — Modifier order and hard-surface vs organic
- `modeling-key-modifiers.md` — Subdivision Surface, Mirror, Boolean, Solidify, Array, Bevel
- `modeling-shrinkwrap-lattice.md` — Shrinkwrap, Lattice, and Decimate

## Shading & Rendering
- `shading-eevee.md` — EEVEE vs Cycles decision and EEVEE Next
- `shading-cycles.md` — Cycles GPU backends and performance
- `shading-render-settings.md` — Film/output settings and common render mistakes
- `shading-principled-bsdf.md` — Principled BSDF and PBR texture setup
- `shading-procedural-textures.md` — Noise, Voronoi, Wave, Color Ramp, Math
- `shading-uv-maps.md` — UV unwrapping, normal maps, and displacement
- `shading-hdri-lighting.md` — World HDRI lighting setup

## Animation
- `animation-data-model.md` — F-curves, actions, and keyframing
- `animation-graph-editors.md` — Dope Sheet, Graph Editor, and 4.x changes
- `animation-nla.md` — NLA editor and action strips
- `animation-drivers.md` — Drivers and expression-based animation
- `animation-shape-keys.md` — Shape keys, relative vs absolute, and facial rigging
- `rigging-armatures.md` — Armatures and constraints
- `rigging-ik-weights.md` — IK vs FK, weight painting, and vertex groups

## Geometry Nodes
- `geometry-nodes-core.md` — What they are, the functional paradigm, and data types
- `geometry-nodes-fields.md` — Fields as per-element recipes
- `geometry-nodes-flow-creation.md` — Flow control, creation, and modification nodes
- `geometry-nodes-instances-attributes.md` — Instances, attributes, realize, and transforms
- `geometry-nodes-scatter-deform.md` — Scatter and curve-deform patterns
- `geometry-nodes-parametric.md` — Parametric shapes and procedural variation
- `geometry-nodes-advanced-patterns.md` — Verlet, attribute transfer, tool choice, and bugs
- `geometry-nodes-simulation.md` — Simulation Zone (Blender 4.0+) temporal simulations

## Sculpting
- `sculpting-dyntopo.md` — Dynamic topology
- `sculpting-multires-remesh.md` — Multires, remesh, and typical head workflow
- `sculpting-brushes.md` — Viewport shading and core brushes
- `sculpting-masking-facesets.md` — Face sets, masking, filters, and performance

## Compositing
- `compositing-core.md` — Compositor vs viewport, render layers, and denoising
- `compositing-passes-exr.md` — Render passes, OpenEXR multilayer, and GPU compositing
- `compositing-color-grading.md` — Color management, AgX, and color grading
- `compositing-effects.md` — Glare, depth of field, and common effects nodes

## Physics
- `physics-rigid-body.md` — Rigid body simulation
- `physics-soft-cloth.md` — Soft body, cloth, and bake practice
- `physics-mantaflow.md` — Mantaflow fluids, smoke, and fire
- `physics-particles.md` — Particle systems, hair, and force fields

## Python Scripting
- `python-bpy-data.md` — bpy module structure and bpy.data
- `python-bpy-context.md` — bpy.context and temp_override
- `python-bpy-ops.md` — bpy.ops, scripting gotchas, and the Info Log
- `python-addon-structure.md` — Add-on structure and application handlers
- `python-custom-ui.md` — Custom operators and panels
- `python-batch-scripting.md` — Batch rename, export, and frame iteration
- `python-cli-render.md` — Headless command-line rendering
- `python-depsgraph.md` — Depsgraph and evaluated data

## Video Editing
- `video-editing-vse-interface.md` — VSE interface and strip types
- `video-editing-vse-editing.md` — Strips, proxies, speed, and text
- `video-editing-render.md` — Rendering and audio
- `video-editing-vs-external.md` — Metadata stamps and VSE vs external editors
