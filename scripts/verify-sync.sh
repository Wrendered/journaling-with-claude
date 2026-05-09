#!/bin/bash
# verify-sync.sh — pre-commit guard that fails if .codex/ is out of sync with .claude/
#
# Runs sync-codex.sh into a temp directory, diffs against committed .codex/ files,
# exits non-zero on drift.
#
# Wire into pre-commit:
#   echo 'bash scripts/verify-sync.sh' >> .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
#
# Or wire into CI as a step.

set -euo pipefail

REPO_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_DIR"

# Save the current committed .codex/ state, run sync, diff, then RESTORE.
# This way the working tree is never dirtied by the verification, even on drift.
TEMP=$(mktemp -d)
trap "rm -rf $TEMP" EXIT

# Snapshot committed state
cp -R .codex "$TEMP/committed"

# Run sync (this mutates .codex/ in-place — necessary because sync-codex.sh
# writes to .codex/ paths directly)
bash scripts/sync-codex.sh >/dev/null

# Snapshot regenerated state
cp -R .codex "$TEMP/regenerated"

# Restore committed state to working tree (verification must not leave dirty files)
rm -rf .codex
cp -R "$TEMP/committed" .codex

# Compare committed vs regenerated
DRIFT=0
while IFS= read -r f; do
  rel="${f#$TEMP/regenerated/}"
  committed_file="$TEMP/committed/$rel"
  if [[ ! -f "$committed_file" ]] || ! diff -q "$committed_file" "$f" >/dev/null 2>&1; then
    echo "DRIFT: .codex/$rel differs from sync output"
    DRIFT=1
  fi
done < <(find "$TEMP/regenerated" -type f)

if [[ $DRIFT -eq 1 ]]; then
  echo
  echo "❌ .codex/ is out of sync with .claude/ source-of-truth."
  echo "   Run: bash scripts/sync-codex.sh"
  echo "   Then commit the regenerated files."
  exit 1
fi

echo "✓ .codex/ is in sync with .claude/"
