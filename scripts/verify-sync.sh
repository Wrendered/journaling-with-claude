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

# Save current state
TEMP=$(mktemp -d)
trap "rm -rf $TEMP" EXIT

# Copy committed .codex/ to temp for comparison baseline
cp -R .codex "$TEMP/before"

# Run sync-codex.sh, then diff
bash scripts/sync-codex.sh >/dev/null

# Compare
DRIFT=0
for f in .codex/hooks.json .codex/agents/*.toml; do
  [[ -f "$f" ]] || continue
  baseline="$TEMP/before/${f#.codex/}"
  if [[ ! -f "$baseline" ]] || ! diff -q "$baseline" "$f" >/dev/null 2>&1; then
    echo "DRIFT: $f differs from sync output"
    DRIFT=1
  fi
done

if [[ $DRIFT -eq 1 ]]; then
  echo
  echo "❌ .codex/ is out of sync with .claude/ source-of-truth."
  echo "   Run: bash scripts/sync-codex.sh"
  echo "   Then commit the regenerated files."
  exit 1
fi

echo "✓ .codex/ is in sync with .claude/"
