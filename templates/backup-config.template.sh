# Private backup configuration
# Copy to private/backup-config.sh and customize
#
# NOTE: This file goes in private/ and will NOT be committed to git.
# Backups include: private/ (except import/) and CLAUDE.md

# Where to store backups (must exist and be writable)
BACKUP_DIR="$HOME/Dropbox/backups/journaling"

# How many backups to keep (older ones pruned automatically)
KEEP_BACKUPS=10
