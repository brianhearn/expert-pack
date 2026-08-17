# Composite conflict resolver

Executable contract for [schemas/composite.md](../../schemas/composite.md) § Cross-Pack Conflict Resolution.

```bash
python tools/composite/test_conflict.py
```

`conflict.resolve()` is the consumer recipe: isolate → authority → agree / `fail_closed` / `flag` / `priority`. It does not write packs and does not require EP MCP.
