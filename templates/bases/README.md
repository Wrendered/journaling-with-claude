# Bases templates — draft / on hold

**Status (2026-05-23):** the three `.base` templates that previously lived here have been moved to [`_draft/`](_draft/). They aren't currently functional on the canonical example vault because the user's `decisions/*.md` and `relationships/*.md` files use body-text fields (`**Status:** Open`, `**Last Updated:** ...`) rather than the YAML frontmatter the queries expect.

Three honest options if you want Bases to work:

1. **Add YAML frontmatter to your decision and relationship files** (~5 min per file, ~20 files total). The frontmatter shape is documented in [`AGENTS.md → YAML Frontmatter Convention`](../../AGENTS.md). Then the templates in `_draft/` light up.
2. **Adjust the templates to query body-text fields** — limited query power; Bases isn't designed for this and works around it awkwardly.
3. **Skip Bases entirely.** The system works fine without them. Claude Code + grep over the vault delivers most query needs.

The `_draft/` versions are preserved as starting points if/when you decide schema cleanup is worth the time — see [`_draft/open-decisions.base`](_draft/open-decisions.base), [`_draft/relationships-by-last-touched.base`](_draft/relationships-by-last-touched.base), [`_draft/journals-by-mood.base`](_draft/journals-by-mood.base).

The journals-by-mood template *should* work today since journal files already have proper frontmatter (`date`, `mood`, `tags`, `people`).

---

## Why these were demoted

A holistic review on 2026-05-23 surfaced that publishing broken templates was worse than not shipping them — they advertised query capability the vault couldn't deliver. Walked back; documented honestly. See [`ROADMAP.md`](../../ROADMAP.md) Phase 1a status.
