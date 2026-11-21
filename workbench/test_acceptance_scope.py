"""New project registration must not enlarge the acceptance execution scope."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from workbench.cli import ROOT


class AcceptanceScopeTests(unittest.TestCase):
    def test_registered_third_project_is_not_implicitly_executed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'workspace'
            root.mkdir()
            for folder in ('workbench', 'lab', 'docs', 'scripts'):
                shutil.copytree(ROOT / folder, root / folder,
                                ignore=shutil.ignore_patterns('__pycache__'))
            third = root / 'lab' / 'third-project'
            shutil.copytree(root / 'lab' / 'repo-intake', third)
            manifest_path = third / 'project.json'
            manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
            manifest['id'] = 'third-project'
            for spec in manifest['tasks'].values():
                spec['argv'] = ['{python}', '-c', "raise RuntimeError('must not run without selection')"]
            manifest_path.write_text(json.dumps(manifest), encoding='utf-8')
            catalog_path = root / 'workbench' / 'catalog.json'
            entries = json.loads(catalog_path.read_text(encoding='utf-8'))
            entries['projects']['third-project'] = 'lab/third-project'
            catalog_path.write_text(json.dumps(entries), encoding='utf-8')
            env = os.environ.copy()
            env.pop('PYTHONPATH', None)
            env.update(PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
            proc = subprocess.run([sys.executable, 'scripts/acceptance.py'], cwd=root,
                                  env=env, capture_output=True, text=True,
                                  encoding='utf-8', timeout=60)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            result = json.loads((root / '.workbench/acceptance.json').read_text(encoding='utf-8'))
            self.assertEqual(set(result['projects']), {'repo-intake', 'reference-audit'})
            self.assertFalse((root / '.workbench/runs/third-project').exists())


if __name__ == '__main__':
    unittest.main()
