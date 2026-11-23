"""Reproduce the 13 logged executions using only committed small fixtures.

Requires prepare_runtime.py. Writes separate reproduction results; does not
modify frozen route files or the original runtime-results.json.
"""
import datetime,hashlib,json,pathlib,subprocess
P=pathlib.Path(__file__).resolve().parents[2];O=P/'evidence/post-jq';B=(O/'_cache/jq-linux-amd64').resolve()
assert hashlib.sha256(B.read_bytes()).hexdigest()=='5942c9b0934e510ee61eb3e30273f1b3fe2590df93933a93d7c58b81d19c8ff5'
original=json.loads((O/'runtime-results.json').read_text());fixtures={x['id']:x for x in json.loads((O/'validation-inputs.json').read_text())};result=[]
for row in original:
 f=P/row['filter_file'];i=P/row['input_file'];assert hashlib.sha256(f.read_bytes()).hexdigest()==row['filter_sha256'];assert hashlib.sha256(i.read_bytes()).hexdigest()==row['input_sha256']
 flags=['-R','-r'] if row['case_id']=='J4' else ['-r'] if row['case_id']=='J1' else ['-c']
 command=[str(B),*flags,'-f',str(f.resolve())];r=subprocess.run(command,input=i.read_bytes(),capture_output=True,timeout=20)
 result.append({'case_id':row['case_id'],'fixture_id':row['fixture_id'],'filter_route':row['filter_route'],'command_argv':command,'stdin_file':row['input_file'],'executed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode(),'matches_logged_observation':r.returncode==row['exit_code'] and r.stdout.decode()==row['stdout'] and r.stderr.decode()==row['stderr'],'expected_stdout':fixtures[row['fixture_id']]['expected_stdout'],'out_of_R0_scope':row.get('out_of_R0_scope',False)})
(O/'reproduction-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'runs':len(result),'same_as_recorded':sum(x['matches_logged_observation'] for x in result),'output':'evidence/post-jq/reproduction-results.json'},ensure_ascii=False))
raise SystemExit(0 if all(x['matches_logged_observation'] for x in result) else 1)
