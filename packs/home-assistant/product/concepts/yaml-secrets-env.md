---
title: "secrets.yaml and !env_var"
type: concept
tags:
  - yaml-configuration
  - secrets
  - env-var
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/yaml-secrets-env
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - yaml-vs-ui.md
  - yaml-includes.md
  - yaml-validation.md
content_hash: sha256:2c80dc1b369da832ecceb8393e8ddd9d102928a890ee36a7c5a98da01203ab17
---
# secrets.yaml and !env_var

`secrets.yaml` keeps API keys and passwords out of version control via `!secret` — it does not encrypt them. `!env_var` reads environment variables and exists only on HA Core (venv), not HA OS or Supervised.

## secrets.yaml

Store sensitive values (API keys, passwords, coordinates) here instead of inline in `configuration.yaml`:

```yaml
# secrets.yaml
google_api_key: "AIzaSyBXXXXXXXXXXXXXXXXXXXX"
mqtt_password: "super-secret-password"
latitude: 30.4518
longitude: -84.2807
home_alarm_code: "1234"
```

Reference in `configuration.yaml`:
```yaml
homeassistant:
  latitude: !secret latitude
  longitude: !secret longitude
```

**What secrets.yaml does NOT do:** It doesn't encrypt values. The file is plaintext. Its purpose is to prevent secrets appearing in code/version control, not to encrypt them. If you use git for your config, ensure `secrets.yaml` is in `.gitignore`.

**Debug mode gotcha:** When running `ha core check` or checking config, secret values are masked in output. This is intentional.

## The `!env_var` Directive (HA Core Only)

Available in HA Core (Python venv) installs only — NOT in HA OS/Supervised. Reads environment variables:

```yaml
# configuration.yaml (Core install only)
http:
  server_host: !env_var SERVER_HOST "0.0.0.0"
  server_port: !env_var SERVER_PORT 8123
```

This enables Docker/container deployments to inject values without editing YAML files. Not applicable to most HA OS users.

## Related Concepts

- [[yaml-vs-ui.md|yaml vs ui]]
- [[yaml-includes.md|yaml includes]]
- [[yaml-validation.md|yaml validation]]
