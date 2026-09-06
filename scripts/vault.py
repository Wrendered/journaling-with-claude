#!/usr/bin/env python3
"""Local, source-preserving journal operations. Python standard library only."""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import sys
import tempfile
import uuid
import zipfile
from zoneinfo import ZoneInfo

REPO = Path(__file__).resolve().parent.parent
SKIP = {'.git', '.venv', 'venv', 'node_modules', '__pycache__', '.cache',
        '.pytest_cache', '.mypy_cache', '.ipynb_checkpoints'}
KINDS = {'user_statement': 'user', 'assistant_framing': 'assistant',
         'assistant_summary': 'assistant', 'system_observation': 'system'}
RELATIONS = {'about', 'mentions', 'source_for', 'related_project', 'supersedes', 'contradicts'}


def digest(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode()).hexdigest()


def now(zone=None):
    zone = zone or os.environ.get('VAULT_TIMEZONE')
    current = dt.datetime.now(ZoneInfo(zone)) if zone else dt.datetime.now().astimezone()
    return current.isoformat(timespec='microseconds')

def fields(data, allowed):
    if not isinstance(data, dict):
        raise ValueError('Input must be a JSON object.')
    unknown = set(data) - set(allowed.split())
    if unknown:
        raise ValueError('Unknown fields: ' + ', '.join(sorted(unknown)))

def sequence(value, label):
    if not isinstance(value, list):
        raise ValueError(label + ' must be an array.')
    return value


def date(value):
    if value is not None:
        dt.date.fromisoformat(value)
    return value


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.:-]{0,159}', value):
        raise ValueError('Invalid identifier: use letters, digits, dot, underscore, colon or hyphen.')
    return value


def stamp(value):
    parsed = dt.datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError('recorded_at must include a timezone offset.')
    return parsed


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='.' + path.name, dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(data.encode() if isinstance(data, str) else data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def dumps(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def parse_record(path):
    text = path.read_bytes().decode('utf-8')
    if not text.startswith('---\n'):
        raise ValueError('Record has no metadata: ' + str(path))
    header, sep, body = text[4:].partition('\n---\n')
    if not sep:
        raise ValueError('Record metadata is not closed: ' + str(path))
    meta = json.loads(header)
    if meta.get('schema') != 2 or meta.get('sha256') != digest(body):
        raise ValueError('Record integrity mismatch: ' + str(path))
    return meta, body


class Vault:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.state_dir = self.root / 'state'
        self.entries = self.root / 'journal/entries'
        self.cache = self.root / '.cache'
        self.views = self.root / 'views'

    @contextlib.contextmanager
    def locked(self):
        self.state_dir.mkdir(parents=True, exist_ok=True)
        with (self.state_dir / '.lock').open('a') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            yield

    def path(self, relative):
        p = (self.root / relative).resolve()
        if not p.is_relative_to(self.root):
            raise ValueError('Path escapes the vault.')
        return p

    def operation(self, kind, object_id, path):
        item = {'id': kind + ':' + object_id, 'operation': kind, 'object': object_id,
                'recorded_at': now(), 'path': str(path.relative_to(self.root))}
        ledger = self.state_dir / 'operations.jsonl'
        if ledger.exists():
            for line in ledger.read_text().splitlines():
                if json.loads(line).get('id') == item['id']:
                    return
        with ledger.open('a', encoding='utf-8') as f:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
            f.flush()
            os.fsync(f.fileno())

    def records(self):
        for p in sorted(self.entries.glob('*/*.md')):
            meta, body = parse_record(p)
            yield p, meta, body

    def source(self, source_id):
        for p, meta, body in self.records():
            if meta['id'] == source_id:
                return p, meta, body
        raise ValueError('Source record not found: ' + source_id)

    def show(self, source_id):
        if source_id.startswith('file:'):
            p = self.path(source_id[5:])
            if p.is_symlink() or p.suffix.lower() not in {'.md', '.txt'}:
                raise ValueError('Unsupported document.')
            return {'path': str(p), 'metadata': {'id': source_id, 'speaker': 'mixed/unknown', 'kind': 'legacy_document'},
                    'text': p.read_bytes().decode('utf-8', errors='replace')}
        if source_id.startswith('import:'):
            sha = source_id.removeprefix('import:')
            if not re.fullmatch(r'[a-f0-9]{64}', sha):
                raise ValueError('Invalid import ID.')
            folder = self.root / 'raw/imports' / sha
            meta = json.loads((folder / 'source.json').read_text())
            p = folder / meta['stored_name']
            content = p.read_bytes()
            if digest(content) != sha:
                raise ValueError('Imported original failed integrity check.')
            return {'path': str(p), 'metadata': meta, 'text': content.decode('utf-8') if p.suffix in {'.txt', '.md'} else None}
        path, meta, body = self.source(source_id)
        return {'path': str(path), 'metadata': meta, 'text': body}

    def capture(self, data):
        fields(data, 'id text kind speaker delivered recorded_at occurred_on session_id title entities references source_origin')
        with self.locked():
            rid = identifier(data.get('id') or 'entry-' + uuid.uuid4().hex)
            existing = list(self.entries.glob('*/' + rid + '.md'))
            old = parse_record(existing[0])[0] if existing else {}
            text = data.get('text')
            if not isinstance(text, str) or not text.strip():
                raise ValueError('A nonempty exact text is required.')
            kind = data.get('kind', 'user_statement')
            speaker = data.get('speaker', KINDS.get(kind))
            if kind not in KINDS or KINDS[kind] != speaker:
                raise ValueError('Speaker and record kind disagree.')
            if speaker == 'assistant' and data.get('delivered') is not True:
                raise ValueError('Only already-delivered assistant text may be recorded.')
            recorded = data.get('recorded_at', old.get('recorded_at', now()))
            local = stamp(recorded)
            occurred = date(data.get('occurred_on'))
            entities = sorted(set(identifier(x) for x in sequence(data.get('entities', []), 'entities')))
            refs = sequence(data.get('references', []), 'references')
            for ref in refs:
                fields(ref, 'relation target evidence')
                if ref.get('relation') not in RELATIONS or not isinstance(ref.get('target'), str) or not ref['target']:
                    raise ValueError('References need an allowed relation and target identifier.')
            meta = {'schema': 2, 'id': rid, 'type': 'journal', 'kind': kind, 'speaker': speaker,
                    'recorded_at': recorded, 'occurred_on': occurred,
                    'session_id': str(data.get('session_id', '')), 'title': str(data.get('title', 'Journal entry')),
                    'entities': entities, 'references': refs, 'sha256': digest(text)}
            if data.get('source_origin'):
                meta['source_origin'] = data['source_origin']
            if speaker == 'assistant':
                meta['delivered'] = True
            if existing:
                if old != meta or parse_record(existing[0])[1] != text:
                    raise ValueError('Record ID already exists with different content. Capture a new correction.')
                self.operation('capture', rid, existing[0])
                return {'id': rid, 'path': str(existing[0]), 'created': False}
            path = self.entries / local.date().isoformat() / (rid + '.md')
            write(path, '---\n' + dumps(meta).rstrip('\n') + '\n---\n' + text)
            self.operation('capture', rid, path)
            return {'id': rid, 'path': str(path), 'created': True}

    def assertions(self):
        return [json.loads(p.read_text()) for p in sorted((self.state_dir / 'assertions').glob('*.json'))]

    def assert_state(self, data):
        fields(data, 'id source evidence kind subject predicate value supersedes as_of')
        with self.locked():
            rid = identifier(data.get('id') or 'state-' + uuid.uuid4().hex)
            source_id = identifier(data['source'])
            _, source, body = self.source(source_id)
            evidence = data.get('evidence')
            if not isinstance(evidence, str) or not evidence.strip() or evidence not in body:
                raise ValueError('Evidence must be an exact nonempty substring of the source.')
            kind = data.get('kind', 'user_report')
            if kind not in {'user_report', 'assistant_hypothesis'}:
                raise ValueError('Unsupported assertion kind.')
            expected = 'user' if kind == 'user_report' else 'assistant'
            if source['speaker'] != expected:
                raise ValueError('Assertion kind does not match source authorship.')
            if not isinstance(data.get('value'), str) or not data['value'].strip():
                raise ValueError('State value must be a nonempty string.')
            subject, predicate = identifier(data['subject']), identifier(data['predicate'])
            supersedes = sorted(set(identifier(x) for x in sequence(data.get('supersedes', []), 'supersedes')))
            known = {s['id']: s for s in self.assertions()}
            for prior in supersedes:
                if prior == rid or prior not in known:
                    raise ValueError('Superseded assertion must already exist.')
                if (known[prior]['subject'], known[prior]['predicate'], known[prior]['kind']) != (subject, predicate, kind):
                    raise ValueError('Supersession must address the same subject, predicate and attribution kind.')
            item = {'schema': 2, 'id': rid, 'subject': subject, 'predicate': predicate,
                    'value': data['value'], 'kind': kind, 'source': source_id, 'evidence': evidence,
                    'as_of': date(data.get('as_of') or source.get('occurred_on') or stamp(source['recorded_at']).date().isoformat()),
                    'recorded_at': source['recorded_at'], 'supersedes': supersedes}
            p = self.state_dir / 'assertions' / (rid + '.json')
            if p.exists():
                if json.loads(p.read_text()) != item:
                    raise ValueError('Assertion ID exists with different content. Write a new superseding assertion.')
                self.operation('state', rid, p)
                return {'id': rid, 'created': False}
            write(p, dumps(item))
            self.operation('state', rid, p)
            return {'id': rid, 'created': True}

    def current(self):
        states = self.assertions()
        superseded = {x for s in states for x in s['supersedes']}
        groups = {}
        for s in states:
            if s['id'] not in superseded:
                groups.setdefault((s['subject'], s['predicate'], s['kind']), []).append(s)
        result = []
        for key, rows in sorted(groups.items()):
            latest = max(s['as_of'] for s in rows)
            current = [s for s in rows if s['as_of'] == latest]
            result.append({'subject': key[0], 'predicate': key[1], 'kind': key[2],
                           'conflict': len({s['value'] for s in current}) > 1, 'assertions': current})
        return result

    def documents(self):
        for base, dirs, files in os.walk(self.root, followlinks=False):
            dirs[:] = sorted(d for d in dirs if d not in SKIP and d not in {'views', 'state'}
                              and not (Path(base) / d).is_symlink())
            for name in sorted(files):
                p = Path(base) / name
                if p.is_symlink() or p.suffix.lower() not in {'.md', '.txt'}:
                    continue
                rel = str(p.relative_to(self.root))
                if rel.startswith('journal/entries/'):
                    meta, body = parse_record(p)
                    yield {'id': meta['id'], 'path': rel, 'title': meta['title'], 'text': body,
                           'speaker': meta['speaker'], 'kind': meta['kind'], 'recorded_at': meta['recorded_at'],
                           'occurred_on': meta['occurred_on'], 'legacy': False, 'meta': meta}
                else:
                    body = p.read_text(encoding='utf-8', errors='replace')
                    title = next((line.lstrip('# ').strip() for line in body.splitlines() if line.startswith('# ')), p.stem)
                    yield {'id': 'file:' + rel, 'path': rel, 'title': title, 'text': body,
                           'speaker': 'mixed/unknown', 'kind': 'legacy_document', 'recorded_at': '',
                           'occurred_on': None, 'legacy': True, 'meta': {}}

    def build(self):
        with self.locked():
            self.cache.mkdir(parents=True, exist_ok=True)
            self.views.mkdir(parents=True, exist_ok=True)
            docs = list(self.documents())
            fd, tmp = tempfile.mkstemp(suffix='.sqlite', dir=self.cache)
            os.close(fd)
            try:
                conn = sqlite3.connect(tmp)
                conn.executescript('CREATE TABLE documents(id TEXT PRIMARY KEY, path TEXT, title TEXT, text TEXT, speaker TEXT, kind TEXT, recorded_at TEXT, occurred_on TEXT, legacy INTEGER); CREATE VIRTUAL TABLE search USING fts5(id UNINDEXED, title, text, tokenize="unicode61");')
                for d in docs:
                    conn.execute('INSERT INTO documents VALUES (?,?,?,?,?,?,?,?,?)', tuple(d[k] for k in ['id', 'path', 'title', 'text', 'speaker', 'kind', 'recorded_at', 'occurred_on', 'legacy']))
                    conn.execute('INSERT INTO search VALUES (?,?,?)', (d['id'], d['title'], d['text']))
                conn.commit()
                conn.close()
                os.replace(tmp, self.cache / 'vault.sqlite')
            finally:
                if os.path.exists(tmp):
                    os.unlink(tmp)
            nodes = {d['id']: {k: d[k] for k in ['id', 'path', 'title', 'text', 'speaker', 'kind', 'recorded_at', 'occurred_on', 'legacy']} for d in docs}
            bypath = {d['path']: d['id'] for d in docs}
            stems = {}
            for d in docs:
                stems.setdefault(Path(d['path']).stem, []).append(d['id'])
            for d in docs:
                for entity in d['meta'].get('entities', []):
                    nodes.setdefault(entity, {'id': entity, 'title': entity.replace(':', ': '), 'kind': 'entity', 'text': ''})
            for assertion in self.assertions():
                nodes.setdefault(assertion['id'], {'id': assertion['id']})
                nodes.setdefault(assertion['subject'], {'id': assertion['subject'], 'title': assertion['subject'], 'kind': 'entity', 'text': ''})
            edges, broken = [], []
            for manifest in (self.root / 'raw/imports').glob('*/source.json'):
                imported = json.loads(manifest.read_text())
                relative = str((manifest.parent / imported['stored_name']).relative_to(self.root))
                iid = imported['id']
                nodes[iid] = {'id': iid, 'title': imported['label'], 'kind': 'imported_original',
                              'speaker': 'unverified', 'path': relative, 'text': '', 'recorded_at': imported['imported_at']}
                if relative in bypath:
                    edges.append({'source': iid, 'target': bypath[relative], 'relation': 'source_for',
                                  'provenance': 'import_manifest', 'evidence': 'SHA-256: ' + imported['sha256']})
                else:
                    bypath[relative] = iid
            for d in docs:
                for entity in d['meta'].get('entities', []):
                    nodes.setdefault(entity, {'id': entity, 'title': entity.replace(':', ': '), 'kind': 'entity', 'text': ''})
                    edges.append({'source': d['id'], 'target': entity, 'relation': 'about', 'provenance': 'declared', 'evidence': ''})
                for ref in d['meta'].get('references', []):
                    if ref['target'] in nodes:
                        edges.append({'source': d['id'], 'target': ref['target'], 'relation': ref['relation'], 'provenance': 'declared', 'evidence': ref.get('evidence', '')})
                    else:
                        broken.append({'path': d['path'], 'target': ref['target'], 'new': True})
                for raw in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', d['text']):
                    link = raw.strip('<>').split('#')[0]
                    if not link or re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', link):
                        continue
                    target = (self.root / d['path']).parent / link
                    target = target.resolve()
                    if target.is_relative_to(self.root):
                        rel = str(target.relative_to(self.root))
                        if rel in bypath:
                            edges.append({'source': d['id'], 'target': bypath[rel], 'relation': 'mentions', 'provenance': 'document_link', 'evidence': raw})
                        elif not target.exists():
                            broken.append({'path': d['path'], 'target': raw, 'new': not d['legacy']})
                for link in re.findall(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]', d['text']):
                    found = stems.get(Path(link.split('#')[0]).stem, [])
                    if len(found) == 1:
                        edges.append({'source': d['id'], 'target': found[0], 'relation': 'mentions', 'provenance': 'wikilink', 'evidence': link})
            for s in self.assertions():
                nodes[s['id']] = {**s, 'title': s['subject'] + ' / ' + s['predicate'], 'text': s['value'], 'speaker': 'user' if s['kind'] == 'user_report' else 'assistant', 'path': 'state/assertions/' + s['id'] + '.json'}
                nodes.setdefault(s['subject'], {'id': s['subject'], 'title': s['subject'].replace(':', ': '), 'kind': 'entity', 'text': ''})
                edges.extend([{'source': s['source'], 'target': s['id'], 'relation': 'source_for', 'provenance': s['kind'], 'evidence': s['evidence']},
                              {'source': s['id'], 'target': s['subject'], 'relation': 'about', 'provenance': s['kind'], 'evidence': s['evidence']}])
                for previous in s['supersedes']:
                    edges.append({'source': s['id'], 'target': previous, 'relation': 'supersedes', 'provenance': s['kind'], 'evidence': s['evidence']})
            graph = {'built_at': now(), 'nodes': list(nodes.values()), 'edges': edges}
            write(self.views / 'graph.json', dumps(graph))
            template = (REPO / 'templates/graph.html').read_text()
            write(self.views / 'graph.html', template.replace('__VAULT_DATA__', json.dumps(graph, ensure_ascii=False).replace('<', '\\u003c')))
            current = ['# Current context', '', '> Generated from dated, sourced assertions. Earlier notes remain historical evidence.', '']
            for g in self.current():
                current += ['## ' + g['subject'] + ' / ' + g['predicate'], '']
                if g['conflict']:
                    current += ['**Unresolved conflicting reports. Ask before treating either as settled.**', '']
                for s in g['assertions']:
                    source = next(d for d in docs if d['id'] == s['source'])
                    label = 'User report' if s['kind'] == 'user_report' else 'Assistant hypothesis, not user adoption'
                    current += [f"- {s['value']} ({label}; as of {s['as_of']}). [Source](../{source['path']})", f"  Evidence: {json.dumps(s['evidence'], ensure_ascii=False)}", '']
            if not self.current():
                current += ['No sourced current-state assertions yet. Ask about current context; older pages may be stale.', '']
            write(self.views / 'current.md', '\n'.join(current))
            timeline = ['# Journal timeline', '', '> Generated from source records. Event dates and recording dates are separate.', '']
            for d in sorted((d for d in docs if not d['legacy']), key=lambda d: stamp(d['recorded_at']).timestamp(), reverse=True):
                timeline.append(f"- {d['recorded_at']} — [{d['title']}](../{d['path']}) ({d['speaker']}; event: {d['occurred_on'] or 'unspecified'})")
            write(self.views / 'timeline.md', '\n'.join(timeline) + '\n')
            report = {'built_at': graph['built_at'], 'documents': len(docs), 'nodes': len(nodes), 'edges': len(edges), 'broken_links': broken}
            write(self.views / 'index-report.json', dumps(report))
            return {k: v for k, v in report.items() if k != 'broken_links'} | {'broken_links': len(broken)}

    def search(self, query, limit=8):
        db = self.cache / 'vault.sqlite'
        self.build()  # Rebuildable index must never hide a just-saved source.
        words = re.findall(r'\w+', query, flags=re.UNICODE)
        if not words:
            return []
        expression = ' AND '.join('"' + w.replace('"', '""') + '"' for w in words)
        with sqlite3.connect('file:' + str(db) + '?mode=ro', uri=True) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute('SELECT d.id,d.path,d.title,d.speaker,d.kind,d.recorded_at,d.occurred_on,d.legacy,snippet(search,2,\'\',\'\',\' … \',48) AS excerpt FROM search JOIN documents d ON d.id=search.id WHERE search MATCH ? ORDER BY bm25(search) LIMIT ?', (expression, max(1, min(limit, 50)))).fetchall()
            return [dict(r) for r in rows]

    def import_source(self, file, label=None):
        src = Path(file).expanduser()
        if not src.is_file() or src.is_symlink():
            raise ValueError('Import needs a regular source file.')
        src = src.resolve()
        content = src.read_bytes()
        hash_value = digest(content)
        with self.locked():
            folder = self.root / 'raw/imports' / hash_value
            manifest = folder / 'source.json'
            if manifest.exists():
                old = json.loads(manifest.read_text())
                if digest((folder / old['stored_name']).read_bytes()) != hash_value:
                    raise ValueError('Imported original failed integrity check.')
                self.operation('import', hash_value, manifest)
                return {'id': 'import:' + hash_value, 'path': str(folder / old['stored_name']), 'created': False}
            target = folder / ('original' + src.suffix.lower())
            write(target, content)
            write(manifest, dumps({'schema': 2, 'id': 'import:' + hash_value, 'sha256': hash_value,
                                   'original_name': src.name, 'stored_name': target.name, 'imported_at': now(),
                                   'label': label or src.stem, 'bytes': len(content)}))
            self.operation('import', hash_value, manifest)
            return {'id': 'import:' + hash_value, 'path': str(target), 'created': True}

    def legacy_manifest(self, commit=False):
        files = {}
        candidates = list((self.root / 'journal').glob('????-W??.md'))
        if (self.root / 'log.md').exists():
            candidates.append(self.root / 'log.md')
        candidates += [p for p in (self.root / 'raw').rglob('*') if p.is_file() and not p.is_symlink() and 'imports' not in p.relative_to(self.root / 'raw').parts]
        for p in sorted(candidates):
            files[str(p.relative_to(self.root))] = digest(p.read_bytes())
        result = {'schema': 2, 'created_at': now(), 'files': files, 'policy': 'Legacy originals remain in place; new capture uses schema 2.'}
        if commit:
            with self.locked():
                path = self.state_dir / 'legacy-manifest.json'
                if path.exists():
                    return json.loads(path.read_text())
                write(path, dumps(result))
                self.operation('migration-baseline', 'legacy-v2', path)
        return result

    def audit(self):
        errors, warnings, ids = [], [], set()
        sources = {}
        for p in self.entries.glob('*/*.md'):
            try:
                meta, body = parse_record(p)
                if meta['id'] in ids:
                    raise ValueError('Duplicate record ID: ' + meta['id'])
                ids.add(meta['id'])
                if KINDS.get(meta['kind']) != meta['speaker']:
                    raise ValueError('Invalid source authorship: ' + str(p))
                if meta['speaker'] == 'assistant' and meta.get('delivered') is not True:
                    raise ValueError('Assistant record lacks delivery confirmation: ' + str(p))
                stamp(meta['recorded_at']); date(meta.get('occurred_on'))
                sources[meta['id']] = (meta, body)
            except (ValueError, KeyError, OSError) as e:
                errors.append(str(e))
        states = {s['id']: s for s in self.assertions()}
        for s in states.values():
            if s.get('kind') not in {'user_report', 'assistant_hypothesis'} or not s.get('evidence'):
                errors.append('Invalid assertion kind or empty evidence: ' + s['id'])
            date(s['as_of']); stamp(s['recorded_at'])
            for prior in s.get('supersedes', []):
                other = states.get(prior)
                if prior == s['id'] or not other or any(s[k] != other[k] for k in ('subject', 'predicate', 'kind')):
                    errors.append('Invalid supersession: ' + s['id'])
            found = sources.get(s['source'])
            if not found or s['evidence'] not in found[1]:
                errors.append('Missing or changed assertion evidence: ' + s['id'])
            elif found[0]['speaker'] != ('user' if s['kind'] == 'user_report' else 'assistant'):
                errors.append('Assertion authorship mismatch: ' + s['id'])
        for p in (self.root / 'raw/imports').glob('*/source.json'):
            m = json.loads(p.read_text()); original = p.parent / m['stored_name']
            if not original.is_file() or digest(original.read_bytes()) != m['sha256']:
                errors.append('Imported source changed: ' + str(p))
        manifest = self.state_dir / 'legacy-manifest.json'
        if manifest.exists():
            for relative, expected in json.loads(manifest.read_text())['files'].items():
                p = self.path(relative)
                if not p.is_file() or digest(p.read_bytes()) != expected:
                    errors.append('Legacy original changed: ' + relative)
        report = self.views / 'index-report.json'
        if report.exists():
            links = json.loads(report.read_text()).get('broken_links', [])
            errors += ['Broken new record link: ' + str(x) for x in links if x['new']]
            if any(not x['new'] for x in links):
                warnings.append(str(sum(not x['new'] for x in links)) + ' legacy link candidates need review; originals were preserved.')
        return {'ok': not errors, 'records': len(ids), 'assertions': len(self.assertions()), 'errors': errors, 'warnings': warnings}

    def backup(self, destination):
        destination = Path(destination).expanduser().resolve()
        if destination.is_relative_to(self.root):
            raise ValueError('Backup destination must be outside the vault.')
        destination.mkdir(parents=True, exist_ok=True)
        archive = destination / ('journaling-with-claude_' + dt.datetime.now().strftime('%Y-%m-%d_%H%M%S') + '_' + uuid.uuid4().hex[:6] + '.zip')
        manifest = {'schema': 2, 'created_at': now(), 'files': {}, 'excluded': []}
        with self.locked(), zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as z:
            for base, dirs, files in os.walk(self.root, followlinks=False):
                dirs[:] = [d for d in dirs if d not in SKIP and d != 'views' and not (Path(base) / d).is_symlink()]
                for name in files:
                    p = Path(base) / name
                    if p.is_symlink() or name in {'.DS_Store', '.lock'} or name.startswith('.env') or name.endswith('.pyc'):
                        manifest['excluded'].append(str(p.relative_to(self.root))); continue
                    content = p.read_bytes(); relative = 'private/' + str(p.relative_to(self.root))
                    z.writestr(relative, content)
                    manifest['files'][relative] = digest(content)
            z.writestr('BACKUP-MANIFEST.json', dumps(manifest))
        checked = verify_backup(archive)
        return {'archive': str(archive), **checked}


def verify_backup(archive, restore_to=None, password=None):
    with zipfile.ZipFile(archive) as z:
        if password is not None:
            z.setpassword(password)
        manifest = json.loads(z.read('BACKUP-MANIFEST.json'))
        if z.testzip():
            raise ValueError('Backup CRC check failed.')
        for name, expected in manifest['files'].items():
            parts = Path(name).parts
            if Path(name).is_absolute() or '..' in parts or not parts or parts[0] != 'private':
                raise ValueError('Unsafe archive path.')
            if digest(z.read(name)) != expected:
                raise ValueError('Backup hash mismatch: ' + name)
        if restore_to:
            dest = Path(restore_to).resolve()
            if dest.exists() and any(dest.iterdir()):
                raise ValueError('Restore requires an empty destination.')
            dest.mkdir(parents=True, exist_ok=True)
            for name, expected in manifest['files'].items():
                path = dest / name; write(path, z.read(name))
                if digest(path.read_bytes()) != expected:
                    raise ValueError('Restored file mismatch: ' + name)
    return {'verified': True, 'files': len(manifest['files']), 'restored': bool(restore_to),
            'vault_path': str(Path(restore_to).resolve() / 'private') if restore_to else None}


def hook(vault, data):
    if not isinstance(data, dict):
        raise ValueError('Hook input must be a JSON object.')
    event = data.get('hook_event_name')
    if event in {'PreToolUse', 'PostToolUse'}:
        from memory_guard import guard
        return guard(vault, data)
    if event == 'UserPromptSubmit':
        prompt = data.get('prompt')
        if not isinstance(prompt, str) or not prompt.strip():
            return {}
        turn = data.get('turn_id')
        rid = 'prompt-' + (digest(str(data.get('session_id')) + ':' + str(turn))[:32] if turn else uuid.uuid4().hex)
        result = vault.capture({'id': rid, 'text': prompt, 'session_id': data.get('session_id', ''),
                                'title': 'Conversation capture', 'source_origin': {'host': 'prompt_hook', 'turn_id': turn}})
        return {'hookSpecificOutput': {'hookEventName': event, 'additionalContext': 'Exact user text saved before response: ' + result['path'] + '. Reuse this source ID for sourced status updates: ' + rid}}
    if event == 'SessionStart':
        vault.build()
        current = (vault.views / 'current.md').read_text()
        return {'hookSpecificOutput': {'hookEventName': event, 'additionalContext': 'Memory v2 is active. Read private/system-instructions.md for personal preferences. Current dated evidence:\n' + current[:10000]}}
    if event in {'Stop', 'PreCompact'}:
        vault.build()
        return {}
    return {}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--vault', default=str(REPO / 'private'))
    sub = p.add_subparsers(dest='command', required=True)
    for command in ['capture', 'state', 'hook']:
        q = sub.add_parser(command); q.add_argument('--input', default='-')
    sub.add_parser('build'); sub.add_parser('audit'); sub.add_parser('current')
    q = sub.add_parser('search'); q.add_argument('query'); q.add_argument('--limit', type=int, default=8)
    q = sub.add_parser('show'); q.add_argument('id')
    q = sub.add_parser('import'); q.add_argument('file'); q.add_argument('--label')
    q = sub.add_parser('legacy-manifest'); q.add_argument('--write', action='store_true')
    q = sub.add_parser('backup'); q.add_argument('--destination', required=True)
    q = sub.add_parser('verify-backup'); q.add_argument('archive'); q.add_argument('--password-prompt', action='store_true'); q.add_argument('--restore-to', help='Restore into a new or empty directory; vault will be DEST/private')
    args = p.parse_args(); v = Vault(args.vault)
    try:
        if args.command in {'capture', 'state', 'hook'}:
            data = json.load(sys.stdin) if args.input == '-' else json.loads(Path(args.input).read_text())
            result = v.capture(data) if args.command == 'capture' else v.assert_state(data) if args.command == 'state' else hook(v, data)
        elif args.command == 'build': result = v.build()
        elif args.command == 'audit': result = v.audit()
        elif args.command == 'current': result = v.current()
        elif args.command == 'search': result = v.search(args.query, args.limit)
        elif args.command == 'show':
            result = v.show(args.id)
        elif args.command == 'import': result = v.import_source(args.file, args.label)
        elif args.command == 'legacy-manifest': result = v.legacy_manifest(args.write)
        elif args.command == 'backup': result = v.backup(args.destination)
        else:
            import getpass
            password = getpass.getpass('Archive password: ').encode() if args.password_prompt else None
            result = verify_backup(args.archive, args.restore_to, password)
        print(dumps(result), end='')
        return 1 if isinstance(result, dict) and result.get('ok') is False else 0
    except (ValueError, TypeError, OSError, KeyError, sqlite3.Error, zipfile.BadZipFile, RuntimeError) as e:
        if args.command == 'hook':
            print(dumps({'systemMessage': 'Journal persistence needs attention: ' + str(e)}), end='')
        else:
            print('vault: ' + str(e), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
