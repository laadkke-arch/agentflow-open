"""Exercise the real pinned SpaceDock MCP, not a mocked agent or model.

Runs only in a disposable Linux container with no external network. The engine
and configure helper come from repairer5812/webjjonku; no MCP server is replaced.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
import time

UPSTREAM = Path('/opt/kc-mcp/scripts')
sys.path.insert(0, str(UPSTREAM))
from configure import configure


class MCP:
    def __init__(self, config: Path, log: Path):
        self.seq = 0
        self.calls = []
        self.messages = queue.Queue(maxsize=100)
        self.log = log.open('w', encoding='utf-8')
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1')
        self.proc = subprocess.Popen(
            ['/usr/local/bin/spacedock', 'serve', '--stdio', '--config', str(config)],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.log,
            text=True, encoding='utf-8', bufsize=1, env=env)
        def consume():
            try:
                for line in self.proc.stdout:
                    if len(line) > 2_000_000:
                        self.messages.put(RuntimeError('oversized MCP response'))
                        return
                    self.messages.put(json.loads(line))
            except Exception as exc:
                self.messages.put(exc)
            finally:
                self.messages.put(None)
        threading.Thread(target=consume, daemon=True).start()
        self.rpc('initialize', {'protocolVersion': '2025-03-26', 'capabilities': {},
                 'clientInfo': {'name': 'agentflow-community-acceptance', 'version': '1'}})
        self.send({'jsonrpc': '2.0', 'method': 'notifications/initialized'})

    def send(self, message):
        self.proc.stdin.write(json.dumps(message) + '\n')
        self.proc.stdin.flush()

    def rpc(self, method, params, timeout=30):
        self.seq += 1
        ident = self.seq
        start = time.monotonic()
        self.send({'jsonrpc': '2.0', 'id': ident, 'method': method, 'params': params})
        while True:
            item = self.messages.get(timeout=max(.01, timeout - (time.monotonic()-start)))
            if item is None or isinstance(item, Exception):
                raise RuntimeError('MCP transport ended unexpectedly')
            if item.get('id') != ident:
                continue
            if 'error' in item:
                raise RuntimeError('MCP protocol error: ' + str(item['error'].get('code')))
            self.calls.append({'method': method, 'tool': params.get('name'),
                               'elapsed_ms': round((time.monotonic()-start)*1000, 2)})
            return item['result']

    def call(self, name, **args):
        result = self.rpc('tools/call', {'name': name, 'arguments': args})
        if result.get('isError'):
            raise AssertionError(name + ': ' + json.dumps(result.get('structuredContent')))
        return result.get('structuredContent', result)

    def denied(self, name, **args):
        result = self.rpc('tools/call', {'name': name, 'arguments': args})
        return result.get('isError') is True

    def close(self):
        if self.proc.poll() is None:
            self.proc.stdin.close()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.terminate()
                try:
                    self.proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    self.proc.kill(); self.proc.wait(timeout=3)
        self.log.close()


def main(fixture: Path, output: Path):
    checks, all_calls = [], []
    def check(name, passed):
        if not passed:
            raise AssertionError(name)
        checks.append(name)
        print('PASS', name, flush=True)
    with tempfile.TemporaryDirectory(prefix='af-real-mcp-') as tmp:
        home = Path(tmp)
        workspace = home / 'projects'
        workspace.mkdir()
        for project in ('repo-intake', 'reference-audit'):
            dest = workspace / project
            result = subprocess.run([sys.executable, '-m', 'workbench', 'export', project, str(dest)],
                cwd=fixture, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'),
                capture_output=True, text=True, timeout=30)
            if result.returncode:
                raise RuntimeError('Project export failed: ' + result.stderr[-1000:])
            for command in (['git','init','-q'], ['git','add','.'],
                ['git','-c','user.name=Integration Test','-c','user.email=integration@example.invalid',
                 'commit','-qm','Disposable source snapshot']):
                subprocess.run(command, cwd=dest, check=True, capture_output=True, timeout=20)
        shared = workspace / 'shared'
        shared.mkdir()
        (shared / 'README.md').write_text('Shared verified procedures only.\n', encoding='utf-8')
        config = configure('http://127.0.0.1:8766', home / 'state', workspace)
        settings = json.loads(config.read_text())
        permissions = ['fs.read','fs.write','command.execute','git.read','workspace.manage','recall.read','recall.write']
        settings['allowed_roots'] = [
            {'id': name, 'name': name, 'path': str(workspace/name),
             'permissions': [p for p in permissions if name != 'shared' or p != 'command.execute']}
            for name in ('repo-intake','reference-audit','shared')]
        config.write_text(json.dumps(settings), encoding='utf-8')
        client = MCP(config, home/'server.log')
        try:
            tools = client.rpc('tools/list', {})['tools']
            names = {t['name'] for t in tools}
            check('real engine exposes workspace/edit/process/recall tools',
                  {'workspace_open','file_edit','exec_command','session_observe','recall_write','recall_search'} <= names)
            output.parent.mkdir(parents=True, exist_ok=True)
            (output.parent/'tool-schemas.json').write_text(json.dumps(tools, indent=2), encoding='utf-8')
            ids = {}
            for name in ('repo-intake','reference-audit','shared'):
                opened = client.call('workspace_open', root_id=name, mode='checkout')
                ids[name] = opened['workspace_id']
            for name in ('repo-intake','reference-audit'):
                wid = ids[name]
                read = client.call('read_file', workspace_id=wid, path='lab/'+name+'/STATE.md')
                check(name+' current state read through MCP', bool(read))
                content = '# Runtime integration\nReviewed source snapshot, not a model-generated completion claim.\n'
                client.call('file_edit', workspace_id=wid, action='write', path='RUNTIME_CHECK.md', content=content)
                check(name+' file write persisted', (workspace/name/'RUNTIME_CHECK.md').read_text() == content)
                changed = client.call('exec_command', workspace_id=wid,
                    command='git status --porcelain', yield_ms=5000, timeout_ms=20000)
                check(name+' change visible in Git', 'RUNTIME_CHECK.md' in json.dumps(changed))
                for task in ('test','demo'):
                    run = client.call('exec_command', workspace_id=wid,
                        command='python3 -m workbench run '+name+' '+task,
                        yield_ms=5000, timeout_ms=30000)
                    deadline = time.monotonic()+30
                    while run.get('exit_code') is None and run.get('session_id') and time.monotonic()<deadline:
                        time.sleep(.1)
                        run = client.call('session_observe', workspace_id=wid,
                            session_id=run['session_id'], max_bytes=10000)
                    check(name+'/'+task+' executed via real MCP', run.get('exit_code') == 0)
                client.call('recall_write', workspace_id=wid, path='handoff.md', mode='create',
                    content='AF-MEMORY-'+name+'\nSource: lab/'+name+'/STATE.md\n')
            for name, other in (('repo-intake','reference-audit'),('reference-audit','repo-intake')):
                found = client.call('recall_search', workspace_id=ids[name], query='AF-MEMORY', max_results=20)
                body = json.dumps(found)
                check(name+' recall separated by root', 'AF-MEMORY-'+name in body and 'AF-MEMORY-'+other not in body)
            client.call('recall_write', workspace_id=ids['shared'], path='lessons.md', mode='create',
                        content='AF-SHARED-PROCEDURE: inspect evidence before recording completion.\n')
            check('shared knowledge has explicit root',
                  'AF-SHARED-PROCEDURE' in json.dumps(client.call('recall_search', workspace_id=ids['shared'], query='AF-SHARED')))
            check('shared knowledge root cannot run commands',
                  client.denied('exec_command', workspace_id=ids['shared'], command='printf nope'))
            check('structured file traversal denied',
                  client.denied('read_file', workspace_id=ids['repo-intake'], path='../reference-audit/RUNTIME_CHECK.md'))
            running = client.call('exec_command', workspace_id=ids['repo-intake'],
                command='python3 -c "import time; time.sleep(1); print(\'AF-SESSION-FINISHED\')"',
                yield_ms=1, timeout_ms=10000)
            check('long command returns a session handle', bool(running.get('session_id')))
            sid = running['session_id']
            for _ in range(100):
                running = client.call('session_observe', workspace_id=ids['repo-intake'], session_id=sid, max_bytes=4096)
                if running.get('exit_code') is not None:
                    break
                time.sleep(.05)
            check('same session completes without re-execution', running.get('exit_code') == 0 and 'AF-SESSION-FINISHED' in json.dumps(running))
            wt = client.call('workspace_open', root_id='repo-intake', mode='worktree', base_ref='HEAD')
            client.call('file_edit', workspace_id=wt['workspace_id'], action='write',
                        path='ISOLATED_TASK.md', content='Temporary worktree change.\n')
            check('managed worktree does not modify source checkout', not (workspace/'repo-intake'/'ISOLATED_TASK.md').exists())
            client.call('workspace_discard', workspace_id=wt['workspace_id'], force=True)
            all_calls.extend(client.calls)
        finally:
            client.close()
        client = MCP(config, home/'server-restarted.log')
        try:
            for name in ('repo-intake','reference-audit'):
                wid = client.call('workspace_open', root_id=name, mode='checkout')['workspace_id']
                memo = client.call('recall_read', workspace_id=wid, path='handoff.md')
                check(name+' recall survives actual server restart', 'AF-MEMORY-'+name in json.dumps(memo))
                check(name+' edited file survives restart',
                      'Reviewed source snapshot' in json.dumps(client.call('read_file', workspace_id=wid, path='RUNTIME_CHECK.md')))
            all_calls.extend(client.calls)
        finally:
            client.close()
    receipt = {'schema':1, 'status':'passed', 'engine':'SpaceDock 0.1.6 via pinned WebJjonku',
        'passed':checks, 'mcp_calls':all_calls,
        'transport':'real local stdio MCP; upstream separate test covers HTTP OAuth',
        'external_network_during_test':False, 'chatgpt_connection_tested':False,
        'user_pc_modified':False, 'automatic_model_loop':False,
        'boundary':'Trusted commands share one container OS user; per-root recall is logical separation, not hostile-tenant isolation.'}
    output.write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    print('PROJECT_MCP_RESULT='+json.dumps({'status':'passed','checks':len(checks),'calls':len(all_calls)}))

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--fixture',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    main(args.fixture.resolve(),args.output.resolve())
