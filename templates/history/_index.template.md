# History

> Imported historical material — past journals, therapy notes, letters. Built by the `import-history` skill.

This folder may not exist until you import historical material. The `import-history` skill creates and populates it.

## Expected files (when populated)

- `journal-raw.txt` — Full text archive, grep-able, never edited
- `quotes-index.md` — Curated significant quotes organized by theme
- `themes-<topic>.md` — Deep compilations of recurring themes (grief, decisions, identity, etc.)
- `relationships-<name>.md` — Pattern analysis for key people across the historical record

## How to search

```bash
grep -i "decision" history/journal-raw.txt | head
grep -l "anxious" history/themes-*.md
```

## Cross-references

- Living relationship files in `private/relationships/` — analysis here is the historical archive
- `private/self-map.md` — stable patterns about you live here (not in per-claim files; that pattern was tried and dropped as redundant with self-map + history/themes)
