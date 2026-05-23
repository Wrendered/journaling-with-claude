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

### Highest-leverage active work (replacing Phase 3 as the current focus)

**A. Finish surfacing the deep-consolidate findings.** `private/_deep-consolidate-report-2026-05-10.md` identified 24 cross-decade patterns; 12 were graduated into `self-map.md`; 12 remain `⏳ Pending`. Closing the most active ones (especially loops directly relevant to live decisions) puts cross-decade material into every session's session-start read.

**B. Wire 8-year history into daily skill flows.** Currently `start-day`, `end-day`, `plan-week`, and `monologue` rarely or never reach into `history/themes-*.md` or `historical-journal.txt`. Daily rituals (highest-frequency touchpoints) skip the richest material. Small skill-text additions surface relevant historical content reflexively rather than only when explicitly asked.

Both A and B are inside-the-existing-system work. Neither adds a tool. Both directly address the "history feels underutilized" frustration.

---

### Phase 3 — Belief revision + outcome tracking (DEFERRED — moved to Backlog)

Originally framed as the next active phase. The holistic review (2026-05-23) recommended *not* proceeding until the existing graduation pipeline is empty — building a second log mechanism on top of a half-finished first one compounds infrastructure debt. Moved to Backlog for now. Will re-promote when the deep-consolidate findings are drained.

---

## Backlog

Captured for future consideration. Not committed; mature ideas graduate to Active phases.

### Phase 3 (deferred from active) — Belief revision + outcome tracking

**Goal:** Make the system capture not just *what* you believe but *how that belief has changed and what evidence changed it*. Over years, becomes a record of your own self-model's evolution you can inspect, disagree with, learn from.

**Two mechanisms:**
- **Belief-revision log.** When a graduation revises an existing self-map entry, capture: prior belief, evidence that overturned it, when. Possibly its own file at `private/beliefs/`, or a new entry type in `log.md`.
- **Outcome tracking on closed decisions.** For decisions that resolve, scheduled 6-month follow-up: was the outcome what you expected? Better? Worse? Feeds back into self-map.

**Why this got deferred:** the May 10 deep-consolidate produced 24 findings; only 12 are graduated. Building a second log mechanism on a half-finished first one compounds infrastructure debt. Re-promote to Active when the existing pipeline is drained.

### #2 Obsidian plugins worth adopting (after Phase 1)

- **Smart Connections** (free, local embeddings) — semantic "related notes" sidebar. Catches connections grep misses. Underrated.
- **Calendar** — month-grid sidebar tied to weekly journals; clickable date navigation.
- **Templater** — dynamic templates (`<% tp.date.now() %>`, prompts) for daily/weekly note scaffolding.
- **Periodic Notes** — opinionated daily/weekly/monthly/yearly note structure.

Phase boundary: install one at a time, evaluate, keep or remove.

### #4 Capture flow improvements

- **Mobile capture** — iOS Shortcut that writes a markdown file into `raw/inbox/`. The next ritual session processes the inbox into journal + relationship files.
- **Audio capture** — voice memo → transcript → raw layer. Local Whisper or paid service. Captures things you wouldn't write down.
- **Photo journals with captions** — date-stamped, optionally semantic-search via embeddings.

### #6 Quarterly scheduled deep-consolidate

Use the `schedule` skill to run `deep-consolidate` on `raw/historical-journal.txt` every 3 months. Each pass produces a fresh `_deep-consolidate-report-YYYY-MM-DD.md`. New findings graduate per the existing process. Status Tracker mechanism handles backlog across reports.

Effort: ~30 min to wire up.

### #7 External integrations

- **Todoist** — already integrated for tasks. Could expand: pull completed-tasks summary into weekly-review automatically.
- **Calendar (Google/iCal)** — events that contextualize journal entries (travel, meetings, milestones).
- **Health data** (sleep, HRV, activity) — sometimes mood patterns track physiological state more than emotional state. Worth correlating.

Privacy posture: all consumed data must come *in* to the local vault; nothing about journal content leaves the machine.

### #8 Cross-decade pattern detection enhancements

- **Belief-revision log over years** (depends on Phase 3) — visualize how core beliefs have shifted.
- **Auto-detected entity recognition** in journal prose, not just `people:` arrays — Claude extracts mentions and proposes wikilink additions during ritual processing.
- **Mood arc visualization** across months/years — Bases + a chart plugin, or a dedicated visualization.
- **Decision outcome calibration** — for resolved decisions, did pre-mortems play out? Develops a sense for which lenses serve you and which are noise.

### #9 Quote bank

A `quotes/` folder (public for shared aphorisms, private for personal quotes) cross-referenced with where each quote shows up in journals or theme files. Useful when a phrase keeps showing up across years.

### #10 Speaking aloud as ritual

Voice-driven monologue → transcript → existing monologue skill pipeline. Different cognitive mode than typing.

---

## Completed phases

### Phase 0 — Obsidian minimal setup (2026-05-22, PR #15)

`.obsidianignore` + `.gitignore` update + README "Using Obsidian (optional)" section. Lets anyone open the project folder as an Obsidian vault without restructuring; per-user `.obsidian/` state never leaks publicly.

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
