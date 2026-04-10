# deploy-prep

Deploy preparation tools for ExpertPack. These tools produce clean, deploy-ready copies of a pack without modifying the source.

## ep-strip-frontmatter.py

Strips YAML frontmatter (`---...---` blocks) from all `.md` files in a pack before indexing.

**Why:** Provenance frontmatter (`id`, `content_hash`, `verified_at`, `verified_by`) is management metadata — it serves tooling and freshness tracking, not retrieval. Embedding it alongside content dilutes semantic similarity scores and wastes context tokens.

**Principle:** Source files (in the ExpertPacks repo) retain full provenance. The help bot indexes clean files. Deploy artifacts are ephemeral and gitignored.

### Usage

```bash
# Standard deploy prep
python3 ep-strip-frontmatter.py --src ./ezt-designer --out ./ezt-designer-deploy

# Dry run — see what would be stripped
python3 ep-strip-frontmatter.py --src ./ezt-designer --out ./ezt-designer-deploy --dry-run

# Suppress overwrite warning
python3 ep-strip-frontmatter.py --src ./ezt-designer --out ./ezt-designer-deploy --force
```

### Recommended deploy pattern

```bash
# 1. Strip frontmatter to a temp deploy dir
python3 ExpertPack/tools/deploy-prep/ep-strip-frontmatter.py \
    --src ExpertPacks/ezt-designer \
    --out /tmp/ezt-designer-deploy \
    --force

# 2. Package and ship
tar czf /tmp/ezt-designer-deploy.tar.gz -C /tmp/ezt-designer-deploy .
scp /tmp/ezt-designer-deploy.tar.gz root@64.225.0.26:/tmp/
ssh root@64.225.0.26 "rm -rf /root/.openclaw/workspace/ezt-designer && \
    mkdir -p /root/.openclaw/workspace/ezt-designer && \
    tar xzf /tmp/ezt-designer-deploy.tar.gz -C /root/.openclaw/workspace/ezt-designer"

# 3. Clean up
rm -rf /tmp/ezt-designer-deploy /tmp/ezt-designer-deploy.tar.gz
```
