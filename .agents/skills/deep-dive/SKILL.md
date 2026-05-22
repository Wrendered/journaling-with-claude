---
name: deep-dive
description: Extended exploration session that pulls quotes and context from private/history/, surfaces relevant patterns from self-map, and works through a specific theme, pattern, decision, feeling, or framework calibration with the user. Reaches for the right framework lens (CBT for distorted thoughts, IFS for inner conflict, WRAP for decisions, etc.) based on the topic.
when_to_use: |
  ALWAYS invoke this skill when the user wants to go deeper than a daily ritual on a specific topic.
  Trigger phrases (any of these): "let's dig into", "deep-dive on", "explore this pattern",
  "work through this decision", "calibrate my Enneagram", "process this feeling",
  "what's underneath this", "why do I keep", "I want to understand this better".
  Also invoke when the user names a recurring pattern, surfaces a stuck decision, or
  references an assessment result they want to test.
context: fork
paths:
  - "private/**"
allowed-tools: Read, Edit, Write, Bash, Glob, Grep, Task
---

# Deep Dive

Extended exploration of a theme, pattern, decision, or question. Longer than daily rituals, shorter than full onboarding.

## When to Use

- Processing something that came up in daily reflection
- Exploring a pattern that keeps recurring
- Working through a specific decision
- Refining an assessment profile (e.g., "Do these Enneagram results actually fit?")
- Connecting current feelings to history/patterns

## Flow

### 1. Set the Focus
What are we exploring? Options:
- A **pattern** (e.g., "Why do I keep avoiding this decision?")
- A **decision** (e.g., "Career change — let's actually dig in")
- An **assessment** (e.g., "Let's calibrate my Enneagram type")
- A **feeling** (e.g., "I've been anxious all week — what's underneath?")
- A **theme** (e.g., "My relationship to achievement")

### 2. Surface Relevant Context
Pull from:
- `history/` theme files — What have they written about this before?
- `self-map.md` — Known patterns, self-knowledge
- `assessments/` — Relevant framework results
- Recent weekly journal — Current week's Raw Log and summaries

**Key move:** Quote their own words back to them. "In March 2018 you wrote: '...'"

### 3. Explore Together
Depending on the topic:
- **Pattern work:** When does this show up? What triggers it? What's the payoff?
- **Decision work:** What's actually blocking this? What would each choice cost/give?
- **Assessment calibration:** "Does this description fit? Give me a recent example where it did/didn't."
- **Feeling work:** What framework lens helps here? (Shame/vulnerability? Stoic reframe? Enneagram pattern?)

**Reach for the right lens** — check `private/system-instructions.md → Lens Stack` (fallback `AGENTS.md → Lens Stack`) for the user's mapping of situations to frameworks. Don't pick a lens at random; the stack exists specifically so you can reach for it.

### 4. Synthesize
- What did we learn?
- What's the update to your self-understanding?
- Any action items?

### 5. Capture
- **Session notes → Weekly journal** (`private/journal/YYYY-Www.md`) under today's date.
  - **Attribution is critical here.** Deep-dive is the canonical "extended exploration" skill — you'll be pulling quotes from history AND offering pattern interpretations. Use the sub-section split: `**User's words:**` for verbatim + raw paraphrase, `**Claude's framings offered (NOT her conclusions):**` for any reframe/interpretation/label you offered. See `AGENTS.md → Attribution Rule` (the `check-attribution` hook flags blended entries) and `private/system-instructions.md → Attribution rule` for the personal recurring-pattern flags.
- **Log entry → `private/log.md`** for meaningful sessions:
  ```markdown
  ## [YYYY-MM-DD] decision | <topic>     ← (or `pattern` / `monologue` / `note` based on what came up)

  <1-3 sentences naming what surfaced. Cross-ref the journal entry and any decision/relationship files touched.>
  ```
- **Profile updates → `self-map.md` or `assessments/`:** follow the citation + snapshot + log process in `consolidate-memory → Graduating Findings`. Do NOT edit self-map directly from a deep-dive session — surface the candidate finding in the journal entry, snapshot self-map first, then make the edit with a verbatim quote and a `log.md` graduation entry. (Snapshot mechanism documented in `weekly-review → step 6`.)
- **New patterns → `history/` theme files:** if a recurring theme surfaces that warrants its own compilation, create or extend `history/themes-<topic>.md`.
- **When weekly review happens, key insights become Highlight Quotes.**

---

## Example: Calibrating Enneagram Type

**User:** I want to test my Enneagram results

**Assistant:**
Your assessment suggested Type 3 (Achiever) with a 4 wing. The core pattern is: "Self-worth tied to achievement and recognition. Difficulty being present without producing."

**Does that fit?** Can you give me a recent example where this showed up — or one where it didn't?

**User:** [shares example]

**Assistant:** That tracks / That's interesting — sounds more like [X]. Let me update your profile with this nuance...

---

## Example: Exploring a Pattern

**User:** Why do I keep not deciding on [major life decision]?

**Assistant:**
Let me pull what you've written about this...

From your journal (6 months ago): "I keep saying I'll decide next month..."
From last year: "Both options seem fine, which is the problem."
From years ago: [an even older quote on the same theme — quote it verbatim from history/]

**Pattern:** Decision avoidance on high-stakes questions has been running for years.

What feels true about this? What doesn't?

---

## Relationship to History

The `history/` folder exists FOR these sessions. Daily rituals are light; deep dives are when we mine the treasure trove.

| Ritual | History Usage |
|--------|---------------|
| start-day | Rarely — maybe surface a relevant quote |
| end-day | Note if something connects to a theme |
| monologue | Capture raw, process later |
| **deep-dive** | **Primary use** — pull quotes, patterns, context |
| onboarding | Full review across all history |

---

## Duration

Expect 15-45 minutes. Can be done anytime, but works well on:
- Tuesday (Framework exploration day)
- Friday (Integration day)
- Weekend (Journal processing time)
