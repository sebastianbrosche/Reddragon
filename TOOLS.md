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

## Heat Lagos API Keys (Miha manages)
- SerpAPI key stored in group doc: `kimi-group-chat/bots/Heat Lagos - API & Access Keys.md`
- Key doc is canonical. ONE doc, updated in place, never duplicated.
- I back it up after every update.
- Missing: Shelly API, bsport login credentials

### Cloudflare Tokens (rolling)
- **Account API (v3, 2026-05-16):** `cfat_gZPIL52Ki9lcyFid6No89Vf8Wj2h2YJixAdm4Dmp90016b9b` — Zone ID: `cb8ab13b857925cdb9b3c0fd9d4ec4bf` — **TESTED: Works** for DNS, Pages, zone management
- **Worker API (v1, 2026-05-16):** `cfut_FWdCjiaC5zFf1rKDt67IQijs7G29pft97GF8dZL4857eec98` — **TESTED: Works** for Workers, KV, Durable Objects, R2
- **Worker API (v2, 2026-05-21):** `cfut_YKTQuAMClyldwvmASE2dtBZ3z0LzDOvrfemTdH7V21836a51` — NEW token for RCP Pages deployment
- **Previous Account (v2, 2026-05-15):** `cfut_zOCov9RQdnKGXndhoWB0TKhHQ5SyLOBQ1HnAwdeZ65e01d72` — Pages:Edit fixed after Sebastian hit save
- **Deprecated:** All previous tokens marked deprecated in group doc
- Sebastian wants all bots to have Cloudflare access

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
