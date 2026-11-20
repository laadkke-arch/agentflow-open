"""Reproducible serialization of manual candidate judgments; not an automatic semantic judge."""
import json
from pathlib import Path
from datetime import datetime, timezone

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
CASES={c['id']:c for c in json.loads((BASE/'cases/CASES.json').read_text())['cases']}
DECISIONS=json.loads((OUT/'manual-decisions.json').read_text())
VALUE={'p':'pass','n':'not_in_scope','u':'unknown','f':'fail'}
LABEL={'C':'CONDITIONAL_TRANSFER','D':'DIRECT_DOCUMENTED','I':'INSUFFICIENT','V':'SURFACE_OR_CONSTRAINT_MISMATCH'}
rows=[]
for key, decisions in DECISIONS.items():
    cid, baseline=key.split('/')
    case=CASES[cid]
    run=json.loads((BASE/'runs'/baseline/(cid+'.json')).read_text())
    assert len(decisions)==len(run['candidates']),key
    for cand,d in zip(run['candidates'],decisions):
        rank=cand['rank']; assert d['rank']==rank,(key,rank)
        h=[]
        for constraint,(state,why) in zip(case['mandatory_constraints'],d['h']):
            h.append({'constraint_id':constraint['id'],'value':VALUE[state],'reason':why})
        assert len(h)==len(case['mandatory_constraints'])
        gold=[]
        for suffix,why in d.get('matches',[]):
            item=next(g for g in case['gold_items'] if g['id'].endswith('-G'+suffix))
            gold.append({'gold_id':item['id'],'match_kind':item['match_kind'],'rationale':why})
        label=LABEL[d.get('label','C')]
        date=d.get('date_status',cand['date_status'])
        ids=[g['gold_id'] for g in gold]
        relevant=[]
        # Explicit source locations from the preserved run; no re-fetch is counted as baseline evidence.
        candidate_text=json.dumps(cand,ensure_ascii=False)
        for index,doc in enumerate(run['opened_documents']):
            if doc.get('status')=='opened' and (doc['url'].rstrip('/') in candidate_text or doc['url'] in d.get('extra_source_urls',[])):
                relevant.append({'path':f'runs/{baseline}/{cid}.json#/opened_documents/{index}',
                                 'url':doc['url'],'sections_read':doc.get('sections_read',''),
                                 'role':'preserved_run_reading'})
        relevant.append({'path':f'runs/{baseline}/{cid}.json#/raw_response','role':'original_candidate_application_and_caveats'})
        relevant.append({'path':f'cases/prefix/{cid}.md','role':'frozen_problem'})
        if gold: relevant.append({'path':'cases/CASES.json','gold_ids':ids,'role':'frozen_gold'})
        for source_id in d.get('extra_sources',[]):
            relevant.append({'source_id':source_id,'path':'evidence/judging-recovery/c01-c10/sources.json','role':'additional_judgment_read_not_baseline_run'})
        transfer={
            'source_mechanism':cand['reason'],
            'target_part':cand.get('application_scope',''),
            'bridge_and_failure_conditions':cand.get('constraints_or_caveat',''),
            'assessment':d['note'],
            'scope':'reference design only; not implementation or deployment observation'
        }
        t=d.get('T','mapped' if label=='CONDITIONAL_TRANSFER' else ('not_needed' if label=='DIRECT_DOCUMENTED' else 'unknown'))
        useful=(not gold and label in ['CONDITIONAL_TRANSFER','DIRECT_DOCUMENTED']
                and not any(x['value'] in ['fail','unknown'] for x in h)
                and d.get('E','supported')=='supported' and d.get('L','ok')=='ok'
                and (label=='DIRECT_DOCUMENTED' or t=='mapped') and not d.get('exclusion'))
        rows.append({
            'case_id':cid,'baseline':baseline,'rank':rank,'candidate_name':cand['name'],
            'candidate_url':cand['url'],'gold_matches':gold,'review_matches':d.get('review_matches',[]),
            'L':d.get('L','ok'),'E':d.get('E','supported'),'H':h,'T':t,
            'transfer_mapping':transfer,'H_assessment_scope':'reference_design',
            'runtime_observation':'not_performed','implementation_H':'unknown',
            'label':label,'link_status':d.get('link_status','opened_in_original_run'),
            'date_status':date,'original_date_status':cand['date_status'],
            'date_evidence':cand.get('date_evidence','unknown'),
            'date_assessment_note':d.get('date_note','원 실행의 날짜 판정을 유지했다. 현재 열람을 과거 존재 증거로 소급하지 않는다.'),
            'strict_historical_gold_ids':ids if date=='pre_decision' and not d.get('exclusion') else [],
            'post_decision_gold_ids':ids if date=='post_decision' and not d.get('exclusion') else [],
            'date_unknown_gold_ids':ids if date=='unknown' and not d.get('exclusion') else [],
            'nongold_useful':useful,
            'nongold_historical_useful':useful and date=='pre_decision' and d.get('historical_useful',True),
            'near_miss':d.get('near_miss',False),'broken_or_fake':False,
            'exclusion':d.get('exclusion'), 'run_exposure_count':len(run.get('exposures',[])),
            'judge':'내부 별도 검토', 'judge_context':'AF-RES-013#2 recovery; gold visible, baseline execution not repeated',
            'evidence_locations':relevant,
            'remaining_check':d.get('remaining_check','구현 적합성은 해당 후보의 연결·실패 조건을 대상 구현에서 시험해야 한다. 이 행은 문서 기반 참고 관계까지만 판정했다.'),
            'judgment_note':d['note'],
            'not_matched_boundary':d.get('not_matched_boundary',[])
        })

assert len(rows)==117,len(rows)
assert len({(r['case_id'],r['baseline'],r['rank']) for r in rows})==len(rows)
payload={'schema_version':1,'judge':'내부 별도 검토','input_commit':'caa2a814727dd485ed0eb9bb8530d6b16fab9584',
         'method':'Manual reading of all 20 raw responses, candidates and opened-document logs; boundary primary-source checks are separate from original runs.',
         'generated_at_utc':datetime.now(timezone.utc).isoformat(),'judgments':rows}
(OUT/'judgments.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
summary={}
for r in rows:
    key=r['case_id']+'/'+r['baseline']
    s=summary.setdefault(key,{'candidates':0,'primary_gold_ids':set(),'historical_gold_ids':set(),'nongold_useful':0,'labels':{}})
    s['candidates']+=1;s['primary_gold_ids'].update(m['gold_id'] for m in r['gold_matches']);s['historical_gold_ids'].update(r['strict_historical_gold_ids'])
    s['nongold_useful']+=int(r['nongold_useful']);s['labels'][r['label']]=s['labels'].get(r['label'],0)+1
for s in summary.values():
    s['primary_gold_ids']=sorted(s['primary_gold_ids']);s['historical_gold_ids']=sorted(s['historical_gold_ids'])
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False))
