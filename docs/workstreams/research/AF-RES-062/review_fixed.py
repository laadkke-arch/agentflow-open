"""Reopen RESULT and acceptance ledger from immutable Git objects."""
import argparse
import hashlib
import json
from pathlib import Path
import posixpath
import re
import subprocess
from datetime import datetime, timezone

BASE=Path(__file__).resolve().parent
REPO=BASE.parents[3]
OWNED=BASE.relative_to(REPO).as_posix()


def main():
    p=argparse.ArgumentParser();p.add_argument('--sha',required=True)
    p.add_argument('--write',action='store_true');p.add_argument('--verify-receipts',action='store_true');a=p.parse_args()
    sha=subprocess.check_output(['git','rev-parse',a.sha+'^{commit}'],cwd=REPO,text=True).strip()
    def blob(name):return subprocess.check_output(['git','show',sha+':'+OWNED+'/'+name],cwd=REPO)
    def exists(name):return subprocess.run(['git','cat-file','-e',sha+':'+posixpath.normpath(OWNED+'/'+name)],cwd=REPO,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0
    rb=blob('RESULT.md');ab=blob('evidence/acceptance-evidence.json');result=rb.decode();ledger=json.loads(ab)
    stats=json.loads(blob('evidence/source-counts.json'));agg=json.loads(blob('streams/supplement/aslett-aggregates.json'))
    broken=[];links=[]
    for href in re.findall(r'(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)',result):
        if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:',href) or href.startswith('#'):continue
        name=href.split('#')[0];links.append(name)
        if not exists(name):broken.append(name)
    evidence=[]
    for c in ledger['criteria']:
        for e in c['evidence']:
            evidence.append(e['path'])
            if not exists(e['path']):broken.append(e['path'])
    if a.verify_receipts:
        for k,v in ledger['technical_execution'].items():
            if isinstance(v,str) and v.startswith('evidence/'):
                evidence.append(v)
                if not exists(v):broken.append(v)
    numeric=[]
    for i in range(0,len(agg['groups']),2):
        c,t=agg['groups'][i:i+2]
        token=f"{c['acceptance_n']}/{c['acceptance_N']}→{t['acceptance_n']}/{t['acceptance_N']}"
        numeric.append(dict(cohort=c['cohort'],sample=c['sample'],truth=c['truth_key'],token=token,present=token in result))
    n=next(c for c in ledger['criteria'] if c['criterion_id']=='C05')['actual']['numerator']
    checks=dict(no_broken_local_links=not broken,all_six_count_contrasts_present=all(r['present'] for r in numeric),
        source_count_matches=n==stats['minimum_distinct_primary_works']==47,
        partial_status_preserved=ledger['status']=='PARTIAL_HANDOFF',
        result_matches_worktree=rb==(BASE/'RESULT.md').read_bytes(),
        acceptance_matches_worktree=ab==(BASE/'evidence/acceptance-evidence.json').read_bytes())
    lines=result.splitlines();table_lines=[i+1 for i,s in enumerate(lines) if s.startswith('| 연구·표본층 |') or s.startswith('| 코호트·조건·비교 |')]
    out=dict(reviewed_utc=datetime.now(timezone.utc).isoformat(),actor='root AI, immutable git show/cat-file reread',
        command=f'python -B {OWNED}/review_fixed.py --sha {sha}'+(' --verify-receipts' if a.verify_receipts else ''),
        fixed_commit=sha,status='PASS' if all(checks.values()) else 'FAIL',checks=checks,
        result_sha256=hashlib.sha256(rb).hexdigest(),acceptance_sha256=hashlib.sha256(ab).hexdigest(),
        required_table_start_lines=table_lines,local_result_links_checked=len(links),acceptance_evidence_paths_checked=len(evidence),
        broken_paths=broken,numeric_contrasts=numeric,
        receipt_reference_scope='Alltechnicalreceiptpaths checked atthiscommit' if a.verify_receipts else 'Scientific ledger paths and RESULT links checked; new verification receipts are sealed in the next commit and checked again before HANDOFF.')
    if a.write:(BASE/'evidence/fixed-result-review.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(out,ensure_ascii=False,indent=2))
    raise SystemExit(0 if out['status']=='PASS' else 1)


if __name__=='__main__':main()
