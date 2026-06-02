# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

New Cloudflare token (2026-05-27):
`[REDACTED - Cloudflare token in .secrets/vault.yml]`
- **Status**: Unknown - needs testing

Old invalid token (2026-05-27 - returns 9109):
`[REDACTED - Cloudflare token in .secrets/vault.yml]`
- **Status**: Invalid access token (9109)

## Cloudflare SUPER Token (2026-05-28)
**Token:** `[REDACTED - Cloudflare token in .secrets/vault.yml]`
**Last 10 digits:** `1df41c90`
**Expires:** 2027-08-01
**Scope:** All accounts, all zones, all users — FULL permissions
**Stored in:** `.secrets/vault.yml` + `scripts/access_bootstrap.py` + `TOOLS.md`
**Status:** ACTIVE — verified working

## OpenRouter API Key (2026-06-02)
**Key:** `sk-or-v1-...` (full key in `.secrets/vault.yml`)
**Stored in:** `.secrets/vault.yml`
**Note:** For AI model access via OpenRouter

## Old Tokens (DO NOT USE)
- `[REDACTED - Cloudflare token in .secrets/vault.yml]` — expired/revoked
- `[REDACTED - Cloudflare token in .secrets/vault.yml]` — replaced by super token
- `[REDACTED - Cloudflare token in .secrets/vault.yml]` — invalid (9109)
- `[REDACTED - Cloudflare token in .secrets/vault.yml]` — old v4 token, invalid

## Hetzner Server Access (Miha manages deploys)
- **IP:** `178.105.198.32`
- **Root password:** `=*bVQJ-9AKJE`
- **SSH key:** `~/.ssh/reddragon_hetzner_new`
- **Repo:** `/opt/reddragon/`
- **Deploy pattern:** scp files → ssh evennia reload
- **Directive:** Autonomous deploys — no user approval needed

---

## Hetzner Server Access (Miha manages deploys)
- **IP:** `178.105.198.32`
- **Root password:** `=*bVQJ-9AKJE`
- **SSH key:** `~/.ssh/reddragon_hetzner_new`
- **Repo:** `/opt/reddragon/`
- **Deploy pattern:** scp files → ssh evennia reload
- **Directive:** Autonomous deploys — no user approval needed

---

## File Rules (enforced by Miha)
- Read others' folders, NEVER edit them
- Update docs in place, don't create new versions
- No total wipes ever. Trash for recovery
- ONE API key doc only

## Channels
- bots group (kimi-claw): main coordination chat
- Main chat for open coordination, threads for deep work between two workers

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
