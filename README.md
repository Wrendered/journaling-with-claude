# Structured Journaling with Claude Code & Codex CLI

I built this project to apply what I've learned [designing reliable AI systems](https://wrenchatwork.substack.com/p/rigorous-work-with-fallible-ai) to create a better journaling practice: daily rituals, weekly reviews, decision tracking, and history that stays searchable over time. It ships with a few frameworks and journaling practices, but you can add whatever resonates. Import old journals and they become organized and accessible, not just archived. The system runs in **both Claude Code and OpenAI Codex CLI** — same skills, same hooks, single source of truth. Your data stays local in markdown files you control. Tell the assistant you're getting started and it'll walk you through onboarding.

---

## How It Works

**Files over chat.** Your self-knowledge accumulates in markdown files you control, not hidden in chat logs. Daily rituals capture intentions and reflections. Weekly reviews surface patterns and keep history searchable.

**Grows with what matters.** Big decisions, recurring patterns, ongoing projects - give them their own space and track your thinking over time. Frameworks from researchers and authors are built in when you need a lens.

**Your history stays searchable.** Import old journals and they become organized and accessible. Weekly summaries, consistent structure, and a purpose-built search agent help Claude find patterns across years of writing.

**No need to pre-organize.** Dump stream-of-consciousness, ramble, think out loud. Clarity comes from the back-and-forth: summarization, follow-up questions, figuring out what resonates.

**Extensible and private.\*** Track projects, habits, ideas. Adapt the structure to your life. Your data stays on your machine, protected by security hooks. *(\*See [Privacy](#privacy) for important caveats.)*

---

## Quick Start

**Requires either:**
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (Anthropic's CLI), OR
- [OpenAI Codex CLI](https://developers.openai.com/codex/cli)

```bash
git clone https://github.com/Wrendered/journaling-with-claude.git
cd journaling-with-claude
```

Open your assistant in this directory and tell it you're getting started. Onboarding triggers automatically and creates the personalized config files.

**Daily:** Say good morning to set your MIT, wind down at night to reflect. The right skill auto-triggers from your intent — you don't need to remember command names.

**Weekly:** Ask to plan the week or review the past week.

**Tip:** Dictation works great here — typos and garbled speech don't matter because Claude processes everything through context. Just start dumping thoughts and the monologue skill picks it up. On macOS: System Settings → Keyboard → Dictation → set shortcut to "Press Globe Key Twice."

---

## How It's Organized

The architecture follows a **three-layer pattern** (modeled on [Karpathy's "LLM Wiki"](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)):

| Layer | Purpose | Location |
|-------|---------|----------|
| **Raw** | Immutable source inputs you don't edit | `private/raw/`, `private/import/`, `private/history/journal-raw.txt` |
| **Wiki** | Synthesized self-knowledge Claude maintains over time | Most of `private/` |
| **Schema** | How the wiki is organized; how the assistant should navigate it | `AGENTS.md` (public) + `private/system-instructions.md` (personal) |

```
private/                  # Your data (gitignored, stays local)
├── _index.md             # MOC — first thing Claude reads (catalog)
├── self-map.md           # Patterns, drivers, self-knowledge
├── dashboard.md          # Current state — MIT, life areas, habits, experiments
├── log.md                # Append-only chronological log (greppable timeline)
├── tags.md               # Controlled vocabulary
├── journal/              # Weekly + daily journal files
├── decisions/            # Big decisions you're working through
├── relationships/        # Key people in your life
├── concepts/             # Atomic notes about you (declarative filenames)
├── history/              # Imported past material (years of writing, processed)
├── raw/                  # Untouched source inputs
├── archive/              # Closed/resolved items
└── assessments/          # Framework calibration results

frameworks/               # Lenses (Atomic Habits, Stoicism, CBT, IFS, WRAP, ...)
daily-practices/          # Journaling rituals (MIT, Gratitude, Seneca, Stoic Morning)
assessments/              # External quizzes (Big Five, Enneagram, MBTI)
exercises/                # Guided deep work (Values Clarification)
templates/                # Starter files copied into private/ on onboarding
.claude/                  # Claude Code config (skills, agents, hooks)
```

**Conventions:**
- `_index.md` files at folder roots are MOCs — Claude reads them first to orient
- YAML frontmatter on entries makes filtering grep-cheap (`status: open`, `type: decision`)
- `log.md` uses prefix format `## [YYYY-MM-DD] type | Title` for cheap timeline reconstruction
- Concept files use declarative filenames (`i-process-grief-by-building-things.md`) — the filename is the claim

The reference folders (`frameworks/`, `daily-practices/`, `assessments/`, `exercises/`) are lenses for self-reflection, not therapeutic protocols. Mention any author, book, or concept that resonates and the add-framework skill will research and integrate it.

---

## Importing Historical Journals

If you have old journals, therapy notes, or past reflections, Claude can process them into a searchable, organized structure.

Tell Claude you have old journals to import — the import-history skill triggers and Claude reads your raw material and builds:
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

## Personalization

The system separates what you share (skills, frameworks, practices, scaffolding) from what's personal (your tone, rituals, lens stack, history).

**Public, generic, tracked:**
- `AGENTS.md` — canonical agent instructions (read by Codex CLI natively, by Claude Code via symlink/import)
- Skills in `.agents/skills/`, frameworks in `frameworks/`, etc.

**Personal, gitignored:**
- `private/system-instructions.md` — your personalized config (tone, lens stack, daily ritual specifics). This is the file you edit.
- `CLAUDE.local.md` and `AGENTS.override.md` — symlinks to `private/system-instructions.md`. Both tools auto-load these.
- Everything in `private/` — your journal, decisions, relationships, history

**During onboarding** the assistant walks you through setting up:
- Daily rituals: morning intention prompts, evening reflection style
- Weekly rhythm: when to plan the week, when to review
- Working style: how to challenge you, what to never do without asking
- Lens stack: which frameworks fit which moments

These all land in `private/system-instructions.md`.

**Sharing:** Fork the repo, customize `private/system-instructions.md` for yourself, pull updates to skills/frameworks/AGENTS.md without losing your preferences.

---

## Dual-Tool Compatibility

The system runs in **both Claude Code and OpenAI Codex CLI** with a single source of truth for skills and hooks. This is unusual; here's how it works.

### Why both

- **Claude Code** — strongest agent integration, native skills, hooks, subagents
- **Codex CLI** — different model family, different ergonomics, broader tool ecosystem (uses [agents.md spec](https://agents.md))

The same daily ritual, the same lens stack, the same hooks fire in either tool.

### What's shared (single source of truth)

| Primitive | Source | How both tools find it |
|---|---|---|
| **System instructions** | `AGENTS.md` (public) + `private/system-instructions.md` (personal) | Codex reads natively. Claude Code reads via `CLAUDE.md` symlink → `AGENTS.md`, plus `CLAUDE.local.md` → `private/system-instructions.md`. |
| **Skills** | `.agents/skills/<name>/SKILL.md` ([agentskills.io](https://agentskills.io) spec) | Codex reads natively. Claude Code reads via `.claude/skills/` symlink. |
| **Hook scripts** | `.claude/hooks/` (env-agnostic shell scripts) | Both tools invoke the same scripts. `.codex/hooks/` is a symlink. |

### What needs adaptation (different config formats)

| Primitive | Claude Code | Codex CLI | Reconciliation |
|---|---|---|---|
| **Hook wiring** | `.claude/settings.json` | `.codex/hooks.json` | Generated from `.claude/settings.json` by `scripts/sync-codex.sh` |
| **Subagents** | `.claude/agents/*.md` (Markdown + YAML) | `.codex/agents/*.toml` (TOML) | Generated from `.claude/agents/` by `scripts/sync-codex.sh` |
| **MCP servers** | `.claude/settings.json` | `.codex/config.toml` | Maintained separately (small, low-rot risk) |

`scripts/verify-sync.sh` is a pre-commit guard that fails if the Codex side has drifted from the Claude side.

### Codex CLI gaps (accept these)

- **No auto-triggered skills.** Codex invokes skills via `$skill-name` (explicit). Claude Code auto-triggers from intent. You'll need to be more explicit on Codex.
- **No auto-dispatched subagents.** Codex spawns subagents only on explicit request.
- **Hooks need `[features] codex_hooks = true`** in `.codex/config.toml` (handled in this repo).

---

## Claude Code & Codex CLI Architecture

Understanding this helps if you want to customize or extend it.

### Skills

Auto-triggered workflows in Claude Code; explicitly invoked in Codex CLI. The skill files (one [agentskills.io](https://agentskills.io)-compliant `SKILL.md` per skill) live in `.agents/skills/` (canonical) with `.claude/skills/` symlinked to that path.

| Skill | Triggers when you... |
|-------|----------------------|
| `start-day` | Say good morning, want to set today's MIT |
| `end-day` | Wind down, ask "how did today go" |
| `monologue` | Start dumping thoughts unprompted |
| `deep-dive` | Want to dig into a pattern, calibrate an assessment, work through a decision |
| `plan-week` | Want to set focus for the week ahead |
| `weekly-review` | Want to look back at the week, organize the journal |
| `onboarding` | Are setting up the system for the first time |
| `import-history` | Have old journals to bring in |
| `add-framework` | Mention a framework or methodology you want to add |
| `setup-backups` | Want to configure automatic backups |
| `backup` | Want to run a backup |

### Agents

Auto-invoked by Claude when relevant. Located in `.claude/agents/`.

| Agent | Triggers on |
|-------|-------------|
| `search` | Questions about your past, patterns, history |

### Hooks

Claude Code hooks that enforce rules. Located in `.claude/hooks/`.

| Hook | Purpose |
|------|---------|
| `PreToolUse` | Blocks `git add`/`commit`/`push` of `private/`, `CLAUDE.md`, `CLAUDE.local.md`, or `AGENTS.override.md` |
| `PostToolUse` | Reviews committed diffs for accidentally included personal info |

### Adding Your Own

**New skill:** Create `.claude/skills/your-skill/SKILL.md` with frontmatter (`name`, `description`). The description is what makes it auto-trigger — list the situations where you want it to fire.

**New framework:** Tell Claude you want to add one — the add-framework skill researches and creates it.

---

## Privacy

**Local storage:** The `private/` folder is gitignored. Your journal files stay on your machine in markdown you control. A security hook blocks any attempt to commit `private/`, `CLAUDE.md`, `CLAUDE.local.md`, or `AGENTS.override.md`.

**But be aware:** When you use Claude Code, your prompts and file contents are sent to Anthropic's servers. This means your reflections pass through their API. What that means for privacy:

- **Training:** Consumer accounts (Pro/Max) can opt out of model training at [claude.ai/settings](https://claude.ai/settings). Commercial API accounts are excluded from training by default.
- **Retention:** With training opt-out, data is retained for 30 days. With opt-in, up to 5 years.
- **Trust & Safety:** Anthropic's safety team can review flagged content regardless of your settings.
- **Telemetry:** You can disable non-essential telemetry with `export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`.

This is a journaling tool, not a secure vault. Don't include passwords, financial account numbers, or information that could harm others if exposed. For maximum privacy, use a commercial API account with zero-retention configured.

**Backups:** Tell Claude you want to set up backups — the setup-backups skill walks you through configuring automatic backups to Dropbox, iCloud, or a local folder. Backups also run during weekly review.

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

*Built for Claude Code & OpenAI Codex CLI*
