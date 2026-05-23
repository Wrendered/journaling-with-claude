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

### Phase 1 — Obsidian visualization + targeted wikilinks

**Goal:** Make Obsidian's Bases and backlinks pane genuinely useful on the existing vault with minimal file churn. Skip the global graph view (it's mostly aesthetic past a few hundred notes). Bases delivers analytical aggregation Claude Code can't already do; targeted wikilinks light up backlinks for high-value entities (people, decisions).

**Components:**

- **1a (public):** Build 3-4 generic Bases templates that work on any consumer's vault: open decisions table, relationships sorted by `last-touched`, journals filtered by mood/tag. Live at `templates/bases/`.
- **1b (per-user):** Convert journal frontmatter `people: [alon, brody]` → `people: ["[[alon]]", "[[brody]]"]`. Targeted backfill across existing weekly journals. Document the convention for future entries.
- **1c (public):** Update skills (`weekly-review`, `consolidate-memory`) to mention Bases conventions where relevant. Update `add-framework` to drop Bases template references for habit-tracking frameworks.

**Status:** in progress (2026-05-23).

**Out of scope (deliberately):** wholesale in-prose wikilink conversion across 250 files. Marginal ROI; Claude grep already serves the "find references" use case better than backlinks pane.

---

### Phase 3 — Belief revision + outcome tracking

**Goal:** Make the system capture not just *what* you believe but *how that belief has changed and what evidence changed it*. Over years, this becomes the most valuable artifact — a record of your own self-model's evolution that you can inspect, disagree with, and learn from.

**Two mechanisms (design pending):**

- **Belief-revision log.** When a graduation revises an existing self-map entry, also capture: what was the prior belief, what evidence overturned it, when. Lives somewhere accessible — probably `log.md` with a new `belief-revision` type, possibly cross-referenced from self-map snapshots. Design questions:
  - Per-graduation? Or batched into the snapshot?
  - Should it be its own file (`private/beliefs/`)?
  - How does it differ from the existing graduation log entry?
- **Outcome tracking on closed decisions.** For decisions that resolve (SF condo SOLD, Safeguards rejection, etc.), schedule a 6-month follow-up: was the outcome what you expected? Better? Worse? What does this teach you? Feeds back into self-map as "I tend to under/overestimate X."

**Public deliverables:**
- Skill updates (`weekly-review`, `consolidate-memory`, possibly `deep-dive`) that invoke these mechanisms.
- Convention documented in the skills + a `templates/beliefs/` example.
- Optional: a Base view "decisions with outcome review pending."

**Per-user deliverables:**
- Their actual belief-revision entries in `private/`.
- Outcome retrospectives on their resolved decisions.

**Status:** design pending. Will write a design doc inside this roadmap once Phase 1 lands.

**Why this is the highest-leverage thing:** the difference between "I have a lot of notes about myself" and "I have a record of how my understanding of myself has changed and what evidence changed it." That's the long-term compounding asset.

---

## Backlog

Captured for future consideration. Not committed; mature ideas graduate to Active phases.

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
