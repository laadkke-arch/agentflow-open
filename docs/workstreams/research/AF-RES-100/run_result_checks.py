"""Run unchanged repository checks on an explicit committed result in an owned worktree.

The common checker writes .workbench logs. Keeping its complete detached checkout
under the owned ignored cache confines those outputs without modifying the checker.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,os,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[4]
OWNED=Path(__file__).resolve().parent
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--target',required=True);ap.add_argument('--receipt',default='evidence/result-checks.json');a=ap.parse_args()
    assert re.fullmatch('[0-9a-f]{40}',a.target),'full committed SHA required'
    receipt=(OWNED/a.receipt).resolve();assert receipt.is_relative_to(OWNED)
    actual=subprocess.check_output(['git','rev-parse',a.target+'^{commit}'],cwd=ROOT,text=True).strip();assert actual==a.target
    area=OWNED/'evidence/_cache';area.mkdir(parents=True,exist_ok=True)
    checkout=area/('verification-'+a.target[:12]);tmp=area/'check-tmp';tmp.mkdir(exist_ok=True)
    setup=None
    if not checkout.exists():
        setup=subprocess.run(['git','worktree','add','--detach',str(checkout),a.target],cwd=ROOT,capture_output=True,text=True)
        if setup.returncode:raise RuntimeError(setup.stderr)
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=checkout,text=True).strip()==a.target
    assert not subprocess.check_output(['git','status','--porcelain'],cwd=checkout,text=True).strip(),'verification checkout is not clean'
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';env['TMPDIR']=str(tmp)
    commands=[('workstream check --fetch',[sys.executable,'-B','-m','workbench.session','check','docs/workstreams/research/AF-RES-100/manifest.json','--fetch']),
              ('common cloud_check',[sys.executable,'-B','scripts/cloud_check.py','--environment','codex-cloud','--fetch-contract','--require-clean'])]
    result={'started_utc':now(),'target_sha':a.target,'verification_checkout':str(checkout),'checkout_mode':'detached committed result; unmodified common checker; all generated logs under owned_path',
            'setup':{'command':['git','worktree','add','--detach',str(checkout),a.target],'exit_code':setup.returncode,'stdout':setup.stdout,'stderr':setup.stderr} if setup else {'reused_clean_same_commit':True},
            'commands':[],'scope':'Actual repository ownership/contract and common workbench gates; not original user requests or upstream jq/Pandoc/R suites.'}
    for label,cmd in commands:
        print('Starting '+label+' on '+a.target,flush=True);start=now()
        r=subprocess.run(cmd,cwd=checkout,env=env,capture_output=True,text=True,timeout=900)
        row={'label':label,'command':cmd,'cwd':str(checkout),'target_sha':a.target,'started_utc':start,'completed_utc':now(),'exit_code':r.returncode,
             'stdout':r.stdout,'stderr':r.stderr,'stdout_sha256':hashlib.sha256(r.stdout.encode()).hexdigest()}
        if label.startswith('workstream'):
            try:row['result']=json.loads(r.stdout)
            except ValueError:row['result']={'parse':'not-json'}
            row['scope']='af-res-100 manifest, fetched integration/dependency pins, ancestry, conflict and owned-path checks; original research execution excluded'
        else:
            cr=checkout/'.workbench/cloud-check.json'
            if cr.exists():
                row['common_receipt']=json.loads(cr.read_text())
                row['session_validation']=row['common_receipt'].get('session_validation')
                gates=[x['name']+':'+str(x.get('exit_code')) for x in row['common_receipt'].get('checks',[])]
                row['scope']='Common gates '+', '.join(gates)+'; individual-session result '+json.dumps(row['session_validation'],ensure_ascii=False)
            else:row['scope']='common receipt missing; inspect stdout/stderr'
        result['commands'].append(row)
        print(label+' exit '+str(r.returncode),flush=True)
    result['completed_utc']=now();result['all_exit_zero']=all(r['exit_code']==0 for r in result['commands'])
    result['ending_head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=checkout,text=True).strip()
    result['ending_clean']=not subprocess.check_output(['git','status','--porcelain'],cwd=checkout,text=True).strip()
    receipt.parent.mkdir(parents=True,exist_ok=True);receipt.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'receipt':str(receipt),'target_sha':a.target,'all_exit_zero':result['all_exit_zero'],'ending_clean':result['ending_clean']},ensure_ascii=False),flush=True)
    raise SystemExit(0 if result['all_exit_zero'] and result['ending_head']==a.target and result['ending_clean'] else 1)
if __name__=='__main__':main()
