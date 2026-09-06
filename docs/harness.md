# Harness and model profiles

The shared contract is AGENTS.md plus docs/memory-contract.md. Both clients discover
the same .agents/skills through the compatibility symlink. Host-specific events and
settings remain in .claude/ and .codex/; generated Codex files are synchronized with
scripts/sync-codex.sh. scripts/verify-sync.sh compares expected content in memory without modifying files.

## Capture lifecycle

- UserPromptSubmit preserves exact user text before the response and provides a
  receipt/source ID. A host turn ID makes retries idempotent; where the host supplies
  none, captures receive unique IDs so repeated messages are not silently dropped.
- SessionStart rebuilds the local index and loads a short current-context view.
- Stop and PreCompact rebuild derived views. They do not record imagined assistant
  text or attempt to parse an unstable internal transcript format.
- PreToolUse guards existing immutable source files against direct file edits.
- PostToolUse checks new attribution-sensitive content; it is advisory.
- Git pre-commit checks staged public paths independently of client hooks.

Restart each client after changing project hook configuration. For an already-open
conversation, follow the current contract explicitly and use manual capture when no
hook receipt is present. A missing receipt is not proof of a successful save.

Run `bash scripts/install-git-hooks.sh` once per checkout; the installer preserves
custom hooks by refusing to replace an unrelated configured hook directory.
Run `bash scripts/check.sh` for synthetic record/hook/privacy tests and config sync.
Run `python3 scripts/vault.py audit` for local source integrity.

## Workload profiles

These are tunable recommendations, not changes to the user's selected model.

| Workload | Common behavior | Optional model-specific tuning |
|---|---|---|
| Capture and supportive conversation | Main conversation; exact user record; short replies; no unnecessary delegation | Preserve personal tone and source rules on every model. |
| Focused retrieval | Search, inspect sources, give exact evidence and dates | Check retrieval coverage at lower effort, especially Fable. |
| Large import or synthesis | Resumable batches; independent mechanical checks | Fable long runs may benefit from an independent reviewer. |
| Repository implementation | Bounded work, concrete acceptance criteria, relevant tests | Opus 5 discourages generic redundant verifier agents; Sol benefits from removing repeated prompt instructions; Astra benefits from explicit scope and stopping conditions. |

Compare models and effort on the same synthetic scenarios; keep costs, latency,
source fidelity, and interaction quality visible. Capability and effort names vary
by client. Do not hard-code a universal maximum-effort or always-delegate rule.
API-specific replay and compaction machinery belongs to an API application; Codex
and Claude Code already provide the surrounding runtime here.

Current primary references (checked September 6, 2026):
- [Sol](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6)
- [Astra](https://developers.openai.com/api/docs/guides/latest-model)
- [Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)
- [Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1)
- [Codex hooks](https://learn.chatgpt.com/docs/hooks)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
