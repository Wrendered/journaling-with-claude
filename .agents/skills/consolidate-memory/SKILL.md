---
name: consolidate-memory
description: Periodic lint pass over the personal vault (private/) that detects contradictions across pages, stale claims that no longer reflect current state, orphan pages with no inbound links from indexes, and concepts mentioned in journal but lacking their own dedicated file. Reports findings without auto-changing files; user decides what to address.
when_to_use: |
  Invoke this skill when the user wants a maintenance pass over their private vault.
  Trigger phrases (any of these): "consolidate my memory", "lint my vault", "audit private",
  "check for contradictions", "find stale notes", "vault maintenance",
  "what's drifted in my self-map", "are my files still accurate".
  Also invoke periodically during weekly-review (every 4-6 weeks) to keep the wiki coherent.
context: fork
paths:
  - "private/**"
allowed-tools: Read, Glob, Grep, Bash, Task
---

# Consolidate Memory

Periodic maintenance pass over the user's personal vault. Surfaces drift without auto-correcting — the user decides what to address.

This is the Karpathy LLM Wiki "lint" operation: contradictions, stale claims, orphans, missing pages.

## When to Use

- User explicitly asks for a vault audit / maintenance pass
- Every 4-6 weeks during weekly-review (suggest, don't force)
- After any major event that might have shifted self-knowledge (job change, breakup, big realization) — old claims may now be wrong
- Before a deep-dive that's going to lean heavily on `self-map.md` for context

## What to Check

### 1. Contradictions across pages

Cross-reference claims in `self-map.md`, `history/themes-*.md`, and recent journal entries. Look for:
- Claims in `self-map.md` that recent entries directly contradict
- Theme files (`history/themes-<topic>.md`) and `self-map.md` making opposing claims about the same pattern
- Decisions whose status (`open` / `resolved`) doesn't match the journal narrative

Use grep to find candidate pairs. Report with file paths and line numbers.

### 2. Stale claims

Read `self-map.md` and `history/themes-*.md`. Flag:
- Claims with `last-touched` more than 6 months old that haven't been validated
- Claims that reference circumstances that have changed (job, relationship, location, health)
- Claims using absolute language ("I always...", "I never...") that recent entries contradict

### 3. Orphan pages

For each file in `private/decisions/`, `private/relationships/`, `private/history/themes-*.md`:
- Check if it's linked from `private/_index.md` or the relevant folder `_index.md`
- Check if it's mentioned anywhere in journal entries from the last 90 days
- Flag pages with no inbound references — they may be candidates for `private/archive/`

### 4. Missing pattern coverage

Grep recent journal entries (last 90 days) for recurring themes:
- If a pattern appears 3+ times across journal entries
- AND `self-map.md` doesn't yet name it
- THEN flag it as a candidate to add as a sharpened entry in `self-map.md` (or, if there's enough multi-year material, a new `history/themes-<topic>.md`)

### 5. Tag drift

Read `private/tags.md`. Compare to actual tags in use across `private/**/*.md` frontmatter:
- Tags used but not in the controlled vocabulary → flag as drift
- Tags in the vocabulary but never used → candidates for removal
- Multiple tags for the same concept (e.g., `career`, `career-move`, `job`) → flag as redundancy

### 6. Index drift

For each `_index.md`, verify:
- Files listed in the index actually exist
- Files in the folder are listed in the index (or reasonably elidable)

## Output Format

Single report file: `private/_consolidation-report.md` (gitignored as part of `private/`).

Structure:

```markdown
# Vault Consolidation Report

**Date:** [today]
**Scope:** [what was scanned]

## 1. Contradictions Found
[list with file paths]

## 2. Stale Claims
[list with file paths and last-touched dates]

## 3. Orphan Pages
[list with reasoning]

## 4. Patterns Worth Adding to self-map.md
[recurring themes from journal that aren't yet named in self-map.md]

## 5. Tag Drift
[tags in use vs. tags.md]

## 6. Index Drift
[files in folders vs files in indexes]

---

## Recommended Actions (user decides)
[prioritized list of what to address]
```

## What NOT to do

- Do not auto-edit files based on findings — surface them, let user decide
- Do not move pages to `archive/` without explicit approval
- Do not delete tags from `tags.md` without the user reviewing
- Do not edit `self-map.md` directly — surface candidate sharpenings/additions, the user decides

## Approach

For large vaults, use parallel subagents:
- Agent 1: Read `self-map.md` + recent journal entries, look for contradictions
- Agent 2: Walk `history/themes-*.md` and `decisions/`, check each for staleness and orphan status
- Agent 3: Grep journal for recurring themes vs. existing self-map entries
- Agent 4: Audit tags + indexes

Consolidate findings into the single report.

For small vaults (under ~50 files), a single sequential pass is fine.

## Graduating Findings (when the user decides to act)

The report (or a deep-consolidate cross-decade pass over `raw/historical-journal.txt`) surfaces candidates. When the user picks one to graduate into `self-map.md`, follow this process.

> **Status tracking.** Each report should include a **Status Tracker** table near the top — one row per finding, with states `✅ Graduated · ✓ Already in vault · ⏳ Pending · ❌ Not graduating`. Update the cell when a finding is acted on. Future sessions can grep `⏳ Pending` across all `_*report*.md` files at `private/` root to surface what's open across reports. This is the durable "save for later" mechanism — don't rely on the report being re-read top-to-bottom.

**1. One at a time, not batch.** Each graduation is a real edit to the user's synthesis of themself. Batches blur sources and lose attribution.

**2. Verify the source quote verbatim.** Re-read the cited entry in `raw/historical-journal.txt` or `journal/YYYY-Www.md`. Quote integrity matters; never paraphrase.

**3. Decide where it lands.** Candidate sections of `self-map.md`:
- **Drivers** / "What Energizes" — motivational, identity, what-pulls-me content
- **Patterns (Bugs)** — loops, avoidance, traps to watch
- **What Works** — active practices, orientations, counter-frames
- **Cross-Framework Patterns** table — one-line patterns linking multiple frameworks

**4. Snapshot self-map.md first.** The `weekly-review` skill auto-snapshots; for ad-hoc graduations between weekly-reviews, copy manually:

```bash
cp private/self-map.md "private/history/self-map-snapshots/self-map_$(date +%Y-%m-%d)_pre-<short-finding-name>.md"
```

**Snapshots are immutable** — once written, do not edit them, even to correct attribution or typos. They preserve "what we believed at that moment," errors and all. Fix issues in the current `self-map.md` instead; the next snapshot captures the correction. If you find yourself wanting to edit a snapshot, take a *new* snapshot of the corrected state.

**5. Edit using this citation format:**

```markdown
- **<Pattern name>** — *"<verbatim quote>"* ([YYYY-MM-DD](raw/historical-journal.txt)). <Brief gloss / why this matters>. Recurrence: <other dated occurrences if any>.
```

For **revisions** to existing entries (not pure additions): preserve the original framing as-is, then append a sub-bullet *"Revised YYYY-MM-DD per &lt;source&gt; — &lt;what's now nuanced or corrected&gt;."* Don't rewrite over the original; layer on top so the evolution is visible.

**6. Append a one-liner to `log.md`:**

```markdown
## [YYYY-MM-DD] graduation | <pattern name> → self-map.md (<section>)

Source: <source file or report>. Why now: <user's reason>. Snapshot: <snapshot filename>.
```

**7. Commit private repo** with a message naming the source: `Graduate <pattern> from <source> → self-map.md (<section>)`.

### Citation conventions

- Always `(YYYY-MM-DD)` — exact date only, no "around X" or relative dates.
- Markdown link the source: `[YYYY-MM-DD](path/to/source.md)`.
- Multi-occurrence patterns: primary citation inline, then `Recurrence: <date1>, <date2>` so future readers can grep all sources.
- Claude framings the user has explicitly adopted: `(Claude's framing, adopted YYYY-MM-DD)` — provenance honest.
- Claude framings the user has NOT explicitly adopted: do NOT graduate. Hold in the report or theme file until the user's own words match.

## Related Skills

- `weekly-review` — surfaces patterns from the past 7 days; this skill is the multi-week version
- `deep-dive` — works on a single specific topic; this skill works across the vault
- `import-history` — adds NEW material to the vault; this skill maintains EXISTING material
