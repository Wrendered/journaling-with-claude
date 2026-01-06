---
description: Initial setup. Run once when starting. Populates private/ files through conversation.
---

## First-Time Setup

Before starting the conversation, check and create what's needed:

1. If `CLAUDE.md` doesn't exist, copy from `CLAUDE.template.md`
2. If `private/` doesn't exist, create the folder structure:
   - `private/journal/`
   - `private/assessments/`
   - `private/decisions/`
3. If `private/self-map.md` doesn't exist, copy from `templates/self-map.template.md`
4. If `private/dashboard.md` doesn't exist, copy from `templates/dashboard.template.md`
5. Copy any missing `_index.md` files from templates

Do this silently, then begin the conversation.

## Purpose

Conversational interview to understand:
1. Identity — Who they are, life stage, context
2. Mission — What matters, where they're headed
3. Self-knowledge — Drivers, patterns, what works
4. Current state — Life areas, satisfaction, focus
5. Working style — How they want to interact

## Approach

- Conversational, not a form
- One question at a time, go deep on interesting threads
- Build files incrementally as answers come in
- Surface tensions and contradictions gently

## Core Questions

### Identity
- What name do you go by?
- What's your current life stage?
- Where are you based? (timezone context)

### Mission
- What are you building toward? (life, not just work)
- What matters most to you right now?
- If you had to pick one word for this year, what would it be?

### Self-Knowledge
- What motivates you? (fear, ambition, curiosity, duty, etc.)
- What patterns trip you up? (be specific)
- When you're at your best, what's true?
- When you're struggling, what's usually going on?

### Life Areas
Rate 1-10 and note what's off:
- Career/work
- Relationships/family
- Health/energy
- Finances
- Personal growth/meaning
- Fun/creativity

### Key People
After the life areas, ask: "Who are the 3-5 most important people in your life right now? Partner, family, friends, mentors, collaborators..."

For each person mentioned:
- Get their name and relationship (partner, best friend, tow partner, etc.)
- One sentence about why they matter
- Create `private/relationships/[name].md` with a stub

Don't go deep here — just capture who matters. The files will fill in over time through `/monologue`, `/deep-dive`, and daily reflections.

### Working Style
- What tone helps you think clearly? (supportive, direct, challenging, etc.)
- What should I never do without asking?
- What's helped in past coaching/therapy/self-work?

## Output

Populate:
- `private/self-map.md` — Patterns, drivers, self-knowledge
- `private/dashboard.md` — Current state, life areas, habits, experiments

Create domain folders as needed (based on what matters to you):
- `private/goals/` — Long-term goals, life direction
- `private/relationships/` — Key people (one file per person)
- `private/career/` — Career planning, job decisions
- `private/health/` — Health tracking, goals
- Or any other domain that fits your life

## Historical Journals (Optional)

Near the end, ask: "Do you have old journals, therapy notes, or past reflections you'd like to bring in?"

If yes:
- Point them to `/import-history`
- They can do it now or later
- It's a separate, deeper process — not required to start using the system

## Teach the Rhythm

Before closing, explain how to use the system and ask about their preferences:

**Daily (suggested, not required):**
- `/start-day` — Morning. Set your MIT, brief check-in.
- `/end-day` — Evening. Reflect on the day.

Some people do both daily. Some do one or the other. Some skip days. Find what works.

**Weekly:**
- `/weekly-review` — Look back, organize the journal, note patterns.
- `/plan-week` — Set focus and intentions for the week ahead.

**Ask:** "When do you want to do your weekly review and planning? Some people do review Friday evening and plan Sunday morning. Others do both together on Sunday. What fits your life?"

**Anytime:**
- `/monologue` — Stream of consciousness. Just talk, Claude captures.
- `/deep-dive [topic]` — Extended exploration of a pattern, decision, or feeling.

## Configure Daily Rituals

The commands are scaffolds — the specific prompts and questions are configured in `CLAUDE.md → Daily Rituals`. Walk through this with them:

**Morning rotating element:**
Ask: "Do you want a daily prompt after setting your MIT? Some options:"
- Stoic prep ("What difficulty might you face?") — good for anticipating challenges
- Values check ("Is today pointed at what matters?") — good for staying aligned
- Gratitude ("What's one thing working well?") — good for positivity
- Nothing — just set MIT and go

"You can rotate these by day, pick one for every day, or skip entirely. What sounds right?"

**Evening reflection:**
Ask: "After capturing how the day went, do you want structured reflection questions?"
- Seneca's 3 Questions (What went well? Where did I go wrong? What could I do better?)
- Simple gratitude (one thing you're grateful for)
- Nothing structured — just capture and close

"There's no right answer. Some people love structure, others find it tedious."

**Update CLAUDE.md:**
Based on their answers, edit the `Daily Rituals` section in `CLAUDE.md`:
- Fill in their morning rotating element preferences (or delete the table if they want minimal)
- Keep only their chosen evening reflection option (delete the others)
- This is what `/start-day` and `/end-day` will reference going forward

## Configure Weekly Rhythm

The weekly commands also read from `CLAUDE.md → Weekly Rhythm`. Walk through this:

**When to run weekly commands:**
- "When works best for your weekly review and planning?" (Options they mentioned earlier)
- Some do both on Sunday, some split across Fri/Sat and Sun/Mon

**Day themes (optional):**
Ask: "Do you want specific focus days during the week?"
- Decision work days (e.g., Mon/Thu for working through open decisions)
- Framework/assessment day (e.g., Tue for exploration)
- Light days (e.g., Wed just rituals)
- Or: No day themes, just the two weekly commands

"Some people like structure throughout the week. Others find it rigid. What sounds right?"

**Update CLAUDE.md:**
Based on their answers, edit the `Weekly Rhythm` section in `CLAUDE.md`:
- Set their preferred days for `/plan-week` and `/weekly-review`
- Fill in day themes if they want them, or delete the table if they prefer minimal
- This is what the weekly commands will reference going forward

## Close

- Summarize what we learned
- Explain the daily/weekly rhythm (above)
- Mention `/import-history` if they have historical material
- Set first MIT for tomorrow
