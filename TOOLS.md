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

## Cloudflare Tokens — PERMANENT FIX (2026-05-23 18:50)

**Working Token (DNS, Zones, Workers, Pages, Billing):**
`cfut_Q4dyJHm7d7kMmMuvASPwOR9z0Cv0xjNpSlbHAO71ab9ecb69`
- Expires: 2027-07-01
- **CANNOT create other tokens** (Cloudflare security policy: sub-tokens can't manage tokens)
- **Use for:** All deploys, DNS, Pages, Workers operations

**Token Management Token (User-level only):**
`cfut_NTG40QlJ3aZ6YynVU10lbosP5FyN0QhsmqBXm3Xecd79fda2`
- Name: "Create Additional Tokens"
- Expires: 2027-06-03
- Has "API Tokens Write" but only for USER-level resources
- **CANNOT create account-level tokens** (no zone/account access)

**To create tokens programmatically, Sebastian needs:**
A SUPER token with BOTH:
1. Account → Account → Read
2. Account → API Tokens → Edit (at account level, not user level)

**Until then:** Sebastian pastes tokens, I save them. No more asking.

---

## Heat Lagos API Keys (Miha manages)
- SerpAPI key stored in group doc: `kimi-group-chat/bots/Heat Lagos - API & Access Keys.md`
- Key doc is canonical. ONE doc, updated in place, never duplicated.
- I back it up after every update.
- Missing: Shelly API, bsport login credentials

### Cloudflare Tokens — WORKING (2026-05-23)
- **Pages deploy token:** `cfut_Q4dyJHm7d7kMmMuvASPwOR9z0Cv0xjNpSlbHAO71ab9ecb69` — **WORKING for Pages deploys**
- **Old v4 token INVALID:** `cfut_ukOJ2c79nvP3dbljXXRRGOiGhokkLDTCHpSzhXQ05ad4b93d` returns 9109 — do not use for deploys
- **User directive:** Do NOT ask for token refresh. v4 token is the permanent one.

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
