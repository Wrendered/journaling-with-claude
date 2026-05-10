# Private Vault Index

> **MOC (Map of Content)** — first thing Claude reads when working in `private/`.
>
> Pattern from Karpathy's "LLM Wiki": index.md is the catalog. Drill into linked pages from here. Avoids needing embeddings/RAG at this scale.

**Last updated:** [auto-update via end-day or weekly-review]

---

## Top-level files

- [self-map.md](self-map.md) — Patterns, drivers, self-knowledge (read every session)
- [dashboard.md](dashboard.md) — Current state: MIT, life areas, habits, experiments (read every session)
- [log.md](log.md) — Append-only chronological log (greppable; `## [YYYY-MM-DD] type | Title`)
- [tags.md](tags.md) — Controlled vocabulary for frontmatter `tags:` (cap ~20 tags)

## Folders

<!-- Stable patterns about yourself live in self-map.md, not their own files.
     Deep theme compilations belong in history/themes-<topic>.md if you have
     substantial historical material. The atomic-notes-per-claim pattern
     was tried and removed: it was redundant with self-map + history/themes,
     and per-claim filenames clashed with the "don't diagnose, frame as
     observation" tone discipline. -->

- [decisions/](decisions/_index.md) — Open and resolved decisions
- [relationships/](relationships/_index.md) — Key people in my life
- [journal/](journal/_index.md) — Weekly journal files (`YYYY-Www.md`) and daily entries (`YYYY-MM-DD.md`)
- [history/](history/_index.md) — Imported historical material (years of past writing)
- [raw/](raw/) — Immutable source inputs (voice memos, clipped articles, screenshots) — never edited
- [archive/](archive/) — Closed/resolved items moved here to keep active folders scannable

## How Claude should use this index

1. Read this file first when entering `private/`.
2. Drill into the relevant folder's `_index.md` for orientation.
3. Use frontmatter (`type:`, `status:`, `revisit:`, `tags:`) to filter via grep.
4. For chronological queries: grep `log.md` for prefixes like `## [2026-` to find recent activity.
5. Don't enumerate all files; use this index + grep + targeted reads.
