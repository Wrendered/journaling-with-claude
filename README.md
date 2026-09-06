# Journaling with Claude and Codex

A personal reflection and knowledge system for Claude Code and OpenAI Codex. Talk naturally, preserve your own words, and connect journals with decisions, relationships, career plans, writing, and projects. The system uses portable local files and a rebuildable search index. Its reliability approach grew out of [designing reliable AI systems](https://wrenchatwork.substack.com/p/rigorous-work-with-fallible-ai).

You can start with a heart dump. You do not need to organize your archive or complete a questionnaire first.

## Getting started

Clone the repository and open it in your chosen client. Python 3.9+ with SQLite FTS5 is required; no additional Python packages or graph service are needed for the core.

```sh
git clone https://github.com/Wrendered/journaling-with-claude.git
cd journaling-with-claude
bash scripts/install-git-hooks.sh
bash scripts/check.sh
```

Tell the assistant you want to start journaling. Onboarding creates missing private pages while preserving existing files. Personal preferences live in `private/system-instructions.md`. `CLAUDE.md` is a compatibility symlink to `AGENTS.md`, so both clients read the same public instructions. `.claude/skills` points to `.agents/skills`.

Restart clients after changing their project hooks. UserPromptSubmit captures each message and returns a receipt. Where the client does not load those hooks, the assistant follows the same capture contract manually. A missing receipt must never be treated as proof of saving.

The Git hook installer preserves existing custom hook systems. If it reports one, integrate the staged privacy and configuration checks into that workflow.

## What happens when you talk

Your exact words are saved before interpretation, including uncertainty and unfinished thoughts. While you are still talking, the assistant keeps acknowledgment brief. You choose when to reflect. Its interpretations stay visibly separate from your words; agreement is a new user statement rather than retroactive authorship.

Corrections create new records and preserve earlier accounts. Current status points to a dated supporting passage. Older imported writing keeps its original context, and conflicting reports stay visible. The system does not invent reasons for a decision you have not explained.

## Where things live

| Layer | Location | Purpose |
|---|---|---|
| Original messages | `private/journal/entries/YYYY-MM-DD/` | Exact text, speaker, stable ID, dates, checksum |
| Imported originals | `private/raw/imports/` | Original bytes, hash, import manifest |
| Sourced state | `private/state/assertions/` | Dated reports, evidence, explicit corrections |
| Personal wiki | `private/relationships/`, `decisions/`, `career/`, `writing/`, `projects/`, `self-map.md` | Useful synthesis with links back to evidence |
| Current and chronological views | `private/views/current.md`, `timeline.md` | Generated from records |
| Interactive graph | `private/views/graph.html` | Local source browser with typed connections |
| Search cache | `private/.cache/vault.sqlite` | Rebuildable SQLite full-text index |
| Operational ledger | `private/state/operations.jsonl` | Compact record of successful operations |

Existing weekly journals, raw history, and `private/log.md` remain intact as legacy material. They stay searchable; new messages use the source-record format. Weekly reviews produce attributed wiki summaries under `private/reviews/`.

Other project repositories remain where they are. Link them from personal project pages and connect those pages to writings, goals, and source records. There is no requirement to merge your code repositories into this vault.

## Everyday entry points

| Say something like | Skill |
|---|---|
| “I need to talk” | monologue |
| “Help me understand this decision” | deep-dive |
| “Good morning” / “Let’s reflect on today” | start-day / end-day |
| “Help me plan the week” / “Review my week” | plan-week / weekly-review |
| “Here are my old journals” | import-history |
| “Check my knowledge system for contradictions” | consolidate-memory |
| “Add this framework” | add-framework |
| “Set up backups” / “Back up my journal” | setup-backups / backup |

Rituals and coaching are optional. Community, relationships, and outside support can be part of the reflection without becoming mandatory tracking chores. External task integrations are optional and follow the user’s requested scope.

## Search, graph, and integrity

```sh
python3 scripts/vault.py build
python3 scripts/vault.py search "a phrase or topic"
python3 scripts/vault.py show SOURCE_ID
python3 scripts/vault.py audit
```

Search refreshes its index so newly saved material is discoverable. Open `private/views/graph.html` locally to explore records and source passages. The page uses no external scripts or network requests. Legacy documents are marked as mixed or unknown authorship until their original passages establish who said what.

This uses ideas from [Karpathy’s LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): preserved inputs, a linked wiki, and a clear schema. Dated evidence and explicit supersession borrow temporal concepts described by [Graphiti](https://github.com/getzep/graphiti). Search is currently lexical. Semantic retrieval such as [QMD](https://github.com/tobi/qmd) can be evaluated later against the same sources if phrasing differences cause misses.

## Backups and privacy

`private/` is ignored by the public repository. Client guards and the Git pre-commit check help prevent accidental public commits; inspect diffs as well. The public repository contains reusable tools, generic instructions, templates, and synthetic tests. Journal entries, personal preferences, imports, generated graphs, search databases, and backup manifests belong in the private vault. Publishing a generated HTML graph would publish its embedded source passages.

Personal files sent to a model are handled by that client/provider. Local storage alone does not mean model processing is offline. A Dropbox or iCloud backup location may sync off the machine.

```sh
python3 scripts/vault.py backup --destination /your/backup/folder
python3 scripts/vault.py verify-backup /your/backup.zip --restore-to /empty/restore-test
```

A backup includes originals, import staging, wiki, and state, with a hash manifest. It excludes generated views/caches, Git internals, environments, `.env*`, and symlinks. Existing backups are never automatically pruned. Restoration requires an empty destination and puts the vault under `DEST/private`. Do not restore over a live vault.

The backup skill uses `private/backup-config.sh`. Its `--encrypt` wrapper supports password entry in an interactive terminal using legacy ZIP encryption; passwords never belong in chat or command arguments. Private Git commits and remote configuration require explicit authorization.

## Maintaining the harness

Read [the memory contract](docs/memory-contract.md) for capture/state/import formats and [the harness guide](docs/harness.md) for lifecycle hooks and model profiles. Shared instructions stay short. Model profiles are recommendations, not changes to your selected model.

After editing `.claude/settings.json` or `.claude/agents/`, run `bash scripts/sync-codex.sh`. The sync check compares without mutating your files. `bash scripts/check.sh` exercises synthetic capture, correction, concurrency, retrieval, attribution, backup/restore, and public privacy cases.

[Roadmap](ROADMAP.md) tracks remaining evaluation work and optional extensions.
