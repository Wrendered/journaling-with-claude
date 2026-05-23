# Roadmap

Active work and backlog ideas for evolving this journaling + self-knowledge system. Updates as features ship. The pattern: mechanisms, conventions, and templates are public; personal content stays in each user's `private/`.

---

## Vision

The system is structurally a Karpathy "LLM Wiki" (raw → wiki → schema). The richest possible version of this tool, long-term, has:

- **Plain markdown that outlives any vendor.** ✅ Built.
- **LLM as editor + pattern-surfacer, human as steerer.** ✅ Built (Claude Code + Codex CLI + skills).
- **Multiple capture modes** (ritual, monologue, deep-dive, audio, mobile). ✅ Built (rituals + monologue); ⏳ audio/mobile pending.
- **Synthesized self-knowledge that grows in a traceable way.** ✅ Built (self-map + snapshots + graduation process).
- **Multiple views over the same data** — time, entity, pattern, state. ⏳ Obsidian Bases (in progress) addresses state + analytical views.
- **Belief-revision tracking** — when synthesis changes, *why*. ⏳ Not built. The deepest long-term compounding asset.
- **Outcome tracking on resolved decisions** — predictions vs reality. ⏳ Not built.

The discipline of writing things down such that future-you can disagree with past-you, *and the system can show you both clearly*, is the actual product.

---

## Active phases

### Phase 1 — Obsidian visualization + targeted wikilinks (PARTIALLY WALKED BACK 2026-05-23)

**Status:** Phase 1b shipped and kept. Phase 1a walked back. Phase 1c dropped.

**What landed and stays:**
- **1b** — Journal frontmatter `people: [alon, brody]` → `people: ["[[alon]]", "[[brody]]"]` backfilled across W01-W21. New entries follow the convention.

**What was walked back (2026-05-23):**
- **1a** — Three generic Bases templates were built at `templates/bases/`. A holistic review then confirmed they wouldn't return rows on the canonical example vault because `decisions/*.md` and `relationships/*.md` use body-text headers (`**Status:** Open`), not the YAML frontmatter Bases queries. Templates moved to `templates/bases/_draft/`; README documents the situation honestly. Three options to revive: add YAML frontmatter to ~20 files (~90 min), adjust queries, or skip Bases.
- **1c** — skill updates referencing Bases never started. Dropped.

**Lesson surfaced by the review:** publishing infrastructure-that-doesn't-actually-work-on-the-author's-vault is worse than not shipping. The graph view + Bases were hypotheses that ambient visualization would surface more patterns; the data so far says the cross-decade work via `deep-consolidate` surfaces more, faster, more usefully. Walked back rather than doubling down.

---

### Highest-leverage active work

**A. Add YAML frontmatter to decisions + relationships.** Per AGENTS.md schema, decision files should have `type / status / created / revisit / tags` frontmatter; relationship files should have `type / relation / since / last-touched`. Today they use body-text headers (`**Status:** Open`). This is schema drift, ~5 min per file, ~20 files total. Once landed: grep works better, wikilinks become more reliable, future Bases / queryable views become viable, AND nothing about LLM-reading workflow gets worse.

**B. Finish surfacing remaining deep-consolidate findings (incremental).** 16 of 24 closed; 8 remain `⏳ Pending` (mostly LOW severity). No rush; close them as relevance surfaces or in the next quarterly deep-consolidate pass.

---

### Phase 3 — Belief revision + outcome tracking (DEFERRED — moved to Backlog)

Originally framed as the next active phase. The holistic review (2026-05-23) recommended *not* proceeding until the existing graduation pipeline is empty — building a second log mechanism on top of a half-finished first one compounds infrastructure debt. Moved to Backlog for now. Will re-promote when the deep-consolidate findings are drained.

---

## Backlog

Captured for future consideration. Not committed; mature ideas graduate to Active phases.

**Scoping decision (2026-05-23):** the system stays inside its current stack — markdown vault + Claude Code + Codex CLI + optionally Obsidian. **Out of scope:** mobile/audio/photo capture, external integrations (calendar, health data, etc.). Future work is organized around five pillars below: improved skills, better organization, better linking, better searching, better visualization.

### 🛠️ Improved skills

- **Quarterly scheduled deep-consolidate** — wire the `schedule` skill to run `deep-consolidate` on `raw/historical-journal.txt` every 3 months. Each pass produces a fresh dated report. Status Tracker handles backlog across reports. ~30 min one-time setup.
- **Belief-revision log mechanism** *(was Phase 3)* — when a graduation revises an existing self-map entry, capture the prior belief, the evidence that overturned it, and when. Possibly its own file at `private/beliefs/`, or a new entry type in `log.md`. The deepest long-term investment when the existing graduation pipeline is mature.
- **Outcome tracking on closed decisions** *(was Phase 3)* — for resolved decisions (SF condo SOLD, Safeguards rejection, etc.), scheduled 6-month follow-up: was the outcome what you expected? Feeds back into self-map as calibration ("I tend to underestimate X").
- **Smarter proactive search triggers** — beyond the start-day/end-day historical-resonance check that just landed, extend to monologue, deep-dive, plan-week so history surfaces in more contexts. Light touch each time.

### 📁 Better organization

- **YAML frontmatter on decisions + relationships** — see Active work. Schema drift cleanup. ~90 min mechanical.
- **Periodic `_archive/` maintenance** — every quarter, review what's accumulated. Some becomes deletable; some becomes a permanent historical reference.
- **`tags.md` review** — controlled vocabulary drift naturally happens; periodic review keeps it lean.

### 🔗 Better linking

- **Cross-reference wikilinks in decision and relationship files** — after frontmatter cleanup, add `[[wikilinks]]` from each decision file to related relationship files and themes, and vice versa. One-time targeted backfill, similar in scope to the journal `people:` wikilink work.
- **Auto-detect entity mentions in journal prose** — Claude extracts proper-noun mentions during ritual processing and proposes wikilink additions. Possible skill enhancement to monologue + end-day.

### 🔍 Better searching

- **Smart Connections plugin** (Obsidian, free, local embeddings) — semantic "related notes" sidebar. Catches connections grep misses. Worth trying once the linking work has matured.
- **Search agent improvements** — smarter cross-year retrieval; better at recognizing themes vs literal text. Could include built-in "deep-search-this-pattern-across-history" mode.

### 📊 Better visualization

- **Local graph view** — works today in Obsidian. Becomes more useful as cross-references grow.
- **Backlinks pane** — works today. Lights up further as wikilinks expand.
- **Revisit Bases templates** — after frontmatter cleanup unblocks them. Aspirational: open-decisions dashboard, relationships-by-last-touched, mood-arc-over-time.
- **Mood arc visualization** — Bases + chart plugin, or dedicated chart. Year-over-year view of mood/tag patterns.
- **Calendar plugin** — month-grid sidebar tied to weekly journals; clickable date navigation. Small.

---

## Completed phases

### Phase 0 — Obsidian minimal setup (2026-05-22, PR #15)

`.obsidianignore` + `.gitignore` update + README "Using Obsidian (optional)" section. Lets anyone open the project folder as an Obsidian vault without restructuring; per-user `.obsidian/` state never leaks publicly.

### Phase 1b — Wikilink convention for journal `people:` arrays (2026-05-23, PR #16)

Backfilled 7 weekly journals from `people: [alon, brody]` → `people: ["[[alon]]", "[[brody]]"]`. New entries use the convention. Documented in ROADMAP. Phase 1a (Bases templates) shipped in same PR but walked back in PR #17.

### Cleanup + history wiring (2026-05-23, PR #17)

Walked back broken Bases templates (moved to `_draft/`, then deleted entirely in follow-up). Wired 9-year history into `start-day` and `end-day` skills via "Historical resonance" sections. Graduated 4 more deep-consolidate findings (§1.5, §3.2, §3.4, §4.4) — total 16 of 24 closed.

### Prior infrastructure (Mar-May 2026)

- Dual Claude Code + Codex CLI compatibility (PRs #3, #4)
- Public-repo privacy hardening, hooks (PRs #6, #8, #11)
- Phase 2 system-instructions split (PR #7)
- Snapshot mechanism for self-map evolution (PR #9)
- Graduation process + citation format (PR #10)
- Status Tracker mechanism (PR #12)
- Skill sweep aligning all 12 skills with current conventions (PR #13)
- `couple/` exercises (PRs prior + #14)

---

## How to update this file

- **When a backlog item matures or you start it:** promote it from Backlog to Active phases. Add a phase number, goals, components, public/per-user split, status.
- **When a phase completes:** move it to Completed phases below with the merge date / PR number.
- **When a new idea surfaces:** drop it in Backlog. No commitment implied. Don't worry about ordering until it matures.

Public-private split is the same as the rest of the project: mechanisms, conventions, templates → public. Personal content → private.
