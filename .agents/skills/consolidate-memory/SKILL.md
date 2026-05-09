---
name: consolidate-memory
description: Periodic lint pass over the personal vault (private/) that detects contradictions across pages, stale claims that no longer reflect current state, orphan pages with no inbound links from indexes, and concepts mentioned in journal but lacking their own dedicated file. Reports findings without auto-changing files; user decides what to address.
when_to_use: |
  Invoke this skill when the user wants a maintenance pass over their private vault.
  Trigger phrases (any of these): "consolidate my memory", "lint my vault", "audit private",
  "check for contradictions", "find stale notes", "vault maintenance",
  "what's drifted in my self-map", "are my files still accurate".
  Also invoke periodically during weekly-review (every 4-6 weeks) to keep the wiki coherent.
context: fork
paths:
  - "private/**"
allowed-tools: Read, Glob, Grep, Bash, Task
---

# Consolidate Memory

Periodic maintenance pass over the user's personal vault. Surfaces drift without auto-correcting — the user decides what to address.

This is the Karpathy LLM Wiki "lint" operation: contradictions, stale claims, orphans, missing pages.

## When to Use

- User explicitly asks for a vault audit / maintenance pass
- Every 4-6 weeks during weekly-review (suggest, don't force)
- After any major event that might have shifted self-knowledge (job change, breakup, big realization) — old claims may now be wrong
- Before a deep-dive that's going to lean heavily on `self-map.md` / `concepts/` for context

## What to Check

### 1. Contradictions across pages

Cross-reference claims in `self-map.md`, `concepts/*.md`, and recent journal entries. Look for:
- Claims in `self-map.md` that recent entries directly contradict
- Two concept files making opposing claims about the same pattern
- Decisions whose status (`open` / `resolved`) doesn't match the journal narrative

Use grep to find candidate pairs. Report with file paths and line numbers.

### 2. Stale claims

Read `self-map.md` and each `concepts/*.md` file. Flag:
- Claims with `last-touched` more than 6 months old that haven't been validated
- Claims that reference circumstances that have changed (job, relationship, location, health)
- Claims using absolute language ("I always...", "I never...") that recent entries contradict

### 3. Orphan pages

For each file in `private/concepts/`, `private/decisions/`, `private/relationships/`:
- Check if it's linked from `private/_index.md` or the relevant folder `_index.md`
- Check if it's mentioned anywhere in journal entries from the last 90 days
- Flag pages with no inbound references — they may be candidates for `private/archive/`

### 4. Missing concept pages

Grep recent journal entries (last 90 days) for recurring themes and claims:
- If a phrase or pattern appears 3+ times across journal entries
- AND there's no concept file capturing it
- THEN flag it as a candidate for graduating to `concepts/`

### 5. Tag drift

Read `private/tags.md`. Compare to actual tags in use across `private/**/*.md` frontmatter:
- Tags used but not in the controlled vocabulary → flag as drift
- Tags in the vocabulary but never used → candidates for removal
- Multiple tags for the same concept (e.g., `career`, `career-move`, `job`) → flag as redundancy

### 6. Index drift

For each `_index.md`, verify:
- Files listed in the index actually exist
- Files in the folder are listed in the index (or reasonably elidable)

## Output Format

Single report file: `private/_consolidation-report.md` (gitignored as part of `private/`).

Structure:

```markdown
# Vault Consolidation Report

**Date:** [today]
**Scope:** [what was scanned]

## 1. Contradictions Found
[list with file paths]

## 2. Stale Claims
[list with file paths and last-touched dates]

## 3. Orphan Pages
[list with reasoning]

## 4. Concepts Worth Graduating
[recurring themes from journal that lack concept files]

## 5. Tag Drift
[tags in use vs. tags.md]

## 6. Index Drift
[files in folders vs files in indexes]

---

## Recommended Actions (user decides)
[prioritized list of what to address]
```

## What NOT to do

- Do not auto-edit files based on findings — surface them, let user decide
- Do not move pages to `archive/` without explicit approval
- Do not delete tags from `tags.md` without the user reviewing
- Do not add new concept files — surface candidates, the user writes them

## Approach

For large vaults, use parallel subagents:
- Agent 1: Read `self-map.md` + recent journal entries, look for contradictions
- Agent 2: Walk `concepts/`, check each for staleness and orphan status
- Agent 3: Grep journal for recurring themes vs. existing concept files
- Agent 4: Audit tags + indexes

Consolidate findings into the single report.

For small vaults (under ~50 files), a single sequential pass is fine.

## Related Skills

- `weekly-review` — surfaces patterns from the past 7 days; this skill is the multi-week version
- `deep-dive` — works on a single specific topic; this skill works across the vault
- `import-history` — adds NEW material to the vault; this skill maintains EXISTING material
