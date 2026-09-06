#!/usr/bin/env bash
# Preserve existing hooks; never silently replace another hook system.
set -euo pipefail
REPO_DIR="$(git rev-parse --show-toplevel)"
cd "$REPO_DIR"
CURRENT_HOOKS="$(git config --get core.hooksPath || true)"
if [[ -n "$CURRENT_HOOKS" && "$CURRENT_HOOKS" != '.githooks' ]]; then
  echo "Existing hooksPath retained: $CURRENT_HOOKS"
  echo 'Add python3 scripts/check_staged.py and bash scripts/verify-sync.sh to your existing pre-commit workflow.'
  exit 1
fi
DEFAULT_PRECOMMIT="$(git rev-parse --git-path hooks/pre-commit)"
if [[ -z "$CURRENT_HOOKS" && -f "$DEFAULT_PRECOMMIT" ]]; then
  echo 'Existing pre-commit retained. Integrate the staged privacy and sync checks before switching hooksPath.'
  exit 1
fi
git config core.hooksPath .githooks
echo 'Installed repository Git hooks.'
