"""Join frozen ranks to same-path observations and recount all denominators."""
from pathlib import Path
from collections import Counter,defaultdict
from datetime import datetime,timezone
import csv,json

P=Path(__file__).resolve().parent
def readcsv(f):return list(csv.DictReader((P/f).open(encoding='utf-8')))
def j(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def writecsv(f,rows):
    with (P/f).open('w',encoding='utf-8',newline='') as out:
        w=csv.DictWriter(out,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)

matches=readcsv('matches.csv');slots=readcsv('slots.csv');reqs=json.loads((P/'requirements.json').read_text())
planned=json.loads((P/'evidence/path-plan.json').read_text())['cases']
expected={(x['case_id'],x['catalog_id']) for x in planned}
observations=[]
for owner in ['paths-schema','paths-ld','root-paths']:
    f=P/'evidence'/owner/'observations.json'
    assert f.exists(),str(f)+' is not complete'
    data=json.loads(f.read_text())
    if isinstance(data,dict):data=data.get('observations',data.get('paths',[]))
    for o in data:o['ledger_owner']=owner;observations.append(o)
by_pair=defaultdict(list)
for o in observations:by_pair[(o['case_id'],o['catalog_id'])].append(o)
assert set(by_pair)==expected,(set(by_pair)-expected,expected-set(by_pair))
assert all(len(v)==3 and {x['path_id'] for x in v}=={'P1','P2','P3'} for v in by_pair.values())
allowed={'complete','partial','confirmed_wrong','unconfirmed'}
assert all(o['judgment'] in allowed for o in observations)

priority={'complete':0,'confirmed_wrong':1,'partial':2,'unconfirmed':3}
verdicts=[];verdict={}
for key,paths in sorted(by_pair.items()):
    # Choose an entire path. Never take C1 from one and C2 from another.
    chosen=min(paths,key=lambda x:(priority[x['judgment']],len(x.get('documents',[])),x['path_id']))
    v={'case_id':key[0],'catalog_id':key[1],'judgment':chosen['judgment'],'chosen_path_id':chosen['path_id'],
       'C1_status':chosen['C1_status'],'C2_status':chosen['C2_status'],'environment_status':chosen['environment_status'],
       'rationale':chosen['rationale'],'path_judgments':{o['path_id']:o['judgment'] for o in paths},
       'budget_statuses':{o['path_id']:o.get('budget_status','inherited_boundary_gap' if o.get('display_word_gap') else 'within_saved_window_budget') for o in paths},
       'ledger_owner':chosen['ledger_owner'],'source_ids':[d.get('source_id') for d in chosen.get('documents',[]) if d.get('source_id')],
       'direct_evidence':chosen.get('direct_evidence'),
       'execution_status':chosen.get('execution_status','not_run')}
    verdicts.append(v);verdict[key]=v
(P/'evidence/candidate-verdicts.json').write_text(json.dumps(verdicts,ensure_ascii=False,indent=2)+'\n')

pathrows=[]
for o in sorted(observations,key=lambda x:(x['case_id'],x['catalog_id'],x['path_id'])):
    docs=o.get('documents',[])
    pathrows.append({'path_id':o['case_id']+'::'+o['catalog_id']+'::'+o['path_id'],'case_id':o['case_id'],'catalog_id':o['catalog_id'],
        'path':o['path_id'],'documents_json':j(docs),'first_document':docs[0].get('fixed_url',docs[0].get('original_url','')) if docs else '',
        'second_document':docs[1].get('fixed_url',docs[1].get('original_url','')) if len(docs)>1 else '',
        'C1_status':o['C1_status'],'C2_status':o['C2_status'],'environment_status':o['environment_status'],
        'same_implementation_version':j(o.get('same_implementation_version')),'judgment':o['judgment'],
        'budget_status':o.get('budget_status','inherited_boundary_gap' if o.get('display_word_gap') else 'within_saved_window_budget'),
        'direct_evidence_json':j(o.get('direct_evidence',{})),'counterexample_json':j(o.get('counterexample',{})),
        'rationale':o['rationale'],'execution_status':o.get('execution_status','not_run'),
        'outside_budget_editor_evidence':j(o.get('outside_budget_editor_evidence','')),
        'observed_utc':o.get('observed_utc',''),'source_ledger':'evidence/'+o['ledger_owner']+'/observations.json'})
writecsv('paths.csv',pathrows)

lookup={(m['case_id'],m['query'],m['fields']):m for m in matches}
def ids(m):return [x['catalog_id'] for x in json.loads(m['all_matches_json'])]
def change(a,b):
    aa,bb=ids(a),ids(b)
    return {'all_new':[x for x in bb if x not in aa],'all_removed':[x for x in aa if x not in bb],
            'top3_new':[x for x in bb[:3] if x not in aa[:3]],'top3_removed':[x for x in aa[:3] if x not in bb[:3]],
            'rank_moves':[{'catalog_id':x,'before':aa.index(x)+1,'after':bb.index(x)+1} for x in aa if x in bb and aa.index(x)!=bb.index(x)]}
changes=[];displacements=[]
for r in reqs:
    c=r['case_id'];lf0,vf0,lf1,vf1=[lookup[(c,q,f)] for q,f in [('L','F0'),('V','F0'),('L','F1'),('V','F1')]]
    allchanges={'field_L':change(lf0,lf1),'field_V':change(vf0,vf1),'query_F0':change(lf0,vf0),'query_F1':change(lf1,vf1)}
    both=[x for x in ids(vf1) if x not in set(ids(lf1)+ids(vf0))]
    judgment_deltas={}
    for axis,d in allchanges.items():
        assert not d['all_removed'],(c,axis,'OR expansion cannot remove a pool member')
        judgment_deltas[axis]={'new_top3':dict(Counter(verdict[(c,x)]['judgment'] for x in d['top3_new'])),
                               'removed_top3':dict(Counter(verdict[(c,x)]['judgment'] for x in d['top3_removed']))}
        for x in d['top3_removed']:
            movement=next((z for z in d['rank_moves'] if z['catalog_id']==x),None)
            displacements.append({'case_id':c,'axis':axis,'catalog_id':x,'movement':movement,'judgment':verdict[(c,x)]['judgment']})
    changes.append({'case_id':c,'layer':r['layer'],'L_F0_count':lf0['total_matches'],'V_F0_count':vf0['total_matches'],
        'L_F1_count':lf1['total_matches'],'V_F1_count':vf1['total_matches'],
        **{k+'_json':j(v) for k,v in allchanges.items()},'both_required_candidates_json':j(both),'judgment_deltas_json':j(judgment_deltas),
        'editor_cost_allocation':'one shared all62-row F1 edit; not twelve independent editing projects',
        'next_verification':'same candidate/version and original environment, paired positive/near-negative; unknown is not unsupported'})
writecsv('changes.csv',changes)
for s in slots:
    if s['display_status']=='filled':
        v=verdict[(s['case_id'],s['catalog_id'])];s['judgment']=v['judgment'];s['chosen_path']=v['chosen_path_id'];s['path_budget_statuses']=j(v['budget_statuses'])
    else:s['chosen_path']='';s['path_budget_statuses']=''
    s['displacement']=j([d for d in displacements if d['case_id']==s['case_id'] and d['catalog_id']==s['catalog_id']]) if s['catalog_id'] else ''
writecsv('slots.csv',slots)

cohort=[]
for layer in ['existing_tuning','new_holdout','all']:
    cases={r['case_id'] for r in reqs if layer=='all' or r['layer']==layer}
    for f in ['F0','F1']:
        for q in ['L','V']:
            mm=[m for m in matches if m['case_id'] in cases and m['fields']==f and m['query']==q]
            ss=[s for s in slots if s['case_id'] in cases and s['fields']==f and s['query']==q]
            counts=Counter(s['judgment'] for s in ss if s['display_status']=='filled')
            cohort.append({'layer':layer,'query':q,'fields':f,'requirement_denominator':len(cases),'nonempty_cases':sum(int(m['total_matches'] or 0)>0 for m in mm),
                'all_match_occurrences':sum(int(m['total_matches'] or 0) for m in mm),'filled_slots':sum(s['display_status']=='filled' for s in ss),
                **{k:counts[k] for k in ['complete','partial','confirmed_wrong','unconfirmed']},
                'accuracy':'not_estimable' if not counts or counts['unconfirmed'] or counts['partial'] else 'fully_adjudicated_only'})
metrics={'counted_utc':datetime.now(timezone.utc).isoformat(),'comparisons':len(matches),'slots':len(slots),
    'filled_slots':sum(s['display_status']=='filled' for s in slots),'empty_reasons':dict(Counter(s['empty_reason'] for s in slots if s['display_status']!='filled')),
    'all_match_occurrences':sum(int(m['total_matches'] or 0) for m in matches),'unique_case_provider_pairs':len(by_pair),'unique_provider_rows':len({k[1] for k in by_pair}),
    'path_observations':len(observations),'candidate_judgments':dict(Counter(v['judgment'] for v in verdicts)),
    'path_judgments':dict(Counter(o['judgment'] for o in observations)),'filled_slot_judgments':dict(Counter(s['judgment'] for s in slots if s['display_status']=='filled')),
    'both_axes_required_pairs':sum(len(json.loads(c['both_required_candidates_json'])) for c in changes),'displacements':displacements,'cohorts':cohort,
    'noncompliant_or_unconfirmed_budget_paths':[{'case_id':r['case_id'],'catalog_id':r['catalog_id'],'path':r['path'],'budget_status':r['budget_status']} for r in pathrows if r['budget_status'] not in ['within_saved_window_budget','within_budget','within_registered_budget','within_registered_document_and_window_limits']],
    'interpretation':'Repeated slots/cells are not independent experiments. Partial support is one documented condition, not a full correct recommendation or observed user success.'}
(P/'evidence/comparison-summary.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n')
print(j({k:v for k,v in metrics.items() if k not in ['cohorts','displacements','noncompliant_or_unconfirmed_budget_paths','interpretation']}))
