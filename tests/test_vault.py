import concurrent.futures
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from vault import Vault, digest, hook, verify_backup
from memory_guard import guard
from check_staged import check


class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.v = Vault(self.base / 'private')

    def capture(self, id='entry-one', text='I paused the garden project yesterday.', **kw):
        return self.v.capture(dict(id=id, text=text, recorded_at='2024-02-12T10:00:00-07:00', **kw))

    def state(self, id='state-one', source='entry-one', **kw):
        data = dict(id=id, source=source, subject='project:garden', predicate='project-status',
                    value='paused', evidence='paused', as_of='2024-02-11')
        data.update(kw)
        return self.v.assert_state(data)

    def test_exact_crlf_and_idempotence(self):
        text = '\r\nCafé\r\n  uncertainty\t\r\n'
        self.assertTrue(self.capture(text=text)['created'])
        self.assertFalse(self.capture(text=text)['created'])
        self.assertEqual(self.v.show('entry-one')['text'], text)
        with self.assertRaises(ValueError): self.capture(text='changed')
        self.assertTrue(self.v.audit()['ok'])

    def test_unknown_types_and_delivery(self):
        for invalid in ([], None, {'text':'x','event_date':'2024-02-11'}, {'text':'x','references':'bad'}, {'text':'x','entities':'x'}):
            with self.assertRaises(ValueError): self.v.capture(invalid)
        with self.assertRaises(ValueError): self.capture(kind='assistant_framing')
        self.capture(kind='assistant_framing', delivered=True)
        with self.assertRaises(ValueError): self.state()
        self.state(kind='assistant_hypothesis')

    def test_source_quote_required(self):
        self.capture()
        with self.assertRaises(ValueError): self.state(evidence='we mutually decided')
        self.state()
        self.assertEqual(self.v.current()[0]['assertions'][0]['as_of'], '2024-02-11')

    def test_supersession_and_old_import(self):
        self.capture(); self.state()
        self.capture(id='entry-older', text='The project is active.', occurred_on='2023-11-01')
        self.state(id='state-older', source='entry-older', value='active', evidence='active', as_of='2023-11-01')
        self.assertEqual(self.v.current()[0]['assertions'][0]['value'], 'paused')
        self.capture(id='entry-correct', text='I was mistaken: the project is active.')
        self.state(id='state-correct', source='entry-correct', value='active', evidence='active', supersedes=['state-one'])
        self.assertEqual(self.v.current()[0]['assertions'][0]['value'], 'active')
        self.assertEqual(self.v.show('entry-one')['text'], 'I paused the garden project yesterday.')

    def test_conflicting_reports_not_silently_chosen(self):
        self.capture(); self.state()
        self.capture(id='entry-other', text='The project is active.')
        self.state(id='state-other', source='entry-other', value='active', evidence='active')
        self.assertTrue(self.v.current()[0]['conflict'])
        self.v.build()
        self.assertIn('Unresolved conflicting', (self.v.views/'current.md').read_text())

    def test_concurrency(self):
        def capture(i): return self.capture(id='entry-'+str(i))
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(capture, range(16)))
        self.assertEqual(len(list(self.v.records())), 16)
        self.assertTrue(all(r['created'] for r in results))
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(lambda _: self.capture(id='same'), range(8)))
        self.assertEqual(sum(r['created'] for r in results), 1)

    def test_fresh_search_show_and_html(self):
        self.v.build()
        self.capture(text='Uniqueexampleword </script><script>alert(1)</script>', entities=['project:garden'])
        hits = self.v.search('Uniqueexampleword')
        self.assertEqual(hits[0]['id'], 'entry-one')
        html = (self.v.views/'graph.html').read_text()
        self.assertNotIn('</script><script>alert(1)</script>', html)
        self.assertIn('Uniqueexampleword', html)
        self.assertIn('connect-src', html)

    def test_import_dedup_and_show(self):
        source = self.base/'old.txt'; source.write_bytes(b'Originaljournalword\r\n')
        first = self.v.import_source(source)
        self.assertFalse(self.v.import_source(source)['created'])
        self.assertEqual(self.v.show(first['id'])['text'], 'Originaljournalword\r\n')
        result = self.v.search('Originaljournalword')[0]
        self.assertEqual(self.v.show(result['id'])['text'], 'Originaljournalword\r\n')
        self.assertEqual(result['speaker'], 'mixed/unknown')
        graph=json.loads((self.v.views/'graph.json').read_text())
        self.assertIn(first['id'], {n['id'] for n in graph['nodes']})
        with self.assertRaises(ValueError): self.state(source=first['id'])
        Path(first['path']).write_text('tampered')
        self.assertFalse(self.v.audit()['ok'])

    def test_import_symlink_rejected(self):
        source=self.base/'original'; source.write_text('original')
        link=self.base/'link'; link.symlink_to(source)
        with self.assertRaises(ValueError): self.v.import_source(link)

    def test_legacy_freeze_and_guard(self):
        journal=self.v.root/'journal/2024-W01.md'; journal.parent.mkdir(parents=True); journal.write_text('Historical unchanged')
        self.v.legacy_manifest(True)
        result=guard(self.v, {'hook_event_name':'PreToolUse', 'tool_input':{'file_path':str(journal), 'new_string':'edit'}})
        self.assertEqual(result['hookSpecificOutput']['permissionDecision'], 'deny')
        journal.write_text('modified')
        self.assertFalse(self.v.audit()['ok'])

    def test_attribution_checks_added_delta(self):
        path=self.v.root/'relationships/example.md';path.parent.mkdir(parents=True);path.write_text("**User’s words:** old section")
        result=guard(self.v, {'hook_event_name':'PostToolUse','tool_input':{'file_path':str(path),'new_string':'She feels certain about the choice.'}})
        self.assertIn('additionalContext', result['hookSpecificOutput'])

    def test_hook_receipt_resume_and_empty(self):
        data={'hook_event_name':'UserPromptSubmit','session_id':'session-one','turn_id':'turn-one','prompt':'This is my exact dump.\nStill going.'}
        result=hook(self.v,data)
        hook(self.v,data)
        self.assertIn('source ID', result['hookSpecificOutput']['additionalContext'])
        self.assertEqual(len(list(self.v.records())),1)
        self.assertEqual(hook(self.v, {'hook_event_name':'UserPromptSubmit','prompt':''}),{})
        self.assertIn('Memory v2',hook(self.v,{'hook_event_name':'SessionStart'})['hookSpecificOutput']['additionalContext'])

    def test_restore_and_tamper(self):
        self.capture(); self.state()
        (self.v.root/'import').mkdir();(self.v.root/'import/older.txt').write_bytes(b'original\r\n')
        backup=self.v.backup(self.base/'backups')
        result=verify_backup(backup['archive'],self.base/'restore')
        restored=Vault(result['vault_path'])
        self.assertEqual(restored.show('entry-one'),dict(self.v.show('entry-one'),path=str(restored.entries/'2024-02-12/entry-one.md')))
        self.assertTrue(restored.audit()['ok'])
        self.assertEqual((restored.root/'import/older.txt').read_bytes(),b'original\r\n')
        with self.assertRaises(ValueError):verify_backup(backup['archive'],self.base/'restore')
        bad=self.base/'bad.zip'
        with zipfile.ZipFile(bad,'w') as archive:
            archive.writestr('BACKUP-MANIFEST.json',json.dumps({'files':{'private/../../escape':digest('x')}}))
            archive.writestr('private/../../escape','x')
        with self.assertRaises(ValueError):verify_backup(bad,self.base/'escape-restore')
        self.assertFalse((self.base/'escape').exists())

    def test_invalid_supersession_detected(self):
        self.capture(); self.state()
        path=self.v.state_dir/'assertions/state-one.json'
        data=json.loads(path.read_text()); data['supersedes']=['missing']; path.write_text(json.dumps(data))
        self.assertFalse(self.v.audit()['ok'])

    def test_retry_repairs_missing_operation_receipt(self):
        self.capture()
        ledger = self.v.state_dir/'operations.jsonl'
        ledger.write_text('')
        self.assertFalse(self.capture()['created'])
        self.assertEqual(len(ledger.read_text().splitlines()), 1)
        self.capture()
        self.assertEqual(len(ledger.read_text().splitlines()), 1)

    def test_timeline_orders_absolute_time(self):
        self.v.capture({'id':'earlier','text':'earlier','recorded_at':'2024-02-12T01:00:00+10:00'})
        self.v.capture({'id':'later','text':'later','recorded_at':'2024-02-11T23:00:00-07:00'})
        self.v.build()
        timeline=(self.v.views/'timeline.md').read_text()
        self.assertLess(timeline.index('later.md'), timeline.index('earlier.md'))

    def test_staged_private_symlink_is_blocked(self):
        repo=self.base/'public';repo.mkdir()
        subprocess.run(['git','init','-q',str(repo)],check=True)
        (repo/'leak.md').symlink_to('private/journal.md')
        subprocess.run(['git','-C',str(repo),'add','leak.md'],check=True)
        self.assertTrue(any('Symlink' in error for error in check(repo)))

    def test_staged_guard_without_client(self):
        repo=self.base/'public';repo.mkdir()
        subprocess.run(['git','init','-q',str(repo)],check=True)
        (repo/'private').mkdir();(repo/'private/example.md').write_text('synthetic personal content')
        subprocess.run(['git','-C',str(repo),'add','private/example.md'],check=True)
        self.assertTrue(check(repo))
        subprocess.run(['git','-C',str(repo),'rm','--cached','-q','private/example.md'],check=True)
        (repo/'AGENTS.md').write_text('generic instructions');(repo/'CLAUDE.md').symlink_to('AGENTS.md')
        subprocess.run(['git','-C',str(repo),'add','AGENTS.md','CLAUDE.md'],check=True)
        self.assertEqual(check(repo),[])

if __name__ == '__main__': unittest.main()
