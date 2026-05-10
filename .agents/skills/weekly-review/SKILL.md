---
name: weekly-review
description: Weekly retrospective ritual that reviews open decisions in private/decisions/, surfaces patterns repeating 3+ times across the week's journal, organizes the weekly journal file with Summary and Highlight Quotes sections, runs the backup skill, commits the local-only private/ git repo, and updates dashboard tracking.
when_to_use: |
  ALWAYS invoke this skill when the user looks back at the past week.
  Trigger phrases (any of these): "weekly review", "let's review the week", "look back at this week",
  "reflect on the past 7 days", "organize the journal", "what happened this week".
  Also invoke if 7+ days have passed since the last weekly-review (check dashboard.md tracking)
  and the user opens the system without a specific topic.
allowed-tools: Read, Edit, Write, Bash, Glob, Grep
---

# Weekly Review

Once-per-week retrospective on decisions, experiments, and patterns. Organizes the weekly journal for future searchability.

Check: `private/system-instructions.md → Weekly Rhythm` for this user's configured timing. If that file is missing or silent, fall back to `AGENTS.md → Weekly Rhythm`.

## Tasks Context (if Todoist connected)

**Try to fetch completed tasks for the week** using `mcp__todoist__find-completed-tasks` with since/until for the past 7 days.

- If it works: Use completion data in the review. Note wins and patterns.
- If it fails: Skip silently and rely on journal for review.

**If not configured** (still has `[Example:...]` placeholders):
- Say: "Your weekly rhythm isn't configured yet. Want to set it up now, or just run the review?"
- If yes: Walk through the configuration from the onboarding skill or edit `private/system-instructions.md` directly
- If skip: Run review with sensible defaults

## Flow

### 1. Decision Review (5-10 min)
Pull all files from `private/decisions/`:
- **For each open decision:**
  - Any new information this week?
  - Any deadlines approaching?
  - Want to work on it next week?
- Update urgency/status
- Pick 1-2 for next week's decision work (see `private/system-instructions.md → Weekly Rhythm` for days)

### 2. Task Review (if Todoist connected) (5 min)
If completed tasks were fetched:
- "You completed [N] tasks this week." List highlights.
- Any tasks that rolled over repeatedly? Surface as pattern.
- Any overdue tasks to reschedule or delete?

### 3. Experiments & What's Working (5 min)
Review `dashboard.md` Active Experiments:
- How did experiments go? → Note in weekly journal
- What's working? (Keep doing)
- What's NOT working? (Adjust)
- Anything to try next week?

### 4. Organize Weekly Journal (10 min)

Open the current week's journal file (`private/journal/YYYY-Www.md`) and add the top sections:

**Required (for search agents):**
- `## Summary` — 2-4 sentences: what happened, major themes
- `## Highlight Quotes` — Pull the most significant quotes from Raw Log

**Optional (include what's relevant):**
- `## Keywords` — Searchable tags
- `## Patterns Noticed` — Recurring themes
- `## Relationships` — Key people mentioned
- `## Decisions` — Movement on open decisions
- `## Goals / Career` — Progress, setbacks
- `## Experiments` — What you're trying
- `## Emotional Themes` — What came up

**Clean up Raw Log:**
- Fix timestamps if needed
- Add structure if entries are messy
- Keep all raw content (don't delete)

### 5. Pattern Flagging (5 min)
Review this week's journal:
- Any themes repeating 3x+?
- Anything connecting to `history/` patterns?
- If pattern is stable/validated → move to `self-map.md`

### 6. Snapshot self-map.md if it changed (1 min)
After any edits to `self-map.md` this week (whether from step 5 above, a `consolidate-memory` pass, or ad-hoc updates), snapshot it so you can see how your synthesis evolved over time:

```bash
# Compare current to most-recent snapshot; only snapshot if different
LATEST=$(ls -t private/history/self-map-snapshots/self-map_*.md 2>/dev/null | head -1)
if [[ -z "$LATEST" ]] || ! diff -q private/self-map.md "$LATEST" > /dev/null; then
  cp private/self-map.md "private/history/self-map-snapshots/self-map_$(date +%Y-W%V).md"
  echo "Snapshotted: self-map_$(date +%Y-W%V).md"
fi
```

This is the "input never mutated" pattern — current `self-map.md` stays the live working copy, but each meaningful version is preserved alongside. Useful when you want to see how your self-understanding shifted over months/quarters without diving into git diffs.

**Snapshots are immutable.** Once a snapshot exists in `private/history/self-map-snapshots/`, do not edit it — including for attribution corrections, typo fixes, or restructuring. The whole point of a snapshot is to preserve "what we believed at that moment," errors and all. If a past self-map.md mis-attributed something, fix it in the *current* self-map.md (which the next snapshot will capture); the historical snapshot stays as evidence of what the synthesis used to be. If you find yourself wanting to edit a snapshot, that's a signal to take a *new* snapshot of the corrected current state instead.

### 7. Assessment Check (1 min)
Glance at `assessments/_index.md` Schedule:
- Anything due soon?

### 8. Next Week Preview
- What's the focus?
- Any big events/deadlines?
- Which decision(s) to work on? (Check `private/system-instructions.md` for decision work days)

### 9. Backup (1 min)
Run weekly backup of private files:
```bash
.claude/skills/backup/scripts/backup-private.sh
```
Confirm backup completed. If not set up yet, invoke the setup-backups skill.

### 10. Commit private/ to local git (1 min)
The `private/` folder is its own local-only git repo (no remote). A weekly commit gives you a permanent restore point alongside the Dropbox backup zip — git stores diffs you can grep through, while the zip is a flat snapshot.

```bash
cd private && git add -A && git status --short
```

Show the user what changed. If anything is staged, commit with a short message:

```bash
cd private && git commit -m "Weekly review YYYY-Www: <one-line theme>"
```

If `git status` is clean (no changes since last commit), skip silently.

**Never** add a remote to this repo. **Never** push it. It's local-only by design — the local git history + Dropbox backup are the two persistence layers; nothing leaves the machine via git.

## After

Update tracking in `dashboard.md`:
```
**Tracking:** Last done: [today] | Next due: [+7 days]
```

## Duration
~30 minutes total

## Flexibility
- Can be split across days if needed
- Core requirement: Hit decision review at least once per week
- Can skip other sections if light week
