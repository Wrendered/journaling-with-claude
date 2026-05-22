---
name: monologue
description: Stream-of-consciousness capture flow that lets the user dump thoughts without interruption, then processes the dump into a clean journal entry, surfaces themes, and offers connections to past entries.
when_to_use: |
  ALWAYS invoke this skill when the user starts processing out loud rather than asking a question.
  Trigger phrases (any of these): "let me ramble", "I need to talk", "brain dump", "venting",
  "stream of consciousness", "just thinking out loud", "I have a lot on my mind".
  Also use when the user starts a long unprompted reflection that isn't a question, or when
  dictation produces a long unstructured passage about feelings, patterns, or experiences.
allowed-tools: Read, Edit, Write, Bash, Glob, Grep
---

# Monologue

Receive a thought-dump, then process it into something useful.

## Trigger

User explicitly invokes this, OR starts typing unprompted reflection that's clearly a dump (not a question).

## Flow

1. **Receive** — Let them talk. Don't interrupt. They'll signal when done (or ask "done?" if it's been a while).

2. **Process** — Once they're done, work through the content:
   - "Let me play that back..." — Summarize the key threads
   - Clean up: fix typos, clarify garbled dictation, organize scattered thoughts
   - Surface what seems most important or emotionally charged
   - Note any patterns connecting to recent entries or known themes
   - **Proactive search:** If they mentioned people, check `private/relationships/` for files. If they mentioned decisions/themes, check relevant folders. Use search agent for journal history. (See AGENTS.md → Proactive Search)

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

5. **Capture** — Append to weekly journal using the attribution split below
   - Their verbatim words and your processing go in distinct sub-sections
   - The `check-attribution` hook will flag entries that blend the two
   - See `AGENTS.md → Attribution Rule` for the full convention; the personal recurring framings to flag live in `private/system-instructions.md`

## Journal Entry Format

Append under today's date in the weekly file (`private/journal/YYYY-Www.md`). The attribution split is non-negotiable — *processing* is exactly the moment when blending becomes invisible if you don't keep the layers separate:

```markdown
**Monologue (HH:MM):** [Brief theme/topic]

**User's words (direct quotes + raw paraphrase):**
[The actual words they said. Quote verbatim where the language carries weight. Paraphrase only for connective tissue, no added framing.]

**Claude's processing (NOT their conclusions):**
[The cleaned-up summary, themes named, patterns spotted. Anything you noticed they didn't explicitly say goes here.]

**Open / unresolved:**
[Questions raised that didn't get answered.]
```

If they engaged with one of your framings ("yeah, that's it"), record their engagement separately — adoption is not authorship.

Also append a log entry to `private/log.md`:
```markdown
## [YYYY-MM-DD] monologue | <one-line theme/topic>

<1-2 sentences naming what came up>
```

The log is the timeline; the journal is the narrative. Both get updated.

## What Happens Later

- The end-day skill reviews the day's entries
- The weekly-review skill organizes the week: adds Summary, Highlight Quotes, optional sections
- Patterns may graduate to `self-map.md` — follow the citation/snapshot/log process in `consolidate-memory → Graduating Findings`. Don't promote anything to self-map ad-hoc from a monologue session.

## Example

**User:** [opens with stream-of-consciousness reflection]

**Assistant:** "Go ahead — I'm listening."

**User:** [5 minutes of rambling dictation with typos about feeling stuck on a decision, frustration at work, missing a place they used to live...]

**Assistant:** "Let me play that back. Three threads: (1) You're second-guessing a decision you already made. (2) Work frustration, specifically feeling unheard in meetings. (3) Missing somewhere you used to live, or maybe what that place represented. Did I get that right?"

**User:** "Yeah. The decision thing is fine, I'm just venting. The place thing is interesting though..."

**Assistant:** "Want me to search for past entries about that? You've written about place and belonging before."

**User:** "Sure."

**Assistant:** [Searches] "Found a few things. Two years ago you wrote about 'home being people, not places' after a move. And last fall there's a thread about identity feeling tied to geography. Does either of those connect to what's coming up now?"

**User:** "The identity one, yeah..."

**Assistant:** [Follows that thread, then captures the processed version]
