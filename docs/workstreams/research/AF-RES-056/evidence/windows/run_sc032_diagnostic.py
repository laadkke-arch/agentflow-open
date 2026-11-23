"""Compile and run only the out-of-budget, research-authored C2 diagnostic.

Inputs are preexisting checkouts: evidence/transient/sc032-build at PIN and
evidence/transient/nlohmann-json at v3.12.0. No package installation or network
fetch is performed by this command. It never edits main retrieval judgments.
"""
from pathlib import Path
import datetime, hashlib, json, subprocess, shutil

HERE=Path(__file__).resolve().parent
TASK=HERE.parents[1]
PROVIDER=TASK/'evidence/transient/sc032-build'
DEPENDENCY=TASK/'evidence/transient/nlohmann-json'
PIN='d5199551f758ba067612979ae32ec35693640ccf'
DEPENDENCY_PIN='55f93686c01528224f448c19128836e7df245f72'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def git(repo,*args):return subprocess.check_output(['git',*args],cwd=repo,text=True).strip()
assert git(PROVIDER,'rev-parse','HEAD')==PIN
assert git(DEPENDENCY,'describe','--tags','--exact-match')=='v3.12.0'
assert git(DEPENDENCY,'rev-parse','HEAD')==DEPENDENCY_PIN
compiler=shutil.which('g++')
assert compiler, 'g++ is required'
exe=TASK/'evidence/transient/sc032-diagnostic'
cmd=[compiler,'-std=c++11','-O0','-I'+str(PROVIDER/'src'),'-I'+str(DEPENDENCY/'single_include'),str(HERE/'schema_fixture.cpp'),*[str(x) for x in sorted((PROVIDER/'src').glob('*.cpp'))],'-o',str(exe)]
r={'started_utc':utc(),'classification':'out-of-budget diagnostic; not the user original program; not main L/V success','provider_sha':PIN,'provider_build_version':'2.4.1 (CMakeLists.txt declaration; not inferred release tag)','dependency_tag':'v3.12.0','dependency_sha':git(DEPENDENCY,'rev-parse','HEAD'),'compiler':subprocess.check_output([compiler,'--version'],text=True).splitlines()[0],'fixture_sha256':hashlib.sha256((HERE/'schema_fixture.cpp').read_bytes()).hexdigest(),'build_command':cmd}
build=subprocess.run(cmd,capture_output=True,text=True,timeout=240)
r.update(build_exit_code=build.returncode,build_stdout=build.stdout,build_stderr=build.stderr)
if build.returncode==0:
 run=subprocess.run([str(exe)],capture_output=True,text=True,timeout=30)
 r.update(run_exit_code=run.returncode,run_stdout=run.stdout,run_stderr=run.stderr)
 if run.returncode==0:r['cases']=json.loads(run.stdout)
else:r['run_status']='미실시: compilation failed'
r['finished_utc']=utc()
(HERE/'sc032-execution.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k not in ['build_stdout','build_stderr','run_stdout','run_stderr','build_command']},ensure_ascii=False))
if build.returncode:print(build.stderr)
raise SystemExit(build.returncode or r.get('run_exit_code',1))
