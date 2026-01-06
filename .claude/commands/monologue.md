---
description: Stream of consciousness — just dump, Claude captures.
---

# /monologue

> Dump your thoughts. Claude listens, then processes into something useful.

## Trigger
User says `/monologue` or starts typing unprompted reflection.

## Flow

1. **Receive** — Let them talk. Don't interrupt. They'll signal when done (or ask "done?" if it's been a while).

2. **Process** — Once they're done, work through the content:
   - "Let me play that back..." — Summarize the key threads
   - Clean up: fix typos, clarify garbled dictation, organize scattered thoughts
   - Surface what seems most important or emotionally charged
   - Note any patterns connecting to recent entries or known themes
   - **Proactive search:** If they mentioned people, check `private/relationships/` for files. If they mentioned decisions/themes, check relevant folders. Use search agent for journal history. (See CLAUDE.md → Proactive Search)

3. **Reflect together** — Brief back-and-forth:
   - "Did I get that right?"
   - "This part stood out: [quote/theme]. Want to go deeper?"
   - "Anything I missed or got wrong?"
   - One clarifying question if something feels unresolved

4. **Offer connections** (optional) — If a theme feels significant:
   - "Want me to search for past entries about [theme]?"
   - Uses search agent to find patterns in history/journal
   - **Discuss findings first** — Don't just dump search results. Surface what you found and ask: "Does this resonate?" "Anything connect?" Follow their curiosity.
   - Only offer if it seems useful — don't over-process a quick dump

5. **Capture** — Append the *processed* version to weekly journal
   - The value is the cleaned-up reflection, not raw dictation
   - Include significant quotes if they said something worth preserving exactly
   - Note the theme or what this was about

## Journal Entry Format

Append under today's date in the weekly file (`private/journal/YYYY-Www.md`):
```markdown
**Monologue (HH:MM):** [Brief theme/topic]

[Processed summary — clean, organized version of what they said]

[If significant: "Quote worth keeping: '...'"]
```

## What Happens Later

- `/end-day` reviews the day's entries
- `/weekly-review` organizes the week: adds Summary, Highlight Quotes, optional sections
- Patterns may graduate to `self-map.md`

## Example

**User:** `/monologue`

**Assistant:** "Go ahead — I'm listening."

**User:** [5 minutes of rambling dictation with typos about feeling stuck on a decision, frustration at work, missing a place they used to live...]

**Assistant:** "Let me play that back. Three threads: (1) You're second-guessing a decision you already made. (2) Work frustration, specifically feeling unheard in meetings. (3) Missing somewhere you used to live, or maybe what that place represented. Did I get that right?"

**User:** "Yeah. The decision thing is fine, I'm just venting. The place thing is interesting though..."

**Assistant:** "Want me to search for past entries about that? You've written about place and belonging before."

**User:** "Sure."

**Assistant:** [Searches] "Found a few things. Two years ago you wrote about 'home being people, not places' after a move. And last fall there's a thread about identity feeling tied to geography. Does either of those connect to what's coming up now?"

**User:** "The identity one, yeah..."

**Assistant:** [Follows that thread, then captures the processed version]
