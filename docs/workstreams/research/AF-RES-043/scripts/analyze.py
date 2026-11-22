"""Grade sealed observations, retain unknown criteria, and compute within-case pairs."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MISSING = "미확인"
NA = "해당 없음"
CONFIGS = ("B", "BL", "BX", "BLX")
COMPARISONS = (("B", "BL", "L"), ("BX", "BLX", "L"), ("B", "BX", "X"), ("BL", "BLX", "X"))


def jl(path):
    return [json.loads(s) for s in path.read_text().splitlines() if s.strip()]


def scalar(value):
    if isinstance(value,(dict,list,bool)):
        return json.dumps(value,ensure_ascii=False,sort_keys=True)
    return MISSING if value is None or value == "" else value


def csvout(path, rows):
    fields=list(rows[0])
    for row in rows:
        fields += [k for k in row if k not in fields]
    with path.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
        w.writeheader()
        for row in rows:w.writerow({k:scalar(row.get(k,MISSING)) for k in fields})


def main():
    cards={r['card_id']:r for r in jl(ROOT/'cards.jsonl')}
    key={r['case_id']:r for r in jl(ROOT/'key.jsonl')}
    seal=json.loads((ROOT/'evidence/read-seal.json').read_text())
    for name,digest in seal['file_sha256'].items():
        if name=='judgments.csv':
            continue  # Its unscored version remains at the phase-III remote commit.
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest, name
    original=[]
    for reader in ('reader_a','reader_b','reader_c'):
        original += jl(ROOT/'readers'/reader/'judgments.jsonl')
    original.sort(key=lambda r:(cards[r['card_id']]['presentation_index'],cards[r['card_id']]['task_order'].index(r['task'])))
    manual={r['judgment_id']:r for r in jl(ROOT/'evidence/adjudication.jsonl')}
    assert set(manual)=={r['judgment_id'] for r in original}
    judgments=[]
    for raw in original:
        j=dict(raw);c=cards[j['card_id']];k=key[j['case_id']];a=manual[j['judgment_id']];task=j['task']
        known=k[task+'_criterion_confirmed']
        assert a['criterion_confirmed']==known
        if not known:
            assert a['supported_correct']==MISSING
        j.update({
            'stratum':k['stratum'],'config':c['config'],
            'criterion_confirmed':known,'expected':k[task+'_expected'] if known else MISSING,
            'action_match':a['action_match'],'supported_correct':a['supported_correct'],
            'assessment_status':a['assessment_status'],'adjudication_reason':a['reason'],
            'criterion_url':k[task+'_criterion_url'],'criterion_locator':k[task+'_criterion_locator'],
            'adjudicator':'root; key-author; same-model-family unblinded self-audit',
            'adjudication_evidence_ids':a['evidence_ids'],
            'H_reconstructed_attained':a['H_reconstructed_attained'],
            'local_X_valid_redisplay':bool(j['local_x_displayed'] and k['X_available']),
            'sx_eligible':k['X_contains_version_or_url_cue'] is False,
            'si_eligible':k[task+'_independent_edition'] is True,
            'historical_strength_note':a['historical_strength_note'],
        })
        judgments.append(j)
    csvout(ROOT/'judgments.csv',judgments)
    by={(j['case_id'],j['task'],j['config']):j for j in judgments}
    pairs=[]
    for case in key:
        for task in ('C','H'):
            for left,right,element in COMPARISONS:
                l=by[case,task,left];r=by[case,task,right];known=l['criterion_confirmed']
                ls,rs=l['supported_correct'],r['supported_correct']
                resolved=known and l['assessment_status'] in ('correct','incorrect') and r['assessment_status'] in ('correct','incorrect')
                if not known:bucket='criterion_unknown'
                elif not resolved:bucket='hold_or_unverified'
                elif ls and rs:bucket='both_correct'
                elif ls:bucket='left_only'
                elif rs:bucket='right_only'
                else:bucket='both_incorrect'
                attainment_delta=int(rs)-int(ls) if known else MISSING
                hrec_known=task=='H' and key[case]['H_reconstructed_criterion_confirmed']
                hdelta=int(r['H_reconstructed_attained'])-int(l['H_reconstructed_attained']) if hrec_known else NA
                p={
                    'pair_id':f'{case}-{task}-{left}--{right}','case_id':case,'stratum':l['stratum'],'task':task,
                    'left_config':left,'right_config':right,'element_added':element,
                    'left_judgment_id':l['judgment_id'],'right_judgment_id':r['judgment_id'],
                    'total_slot_eligible':True,'criterion_confirmed':known,'both_resolvable':resolved,'exclusive_bucket':bucket,
                    'left_supported_correct':ls,'right_supported_correct':rs,'attainment_delta':attainment_delta,
                    'left_action_or_level':l['action'] if task=='C' else l['historical_level'],
                    'right_action_or_level':r['action'] if task=='C' else r['historical_level'],
                    'decision_changed':(l['action']!=r['action']) if task=='C' else (l['historical_level']!=r['historical_level']),
                    'publisher_open_delta':r['publisher_opens']-l['publisher_opens'],
                    'local_X_valid_delta':int(r['local_X_valid_redisplay'])-int(l['local_X_valid_redisplay']),
                    'normative_hold_left':task=='C' and l['action']=='보류' and l['supported_correct'] is True,
                    'normative_hold_right':task=='C' and r['action']=='보류' and r['supported_correct'] is True,
                    'left_hold_reason':l['hold_reason'],'right_hold_reason':r['hold_reason'],
                    'X_documentary_current_conflict':case=='J01' and task=='C' and element=='X',
                    'X_wrong_assertive_decision_observed':bool(task=='C' and element=='X' and known and r['assessment_status']=='incorrect' and r['action']!='보류'),
                    'causal_attribution_to_added_element':'미확인; same-reader order and retrieval-route differences remain',
                    'sx_eligible':l['sx_eligible'],'sx_bucket':bucket if l['sx_eligible'] else NA,
                    'si_eligible':l['si_eligible'],'si_bucket':bucket if l['si_eligible'] else NA,
                    'reconstructed_criterion_confirmed':hrec_known,
                    'reconstructed_attainment_delta':hdelta,
                    'L_kind':key[case]['L_kind'],'L_version_pinned':key[case]['L_version_pinned'],
                    'criterion_url':l['criterion_url'],'criterion_locator':l['criterion_locator'],
                    'evidence_ids':[l['judgment_id'],r['judgment_id']]+l['read_ids']+r['read_ids'],
                }
                pairs.append(p)
    assert len(pairs)==64
    csvout(ROOT/'pairs.csv',pairs)
    summaries=[]
    for sensitivity in ('original','S-X','S-I'):
        for stratum in ('natural','correction_first'):
            for task in ('C','H'):
                for left,right,element in COMPARISONS:
                    allp=[p for p in pairs if p['stratum']==stratum and p['task']==task and p['left_config']==left and p['right_config']==right]
                    chosen=[p for p in allp if sensitivity=='original' or p['sx_eligible' if sensitivity=='S-X' else 'si_eligible']]
                    buckets=Counter(p['exclusive_bucket'] for p in chosen)
                    nknown=sum(p['criterion_confirmed'] for p in chosen)
                    gains=[p['case_id'] for p in chosen if p['attainment_delta']==1]
                    losses=[p['case_id'] for p in chosen if p['attainment_delta']==-1]
                    summaries.append({
                        'sensitivity':sensitivity,'stratum':stratum,'task':task,'comparison':left+'↔'+right,'element_added':element,
                        'original_slots':len(allp),'selected_slots':len(chosen),'criterion_confirmed_n':nknown,'both_resolvable_n':sum(p['both_resolvable'] for p in chosen),
                        **{x:buckets[x] for x in ('both_correct','left_only','right_only','both_incorrect','hold_or_unverified','criterion_unknown')},
                        'left_attained':sum(p['left_supported_correct'] is True for p in chosen),
                        'right_attained':sum(p['right_supported_correct'] is True for p in chosen),
                        'attainment_gain_cases':gains,'attainment_loss_cases':losses,
                        'gain_fraction':f'{len(gains)}/{nknown}' if nknown else NA,
                        'L_without_X_sufficient': [p['case_id'] for p in chosen if element=='L' and left=='B' and p['right_supported_correct'] is True],
                        'X_wrong_assertive_case_ids':[p['case_id'] for p in chosen if p['X_wrong_assertive_decision_observed']],
                        'pair_ids':[p['pair_id'] for p in chosen],
                    })
    config_summary=[]
    for stratum in ('natural','correction_first'):
        for task in ('C','H'):
            for config in CONFIGS:
                js=[j for j in judgments if j['stratum']==stratum and j['task']==task and j['config']==config]
                eligible=[j for j in js if j['criterion_confirmed']]
                config_summary.append({'stratum':stratum,'task':task,'config':config,'slots':len(js),'criterion_n':len(eligible),
                    'supported_correct_n':sum(j['supported_correct'] is True for j in eligible),
                    'success_fraction':f"{sum(j['supported_correct'] is True for j in eligible)}/{len(eligible)}" if eligible else NA,
                    'unknown_criterion_n':len(js)-len(eligible),
                    'raw_publisher_matches':sum(j['historical_level']=='publisher_edition_match' for j in js),
                    'reconstructed_matches':sum(j['H_reconstructed_attained'] is True for j in js),
                    'reconstructed_eligible_n':sum(key[j['case_id']]['H_reconstructed_criterion_confirmed'] for j in js) if task=='H' else NA,
                    'valid_local_X_displays':sum(j['local_X_valid_redisplay'] for j in js)})
    reads=[r for reader in ('reader_a','reader_b','reader_c') for r in jl(ROOT/'readers'/reader/'reads.jsonl')]
    publisher=[r for r in reads if r['mode']=='publisher_open']
    failures=[r for r in publisher if 'fail' in str(r['outcome']).lower() or r['outcome'] in ('error','access_failure','unavailable')]
    summary={
        'phase_iii_commit':'6c58c98d60351b9b125a8611887fec0972aeae1f','input_key_sha256':hashlib.sha256((ROOT/'key.jsonl').read_bytes()).hexdigest(),
        'cards':len(cards),'judgments':len(judgments),'pairs':len(pairs),'reads':len(reads),'publisher_opens':len(publisher),
        'publisher_failures':len(failures),'publisher_outcome_counts':dict(Counter(str(r['outcome']) for r in publisher)),
        'local_X_events':sum(r['mode']=='local_X' for r in reads),'valid_X_displays_C_H':sum(j['local_X_valid_redisplay'] for j in judgments),
        'valid_X_displays_H':sum(j['local_X_valid_redisplay'] for j in judgments if j['task']=='H'),
        'H_raw_level_counts':dict(Counter(j['historical_level'] for j in judgments if j['task']=='H')),
        'C_raw_action_counts':dict(Counter(j['action'] for j in judgments if j['task']=='C')),
        'C_supported_n':sum(j['supported_correct'] is True for j in judgments if j['task']=='C'),
        'C_criterion_n':sum(j['criterion_confirmed'] for j in judgments if j['task']=='C'),
        'strict_H_supported_n':sum(j['supported_correct'] is True for j in judgments if j['task']=='H'),
        'strict_H_criterion_n':sum(j['criterion_confirmed'] for j in judgments if j['task']=='H'),
        'config_summary':config_summary,'pair_summary':summaries,
    }
    (ROOT/'evidence/analysis-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'evidence/scored-judgments.jsonl').write_text(''.join(json.dumps(j,ensure_ascii=False)+'\n' for j in judgments))
    print(json.dumps({k:v for k,v in summary.items() if k not in ('config_summary','pair_summary')},ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
