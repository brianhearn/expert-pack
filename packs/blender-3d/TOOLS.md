# Pack Tools & Capabilities

Integrator contract for the Blender 3D pack. Not loaded into agent context by default.

## Authority and grounding

Read `manifest.authority_boundary` before answering.

- Answer only inside `in_scope` (Blender pipeline topics documented in this pack).
- Decline other DCC/editing tools except as brief contrast, plus legal/medical/financial advice.
- If no supporting atom is retrieved, say so — do not invent Blender UI paths or shortcut keys.

## Retrieval

- **Recommended backend:** EP MCP `/search`, OpenClaw RAG, or a plain vector store pointed at this directory.
- **Chunking:** concept atoms target 400–800 tokens (1,000 ceiling). Oversized `atomic` files carry `.chunks.yaml` sidecars with `context_prefix`.
- **Consume loop:** search → read the whole atom → expand `requires:` → stop (budget 3 / cap 7).
- **Reconstruct / TAC:** use when the consumer needs auditable claim-to-span answers.

## Agent workflows

- Hard-surface modeling → `workflows/hard-surface-modeling.md`
- Character animation → `workflows/character-animation.md`
- Product visualization → `workflows/product-visualization.md`
- Motion graphics → `workflows/motion-graphics.md`
- Scene optimization → `workflows/scene-optimization.md`
