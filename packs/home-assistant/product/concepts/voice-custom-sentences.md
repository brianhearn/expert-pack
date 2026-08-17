---
title: "Custom Assist Sentences"
type: concept
tags:
  - voice-assistant
  - intents
  - custom-sentences
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/voice-custom-sentences
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - voice-assist-practices.md
  - voice-llm-agents.md
  - automation-trigger-action.md
content_hash: sha256:8c8ec886bbbbd8a19d9d74c8e32741475627f394b78fbb7a685dd2535d52e2ea
---
# Custom Assist Sentences

Assist's built-in sentence coverage is limited to common smart home commands. Custom sentences in `config/custom_sentences/en/` plus `intent_script` let you add phrases like "good night" or "movie time" that run scripts and scenes.

## Custom Sentences

Assist's built-in sentence coverage is limited to common smart home commands. You can extend it with custom sentences defined in YAML files.

**Location:** `config/custom_sentences/en/` (create if it doesn't exist)

**Example — custom commands:**
```yaml
# config/custom_sentences/en/custom.yaml
language: "en"
intents:
  GoodNight:
    data:
      - sentences:
          - "good night"
          - "I'm going to bed"
          - "goodnight"
  
  MovieMode:
    data:
      - sentences:
          - "movie time"
          - "start movie mode"
          - "we're watching a movie"
```

Then in `configuration.yaml` (or `intents.yaml`):
```yaml
intent_script:
  GoodNight:
    speech:
      text: "Good night! Lights off and alarm set."
    action:
      - action: script.good_night_routine
  
  MovieMode:
    speech:
      text: "Enjoy the movie!"
    action:
      - action: scene.turn_on
        target:
          entity_id: scene.movie_mode
```

Custom sentences support slots (variables), lists, and wildcards. You can build surprisingly capable custom commands this way.

## Related Concepts

- [[voice-assist-practices.md|voice assist practices]]
- [[voice-llm-agents.md|voice llm agents]]
- [[automation-trigger-action.md|automation trigger action]]
