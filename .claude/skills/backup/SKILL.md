---
name: backup
description: Runs the configured backup script (.claude/skills/backup/scripts/backup-private.sh) to create a timestamped zip of private/ data in the user's chosen location. Supports an --encrypt flag for password-protected backups.
when_to_use: |
  ALWAYS invoke this skill when the user wants to run a backup right now.
  Trigger phrases (any of these): "back up my data", "run a backup", "save my journal",
  "preserve my private data", "back up to Dropbox", "manual backup".
  Also invoke automatically near the end of the weekly-review skill (after journal organization),
  or before any major restructuring of private/ files.
  For first-time configuration use the `setup-backups` skill instead.
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

If backup hasn't been configured yet, invoke the `setup-backups` skill to:
1. Choose backup location (Dropbox, iCloud, local)
2. Create config file
3. Test the backup

## When to Backup

- Automatically near the end of the `weekly-review` skill
- Manually anytime with the commands above
- Before major changes to journal structure
