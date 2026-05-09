# Personal Log

> **Append-only chronological log.** Greppable, never reorganized.
>
> Pattern from Karpathy's "LLM Wiki": one consistent prefix format makes timeline reconstruction cheap with `grep` instead of full-file scans.

## Format

Each entry uses this prefix:

```
## [YYYY-MM-DD] <type> | <title>
```

Types:
- `morning` — start-day entries
- `evening` — end-day entries
- `monologue` — captured stream-of-consciousness
- `decision` — decision made or revisited
- `ingest` — raw source pulled in (article, book, conversation)
- `pattern` — pattern surfaced 3+ times
- `note` — anything else worth a timestamp

Body is short — 1-3 paragraphs, or a quoted snippet plus context. Long-form reflection belongs in `journal/YYYY-Www.md`. The log is the timeline; the journal is the narrative.

## How to grep

```bash
grep "^## \[2026-05" log.md       # everything in May 2026
grep "^## \[.*\] decision" log.md # all decisions ever
grep "^## \[2026-W19" log.md      # entries by week (if you log week-num style too)
```

---

## Entries

<!-- Newest at top OR bottom; pick one and stick to it. Karpathy's gist uses chronological top-to-bottom. -->

## [2026-05-09] note | Log started

First entry. The log will fill up over time as skills (start-day, end-day, monologue, deep-dive) append automatically.
