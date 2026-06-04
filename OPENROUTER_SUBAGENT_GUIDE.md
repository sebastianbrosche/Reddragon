# OpenRouter Subagent Setup Guide for Adam & Sarah

**Prepared by:** Miha (Kimi Claw)  
**Date:** 2026-06-04  
**For:** Adam (Heath Lagos) and Sarah (Yoga for BJJ)  
**Topic:** How to spawn subagents via OpenRouter instead of relying only on Kimi Claw

---

## What This Is

Miha just configured OpenRouter as a backup/alternative model provider for spawning subagents. This means you can now spawn subagents with different AI models (Claude, Gemini, DeepSeek, etc.) without depending solely on Kimi Claw's infrastructure.

**Why it matters:** Less vendor lock-in, more model choice, cheaper options for simple tasks, and better availability when one provider is down.

---

## How Subagent Spawning Works

### Basic Command

```json
sessions_spawn({
  "task": "Your task description here",
  "model": "deepseek"  // or any alias below
})
```

### Available Model Aliases

| Alias | Full Model | Best For | Context | Cost (input/output per M) |
|-------|-----------|----------|---------|---------------------------|
| `kimi-k2p6` | `kimi-coding/k2p6` | General coding, reasoning | 131K | Kimi rates |
| `claude-sonnet` | `anthropic/claude-3.5-sonnet` | Complex coding, analysis | 200K | $3/$15 |
| `gemini-pro` | `google/gemini-2.5-pro-exp-03-25` | Long documents, 1M context | 1M | $1.25/$3.75 |
| `llama-70b` | `meta-llama/llama-3.1-70b-instruct` | Fast, cheap, simple tasks | 131K | ~$0.30/$0.60 |
| `deepseek` | `deepseek/deepseek-chat` | Code, reasoning, cheap | 64K | ~$0.50/$2.00 |
| `mistral-large` | `mistralai/mistral-large` | Multilingual, European | 131K | ~$2/$6 |

**Rule of thumb:**
- Quick/trivial tasks → `llama-70b` or `deepseek`
- Complex coding → `claude-sonnet` or `deepseek`
- Long documents → `gemini-pro` (1M context!)
- Default/unsure → `deepseek` (balanced, cheap)

---

## Configuration Details

### OpenRouter Provider Setup

```json
{
  "models": {
    "providers": {
      "openrouter": {
        "baseUrl": "https://openrouter.ai/api/v1",
        "apiKey": "sk-or-v1-...",
        "api": "openai-completions",
        "headers": {
          "HTTP-Referer": "https://hestiafoundation.org",
          "X-OpenRouter-Title": "Hestia Foundation - OpenClaw"
        },
        "models": [ ... ]
      }
    }
  }
}
```

### Subagent Defaults

```json
{
  "agents": {
    "defaults": {
      "subagents": {
        "model": "deepseek",
        "maxSpawnDepth": 2,
        "maxChildrenPerAgent": 8,
        "maxConcurrent": 8,
        "runTimeoutSeconds": 900,
        "announceTimeoutMs": 120000
      }
    }
  }
}
```

---

## Practical Examples

### Example 1: Quick Code Review
```json
sessions_spawn({
  "task": "Review this Python function for bugs and style issues.\n\n```python\ndef calculate_total(items):\n    total = 0\n    for item in items:\n        total += item.price * item.quantity\n    return total\n```",
  "model": "llama-70b"
})
```

### Example 2: Complex Architecture Design
```json
sessions_spawn({
  "task": "Design a database schema for a yoga class booking system with users, classes, instructors, payments, and waitlists. Include indexing strategy and relationships.",
  "model": "claude-sonnet"
})
```

### Example 3: Long Document Analysis
```json
sessions_spawn({
  "task": "Read this 50-page PDF and extract all key findings, methodology, and conclusions. Summarize in 500 words.",
  "model": "gemini-pro"
})
```

### Example 4: Batch Parallel Tasks
```json
// Spawn 3 subagents in parallel, each with a different model
sessions_spawn({
  "task": "Draft a tweet thread about our upcoming yoga retreat.",
  "model": "deepseek"
});

sessions_spawn({
  "task": "Create a Facebook post for the same retreat.",
  "model": "llama-70b"
});

sessions_spawn({
  "task": "Write an Instagram caption with hashtags.",
  "model": "claude-sonnet"
});
```

---

## Important Notes

1. **Model override bug is FIXED** (as of 2026.04+): The model you specify is actually used at inference time, not ignored.

2. **Subagents are isolated**: No memory, no user context. You must pass everything needed in the `task` prompt.

3. **Results auto-announce**: Subagents announce results back to the chat automatically. No manual fetching needed.

4. **Max depth = 2**: A subagent can spawn its own subagents, but only 1 level deep. Don't go deeper.

5. **Max concurrent = 8**: Don't try to spawn more than 8 at once. Batch in groups if needed.

6. **Cost tracking**: OpenRouter returns `cost` in responses. Check your dashboard at https://openrouter.ai/activity

7. **Fallback behavior**: If a model fails, OpenRouter can auto-fallback to another provider for the same model family (if configured).

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| "Model not found" | Wrong alias or provider not configured | Check `agents.defaults.models` aliases |
| "Provider error" | OpenRouter API key invalid | Verify `sk-or-v1-...` key in config |
| Subagent hangs | Task too long or model overloaded | Reduce timeout, try different model |
| High costs | Using expensive model for simple task | Switch to `llama-70b` or `deepseek` |
| Results not appearing | Announce timeout too short | Increase `announceTimeoutMs` |

---

## Key OpenRouter Resources

- **API Docs:** https://openrouter.ai/docs
- **Models List:** https://openrouter.ai/models
- **Pricing:** https://openrouter.ai/models (click any model)
- **Activity Dashboard:** https://openrouter.ai/activity
- **API Key:** In `~/.openclaw/config.json` under `models.providers.openrouter.apiKey`

---

## Quick Reference Card

```
Spawn cheap & fast:   model: "llama-70b"
Spawn balanced:       model: "deepseek"
Spawn smart & slow:   model: "claude-sonnet"
Spawn for huge docs:  model: "gemini-pro"
Default if unsure:    model: "deepseek"
```

---

*Questions? Ask Miha. He set this up and knows where the bodies are buried.*

**Miha's note:** *"I already tested this. It works. Don't overthink it."*
