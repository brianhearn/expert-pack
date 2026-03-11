# Blender Knowledge Sources — Coverage Map

Source discovery document for the Blender ExpertPack. Lists all major knowledge sources, their content type, quality, and coverage gaps.

---

## Official Documentation

### Blender Manual
- **URL:** https://docs.blender.org/manual/en/latest/
- **Type:** Comprehensive reference manual
- **Coverage:** All features, every tool, every operator
- **Quality:** High accuracy, authoritative, maintained by Blender Foundation
- **Gaps:** Descriptive not prescriptive — tells you what each button does, not *when* or *why* to use it. Limited workflow guidance. Minimal "gotcha" documentation.
- **Use for:** Confirming exact parameter names, understanding what a feature does, checking version-specific changes
- **Notable:** The manual has a "Scripting" section that documents the Python API integration at a conceptual level; the actual API reference is separate

### Blender Python API Reference
- **URL:** https://docs.blender.org/api/current/
- **Type:** API reference (auto-generated from source)
- **Coverage:** Every Python-accessible class, method, and property in bpy
- **Quality:** Complete but terse — minimal examples, often requires cross-referencing with manual
- **Gaps:** No workflow guidance, context requirements often undocumented (many operators require specific mode or selection state)
- **Use for:** Scripting, add-on development, automation

### developer.blender.org
- **URL:** https://developer.blender.org
- **Type:** Developer hub (task tracker, design docs, module notes)
- **Coverage:** Architecture decisions, bug reports, feature proposals, module team discussions
- **Quality:** Variable — design docs are excellent, bug reports range from detailed to cryptic
- **Gaps:** Not user-facing; requires understanding Blender's internal architecture to be useful
- **Use for:** Understanding *why* something works (or doesn't) a certain way; tracking known issues; understanding upcoming changes

### Blender Release Notes
- **URL:** https://wiki.blender.org/wiki/Reference/Release_Notes
- **Type:** Version changelogs
- **Coverage:** New features, removed features, API changes, workflow improvements
- **Quality:** High — written by module owners
- **Use for:** Understanding what changed between versions; identifying if a tutorial is outdated

---

## Community Forums

### Blender Artists Forum
- **URL:** https://blenderartists.org
- **Type:** Community forum (long-form discussion, WIP threads, support)
- **Coverage:** Everything — years of accumulated community wisdom
- **Quality:** Variable, but the old threads (2015–2022) often contain the best troubleshooting knowledge
- **Notable:** The "Resources" section has massive free asset/addon compilations. Support threads often contain workarounds for known bugs before official fixes landed.
- **Use for:** Esoteric problems, "how did you do X" questions, finding old workarounds

### Blender Stack Exchange
- **URL:** https://blender.stackexchange.com
- **Type:** Q&A site
- **Coverage:** Technical questions with structured answers
- **Quality:** High signal-to-noise — voted answers rise to top
- **Notable:** Excellent for Python scripting questions, modifier behavior questions, and mathematical rigging problems
- **Use for:** Technical "how to" questions with definitive answers

### r/blender (Reddit)
- **URL:** https://reddit.com/r/blender
- **Subscribers:** 1.5M+ (as of 2026)
- **Type:** Community feed — showcases, questions, news
- **Quality:** Highly variable; showcase posts are inspirational, help posts range from excellent to misleading
- **Notable:** r/blenderhelp is a separate subreddit specifically for support questions — higher quality answers than main sub
- **Use for:** Inspiration, community pulse, quick sanity checks; NOT for authoritative technical info

### r/blenderhelp
- **URL:** https://reddit.com/r/blenderhelp
- **Type:** Dedicated help subreddit
- **Quality:** Better than main r/blender for troubleshooting; answers usually include screenshots
- **Use for:** Visual troubleshooting questions

### CGSociety Forums
- **URL:** https://forums.cgsociety.org
- **Coverage:** General CG, including Blender; older threads have excellent fundamentals discussion
- **Quality:** High professional level, somewhat inactive in recent years
- **Use for:** Fundamentals that transcend specific software versions (topology, shading theory, compositing)

### Polycount Forum
- **URL:** https://polycount.com/forum
- **Coverage:** Game art pipeline, topology, UV mapping, baking; Blender sections growing rapidly
- **Quality:** High professional level, game-art focused
- **Use for:** Low-poly techniques, baking workflows, game-ready asset pipelines, topology critique methodology

---

## YouTube Channels (Ranked by Production Value / Depth)

### Blender Guru (Andrew Price)
- **URL:** https://youtube.com/@blenderguru
- **Specialty:** Beginner to intermediate, photorealism, architectural visualization
- **Notable content:** The Donut Tutorial (most-watched Blender tutorial series ever), Anvil series, Blender benchmark comparisons
- **Depth:** Medium — excellent for fundamentals, sometimes oversimplifies advanced topics
- **Best for:** Absolute beginners, photorealistic rendering techniques

### CG Cookie
- **URL:** https://youtube.com/@cgcookie / cgcookie.com (paid platform)
- **Specialty:** Structured courses, professional workflow, topology
- **Notable content:** Character creation, topology fundamentals (Kent Trammell), hard surface modeling
- **Depth:** High — one of the most thorough training platforms
- **Best for:** Systematic skill building, topology theory, character work

### Ducky 3D
- **URL:** https://youtube.com/@Ducky3D
- **Specialty:** Abstract motion design, procedural shading, satisfying loops
- **Notable content:** Geometry Nodes motion design, EEVEE material experiments, color palette tutorials
- **Depth:** Medium — workflow-focused, shows practical techniques
- **Best for:** Motion graphics, Geometry Nodes, procedural materials

### Default Cube
- **URL:** https://youtube.com/@DefaultCube
- **Specialty:** Geometry Nodes deep dives, procedural workflows, technical Blender
- **Notable content:** Geometry Nodes field explanations, attribute system deep dives
- **Depth:** High — genuinely deep technical content, not beginner-friendly
- **Best for:** Geometry Nodes mastery, procedural geometry understanding

### Ian Hubert
- **URL:** https://youtube.com/@IanHubert2
- **Specialty:** "Lazy Tutorials" — cinematic VFX on a budget, creative problem-solving
- **Notable content:** "Lazy Tutorials" 1-minute series (transformative for intermediate users), Dynamo Dream short film
- **Depth:** Unique — shows creative shortcuts, texture projection tricks, compositing for VFX
- **Best for:** Learning to work FAST, creative problem-solving, mixing photography with 3D, "good enough" philosophy

### Grant Abbitt
- **URL:** https://youtube.com/@GrantAbbitt
- **Specialty:** Game art, character design, stylized modeling, Blender for beginners
- **Notable content:** "Learn Sculpting" series, "Get Good at Blender" series, low-poly game character workflows
- **Depth:** Medium — very accessible, good fundamentals coverage
- **Best for:** Game art pipeline, stylized characters, beginners who want game-ready assets

### Curtis Holt
- **URL:** https://youtube.com/@curtisholt4865 / curtisholt.online
- **Specialty:** Python scripting, add-on development, Blender internals
- **Notable content:** Python API tutorials, custom node group walkthroughs
- **Depth:** High technical depth for scripting/development content
- **Best for:** Blender Python scripting, add-on development, automation

### Stylized Station (Phil Vaugn)
- **URL:** https://youtube.com/@StylizedStation
- **Specialty:** Stylized/NPR (non-photorealistic) rendering, hand-painted textures
- **Notable content:** Stylized character workflow series
- **Best for:** Anime-style, hand-painted, non-photorealistic workflows

### Royal Skies
- **URL:** https://youtube.com/@RoyalSkies
- **Specialty:** Animation, rigging, NLA editor, game export
- **Notable content:** Short, efficient tutorials on animation fundamentals
- **Best for:** Animation workflow, NLA editor, Rigify deep dives

---

## Blender Studio (Official Open Movies)

- **URL:** https://studio.blender.org
- **Type:** Production files, breakdown articles, open movie assets
- **Content:** Complete production files for Blender's open movies (Sintel, Tears of Steel, Agent 327, Cosmos Laundromat, Sprite Fright, Charge, etc.)
- **Quality:** Extremely high — created by professional Blender developers and artists
- **Notable:** The production blogs for each film are invaluable — they document the actual problems encountered and solutions found in real production
- **Use for:** Learning professional-grade node setups, rigging approaches, compositing pipelines; reference for "how would a professional do X"

---

## Books

### "Blender 4.x Shading and Lighting"
- Various publishers release updated Blender books; check publication year carefully
- Most Blender books go out of date quickly — prefer books covering fundamentals over UI-specific content

### "The Blender Python API" (Payne)
- Focused on scripting; holds up better than visual tutorial books since API concepts are more stable
- Supplements the official API docs with workflow context

### Digital content creation textbooks
- University-level 3D fundamentals books (not Blender-specific) often cover topology, UV mapping, and rendering theory better than any Blender resource — the fundamentals are software-agnostic

---

## Specialized Resources

### Poly Haven
- **URL:** https://polyhaven.com
- **Content:** Free HDRIs, textures (PBR), and 3D models under CC0 license
- **Relevance:** The go-to source for real-world lighting (HDRIs) and PBR texture maps; essential for photorealistic workflows

### BlenderKit
- **URL:** https://www.blenderkit.com
- **Content:** Asset library (materials, models, HDRIs) integrated directly into Blender
- **Relevance:** The built-in BlenderKit add-on (enabled by default in recent versions) provides one-click access to thousands of assets

### Blender Extensions (extensions.blender.org)
- **URL:** https://extensions.blender.org
- **Content:** Official add-on marketplace introduced in Blender 4.2
- **Relevance:** Replaces the older Python scripts repository; standardizes add-on distribution

### Blender Conference Talks (BCON)
- **URL:** https://www.youtube.com/c/BlenderFoundation
- **Content:** Annual conference talks by Blender developers and power users
- **Quality:** Highest — module developers explaining their systems directly
- **Use for:** Deep understanding of architecture decisions, future roadmap, production case studies

---

## Coverage Gaps

The following areas have limited high-quality community documentation:
- **Geometry Nodes Simulation Nodes** (added 3.6) — still maturing, best source is Default Cube's channel and Blender Studio blog posts
- **EEVEE Next internals** — what the rendering pipeline actually does vs classic EEVEE; documentation is sparse
- **Python API gotchas** — context managers, mode requirements, operator vs data API — Stack Exchange is the best source
- **Large-scale production pipeline** — Blender in studio VFX pipelines; Blender Studio posts are the best resource
- **Grease Pencil v3** (major rewrite in 4.3) — documentation was in flux at time of pack creation
