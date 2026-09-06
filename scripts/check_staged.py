#!/usr/bin/env python3
"""Reject private paths and common credential patterns without printing contents."""
import posixpath
import re
import subprocess
import sys


def check(root='.'):
    def git(*args):
        return subprocess.check_output(['git', '-C', str(root), *args])
    paths = git('diff', '--cached', '--name-only', '--diff-filter=ACMR', '-z').decode().split('\0')
    problems = []
    for path in filter(None, paths):
        parts = path.split('/')
        if 'private' in parts or any(p.startswith('.env') and p not in {'.env.example', '.env.template'} for p in parts):
            problems.append('Private or secret file staged: ' + path); continue
        content = git('show', ':' + path)
        entry = git('ls-files', '--stage', '--', path)
        if entry.startswith(b'120000 '):
            target = content.decode('utf-8', errors='replace')
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path), target))
            if target.startswith('/') or resolved == '..' or resolved.startswith('../') or 'private' in resolved.split('/'):
                problems.append('Symlink points outside public files: ' + path)
        if re.search(rb'/(?:Users|home)/[A-Za-z0-9_.-]+/', content):
            problems.append('Local home path staged: ' + path)
        if re.search(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:sk-proj-|ghp_)[A-Za-z0-9_-]{20,}', content):
            problems.append('Possible credential staged: ' + path)
    return problems

if __name__ == '__main__':
    errors = check()
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        print('Remove these items from the public commit and review the staged diff.', file=sys.stderr)
    sys.exit(bool(errors))
