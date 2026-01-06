---
description: Process old journals into searchable structure.
---

# /import-history

> Process historical journals, therapy notes, or past reflections into a searchable, organized structure.

## What You're Working With

The user has historical material — could be:
- One big text file with years of entries
- Multiple separate files (by year, by period, etc.)
- Photos of handwritten journals
- Therapy notes, letters, old reflections
- Mix of formats

**Format notes:**
- Plain text (`.txt`, `.md`) is easiest to process in chunks
- Images work — Claude can read handwritten journals, but it's slower
- PDFs are harder — ask them to convert to text if possible

**Where to put it:** `private/import/` — already gitignored, safe for personal material. Create the folder if it doesn't exist.

**Start by understanding what they have.** Ask about volume, format, time span. Then figure out the best approach together. Be flexible — every archive is different.

## What We're Building Toward

The goal is a `private/history/` folder that makes the past **searchable and surfaceable**. When patterns repeat, you can say "you wrote about this three years ago..."

### Target Structure

```
private/history/
├── journal-raw.txt          # Full text, grep-able (preserve everything)
├── quotes-index.md          # Significant quotes organized by theme
├── themes-[topic].md        # Deep compilations of recurring themes
└── relationships-[name].md  # Pattern analysis for key people
```

### What Makes Each File Useful

**journal-raw.txt**
- Complete, searchable archive
- Dates preserved where possible
- Nothing lost

**quotes-index.md**
- The user's own words that capture something important
- Organized by theme (identity, decisions, relationships, growth, etc.)
- Include dates/context so you can find the full entry
- These are the quotes you'll surface in future sessions

**themes-[topic].md**
- Deep dive on a recurring theme (grief, career uncertainty, self-worth, etc.)
- Pull relevant quotes, show how the theme evolved
- Note patterns: "This comes up when X happens"

**relationships-[name].md**
- For significant people who appear repeatedly
- Patterns in how the user relates to them
- Key moments, unresolved threads

## How to Approach This

**Go slow. Be careful.** This is years of someone's inner life. Read thoroughly before organizing.

1. **Start by reading** — Get a feel for what's there. What themes recur? Who shows up repeatedly? What quotes jump out?

2. **Create journal-raw.txt first** — Consolidate everything into one searchable file. Preserve dates and structure where possible.

3. **Build the quotes index** — Pull significant quotes as you read. Organize by theme. This is the most useful artifact.

4. **Create theme files for what's prominent** — You don't need to force themes. If grief is a major thread, create `themes-grief.md`. If not, don't.

5. **Create relationship files if relevant** — Only for people who matter to the user's patterns. Not everyone mentioned.

## For Large Volumes

If there's a lot of material (years of journals), use parallel subagents:

- One agent per major theme or time period
- Each agent reads deeply, extracts quotes and patterns
- Consolidate their findings into the final structure

This might mean 5-10 agents working different threads simultaneously. That's fine — it's better to be thorough than to rush.

## Be Flexible

- The user's history might be 6 months or 20 years
- It might be deeply personal or relatively light
- Some people have clear themes, others are more scattered
- Adjust depth and structure to what's actually there

## When You're Done

### 1. Create/Update the Index

Generate or update `private/history/_index.md` to describe what was created. This index tells search agents how to navigate the history.

Required sections:
- **For Search Agents** — Quick orientation, what files exist, how to search
- **Files** — List of all files with descriptions
- **How to Search** — Grep commands, theme navigation

The index should be self-describing so search agents know how to work with whatever structure you created.

### 2. Summarize

- Major themes, key relationships, notable patterns
- Anything that surprised you or seems significant
- The user now has a searchable past

## Bootstrap Living Files

History analysis files are read-only archives. **Living files** get updated through daily use. After import, bridge the two.

### 1. Create Relationship Stubs (Always Do This)

Everyone has significant people. For each person who:
- Has a `history/relationships-*.md` analysis file
- Appears 5+ times in the journal
- Is mentioned in theme files as significant
- User identifies as important

Create a stub in `private/relationships/[name].md`:

```markdown
# [Name]

> [One-line relationship description]

**Last Updated:** [date]

---

## Who They Are

[Basic facts from history]

## Our Relationship

[Key dynamics, how you met, what they mean]

## Historical Context

See `history/relationships-[name].md` for deep historical analysis (if exists).

---

## Patterns / Notes

*[Add as patterns emerge]*
```

**Don't skip this step.** The history analysis is an archive. The living file is what gets surfaced in daily use.

### 2. Surface Themes, Ask About Structure

Different people organize differently. After identifying recurring themes, **ask**:

> "I found these recurring threads in your history: [list themes]. Some people find it helpful to have dedicated folders or files for things like this. Would any of these benefit from their own space? Or do you prefer to let structure emerge organically?"

**Examples of what might emerge:**
- Recurring decisions → `decisions/` folder
- Career uncertainty → `career/` folder or file
- Health journey → `health/` folder
- Financial goals → `finances/` folder
- Creative projects → `projects/` folder

**Don't assume.** Let the user decide what matters enough to organize.

### 3. Populate Self-Map

Pull stable patterns from history into `self-map.md`:
- Core drivers and motivations
- Recurring patterns (bugs)
- What works, what doesn't
- Cross-framework insights if assessments are mentioned

## Privacy Reminder

This is deeply personal content. Work carefully. Everything stays in `private/`.

## Search Agent Compatibility

The search agent (`.claude/agents/search.md`) will read `history/_index.md` to understand the structure. Make sure your index:
- Lists all files that exist
- Describes what each file contains
- Provides search strategies (grep, theme files, relationship files)
- Cross-references to `journal/_index.md` for current journals
