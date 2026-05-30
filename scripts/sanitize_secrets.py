#!/usr/bin/env python3
"""
Sanitize secrets from tracked files before Git commit.
Replaces token values with [REDACTED] placeholders.
"""

import re
import sys
from pathlib import Path

# Token patterns to redact
TOKEN_PATTERNS = [
    (r'cfut_[A-Za-z0-9]{40,}', '[REDACTED - Cloudflare token in .secrets/vault.yml]'),
    (r'ghp_[A-Za-z0-9]{36,}', '[REDACTED - GitHub PAT in .secrets/vault.yml]'),
    (r'gho_[A-Za-z0-9]{36,}', '[REDACTED - GitHub OAuth token in .secrets/vault.yml]'),
    (r'\bAKIA[A-Z0-9]{16,}\b', '[REDACTED - AWS key]'),
]

FILES_TO_SANITIZE = [
    'MEMORY.md',
    'TOOLS.md',
    'USER.md',
    'scripts/access_bootstrap.py',
    'memory/2026-05-16.md',
    'memory/2026-05-21.md',
    'memory/2026-05-28.md',
    'memory/2026-05-29.md',
    'memory/.dreams/events.jsonl',
]

def sanitize_file(filepath):
    """Replace secrets in a file."""
    path = Path(filepath)
    if not path.exists():
        print(f"SKIP: {filepath} (not found)")
        return 0
    
    content = path.read_text(encoding='utf-8', errors='replace')
    original = content
    replacements = 0
    
    for pattern, replacement in TOKEN_PATTERNS:
        matches = list(re.finditer(pattern, content))
        if matches:
            content = re.sub(pattern, replacement, content)
            replacements += len(matches)
    
    if content != original:
        path.write_text(content, encoding='utf-8')
        print(f"CLEANED: {filepath} ({replacements} secret(s) redacted)")
    else:
        print(f"CLEAN: {filepath} (no secrets found)")
    
    return replacements

def main():
    total = 0
    for filepath in FILES_TO_SANITIZE:
        total += sanitize_file(filepath)
    
    print(f"\nTotal secrets redacted: {total}")
    return 0 if total > 0 else 0

if __name__ == '__main__':
    sys.exit(main())
