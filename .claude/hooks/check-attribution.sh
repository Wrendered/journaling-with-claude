#!/bin/bash
# Attribution hook: Warn when journal entries blend user's words with Claude's framing
#
# PostToolUse on Write/Edit/MultiEdit when path matches private/journal/ or private/decisions/ or
# private/relationships/. Soft warning via additionalContext — does not block the operation.
#
# Why: The user's journal must preserve THEIR words distinctly from Claude's framings, so
# they can re-read what they actually said vs. what Claude offered. Blending the two
# corrupts the historical record.
#
# What we check:
# - If the file is in private/journal/, private/decisions/, or private/relationships/
# - AND the diff added prose that looks like reflection content (not just structure)
# - THEN check whether Claude's framings are clearly separated from the user's words
#
# Heuristic: a journal entry should have either (a) explicit attribution sub-headers like
# "**Her words:**" / "**Claude's framings:**", or (b) only direct quotes (no narrative
# rewriting of what the user said). If it has free narrative without attribution, warn.

set -e

# Bail silently if jq isn't available — this hook is advisory, not load-bearing
command -v jq >/dev/null 2>&1 || exit 0

TOOL_INPUT=$(cat)
hook_event=$(echo "$TOOL_INPUT" | jq -r '.hook_event_name // ""' 2>/dev/null || echo "")
tool_name=$(echo "$TOOL_INPUT" | jq -r '.tool_name // ""' 2>/dev/null || echo "")

# Tools that edit files: Claude Code (Write/Edit/MultiEdit) and OpenAI Codex CLI (apply_patch).
# If we don't recognize the tool, exit silently — this hook is advisory.
case "$tool_name" in
  Write|Edit|MultiEdit|apply_patch) ;;
  *) exit 0 ;;
esac

# Get the file path from tool input.
# Claude Code: .tool_input.file_path (Write/Edit) or .tool_input.path
# Codex apply_patch: paths are embedded in the patch payload at .tool_input.command (or .tool_input.input)
file_path=$(echo "$TOOL_INPUT" | jq -r '.tool_input.file_path // .tool_input.path // ""' 2>/dev/null || echo "")

# If we got nothing and this is Codex apply_patch, scrape the first path out of the patch payload.
# apply_patch format includes lines like `*** Update File: path/to/file` and `*** Add File: path/to/file`.
if [[ -z "$file_path" && "$tool_name" == "apply_patch" ]]; then
  patch_payload=$(echo "$TOOL_INPUT" | jq -r '.tool_input.command // .tool_input.input // .tool_input.patch // ""' 2>/dev/null || echo "")
  # Pick the first matching path from the patch
  file_path=$(echo "$patch_payload" | grep -oE '^\*\*\* (Update|Add|Move) File: [^[:space:]]+' | head -1 | sed -E 's/^\*\*\* (Update|Add|Move) File: //')
fi

if [[ -z "$file_path" ]]; then
  exit 0
fi

# Only check files in attribution-sensitive paths
attribution_paths='private/journal/|private/decisions/|private/relationships/|private/log\.md'
if ! echo "$file_path" | grep -qE "$attribution_paths"; then
  exit 0
fi

# PostToolUse: file already written, can read it
if [[ "$hook_event" != "PostToolUse" ]]; then
  exit 0
fi

# Skip if file doesn't exist (might have been deleted)
if [[ ! -f "$file_path" ]]; then
  exit 0
fi

# Read the file
content=$(cat "$file_path" 2>/dev/null || echo "")

# Skip very short files (less than 100 chars — probably just frontmatter)
if [[ ${#content} -lt 100 ]]; then
  exit 0
fi

# Check for attribution markers (these indicate proper separation)
# grep -c always prints a count and returns 0 if matches, 1 if none — we just want the count
has_attribution=$(printf '%s' "$content" | grep -ciE 'their words|her words|his words|user.s words|claude.s framing|claude.s interpretation|\*\*Quote' || true)
has_attribution=${has_attribution:-0}

# Check for narrative-style writing about the user (heuristic: third-person "she/he/they" + verb patterns)
has_narrative=$(printf '%s' "$content" | grep -ciE 'she (said|feels|thinks|noted|mentioned|seemed)|he (said|feels|thinks|noted|mentioned|seemed)|they (said|feel|think|noted|mentioned|seemed)' || true)
has_narrative=${has_narrative:-0}

# If there's narrative without attribution markers, warn
if [[ "$has_narrative" -gt 0 && "$has_attribution" -eq 0 ]]; then
  message="ATTRIBUTION CHECK: The file at ${file_path} contains ${has_narrative} narrative-style description(s) of what the user said/felt/thought. Per the attribution rule (CLAUDE.md): journal entries must clearly separate the user actual words from Claude framings or interpretations. Use sub-sections like **Their words:** for direct quotes or paraphrase, and **Claude framings offered:** for any reframe or pattern Claude proposed. Re-read the file and refactor if needed."

  jq -n --arg msg "$message" '{
    hookSpecificOutput: {
      hookEventName: "PostToolUse",
      additionalContext: $msg
    }
  }'
fi

exit 0
