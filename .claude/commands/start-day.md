---
description: Morning kickoff. Sets intentions and MIT for the day.
---

## Context

Run: `date '+%A %B %d, %Y %H:%M'`

Read silently: `private/self-map.md`, `private/dashboard.md`

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
- Connect to mission/deadlines if relevant

## Identity Check (optional, when relevant)

If they're working on building a habit or making a change, ask:

"What would the person you're becoming do today?"

Or: "Who are you voting to be with this?"

Keep light — identity framing helps but shouldn't feel heavy.

## Rotating Element

**Check CLAUDE.md → Daily Rituals → Morning** for this user's configured rotating element.

**If not configured** (still has `[Example:...]` placeholders, or section is missing):
- Say: "Your daily rituals aren't configured yet. Want to set them up now, or skip for today?"
- If yes: Walk through the configuration flow from `/onboarding` → "Configure Daily Rituals" section
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
