"""Read-only content checks plus an owned-path JSON receipt; no product tests."""
from pathlib import Path
from collections import Counter,defaultdict
import csv, datetime, hashlib, json, re, subprocess, sys

B=Path(__file__).resolve().parents[1]
ROOT=B.parents[3]
checks=[]
def test(key, ok, detail=''):
    checks.append(dict(key=key,passed=bool(ok),detail=detail))
def csvread(name):
    with (B/name).open(newline='') as f:
        raw=list(csv.reader(f))
    test(name+':columns',bool(raw) and all(len(r)==len(raw[0]) for r in raw[1:]), {'header_columns':len(raw[0]),'rows':len(raw)-1})
    test(name+':unique_headers',len(raw[0])==len(set(raw[0])))
    return list(csv.DictReader((B/name).open(newline='')))
def j(name):return json.loads((B/name).read_text())
def parse(t):return datetime.datetime.fromisoformat(t.replace(' UTC','+00:00').replace('Z','+00:00'))

names=['ENROLLMENT.csv','EVENTS.csv','VIEWS.csv','OUTCOMES.csv','PINS.csv','PAIRS.csv','Q_CHECK.csv','COMMITS.csv']
ledgers={n:csvread(n) for n in names}
en,events,views,out,pins=[ledgers[n] for n in names[:5]]
cases=j('CASES.json'); ci={r['issue_id']:r for r in cases}; ev={r['event_id']:r for r in events}
ss=[json.loads(l) for l in (B/'SOURCES.jsonl').read_text().splitlines() if l.strip()];si={r['source_id']:r for r in ss}
for name,rows,key in [('ENROLLMENT',en,'enrollment_id'),('EVENTS',events,'event_id'),('VIEWS',views,'view_id'),('OUTCOMES',out,'outcome_id'),('PINS',pins,'pin_id'),('SOURCES',ss,'source_id')]:
    test(name+':unique_key',len({r[key] for r in rows})==len(rows))
test('main_12_and_diagnostic_12',Counter(c['scope'] for c in cases)=={'main':12,'diagnostic':12})
test('initial32_total64',len(en)==64 and sum(int(r['sequence'])<=8 for r in en)==32)
test('first_body_recovery_56',sum(r['initial_body_verified']=='true' for r in en)==56)
test('chosen24_original_recovered',all(next(r for r in en if r['issue_id']==c['issue_id'])['initial_body_verified']=='true' for c in cases))
for repo in {r['repository'] for r in en}:
    rs=[r for r in en if r['repository']==repo]
    test('queue:'+repo,sorted(int(r['sequence']) for r in rs)==list(range(1,17)))
    eligible=[r['issue_id'] for r in rs if r['eligible']=='true'][:3]
    selected=[r['issue_id'] for r in rs if r['selected_main']=='true']
    test('first3:'+repo,eligible==selected)
for r in views+out+pins+events:
    test('issue_join:'+str(r.get('view_id',r.get('outcome_id',r.get('pin_id',r.get('event_id'))))),r['issue_id'] in ci)
counted=[r for r in ss if r['count_toward_minimum']]
test('lineage_count_unique',len({r['lineage_id'] for r in counted})==len(counted))
test('direct_read_for_counted',all(r['direct_read'] is True for r in counted))
sa=j('evidence/source-audit.json')
test('minimum_20_12_8',sa['totals']['counted_original_works']>=20 and sa['totals']['counted_original_issues']>=12 and sa['totals']['counted_official_works']>=8)
test('source_claim_boundaries',all(r.get('verified_claim') and r.get('cannot_determine') and r.get('contrary_or_unknown') for r in ss))
for p in pins:
    test('pin_source:'+p['pin_id'],p['source_id'] in si)
    test('pin_fixed_SHA:'+p['pin_id'],bool(re.search(r'/blob/[0-9a-f]{40}/',p['pinned_url'])))
for c in cases:
    ab=[r for r in views if r['issue_id']==c['issue_id']];a=next(r for r in ab if r['view']=='A');b=next(r for r in ab if r['view']=='B')
    test('two_views:'+c['issue_id'],len(ab)==2)
    same=['candidate_ids','candidate_1','candidate_2','version','evidence_sections','goal','prohibitions','selected_field']
    test('same_packet:'+c['issue_id'],all(a[k]==b[k] for k in same))
    test('one_field:'+c['issue_id'],int(b['values_copied_into_B'])<=1 and int(b['new_information_values'])<=1)
    if c['B_value'] is not None:
        be=ev.get(c['B_event_id'],{})
        test('B_author:'+c['issue_id'],str(be.get('actor_id'))==str(c['author_id']))
        test('B_source:'+c['issue_id'],bool(be) and be.get('original_url')==c['B_source_url'])
    else:
        cr=next(r for r in out if r['row_type']=='case' and r['issue_id']==c['issue_id'])
        test('noB_not_zero:'+c['issue_id'],cr['strict_accuracy_change']=='unobservable' and cr['strict_effect_denominator']=='false')
    for candidate in c['candidates']:
        ps=[r for r in pins if r['issue_id']==c['issue_id'] and r['candidate_id']==candidate['id']]
        docs=defaultdict(set)
        for p in ps:docs[p['source_id']].add(p['section'])
        test('budget_packet:'+candidate['id'],1<=len(docs)<=2 and all(len(v)==1 for v in docs.values()))
seals=j('evidence/seal-verification.json');times={s['sha']:parse(s['committed_utc']) for s in seals['commits']}
test('all_sealed_files_unchanged',seals['all_match'] and len(seals['files'])==21)
for c in cases:
    test('seal_time:'+c['issue_id'],parse(c['cutoff_A_utc'])<times[c['A_seal_sha']]<parse(c['first_comment_read_utc']), 'Previously exposed current text/comments remain separately marked; this does not erase prior exposure.')
test('new1_redundant2',sum(c['B_is_new'] for c in cases)==1 and sum(c['B_value'] is not None and not c['B_is_new'] for c in cases)==2)
test('ask8_skip16',Counter(c['question_decision'] for c in cases)=={'ask':8,'skip':16})
test('FP_denominator2_not8',sum(c['false_positive_denominator'] for c in cases)==2 and all(c['false_positive'] is False for c in cases if c['false_positive_denominator']))
test('strict_effect_NA',not any(c['strict_effect_denominator'] for c in cases))
test('Q1_Q8_complete',{r['question_id'] for r in ledgers['Q_CHECK.csv']}=={f'Q{i}' for i in range(1,9)})
for q in ledgers['Q_CHECK.csv']:
    test('Q_evidence:'+q['question_id'],all(s in si for s in q['evidence_source_ids'].split(';')) and bool(q['counterexample_search_and_readout']) and bool(q['unknown_and_resume_source']))
for g in j('evidence/ledger-summary.json')['groups']:
    test('table3_sum:'+g['scope']+g['necessity'],g['improved']+g['same']+g['worsened']+g['unobservable']==g['slots'])

result=B/'RESULT.md'
if result.exists():
    lines=result.read_text().splitlines();tables=[];current=[]
    for line in lines+['']:
        if line.startswith('|'):current.append(line)
        elif current:tables.append(current);current=[]
    for i,t in enumerate(tables,1):
        cols=[len(re.split(r'(?<!\\)\|',x))-2 for x in t]
        test('RESULT_table_columns:'+str(i),len(set(cols))==1,cols)
    test('required_tables_first',len(tables)>=4 and [len(re.split(r'(?<!\\)\|',t[0]))-2 for t in tables[:4]]==[5,8,8,8])
    test('weaknesses_exactly3',len(re.findall(r'^### 약점 [123]\b',result.read_text(),re.M))==3)
    test('RESULT_Q1_Q8',all(re.search(r'^### Q'+str(i)+r'\b',result.read_text(),re.M) for i in range(1,9)))
else:test('RESULT_pending_before_results_bundle',True,'not yet created; not a final validation')

head=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,text=True,capture_output=True)
target=head.stdout.strip() if head.returncode==0 else 'unavailable'
input_paths=[B/n for n in names]+[B/'CASES.json',B/'SOURCES.jsonl']+([result] if result.exists() else [])
receipt=dict(generated_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),command='python -B docs/workstreams/research/AF-RES-070/tools/validate.py',cwd=str(ROOT),target_git_head=target,working_tree_input_hashes={str(p.relative_to(B)):hashlib.sha256(p.read_bytes()).hexdigest() for p in input_paths},checks=checks,passed=sum(x['passed'] for x in checks),failed=[x for x in checks if not x['passed']],limitations=['Historical product binaries not executed','Unrecovered edit histories and missing access UTC remain explicit','Scope Git comparison and final remote SHA re-open are separate receipts'])
receipt['exit_code']=0 if not receipt['failed'] else 1
(B/'evidence/validation.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ['target_git_head','passed','failed','exit_code']},ensure_ascii=False))
sys.exit(receipt['exit_code'])
