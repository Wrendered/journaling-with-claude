---
name: backup
description: Run backups of private journal data to configured location. Use when user mentions backup, saving data, preserving journals, or during weekly review.
allowed-tools: Read, Bash
---

# Backup Private Data

Run the backup script to create a timestamped archive of private data.

## Quick Backup

```bash
.claude/skills/backup/scripts/backup-private.sh
```

## Encrypted Backup

For password-protected backup:

```bash
.claude/skills/backup/scripts/backup-private.sh --encrypt
```

## What Gets Backed Up

- `private/` folder (excluding `import/`)
- `CLAUDE.md`

Backups are timestamped zips. Last 10 kept, older pruned automatically.

## Check Configuration

Read the config to find backup location:

```bash
cat private/backup-config.sh
```

## List Existing Backups

After reading config for BACKUP_DIR:

```bash
ls -la [BACKUP_DIR]
```

## First-Time Setup

If backup hasn't been configured yet, run `/setup-backups` command to:
1. Choose backup location (Dropbox, iCloud, local)
2. Create config file
3. Test the backup

## When to Backup

- Automatically during `/weekly-review`
- Manually anytime with the commands above
- Before major changes to journal structure
