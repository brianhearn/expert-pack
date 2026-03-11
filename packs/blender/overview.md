# Blender 3D Creation Suite — ExpertPack

> **Lead summary:** Blender is a free and open-source 3D creation suite that covers the *entire* 3D pipeline in a single application: modeling, sculpting, rigging, animation, simulation, rendering (Cycles and EEVEE), compositing, motion tracking, video editing, and the powerful procedural Geometry Nodes system. This ExpertPack focuses on practitioner-level knowledge — decision frameworks, workflow patterns, keyboard shortcuts, and the tribal wisdom that takes years to accumulate. It complements the official manual rather than restating it.

## What Makes Blender Unique

Blender is not just a 3D modeler with a renderer bolted on. It is one of the most comprehensive creative tools ever built, and entirely free. The scope is staggering:

- **Modeling:** Polygon mesh modeling, NURBS curves and surfaces, metaballs
- **Sculpting:** Dynamic topology (Dyntopo), multi-resolution, virtual sculpting brushes
- **Shading:** Node-based PBR materials, procedural texturing, Shader Editor
- **Rendering:** EEVEE (real-time rasterization) and Cycles (path tracing), plus Workbench for viewport display
- **Animation:** Keyframing, armature-based rigging, shape keys, constraints, drivers, NLA editor
- **Simulation:** Fluid, smoke/fire, cloth, soft body, rigid body, particles
- **Geometry Nodes:** Fully procedural, node-based geometry creation and modification
- **Compositing:** Node-based post-processing, render passes, color grading
- **Video Editing:** Built-in VSE (Video Sequence Editor) for non-linear editing
- **Grease Pencil:** 2D animation drawn in 3D space — unique to Blender
- **Scripting:** Python API (bpy) exposes nearly everything — fully extensible

Current production version is **Blender 5.0** (2026), with **Blender 4.2 LTS** as the long-term support release for studios requiring stability.

## What This Pack Covers

This is not a beginner tutorial. It is the reference guide that answers the questions you hit *after* you know the basics — the second-order knowledge:

- **Why** topology matters (not just what it is)
- **When** to use EEVEE vs Cycles — the actual decision criteria
- **How** Blender's data model works (data-blocks, linking, instancing) — the mental model most users never fully grasp
- **What** the Geometry Nodes field/attribute paradigm means in practice
- **Which** modifier order matters and why it breaks things when wrong
- **How** to avoid the dozen most common mistakes that plague intermediate users

## Who It's For

- **Intermediate Blender users** who know the basics but hit walls on "why doesn't this work?"
- **Developers and technical artists** who need to understand the data model for scripting or pipeline work
- **Artists from other software** (Maya, Cinema 4D, 3ds Max) making the transition
- **Hobbyists** who want to accelerate past the "watched 50 hours of tutorials but still confused" phase
- **Professionals** using Blender in production pipelines who need reference knowledge on demand

## How to Use This Pack

Start with **Core Architecture** (`concepts/core-architecture.md`) to build the mental model — Blender's data-block system and object hierarchy explains why things behave the way they do. Then:

- For material/rendering questions → `concepts/shading-rendering.md`
- For modeling topology questions → `concepts/modeling-fundamentals.md`
- For procedural/GeoNodes questions → `concepts/geometry-nodes.md`
- For common errors and confusing behaviors → `troubleshooting/common-mistakes.md`
- For hard surface modeling workflows → `workflows/hard-surface-modeling.md`

## The Philosophy of This Pack

The official Blender manual at `docs.blender.org` is comprehensive but descriptive — it tells you *what* each button does. This pack tells you *why* things work the way they do and *when* to use each approach. The best Blender knowledge lives in YouTube comments, Blender Artists forum threads from 2018, and the brains of senior technical artists. This pack distills that knowledge into a form an AI agent can use to help you make better decisions.

## Key Versions Reference

| Version | Status | Notes |
|---------|--------|-------|
| 5.0 | Current | Major release, EEVEE improvements, GeoNodes expansion |
| 4.2 LTS | Long-Term Support | Studio production workhorse, patches until ~2026 |
| 4.0–4.1 | Superseded | EEVEE Next introduced in 4.2 |
| 3.6 LTS | Legacy LTS | Many tutorials still reference this |
