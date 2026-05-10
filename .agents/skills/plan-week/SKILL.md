---
name: plan-week
description: Forward-looking weekly planning ritual that sets the week's focus, checks habits, surfaces open decisions and deadlines from private/decisions/, and optionally creates Todoist tasks for planned actions.
when_to_use: |
  ALWAYS invoke this skill when the user looks ahead at the upcoming week.
  Trigger phrases (any of these): "plan my week", "weekly planning", "set up the week",
  "what should I focus on this week", "set weekly intentions", "this week's focus".
  Also invoke at the start of a configured planning day (Sun/Mon typical) if the user opens
  the system without a specific topic.
allowed-tools: Read, Edit, Write, Bash, Glob
---

# Plan Week

Forward-looking weekly planning. Different from weekly-review (retrospective).

## Context

Run: `date '+%A %B %d, %Y'`

Read: `private/dashboard.md` (current state, habits, active decisions)

Check: `private/system-instructions.md → Weekly Rhythm` for this user's configured timing and cadence. If that file is missing or silent, fall back to `AGENTS.md → Weekly Rhythm`.

## Tasks (if Todoist connected)

**Try to fetch this week's tasks** using `mcp__todoist__find-tasks-by-date` with startDate: "today" and daysCount: 7.

- If it works: Use task list to inform planning discussion.
- If it fails: Skip silently and rely on dashboard.md for planning.

## Purpose

**Timing:** Check `private/system-instructions.md` for when user prefers to run this (Sun/Mon typical, but configurable).

**If not configured** (still has `[Example:...]` placeholders):
- Say: "Your weekly rhythm isn't configured yet. Want to set it up now, or just run the planning?"
- If yes: Walk through the configuration from the onboarding skill or edit `private/system-instructions.md` directly
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
- Which 1-2 to work on this week? (Check `private/system-instructions.md → Weekly Rhythm` for decision work days)

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
