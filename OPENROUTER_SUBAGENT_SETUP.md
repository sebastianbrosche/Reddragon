# OpenRouter Subagent Configuration for OpenClaw

**Purpose:** Enable spawning sub-agents via OpenRouter models so you are not locked to Kimi Claw for parallel work. This lets you run cheaper models for subagents while keeping your main session on the high-quality model you prefer.

**Your OpenRouter API Key:** `[REDACTED - see .secrets/vault.yml]` (from `.secrets/vault.yml`)

---

## What This Gives You

| Before | After |
|--------|-------|
| Main agent only (kimi-coding/k2p6) | Main agent on k2p6 + subagents on cheaper OpenRouter models |
| No parallel task execution | Up to 8 concurrent subagents, each on its own model |
| Single depth (flat) | Orchestrator pattern: main → orchestrator → worker subagents |
| Cost: same for all tasks | Cost-optimized routing: cheap models for simple tasks, premium for complex |

---

## Quick Start — Add This to `openclaw.json`

File location: `/root/.openclaw/openclaw.json`

### 1. Add OpenRouter as a Model Provider

In the `models.providers` section, add the `openrouter` block alongside your existing `kimi-coding` provider:

```json
"models": {
  "mode": "merge",
  "providers": {
    "kimi-coding": {
      "baseUrl": "https://agent-gw.kimi.com/coding",
      "apiKey": "sk-kimi-tKLSvTV6dwhpJaa2FD8kkZffBF0dcnkh0bS9LBUEye18d4oqE8ObOd27w4dUb8wW",
      "api": "anthropic-messages",
      "headers": {
        "User-Agent": "Kimi Claw Plugin",
        "X-Kimi-Claw-ID": "19e220de-e5e2-8fbf-8000-000076d7a8cd"
      },
      "models": [
        {
          "id": "k2p6",
          "name": "k2p6",
          "input": ["text", "image"],
          "reasoning": true,
          "headers": {
            "User-Agent": "Kimi Claw Plugin",
            "X-Kimi-Claw-ID": "19e220de-e5e2-8fbf-8000-000076d7a8cd"
          },
          "contextWindow": 131072,
          "maxTokens": 32768
        }
      ]
    },
    "openrouter": {
      "baseUrl": "https://openrouter.ai/api/v1",
      "apiKey": "[REDACTED - see .secrets/vault.yml]",
      "api": "openai-messages",
      "headers": {
        "HTTP-Referer": "https://hestiafoundation.org",
        "X-OpenRouter-Title": "Hestia Foundation - OpenClaw"
      },
      "models": [
        {
          "id": "anthropic/claude-3.5-sonnet",
          "name": "claude-sonnet-3.5",
          "input": ["text", "image"],
          "reasoning": true,
          "contextWindow": 200000,
          "maxTokens": 8192
        },
        {
          "id": "google/gemini-2.5-pro-exp-03-25",
          "name": "gemini-2.5-pro",
          "input": ["text", "image"],
          "reasoning": true,
          "contextWindow": 1000000,
          "maxTokens": 65536
        },
        {
          "id": "meta-llama/llama-3.1-70b-instruct",
          "name": "llama-3.1-70b",
          "input": ["text"],
          "reasoning": false,
          "contextWindow": 131072,
          "maxTokens": 8192
        },
        {
          "id": "deepseek/deepseek-chat",
          "name": "deepseek-chat",
          "input": ["text"],
          "reasoning": true,
          "contextWindow": 64000,
          "maxTokens": 8192
        },
        {
          "id": "mistralai/mistral-large",
          "name": "mistral-large",
          "input": ["text", "image"],
          "reasoning": false,
          "contextWindow": 131072,
          "maxTokens": 8192
        }
      ]
    }
  }
}
```

### 2. Add Model Aliases

In the `agents.defaults.models` section, add aliases for the OpenRouter models:

```json
"models": {
  "kimi-coding/k2p6": {
    "alias": "kimi-k2p6"
  },
  "openrouter/anthropic/claude-3.5-sonnet": {
    "alias": "claude-sonnet"
  },
  "openrouter/google/gemini-2.5-pro-exp-03-25": {
    "alias": "gemini-pro"
  },
  "openrouter/meta-llama/llama-3.1-70b-instruct": {
    "alias": "llama-70b"
  },
  "openrouter/deepseek/deepseek-chat": {
    "alias": "deepseek"
  },
  "openrouter/mistralai/mistral-large": {
    "alias": "mistral-large"
  }
}
```

### 3. Configure Subagent Defaults

Add the `subagents` block inside `agents.defaults`:

```json
"agents": {
  "defaults": {
    "heartbeat": {
      "every": "60m"
    },
    "compaction": {
      "mode": "safeguard"
    },
    "thinkingDefault": "high",
    "model": {
      "primary": "kimi-coding/k2p6"
    },
    "models": {
      "kimi-coding/k2p6": {
        "alias": "kimi-k2p6"
      },
      "openrouter/anthropic/claude-3.5-sonnet": {
        "alias": "claude-sonnet"
      },
      "openrouter/google/gemini-2.5-pro-exp-03-25": {
        "alias": "gemini-pro"
      },
      "openrouter/meta-llama/llama-3.1-70b-instruct": {
        "alias": "llama-70b"
      },
      "openrouter/deepseek/deepseek-chat": {
        "alias": "deepseek"
      },
      "openrouter/mistralai/mistral-large": {
        "alias": "mistral-large"
      }
    },
    "subagents": {
      "model": "openrouter/deepseek/deepseek-chat",
      "maxSpawnDepth": 2,
      "maxChildrenPerAgent": 5,
      "maxConcurrent": 8,
      "runTimeoutSeconds": 900,
      "announceTimeoutMs": 120000
    },
    "memorySearch": {
      ...
    }
  }
}
```

### 4. Enable Agent-to-Agent Communication (Optional but Recommended)

In the `tools` section, ensure these are set:

```json
"tools": {
  "profile": "full",
  "sessions": {
    "visibility": "all"
  },
  "agentToAgent": {
    "enabled": true,
    "allow": ["*"]
  }
}
```

### 5. Allow Subagent Spawning

Ensure the main agent can spawn itself as a subagent. The `agents.defaults.subagents` config already covers this, but if you want explicit allowlisting:

```json
"agents": {
  "list": [
    {
      "id": "main",
      "subagents": {
        "allowAgents": ["main"]
      }
    }
  ]
}
```

If you don't have an `agents.list` section, you can add it alongside `agents.defaults`.

---

## Model Selection Cheat Sheet

| Alias | Model | Cost | Best For |
|-------|-------|------|----------|
| `kimi-k2p6` | kimi-coding/k2p6 | Medium | Main agent — complex reasoning, coding, architecture decisions |
| `claude-sonnet` | Claude 3.5 Sonnet | Medium-High | Subagent — high-quality reasoning, writing, analysis |
| `gemini-pro` | Gemini 2.5 Pro | Medium | Subagent — long context, multimodal, research |
| `llama-70b` | Llama 3.1 70B | Low | Subagent — fast, cheap, good for parallel tasks |
| `deepseek` | DeepSeek Chat | Very Low | Subagent — ultra-cheap, good for code, summaries |
| `mistral-large` | Mistral Large | Low | Subagent — European provider, good for multilingual |

**Cost strategy:** Set subagents to `deepseek` or `llama-70b` by default. Override to `claude-sonnet` or `gemini-pro` when the task explicitly needs high reasoning quality.

---

## How to Spawn Subagents

### From within an agent session (tool call):

```json
{
  "task": "Research the latest EU housing grants and compile a summary",
  "model": "openrouter/deepseek/deepseek-chat",
  "runTimeoutSeconds": 600
}
```

Or using aliases:

```json
{
  "task": "Write a technical blog post about ground screw foundations",
  "model": "deepseek",
  "runTimeoutSeconds": 600
}
```

### From chat (slash command):

```
/spawn --model deepseek "Research the latest EU housing grants"
```

### Orchestrator pattern (depth 2):

```
Main agent (kimi-k2p6) 
  → spawns orchestrator subagent (claude-sonnet) 
    → spawns 3 worker subagents (deepseek, llama-70b, deepseek)
```

The orchestrator synthesizes results and announces back to main.

---

## Verification Steps

After editing `openclaw.json`:

1. **Restart the gateway:**
   ```bash
   openclaw gateway restart
   ```

2. **Check model availability:**
   ```bash
   openclaw status
   ```
   Look for the new models in the status output.

3. **Test a subagent spawn:**
   ```
   /spawn --model deepseek "What is 2+2?"
   ```

4. **Check subagent model:**
   ```
   /subagents list
   /subagents info <id>
   ```
   Verify the model field shows the OpenRouter model.

---

## Important Notes

- **Token usage:** Each subagent runs in its own context. 5 parallel subagents = ~5x the token cost of sequential. Offset this by using cheaper models.
- **Model fallback:** If OpenRouter returns a 5xx or rate-limits, OpenRouter automatically falls back to another provider for the same model. You don't handle this.
- **Context isolation:** Subagents do NOT automatically inherit `SOUL.md`, `USER.md`, etc. Pass context explicitly in the task description if needed.
- **Depth 2 limit:** Workers (depth 2) cannot spawn further children. Only the orchestrator (depth 1) can spawn workers.

---

## Full Reference

- OpenClaw subagent docs: https://docs.openclaw.ai/tools/subagents
- OpenRouter models: https://openrouter.ai/models
- OpenRouter pricing: https://openrouter.ai/models (sort by price)
- OpenClaw `/spawn` command: https://github.com/openclaw/openclaw/issues/6162

---

*Document created 2026-06-03. OpenRouter key verified from vault. Gateway config path: `/root/.openclaw/openclaw.json`*
