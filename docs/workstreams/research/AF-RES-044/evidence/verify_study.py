"""Verify sealed denominators, actual trial accounting, ID arithmetic and report shape.

This is a deterministic audit of committed observations, not an application
runtime test or an independent human assessment of source interpretation.
"""
from pathlib import Path
from collections import Counter
from urllib.parse import urljoin,urldefrag
import csv,json,hashlib,datetime

ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
def jl(p):return [json.loads(s) for s in (ROOT/p).read_text().splitlines()]
def csvrows(p):return list(csv.DictReader((ROOT/p).open()))
checks=[]
def check(name,condition,unit,observed,expected,evidence):
    checks.append(dict(check=name,met=bool(condition),unit=unit,observed=observed,expected=expected,evidence=evidence))

pool=csvrows('pool.csv');frame=csvrows('frame.csv');req=csvrows('requirements.csv')
groups=jl('groups.jsonl');views=jl('views.jsonl');plans=jl('evidence/trial-plan.jsonl');obs=jl('evidence/trial-observations.jsonl')
clicks=csvrows('clicks.csv');results=load('evidence/results-data.json');sources=jl('sources.jsonl')
bytrial={r['trial_id']:r for r in clicks};byobs={r['trial_id']:r for r in obs};bypool={p['candidate_id']:p for p in pool}
cases=load('evidence/cases.json');gold=load('evidence/pool-gold-summary.json')
for name,digest in load('evidence/input-freeze.json')['files'].items():
    actual=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
    check('sealed_'+name,actual==digest,'SHA256',actual,digest,'evidence/input-freeze.json')
check('sample_frame',Counter(r['ledger'] for r in frame)=={'P':40,'V':40},'exposed issue rows',dict(Counter(r['ledger'] for r in frame)),{'P':40,'V':40},'frame.csv2–81')
selected=[r for r in frame if r['selected']=='True']
check('natural_strata',Counter((r['ledger'],r['stratum']) for r in selected)=={('P','N'):2,('P','K'):2,('V','N'):2,('V','K'):2},'selected requests',len(selected),8,'frame.csv selected=True')
check('six_slots_per_case',len(pool)==72 and all([int(p['rank']) for p in pool if p['case_id']==c['case_id']]==list(range(1,7)) for c in cases),'candidate slots',len(pool),72,'pool.csv2–73')
check('raw_href_resolution',all(urljoin(p['html_url'],p['raw_href'])==p['url'] for p in pool if p['url']),'nonempty href slots',sum(bool(p['url']) for p in pool),41,'pool.csv raw_href/html_url/url')
check('missing_not_exhausted',Counter(p['empty_kind'] for p in pool if not p['url'])=={'unobserved':24,'exhausted_scope':7},'empty slots',dict(Counter(p['empty_kind'] for p in pool if not p['url'])),{'unobserved':24,'exhausted_scope':7},'pool.csv empty_kind')
check('identical_three_method_input',len(groups)==36 and all(g['input_candidates']==[p['candidate_id'] for p in pool if p['case_id']==g['case_id']] and g['gold_used_as_key'] is False for g in groups),'case-method groups',len(groups),36,'groups.jsonl1–36')
check('three_cards_and_fixed_labels',len(views)==36 and all(len(v['cards'])==3 and all(c['description']=='' and c['description_length']==0 and (c['label']=='원문 보기' and c['label_length']==5 if c['url'] else c['label']=='' and c['label_length']==0) for c in v['cards']) for v in views),'display cards',sum(len(v['cards']) for v in views),108,'views.jsonl1–36')
for g,v in zip(groups,views):
    expected=[x['representative'] for x in g['groups'][:3]];expected+= [None]*(3-len(expected))
    check('first_representative_'+v['view_id'],expected==[c['candidate_id'] for c in v['cards']] and all(x['representative']==x['members'][0] for x in g['groups']),'ordered representatives',[c['candidate_id'] for c in v['cards']],expected,'groups.jsonl and views.jsonl '+v['view_id'])
check('plan_observation_identity',len(plans)==len(obs)==1924 and len(byobs)==1924 and set(byobs)=={t['trial_id'] for t in plans} and all(t['steps']==byobs[t['trial_id']]['steps'] for t in plans),'unique fixed-plan trials',len(byobs),1924,'trial-plan.jsonl / trial-observations.jsonl')
check('actual_cost_and_fresh_start',all(t['fresh_start'] and t['budget']==2 and 1<=byobs[t['trial_id']]['cost_used']==len(byobs[t['trial_id']]['arrivals'])<=sum(s['cost'] for s in t['steps'])<=2 for t in plans),'cost-limited independent trials',len(plans),1924,'trial-observations.jsonl cost_used and steps')
pop=Counter(r['observation_population'] for r in clicks)
check('no_cloned_shared_trials',len(bytrial)==len(clicks)==1927 and pop=={'main_fixed_plan':1924,'separate_browser':1,'separate_shared_revalidation':2},'actual unique trials',dict(pop),{'main_fixed_plan':1924,'separate_browser':1,'separate_shared_revalidation':2},'clicks.csv2–1928')
check('semantic_scope_is_arrived',all(int(r['semantic_read_scope_count'])<=int(r['successful_destination_count']) for r in clicks),'admitted read scopes',sum(int(r['semantic_read_scope_count']) for r in clicks),3051,'clicks.csv semantic_read_scope_count / successful_destination_count')
check('no_false_sibling_http',all(r['connectivity_success']=='해당 없음' and r['semantic_read_scope_count']=='0' for r in clicks if r['source_destination_count']=='0'),'no-document trials',sum(r['source_destination_count']=='0' for r in clicks),55,'clicks.csv siblings_only')
attempted={a['url'] for r in clicks for a in json.loads(r['arrivals'])};arrived={a['url'] for r in clicks for a in json.loads(r['arrivals']) if a['success']}
check('all_candidate_links_attempted',all(p['url'] in attempted for p in pool if p['url']),'nonempty candidate slots attempted',sum(p['url'] in attempted for p in pool if p['url']),41,'clicks.csv arrivals; source-level semantic reads in sources.jsonl')
for v in results['views']:
    cid=v['case_id'];vid=cid+'-'+v['method'];tr=[r for r in clicks if vid in json.loads(r['applicable_views'])]
    eligible=set(v['eligible_ids'] or []);union=set().union(*(set(json.loads(r['confirmed_complete_ids'])) for r in tr)) if tr else set()
    witnesses=all(tid in bytrial and aid in json.loads(bytrial[tid]['confirmed_complete_ids']) and vid in json.loads(bytrial[tid]['applicable_views']) and int(bytrial[tid]['actual_cost'])<=2 for aid,tid in v['witnesses'].items())
    check('single_trial_witness_'+vid,witnesses,'complete-ID witnesses',len(v['witnesses']),len(union),'results-data.json witnesses → clicks.csv trial_id')
    if v['input_pool_observed']:
        check('union_and_max_'+vid,set(v['reachable_original_pool_ids'])==union&eligible and set(v['additional_ids_outside_denominator'])==union-eligible and v['max_complete_original_pool_ids_in_one_trial']==max((len(json.loads(r['confirmed_original_pool_ids'])) for r in tr),default=0),'complete original-pool IDs',len(union&eligible),len(v['reachable_original_pool_ids']),'results-data.json; clicks.csv independent rows')
        check('W_monotone_'+vid,set(v['direct_complete_ids'])<=set(v['W_direct_complete_ids']) and set(v['reachable_original_pool_ids'])<=set(v['W_reachable_original_pool_ids']),'strict evidence subset',True,True,'results-data.json W fields')
    else:
        check('unknown_pool_not_zero_'+vid,all(v[k] is None for k in ['eligible_count','eligible_ids','direct_complete_ids','reachable_original_pool_ids','max_complete_original_pool_ids_in_one_trial']),'unobserved quantities','미확인','미확인','results-data.json P cases')
check('expected_pool_denominators',{c:g['eligible_count'] for c,g in gold.items()}=={'P1':None,'P2':None,'P3':None,'P4':None,'V1':0,'V2':0,'V3':0,'V4':0,'C1':2,'C2':11,'C3':1,'C4':0},'complete pool alternatives',sum(g['eligible_count'] or 0 for g in gold.values()),14,'pool-gold-summary.json; gold-paths.csv')
changes=csvrows('changes.csv')
for i,r in enumerate(changes,2):
    if r['row_type']=='paired' and r['before_ids']!='미확인':
        before=set(json.loads(r['before_ids']));after=set(json.loads(r['after_ids']))
        check('bidirectional_difference_line'+str(i),set(json.loads(r['gained_ids']))==after-before and set(json.loads(r['lost_ids']))==before-after,'alternative ID set difference',True,True,'changes.csv'+str(i))
required={'source_id','original_url','pinned_url_or_version','publisher','event_or_publication_date','checked_utc','locator','source_kind','verified_fact','limitation','question_ids','case_ids','duplicate_group','counted'}
counted=[s for s in sources if s['counted']]
check('source_schema_and_unique_primary',all(required<=s.keys() for s in sources) and len({s['source_id'] for s in sources})==len(sources) and len({s['duplicate_group'] for s in counted})==len(counted) and len(counted)>=28,'distinct counted originals',len(counted),'>=28','sources.jsonl; source-count-audit.json')
review=jl('evidence/final-source-review.jsonl')
check('final_Q1_Q7_reopened',set(q for s in review if s['source_kind']!='access_failure' for q in s['question_ids'])=={'Q'+str(i) for i in range(1,8)},'question IDs with successful final source reread',7,7,'final-source-review.jsonl')
lines=(ROOT/'RESULT.md').read_text().splitlines();blocks=[];current=[]
for n,line in enumerate(lines,1):
    if line.startswith('| '):current.append((n,line))
    elif current:blocks.append(current);current=[]
if current:blocks.append(current)
check('required_table_order',lines[0].startswith('# ') and blocks[0][0][0]==3 and len(blocks[0])-2==12 and len(blocks[1])-2==36,'first two table body rows',[len(blocks[0])-2,len(blocks[1])-2],[12,36],'RESULT.md3–55')
check('exactly_three_ending_weaknesses',len(blocks[-1])-2==3 and blocks[-1][-1][0]==len(lines),'last table rows',len(blocks[-1])-2,3,'RESULT.md final table; evidence/weaknesses.json')
report={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'audit_kind':'deterministic research-ledger self-check; no application execution or human-behavior claim','all_checks_passed':all(x['met'] for x in checks),'passed':sum(x['met'] for x in checks),'total':len(checks),'checks':checks,'counts':{'natural_slots':48,'control_slots':24,'nonempty_slots':41,'unique_candidate_urls':len({p['url'] for p in pool if p['url']}),'candidate_original_documents':len({urldefrag(p['url'])[0] for p in pool if p['url']}),'candidate_slots_arrived_exact_scope':sum(p['url'] in arrived for p in pool if p['url']),'observed_natural_slot_positions':24,'active_source_rows':len(sources),'counted_primary_originals':len(counted),'unique_actual_trials':len(clicks),'admitted_semantic_scopes':sum(int(r['semantic_read_scope_count']) for r in clicks),'successful_arrivals':sum(int(r['successful_destination_count']) for r in clicks)},'acceptance_note':'Passing arithmetic does not satisfy the missing natural pools, V3 rule deviation, or insufficient positive controls.'}
(ROOT/'evidence/verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False))
if not report['all_checks_passed']:
    print(json.dumps([x for x in checks if not x['met']],ensure_ascii=False,indent=2))
    raise SystemExit(1)
