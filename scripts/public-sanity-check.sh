#!/bin/bash
# Public-release sanity checks for the tracked repo.

set -euo pipefail

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT_DIR"

failures=0

pass() {
  printf 'ok - %s\n' "$1"
}

fail() {
  printf 'FAIL - %s\n' "$1" >&2
  failures=$((failures + 1))
}

warn() {
  printf 'warn - %s\n' "$1" >&2
}

require_rg() {
  if ! command -v rg >/dev/null 2>&1; then
    fail "ripgrep (rg) is required for public sanity checks"
    exit 1
  fi
}

check_sync() {
  local temp
  temp="$(mktemp -d "${TMPDIR:-/tmp}/journaling-with-claude-sync.XXXXXX")"
  trap 'rm -rf "$temp"' RETURN

  mkdir -p "$temp"
  cp -R .claude .codex scripts "$temp/"

  if (cd "$temp" && bash scripts/verify-sync.sh) >/tmp/journaling-with-claude-verify-sync.out 2>&1; then
    pass ".codex generated files are in sync"
  else
    cat /tmp/journaling-with-claude-verify-sync.out >&2
    fail ".codex generated files drifted from .claude source"
  fi
}

check_tracked_private_paths() {
  local tracked
  tracked="$(git ls-files private CLAUDE.local.md AGENTS.override.md .env .env.local '*.pem' '*.key' '*.sqlite' '*.db' 2>/dev/null || true)"
  if [[ -n "$tracked" ]]; then
    printf '%s\n' "$tracked" >&2
    fail "sensitive paths are tracked"
  else
    pass "no private/ or obvious secret files are tracked"
  fi
}

check_stale_personal_config_refs() {
  local refs
  refs="$(
    rg --hidden -n 'AGENTS\.override|CLAUDE\.local|configure in CLAUDE\.md|edit AGENTS\.md directly|Update AGENTS\.md|Check AGENTS\.md|configured in `AGENTS\.md' \
      --glob '!.git/**' \
      --glob '!private/**' \
      --glob '!.claude/worktrees/**' \
      --glob '!scripts/public-sanity-check.sh' \
      . || true
  )"
  if [[ -n "$refs" ]]; then
    printf '%s\n' "$refs" >&2
    fail "stale personal-config references found"
  else
    pass "no stale override/CLAUDE personal-config references"
  fi
}

check_secret_like_content() {
  local hits
  hits="$(
    git grep -I -l -E '(api[_-]?key|client_secret|github_pat_|ghp_|sk-[A-Za-z0-9]{20,}|BEGIN (RSA|OPENSSH|EC|PRIVATE) KEY|password[[:space:]]*[:=]|bearer [A-Za-z0-9._-]{20,})' \
      -- . ':!private' ':!scripts/public-sanity-check.sh' ':!scripts/check_staged.py' ':!tests' || true
  )"
  if [[ -n "$hits" ]]; then
    printf '%s\n' "$hits" >&2
    fail "secret-like content found in tracked files"
  else
    pass "no obvious secret-like content in tracked files"
  fi
}

check_worktree_junk() {
  local junk
  junk="$(find . -path ./.git -prune -o -path ./private -prune -o -path './.claude/worktrees' -prune -o \( -name .DS_Store -o -name '*.pyc' -o -name .env -o -name .env.local \) -print)"
  if [[ -n "$junk" ]]; then
    printf '%s\n' "$junk" >&2
    warn "local ignored junk exists; remove before packaging a release tarball"
  else
    pass "no obvious local junk outside private/"
  fi
}

check_identity_exposure() {
  local emails
  emails="$(git log --all --format='%ae' | sort -u | rg -v 'users\.noreply\.github\.com$' || true)"
  if [[ -n "$emails" ]]; then
    printf '%s\n' "$emails" >&2
    warn "git history exposes non-noreply author email(s); decide if this is intentional before wider sharing"
  else
    pass "git history uses noreply author emails"
  fi
}

require_rg
check_sync
check_tracked_private_paths
check_stale_personal_config_refs
check_secret_like_content
check_worktree_junk
check_identity_exposure

if [[ "$failures" -gt 0 ]]; then
  printf '\n%d public sanity check(s) failed.\n' "$failures" >&2
  exit 1
fi

printf '\nPublic sanity checks passed.\n'
