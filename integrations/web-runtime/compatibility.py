"""Verify the workbench's actual Python contract and Git persistence over MCP."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from exercise import MCP, configure


def main(fixture, output):
    checks=[]
    def check(label, value):
        if not value: raise AssertionError(label)
        checks.append(label)
        print('PASS',label,flush=True)
    with tempfile.TemporaryDirectory(prefix='af-compatibility-') as temp:
        root=Path(temp)
        projects=root/'projects'
        projects.mkdir()
        checkout=projects/'agentflow-open'
        subprocess.run([sys.executable,'-m','workbench','export','repo-intake',str(checkout)],
            cwd=fixture,check=True,capture_output=True,text=True,timeout=30)
        for args in (['git','init','-q'],['git','add','.'],
            ['git','-c','user.name=Runtime Test','-c','user.email=runtime@example.invalid','commit','-qm','Fixture']):
            subprocess.run(args,cwd=checkout,check=True,capture_output=True,timeout=20)
        config=configure('http://127.0.0.1:8766',root/'state',projects)
        client=MCP(config,root/'server.log')
        try:
            wid=client.call('workspace_open',root_id='agentflow-open',mode='checkout')['workspace_id']
            def command(text):
                result=client.call('exec_command',workspace_id=wid,command=text,yield_ms=5000,timeout_ms=30000)
                for _ in range(100):
                    if result.get('exit_code') is not None: break
                    time.sleep(.1)
                    result=client.call('session_observe',workspace_id=wid,session_id=result['session_id'],max_bytes=20000)
                if result.get('exit_code') != 0:
                    raise AssertionError('MCP command failed: '+json.dumps(result))
                return result
            check('Python runtime satisfies real workbench doctor',command('python3 -m workbench doctor').get('exit_code')==0)
            client.call('file_edit',workspace_id=wid,action='write',path='MCP_GIT_RECORD.md',
                content='# Runtime verification\nAF-GIT-PERSISTENCE: verified disposable fixture, no remote push.\n')
            check('existing tests pass after MCP write',command('python3 -m workbench run repo-intake test').get('exit_code')==0)
            command("git add -- MCP_GIT_RECORD.md && git -c user.name='Runtime Test' -c user.email='runtime@example.invalid' commit -m 'Record verified MCP change'")
            check('MCP write committed as real Git object','AF-GIT-PERSISTENCE' in json.dumps(command('git show HEAD:MCP_GIT_RECORD.md')))
            commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=checkout,text=True,timeout=5).strip()
        finally: client.close()
        restored=root/'restored'
        subprocess.run(['git','clone','--no-hardlinks',str(checkout),str(restored)],check=True,capture_output=True,timeout=20)
        check('new checkout contains committed MCP file','AF-GIT-PERSISTENCE' in (restored/'MCP_GIT_RECORD.md').read_text())
        result=subprocess.run([sys.executable,'-m','workbench','doctor'],cwd=restored,capture_output=True,text=True,timeout=15)
        check('new checkout satisfies Python contract',result.returncode==0)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps({'status':'passed','passed':checks,'python':sys.version.split()[0],
        'fixture_commit':commit,'remote_push_tested':False,'personal_credentials_used':False},indent=2),encoding='utf-8')
    print('COMPATIBILITY_RESULT='+json.dumps({'status':'passed','checks':len(checks),'python':sys.version.split()[0]}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--fixture',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();main(a.fixture.resolve(),a.output.resolve())
