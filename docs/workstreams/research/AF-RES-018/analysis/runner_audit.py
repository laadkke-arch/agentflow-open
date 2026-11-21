#!/usr/bin/env python3
"""Read-only checks on real runs and parent-side discovery freeze receipts.

No retrieval or candidate generation is simulated. Parent invokes --freeze after
an executor has finished its discovery answer and before revealing check names.
"""
from pathlib import Path
import argparse, datetime, hashlib, json
from common import document_counts

ROOT = Path(__file__).resolve().parents[1]

def digest(obj):
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()

def receipt(run):
    return {
        'case_id': run['case_id'], 'condition': run['baseline'],
        'raw_response_sha256': hashlib.sha256(run['raw_response'].encode()).hexdigest(),
        'candidates_sha256': digest(run['candidates']),
        'query_prefix_sha256': digest(run['queries']),
        'document_prefix_sha256': digest(run['opened_documents']),
        'query_prefix_count': len(run['queries']),
        'document_prefix_count': len(run['opened_documents']),
        'stage1_frozen_at_utc': run.get('stage1_frozen_at_utc'),
        'receipt_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }

def audit(path, frozen=None):
    path=path.resolve();errors=[];warnings=[]
    try: r=json.loads(path.read_text())
    except Exception as e:return {'path':str(path.relative_to(ROOT)), 'errors':[str(e)]}
    for k in ['case_id','baseline','raw_response','candidates','queries','opened_documents',
              'started_at_utc','ended_at_utc','gold_seen','other_runs_seen','budget']:
        if k not in r:errors.append('missing '+k)
    if errors:return {'path':str(path.relative_to(ROOT)), 'errors':errors}
    if r['gold_seen'] is not False or r['other_runs_seen'] is not False:
        errors.append('reported contamination')
    if r['case_id']!=path.stem or r['baseline']!=path.parent.name:
        errors.append('assigned path/identity mismatch')
    counts={'search_queries':len(r['queries']),'opened_pages':len(r['opened_documents']),
            'candidate_count':len(r['candidates'])}
    for k,limit in [('search_queries',12),('candidate_count',10)]:
        if counts[k]>limit:errors.append(f'{k} {counts[k]} > {limit}')
        if r['budget'].get(k)!=counts[k]:errors.append('budget mismatch '+k)
    declared=r['budget'].get('opened_pages');normal=document_counts(r['opened_documents'])['normalized_document_budget']
    if not isinstance(declared,int) or not normal<=declared<=counts['opened_pages']:
        errors.append(f'opened budget inconsistent with logged attempts: normalized={normal}, declared={declared}, events={counts["opened_pages"]}')
    elif declared>20 or normal>20:errors.append(f'opened budget exceeds20: normalized={normal}, declared={declared}')
    elif declared!=counts['opened_pages']:warnings.append('declared opens exclude some recorded rereads/finds; normalized cost verified')
    counts['normalized_document_budget']=normal
    ranks=[c.get('rank') for c in r['candidates']]
    if ranks!=list(range(1,len(ranks)+1)):errors.append('rank sequence')
    for i,q in enumerate(r['queries']):
        if not q.get('q') or not q.get('at_utc'):errors.append(f'query {i} lacks literal/time')
    for i,d in enumerate(r['opened_documents']):
        if not d.get('url') or not d.get('at_utc'):errors.append(f'document {i} lacks URL/time')
        if d.get('date_status') not in ['pre_decision','post_decision','unknown']:
            if str(d.get('date_status','')).startswith('mixed') and isinstance(d.get('post_decision'),bool):
                warnings.append(f'document {i} mixed date text retained; post_decision boolean governs conservative temporal analysis')
            elif 'unknown' in str(d.get('date_status','')).lower() and d.get('post_decision') in [True,False,None]:
                warnings.append(f'document {i} descriptive date uncertainty retained; treated as unknown unless explicitly post_decision')
            else:errors.append(f'document {i} date_status')
    for k in ['started_at_utc','ended_at_utc']:
        value=r[k]
        if k=='ended_at_utc' and value is None and not r.get('checks'):
            value=r.get('stage1_frozen_at_utc')
        try:
            if value.endswith(' UTC'):datetime.datetime.strptime(value,'%Y-%m-%d %H:%M:%S UTC')
            else:datetime.datetime.fromisoformat(value.replace('Z','+00:00'))
        except Exception:errors.append('bad datetime '+k)
    if frozen:
        if hashlib.sha256(r['raw_response'].encode()).hexdigest()!=frozen['raw_response_sha256']:
            errors.append('discovery raw response changed after freeze')
        if digest(r['candidates'])!=frozen['candidates_sha256']:
            errors.append('discovery candidates changed after freeze')
        if digest(r['queries'][:frozen['query_prefix_count']])!=frozen['query_prefix_sha256']:
            errors.append('discovery queries changed after freeze')
        if digest(r['opened_documents'][:frozen['document_prefix_count']])!=frozen['document_prefix_sha256']:
            errors.append('discovery document log changed after freeze')
        checks=r.get('checks',[])
        if len(checks)!=3:errors.append('not exactly three checks')
        for c in checks:
            decision=c.get('decision',c.get('verdict'))
            if decision not in ['keep','exclude']:errors.append('invalid check decision')
            elif 'decision' not in c:warnings.append('check uses verdict as field alias for keep/exclude; raw record retained')
            if not c.get('reason'):errors.append('check without reason')
    return {'path':str(path.relative_to(ROOT)), 'errors':errors, 'warnings':warnings, 'counts':counts,
            'execution_status':r.get('execution_status'), 'checks':len(r.get('checks',[]))}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--freeze',nargs=2,metavar=('CONDITION','QID'))
    p.add_argument('--audit',action='store_true');a=p.parse_args()
    if a.freeze:
        cond,qid=a.freeze; path=ROOT/'runs'/cond/(qid+'.json');r=json.loads(path.read_text())
        out=ROOT/'runs'/'freeze'/f'{cond}-{qid}.json';out.parent.mkdir(parents=True,exist_ok=True)
        if out.exists():raise SystemExit('receipt already exists; refusing to rewrite')
        if r.get('checks'):raise SystemExit('checks already present; cannot assert pre-injection freeze')
        errors=audit(path)['errors']
        if errors:raise SystemExit(json.dumps(errors))
        out.write_text(json.dumps(receipt(r),ensure_ascii=False,indent=2)+'\n')
        print(str(out.relative_to(ROOT)))
    elif a.audit:
        result=[]
        for cond in ['A','P']:
            for path in sorted((ROOT/'runs'/cond).glob('*.json')):
                f=ROOT/'runs'/'freeze'/f'{cond}-{path.stem}.json'
                result.append(audit(path,json.loads(f.read_text()) if f.exists() else None))
        print(json.dumps(result,ensure_ascii=False,indent=2))
        raise SystemExit(any(r['errors'] for r in result))
