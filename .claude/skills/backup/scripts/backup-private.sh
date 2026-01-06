#!/bin/bash
# Backup private/ and CLAUDE.md to Dropbox
#
# Usage:
#   ./backup-private.sh           # Regular backup
#   ./backup-private.sh --encrypt # Encrypted backup (prompts for password)
#
# Backups stored in: ~/Dropbox/backups/personal-assistant/

set -e

# Config (defaults, can override in private/backup-config.sh)
REPO_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
BACKUP_DIR="$HOME/Dropbox/backups/personal-assistant"
KEEP_BACKUPS=10

# Load private config if exists (overrides BACKUP_DIR, KEEP_BACKUPS)
if [[ -f "$REPO_DIR/private/backup-config.sh" ]]; then
    source "$REPO_DIR/private/backup-config.sh"
fi

TIMESTAMP=$(date '+%Y-%m-%d_%H%M%S')
BACKUP_NAME="personal-assistant_${TIMESTAMP}.zip"

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

# Copy files to stage (excluding import/)
echo "Staging files..."
if [[ -d "$REPO_DIR/private" ]]; then
    mkdir -p "$TEMP_DIR/private"
    for item in "$REPO_DIR/private"/*; do
        item_name=$(basename "$item")
        if [[ "$item_name" != "import" ]]; then
            cp -r "$item" "$TEMP_DIR/private/"
        fi
    done
else
    echo "Note: private/ not found"
fi
cp "$REPO_DIR/CLAUDE.md" "$TEMP_DIR/" 2>/dev/null || echo "Note: CLAUDE.md not found"

# Check we have something to backup
if [[ ! -d "$TEMP_DIR/private" && ! -f "$TEMP_DIR/CLAUDE.md" ]]; then
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
ls -t personal-assistant_*.zip 2>/dev/null | tail -n +$((KEEP_BACKUPS + 1)) | xargs rm -f 2>/dev/null || true

# Report
BACKUP_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_NAME" | cut -f1)
BACKUP_COUNT=$(ls -1 "$BACKUP_DIR"/personal-assistant_*.zip 2>/dev/null | wc -l | tr -d ' ')

echo ""
echo "Backup complete:"
echo "  File: $BACKUP_DIR/$BACKUP_NAME"
echo "  Size: $BACKUP_SIZE"
echo "  Total backups: $BACKUP_COUNT"
