---
name: setup-backups
description: Configure a personal backup destination and verify a first snapshot without pruning existing archives.
---

# Setup Backups

Read [the shared memory contract](../../../docs/memory-contract.md) before the first capture, state update, or import in a session. Use AGENTS.md for privacy, attribution, and current-context precedence.

1. Read current configuration and personal backup notes. Reuse an already-authorized active location; never resume writing into a frozen archive.
2. If no destination is known, ask where backups should live. A folder synced by another service may leave this machine; describe the location accurately.
3. Write private/backup-config.sh using templates/backup-config.template.sh and the chosen path. Preserve older backups and do not configure retention deletion.
4. Run the backup skill, verify the manifest, and restore into an empty temporary directory as a rehearsal. Record the successful path and date in personal operating notes.
5. Do not add a recurring automation unless the user requested scheduling. Do not add Git remotes, commit private data, or promise offsite upload from local verification.
