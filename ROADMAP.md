# Roadmap

## Implemented September 2026

- Shared concise instructions and twelve focused skills for Claude Code and Codex.
- Exact source capture with stable IDs, speaker attribution, checksums, and separate event/recording dates.
- Sourced current-state assertions, explicit supersession, and visible conflicting reports.
- Preserved legacy journals and content-addressed imports.
- Rebuildable full-text search, timeline, current context, and a local interactive graph.
- Client lifecycle adapters, direct-file source guards, changed-text attribution checks, and independent Git staged privacy checks.
- Verified non-pruning backups and restoration into an empty location.
- Synthetic regression tests and independent forward testing.

## Next, driven by actual use

- Evaluate conversational fit with consented or synthetic heart-dump scenarios across selected model/effort combinations. The local regression suite does not constitute a cross-model benchmark.
- Test hooks end to end in fresh client sessions. Already-open sessions use explicit manual capture when no hook receipt is available.
- Improve legacy links incrementally, without rewriting original journals or treating old summaries as current facts.
- Add format-specific extraction adapters as real journal imports arrive; retain originals and extraction provenance.
- Compare lexical retrieval with optional local semantic search on known-answer queries if paraphrase misses become material.
- Add optional graph filtering or Obsidian integration when it makes a concrete reflection workflow easier.

Keep raw files portable, indexes replaceable, and maintenance smaller than the practice it supports. No dedicated graph server or API orchestration layer is required by the current workflow.
