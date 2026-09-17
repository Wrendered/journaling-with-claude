#!/usr/bin/env python3
"""File-tool guardrails; source hashes remain the audit boundary for shell edits."""
import json
from pathlib import Path
import re


def changed_files(data):
    tool = data.get('tool_input', {})
    if isinstance(tool, str):
        tool = {'patch': tool}
    changes = []
    if isinstance(tool, dict):
        if tool.get('file_path') or tool.get('path'):
            delta = tool.get('new_string', tool.get('content', ''))
            if 'edits' in tool:
                delta = '\n'.join(str(x.get('new_string', '')) for x in tool['edits'])
            changes.append((tool.get('file_path', tool.get('path')), delta))
        patch = tool.get('patch', tool.get('input', ''))
        if isinstance(patch, str):
            path, lines = None, []
            for line in patch.splitlines():
                match = re.match(r'\*\*\* (?:Update|Add|Delete) File: (.+)', line)
                if match:
                    if path: changes.append((path, '\n'.join(lines)))
                    path, lines = match[1], []
                elif line.startswith('*** Move to: '):
                    changes.append((line[13:], ''))
                elif line.startswith('+'):
                    lines.append(line[1:])
            if path: changes.append((path, '\n'.join(lines)))
    return changes


def guard(vault, data):
    event = data.get('hook_event_name')
    cwd = Path(data.get('cwd') or vault.root.parent)
    manifest = vault.state_dir / 'legacy-manifest.json'
    frozen = json.loads(manifest.read_text()).get('files', {}) if manifest.exists() else {}
    warnings = []
    for path, delta in changed_files(data):
        target = (cwd / path).resolve()
        if not target.is_relative_to(vault.root): continue
        rel = str(target.relative_to(vault.root))
        immutable = rel.startswith(('journal/entries/', 'raw/imports/', 'state/assertions/')) or rel in frozen or rel == 'state/legacy-manifest.json'
        if event == 'PreToolUse' and immutable:
            return {'hookSpecificOutput': {'hookEventName': event, 'permissionDecision': 'deny',
                    'permissionDecisionReason': 'This is a preserved source or assertion. Use scripts/vault.py capture, import, or state; make a new correction instead of replacing evidence.'}}
        if event == 'PostToolUse' and re.match(r'(journal|decisions|relationships|history)/', rel):
            # Inspect only inserted/replacement text; old file headings cannot mask a new addition.
            narrative = re.search(r'\b(she|he|they) (said|feels?|thinks?|noted|mentioned|seemed)\b', str(delta), re.I)
            labelled = re.search(r"user.s words|assistant.s? (framing|interpretation)|claude.s (framing|interpretation)", str(delta), re.I)
            if narrative and not labelled:
                warnings.append(rel)
    if warnings:
        return {'hookSpecificOutput': {'hookEventName': event, 'additionalContext':
                'Review attribution in the text just added to: ' + ', '.join(warnings) + '. Keep exact user words separate from assistant interpretation. This heuristic cannot verify meaning.'}}
    return {}
