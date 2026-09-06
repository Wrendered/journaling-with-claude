# Personal knowledge and reflection system

Shared instructions for Codex and Claude Code. `CLAUDE.md` is the compatibility
symlink to this file. Generic behavior belongs here; personal preferences and
all personal content belong in `private/`.

## Start with relevant, current context

1. Read `private/system-instructions.md` if present.
2. Read `private/views/current.md` for dated current reports and unresolved
   conflicts. Run `python3 scripts/vault.py build` if this view is missing or
   newer source records have arrived.
3. Read `private/_index.md` for navigation. For a personal conversation, use the
   recent records in `private/views/timeline.md`; retrieve other history as needed.
   For repository work, inspect the relevant code and instructions.
4. Read `private/self-map.md` only when its broader synthesis is relevant. Treat
   its older descriptions as interpretations to verify against current evidence.

If no personal vault exists, use onboarding. A returning user can start talking
immediately; organizing old material is independent work.

## Conversation

Be direct, attentive, and concise. No emojis unless requested. Follow the user's
personal tone preferences and their current request. Ask one useful question at
a time when reflection calls for it. A heart dump or vent may simply need room
and acknowledgment; let the user signal when they want synthesis or questions.
A technical request can receive substantial technical work.

Ground observations in the user's actual words. Ask whether a connection fits;
do not diagnose, prescribe a life decision, or turn a recurring phrase into a
fixed identity. Frameworks are optional lenses from the reference library.
Research unfamiliar expertise using primary sources; independent research can
be delegated when it usefully divides the work.

## Memory contract

Read [docs/memory-contract.md](docs/memory-contract.md) before the first capture,
state change, import, or migration in a session. Use `scripts/vault.py` for these
operations. It needs Python 3.9+ with SQLite FTS5; no service or API key is needed.

- Capture meaningful user text verbatim and promptly. UserPromptSubmit hooks do
  this automatically in configured clients and return a source ID. Reuse that
  record instead of duplicating it. If a hook receipt is absent, capture manually
  with a stable message ID. State explicitly if saving fails.
- New canonical records live in `private/journal/entries/YYYY-MM-DD/`. Old weekly
  journals and `private/log.md` are preserved legacy records, not new write targets.
- Store only assistant text already delivered to the user. Planned responses are
  not memories. User adoption of an interpretation is a separate sourced event.
- Source records are immutable. Capture a correction as a new record. Current
  status is represented by sourced assertions, with explicit supersession where
  needed. The event date and recording date are separate; unknown dates stay unknown.
- An exact supporting quote is required for a status assertion. Quote matching
  proves text provenance, not that the proposed interpretation follows from it.
  Thoughts, fears, hypotheticals, and assistant hypotheses keep their attribution.
- `private/views/` and `private/.cache/` are generated. Rebuild them; do not edit
  them. Timeline, search, current context, and graph derive from source records.
- Keep narrative people/decision/project pages when they are useful, with links
  to evidence. Avoid copying changing status into multiple indexes or dashboards.
  Dashboard carries chosen tasks and navigation; current status links to the view.
- Retain original imported bytes and citation paths. Import is content-addressed.
  Legacy archives remain searchable and clearly labeled as mixed/unknown authorship.
- Use `search`, `show`, and source files to answer history questions. Inspect
  originals before quoting. If retrieval finds nothing, report a coverage gap,
  not a conclusion that the user never discussed it.

## Skills and references

Skills live in `.agents/skills/`; `.claude/skills` points there. The existing
start-day, end-day, monologue, deep-dive, plan-week, weekly-review, import-history,
consolidate-memory, onboarding, add-framework, backup, and setup-backups entry
points remain available. Use their scope descriptions; do not run a ritual merely
because a date has passed. Interactive reflection stays in the main conversation.

- Storage and command examples: [memory contract](docs/memory-contract.md)
- Client setup and model-specific tuning: [harness](docs/harness.md)
- Frameworks, daily practices, assessments, exercises: their folder indexes

## Working with multiple agents

Assign ownership before parallel writes. One agent owns any given private file.
Use independent agents for bounded research or forward-testing when helpful;
keep ordinary conversation together. For a non-trivial handoff, leave a short
local-only note in `private/handoffs/` naming task, files, validation and open issues.
Do not introduce a second task-coordination system. Shared durable behavior belongs
in tracked files, and personal content belongs only in `private/`.

## Persistence, privacy, and validation

Never stage or commit `private/` or personal information into the parent public
repository. The private vault has no remote; never add one or publish it without
explicit user instruction. Default to verified backup files. Do not make private
Git commits unless explicitly authorized by the user or their personal policy.

The Git pre-commit guard checks staged paths independently of client tool hooks.
Inspect public diffs for personal content as well. Do not add a license unless asked.
Preserve existing uncommitted work. Back up before broad migration; keep source
hashes and a restoreable manifest. No automatic deletion of older backups.

For harness changes, run `bash scripts/check.sh`. For vault changes, run
`python3 scripts/vault.py build` and `python3 scripts/vault.py audit`. Mechanical
checks protect files and attribution structure; evaluate semantic fidelity and
interaction quality using representative scenarios. Do not claim a model
benchmark or external integration was tested when only local checks ran.
