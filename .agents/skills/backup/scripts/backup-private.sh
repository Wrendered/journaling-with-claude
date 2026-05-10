#!/bin/bash
# Backup private/ to the configured destination
#
# Usage:
#   ./backup-private.sh           # Regular backup
#   ./backup-private.sh --encrypt # Encrypted backup (prompts for password)
#
# Backups stored in: ~/Dropbox/backups/journaling-with-claude/

set -e

# Config (defaults, can override in private/backup-config.sh)
REPO_DIR="$(cd "$(dirname "$0")/../../../.." && pwd)"
BACKUP_DIR="$HOME/Dropbox/backups/journaling-with-claude"
KEEP_BACKUPS=10

# Load private config if exists (overrides BACKUP_DIR, KEEP_BACKUPS)
if [[ -f "$REPO_DIR/private/backup-config.sh" ]]; then
    source "$REPO_DIR/private/backup-config.sh"
fi

TIMESTAMP=$(date '+%Y-%m-%d_%H%M%S')
BACKUP_NAME="journaling-with-claude_${TIMESTAMP}.zip"

# Parse args
ENCRYPT=false
if [[ "$1" == "--encrypt" ]]; then
    ENCRYPT=true
fi

# Create backup directory if needed
mkdir -p "$BACKUP_DIR"

# Verify backup directory is writable
if [[ ! -w "$BACKUP_DIR" ]]; then
    echo "Error: $BACKUP_DIR is not writable" >&2
    exit 1
fi

# Create temp directory for staging
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Copy files to stage, excluding generated/cached folders and import/
# Excluded: import/ (top-level), .git (local repo), .venv (Python venvs anywhere),
#           __pycache__, .ipynb_checkpoints, .DS_Store, *.pyc, .env
echo "Staging files..."
if [[ -d "$REPO_DIR/private" ]]; then
    mkdir -p "$TEMP_DIR/private"
    rsync -a \
        --exclude='import' \
        --exclude='.git' \
        --exclude='.venv' \
        --exclude='__pycache__' \
        --exclude='.ipynb_checkpoints' \
        --exclude='.DS_Store' \
        --exclude='*.pyc' \
        --exclude='.env' \
        "$REPO_DIR/private/" "$TEMP_DIR/private/"
else
    echo "Note: private/ not found"
fi

# Check we have something to backup
if [[ ! -d "$TEMP_DIR/private" ]]; then
    echo "Error: Nothing to backup"
    exit 1
fi

# Create zip
echo "Creating backup..."
cd "$TEMP_DIR"

if [[ "$ENCRYPT" == true ]]; then
    echo "Encrypting backup (you'll be prompted for password)..."
    zip -r -e "$BACKUP_DIR/$BACKUP_NAME" . -x "*.DS_Store"
else
    zip -r "$BACKUP_DIR/$BACKUP_NAME" . -x "*.DS_Store"
fi

# Prune old backups (keep last N)
echo "Pruning old backups (keeping last $KEEP_BACKUPS)..."
cd "$BACKUP_DIR"
ls -t journaling-with-claude_*.zip 2>/dev/null | tail -n +$((KEEP_BACKUPS + 1)) | xargs rm -f 2>/dev/null || true

# Report
BACKUP_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_NAME" | cut -f1)
BACKUP_COUNT=$(ls -1 "$BACKUP_DIR"/journaling-with-claude_*.zip 2>/dev/null | wc -l | tr -d ' ')

echo ""
echo "Backup complete:"
echo "  File: $BACKUP_DIR/$BACKUP_NAME"
echo "  Size: $BACKUP_SIZE"
echo "  Total backups: $BACKUP_COUNT"
