---
description: Research, add, and personalize a new framework, assessment, daily practice, or exercise.
---

# /add-framework [name]

> Add a new framework, assessment, daily practice, or exercise to the library. Research it, route it to the correct folder, and suggest integrations.

## Content Types

This command handles four types of content:

| Type | Folder | Examples | What it is |
|------|--------|----------|------------|
| **Framework** | `frameworks/` | Stoicism, Atomic Habits, GTD, Brene Brown | Lens for framing problems |
| **Assessment** | `assessments/` | Enneagram, MBTI, Big Five, StrengthsFinder | External quiz you take |
| **Daily Practice** | `daily-practices/` | Gratitude, Stoic Morning Prep, Evening Review | Morning/evening journaling ritual |
| **Exercise** | `exercises/` | Values Clarification, Personal Mission | Guided deep work (do periodically) |

**Classification guide:**
- External quiz that gives you a type/score? → `assessments/`
- Short prompt for daily/weekly journaling? → `daily-practices/`
- Guided deep work you do yourself? → `exercises/`
- Lens for thinking about problems? → `frameworks/`

## Public vs Private

| Content | Location | Contains |
|---------|----------|----------|
| **Generic reference** | `frameworks/`, `assessments/`, `daily-practices/`, or `exercises/` | Instructions. Shareable, no personal data. |
| **Personal results** | `private/assessments/[name].md` | My results, my answers, my patterns. |

**Rule:** Never put personal details in public folders. That content belongs in `private/assessments/`.

## Input

User provides: A framework name, author, book, or concept they want to add.

Examples:
- `/add-framework Getting Things Done` → frameworks/
- `/add-framework Myers-Briggs` → assessments/
- `/add-framework Bullet Journal` → daily-practices/
- `/add-framework Personal Mission Statement` → exercises/
- `/add-framework Cal Newport Deep Work` → frameworks/

## Process

### 1. Research (use parallel subagents)

Send 2-3 subagents to research:

**Subagent 1: Core concepts**
- What is this framework/approach?
- Who created it? What's the origin?
- What are the core concepts and vocabulary?
- What problems does it solve?

**Subagent 2: Practical application**
- What are the key exercises or practices?
- What does daily/weekly application look like?
- What are the best resources (books, assessments, websites)?
- Any cautions or limitations?

**Subagent 3: Classification & integration**
- Is this a framework, personality system, or practice?
- How does this relate to our existing content?
- Does it overlap with anything we have? (If so, what's unique?)
- Where might it fit in daily/weekly rituals?

### 2. Classify and route

Based on research, determine the correct folder:

| If it's a... | Create file at... | Update index... |
|--------------|-------------------|-----------------|
| Framework | `frameworks/[name].md` | `frameworks/_index.md` |
| Assessment | `assessments/[name].md` | `assessments/_index.md` |
| Daily Practice | `daily-practices/[name].md` | `daily-practices/_index.md` |
| Exercise | `exercises/[name].md` | `exercises/_index.md` |

### 3. Create the file

**For frameworks** (`frameworks/[name].md`):

```markdown
# [Framework Name]

> [One-line description of what it is]

**Source:** [Book/Author/Origin]

---

## Core Concept

[2-3 paragraphs on what this is and why it matters]

---

## Key Ideas

[The main concepts, vocabulary, or model]

---

## Key Exercises

[Practical things to try — formatted as actionable steps]

---

## When to Use This

[Situations where this lens is helpful]

---

## Resources

- [Primary book/source]
- [Website if applicable]
- [Assessment if applicable]
```

**For assessments** (`assessments/[name].md`):

```markdown
# [System Name]

> [One-line description]

---

## Core Concept

[What this system measures/describes]

---

## The Types/Categories

[Overview of the types, traits, or categories]

---

## How to Use It

[What to do with this information — self-awareness, relationships, growth]

---

## Resources

- [Assessment link]
- [Key book/source]
```

**For daily practices** (`daily-practices/[name].md`):

```markdown
# [Practice Name]

> [One-line description]

---

## The Practice

**When:** [Morning/Evening/Anytime]
**Time:** [X minutes]
**Source:** [Origin]

---

## How to Do It

[Step by step instructions]

---

## Why It Works

[The mechanism or research behind it]

---

## Variations

[Alternative ways to do it]

---

## Source

[Where this practice comes from]
```

**For exercises** (`exercises/[name].md`):

```markdown
# [Exercise Name]

> [One-line description]

---

## The Exercise

**Time:** [X minutes]
**Frequency:** Once, then revisit every 6-12 months
**Source:** [Origin]
**Output:** Store results in `private/assessments/[name].md`

---

## How to Do It

[Step by step guided process]

---

## Using Your Results

[What to do with the output — decision filter, daily check-in, etc.]

---

## Source

[Where this exercise comes from]
```

### 4. Update indexes

**Update the appropriate index:**
- Add row to Quick Reference table
- Add to selection guide or related section

**Update personal index** — Add to `private/assessments/_index.md`:
- Add row to Framework Status table (Reference: ✓, Personalized: —)

### 5. Suggest integrations

Based on the research, suggest:

**Ritual integration (if applicable):**
- Does this suggest a morning practice? → Propose addition to /start-day
- Does this suggest an evening practice? → Propose addition to /end-day
- Does this suggest a weekly practice? → Propose addition to /weekly-review

**CLAUDE.md updates:**
- Add to appropriate section (frameworks, assessments, daily-practices, or exercises)
- Add to selection guide if framework

**Dashboard integration (if applicable):**
- Does it suggest tracking something? → Propose dashboard section

### 6. Present to user

Show:
1. Summary of what was learned
2. Classification decision (framework/assessment/daily-practice/exercise)
3. The created file (or preview)
4. Proposed integrations
5. Ask: "Want me to make these integration updates?"

### 7. Personalize (optional but recommended)

After integrations, ask: "Want to personalize this to your life?"

If yes, the approach depends on type:

**Personality systems** (Enneagram, MBTI, etc.):
- Link to external assessment if available
- Discuss results together
- Calibrate to their specific patterns
- Create `private/assessments/[name].md` with full discussion
- Add key patterns to `private/self-map.md`

**Habit-based frameworks** (Atomic Habits, GTD, Deep Work, etc.):
- Ask: What habits/practices do you want to build from this?
- For each: What's the identity? ("I'm someone who...")
- For each: What's the cue or stack?
- Add to `private/dashboard.md` → Habits I'm Building section

**Values/philosophy frameworks** (Stoicism, Brene Brown, NVC, etc.):
- Run a key exercise (values clarification, evening review, etc.)
- Discuss how principles apply to their current situation
- Create `private/assessments/[name].md` with exercise results
- Note patterns that connect to existing self-knowledge

**Practices** (Morning Pages, Bullet Journal, etc.):
- Add to morning/evening rotation if desired
- Set up in CLAUDE.md Daily Rituals section
- Track in dashboard if building the habit

**After personalization:** Update `private/assessments/_index.md` — change Personalized from "—" to "✓".

## Example Output

```
## Added: Myers-Briggs (MBTI)

**Type:** Assessment → assessments/mbti.md

**Core idea:** 16 personality types based on four dichotomies (E/I, S/N, T/F, J/P).

**Created:** `assessments/mbti.md`

**Suggested integrations:**
- Link to official assessment in Resources
- Reference in deep-dive for personality exploration
- Could pair with Enneagram for fuller picture

**Overlaps with:** Enneagram (both are typing systems, different angles)

Want me to make these integration updates?
```

## Notes

- Always check for overlap with existing content before creating
- If highly overlapping, suggest enhancing existing file instead
- User can always say "just create the file, skip integrations"
- Keep files focused — reference the source for full depth
