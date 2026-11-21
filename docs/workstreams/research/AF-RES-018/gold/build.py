#!/usr/bin/env python3
"""Integrate pre-execution answer records and separately scoped check truth."""
from pathlib import Path
import csv,datetime,hashlib,json,random,re,subprocess,collections
ROOT=Path(__file__).resolve().parents[1]
if any(list((ROOT/'runs'/c).glob('*.json')) for c in ['A','P']):
    raise SystemExit('Frozen gold: executions exist. Reproduce at the pre-execution commit in an isolated checkout; do not overwrite current gold.')
def read(p):return json.loads((ROOT/p).read_text())
def write(p,d):(ROOT/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def norm(s):return re.sub(r'[^a-z0-9]+',' ',str(s).lower()).strip()

meta={r['id']:r for r in read('questions/metadata.json')}
drafts=[]
for f in ['gold/draft-a/checks-draft.json','gold/draft-b/checks-draft.json']:
    for q in read(f)['questions']:
        assert q['question_sha256']==meta[q['qid']]['sha256']
        drafts.append((q['qid'],q['checks'],f))
new=collections.defaultdict(list)
for c in read('questions/new-draft/checks-draft.json')['rows']:new[c['qid']].append(c)
for qid,rows in new.items():drafts.append((qid,rows,'questions/new-draft/checks-draft.json'))
assert len(drafts)==53 and {q for q,c,f in drafts}==set(meta)
rng=random.Random(18018);questions=[]
for qid,rows,ledger in sorted(drafts):
    assert len(rows)==3
    checks=[]
    for i,r in enumerate(rows):
        c=dict(r);name=c.get('name') or c.get('candidate');url=c.get('url') or c.get('candidate_url')
        assert name, (qid,i,'missing named candidate')
        assert url or qid=='T054', (qid,i,'missing artifact URL')
        slot=c['slot'];is_pos=slot=='positive' and str(c.get('grade')) in ['1','2']
        pos=c.get('eligible_positive_denominator',is_pos)
        neg=c.get('eligible_current_strict_N_denominator',c.get('eligible_strict_n_denominator',c.get('strict_N_count_eligible',False)))
        zero=c.get('eligible_unrelated_denominator',slot in ['unrelated','irrelevant'])
        cid='CK-'+hashlib.sha256(f'18018:{qid}:{i}:{name}'.encode()).hexdigest()[:12]
        c.update({'check_id':cid,'qid':qid,'name':name,'url':url,
                  'source_check_id':r.get('check_id'),'ledger':ledger,
                  'eligible_positive_denominator':bool(pos),
                  'eligible_current_strict_N_denominator':bool(neg),
                  'eligible_unrelated_denominator':bool(zero),
                  'parent_grade_provenance':'external records for2/1; scoped worker adjudication for constructed N/0; see ledger'})
        checks.append(c)
    rng.shuffle(checks)
    questions.append({'qid':qid,'question_sha256':meta[qid]['sha256'],
                      'positive_available':any(c['eligible_positive_denominator'] for c in checks),
                      'current_strict_N_available':any(c['eligible_current_strict_N_denominator'] for c in checks),
                      'checks':checks})
write('gold/checks.json',{'status':'FROZEN_BEFORE_EXECUTION','seed':18018,
                         'ordering':'independent Random(18018), sorted question IDs, shuffle three source slots',
                         'questions':questions,
                         'scope_warning':'Three named probes per question are complete; three requested truth roles are not complete. Unavailable roles are excluded from their denominators, never relabeled as strict N.'})

answers=[]
for x in read('gold/old-answers.json'):
    r=dict(x);r['temporal_scope']='fixed014 historical external answer record'
    r['eligible_for_entity_recall']=True;answers.append(r)
for x in read('questions/new-draft/gold-draft.json')['rows']:
    r=dict(x);r['query_id']=r['qid'];r['source_url']=r['evidence_url'];r['gold_provenance']=r['record_type']
    r['gold_judge']=r['judge'];r['temporal_scope']='external record observed through 2026-11-21, may follow changed constraints'
    r['eligible_for_entity_recall']=True
    pos=next((c for q in questions if q['qid']==r['query_id'] for c in q['checks'] if c['name']==r['candidate']),None)
    if pos:r['candidate_url']=pos['url']
    answers.append(r)
answers.extend(read('gold/draft-b/supplemental-answers.json')['answers'])
sha011='478c301b693896e2c6d777f46ac441f071bfdfe8'
near=json.loads(subprocess.check_output(['git','show',sha011+':docs/workstreams/research/AF-RES-011/evidence/near-misses.json']))['pairs']
for n in near:
    if not n.get('count_as_near_miss') or n['case_id'] not in meta:continue
    exists=any(r['query_id']==n['case_id'] and str(r['grade'])=='N' and norm(r['candidate'])==norm(n['candidate']) for r in answers)
    if exists:continue
    answers.append({'query_id':n['case_id'],'candidate':n['candidate'],'candidate_url':None,'grade':'N',
                    'answer_id':n.get('answer_id'),'source_url':n['url'],'evidence_id':n['id'],'mapping':'historical_external_rejection',
                    'gold_provenance':'fixed011 strict near-miss external record','gold_judge':'prior worker coding of external rejection',
                    'source_sha':sha011,'temporal_scope':'historical requirement/edition; current validity separate in checks',
                    'eligible_for_entity_recall':True,'note':n['limits']})
for r in answers:
    r['entity_id']='E-'+hashlib.sha256((r['query_id']+':'+norm(r['candidate'])).encode()).hexdigest()[:12]
    r.setdefault('eligible_for_entity_recall',True);r.setdefault('temporal_scope','external record; current compliance separate')
    r.setdefault('candidate_url',None)
write('gold/answers.json',answers)
fields=['query_id','entity_id','candidate','candidate_url','grade','answer_id','source_url','evidence_id','mapping','gold_provenance','gold_judge','source_sha','temporal_scope','eligible_for_entity_recall','note']
with (ROOT/'gold/answers.tsv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',extrasaction='ignore');w.writeheader();w.writerows(answers)
summary={'question_count':len(questions),'named_probe_count':sum(len(q['checks']) for q in questions),
         'positive_eligible':sum(c['eligible_positive_denominator'] for q in questions for c in q['checks']),
         'strict_N_eligible':sum(c['eligible_current_strict_N_denominator'] for q in questions for c in q['checks']),
         'unrelated_eligible':sum(c['eligible_unrelated_denominator'] for q in questions for c in q['checks']),
         'all_three_roles_questions':sum(q['positive_available'] and q['current_strict_N_available'] for q in questions),
         'missing_positive':[q['qid'] for q in questions if not q['positive_available']],
         'missing_current_strict_N':[q['qid'] for q in questions if not q['current_strict_N_available']],
         'external_answer_rows':len(answers),'external_grade_counts':dict(collections.Counter(str(r['grade']) for r in answers)),
         'entity_recall_questions':sum(any(r['query_id']==qid and str(r['grade']) in ['1','2'] and r['eligible_for_entity_recall'] for r in answers) for qid in meta),
         'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'A_runs':len(list((ROOT/'runs/A').glob('*.json'))),'P_runs':len(list((ROOT/'runs/P').glob('*.json')))}
assert summary['named_probe_count']==159 and summary['A_runs']==summary['P_runs']==0
write('gold/VALIDATION.json',summary)
print(json.dumps(summary,ensure_ascii=False,indent=2))
