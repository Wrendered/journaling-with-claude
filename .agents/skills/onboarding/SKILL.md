---
name: onboarding
description: First-time setup ritual that creates private/ folder structure from templates, conducts a conversational interview to populate self-map.md and dashboard.md, captures key relationships, and configures daily and weekly rituals in AGENTS.md.
when_to_use: |
  ALWAYS invoke this skill when the user is new to the system or asks how to begin.
  Trigger phrases (any of these): "I'm new here", "getting started", "set me up",
  "how do I begin", "first time", "onboard me", "initial setup".
  Also invoke automatically if private/self-map.md or private/dashboard.md don't exist
  when the user opens their first session.
allowed-tools: Read, Edit, Write, Bash, Glob
---

# Onboarding

First-time conversational setup. Builds the foundation files through interview, not forms.

## First-Time Setup

Before starting the conversation, check and create what's needed. The structure must match what AGENTS.md tells the assistant to read first.

1. **AGENTS.md** is tracked in the repo — should always exist after `git clone`. If somehow missing, the user has a deeper problem; bail and tell them.
2. If `private/` doesn't exist, create the full folder structure:
   - `private/journal/`
   - `private/assessments/`
   - `private/decisions/`
   - `private/relationships/`
   - `private/raw/`
   - `private/archive/`
   - (`private/history/` is created later by the import-history skill if user has historical material)
3. Copy starter files from templates (only if not present):
   - `templates/system-instructions.template.md` → `private/system-instructions.md` (the user's personal config — tone, lens stack, daily ritual specifics)
   - `templates/self-map.template.md` → `private/self-map.md`
   - `templates/dashboard.template.md` → `private/dashboard.md`
   - `templates/_index.template.md` → `private/_index.md`
   - `templates/log.template.md` → `private/log.md`
   - `templates/tags.template.md` → `private/tags.md`
   - `templates/decisions/_index.template.md` → `private/decisions/_index.md`
   - `templates/relationships/_index.template.md` → `private/relationships/_index.md`
   - `templates/journal/_index.md` → `private/journal/_index.md`
   - `templates/assessments/_index.md` → `private/assessments/_index.md`
4. Set up Claude Code to read AGENTS.md (Codex reads it natively):
   - **CHECK FIRST:** If `CLAUDE.md` already exists (regular file or symlink), STOP and ask the user before doing anything. They likely have personalized content that would be silently clobbered by `ln -sf`.
   - Safe-only setup: `[[ ! -e CLAUDE.md ]] && ln -s AGENTS.md CLAUDE.md` (no `-f`, fails if file exists)
   - If existing CLAUDE.md present: confirm with user, back it up to `private/CLAUDE.md.backup-<date>`, then create symlink.

   Note: there are no separate override files. AGENTS.md instructs the assistant to read `private/system-instructions.md` at session start, so personalization loads via that single file regardless of which tool is reading.

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

Don't go deep here — just capture who matters. The files will fill in over time through monologue, deep-dive, and daily reflections.

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
- Point them to the import-history skill
- They can do it now or later
- It's a separate, deeper process — not required to start using the system

## Teach the Rhythm

Before closing, explain how to use the system and ask about their preferences:

**Daily (suggested, not required):**
- start-day — Morning. Set your MIT, brief check-in.
- end-day — Evening. Reflect on the day.

Some people do both daily. Some do one or the other. Some skip days. Find what works.

**Weekly:**
- weekly-review — Look back, organize the journal, note patterns.
- plan-week — Set focus and intentions for the week ahead.

**Ask:** "When do you want to do your weekly review and planning? Some people do review Friday evening and plan Sunday morning. Others do both together on Sunday. What fits your life?"

**Anytime:**
- monologue — Stream of consciousness. Just talk, Claude captures.
- deep-dive [topic] — Extended exploration of a pattern, decision, or feeling.

## Configure Daily Rituals

The skills are scaffolds — the specific prompts and questions are configured in `AGENTS.md → Daily Rituals`. Walk through this with them:

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

**Update AGENTS.md:**
Based on their answers, edit the `Daily Rituals` section in `AGENTS.md`:
- Fill in their morning rotating element preferences (or delete the table if they want minimal)
- Keep only their chosen evening reflection option (delete the others)
- This is what start-day and end-day will reference going forward

## Configure Weekly Rhythm

The weekly skills also read from `AGENTS.md → Weekly Rhythm`. Walk through this:

**When to run weekly skills:**
- "When works best for your weekly review and planning?" (Options they mentioned earlier)
- Some do both on Sunday, some split across Fri/Sat and Sun/Mon

**Day themes (optional):**
Ask: "Do you want specific focus days during the week?"
- Decision work days (e.g., Mon/Thu for working through open decisions)
- Framework/assessment day (e.g., Tue for exploration)
- Light days (e.g., Wed just rituals)
- Or: No day themes, just the two weekly skills

"Some people like structure throughout the week. Others find it rigid. What sounds right?"

**Update AGENTS.md:**
Based on their answers, edit the `Weekly Rhythm` section in `AGENTS.md`:
- Set their preferred days for plan-week and weekly-review
- Fill in day themes if they want them, or delete the table if they prefer minimal
- This is what the weekly skills will reference going forward

## Close

- Summarize what we learned
- Explain the daily/weekly rhythm (above)
- Mention the import-history skill if they have historical material
- Set first MIT for tomorrow
