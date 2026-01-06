# Structured Journaling with Claude Code

I built this project to apply what I've learned [designing reliable AI systems](https://wrenchatwork.substack.com/p/rigorous-work-with-fallible-ai) with Claude Code to create a better journaling practice: daily rituals, weekly reviews, decision tracking, and history that stays searchable over time. It ships with a few frameworks and journaling practices, but you can add whatever resonates. Import old journals and they become organized and accessible, not just archived. It's an experiment in leveraging Claude Code's larger toolkit: commands, agents, skills, and hooks. Your data stays local in markdown files you control. Start with `/onboarding` and build from there.

---

## How It Works

**Files over chat.** Your self-knowledge accumulates in markdown files you control, not hidden in chat logs. Daily rituals capture intentions and reflections. Weekly reviews surface patterns and keep history searchable.

**Grows with what matters.** Big decisions, recurring patterns, ongoing projects - give them their own space and track your thinking over time. Frameworks from researchers and authors are built in when you need a lens.

**Your history stays searchable.** Import old journals and they become organized and accessible. Weekly summaries, consistent structure, and a purpose-built search agent help Claude find patterns across years of writing.

**No need to pre-organize.** Dump stream-of-consciousness, ramble, think out loud. Clarity comes from the back-and-forth: summarization, follow-up questions, figuring out what resonates.

**Extensible and private.\*** Track projects, habits, ideas. Adapt the structure to your life. Your data stays on your machine, protected by security hooks. *(\*See [Privacy](#privacy) for important caveats.)*

---

## Quick Start

**Requires:** [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (Anthropic's CLI for Claude)

```bash
git clone https://github.com/Wrendered/journaling-with-claude.git
cd journaling-with-claude
```

Open Claude Code in this directory and run `/onboarding`. Claude handles the rest.

**Daily:** `/start-day` (morning) and `/end-day` (evening) create a reflection rhythm. Use what works for you.

**Weekly:** `/weekly-review` to look back, `/plan-week` to set direction.

**Tip:** Dictation works great here — typos and garbled speech don't matter because Claude processes everything through context. `/monologue` is built for this. On macOS: System Settings → Keyboard → Dictation → set shortcut to "Press Globe Key Twice."

---

## How It's Organized

```
private/                  # Your data (gitignored, stays local)
├── self-map.md           # Patterns, drivers, self-knowledge
├── dashboard.md          # Current state — MIT, life areas, habits, experiments
├── journal/              # Weekly journal files
├── decisions/            # Big decisions you're working through
└── assessments/          # Framework results (Enneagram, etc.)

frameworks/               # Life philosophies (Atomic Habits, Stoicism, Brené Brown)
personality/              # Typing systems (Enneagram)
practices/                # Journaling exercises (MIT, Gratitude, Seneca's Evening Review)
templates/                # Starter files to copy into private/
.claude/                  # Claude Code configuration (commands, agents, skills, hooks)
```

The reference folders (`frameworks/`, `personality/`, `practices/`) are lenses for self-reflection, not therapeutic protocols. Use `/add-framework` to add any author, book, or concept that resonates.

---

## Importing Historical Journals

If you have old journals, therapy notes, or past reflections, Claude can process them into a searchable, organized structure.

Run `/import-history` — Claude will read your raw material and build:
- A searchable full-text archive
- A quotes index organized by theme
- Theme files for recurring patterns
- Relationship files for key people

Years of reflection become accessible context, not buried archives.

Not required to start. Powerful if you have it.

---

## Intelligent Search

Ask Claude about your past and it searches automatically. No special command needed.

> "What have I written about decision-making?"
> "When did I first mention wanting to change careers?"
> "Find patterns about avoidance"

This works because the whole system keeps your data search-ready: weekly reviews generate summaries, journals follow a consistent structure, and index files describe what exists. The search agent reads those indexes first, scans summaries to find relevant timeframes, then dives into raw content only when needed. Patterns across time, not just keyword matches.

---

## Personalization: How CLAUDE.md Works

The system separates what you can share (commands, frameworks, practices) from what's personal (your preferences, rituals, history).

**CLAUDE.md is your configuration file.** When you run `/onboarding`, Claude walks you through setting up:
- Daily rituals: What prompts do you want in `/start-day` and `/end-day`?
- Weekly rhythm: When do you run `/plan-week` and `/weekly-review`?
- Working style: How should Claude challenge you?

Commands read from CLAUDE.md to know what to do. The command files in `.claude/commands/` are generic orchestrators. Your preferences live in CLAUDE.md.

**To customize:**
1. Copy `CLAUDE.template.md` to `CLAUDE.md` (done automatically by `/onboarding`)
2. Edit the "Daily Rituals" and "Weekly Rhythm" sections
3. Commands will use your configuration

**What this means for sharing:** You can fork this repo, customize CLAUDE.md for yourself, and still pull updates to commands and frameworks without losing your preferences. CLAUDE.md is gitignored.

---

## Claude Code Architecture

This project uses Claude Code's full toolkit. Understanding this helps if you want to customize or extend it.

### Commands

Explicit workflows you invoke with `/name`. Located in `.claude/commands/`.

| Command | Purpose |
|---------|---------|
| `/start-day` | Morning kickoff — set your MIT |
| `/end-day` | Evening review — what went well, what didn't |
| `/check-day` | Quick mid-day check-in |
| `/monologue` | Stream of consciousness — just dump |
| `/deep-dive [topic]` | Extended exploration of a pattern or decision |
| `/plan-week` | Weekly planning — set focus and intentions |
| `/weekly-review` | Look back, organize journal, note patterns |
| `/onboarding` | Initial setup — run once |
| `/import-history` | Process old journals into searchable structure |
| `/add-framework [name]` | Research and add a new framework |
| `/setup-backups` | Configure automatic backups |

### Agents

Auto-invoked by Claude when relevant. Located in `.claude/agents/`.

| Agent | Triggers on |
|-------|-------------|
| `search` | Questions about your past, patterns, history |

### Skills

Domain knowledge Claude applies automatically. Located in `.claude/skills/`.

| Skill | Purpose |
|-------|---------|
| `backup` | Knows how to run and configure backups |

### Hooks

Claude Code hooks that enforce rules. Located in `.claude/hooks/`.

| Hook | Purpose |
|------|---------|
| `PreToolUse` | Blocks `git add`/`commit`/`push` of `private/` or `CLAUDE.md` |
| `PostToolUse` | Reviews committed diffs for accidentally included personal info |

### Adding Your Own

**New command:** Create `.claude/commands/your-command.md`

**New framework:** Run `/add-framework [name]` — Claude researches and creates it

---

## Privacy

**Local storage:** The `private/` folder is gitignored. Your journal files stay on your machine in markdown you control. A security hook blocks any attempt to commit `private/` or `CLAUDE.md`.

**But be aware:** When you use Claude Code, your prompts and file contents are sent to Anthropic's servers. This means your reflections pass through their API. What that means for privacy:

- **Training:** Consumer accounts (Pro/Max) can opt out of model training at [claude.ai/settings](https://claude.ai/settings). Commercial API accounts are excluded from training by default.
- **Retention:** With training opt-out, data is retained for 30 days. With opt-in, up to 5 years.
- **Trust & Safety:** Anthropic's safety team can review flagged content regardless of your settings.
- **Telemetry:** You can disable non-essential telemetry with `export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`.

This is a journaling tool, not a secure vault. Don't include passwords, financial account numbers, or information that could harm others if exposed. For maximum privacy, use a commercial API account with zero-retention configured.

**Backups:** Run `/setup-backups` to configure automatic backups of your private files to Dropbox, iCloud, or a local folder. Backups run during `/weekly-review`.

---

## A Note About This Tool

This is a space for reflection, not therapy. Writing things down, noticing patterns, and having a thinking partner can be genuinely valuable for self-understanding. Many people find that journaling helps them process experiences, clarify their thoughts, and track what matters to them.

That said, this tool isn't treatment. If you're working through something heavy, a good therapist can offer things this can't: clinical training, the nuance of face-to-face conversation, and professional support tailored to your specific situation. Using both together often works well.

**If you're in crisis:**
- **988** Suicide & Crisis Lifeline: Call or text 988 (US, 24/7, free, confidential)
- **Crisis Text Line:** Text HOME to 741741
- **International:** [findahelpline.com](https://findahelpline.com)

There's no shame in needing support. These resources exist because hard times are part of being human.

---

*Built for Claude Code*
