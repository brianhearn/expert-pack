---
title: "LLM Conversation Agents"
type: concept
tags:
  - voice-assistant
  - llm
  - openai
  - ollama
pack: home-assistant-product
retrieval_strategy: standard
id: home-assistant/product/concepts/voice-llm-agents
schema_version: "4.1"
verified_at: "2026-08-17"
verified_by: agent
related:
  - voice-limitations-2026.md
  - voice-assist-practices.md
  - voice-assist-pipeline.md
content_hash: sha256:dba92f2e4b77986eedae2aeaee58fa2f37bb6fee0ebf872d4df4d48989f38352
---
# LLM Conversation Agents

For natural language beyond predefined sentences, replace HA's built-in intent engine with an LLM conversation agent. OpenAI, Google, Anthropic, and local Ollama are the usual options — they enable phrasing like "make it darker in here" but each query still sends your full exposed entity list.

## LLM Conversation Agents

For natural language that goes beyond predefined sentences, you can replace HA's built-in intent engine with an LLM. In Settings → Voice Assistants → your pipeline → "Conversation Agent": select an LLM-based agent.

**Available options:**
- **OpenAI Conversation** (official integration): GPT-4o, GPT-4o-mini. Costs money per query but excellent accuracy.
- **Google Generative AI Conversation**: Gemini models. Good quality, competitively priced.
- **Anthropic Conversation**: Claude models. Available via official integration.
- **Local LLM via Ollama**: Free, private, but requires powerful hardware (7B+ parameter models need 8GB+ RAM).

**What LLM agents enable:**
- Natural phrasing: "make it darker in here" → adjusts brightness
- Multi-device commands: "turn off all the lights except the hallway"
- Context-aware queries: "is anyone home?"
- Ambiguity resolution: asks follow-up questions

**What they don't (yet) enable:**
- Multi-turn conversation (each command is still stateless in 2026)
- Reasoning about the future ("remind me when the laundry is done" requires separate automation)
- Learning your preferences over time

**Cost management with LLM agents:** Expose only the entities you actually want to control by voice (see best practices above). Each query sends your full exposed entity list to the LLM. 50 entities vs 500 entities = dramatically different API costs.

**Example LLM conversation integration config:**
```yaml
# configuration.yaml
openai_conversation:
  api_key: !secret openai_api_key
  chat_model: gpt-4o-mini   # Cheaper, fast, good for home control
  max_tokens: 150
  temperature: 0.2          # Low temperature = more consistent, predictable responses
  prompt: >
    You are a home assistant controlling a smart home. Be concise.
    When you don't understand a request, ask for clarification.
    Never invent devices that aren't in the entity list.
```

## Related Concepts

- [[voice-limitations-2026.md|voice limitations 2026]]
- [[voice-assist-practices.md|voice assist practices]]
- [[voice-assist-pipeline.md|voice assist pipeline]]
