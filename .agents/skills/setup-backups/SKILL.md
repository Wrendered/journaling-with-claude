---
name: setup-backups
description: One-time configuration of automatic backups of private/ data to Dropbox, iCloud, or a local path. Verifies the destination, creates private/backup-config.sh from the template, runs a test backup, and confirms success.
when_to_use: |
  ALWAYS invoke this skill when the user wants to configure backups for the first time.
  Trigger phrases (any of these): "set up backups", "configure backups", "how do I back up",
  "where do my journals go", "I want to preserve this data", "back up to Dropbox",
  "back up to iCloud".
  Do NOT invoke for routine backup runs — that's the `backup` skill.
allowed-tools: Read, Edit, Write, Bash
---

# Setup Backups

One-time setup for automatic backups of private data.

## What Gets Backed Up

- `private/` folder (excluding `import/`)
- `AGENTS.md`

Backups are timestamped zips stored in your configured location. Last 10 kept, older pruned automatically.

## Setup Flow

### 0. Verify backup destination exists

Before setup, confirm your backup destination's parent directory exists:
- Dropbox: `ls ~/Dropbox` (should exist if Dropbox installed)
- iCloud: `ls ~/Library/Mobile\ Documents/com~apple~CloudDocs`
- Local: Any local path you choose

### 1. Check backup location

Ask user: "Where do you want backups stored?"

Default: `~/Dropbox/backups/personal-assistant/`

Other options:
- iCloud: `~/Library/Mobile Documents/com~apple~CloudDocs/backups/personal-assistant/`
- Local: `~/backups/personal-assistant/`
- Custom path

Verify the parent directory exists.

### 2. Create private config

Copy template to `private/backup-config.sh`:

```bash
cp templates/backup-config.template.sh private/backup-config.sh
```

Update BACKUP_DIR in the config to user's chosen location.

### 3. Create backup directory

```bash
mkdir -p [BACKUP_DIR]
```

### 4. Test the backup

Run the backup script to verify it works:

```bash
.claude/skills/backup/scripts/backup-private.sh
```

Confirm backup was created successfully.

### 5. Confirm setup

Show summary:
- Backup location
- Runs during weekly-review
- Manual: `.claude/skills/backup/scripts/backup-private.sh`
- Encrypted: `.claude/skills/backup/scripts/backup-private.sh --encrypt`

## Manual Backup

Anytime, run:

```bash
.claude/skills/backup/scripts/backup-private.sh           # Regular
.claude/skills/backup/scripts/backup-private.sh --encrypt # Password-protected
```

## Checking Backups

```bash
ls -la [BACKUP_DIR]
```

## Notes

- Backups exclude `private/import/` (one-time processing material)
- Encrypted backups prompt for password — don't forget it!
