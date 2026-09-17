#!/usr/bin/env bash
# Verified backups with originals and import staging; never prune old archives.
set -euo pipefail
REPO_DIR="$(cd "$(dirname "$0")/../../../.." && pwd)"
BACKUP_DIR="$HOME/Dropbox/backups/journaling-with-claude"
if [[ -f "$REPO_DIR/private/backup-config.sh" ]]; then
  source "$REPO_DIR/private/backup-config.sh"
fi
if [[ $# -eq 0 ]]; then
  exec python3 "$REPO_DIR/scripts/vault.py" backup --destination "$BACKUP_DIR"
fi
if [[ "$1" != '--encrypt' || $# -ne 1 ]]; then
  echo 'Usage: backup-private.sh [--encrypt]' >&2
  exit 1
fi
if [[ ! -t 0 ]]; then
  echo 'Encrypted backups require an interactive terminal for password entry.' >&2
  exit 1
fi
STAGING_DIR="$(mktemp -d)"
trap 'rm -rf "$STAGING_DIR"' EXIT
python3 "$REPO_DIR/scripts/vault.py" backup --destination "$STAGING_DIR" > "$STAGING_DIR/result.json"
ARCHIVE_PATH="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["archive"])' "$STAGING_DIR/result.json")"
python3 "$REPO_DIR/scripts/vault.py" verify-backup "$ARCHIVE_PATH" --restore-to "$STAGING_DIR/restored"
python3 - "$ARCHIVE_PATH" "$STAGING_DIR/restored/BACKUP-MANIFEST.json" <<'PY'
import sys, zipfile
from pathlib import Path
with zipfile.ZipFile(sys.argv[1]) as archive:
    Path(sys.argv[2]).write_bytes(archive.read('BACKUP-MANIFEST.json'))
PY
mkdir -p "$BACKUP_DIR"
ENCRYPTED_PATH="$BACKUP_DIR/$(basename "$ARCHIVE_PATH" .zip)_encrypted.zip"
cd "$STAGING_DIR/restored"
echo 'ZIP encryption uses legacy ZipCrypto. Enter the password in this terminal.'
zip -q -r -e "$ENCRYPTED_PATH" private BACKUP-MANIFEST.json
python3 "$REPO_DIR/scripts/vault.py" verify-backup "$ENCRYPTED_PATH" --password-prompt
printf 'Verified encrypted backup: %s\n' "$ENCRYPTED_PATH"
