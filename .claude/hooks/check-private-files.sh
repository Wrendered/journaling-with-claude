#!/bin/bash
# Security hook: Block private files (hard) + Review diff content (soft)
#
# PreToolUse: Block private/ or CLAUDE.md / AGENTS.override.md / CLAUDE.local.md paths (exit 2)
# PostToolUse: Inject diff to assistant for content review (additionalContext)
#
# Works in both Claude Code (sets $CLAUDE_PROJECT_DIR) and OpenAI Codex CLI
# (sets its own project root vars). Falls back to git rev-parse.

set -e

# Bail silently if jq isn't available
command -v jq >/dev/null 2>&1 || exit 0

# Env-agnostic project root detection.
# Capture rev-parse separately so `set -e` doesn't abort on non-zero exit
# when running outside a git repo (Codex/Claude both should set the env var,
# but this is defensive).
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-${CODEX_PROJECT_DIR:-}}"
if [[ -z "$PROJECT_DIR" ]]; then
  PROJECT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || true)"
fi
[[ -z "$PROJECT_DIR" ]] && exit 0

TOOL_INPUT=$(cat)
hook_event=$(echo "$TOOL_INPUT" | jq -r '.hook_event_name // ""' 2>/dev/null || echo "")
command=$(echo "$TOOL_INPUT" | jq -r '.tool_input.command // ""' 2>/dev/null || echo "")

# If no command found, allow
if [[ -z "$command" ]]; then
  exit 0
fi

# Skip compound commands (each part checked separately)
if [[ "$command" == *"&&"* ]] || [[ "$command" == *";"* ]]; then
  exit 0
fi

# === GIT COMMIT ===
if [[ "$command" =~ ^git\ commit ]]; then

  # --- PreToolUse: Hard block private files ---
  if [[ "$hook_event" == "PreToolUse" ]]; then
    staged_files=$(cd "$PROJECT_DIR" && git diff --cached --name-only 2>/dev/null || echo "")

    if echo "$staged_files" | grep -qE '^private/|^CLAUDE\.md$'; then
      echo "" >&2
      echo "SECURITY BLOCK: Cannot commit private/ or CLAUDE.md!" >&2
      echo "" >&2
      echo "Blocked files:" >&2
      echo "$staged_files" | grep -E '^private/|^CLAUDE\.md$' | sed 's/^/  - /' >&2
      echo "" >&2
      echo "Run 'git reset HEAD <file>' to unstage them." >&2
      exit 2
    fi
    exit 0
  fi

  # --- PostToolUse: Content review via additionalContext ---
  if [[ "$hook_event" == "PostToolUse" ]]; then
    # Get the diff of what was just committed
    committed_diff=$(cd "$PROJECT_DIR" && git show --format="" HEAD 2>/dev/null || echo "")

    if [[ -n "$committed_diff" ]]; then
      jq -n \
        --arg diff "$committed_diff" \
        '{
          hookSpecificOutput: {
            hookEventName: "PostToolUse",
            additionalContext: ("CONTENT REVIEW: Check this committed diff for personal information (names, locations, private details). If you see any sensitive info, recommend: git reset --soft HEAD~1\n\n" + $diff)
          }
        }'
    fi
    exit 0
  fi
fi

# === GIT ADD ===
if [[ "$command" =~ ^git\ add ]]; then
  # Direct add of private/ folder or CLAUDE.md
  if [[ "$command" =~ (^|[[:space:]])private/ ]] || [[ "$command" =~ (^|[[:space:]])CLAUDE\.md([[:space:]]|$) ]]; then
    echo "" >&2
    echo "SECURITY BLOCK: Cannot add private/ or CLAUDE.md to git!" >&2
    exit 2
  fi

  # git add . or git add -A
  if [[ "$command" =~ git\ add\ (\.|--all|-A) ]]; then
    untracked=$(cd "$PROJECT_DIR" && git status --porcelain 2>/dev/null | grep -E '^\?\? (private/|CLAUDE\.md)' || echo "")
    if [[ -n "$untracked" ]]; then
      echo "" >&2
      echo "SECURITY BLOCK: 'git add .' would include private files!" >&2
      echo "Use 'git add <specific-files>' instead." >&2
      exit 2
    fi
  fi
fi

# === GIT PUSH ===
if [[ "$command" =~ ^git\ push ]]; then
  remote_branch=$(cd "$PROJECT_DIR" && git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo "origin/main")
  commits_files=$(cd "$PROJECT_DIR" && git diff --name-only "$remote_branch"..HEAD 2>/dev/null || echo "")

  if echo "$commits_files" | grep -qE '^private/|^CLAUDE\.md$'; then
    echo "" >&2
    echo "SECURITY BLOCK: Cannot push commits containing private/ or CLAUDE.md!" >&2
    echo "" >&2
    echo "Blocked files in commits:" >&2
    echo "$commits_files" | grep -E '^private/|^CLAUDE\.md$' | sed 's/^/  - /' >&2
    exit 2
  fi
fi

exit 0
