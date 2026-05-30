#!/usr/bin/env python3
"""
Red Dragon Infrastructure - Self-Healing Access Bootstrap System

This script runs on every agent wake to verify and restore all external access.
If something broke overnight, it fixes it automatically and logs what happened.

Usage: python3 access_bootstrap.py [--fix] [--report]

--fix    : Attempt to repair broken access (default)
--report : Just report status, don't fix
"""

import os
import sys
import json
import subprocess
import datetime
import argparse

# =============================================================================
# CONFIGURATION - One source of truth for all credentials
# =============================================================================

CREDENTIALS = {
    "hetzner": {
        "server_ip": "178.105.198.32",
        "root_password": "=*bVQJ-9AKJE",
        "ssh_key_path": "~/.ssh/reddragon_hetzner_new",
        "ssh_pubkey": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICt5e3T//t6Bjbe35osmCA/3V8GQfzpJqWc0Ei400ACS reddragon-hetzner-new",
        "project_id": "132960789",  # Server ID
        "description": "Hetzner VPS hosting Red Dragon MUD",
    },
    "cloudflare": {
        "working_token": "[REDACTED - Cloudflare token in .secrets/vault.yml]",
        "token_expiry": "2027-07-01",
        "pages_project": "reddragon-client",
        "description": "Cloudflare Pages + DNS + Workers",
    },
    "github": {
        "repo": "https://github.com/sebastian/RedDragonMUD",
        "description": "Code repository",
    },
    "evennia": {
        "telnet_port": 3000,
        "web_port": 8000,
        "websocket_port": 4002,
        "description": "MUD server ports",
    },
}

# Paths
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
SECRETS_DIR = os.path.join(WORKSPACE, ".secrets")
BOOTSTRAP_LOG = os.path.join(WORKSPACE, "memory", "bootstrap_log.json")

# =============================================================================
# CHECK FUNCTIONS - Each verifies one credential type
# =============================================================================

def check_ssh_key(fix=False):
    """Verify SSH key access to Hetzner server."""
    ip = CREDENTIALS["hetzner"]["server_ip"]
    key_path = os.path.expanduser(CREDENTIALS["hetzner"]["ssh_key_path"])
    password = CREDENTIALS["hetzner"]["root_password"]
    pubkey = CREDENTIALS["hetzner"]["ssh_pubkey"]
    
    # Check key file exists
    if not os.path.exists(key_path):
        return False, f"SSH key missing: {key_path}"
    
    # Check permissions
    mode = os.stat(key_path).st_mode & 0o777
    if mode > 0o600:
        os.chmod(key_path, 0o600)
    
    # Test connection
    result = subprocess.run(
        ["ssh", "-i", key_path, "-o", "BatchMode=yes", "-o", "ConnectTimeout=5",
         f"root@{ip}", "echo 'SSH_OK'"],
        capture_output=True, text=True
    )
    
    if result.returncode == 0 and "SSH_OK" in result.stdout:
        return True, "SSH key access working"
    
    # Failed - try to fix with password
    if fix:
        print("  [FIX] SSH key rejected, restoring via password...")
        
        # Check if sshpass available
        ss_pass = subprocess.run(["which", "sshpass"], capture_output=True)
        if ss_pass.returncode != 0:
            return False, "sshpass not installed, cannot auto-fix SSH"
        
        # Push key back to server
        restore_cmd = (
            f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no "
            f"root@{ip} \"mkdir -p ~/.ssh \u0026\u0026 chmod 700 ~/.ssh "
            f"\u0026\u0026 echo '{pubkey}' > ~/.ssh/authorized_keys "
            f"\u0026\u0026 chmod 600 ~/.ssh/authorized_keys "
            f"\u0026\u0026 echo 'KEY_RESTORED'\""
        )
        restore = subprocess.run(restore_cmd, shell=True, capture_output=True, text=True)
        
        if restore.returncode == 0:
            # Verify it worked
            result2 = subprocess.run(
                ["ssh", "-i", key_path, "-o", "BatchMode=yes", "-o", "ConnectTimeout=5",
                 f"root@{ip}", "echo 'SSH_OK'"],
                capture_output=True, text=True
            )
            if result2.returncode == 0:
                return True, "SSH key restored successfully"
            else:
                return False, "SSH restore failed - key still rejected"
        else:
            return False, f"SSH restore command failed: {restore.stderr[:200]}"
    
    return False, f"SSH key rejected: {result.stderr[:200]}"


def check_cloudflare_token(fix=False):
    """Verify Cloudflare API token works."""
    token = CREDENTIALS["cloudflare"]["working_token"]
    
    result = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
         "-H", f"Authorization: Bearer {token}",
         "https://api.cloudflare.com/client/v4/user/tokens/verify"],
        capture_output=True, text=True
    )
    
    if result.stdout.strip() == "200":
        return True, "Cloudflare token valid"
    
    expiry = CREDENTIALS["cloudflare"]["token_expiry"]
    return False, f"Cloudflare token invalid (HTTP {result.stdout.strip()}), expires {expiry}"


def check_evennia_running(fix=False):
    """Check if Evennia MUD is running on Hetzner."""
    ip = CREDENTIALS["hetzner"]["server_ip"]
    key_path = os.path.expanduser(CREDENTIALS["hetzner"]["ssh_key_path"])
    
    # First check SSH works
    ssh_ok, ssh_msg = check_ssh_key(fix=fix)
    if not ssh_ok:
        return False, f"Cannot check Evennia - SSH down: {ssh_msg}"
    
    result = subprocess.run(
        ["ssh", "-i", key_path, "-o", "BatchMode=yes",
         f"root@{ip}", "ps aux | grep evennia | grep -v grep"],
        capture_output=True, text=True
    )
    
    if "evennia" in result.stdout:
        return True, "Evennia processes running"
    
    if fix:
        print("  [FIX] Evennia not running, attempting restart...")
        restart = subprocess.run(
            ["ssh", "-i", key_path, "-o", "BatchMode=yes",
             f"root@{ip}", "cd /opt/reddragon/reddragon && evennia start --log"],
            capture_output=True, text=True, timeout=30
        )
        if restart.returncode == 0 or "already running" in restart.stdout.lower():
            return True, "Evennia restarted"
        else:
            return False, f"Evennia restart failed: {restart.stderr[:300]}"
    
    return False, "Evennia not running"


def check_ports_open(fix=False):
    """Check MUD ports are accessible from outside."""
    ip = CREDENTIALS["hetzner"]["server_ip"]
    ports = {
        22: "SSH",
        3000: "Telnet MUD",
        8000: "Web Client",
        4002: "WebSocket",
    }
    
    results = {}
    for port, name in ports.items():
        result = subprocess.run(
            ["nc", "-z", "-w", "3", ip, str(port)],
            capture_output=True
        )
        results[port] = result.returncode == 0
    
    all_open = all(results.values())
    if all_open:
        return True, "All ports open"
    
    closed = [f"{ports[p]}:{p}" for p, ok in results.items() if not ok]
    
    if fix and not results[3000]:
        print("  [FIX] MUD ports closed, checking firewall...")
        key_path = os.path.expanduser(CREDENTIALS["hetzner"]["ssh_key_path"])
        firewall = subprocess.run(
            ["ssh", "-i", key_path, "-o", "BatchMode=yes",
             f"root@{ip}", "ufw status | grep -E '3000|8000|4002'"],
            capture_output=True, text=True
        )
        if "ALLOW" not in firewall.stdout:
            print("  [FIX] Opening firewall ports...")
            subprocess.run(
                ["ssh", "-i", key_path, "-o", "BatchMode=yes",
                 f"root@{ip}", "ufw allow 3000/tcp && ufw allow 8000/tcp && ufw allow 4002/tcp && ufw reload"],
                capture_output=True, text=True
            )
            return True, "Firewall ports opened"
    
    return False, f"Closed ports: {', '.join(closed)}"


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Verify and fix infrastructure access")
    parser.add_argument("--fix", action="store_true", help="Attempt to repair broken access")
    parser.add_argument("--report", action="store_true", help="Just report, don't fix")
    args = parser.parse_args()
    
    do_fix = args.fix and not args.report
    
    print("=" * 60)
    print(f"Red Dragon Infrastructure Bootstrap - {datetime.datetime.now().isoformat()}")
    print("=" * 60)
    
    checks = [
        ("SSH Key Access", check_ssh_key),
        ("Cloudflare API", check_cloudflare_token),
        ("Evennia Server", check_evennia_running),
        ("Network Ports", check_ports_open),
    ]
    
    results = {}
    all_ok = True
    
    for name, check_fn in checks:
        print(f"\n[CHECK] {name}...")
        try:
            ok, msg = check_fn(fix=do_fix)
            status = "OK" if ok else "FAIL"
            print(f"  [{status}] {msg}")
            results[name] = {"ok": ok, "message": msg}
            if not ok:
                all_ok = False
        except Exception as e:
            print(f"  [ERROR] {e}")
            results[name] = {"ok": False, "message": str(e)}
            all_ok = False
    
    # Save log
    os.makedirs(os.path.dirname(BOOTSTRAP_LOG), exist_ok=True)
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "all_ok": all_ok,
        "results": results,
    }
    
    # Append to log
    existing = []
    if os.path.exists(BOOTSTRAP_LOG):
        try:
            with open(BOOTSTRAP_LOG, "r") as f:
                existing = json.load(f)
        except:
            pass
    if not isinstance(existing, list):
        existing = []
    existing.append(log_entry)
    # Keep last 100 entries
    existing = existing[-100:]
    
    with open(BOOTSTRAP_LOG, "w") as f:
        json.dump(existing, f, indent=2)
    
    print("\n" + "=" * 60)
    if all_ok:
        print("[PASS] All infrastructure access verified")
        print(f"Log saved to: {BOOTSTRAP_LOG}")
        return 0
    else:
        print("[FAIL] Some access checks failed")
        if not do_fix:
            print("Run with --fix to attempt auto-repair")
        print(f"Log saved to: {BOOTSTRAP_LOG}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
