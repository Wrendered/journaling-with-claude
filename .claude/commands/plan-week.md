---
description: Weekly planning. Set focus, habits, and intentions for the week ahead.
---

## Context

Run: `date '+%A %B %d, %Y'`

Read: `private/dashboard.md` (current state, habits, active decisions)

Check: `CLAUDE.md → Weekly Rhythm` for this user's configured timing and cadence.

## Tasks (if Todoist connected)

**Try to fetch this week's tasks** using `mcp__todoist__find-tasks-by-date` with startDate: "today" and daysCount: 7.

- If it works: Use task list to inform planning discussion.
- If it fails: Skip silently and rely on dashboard.md for planning.

## Purpose

Forward-looking planning for the week. Different from `/weekly-review` (retrospective).

**Timing:** Check CLAUDE.md for when user prefers to run this (Sun/Mon typical, but configurable).

**If not configured** (still has `[Example:...]` placeholders):
- Say: "Your weekly rhythm isn't configured yet. Want to set it up now, or just run the planning?"
- If yes: Walk through the configuration from `/onboarding` or edit CLAUDE.md directly
- If skip: Run planning with sensible defaults

## Flow

### 1. What's the focus this week?

One theme or priority. Not a task list.

Examples:
- "Ship the feature"
- "Rest and recover"
- "Make progress on [open decision]"
- "Build the morning routine habit"

### 2. Habits check

If they have habits in dashboard.md:
- Which to continue?
- Any to add, pause, or adjust?
- What's the 2-minute version if starting something new?

If no habits yet, ask if they want to set one up. Use Atomic Habits framework:
- Identity: Who are you trying to become?
- Habit: What's one small thing that person would do?
- Stack: What existing routine could you attach it to?

### 3. Decisions on deck

Glance at `private/decisions/`:
- Any with approaching deadlines?
- Which 1-2 to work on this week? (Check CLAUDE.md → Weekly Rhythm for decision work days)

### 4. Commitments and deadlines

Anything time-sensitive this week? Surface from dashboard or ask.

**If Todoist connected:** Show upcoming tasks with due dates this week.

### 5. Create tasks (if Todoist connected)

For any concrete actions discussed, offer to create Todoist tasks:
- "Want me to add these to Todoist?"
- Route to appropriate project (Life Admin, Houses, etc.)
- Set due dates based on discussion

## Output

Update `private/dashboard.md`:
- This Week → Focus
- Habits section if changed
- Any new actions with deadlines

## Close

Keep it light. The plan is a compass, not a contract.

"What would make this a good week?"
