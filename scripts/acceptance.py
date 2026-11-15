"""Exercise the workbench in fresh processes and separate exported workspaces."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from workbench.cli import (catalog, context, digest, export_project, git_state,
                           run_task, source_check, verify_receipt)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def command(argv, cwd, timeout=60):
    env = os.environ.copy()
    env.pop('PYTHONPATH', None)
    env.update(PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
    proc = subprocess.run(argv, cwd=cwd, capture_output=True, text=True,
                          encoding='utf-8', timeout=timeout, env=env)
    if proc.returncode:
        raise RuntimeError(f'command failed ({proc.returncode}): {argv}\n{proc.stdout}\n{proc.stderr}')
    return proc.stdout


def execute(require_git=False):
    out = ROOT / '.workbench'
    out.mkdir(exist_ok=True)
    result = {'schema':1, 'scope':'workbench acceptance, not discovery product',
              'source':git_state(ROOT), 'python':sys.version.split()[0],
              'projects':{}, 'exports':{}, 'new_model_session_tested':False}
    markers = {'repo-intake':'INTAKE_ONLY_4C21', 'reference-audit':'AUDIT_ONLY_9E52'}
    for name in catalog():
        source_count = source_check(ROOT / catalog()[name] / 'sources.json')
        runs = []
        for task in ('test', 'demo'):
            path, receipt = run_task(name, task)
            print(f'=== {name}/{task} stdout ===', flush=True)
            print(path.with_name('stdout.txt').read_text(encoding='utf-8', errors='replace'), flush=True)
            print(f'=== {name}/{task} stderr ===', flush=True)
            print(path.with_name('stderr.txt').read_text(encoding='utf-8', errors='replace'), flush=True)
            require(receipt['status']=='passed', f'{name}/{task} failed: {path}')
            verify_receipt(path,name)
            runs.append({'task':task, 'receipt':path.relative_to(ROOT).as_posix(),
                         'id':receipt['id'], 'status':receipt['status']})
        # Fresh OS process without chat state or inherited PYTHONPATH.
        raw = command([sys.executable,'-m','workbench','context',name,'--query','contract'],ROOT)
        pack = json.loads(raw)
        require(markers[name] in raw, 'own project marker missing')
        for other, marker in markers.items():
            require(other==name or marker not in raw, 'cross-project context leak')
        (out / f'context-{name}.json').write_text(raw,encoding='utf-8')
        result['projects'][name] = {'runs':runs, 'source_records':source_count,
                                    'context_files':[x['path'] for x in pack['files']],
                                    'context_process':'fresh process, not a fresh AI session'}
    # A second project reuses the shared module, but cannot see the first project's files.
    with tempfile.TemporaryDirectory(prefix='workbench-reuse-') as temp:
        for name in catalog():
            target = Path(temp)/name
            export_project(name,target)
            require(list(catalog(target))==[name], 'export catalog mixed projects')
            other = 'reference-audit' if name=='repo-intake' else 'repo-intake'
            require(not (target/'lab'/other).exists(), 'other project included in export')
            output = command([sys.executable,'-m','workbench','run',name,'test'],target)
            exported_run = json.loads(output)
            require(exported_run['status']=='passed','exported task failed')
            require(digest(target/'workbench/urls.py')==digest(ROOT/'workbench/urls.py'),'shared helper drifted')
            result['exports'][name] = {'status':'passed','other_project_absent':True,
                                      'shared_helper_sha256':digest(target/'workbench/urls.py')}
    source = git_state(ROOT)
    if source['commit']:
        bundle = out/'source.bundle'
        if bundle.exists():
            bundle.unlink()
        command(['git','bundle','create',str(bundle),'--all','HEAD'],ROOT)
        command(['git','bundle','verify',str(bundle)],ROOT)
        with tempfile.TemporaryDirectory(prefix='workbench-restore-') as temp:
            restored = Path(temp)/'restored'
            command(['git','clone','--quiet','--no-checkout',str(bundle),str(restored)],ROOT)
            command(['git','checkout','--quiet','--detach',source['commit']],restored)
            require(git_state(restored)['commit']==source['commit'],'restored commit mismatch')
            output = command([sys.executable,'-m','workbench','run','repo-intake','demo'],restored)
            require(json.loads(output)['status']=='passed','restored demo failed')
        result['backup']={'status':'passed','commit':source['commit'],'sha256':digest(bundle),
                          'scope':'Git objects and refs only; not issues, secrets, DB, LFS or untracked files'}
    else:
        require(not require_git,'Git checkout is required for CI backup acceptance')
        result['backup']={'status':'not-executed','reason':'local staging is not a Git clone'}
    result['status']='passed'
    (out/'acceptance.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('WORKBENCH_ACCEPTANCE='+json.dumps(result,sort_keys=True))
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--require-git',action='store_true')
    args=p.parse_args()
    execute(args.require_git)
