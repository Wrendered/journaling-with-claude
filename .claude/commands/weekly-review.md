---
description: Review decisions, experiments, and patterns. Retrospective.
---

# /weekly-review

> Once-per-week check-in on decisions, experiments, and patterns.

Check: `CLAUDE.md → Weekly Rhythm` for this user's configured timing.

**If not configured** (still has `[Example:...]` placeholders):
- Say: "Your weekly rhythm isn't configured yet. Want to set it up now, or just run the review?"
- If yes: Walk through the configuration from `/onboarding` or edit CLAUDE.md directly
- If skip: Run review with sensible defaults

## Trigger
User says `/weekly-review` or it's been 7+ days since last one.

## Flow

### 1. Decision Review (5-10 min)
Pull all files from `private/decisions/`:
- **For each open decision:**
  - Any new information this week?
  - Any deadlines approaching?
  - Want to work on it next week?
- Update urgency/status
- Pick 1-2 for next week's decision work (see CLAUDE.md → Weekly Rhythm for days)

### 2. Experiments & What's Working (5 min)
Review `dashboard.md` Active Experiments:
- How did experiments go? → Note in weekly journal
- What's working? (Keep doing)
- What's NOT working? (Adjust)
- Anything to try next week?

### 3. Organize Weekly Journal (10 min)

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

### 4. Pattern Flagging (5 min)
Review this week's journal:
- Any themes repeating 3x+?
- Anything connecting to `history/` patterns?
- If pattern is stable/validated → move to `self-map.md`

### 5. Assessment Check (1 min)
Glance at `assessments/_index.md` Schedule:
- Anything due soon?

### 6. Next Week Preview
- What's the focus?
- Any big events/deadlines?
- Which decision(s) to work on? (Check CLAUDE.md for decision work days)

### 7. Backup (1 min)
Run weekly backup of private files:
```bash
.claude/skills/backup/scripts/backup-private.sh
```
Confirm backup completed. If not set up yet, run `/setup-backups`.

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
