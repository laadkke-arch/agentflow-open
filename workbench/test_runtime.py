import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from workbench.cli import (ROOT, catalog, contained, context, export_project,
                           project, run_task, source_check, verify_receipt)


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.parent = Path(self.temp.name)
        self.root = self.parent / 'workspace'
        self.root.mkdir()
        for folder in ('workbench', 'lab', 'docs'):
            shutil.copytree(ROOT / folder, self.root / folder,
                            ignore=shutil.ignore_patterns('__pycache__'))

    def tearDown(self):
        self.temp.cleanup()

    def manifest(self, name='repo-intake', update=None):
        path = self.root / 'lab' / name / 'project.json'
        data = json.loads(path.read_text(encoding='utf-8'))
        if update:
            update(data)
            path.write_text(json.dumps(data), encoding='utf-8')
        return data

    def test_project_registry(self):
        self.assertEqual(set(catalog(self.root)), {'repo-intake','reference-audit'})

    def test_unknown_project(self):
        with self.assertRaisesRegex(ValueError, 'unknown project'):
            project('not-real', self.root)

    def test_project_identity_mismatch(self):
        self.manifest(update=lambda d: d.update(id='wrong'))
        with self.assertRaisesRegex(ValueError, 'identity mismatch'):
            project('repo-intake', self.root)

    def test_reject_parent_and_absolute_paths(self):
        for path in ('../outside', '/tmp/outside', '.git/config', 'C:/temp/file', '..\\file'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                contained(self.root, path, False)

    def test_reject_symlink_escape(self):
        outside = self.parent / 'outside.txt'
        outside.write_text('outside')
        try:
            (self.root/'escape').symlink_to(outside)
        except OSError:
            self.skipTest('symlink creation requires extra privileges on this host')
        with self.assertRaises(ValueError):
            contained(self.root, 'escape')

    def test_manifest_context_cannot_escape(self):
        self.manifest(update=lambda d: d['context'].append('../../README.md'))
        with self.assertRaises(ValueError):
            context('repo-intake', root=self.root)

    def test_missing_context_file(self):
        (self.root/'lab/repo-intake/STATE.md').unlink()
        with self.assertRaises(ValueError):
            context('repo-intake', root=self.root)

    def test_context_contains_own_not_other_project(self):
        for name, own, other in [('repo-intake','INTAKE_ONLY_4C21','AUDIT_ONLY_9E52'),
                                 ('reference-audit','AUDIT_ONLY_9E52','INTAKE_ONLY_4C21')]:
            result = json.dumps(context(name, root=self.root))
            self.assertIn(own, result)
            self.assertNotIn(other, result)

    def test_unknown_search_keeps_required_handover(self):
        pack = context('repo-intake', 'nonexistentterm', root=self.root)
        self.assertEqual({Path(x['path']).name for x in pack['files']}, {'BRIEF.md','STATE.md'})

    def test_context_search_finds_decision(self):
        pack = context('repo-intake', 'manual review', root=self.root)
        self.assertTrue(any(x['path'].endswith('DECISIONS.md') for x in pack['files']))

    def test_budget_and_omissions_explicit(self):
        pack = context('repo-intake', budget=1200, root=self.root)
        self.assertLessEqual(pack['content_characters'],1200)
        self.assertTrue(pack['omitted'])

    def test_impossible_budget_is_not_silent(self):
        for size in (1, 999, 64001):
            with self.assertRaises(ValueError):
                context('repo-intake', budget=size, root=self.root)

    def test_big_context_rejected(self):
        (self.root/'lab/repo-intake/STATE.md').write_text('X'*300000)
        with self.assertRaisesRegex(ValueError,'too large'):
            context('repo-intake',root=self.root)

    def test_manifest_rejects_arbitrary_shell(self):
        self.manifest(update=lambda d: d['tasks']['demo'].update(argv=['bash','-c','echo unsafe']))
        with self.assertRaisesRegex(ValueError, 'Python interpreter'):
            project('repo-intake',self.root)

    def test_manifest_rejects_unbounded_timeout(self):
        for value in (0, 121, True, '10'):
            self.manifest(update=lambda d: d['tasks']['demo'].update(timeout=value))
            with self.assertRaises(ValueError):
                project('repo-intake',self.root)

    def test_unknown_task(self):
        with self.assertRaisesRegex(ValueError, 'not declared'):
            run_task('repo-intake','something-else',self.root)

    def test_receipt_success_and_verify(self):
        path, receipt = run_task('repo-intake','demo',self.root)
        self.assertEqual(receipt['status'],'passed')
        self.assertEqual(receipt['attempts'],1)
        self.assertEqual(verify_receipt(path,'repo-intake',self.root)['status'],'matched')

    def test_nonzero_exit_is_not_passed(self):
        self.manifest(update=lambda d: d['tasks']['demo'].update(argv=['{python}','-c','raise SystemExit(3)']))
        path, receipt = run_task('repo-intake','demo',self.root)
        self.assertEqual(receipt['status'],'failed')
        self.assertEqual(receipt['returncode'],3)
        with self.assertRaisesRegex(ValueError,'successful run'):
            verify_receipt(path,'repo-intake',self.root)

    def test_timeout_is_not_retried(self):
        self.manifest(update=lambda d: d['tasks']['demo'].update(argv=['{python}','-c','import time; time.sleep(10)'],timeout=1))
        path, receipt = run_task('repo-intake','demo',self.root)
        self.assertEqual(receipt['status'],'timed-out')
        self.assertEqual(receipt['attempts'],1)
        self.assertLess(receipt['duration_seconds'],5)

    def test_receipt_stale_after_source_edit(self):
        path, _ = run_task('repo-intake','demo',self.root)
        source = self.root/'workbench/urls.py'
        source.write_text(source.read_text()+'\n# changed\n')
        with self.assertRaisesRegex(ValueError,'stale'):
            verify_receipt(path,'repo-intake',self.root)

    def test_receipt_altered_log_detected(self):
        path, _ = run_task('repo-intake','demo',self.root)
        path.with_name('stdout.txt').write_text('forged output')
        with self.assertRaisesRegex(ValueError,'altered'):
            verify_receipt(path,'repo-intake',self.root)

    def test_receipt_other_project_rejected(self):
        path, _ = run_task('repo-intake','demo',self.root)
        with self.assertRaisesRegex(ValueError,'identity mismatch'):
            verify_receipt(path,'reference-audit',self.root)

    def test_task_cannot_mutate_inputs_and_claim_pass(self):
        code = "from pathlib import Path; p=Path('fixtures/input.json'); p.write_text('[]')"
        self.manifest(update=lambda d: d['tasks']['demo'].update(argv=['{python}','-c',code]))
        _, receipt = run_task('repo-intake','demo',self.root)
        self.assertEqual(receipt['returncode'],0)
        self.assertEqual(receipt['status'],'inputs-changed')

    def test_deleted_input_still_leaves_failure_receipt(self):
        code = "from pathlib import Path; Path('fixtures/input.json').unlink()"
        self.manifest(update=lambda d: d['tasks']['demo'].update(argv=['{python}','-c',code]))
        path, receipt = run_task('repo-intake','demo',self.root)
        self.assertTrue(path.is_file())
        self.assertEqual(receipt['status'],'inputs-changed')
        self.assertIsNotNone(receipt['tracking_error'])

    def test_sources_validate(self):
        self.assertEqual(source_check(self.root/'lab/repo-intake/sources.json'),4)

    def test_duplicate_source_id_rejected(self):
        path=self.root/'lab/repo-intake/sources.json'
        items=json.loads(path.read_text())
        items.append(copy.deepcopy(items[0]))
        path.write_text(json.dumps(items))
        with self.assertRaisesRegex(ValueError,'duplicate'):
            source_check(path)

    def test_source_empty_credentials_rejected(self):
        path=self.root/'lab/repo-intake/sources.json'
        items=json.loads(path.read_text())
        items[0]['url']='https://@github.com/a/b'
        path.write_text(json.dumps(items))
        with self.assertRaisesRegex(ValueError,'without credentials'):
            source_check(path)

    def test_bad_source_shapes_rejected(self):
        path=self.root/'lab/repo-intake/sources.json'
        for obj in ([], {}, [7], [{}]):
            path.write_text(json.dumps(obj))
            with self.assertRaises(ValueError):
                source_check(path)

    def test_export_excludes_other_project_and_secrets(self):
        (self.root/'.env').write_text('FAKE_SECRET=do-not-copy')
        dest=self.parent/'export'
        export_project('repo-intake',dest,self.root)
        self.assertEqual(list(catalog(dest)),['repo-intake'])
        self.assertFalse((dest/'lab/reference-audit').exists())
        self.assertFalse((dest/'.env').exists())
        self.assertFalse((dest/'.git').exists())
        self.assertTrue((dest/'docs/procedures/evidence-first.md').is_file())

    def test_export_runs_without_original_pythonpath(self):
        dest=self.parent/'export'
        export_project('reference-audit',dest,self.root)
        env=os.environ.copy()
        env.pop('PYTHONPATH',None)
        env['PYTHONUTF8']='1'
        proc=subprocess.run([sys.executable,'-m','workbench','run','reference-audit','test'],
                            cwd=dest,env=env,capture_output=True,text=True,timeout=30)
        self.assertEqual(proc.returncode,0,proc.stderr+proc.stdout)

    def test_export_will_not_overwrite(self):
        dest=self.parent/'export'
        dest.mkdir()
        with self.assertRaises(ValueError):
            export_project('repo-intake',dest,self.root)

    def test_export_rejects_workspace_child(self):
        with self.assertRaises(ValueError):
            export_project('repo-intake',self.root/'export',self.root)


if __name__=='__main__':
    unittest.main()
