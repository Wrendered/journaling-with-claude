---
name: backup
description: Create a verified, non-pruning backup of the private vault and optionally test restoration.
---

# Backup

Read [the shared memory contract](../../../docs/memory-contract.md) before the first capture, state update, or import in a session. Use AGENTS.md for privacy, attribution, and current-context precedence.

1. Read private/backup-config.sh and personal backup notes. Use the configured destination, preserving any explicit frozen-archive decision. If none is configured, ask for a destination or use setup-backups.
2. Run bash .agents/skills/backup/scripts/backup-private.sh. The shared vault tool snapshots originals, imports, wiki, and state under a lock, includes a hash manifest, and verifies the archive. It excludes caches, generated views, secrets files, and Git internals. It never prunes previous backups.
3. A directory named Dropbox or iCloud is a configured backup location; do not claim cloud upload completion from a local write.
4. For a restore rehearsal, use scripts/vault.py verify-backup ARCHIVE --restore-to EMPTY_DIR. The restored vault is EMPTY_DIR/private. Never restore over the live vault.
5. Report the path, verification result, and any exclusions relevant to the request. Encryption uses the wrapper’s --encrypt option in an interactive terminal; never put a password in a command, chat, or log. Do not commit private files.
