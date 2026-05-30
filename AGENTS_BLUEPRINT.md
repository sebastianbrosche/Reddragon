# Agent Access Blueprint - Self-Healing Infrastructure

**Every agent** (Miha, Adam, Sarah, future bots) reads this on startup.

## The Problem
- SSH keys get wiped on server rebuilds
- API tokens expire silently
- Bots lose access mid-work and can't tell you why
- Different agents have different credentials scattered across files

## The Solution

### 1. Single Source of Truth
```
~/.openclaw/workspace/.secrets/vault.yml    # All credentials
~/.openclaw/workspace/scripts/access_bootstrap.py  # Self-healing checker
```

### 2. On Every Bot Wake
Each agent runs (or checks results from):
```bash
python3 scripts/access_bootstrap.py --fix
```

This verifies:
- ✅ SSH key works → auto-restores if broken
- ✅ Cloudflare token valid → warns before expiry
- ✅ Evennia running → auto-restarts if down
- ✅ Firewall ports open → auto-opens if closed

### 3. Agent-Specific Wiring

**Miha (Infrastructure/Red Dragon)**
- Uses `vault.yml` for SSH, Cloudflare, Hetzner
- Runs bootstrap before any deploy
- If SSH fails: uses password to push key back

**Adam (Heat Lagos / Business)**
- Uses `vault.yml` for API keys (bsport, SerpAPI, etc.)
- Checks API health on startup
- Stores results in `memory/bootstrap_log.json`

**Sarah (Yoga/Content)**
- Uses `vault.yml` for Cloudflare Pages, Google APIs
- Verifies website deployments reachable
- Checks Facebook API status (frequent breakage)

## Quick Commands

```bash
# Check everything
python3 scripts/access_bootstrap.py

# Check + auto-fix
python3 scripts/access_bootstrap.py --fix

# Just report
python3 scripts/access_bootstrap.py --report

# Read credentials
python3 -c "import yaml; print(yaml.safe_load(open('.secrets/vault.yml'))['hetzner_server_ip'])"
```

## Deployment

**On Hetzner (server-side):**
```bash
# Copy bootstrap there too
scp scripts/access_bootstrap.py root@178.105.198.32:/opt/reddragon/

# Server can self-heal from inside
ssh root@178.105.198.32 "python3 /opt/reddragon/access_bootstrap.py --fix"
```

**Cron (optional):**
Run every 6 hours to catch issues early.

## Recovery Playbook

**SSH key broken:**
```bash
# From any machine with the password:
sshpass -p '=*bVQJ-9AKJE' ssh -o StrictHostKeyChecking=no root@178.105.198.32 \
  "echo 'YOUR_PUB_KEY' > ~/.ssh/authorized_keys"
```

**Cloudflare token expired:**
1. Log into dash.cloudflare.com
2. Go to My Profile → API Tokens
3. Create new token with: Zone:Read, DNS:Edit, Pages:Edit
4. Update `vault.yml`
5. Test: `curl -H "Authorization: Bearer NEW_TOKEN" https://api.cloudflare.com/client/v4/user/tokens/verify`

**Evennia down:**
```bash
ssh -i ~/.ssh/reddragon_hetzner_new root@178.105.198.32
cd /opt/reddragon/reddragon
evennia start
evennia reload  # if running but broken
```

## Bot Bootstrap Snippet

Every agent should include this pattern:

```python
# In agent startup / first message handler
import subprocess
import os

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
BOOTSTRAP = os.path.join(WORKSPACE, "scripts", "access_bootstrap.py")
VAULT = os.path.join(WORKSPACE, ".secrets", "vault.yml")

def bootstrap_access():
    """Run self-healing check, return status."""
    if os.path.exists(BOOTSTRAP):
        result = subprocess.run(
            ["python3", BOOTSTRAP, "--fix"],
            capture_output=True, text=True, timeout=60
        )
        return result.returncode == 0, result.stdout
    return False, "Bootstrap script not found"

# Call on startup
ok, output = bootstrap_access()
if not ok:
    print(f"[WARN] Infrastructure issues: {output}")
```

## Memory
- Bootstrap log: `memory/bootstrap_log.json`
- Last check timestamp: read from log
- Failures are logged with timestamps for pattern detection
