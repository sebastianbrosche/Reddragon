#!/bin/bash
#
# Miha Backup Script - Backs up workspace to Git (originally Google Drive via rclone)
# Triggered by "good night" or manual execution
# Changed 2026-05-30: Switched from Google Drive to Git
#

PROJECT_DIR="/root/.openclaw/workspace"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
COMMIT_MSG="backup: ${TIMESTAMP}"

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=== Miha Git Backup System ==="
echo "Timestamp: $(date)"
echo "Project: ${PROJECT_DIR}"
echo "Target: Git remote origin"
echo ""

# Check if Git repo exists
cd "${PROJECT_DIR}"

if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}ERROR: Not a Git repository.${NC}"
    echo "Run: git init && git remote add origin <url>"
    exit 1
fi

# Check if remote is configured
REMOTE_URL=$(git remote get-url origin 2>/dev/null)
if [ -z "${REMOTE_URL}" ]; then
    echo -e "${RED}ERROR: No Git remote configured.${NC}"
    exit 1
fi

# Hide the token in output
SAFE_URL=$(echo "${REMOTE_URL}" | sed 's/https:\/\/[^@]*@/https:\/\/***@/')
echo "Remote: ${SAFE_URL}"
echo ""

# Check if there are any changes to commit
# - Staged changes
# - Unstaged changes
# - Untracked files (respecting .gitignore)
HAS_CHANGES=0

if ! git diff --cached --quiet 2>/dev/null; then
    HAS_CHANGES=1
    echo "[ ] Staged changes found"
fi

if ! git diff --quiet 2>/dev/null; then
    HAS_CHANGES=1
    echo "[ ] Unstaged changes found"
fi

if [ -n "$(git ls-files --others --exclude-standard)" ]; then
    HAS_CHANGES=1
    echo "[ ] New untracked files found"
fi

if [ ${HAS_CHANGES} -eq 0 ]; then
    echo -e "${GREEN}No changes to back up. Everything is up to date.${NC}"
    echo "=== BACKUP COMPLETE (no changes) ==="
    exit 0
fi

echo ""

echo "[1/4] Running secret sanitization..."
python3 /root/.openclaw/workspace/scripts/sanitize_secrets.py || true

# Stage all changes (respects .gitignore)
echo "[2/4] Staging changes..."
git add -A
STAGED_COUNT=$(git diff --cached --numstat | wc -l)
echo "    ${STAGED_COUNT} file(s) staged"

# Commit
echo "[3/4] Committing..."
git commit -m "${COMMIT_MSG}" --quiet

if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Git commit failed${NC}"
    exit 1
fi

COMMIT_HASH=$(git rev-parse --short HEAD)
echo "    Commit: ${COMMIT_HASH}"

# Push
echo "[4/4] Pushing to origin..."
BRANCH=$(git branch --show-current)
git push origin "${BRANCH}" --quiet

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}=== BACKUP COMPLETE ===${NC}"
    echo "Commit: ${COMMIT_HASH}"
    echo "Branch: ${BRANCH}"
    echo "Message: ${COMMIT_MSG}"
    echo "Time: $(date)"
    echo "========================"
    exit 0
else
    echo -e "${RED}ERROR: Git push failed${NC}"
    exit 1
fi
