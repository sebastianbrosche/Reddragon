#!/bin/bash
#
# Miha Backup Script - Backs up Red Dragon MUD to Google Drive
# Triggered by "good night" or manual execution
#

BACKUP_DIR="/tmp/miha_backup"
GDRIVE_FOLDER="KIMIMIHA"
PROJECT_DIR="/root/.openclaw/workspace/reddragon"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="miha_backup_${TIMESTAMP}.tar.gz"

echo "=== Miha Backup System ==="
echo "Timestamp: $(date)"
echo "Project: ${PROJECT_DIR}"
echo "Target: Google Drive /${GDRIVE_FOLDER}/${BACKUP_NAME}"
echo ""

# Check if rclone is configured
if ! rclone listremotes 2>/dev/null | grep -q "gdrive"; then
    echo "ERROR: Google Drive not configured."
    echo "Run: rclone config (choose Google Drive, name it 'gdrive')"
    echo "Or use the web auth: rclone authorize 'drive'"
    exit 1
fi

# Create backup directory
mkdir -p "${BACKUP_DIR}"

# Package the project
echo "[1/4] Packaging Red Dragon MUD..."
tar czf "${BACKUP_DIR}/${BACKUP_NAME}" \
    -C "$(dirname ${PROJECT_DIR})" \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    --exclude='evennia.db3' \
    --exclude='server/logs' \
    --exclude='server/.static' \
    --exclude='*.pid' \
    --exclude='*.log' \
    "$(basename ${PROJECT_DIR})"

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create backup archive"
    exit 1
fi

echo "[2/4] Archive created: ${BACKUP_NAME}"
echo "[3/4] Size: $(du -h ${BACKUP_DIR}/${BACKUP_NAME} | cut -f1)"

# Ensure KIMIMIHA folder exists and upload
echo "[4/4] Uploading to Google Drive..."
rclone mkdir "gdrive:${GDRIVE_FOLDER}" 2>/dev/null

rclone copy "${BACKUP_DIR}/${BACKUP_NAME}" "gdrive:${GDRIVE_FOLDER}/" \
    --progress \
    --drive-keep-revision-forever=false

if [ $? -eq 0 ]; then
    echo ""
    echo "=== BACKUP COMPLETE ==="
    echo "File: ${BACKUP_NAME}"
    echo "Location: Google Drive /${GDRIVE_FOLDER}/"
    echo "Time: $(date)"
    echo "========================"
    
    # Clean up old local backups (keep last 5)
    ls -t ${BACKUP_DIR}/miha_backup_*.tar.gz 2>/dev/null | tail -n +6 | xargs rm -f 2>/dev/null
    
    # Clean up old Google Drive backups (keep last 10)
    rclone delete "gdrive:${GDRIVE_FOLDER}" --drive-trashed-only --drive-use-trash=false 2>/dev/null
    OLD_BACKUPS=$(rclone ls "gdrive:${GDRIVE_FOLDER}" 2>/dev/null | grep "miha_backup_" | sort -r | tail -n +11 | awk '{print $2}')
    for old in $OLD_BACKUPS; do
        rclone delete "gdrive:${GDRIVE_FOLDER}/${old}" 2>/dev/null
    done
    
    exit 0
else
    echo "ERROR: Upload failed"
    exit 1
fi
