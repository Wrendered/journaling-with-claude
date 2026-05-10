#!/bin/bash
# Security hook: Block private files (hard) + Review diff content (soft)
#
# PreToolUse: Block private/ or CLAUDE.md (exit 2)
# PostToolUse: Inject diff to assistant for content review (additionalContext)
#
# Works in both Claude Code (sets $CLAUDE_PROJECT_DIR) and OpenAI Codex CLI
# (sets its own project root vars). Falls back to git rev-parse.
#
# Compound commands (&& and ;) are split and each segment is checked. The previous
# version bailed on compound commands, allowing `git add -f private/x && git commit`
# to bypass entirely. That hole is now closed.

set -e

# Bail silently if jq isn't available
command -v jq >/dev/null 2>&1 || exit 0

# Env-agnostic project root detection.
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

# === Path patterns (single source of truth) ===
# A staged-files regex that matches one filename per line.
BLOCKED_FILES_REGEX='^private/|^CLAUDE\.md$'
# An argument-position regex for `git add <path>` etc. Matches both `private`
# and anything under `private/`.
BLOCKED_ARG_REGEX='(^|[[:space:]])(private(/[^[:space:]]*)?|CLAUDE\.md)([[:space:]]|$)'
BLOCKED_LIST="private/ or CLAUDE.md"

normalize_segment() {
  local normalized="$1"
  # Handle common shell spellings without trying to be a full shell parser:
  #   git add ./private/foo
  #   git add "private/journal/today.md"
  normalized="${normalized//\"/}"
  normalized="${normalized//\'/}"
  normalized="$(printf '%s' "$normalized" | sed -E 's#(^|[[:space:]])\./([[:space:]]|$)#\1.\2#g; s#(^|[[:space:]])\./#\1#g')"
  printf '%s' "$normalized"
}

blocked_status_entries() {
  local include_ignored="${1:-false}"
  local status_args=(--porcelain --untracked-files=all)
  [[ "$include_ignored" == "true" ]] && status_args+=(--ignored=matching)

  cd "$PROJECT_DIR" && git status "${status_args[@]}" 2>/dev/null \
    | grep -E "^[? !]{2} (private/|CLAUDE\.md)" || true
}

# Per-segment check function
check_segment() {
  local seg="$1"
  # Strip leading whitespace
  seg="$(echo "$seg" | sed -e 's/^[[:space:]]*//')"
  [[ -z "$seg" ]] && return 0
  local normalized_seg
  normalized_seg="$(normalize_segment "$seg")"

  # === GIT COMMIT ===
  if [[ "$normalized_seg" =~ ^git[[:space:]]+commit ]]; then
    if [[ "$hook_event" == "PreToolUse" ]]; then
      staged_files=$(cd "$PROJECT_DIR" && git diff --cached --name-only 2>/dev/null || echo "")
      if echo "$staged_files" | grep -qE "$BLOCKED_FILES_REGEX"; then
        echo "" >&2
        echo "SECURITY BLOCK: Cannot commit ${BLOCKED_LIST}!" >&2
        echo "" >&2
        echo "Blocked files:" >&2
        echo "$staged_files" | grep -E "$BLOCKED_FILES_REGEX" | sed 's/^/  - /' >&2
        echo "" >&2
        echo "Run 'git reset HEAD <file>' to unstage them." >&2
        exit 2
      fi
    fi
    return 0
  fi

  # === GIT ADD ===
  if [[ "$normalized_seg" =~ ^git[[:space:]]+add ]]; then
    # Direct add of a blocked path as argument
    if [[ "$normalized_seg" =~ $BLOCKED_ARG_REGEX ]]; then
      echo "" >&2
      echo "SECURITY BLOCK: Cannot add ${BLOCKED_LIST} to git!" >&2
      echo "  Command segment: $seg" >&2
      exit 2
    fi
    # git add . / -A / --all can sweep in blocked files. With -f/--force, ignored
    # files are also candidates, so include ignored matches in the scan.
    if [[ "$normalized_seg" =~ (^|[[:space:]])(\.|--all|-A)([[:space:]]|$) ]]; then
      include_ignored=false
      [[ "$normalized_seg" =~ (^|[[:space:]])(-f|--force)([[:space:]]|$) ]] && include_ignored=true
      blocked_entries="$(blocked_status_entries "$include_ignored")"
      if [[ -n "$blocked_entries" ]]; then
        echo "" >&2
        echo "SECURITY BLOCK: bulk git add would include blocked files!" >&2
        echo "Blocked files:" >&2
        echo "$blocked_entries" | sed 's/^/  /' >&2
        echo "Use 'git add <specific-files>' instead." >&2
        exit 2
      fi
    fi
    return 0
  fi

  # === GIT PUSH ===
  if [[ "$normalized_seg" =~ ^git[[:space:]]+push ]]; then
    remote_branch=$(cd "$PROJECT_DIR" && git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo "origin/main")
    commits_files=$(cd "$PROJECT_DIR" && git diff --name-only "$remote_branch"..HEAD 2>/dev/null || echo "")
    if echo "$commits_files" | grep -qE "$BLOCKED_FILES_REGEX"; then
      echo "" >&2
      echo "SECURITY BLOCK: Cannot push commits containing ${BLOCKED_LIST}!" >&2
      echo "" >&2
      echo "Blocked files in commits:" >&2
      echo "$commits_files" | grep -E "$BLOCKED_FILES_REGEX" | sed 's/^/  - /' >&2
      exit 2
    fi
    return 0
  fi
}

# === Handle compound commands by splitting on && and ; ===
# Naive split: doesn't respect shell quoting. We compensate below by detecting
# fragments that look truncated (unbalanced quotes) and ignoring them.
segments_text=$(echo "$command" | sed -E 's/[[:space:]]*&&[[:space:]]*/\n/g; s/[[:space:]]*;[[:space:]]*/\n/g; s/[[:space:]]*\|\|[[:space:]]*/\n/g')

# Track during the loop whether an actual `git commit` was executed in the OUTER
# repo (PROJECT_DIR). Used by the PostToolUse content-review at the bottom.
COMMIT_DETECTED=false
COMMIT_IN_SUBREPO=false
COMMIT_DIR="$PROJECT_DIR"
# Tracks the cwd as we walk segments. Updated by `cd <dir>` segments so a later
# `git commit` segment can be attributed to the right repo.
WORKING_DIR="$PROJECT_DIR"

# Unbalanced-quote detector. If a segment has an odd count of either quote type,
# it's almost certainly a fragment of a quoted string that the naive `&&`/`;` split
# tore in half — like `echo "When I 'cd && git commit', the hook..."`. Skip those.
segment_is_quote_fragment() {
  local s="$1"
  local single_count double_count
  single_count=$(printf '%s' "$s" | tr -cd "'" | wc -c | tr -d ' ')
  double_count=$(printf '%s' "$s" | tr -cd '"' | wc -c | tr -d ' ')
  [[ $((single_count % 2)) -ne 0 || $((double_count % 2)) -ne 0 ]]
}

while IFS= read -r segment; do
  segment_trimmed=$(echo "$segment" | sed -e 's/^[[:space:]]*//')

  # Skip fragments from a sed-split inside a quoted string.
  if segment_is_quote_fragment "$segment_trimmed"; then
    continue
  fi

  # Track `cd <dir>` so we can attribute a later `git commit` to the right repo.
  if [[ "$segment_trimmed" =~ ^cd[[:space:]]+([^[:space:]]+) ]]; then
    cd_target="${BASH_REMATCH[1]}"
    # Strip surrounding quotes (defense against `cd "foo"`)
    cd_target="${cd_target%\"}"; cd_target="${cd_target#\"}"
    cd_target="${cd_target%\'}"; cd_target="${cd_target#\'}"
    if [[ "$cd_target" = /* ]]; then
      WORKING_DIR="$cd_target"
    else
      WORKING_DIR="$PROJECT_DIR/$cd_target"
    fi
  fi

  # Detect a real `git commit` (anchored to start of segment after normalization).
  normalized=$(normalize_segment "$segment_trimmed")
  if [[ "$normalized" =~ ^git[[:space:]]+commit ]]; then
    COMMIT_DETECTED=true
    COMMIT_DIR="$WORKING_DIR"
    # If the commit is happening in a subdir that has its own .git, treat it as
    # a sub-repo commit. Don't run the parent-repo content-review against it
    # (the diff would be wrong AND might surface unrelated PII).
    if [[ "$WORKING_DIR" != "$PROJECT_DIR" ]]; then
      if [[ -d "$WORKING_DIR/.git" || -f "$WORKING_DIR/.git" ]]; then
        COMMIT_IN_SUBREPO=true
      fi
    fi
  fi

  check_segment "$segment"
done <<< "$segments_text"

# === PostToolUse content review (only fires for real outer-repo commits) ===
if [[ "$hook_event" == "PostToolUse" && "$COMMIT_DETECTED" == "true" && "$COMMIT_IN_SUBREPO" == "false" ]]; then
  committed_diff=$(cd "$COMMIT_DIR" && git show --format="" HEAD 2>/dev/null || echo "")
  committed_sha=$(cd "$COMMIT_DIR" && git rev-parse --short HEAD 2>/dev/null || echo "")
  if [[ -n "$committed_diff" ]]; then
    jq -n \
      --arg diff "$committed_diff" \
      --arg sha "$committed_sha" \
      --arg dir "$COMMIT_DIR" \
      '{
        hookSpecificOutput: {
          hookEventName: "PostToolUse",
          additionalContext: ("CONTENT REVIEW (commit " + $sha + " in " + $dir + "): Check this committed diff for personal information (names, locations, private details). If you see any sensitive info, recommend: git reset --soft HEAD~1\n\n" + $diff)
        }
      }'
  fi
fi

exit 0
