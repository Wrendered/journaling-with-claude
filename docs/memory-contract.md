# Memory contract, version 2

Original records are durable. Current context, search, timelines, and the graph
are derived. All commands use `python3 scripts/vault.py`; `--vault PATH` before
the subcommand selects an isolated test vault. The default is this repo's private/.

## Capture

Send a UTF-8 JSON object to `capture --input FILE` (or stdin). Write the JSON
with a file tool or a properly quoted heredoc; never interpolate a heart dump into
shell command text. A user record needs `text` and a stable `id` when available:

```json
{
  "id": "session-example-message-1",
  "session_id": "session-example",
  "title": "A decision I want to remember",
  "text": "I paused the garden project yesterday. I want to remember why.",
  "recorded_at": "2024-02-12T14:00:00+00:00",
  "occurred_on": "2024-02-11",
  "entities": ["project:garden", "decision:example"]
}
```

The hook receipt identifies an already-saved source. Reuse it. Without a receipt,
capture manually before analysis. Each message gets its own record; `session_id`
groups the conversation. Repeating an ID with identical content is idempotent;
changing its text raises an error. Use a new ID for corrections.

`recorded_at` defaults to the machine’s local time with an offset (`VAULT_TIMEZONE` can set an IANA timezone). Unknown JSON fields are rejected rather than silently discarded. Set `occurred_on` only when
established; missing event dates remain null. A relative date is resolved from the
user's local date, not UTC or import time. Preserve approximate timing in the exact
text rather than fabricating a precise date.

Kinds: `user_statement` / speaker `user`; `assistant_framing` or
`assistant_summary` / speaker `assistant`; `system_observation` / speaker `system`.
Assistant kinds require `delivered: true`. Do not set it on text you plan to send.
Normally only user text needs immediate capture. Add already-delivered assistant
context later when useful, with references to the relevant source IDs.

`references` is an optional list of `{relation, target, evidence}`. Relations are
`about`, `mentions`, `source_for`, `related_project`, `supersedes`, `contradicts`.
Targets are record/document/entity identifiers shown in graph.json. A declared
connection is a navigation assertion, not automatic evidence of semantic agreement.

The Markdown frontmatter contains a JSON object (valid YAML), including body
checksum and stable ID. The body is the exact text. Use `show ID` for the complete
record. Source files are immutable; never fix spelling in place.

## Current context

Use `state --input FILE` only when a meaningful status update helps later sessions.

```json
{
  "id": "example-status-1",
  "subject": "project:garden",
  "predicate": "project-status",
  "value": "Project paused",
  "source": "session-example-message-1",
  "evidence": "I paused the garden project yesterday.",
  "as_of": "2024-02-11",
  "kind": "user_report"
}
```

The source must exist and the evidence must match its text exactly. User reports
require user sources. Assistant hypotheses require assistant sources and stay
visibly separate. A fear about an outcome is not evidence that the outcome occurred.
Use the narrowest supported wording. Adoption requires a new user source; authorship
of the original idea remains with the assistant.

A correction uses a new assertion ID and `supersedes: ["example-status-1"]`.
Supersession is limited to the same subject, predicate, and attribution kind.
Without explicit supersession, the latest as-of date supplies the current view;
disagreeing reports on the same date remain an unresolved conflict. Importing older
material cannot override a newer event just because it was ingested later.

Run `build` after meaningful updates. `current` returns the computed status as JSON.
Use private/views/current.md as the current-state entry point. Narrative entity
pages may explain context but should link here instead of repeating mutable state.

## Retrieval and graph

`build` indexes new records and existing .md/.txt files using SQLite FTS5. Originals
stay where they are. Existing Markdown and wikilinks become navigation edges;
record entities and sourced assertions add explicit typed edges. Ambiguous legacy
wikilinks are not guessed. External code repositories stay in place and can be
referenced from project pages; their contents are not silently ingested.

- `search "words to find" --limit 8` gives passages and attribution metadata.
- `show SOURCE_ID` retrieves a new record, a `file:` document, or an `import:` manifest and text when supported.
- Read the returned path for a legacy document and verify the relevant passage.
- `private/views/graph.html` is a local interactive view with no network calls.
- `private/views/timeline.md` lists new source records by recording time.
- `private/views/index-report.json` identifies legacy link candidates.

Search is lexical and replaceable. When paraphrase matching is needed, use broader
terms and existing indexes; evaluate a local semantic index on the same questions
before adopting one. Graph edges and synthesized text are not independent evidence.

## Historical import and migration

`import PATH --label LABEL` preserves the source bytes under a SHA-256 directory in
raw/imports. Repeated imports return the existing source. Extraction, OCR, and
summaries are separate derived records linked to that source. This command preserves
files; it does not claim to transcribe PDFs, images, or audio. Use a suitable tool
for the provided medium, retain confidence/uncertainty, and verify quotations.

`legacy-manifest` previews the frozen legacy originals; `legacy-manifest --write`
records their hashes. Old weekly journals, raw files, and log.md stay in place.
Do not infer source authorship while importing mixed legacy documents. New curated
records can cite `source_origin` with legacy path and passage context. Never label extracted or summarized material as a present user message. Import IDs cannot establish user-attributed current state; use an actual captured user confirmation.

New capture writes no duplicate narrative into log.md. state/operations.jsonl is
a compact operational ledger. Weekly summaries live in reviews/ with
source links; they are assistant synthesis, not replacements for original messages.

## Integrity and restore

`audit` checks new record checksums/authorship, exact assertion evidence, imported
bytes, and frozen legacy sources. Legacy link warnings are review candidates;
source corruption and invalid new records fail the check. This cannot prove a
psychological interpretation true or decide whether two statements are compatible.

`backup --destination PATH` makes a ZIP with a checksum manifest and verifies it.
It includes private/import originals and state, excludes caches/views, environments,
.git, and secrets named .env*. It never prunes older backups. Destination must be
outside the vault. Existing external symlinks are not followed.

`verify-backup ARCHIVE --restore-to EMPTY_DIRECTORY` verifies and restores into an
empty location, then checks restored hashes. It never replaces a live vault. Use
this before relying on a backup. The normal backup skill uses the private configured
destination. Private Git commits remain subject to explicit personal authorization.

## Interaction requirements

For a heart dump, capture each message and keep acknowledgment short while the user
continues. A partial dump does not need a summary, question, or interpretation.
When the user is ready, help organize what they actually said, what remains uncertain,
and what they want to remember. Save reasons for a decision from their account;
missing reasons stay missing even if older deliberations suggest plausible ones.

A fresh session should recover current facts and their sources. It should neither
turn the most recent feeling into a permanent trait nor treat an old summary as
present-day truth. Keep maintenance progress out of the journal's personal narrative.
