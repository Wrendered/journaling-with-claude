# Concepts

> **Atomic notes about yourself.** One idea per file. Declarative filenames.
>
> Pattern from Andy Matuschak / Zettelkasten: evergreen notes are atomic and titled as claims, so the filename itself is a useful piece of context.

## How to use

Each file captures **one stable insight** about yourself, your patterns, your values, or how you operate. Distilled from journal entries and deep-dives over time, not written in advance.

### Filename convention

Declarative statements, kebab-case, lowercase:

```
i-process-grief-by-building-things.md
my-curiosity-is-stronger-than-my-discipline.md
i-avoid-decisions-when-shame-is-loud.md
i-think-best-by-talking-out-loud.md
performance-coaching-doesn't-work-when-the-stuck-is-upstream-of-action.md
```

The filename is the claim. The body is the evidence and the nuance.

### Body structure

```markdown
---
type: concept
created: 2026-05-09
last-touched: 2026-05-09
tags: [self-knowledge, pattern]
---

# [Filename as title]

## Where it shows up

[Specific situations where this is true. Quote your own words from past entries when possible.]

## Where it isn't true

[Counterexamples. The nuance that prevents this from becoming a label.]

## Related concepts

- [link to related concept file]

## History

- 2026-05-09 — first noted in deep-dive about [topic]
- [later additions as the concept gets refined]
```

## Difference from self-map.md

- `self-map.md` is the **summary** — short, scannable, evergreen
- `concepts/` are the **claims** — one per file, with context and history
- Insights graduate: noticed in journal → tested in deep-dive → if stable, become a concept file → if very stable, summarized in self-map

## What NOT to put here

- Today's mood (that's in `log.md` or daily journal)
- Decisions in progress (that's in `decisions/`)
- Information about other people (that's in `relationships/`)
- Random insights you haven't tested yet (let them stay in journal until they recur)
