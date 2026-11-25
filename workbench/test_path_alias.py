"""Regression for resolved files versus an aliased workspace root."""
from pathlib import Path
import shutil
import tempfile
import unittest

from workbench.cli import ROOT, context, export_project, run_task, verify_receipt


class WorkspaceAliasTests(unittest.TestCase):
    def test_workspace_alias_uses_one_canonical_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            root = parent / 'workspace'
            root.mkdir()
            for folder in ('workbench', 'lab', 'docs'):
                shutil.copytree(ROOT / folder, root / folder,
                                ignore=shutil.ignore_patterns('__pycache__'))
            alias = parent / 'workspace-alias'
            try:
                alias.symlink_to(root.resolve(), target_is_directory=True)
            except OSError:
                self.skipTest('directory symlink creation is unavailable on this host')
            pack = context('repo-intake', root=alias)
            self.assertTrue(pack['files'])
            path, receipt = run_task('repo-intake', 'demo', alias)
            self.assertEqual(receipt['status'], 'passed')
            alias_receipt = alias / path.relative_to(root.resolve())
            self.assertEqual(verify_receipt(alias_receipt, 'repo-intake', alias)['status'], 'matched')
            export_project('repo-intake', parent / 'alias-export', alias)
            self.assertTrue((parent / 'alias-export' / 'EXPORT.json').is_file())


if __name__ == '__main__':
    unittest.main()
