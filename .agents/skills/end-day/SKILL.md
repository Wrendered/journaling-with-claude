---
name: end-day
description: Evening reflection ritual that captures how the day went, wins and lessons, runs the user's configured reflection questions (Seneca's questions, gratitude, etc.), checks habit streaks, and surfaces patterns repeating 3+ times.
when_to_use: |
  ALWAYS invoke this skill when the user winds down or signals end-of-day intent.
  Trigger phrases (any of these): "good night", "wrapping up", "end of day", "how did today go",
  "evening reflection", "let's review today", "before bed", "done for today",
  or any clear shift to retrospective framing about today.
allowed-tools: Read, Edit, Write, Bash, Glob
---

# End Day

Evening ritual. Captures the day, surfaces patterns, sets up tomorrow.

## Context

Run: `date '+%A %B %d, %Y %H:%M'`

Read silently: `private/self-map.md`, `private/dashboard.md`

## Tasks (if Todoist connected)

**Try to fetch completed tasks** using `mcp__todoist__find-completed-tasks` for today.

- If it works: Note completed tasks for the reflection.
- If it fails: Skip silently and continue.

## Pulse Check

Start with: "How are you feeling? (One word is fine, rambling is fine too.)"

Just receive it. Note energy level for pattern tracking.

## Ask

Then: "How'd the day go?"

Let them talk. Don't ask 5 questions.

## Follow up (maybe)

One question if needed:
- "Did you get your one thing done?"
- "What got in the way?"
- "Anything carrying to tomorrow?"

Or nothing.

## Evening Reflection

**Check AGENTS.md → Daily Rituals → Evening** for this user's configured reflection questions.

**If not configured** (still has `Option A/B/C` template text, or section is missing):
- Say: "Your evening reflection isn't configured yet. Want to set it up now, or skip for today?"
- If yes: Walk through the configuration flow from the onboarding skill → "Configure Daily Rituals" section
- If skip: Just capture what they shared and close

**If configured:** Use whatever they've set (Seneca's questions, gratitude, nothing, etc.).

## Habit Check (if tracking habits)

Glance at `dashboard.md` Habits section:
- Did they show up for their keystone habits today?
- If yes: Update streak, acknowledge briefly
- If missed: "Never miss twice. What's the 2-minute version for tomorrow?"

Don't belabor this — quick check, move on.

## Update

**Always update weekly journal (`private/journal/YYYY-Www.md`):**
- Append to today's entry in Raw Log:
  ```markdown
  **Evening:** Feeling: [pulse]. [what happened, how it went, reflection responses if any]
  ```
- Quote important words verbatim
- Note patterns, wins, or blocks

**Also append a log entry to `private/log.md`:**
- Format: `## [YYYY-MM-DD] evening | <one-line theme>`
- Body: 1-3 sentences capturing the essence (what happened, what landed). Long-form goes in the journal; the log is the timeline.
- This is what makes Claude able to grep the timeline cheaply later.

**Update `private/dashboard.md`:**
- Clear completed items from queue
- Update habit streaks if tracking

**Update `private/self-map.md` only if:**
- New long-term pattern discovered
- Mission clarity changed

## Surface patterns

If pattern (3x+):
- "You've mentioned [X] a few times. Worth naming?"
- "That's the third day you [pattern]. What's going on?"

If they hit MIT multiple days:
- "That's [N] days in a row. What's working?"

If they missed MIT:
- "What got in the way?" — no guilt

## Tomorrow Preview (if Todoist connected)

**Try to fetch tomorrow's tasks** using `mcp__todoist__find-tasks-by-date` with tomorrow's date.

- If tasks found: "Tomorrow you have: [list 2-3 key tasks]"
- If no tasks or not connected: Skip silently.

## Close

Short:
- "Rest."
- "Tomorrow: [their next thing if set]"
- Connect to mission if appropriate
