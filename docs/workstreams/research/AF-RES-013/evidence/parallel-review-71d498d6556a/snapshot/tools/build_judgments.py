"""Expand explicit, candidate-by-candidate research judgments; never infer matches.

All substantive axis values and match explanations come from reviewed notes.
This program checks coverage and computes the already frozen labels/counts.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = {c['id']: c for c in json.loads((ROOT/'cases/CASES.json').read_text())['cases']}

def build():
    records, reviewed_runs, seen_runs = [], [], set()
    for f in sorted((ROOT/'evidence/judgments').glob('*.notes.json')):
        note = json.loads(f.read_text())
        cid, baseline = note['case_id'], note['baseline']
        assert (baseline,cid) not in seen_runs, ('duplicate reviewed run',baseline,cid)
        seen_runs.add((baseline,cid))
        case = CASES[cid]
        runpath = ROOT/'runs'/baseline/(cid+'.json')
        run = json.loads(runpath.read_text())
        candidates = {x['rank']:x for x in run['candidates']}
        assert set(candidates) == {x['rank'] for x in note['judgments']}, (cid, 'coverage')
        primary = {x['id']:x for x in case['gold_items']}
        review = {x['id']:x for x in case.get('review_gold_items',[])}
        reviewed_runs.append({'case_id':cid,'baseline':baseline,'candidate_count':len(candidates),'notes':str(f.relative_to(ROOT))})
        for n in note['judgments']:
            c = candidates[n['rank']]
            assert n['L'] in ('ok','broken','missing')
            assert n['E'] in ('supported','contradicted','unknown')
            assert n['T'] in ('not_needed','mapped','analogy_only','unknown')
            assert len(n['H']) == len(case['mandatory_constraints']), (cid, n['rank'], 'H coverage')
            H = []
            for constraint, axis in zip(case['mandatory_constraints'],n['H']):
                assert axis[0] in ('pass','fail','unknown','not_in_scope')
                assert axis[1]
                H.append({'constraint_id':constraint['id'],'constraint':constraint['text'],'value':axis[0],'reason':axis[1]})
            assert any(h['value'] != 'not_in_scope' for h in H)
            if n['T'] == 'mapped': assert n.get('transfer_mapping')
            gold = []
            for match in n.get('gold_matches',[]):
                assert match['gold_id'] in primary
                assert match['rationale']
                gold.append({'gold_id':match['gold_id'],'match_kind':primary[match['gold_id']]['match_kind'],'match_basis':match.get('match_basis',primary[match['gold_id']]['match_kind']),'external_entity_hit':match.get('external_entity_hit'),'rationale':match['rationale']})
            for match in n.get('review_matches',[]): assert match['gold_id'] in review
            fail = n['E']=='contradicted' or any(h['value']=='fail' for h in H)
            insufficient = n['L']!='ok' or n['E']=='unknown' or any(h['value']=='unknown' for h in H) or n['T'] in ('analogy_only','unknown')
            label = 'SURFACE_OR_CONSTRAINT_MISMATCH' if fail else 'INSUFFICIENT' if insufficient else 'CONDITIONAL_TRANSFER' if n['T']=='mapped' else 'DIRECT_DOCUMENTED'
            if n.get('expected_label'): assert label == n['expected_label'], (cid,n['rank'],label,n['expected_label'])
            date = n.get('date_status',c.get('date_status','unknown'))
            assert date in ('pre_decision','post_decision','unknown'), (cid,date)
            excluded = n.get('exclusion',False)
            useful = not gold and not excluded and label in ('DIRECT_DOCUMENTED','CONDITIONAL_TRANSFER')
            ids = [x['gold_id'] for x in gold] if not excluded else []
            evidence = [str(runpath.relative_to(ROOT))+'#/candidates/'+str(n['rank']-1),str(runpath.relative_to(ROOT))+'#/opened_documents'] + note.get('additional_evidence',[]) + n.get('additional_evidence',[])
            records.append({'case_id':cid,'baseline':baseline,'rank':n['rank'],'candidate_name':c['name'],'candidate_url':c['url'],
              'candidate_claim':c.get('reason',''),'gold_matches':gold,'match_rationale':n['match_rationale'],'review_matches':n.get('review_matches',[]),
              'L':n['L'],'E':n['E'],'E_reason':n.get('E_reason'),'H':H,'T':n['T'],'transfer_mapping':n.get('transfer_mapping'),
              'H_assessment_scope':n['scope'],'runtime_observation':'not_performed','label':label,
              'link_status':n['link_status'],'date_status':date,'run_reported_date_status':c.get('date_status','unknown'),
              'strict_historical_gold_ids':ids if date=='pre_decision' else [],
              'post_decision_gold_ids':ids if date=='post_decision' else [],'date_unknown_gold_ids':ids if date=='unknown' else [],
              'nongold_useful':useful,'nongold_historical_useful':useful and date=='pre_decision',
              'near_miss':label=='SURFACE_OR_CONSTRAINT_MISMATCH','broken_or_fake':n['link_status'] in ('http_404','http_410','wrong_target','fabricated'),
              'exclusion':excluded,'judge':note['judge'],'internal_separate_review':n.get('internal_review'),
              'evidence_locations':evidence,'remaining_check':n['remaining_check']})
    # Keep every required axis, match, date and judge in the main file. Repeated
    # explanations also remain verbatim in small, hash-checked per-run files.
    # This is a lossless serialization change, not a new judgment or run.
    expanded = ROOT/'evidence/judgments/expanded'
    expanded.mkdir(exist_ok=True)
    details, compact = [], []
    detail_only = {'candidate_claim','match_rationale','E_reason','transfer_mapping',
        'H_assessment_scope','runtime_observation','link_status',
        'internal_separate_review','evidence_locations','remaining_check'}
    for run in reviewed_runs:
        rows = [r for r in records if r['baseline']==run['baseline'] and r['case_id']==run['case_id']]
        path = expanded/(run['baseline']+'-'+run['case_id']+'.json')
        path.write_text(json.dumps({'case_id':run['case_id'],'baseline':run['baseline'],'judgments':rows},ensure_ascii=False,indent=2)+'\n')
        rel = str(path.relative_to(ROOT))
        details.append({'path':rel,'judgment_count':len(rows),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        for i, row in enumerate(rows):
            item = {k:v for k,v in row.items() if k not in detail_only}
            item['H'] = [{k:h[k] for k in ['constraint_id','value']} for h in row['H']]
            item['gold_matches'] = [{k:v for k,v in m.items() if k!='rationale'} for m in row['gold_matches']]
            item['details'] = rel+'#/judgments/'+str(i)
            compact.append(item)
    result = {'schema_version':'AF-RES-013-judgments-2','protocol_commit':'2b798c7d2b7355b649691c18de196104ceabb0f0','gold_commit':'f6f59a85949a001792b80260dd454c3fcc714a70',
      'method':'Explicit researcher coding of original candidate use; original run JSON is unchanged. Counts are document-author gold matches, not relevance completeness or demonstrated runtime utility.',
      'role_correction_ledger':'evidence/ROLE_CORRECTIONS.json; initial item identity remains frozen; one role corrected under unchanged SCOPE rule with original value retained',
      'details_contract':'Every candidate has L/E/H/T, label, judge, matches and temporal counts here. Its details JSON pointer resolves to the complete verbatim expanded judgment, including constraint text/reasons, remaining_check, evidence and review annotations. detail_shards are SHA-256 checked by validate_deliverables.py. No field or judgment was discarded.',
      'detail_only_fields':sorted(detail_only),'detail_shards':details,
      'reviewed_runs':reviewed_runs,'judgments':compact}
    (ROOT/'JUDGMENTS.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n')
    print(json.dumps({'reviewed_runs':len(reviewed_runs),'candidate_judgments':len(records),'labels':{k:sum(r['label']==k for r in records) for k in ['DIRECT_DOCUMENTED','CONDITIONAL_TRANSFER','SURFACE_OR_CONSTRAINT_MISMATCH','INSUFFICIENT']}},ensure_ascii=False))

if __name__=='__main__': build()
