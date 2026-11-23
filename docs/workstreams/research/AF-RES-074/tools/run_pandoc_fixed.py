#!/usr/bin/env python3
"""Execute pinned official fixture commands with a supplied Pandoc2.11.3.2 binary."""
import argparse,datetime,hashlib,json,shlex,subprocess
from pathlib import Path
P=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--binary',required=True);ap.add_argument('--output',default='evidence/pandoc-fixed-run.json');a=ap.parse_args()
binary=Path(a.binary).resolve()
vr=subprocess.run([str(binary),'--version'],capture_output=True,text=True,timeout=30)
assert vr.returncode==0 and '2.11.3.2' in vr.stdout.splitlines()[0],vr.stdout
fixture=json.loads((P/'evidence/pandoc-fixed-fixtures.json').read_text())
result={'actor':'root model in supplied cloud shell','version_stdout':vr.stdout,'binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'source_pin':fixture['pin'],'layer':'researcher execution of official tagged fixtures on historical release; after exposure, not preregistered or public CI receipt','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tests':[]}
for t in fixture['tests']:
    stages=[]; stage=[]
    for word in shlex.split(t['command']):
        if word=='|':stages.append(stage);stage=[]
        else:stage.append(word)
    stages.append(stage)
    data=t['input'].encode();calls=[]
    for stage in stages:
        assert stage[0]=='pandoc' and all(w not in (';','&&','||') for w in stage)
        argv=[str(binary)]+stage[1:]
        r=subprocess.run(argv,input=data,capture_output=True,timeout=30)
        calls.append({'argv':argv,'input_sha256':hashlib.sha256(data).hexdigest(),'exit_code':r.returncode,'stderr':r.stderr.decode(errors='replace'),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest()})
        assert r.returncode==0,(t['test_id'],calls[-1])
        data=r.stdout
    actual=data.decode();expected=t['expected_stdout']
    result['tests'].append({'test_id':t['test_id'],'source_url':t['source_url'],'command':t['command'],'stdin_sha256':t['stdin_sha256'],'expected_stdout':expected,'actual_stdout':actual,'actual_stdout_sha256':hashlib.sha256(data).hexdigest(),'expected_stdout_sha256':hashlib.sha256(expected.encode()).hexdigest(),'exact_stdout_match':actual==expected,'calls':calls,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
result['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
result['test_count']=len(result['tests']);result['process_invocations']=sum(len(t['calls']) for t in result['tests']);result['all_exit_zero']=True;result['all_stdout_exact']=all(t['exact_stdout_match'] for t in result['tests'])
output=(P/a.output).resolve();assert output.is_relative_to(P),'Output must stay in owned path'
output.parent.mkdir(parents=True,exist_ok=True)
output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['test_count','process_invocations','all_exit_zero','all_stdout_exact']},indent=2))
for t in result['tests']:
    if not t['exact_stdout_match']:print(t['test_id'],'actual',repr(t['actual_stdout']),'expected',repr(t['expected_stdout']))
