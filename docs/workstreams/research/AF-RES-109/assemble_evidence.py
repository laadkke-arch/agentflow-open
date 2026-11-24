#!/usr/bin/env python3
"""Rebuild adjudicated ledgers from the immutable search seal and reader records.

This does not run searches or candidate experiments. It never modifies raw arm files.
Only the AF-RES-109 directory is an output destination.
"""
import csv
import hashlib
import io
import json
import pathlib
import subprocess
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PREFIX = 'docs/workstreams/research/AF-RES-109/'
SEARCH_SEAL = '628e33709b0be7a19486f1bfeaef93f42e129394'

def jl(path):
    return [json.loads(s) for s in pathlib.Path(path).read_text().splitlines() if s.strip()]

def frozen(path):
    return subprocess.check_output(['git','show',f'{SEARCH_SEAL}:{PREFIX}{path}'], cwd=REPO).decode()

def dumpj(path, rows):
    path.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))

def dumpcsv(path, rows, fields=None):
    fields = fields or list(rows[0])
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fields,lineterminator='\n'); w.writeheader(); w.writerows(rows)

def value(v):
    return json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else ('' if v is None else v)

def main():
    candidates=list(csv.DictReader(io.StringIO(frozen('candidates.csv'))))
    original_fields=list(candidates[0])
    requests={r['id']:r for r in jl(ROOT/'requests.jsonl')}
    mapping=json.loads((ROOT/'evidence/blind-id-map.json').read_text())
    candidate_to_variant={x['candidate_id']:x['variant_id'] for x in mapping}
    judgments={}
    for part in ['r1-r3','r4-r6']:
        for r in jl(ROOT/f'evidence/blind/{part}/judgments.jsonl'):
            assert r['variant_id'] not in judgments
            r['_reader_group']=part
            judgments[r['variant_id']]=r
    assert len(judgments)==len(candidate_to_variant)==33

    audit=json.loads((ROOT/'evidence/audit/execution-audit.json').read_text())
    pairs={p['request_id']:p for p in audit['pairs']}
    cost_by_arm={a['arm_id']:a for a in audit['arms']}
    choices=[]
    source_links={}
    updates=[]
    forms={
      'R1-A-1':'단일 기능','R1-A-2':'동종 부품','R1-B-1':'단일 기능','R1-B-2':'동종 부품',
      'R2-A-1':'단일 기능','R2-A-2':'단일 기능','R2-A-3':'단일 기능',
      'R2-B-1':'단일 기능','R2-B-2':'동종 부품','R2-B-3':'동종 부품',
      'R3-A-1':'동종 부품','R3-A-2':'단일 기능','R3-B-1':'단일 기능','R3-B-2':'단일 기능','R3-B-3':'동종 부품',
      'R4-A-1':'동종 부품','R4-A-2':'단일 기능','R4-A-3':'동종 부품','R4-B-1':'동종 부품','R4-B-2':'단일 기능','R4-B-3':'단일 기능',
      'R5-A-1':'동종 부품','R5-A-2':'동종 부품','R5-A-3':'단일 기능','R5-B-1':'동종 부품','R5-B-2':'동종 부품','R5-B-3':'동종 부품',
      'R6-A-1':'동종 부품','R6-A-2':'동종 부품','R6-A-3':'단일 기능','R6-B-1':'동종 부품','R6-B-2':'동종 부품','R6-B-3':'단일 기능',
    }
    for c in candidates:
        cid=c['candidate_id']; rid=c['request_id']; aid=rid+'-'+c['arm']; rank=int(c['returned_rank'])
        a=pairs[rid]['arms'][aid]
        prefix='eligible' if rank in a['unambiguous_eligible_ranks'] else ('indeterminate' if rank in a['indeterminate_ranks'] else 'excluded')
        c.update(adjudication_source='',adjudicated_form='공석',source_relation='vacancy',
                 historical_judgment='',common_prefix_status=prefix,
                 strict_comparison_eligible='False',strict_full_solution='False',
                 original_discussion_blind='False' if rid=='R6' else 'True',
                 method_rank_blind='True',source_verified_for_candidate='False',
                 conditional_target_fit='vacancy',root_interpretation='',
                 new_implementation_flag='0',new_test_flag='0',choice_key='',test_key='',
                 source_verification_ids='',postsearch_counter_source=f'COUNTER-{rid}-'+{'R1':'GETTEXT','R2':'PLAYWRIGHT','R3':'KUBERNETES','R4':'QT','R5':'CYTOSCAPE','R6':'UIEVENTS'}[rid])
        if cid not in candidate_to_variant:
            assert c['return_state']=='vacant'
            c.update(fit_condition_1='vacancy',fit_condition_2='vacancy',lineage_id='vacancy',judgment='공석 유지',novelty_class='vacancy',judgment_reason=c['vacancy_reason'])
            continue
        j=judgments[candidate_to_variant[cid]]; group=j['_reader_group']
        sid_prefix='BLIND13-' if group=='r1-r3' else 'BLIND46-'
        verification=[sid_prefix+s for s in j['source_ids']]
        hist=j['historical_availability']
        historical_status=hist.get('status') or hist.get('candidate_edition','unknown')
        c.update(fit_condition_1=j['condition1'],fit_condition_2=j['condition2'],
                 lineage_id=j['lineage_key'],judgment=j['decision'],novelty_class=j['novelty_class'],
                 judgment_reason=j['why'],blind_id=j['variant_id'],adjudication_source=f'evidence/blind/{group}/judgments.jsonl#{j["variant_id"]}',
                 adjudicated_form=forms[cid],source_relation='same_product_or_near_software_domain',
                 historical_judgment=value(hist),new_implementation_flag=str(j['new_implementation_count']),
                 new_test_flag=str(j['new_test_count']),choice_key=j.get('choice_key') or '',test_key=j.get('test_key') or '',
                 source_verified_for_candidate=str(cid!='R2-B-3'),
                 conditional_target_fit='conditional' if 'partial' in [j['condition1'],j['condition2']] else ('near_miss' if 'no' in [j['condition1'],j['condition2']] else 'source_contract_only'),
                 source_verification_ids=value(verification))
        if cid in ['R5-B-2','R5-B-3']:
            c['conditional_target_fit']='same_pair_interpretation_only'
            c['root_interpretation']='Blind reader yes/yes applies only to repeated same-endpoint pairs. Original image/topology is unresolved; no unqualified whole-request success. Raw judgments retained.'
            updates.append(dict(candidate_id=cid,field='unqualified_full_fit',earlier='blind yes/yes under same-pair reading',final='conditional, original topology unresolved',basis='counterchecks.csv:R5; blind review itself scopes the same-pair interpretation',changed_by='root after blind review'))
        if rid=='R6':
            c['root_interpretation']+=' All final R6 judgments postdate the reader outcome exposure; descriptive provisional counts only.'
        if cid=='R2-B-3':
            updates.append(dict(candidate_id=cid,field='accepted_comparator',earlier='search arm claims operative source read',final='hold; independent operative-source acquisition failed; implementation/test flags0',basis='BLIND13-S05; evidence/blind/r1-r3/review.md',changed_by='blind_r1_r3'))
        choice=dict(candidate_id=cid,request_id=rid,arm=c['arm'],returned_rank=c['returned_rank'],
                    blind_variant_id=j['variant_id'],source_url=c['url'],source_ids=value(verification),
                    old_approach=requests[rid]['known_baseline'],
                    changed_unit_order_responsibility=c['changed_choice'],
                    preserved_condition_1=requests[rid]['condition_1'],preserved_condition_2=requests[rid]['condition_2'],
                    minimum_input=j.get('proposed_test_input') or c['minimal_discriminating_input'],
                    expected_output=j.get('proposed_expected_output') or c['expected_output'],
                    broken_source_assumption=j['counterexample'],
                    source_clause=j['exact_section'],
                    condition_1_fit=j['condition1'],condition_2_fit=j['condition2'],
                    conditional_target_fit=c['conditional_target_fit'],
                    novelty_class=j['novelty_class'],new_implementation_flag=j['new_implementation_count'],
                    new_test_flag=j['new_test_count'],choice_key=j.get('choice_key') or '',test_key=j.get('test_key') or '',
                    current_eligibility='provisional_exposed_reader' if rid=='R6' else 'conditional_source_based',
                    historical_status=historical_status,historical_basis=value(hist),
                    common_prefix_status=prefix,strict_comparison_eligible=False,
                    method_rank_blind=True,original_discussion_blind=(rid!='R6'),
                    natural_input=True,test_input_kind='researcher_proposed_synthetic_or_diagnostic',
                    experiment_executed=False,observed_application_result='미확인',
                    author_awareness='사전 목록에 없음만 판정; 원 개발자 미인지 미확인',
                    new_distant_domain_principle=False,
                    counter_source_id=c['postsearch_counter_source'],next_observation=j['minimal_next_observation'])
        choices.append(choice)
        for sid in j['source_ids']:source_links.setdefault((group,sid),set()).add(cid)
    dumpcsv(ROOT/'candidates.csv',candidates)
    dumpcsv(ROOT/'choices.csv',choices)
    dumpj(ROOT/'evidence/adjudication-changes.jsonl',updates)

    # Keep all source reads; allocate primary counts only once by audited work genealogy.
    original_sources=[json.loads(s) for s in frozen('sources.jsonl').splitlines() if s.strip()]
    sources=original_sources[:]
    accounting=json.loads((ROOT/'evidence/source-accounting.json').read_text())
    families={sid:entry for entry in accounting['families'] for sid in entry['source_ids']}
    preferred={entry['credited_source_id'] for entry in accounting['families'] if entry.get('credited_source_id')}
    for raw in jl(ROOT/'evidence/search-sources-unadjudicated.jsonl'):
        r=dict(raw);sid=r['source_id'];entry=families[sid]
        r['arm_claimed_unique_primary']=r.get('counts_as_unique_primary')
        r['arm_original_work_id']=r.get('original_work_id')
        r['original_work_id']=entry['work_id']
        r['counts_as_unique_primary']=sid in preferred
        r['count_category']='search_returned' if sid in preferred else 'search_read_not_additional_primary'
        r['count_reason']=entry['reason']
        r['reopened_or_same_work']=not r['counts_as_unique_primary']
        r['phase']='sealed_search'
        r['discovery_credit']=sid in preferred
        sources.append(r)
    for group in ['r1-r3','r4-r6']:
        sid_prefix='BLIND13-' if group=='r1-r3' else 'BLIND46-'
        for raw in jl(ROOT/f'evidence/blind/{group}/sources.jsonl'):
            r=dict(raw); oldid=r['source_id'];r['source_id']=sid_prefix+oldid
            r['reader_record_id']=oldid;r['source_record']=f'evidence/blind/{group}/sources.jsonl'
            r['reader_questions']=r.get('questions',[])
            r['questions']=['Q4','Q5','Q6']
            r['linked_candidates']=sorted(source_links.get((group,oldid),set()))
            r['phase']='postsearch_blind_verification';r['discovery_credit']=False
            r['counts_as_unique_primary']=False
            r['limits']=r.get('limits') or r.get('limitations') or '未確認 / not provided in reader record'
            sources.append(r)
    for r in jl(ROOT/'evidence/postsearch/sources.jsonl'):sources.append(r)
    if (ROOT/'evidence/postsearch/root-rereads.jsonl').exists():
        sources.extend(jl(ROOT/'evidence/postsearch/root-rereads.jsonl'))
    for raw in jl(ROOT/'evidence/aftermath/sources.jsonl'):
        r=dict(raw)
        r['source_id']=r['source_id'] if r['source_id'].startswith('AFTER-') else 'AFTER-'+r['source_id']
        r['actual_url']=r.get('actual_url') or r.get('arrived_url')
        # A failed endpoint has no observed destination; retain null.
        r['edition']=r.get('edition') or r.get('version_date','未確認')
        r['direct_read_utc']=r.get('direct_read_utc') or r.get('read_utc')
        r['limits']=r.get('limits') or r.get('limitations','未確認')
        r['counter_observation']=r.get('counter_observation') or r.get('counter_observations','未確認')
        r.setdefault('published_utc', None)
        r['questions']=['Q7'];r['counts_as_unique_primary']=False;r['count_category']='same_episode_aftermath'
        r['reader']=r.get('reader','execution_audit post-search phase')
        r['phase']='postsearch_aftermath';r['discovery_credit']=False
        sources.append(r)
    ids=[r['source_id'] for r in sources];assert len(ids)==len(set(ids))
    dumpj(ROOT/'sources.jsonl',sources)
    after=list(csv.DictReader((ROOT/'evidence/aftermath/aftermath.csv').open()))
    dumpcsv(ROOT/'aftermath.csv',after)

    costrows=[]
    for a in audit['arms']:
        aid=a['arm_id'];rid,arm=aid.split('-'); obs=a['observed'];p=pairs[rid]
        rr=json.loads((ROOT/f'evidence/search/{aid}/returns.json').read_text())
        prefix=p['arms'][aid]
        own=[r for r in choices if r['request_id']==rid and r['arm']==arm]
        prefixrows=[r for r in own if r['common_prefix_status']=='eligible']
        count=lambda rs,flag,key:len({r[key] for r in rs if int(r[flag]) and r[key]})
        costrows.append(dict(request_id=rid,arm=arm,queries=rr['actual_queries'],explicit_opens=rr['actual_explicit_opens'],
                             final_links=len(own),vacancies=3-len(own),start_utc=a['start_utc'],end_utc=a['end_utc'],
                             wall_seconds=a['wall_seconds'],automatic_reads='미확인',tokens='미확인',money='미확인',
                             common_cap_queries=p['common_caps']['queries'],common_cap_explicit_opens=p['common_caps']['explicit_opens'],
                             common_eligible_ranks=value(prefix['unambiguous_eligible_ranks']),
                             common_indeterminate_ranks=value(prefix['indeterminate_ranks']),
                             full_unique_choices=count(own,'new_implementation_flag','choice_key'),
                             full_unique_tests=count(own,'new_test_flag','test_key'),
                             common_acquired_choice_keys=count(prefixrows,'new_implementation_flag','choice_key'),
                             common_acquired_test_keys=count(prefixrows,'new_test_flag','test_key'),
                             common_result_semantics='acquisition eligibility only; not a shortened-budget rerun or proof of proposal formulation at cutoff',
                             strict_comparison_eligible=False))
    dumpcsv(ROOT/'costs.csv',costrows)
    print(json.dumps({'candidate_slots':len(candidates),'choices_rows':len(choices),'source_rows':len(sources),'cost_rows':len(costrows),'aftermath_rows':len(after)},ensure_ascii=False))

if __name__=='__main__':main()
