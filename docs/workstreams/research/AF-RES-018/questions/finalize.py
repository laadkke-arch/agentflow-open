#!/usr/bin/env python3
"""Freeze non-identifying inputs and seeded dispatch; never write source bodies."""
from pathlib import Path
import argparse, concurrent.futures, hashlib, json, random, collections
from generate import text_of, request_json, now

ROOT=Path(__file__).resolve().parents[1]
COMMON=('Read only this question and your assigned condition rules. Do not read metadata, gold, '
        'other questions, other runs, repository history, or source-thread answers. The original '
        'command fetches the fixed question only and verifies its hash; this input retrieval is '
        'outside the search budget. User caps override A legacy15: at most10 candidates,12 literal '
        'search queries,20 opened-document attempts INCLUDING later checks. Failed opens count. '
        'A uses RULES_A A section only. Both conditions must attempt one unauthenticated public '
        'code-search surface; count its query and open. Exclude the question thread, its copies and '
        'pages citing it; log even snippet exposures. Use independent primary sources. Write the '
        'complete discovery answer in English in raw_response and English candidate reasons; '
        'do not shorten the raw answer to the later30-word judging format. Save actual UTC times, '
        'literal queries, actually opened URLs, evidence and publication/date status. After '
        'discovery save candidates and raw_response, stage1_frozen_at_utc, stage1 budget counts; '
        'leave checks empty and tell parent discovery is frozen. Parent will reveal3 unlabeled '
        'checks; use only remaining same budget and do not edit discovery answer/candidates/log '
        'prefixes. Record checks_started_at_utc/checks_ended_at_utc separately to distinguish '
        'parent waiting time. Write only your assigned runs/A or runs/P JSON. No commits or '
        'branch changes. Never save source bodies, usernames or long quotations.')

def prepare_original(r):
    at=now();d,status=request_json(r['revision_loader_url'])
    x=next(x for x in d['items'] if x.get('revision_guid')==r['revision_guid'] and x.get('body'))
    t=text_of(x['body'],x.get('title',''))
    proof={'url':r['revision_loader_url'],'revision_guid':r['revision_guid'],
           'revision_number':1,'at_utc':at,'status':status,
           'body_html_sha256':hashlib.sha256(x['body'].encode()).hexdigest(),
           'question_sha256':hashlib.sha256(t.encode()).hexdigest(),
           'word_count':len(t.split()),
           'normalization':'questions.generate.text_of v1; title + rendered body; paragraph lines; collapse spaces'}
    return r['id'],proof,t

def main(refresh):
    if any(list((ROOT/'runs'/c).glob('*.json')) for c in ['A','P']):
        raise SystemExit('Frozen questions: executions exist. Reproduce at the pre-execution commit in an isolated checkout; do not overwrite current inputs.')
    old=json.loads((ROOT/'questions/old-metadata.json').read_text())
    new=json.loads((ROOT/'questions/new-draft/new-questions.json').read_text())
    assert len(old)==33 and len(new)==20
    proof_path=ROOT/'questions/new-initial-retrieval.json'
    if refresh:
        originals=[r for r in new if r.get('initial_revision_recovered')]
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
            got=list(ex.map(prepare_original,originals))
        proofs={qid:proof for qid,proof,t in got}
        proof_path.write_text(json.dumps(proofs,ensure_ascii=False,indent=2)+'\n')
        for qid,proof,t in got:print('\nORIGINAL',qid,proof['question_sha256'],'\n'+t)
    else:proofs=json.loads(proof_path.read_text())
    rows=list(old)
    for r in new:
        rr=dict(r);rr['question_summary']=r['summary'];rr['source_subset']='new_directly_screened'
        rr['input_mode']='original' if r['id'] in proofs else 'summary'
        if rr['input_mode']=='original':
            rr['sampling_text_sha256']=r['sha256'];rr['initial_retrieval']=proofs[r['id']]
            rr['sha256']=rr['initial_retrieval']['question_sha256'];rr['word_count']=rr['initial_retrieval']['word_count']
        else:
            rr['initial_retrieval']={'url':r['url'],'status':'current_question_read_initial_revision_unverified',
                                     'at_utc':r['read_at_utc'],'reason':'no initial revision history recovered; execute paraphrase'}
            rr['sha256']=hashlib.sha256(rr['question_summary'].encode()).hexdigest()
            rr['word_count']=len(rr['question_summary'].split())
        rows.append(rr)
    for r in rows:
        inp={'case_id':r['id'],'question_date':r['date'],'question_url_excluded_from_search':r['url'],
             'input_mode':r['input_mode'],'question_sha256':r['sha256'],'question_source':r['initial_retrieval'],
             'question_summary':r['question_summary'] if r['input_mode']=='summary' else None,
             'read_original_command':('python docs/workstreams/research/AF-RES-018/questions/generate.py --emit '+r['id']) if r['input_mode']=='original' else None,
             'common_run_instructions':COMMON}
        (ROOT/'questions/inputs'/f"{r['id']}.json").write_text(json.dumps(inp,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'questions/metadata.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    rng=random.Random(18018);qids=sorted(r['id'] for r in rows);rng.shuffle(qids);order=[]
    for qid in qids:
        conditions=['A','P'];rng.shuffle(conditions)
        for cond in conditions:order.append({'dispatch_index':len(order)+1,'qid':qid,'condition':cond,
                                            'input':f'questions/inputs/{qid}.json','rules':'RULES_A.md' if cond=='A' else 'PROCEDURE.md',
                                            'output':f'runs/{cond}/{qid}.json'})
    (ROOT/'questions/dispatch.json').write_text(json.dumps({'seed':18018,'algorithm':'shuffle sorted question IDs then shuffle [A,P] within each question',
                                                         'python_random':'MT19937','order':order},ensure_ascii=False,indent=2)+'\n')
    counts={'questions':len(rows),'new_platforms':dict(collections.Counter(r['platform'] for r in rows if r['cohort']=='new')),
            'by_cohort_mode':dict(collections.Counter(r['cohort']+'/'+r['input_mode'] for r in rows)),
            'old_main_scope':dict(collections.Counter(r['whole_or_part'] for r in rows if r.get('source_subset')=='main')),
            'dispatches':len(order),'generated_at_utc':now(),'source_bodies_stored':False}
    assert all(r['date']>='2026-06-01' for r in rows if r['cohort']=='new')
    assert max(counts['new_platforms'].values())<=10 and len(counts['new_platforms'])>=3
    assert counts['old_main_scope']=={'whole':15,'part':15}
    (ROOT/'questions/VALIDATION.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(counts,ensure_ascii=False));print('First dispatches:',order[:6])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--refresh-originals',action='store_true');a=p.parse_args();main(a.refresh_originals)
