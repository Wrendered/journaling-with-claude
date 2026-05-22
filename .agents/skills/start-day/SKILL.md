---
name: start-day
description: Morning kickoff ritual that captures a pulse check, sets the MIT (Most Important Task), surfaces today's tasks if Todoist is connected, and runs the user's configured rotating element (Stoic prep, gratitude, values check-in, etc.).
when_to_use: |
  ALWAYS invoke this skill when the user opens a new day or signals morning intent.
  Trigger phrases (any of these): "good morning", "starting my day", "morning check-in",
  "what should I focus on today", "set my MIT", "let's get going", "ready to start",
  or any first message of a new calendar day that mentions intentions or tasks.
allowed-tools: Read, Edit, Write, Bash, Glob
---

# Start Day

Morning ritual. Sets intention and the one thing that matters today.

## Context

Run: `date '+%A %B %d, %Y %H:%M'`

Read silently in this order: `private/system-instructions.md`, `private/_index.md`, `private/self-map.md`, `private/dashboard.md`. (System-instructions and _index are also session-start reads in AGENTS.md — listed here for the case where this skill is invoked mid-session and they haven't been loaded yet.)

## Tasks (if Todoist connected)

**Try to fetch today's tasks** using `mcp__todoist__find-tasks-by-date` with startDate: "today".

- If it works: You have task integration. Surface today's tasks and overdue items when asking about MIT.
- If it fails or no tasks found: Skip this section silently. Continue with the normal flow.

Don't error out if Todoist isn't configured. Just proceed without task context.

## Pulse Check

Start with: "How are you feeling? (One word is fine, rambling is fine too.)"

Just receive it. Don't problem-solve unless asked. Note energy level for pattern tracking.

## Ask

Then ask for today's **MIT (Most Important Task)**.

**If tasks were fetched:** Show today's tasks and overdue items, then ask: "Any of these your MIT, or something else?"

Adapt as needed: explain concepts if user is new, help them pick if they're torn.

Wait for their answer.

## After they answer

- Update `private/dashboard.md`: Set MIT Today
- Append to weekly journal (`private/journal/YYYY-Www.md`) under today's date:
  ```markdown
  ### [Day] [Date]
  **Morning:** Feeling: [pulse]. MIT: [their MIT]. [rotating element response if any]
  ```
  **Attribution:** if the rotating element produces a reframe of what they said (a Stoic recasting, a CBT thought-test, etc.), label it `Claude's framing:` and keep their words separate. See `AGENTS.md → Attribution Rule` — the `check-attribution` hook will flag blended entries.
- Append a log entry to `private/log.md`:
  ```markdown
  ## [YYYY-MM-DD] morning | <MIT or theme>

  <one-line context: feeling, what's pulling them today>
  ```
  The log is the timeline; the journal is the narrative. Both get updated.
- Connect to mission/deadlines if relevant

## Identity Check (optional, when relevant)

If they're working on building a habit or making a change, ask:

"What would the person you're becoming do today?"

Or: "Who are you voting to be with this?"

Keep light — identity framing helps but shouldn't feel heavy.

## Rotating Element

**Check `private/system-instructions.md → Daily Rituals → Morning`** for this user's configured rotating element. If that file is missing or silent, fall back to `AGENTS.md → Daily Rituals`.

**If not configured** (still has `[Example:...]` placeholders, or section is missing):
- Say: "Your daily rituals aren't configured yet. Want to set them up now, or skip for today?"
- If yes: Walk through the configuration flow from the onboarding skill → "Configure Daily Rituals" section
- If skip: Just close after MIT, no rotating element

**If configured:** Use whatever they've set. The rotating element is personal preference — some want Stoic prep, some want gratitude, some want nothing.

## Close

Short:
- "Go."
- "One thing. Get it done."
- "[X] days to [deadline]."

## Observe (internal)

Notice:
- Energy in their words
- Hesitation or avoidance
- Same MIT as yesterday?
- Pattern emerging?

If pattern (3x+), surface it: "This is the third time you've set this. What's in the way?"

## People Mentioned

If user mentions someone by name (friend, partner, collaborator):
1. List `private/relationships/` filenames to check if they have a file
2. If file exists → Read it for context
3. If no file → Use search agent to find journal mentions
4. If significant person with no file → Offer to create one

Don't let key people slip by without context.
