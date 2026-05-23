# Bases templates

Live tables/views over the vault's frontmatter, using Obsidian's [Bases](https://obsidian.md/help/bases) core plugin (left beta early 2026). Each `.base` file in this folder is a generic starting point that should work on any consumer's vault — copy or symlink one into your active vault location and customize from there.

**Requires:** Obsidian 1.9+ with Bases enabled (Settings → Core plugins → Bases).

---

## Templates available

| File | What it shows | Frontmatter it reads |
|---|---|---|
| [`open-decisions.base`](open-decisions.base) | All files in `decisions/` with `status: open`, sorted by `revisit` date | `status`, `revisit`, `created`, `tags` |
| [`relationships-by-last-touched.base`](relationships-by-last-touched.base) | All files in `relationships/` sorted by `last-touched` (most stale first) | `relation`, `since`, `last-touched` |
| [`journals-by-mood.base`](journals-by-mood.base) | Weekly journal entries filtered by a mood tag of your choice | `date`, `week`, `mood`, `tags`, `people` |

---

## How to use

1. **Copy** one of the `.base` files into your vault wherever you want it to appear (e.g., a top-level `dashboards/` folder, or just at the vault root).
2. **Open it in Obsidian** — it renders as an interactive table. Drag columns, change filters, save the view.
3. **Edit the YAML** if you want to customize the query. The format is documented at [obsidian.md/help/bases](https://obsidian.md/help/bases).

**Important:** The queries assume specific frontmatter keys (`status`, `revisit`, `last-touched`, `mood`, etc.). If your vault doesn't use those keys, the base returns an empty table — either rename your frontmatter to match or edit the base.

---

## Per-user vs shared

The templates here are **public and generic** — designed to work on any vault that follows the project's frontmatter conventions. They live in `templates/bases/` (tracked in git).

If you build personalized Bases with filters specific to your life (e.g., "Anthropic-process decisions only", "journal entries during the Australia trip"), put those in `private/bases/` (gitignored with the rest of `private/`). They never leave your machine.

---

## Conventions for new templates

When adding to `templates/bases/`:

- Use only frontmatter keys that exist across many users' vaults — the documented schema in `AGENTS.md → Frontmatter` + per-skill conventions
- Don't hardcode personal values (e.g., specific names, employers, locations) — leave those as `[customize me]` placeholders or skip them
- Add the new template to the table above with a one-line description
