# How to Access the OpenRouter Subagent Guide

**File:** `OPENROUTER_SUBAGENT_GUIDE.md`  
**Location:** `/root/.openclaw/workspace/` (shared workspace)  
**Who:** Adam and Bob  

---

## Access Methods

### 1. Direct Read (if you have workspace access)
```bash
cat /root/.openclaw/workspace/OPENROUTER_SUBAGENT_GUIDE.md
```

### 2. Via Miha (if you need it delivered)
Ask Miha to paste the contents, or summarize specific sections. He can also email it, send it to your channel, or convert it to PDF if needed.

### 3. GitHub (if synced)
If the workspace is synced to `github.com/sebastianbrosche/Reddragon`, pull the latest and check the repo root.

---

## Quick Summary of What's Inside

- **6 model aliases** with costs and use cases
- **4 practical examples** (code review, architecture, document analysis, batch tasks)
- **Config details** — provider setup, subagent defaults, timeout settings
- **Troubleshooting table** — common errors and fixes
- **Quick-reference card** — which model to pick when

**TL;DR:** If you spawn a subagent and want it cheap, use `model: "llama-70b"`. If you want it smart, use `model: "claude-sonnet"`. Default is `deepseek`.

---

**Questions?** Ask Miha directly. He wrote the guide and can clarify anything.
