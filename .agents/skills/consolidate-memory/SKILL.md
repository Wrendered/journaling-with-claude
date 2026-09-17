---
name: consolidate-memory
description: Audit source integrity, stale wiki claims, contradictory state, and broken links; propose evidence-backed repairs.
---

# Consolidate Memory

Read [the shared memory contract](../../../docs/memory-contract.md) before the first capture, state update, or import in a session. Use AGENTS.md for privacy, attribution, and current-context precedence.

1. Read the memory contract, build derived views, and run scripts/vault.py audit. Capture the request if it contains reflection.
2. Inspect generated current-state conflicts and index-report.json. Separate errors affecting new evidence from legacy link candidates, including code examples and stale filenames.
3. Check wiki assertions against cited originals. A recent summary of old material does not establish current truth. Count independent observations and identify missing dates or provenance.
4. Produce a concise report under private/reviews/ with exact source links, confidence, and proposed edits. Do not silently resolve conflicting reports or turn assistant hypotheses into user conclusions.
5. Repair mechanical derived output directly. For substantive wiki changes, use already-given authorization or discuss the concrete proposed edit. Originals remain immutable; corrections become new records and explicit supersessions.
6. Rebuild and re-audit after changes. Report unresolved issues honestly. Do not run deletion, private Git commits, or backup pruning.
