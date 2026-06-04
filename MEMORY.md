
---

## Elastomania/Across Mod System — DEFERRED (2026-06-04)
**Status:** User said "save it for later" — not building now, logged for future activation.
**Spec:** Full spec file at `downloads/19e8f63a-3e12-88b9-8000-0000bf9b6daa_elasto_ai_agent_spec.md`
**What it is:** Fork Across repo, add child-friendly visual skin/mod layer (decoupled from physics), image upload for rider/bike skins, preserve deterministic replay.
**What I can do:** Fork, build skin system, set up GitHub repo, write Windows installer (Inno/NSIS). Build CI for `.exe` via GitHub Actions since I'm on Linux.
---

## Dual OpenClaw Instance Setup — PREFERRED (2026-06-04)
**User choice:** Option C — Browser Relay with two Chrome profiles
**Status:** Ready to deploy tomorrow (new computer migration)
**Goal:** Two independent gateway instances (18789 + 18790), each with own Chrome + Browser Relay, controlled entirely via Telegram (no monitor needed)
**Architecture:**
- Instance 1: Default port 18789, default workspace, existing Telegram bot
- Instance 2: Port 18790, separate workspace (`OPENCLAW_HOME=/root/.openclaw-instance2`), NEW Telegram bot token needed
- Chrome Profile 1: Browser Relay → ws://127.0.0.1:18789
- Chrome Profile 2: Browser Relay → ws://127.0.0.1:18790
- Both autostart on boot via systemd/crontab
**Next step:** Create second Telegram bot token via @BotFather, then deploy after new computer arrives
**Note:** User has a new computer coming tomorrow — migrate this setup there

---

## claude-mem + context — INSTALLED (2026-06-05)
**claude-mem** (persistent memory plugin) installed and enabled in OpenClaw. Worker running on port 37777 with OpenRouter provider. Gateway restart pending to fully activate.
**neuledge/context** (MCP docs server) installed globally at `/usr/bin/context` v1.1.0. React docs tested and working. Available to all subagents via shell commands.

