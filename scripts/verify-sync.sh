#!/bin/bash
# verify-sync.sh — pre-commit guard that fails if .codex/ generated files are out of sync
#                   with the .claude/ source-of-truth.
#
# What it checks (only the files that sync-codex.sh actually generates):
#   .codex/hooks.json
#   .codex/agents/*.toml
#
# What it doesn't check:
#   .codex/config.toml      — Codex-specific config, hand-maintained
#   .codex/hooks/           — symlink, not regenerated
#   anything else under .codex/
#
# Bidirectional check: catches both modified files AND stale generated files
# (e.g. .codex/agents/foo.toml left over after .claude/agents/foo.md was deleted).
#
# Wire into pre-commit:
#   echo 'bash scripts/verify-sync.sh' >> .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit

set -euo pipefail

REPO_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_DIR"

# Snapshot the current generated files before sync mutates them.
TEMP=$(mktemp -d)
trap "rm -rf $TEMP" EXIT

mkdir -p "$TEMP/committed" "$TEMP/regenerated"

# Snapshot committed state of generated files (skip symlinks and non-generated stuff)
[[ -f .codex/hooks.json ]]       && cp .codex/hooks.json       "$TEMP/committed/hooks.json"
[[ -d .codex/agents ]] && for f in .codex/agents/*.toml; do
  [[ -f "$f" ]] && cp "$f" "$TEMP/committed/$(basename "$f")"
done

# Run sync (mutates working tree)
bash scripts/sync-codex.sh >/dev/null

# Snapshot regenerated state
[[ -f .codex/hooks.json ]]       && cp .codex/hooks.json       "$TEMP/regenerated/hooks.json"
[[ -d .codex/agents ]] && for f in .codex/agents/*.toml; do
  [[ -f "$f" ]] && cp "$f" "$TEMP/regenerated/$(basename "$f")"
done

# Restore committed state to working tree (verification must not leave dirty files)
[[ -f "$TEMP/committed/hooks.json" ]] && cp "$TEMP/committed/hooks.json" .codex/hooks.json
for f in "$TEMP/committed"/*.toml; do
  [[ -f "$f" ]] && cp "$f" ".codex/agents/$(basename "$f")"
done
# Stale-on-disk: if working tree had a .toml that committed snapshot doesn't have,
# that's an in-progress addition the user is making. Leave it. (The drift check below
# will flag it as "missing from committed" which is the user's signal to commit it.)

# Bidirectional comparison
DRIFT=0
DRIFT_OUTPUT=$(diff -r --brief "$TEMP/committed" "$TEMP/regenerated" 2>&1 || true)

if [[ -n "$DRIFT_OUTPUT" ]]; then
  echo "$DRIFT_OUTPUT" | while IFS= read -r line; do
    case "$line" in
      "Files "*" differ"*)
        rel=$(echo "$line" | sed -E "s|^Files [^ ]+/(.+) and [^ ]+/.+ differ$|\1|")
        echo "DRIFT (modified): .codex/.../$rel — sync-codex.sh would change it"
        ;;
      "Only in $TEMP/committed"*)
        name=$(echo "$line" | sed -E "s|^Only in [^:]+: (.*)$|\1|")
        echo "DRIFT (stale, should be deleted): .codex/.../$name"
        ;;
      "Only in $TEMP/regenerated"*)
        name=$(echo "$line" | sed -E "s|^Only in [^:]+: (.*)$|\1|")
        echo "DRIFT (missing, sync would create): .codex/.../$name"
        ;;
    esac
  done
  DRIFT=1
fi

if [[ $DRIFT -eq 1 ]]; then
  echo
  echo "❌ .codex/ is out of sync with .claude/ source-of-truth."
  echo "   Run: bash scripts/sync-codex.sh"
  echo "   Then 'git add .codex/' and commit."
  echo "   For stale files (deleted Claude source), 'git rm .codex/<path>' then commit."
  exit 1
fi

echo "✓ .codex/ generated files are in sync with .claude/"
