# Miha Backup Guide — For All Agents

**Date:** 2026-05-30
**Author:** Miha
**Status:** ACTIVE — replaces old Google Drive backup routine

---

## What Changed

**Old system:** `backup_miha.sh` created a tarball and uploaded to Google Drive via `rclone`.  
**New system:** `backup_miha.sh` commits changes to Git and pushes to GitHub.

**Why:** Git gives us version history, delta tracking, and no dependency on rclone or Google Drive service accounts. Push protection also prevents secrets from leaking.

---

## Quick Reference

| Item | Value |
|---|---|
| **Script** | `backup_miha.sh` (in `/root/.openclaw/workspace/`) |
| **Repository** | `https://github.com/sebastianbrosche/Reddragon.git` |
| **Branch** | `master` |
| **Cron** | Daily at `03:17` (off-peak) |
| **Secret Store** | `.secrets/vault.yml` — **never commit this** |
| **Sanitizer** | `scripts/sanitize_secrets.py` — runs before every commit |

---

## How to Trigger a Backup

### 1. Automatic (daily)
```
03:17 * * * /bin/bash /root/.openclaw/workspace/backup_miha.sh >> /root/.openclaw/workspace/backup.log 2>&1
```
Runs every morning. No action needed.

### 2. Manual (on demand)
```bash
cd /root/.openclaw/workspace
bash backup_miha.sh
```

### 3. From code (agent-initiated)
```bash
# Run the script from any working directory
bash /root/.openclaw/workspace/backup_miha.sh
```

---

## What Gets Backed Up

Everything in the workspace **except** these (enforced by `.gitignore`):

| Excluded | Reason |
|---|---|
| `.secrets/` | All API tokens, passwords, credentials — **local only** |
| `downloads/` | Temporary downloaded files |
| `mud/evenv/` | Python virtual environment (189 MB) |
| `*.log`, `*.pid`, `evennia.db3` | Runtime artifacts |
| `__pycache__/` | Compiled Python cache |
| `reddragon_local_archived/`, `reddragon_local_backup_*.tgz` | Large archives (already archived locally) |
| `hestia-foundation/` | Submodule — has its own repo |
| `rcp/website/` | Submodule — has its own repo |

---

## Secret Sanitization (Important!)

Before every commit, the script runs `scripts/sanitize_secrets.py`. It scans these files for token patterns:

- `cfut_...` (Cloudflare tokens)
- `ghp_...` (GitHub PATs)
- `gho_...` (GitHub OAuth tokens)
- `AKIA...` (AWS keys)

**Files scanned:** `MEMORY.md`, `TOOLS.md`, `USER.md`, `scripts/access_bootstrap.py`, and all memory files.

**Rule:** If you save a token in a tracked file, the sanitizer will redact it and replace it with `[REDACTED - see .secrets/vault.yml]`. The real value must live in **`.secrets/vault.yml`** only.

---

## How to Add a New Secret

**Never paste raw tokens into tracked files.** Follow this process:

```bash
# 1. Save the secret to the vault
edit /root/.openclaw/workspace/.secrets/vault.yml

# 2. Reference it in tracked files with a placeholder
# Example in TOOLS.md:
# Cloudflare token: see .secrets/vault.yml (last 10 digits: 1df41c90)

# 3. Run the backup — sanitizer will catch any mistakes
bash backup_miha.sh
```

---

## What to Do If GitHub Push Fails

### Error: "secret detected" (push protection)

1. Run the sanitizer manually:
   ```bash
   python3 /root/.openclaw/workspace/scripts/sanitize_secrets.py
   ```
2. Check what was found: `git diff` (should show redacted tokens)
3. Stage and re-commit:
   ```bash
   git add -A && git commit -m "fix: sanitize secrets" && git push origin master
   ```

### Error: "Repository moved"

The remote is already updated to `https://github.com/sebastianbrosche/Reddragon.git`. If you see this error, check:

```bash
cd /root/.openclaw/workspace
git remote -v
```

It should show:
```
origin  https://ghp_****@github.com/sebastianbrosche/Reddragon.git (fetch)
origin  https://ghp_****@github.com/sebastianbrosche/Reddragon.git (push)
```

If it still shows the old `reddragon` URL (lowercase), update it:
```bash
git remote set-url origin https://ghp_$(grep -o 'ghp_[A-Za-z0-9]*' /root/.openclaw/workspace/.secrets/vault.yml | head -1)@github.com/sebastianbrosche/Reddragon.git
```

### Error: "Authentication failed"

The GitHub PAT is stored in `.secrets/vault.yml`. Verify it:
```bash
# Check if PAT is valid
curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $(grep -o 'ghp_[A-Za-z0-9]*' /root/.openclaw/workspace/.secrets/vault.yml | head -1)" https://api.github.com/user
```

If it returns `401`, the PAT is expired. Tell Sebastian to generate a new one.

---

## Submodule Handling

Two directories are **submodules** — they have their own Git repos and should NOT be committed into the parent workspace:

| Submodule | Its own repo |
|---|---|
| `hestia-foundation/` | `sebastianbrosche/hestiafoundation` |
| `rcp/website/` | (unknown — ask if needed) |

**If you make changes inside a submodule:**
1. `cd` into the submodule directory
2. `git add -A && git commit -m "..." && git push` from there
3. The parent workspace backup will notice the submodule hash changed and commit that pointer

The backup script handles the case where only submodule changes exist — it skips the commit gracefully rather than failing.

---

## Checking Backup Status

```bash
# View recent commits
cd /root/.openclaw/workspace
git log --oneline -5

# Check cron job
crontab -l

# Check backup log
tail -20 /root/.openclaw/workspace/backup.log

# Check if there are uncommitted changes
git status --short
```

---

## Restoring From Backup

```bash
# Clone the repository to a new machine
git clone https://github.com/sebastianbrosche/Reddragon.git

# Or pull latest on existing machine
cd /root/.openclaw/workspace
git pull origin master
```

**Note:** Secrets will NOT be restored — `.secrets/` is excluded. You must recreate the vault manually from another source (Sebastian's password manager, etc.)

---

## Rules for All Agents

1. **Never commit `.secrets/`** — it's in `.gitignore` for a reason
2. **Never paste tokens into `MEMORY.md`, `TOOLS.md`, or `USER.md`** — use placeholders
3. **Run the backup after significant work** — don't let days of changes pile up
4. **If backup fails, don't ignore it** — fix the issue (usually secrets in tracked files)
5. **Submodules are separate** — commit changes inside them, not from the parent repo

---

## Emergency: If the Backup System Breaks

```bash
# 1. Check if Git repo exists
git rev-parse --git-dir

# 2. Check if remote is configured
git remote -v

# 3. Check if PAT is valid
curl -H "Authorization: token $(grep -o 'ghp_[A-Za-z0-9]*' /root/.openclaw/workspace/.secrets/vault.yml | head -1)" https://api.github.com/user | grep login

# 4. If all else fails, create a manual tarball as fallback
cd /root/.openclaw/workspace
tar -czf /tmp/miha_backup_$(date +%Y%m%d_%H%M%S).tgz \
  --exclude='.secrets' --exclude='downloads' --exclude='mud/evenv' \
  --exclude='*.log' --exclude='__pycache__' .
```

---

## Contact

If something goes wrong with the backup system, **tell Sebastian immediately** — data loss is the one thing we don't get back.

— Miha
