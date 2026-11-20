"""Aggregate explicit judgments; no automatic relevance or entity inference.

Gold hits are distinct case/item pairs. Candidate quality remains candidate-level.
Temporal eligibility and exposed runs are separate sensitivity views.
"""
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROLES = ['같은 목적 완성품','재사용 부품','같은 분야의 다른 설계','다른 언어·생태계','다른 분야 원리','표준·논문']
LABELS = ['DIRECT_DOCUMENTED','CONDITIONAL_TRANSFER','SURFACE_OR_CONSTRAINT_MISMATCH','INSUFFICIENT']

def instant(value):
    return datetime.fromisoformat(value.replace(' UTC','+00:00').replace('Z','+00:00'))

def main():
    cases = json.loads((ROOT/'cases/CASES.json').read_text())['cases']
    jd = json.loads((ROOT/'JUDGMENTS.json').read_text())
    rows = jd['judgments']
    reviewed = {(r['baseline'],r['case_id']) for r in jd['reviewed_runs']}
    gold = {(c['id'],g['id']):g for c in cases for g in c['gold_items']}
    out = {'schema_version':1,'gold_items':len(gold),'case_count':len(cases),
           'units':{'hits':'distinct case/gold-item pairs','quality':'candidate rows; not distinct deployed solutions',
                    'identity_hits':'all dates, excluded candidates removed','historical_hits':'same identity with verified pre-decision evidence',
                    'clean_subset':'runs with no recorded exposure of any kind, a conservative reported-exposure sensitivity'},
           'baselines':{},'cases':[],'families':{},'roles':{},'match_kinds':{},'pending':[]}

    def hits(rs, field='gold_matches'):
        if field=='gold_matches':
            return {(r['case_id'],g['gold_id']) for r in rs if not r['exclusion'] for g in r[field]}
        return {(r['case_id'],g) for r in rs if not r['exclusion'] for g in r[field]}

    for b in ['A','B']:
        rs=[r for r in rows if r['baseline']==b]
        runs={c['id']:json.loads((ROOT/'runs'/b/(c['id']+'.json')).read_text()) for c in cases if (ROOT/'runs'/b/(c['id']+'.json')).exists()}
        covered={cid for bb,cid in reviewed if bb==b}
        complete=set(runs)==covered=={c['id'] for c in cases}
        ih=hits(rs); hh=hits(rs,'strict_historical_gold_ids')
        post=hits(rs,'post_decision_gold_ids'); unknown=hits(rs,'date_unknown_gold_ids')
        clean={cid for cid,r in runs.items() if not r.get('exposures')}
        eligible_gold={x for x in gold if x[0] in covered}
        nongold=[r for r in rs if not r['gold_matches'] and not r['exclusion']]
        useful=[r for r in rs if r['nongold_useful']]
        huseful=[r for r in rs if r['nongold_historical_useful']]
        raw_historical={(r['case_id'],g['gold_id']) for r in rs if not r['exclusion'] and r['run_reported_date_status']=='pre_decision' for g in r['gold_matches']}
        out['baselines'][b]={
          'complete_all_cases':complete,'run_count':len(runs),'judged_run_count':len(covered),
          'candidate_count':len(rs),'raw_candidate_count':sum(len(r['candidates']) for r in runs.values()),
          'gold_denominator':len(eligible_gold),'identity_hit_count':len(ih),'historical_hit_count':len(hh),
          'post_decision_hit_count':len(post),'date_unknown_hit_count':len(unknown),
          'post_only_hit_count':len(post-hh),'unknown_only_hit_count':len(unknown-hh-post),
          'cases_with_identity_hit':len({x[0] for x in ih}),'cases_with_historical_hit':len({x[0] for x in hh}),
          'labels':dict(Counter(r['label'] for r in rs)),
          'candidate_dates':dict(Counter(r['date_status'] for r in rs)),
          'nongold_candidates_judged':len(nongold),'nongold_useful':len(useful),
          'nongold_historical_useful':len(huseful),'cases_with_nongold_useful':len({r['case_id'] for r in useful}),
          'cases_with_nongold_historical_useful':len({r['case_id'] for r in huseful}),
          'nongold_useful_with_narrowed_H':sum(any(h['value']=='not_in_scope' for h in r['H']) for r in useful),
          'nongold_useful_all_H_pass':sum(all(h['value']=='pass' for h in r['H']) for r in useful),
          'nongold_useful_labels':dict(Counter(r['label'] for r in useful)),
          'near_miss':sum(r['near_miss'] for r in rs),'broken_or_fake':sum(r['broken_or_fake'] for r in rs),
          'non_ok_L':sum(r['L']!='ok' for r in rs),'exposed_run_count':sum(bool(r.get('exposures')) for r in runs.values()),
          'exposure_records':sum(len(r.get('exposures',[])) for r in runs.values()),
          'clean_subset':{'cases':len(clean & covered),'gold_denominator':sum(cid in clean for cid,g in eligible_gold),
                          'identity_hits':sum(cid in clean for cid,g in ih),'historical_hits':sum(cid in clean for cid,g in hh)},
          'date_review_changes':sum(r['date_status']!=r['run_reported_date_status'] for r in rs),
          'historical_hits_using_original_run_dates':len(raw_historical),
          'judges':dict(Counter(r['judge'] for r in rs)),
          'candidate_count_range':[min((len(r['candidates']) for r in runs.values()),default=0),max((len(r['candidates']) for r in runs.values()),default=0)],
          'query_count_range':[min((r['budget']['search_queries'] for r in runs.values()),default=0),max((r['budget']['search_queries'] for r in runs.values()),default=0)],
          'opened_budget_range':[min((r['budget']['opened_pages'] for r in runs.values()),default=0),max((r['budget']['opened_pages'] for r in runs.values()),default=0)],
          'first_start_utc':min((instant(r['started_at_utc']) for r in runs.values()),default=None).isoformat() if runs else None,
          'last_end_utc':max((instant(r['ended_at_utc']) for r in runs.values()),default=None).isoformat() if runs else None,
          'identity_hits':sorted([list(x) for x in ih]),'historical_hits':sorted([list(x) for x in hh])}
        out['pending'] += [{'baseline':b,'case_id':c['id'],'run_exists':c['id'] in runs,'judgments_exist':c['id'] in covered} for c in cases if c['id'] not in covered]

    for c in cases:
        cg={g['id'] for g in c['gold_items']}
        item={'case_id':c['id'],'family':c['family'],'url':c['url'],'decision_date':c['decision_date'],
              'gold_count':len(cg),'roles':dict(Counter(g['role'] for g in c['gold_items'])),'baselines':{}}
        for b in ['A','B']:
            rs=[r for r in rows if r['case_id']==c['id'] and r['baseline']==b]
            ih={g for cid,g in hits(rs)}; hh={g for cid,g in hits(rs,'strict_historical_gold_ids')}
            runfile=ROOT/'runs'/b/(c['id']+'.json'); run=json.loads(runfile.read_text()) if runfile.exists() else {}
            item['baselines'][b]={'judged':(b,c['id']) in reviewed,'candidate_count':len(rs),'identity_hits':sorted(ih),'historical_hits':sorted(hh),
               'post_decision_hits':sorted(g for cid,g in hits(rs,'post_decision_gold_ids')),'date_unknown_hits':sorted(g for cid,g in hits(rs,'date_unknown_gold_ids')),
               'missed_identity':sorted(cg-ih),'missed_historical':sorted(cg-hh),
               'nongold_count':sum(not r['gold_matches'] for r in rs),'nongold_useful':sum(r['nongold_useful'] for r in rs),
               'nongold_historical_useful':sum(r['nongold_historical_useful'] for r in rs),
               'near_miss':sum(r['near_miss'] for r in rs),'broken_or_fake':sum(r['broken_or_fake'] for r in rs),
               'exposure_records':len(run.get('exposures',[])),'candidate_dates':dict(Counter(r['date_status'] for r in rs)),
               'insufficient':sum(r['label']=='INSUFFICIENT' for r in rs),'judge':sorted({r['judge'] for r in rs})}
        out['cases'].append(item)

    for dim, values, getter in [('roles',ROLES,lambda c,g:g['role']),
          ('families',sorted({c['family'] for c in cases}),lambda c,g:c['family']),
          ('match_kinds',['external_entity','structural_design'],lambda c,g:g['match_kind'])]:
        for value in values:
            universe={(c['id'],g['id']) for c in cases for g in c['gold_items'] if getter(c,g)==value}
            ent={'gold_count':len(universe),'case_count':len({cid for cid,g in universe}),'baselines':{}}
            for b in ['A','B']:
                rs=[r for r in rows if r['baseline']==b]; ih=hits(rs)&universe; hh=hits(rs,'strict_historical_gold_ids')&universe
                ent['baselines'][b]={'identity_hits':len(ih),'historical_hits':len(hh),
                  'identity_ratio':len(ih)/len(universe) if universe else None,'historical_ratio':len(hh)/len(universe) if universe else None,
                  'missed_identity_case_ids':sorted({cid for cid,g in universe-ih})}
            out[dim][value]=ent

    ihA={tuple(x) for x in out['baselines']['A']['identity_hits']}; ihB={tuple(x) for x in out['baselines']['B']['identity_hits']}
    hhA={tuple(x) for x in out['baselines']['A']['historical_hits']}; hhB={tuple(x) for x in out['baselines']['B']['historical_hits']}
    out['union']={'identity_hits':len(ihA|ihB),'historical_hits':len(hhA|hhB),'identity_overlap':len(ihA&ihB),'historical_overlap':len(hhA&hhB),
      'A_only_identity':len(ihA-ihB),'B_only_identity':len(ihB-ihA),'A_only_historical':len(hhA-hhB),'B_only_historical':len(hhB-hhA)}
    out['original_thirty_sensitivity']={'excluded_case':'C31','reason':'Documented eligibility-segmentation repair added C31 before gold publication, after some original-prefix A runs had started.',
      'gold_denominator':sum(cid!='C31' for cid,g in gold),
      'A_identity_hits':sum(cid!='C31' for cid,g in ihA),'B_identity_hits':sum(cid!='C31' for cid,g in ihB),
      'A_historical_hits':sum(cid!='C31' for cid,g in hhA),'B_historical_hits':sum(cid!='C31' for cid,g in hhB)}
    without_jed=[r for r in rows if r['baseline']=='B' and not (r['case_id']=='C20' and r['rank']==5)]
    out['mechanism_match_sensitivity']={'reason':'SCOPE allows the same explicit mechanism, but Jed is not GNU gettext project identity. Keep that match basis visible.',
      'B_without_Jed_mechanism_hit':{'identity_hits':len(hits(without_jed)), 'historical_hits':len(hits(without_jed,'strict_historical_gold_ids')),'gold_denominator':len(gold)},
      'affected_candidate':'B-C20-r5','main_match_basis':'same_explicit_mechanism','main_external_entity_identity':False}
    out['role_correction_sensitivity']={'original_gold_commit':'f6f59a85949a001792b80260dd454c3fcc714a70','original_distant_items':0,
      'corrected_distant_items':sum(g['role']=='다른 분야 원리' for g in gold.values()),'gold_denominator':len(gold),
      'broad_boundary_including_PySizer':2,'role_correction_ledger':'evidence/ROLE_CORRECTIONS.json',
      'items_added_or_removed':0,'rule_changed':False}
    out['review_pool']={'raw_extra_entries':sum(len(c.get('review_gold_items',[])) for c in cases),'distinct_novel_entries':6,
      'expanded_denominator':len(gold)+6,'deduplication':'R0123-RV05 DRF aliases primary DataRaceFree; no extra denominator item',
      'hit_rows':[{'case_id':r['case_id'],'baseline':r['baseline'],'rank':r['rank'],'matches':r['review_matches'],'date_status':r['date_status']} for r in rows if r['review_matches']]}
    (ROOT/'evidence/AGGREGATES.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'cases':len(cases),'gold':len(gold),'pending_runs':len(out['pending']),
        'baselines':{b:{k:v for k,v in s.items() if k not in ['identity_hits','historical_hits']} for b,s in out['baselines'].items()}},ensure_ascii=False))

if __name__=='__main__':main()
