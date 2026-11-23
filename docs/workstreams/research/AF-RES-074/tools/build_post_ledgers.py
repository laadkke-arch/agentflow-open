#!/usr/bin/env python3
"""Normalize sealed research ledgers; retain post-adjudication changes explicitly."""
import collections
import csv
import json
from pathlib import Path

P = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((P / path).read_text())
def lines(path):
    return [json.loads(s) for s in (P / path).read_text().splitlines()]
def dump(path, value):
    (P / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
def writecsv(path, rows):
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with (P / path).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=keys, lineterminator='\n')
        w.writeheader()
        for row in rows:
            w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict, bool)) or v is None else v for k, v in row.items()})

packets = {p['case_id']: p for p in lines('packets.jsonl')}
policy_rows = list(csv.DictReader((P / 'policies.csv').open()))
policy = {p['row_id']: p for p in policy_rows}
panpost = {r['case_id']:r for r in read('streams/pandoc/post-analysis.json')}
roottech = {r['source_id']:r for r in read('evidence/root-technical-review.json')['rows']}
initial_review={r['case_id']:r for r in csv.DictReader((P/'initial-version-review.csv').open())} if (P/'initial-version-review.csv').exists() else {}
fixed_run=read('evidence/pandoc-fixed-run.json') if (P/'evidence/pandoc-fixed-run.json').exists() else None

# Source counts use conservative document genealogies, not file/function counts.
sources = []
for domain, files in [('pandoc',['sources.jsonl','sources-extension.jsonl','sources-opening-retry.jsonl']), ('gdal',['sources-pre.jsonl','sources-post.jsonl','sources-extension.jsonl','sources-initial-recovery.jsonl']), ('crossfield',['sources.jsonl'])]:
    for fn in files:
        if not (P/f'streams/{domain}/{fn}').exists(): continue
        for r in lines(f'streams/{domain}/{fn}'):
            if domain == 'pandoc':
                s = dict(source_id=r['source_id'], work_id=r['work_id'], original_url=r['original_url'], arrival_url=r['arrived_url'], author_publisher=r['publisher'], version_time=r['version_time'], checked_utc=r['checked_utc'], read_location=r['direct_location'], confirmed_content=r['confirmed_content'], supports_q=r['supports_q'], claim_ids=r['claim_ids'], limitations=r['limits_counterevidence'], counterevidence=r['limits_counterevidence'], access_status=r['access_status'], direct_read=r['access_status']=='read_full_target_sections', minimum_count=r['minimum_count'], minimum_category=r['category'], minimum_count_reason=r['minimum_count_reason'], phase=r['phase'])
            elif domain == 'gdal':
                sid=r['source_id']
                cat = ('request' if sid.startswith('GDAL-I') else 'test_example' if sid.startswith('GDAL-TEST') else 'spec_manual' if sid.startswith(('GDAL-DOC','GDAL-SPEC','GDAL-COMMIT')) else 'code' if sid.startswith(('GDAL-API','GDAL-CODE')) else 'event' if 'COMMENT' in sid else 'access' if 'ARCHIVE' in sid else 'fixture')
                s = dict(source_id=sid, work_id=r['independent_work_id'], original_url=r['original_url'], arrival_url=r['arrival_url'], author_publisher=f"{r.get('author','')} / {r['publisher']}", version_time=r['version'], checked_utc=r['checked_utc'], read_location=r['read_location'], confirmed_content=r['confirmed'], supports_q=r['supports'], claim_ids=[sid+'-claim'], limitations=r['limitations'], counterevidence=r['counterevidence'], access_status=r['access_status'], direct_read=r['access_status'].startswith('direct_original'), minimum_count=r['counted'], minimum_category=cat, minimum_count_reason=r['count_reason'], phase=r['stratum'])
                if sid.startswith('GDAL-DOC'):
                    s['stream_work_id'] = s['work_id']
                    s['work_id'] = 'OSGeo/gdal:official-user-manual'
                    s['minimum_count_reason'] += '; root groups all GDAL user manual pages/versions as one work'
            else:
                s = dict(source_id=r['source_id'], work_id=r['work_id'], original_url=r['original_url'], arrival_url=r['arrival_url'], author_publisher=r['author_publisher'], version_time=r['version_or_date'], checked_utc=r['checked_utc'], checked_utc_meaning=r.get('checked_utc_meaning'), read_location=r['read_sections'], confirmed_content=r['confirmed_content'], supports_q=r['supports_questions'], claim_ids=r['claim_ids'], limitations=r['limitations'], counterevidence=r['counterevidence'], access_status=r['access_status'], direct_read=r['direct_read'], minimum_count=r['count_for_minimum'], minimum_category='crossfield_procedure', minimum_count_reason=r['minimum_reason'], phase=r['layer'])
            s['source_stream'] = f'streams/{domain}/{fn}'
            if domain=='pandoc' and r['access_status']=='opened_event_recovered_direct':s['direct_read']=True
            if domain=='gdal' and r['access_status'].startswith('direct_'):s['direct_read']=True
            s['reviewer'] = domain + ' model'
            s['direct_independent_work'] = bool(s['minimum_count'])
            if s['minimum_category'] == 'code':
                s['minimum_count'] = False
                s['minimum_count_reason'] += '; implementation is additional evidence outside four minimum categories'
            if s['source_id'] in roottech:
                s['root_reread'] = roottech[s['source_id']]
            sources.append(s)
if (P/'evidence/context-sources.jsonl').exists():
    sources.extend(lines('evidence/context-sources.jsonl'))
if (P/'evidence/root-additional-sources.jsonl').exists():
    sources.extend(lines('evidence/root-additional-sources.jsonl'))

seen = set()
for s in sources:
    if s['minimum_count']:
        assert s['direct_read'], s['source_id']
        if s['work_id'] in seen:
            s['minimum_count'] = False
            s['minimum_count_reason'] += '; root deduplicated previously counted original work'
        else:
            seen.add(s['work_id'])
with (P / 'sources.jsonl').open('w') as f:
    for s in sources:
        f.write(json.dumps(s, ensure_ascii=False) + '\n')

criteria=[]
for domain in ['pandoc','gdal']:
    for r in read(f'streams/{domain}/criteria.json'):
        cid=r['case_id']; p=packets[cid]; v=r.get('variants',[])
        c=dict(criterion_id=r['criterion_id'],case_id=cid,stratum=p['stratum'],version=r.get('version',r.get('pinned_version')),field=p['field'],value1=p['values'][0],value2=p['values'][1],input1=v[0] if v else r.get('input1',r.get('input_common')),input2=v[1] if v else r.get('input2',r.get('input_common')),expected_output1=v[0]['expected_output'] if v else r.get('expected_output1',r.get('expected_output_value1')),expected_output2=v[1]['expected_output'] if v else r.get('expected_output2',r.get('expected_output_value2')),criterion_urls=r['criterion_urls'],same_version=r.get('same_version'),same_input=r.get('same_input', True if p['stratum']=='constructed' else None),only_one_field_changed=r.get('only_one_field_varied',r.get('only_one_field_changed')),expected_equal=r.get('expected_equal',r.get('equal_output')),historical_execution_status='not_performed',historical_execution_output1=None,historical_execution_output2=None,researcher_execution_version='GDAL 3.10.3' if cid.startswith('GDAL-C') else None,researcher_execution_output1=r.get('executed_output_value1') if cid.startswith('GDAL-C') else None,researcher_execution_output2=r.get('executed_output_value2') if cid.startswith('GDAL-C') else None,evidence_level=r.get('evidence_level',r.get('criterion_level','bounded specification; natural full-goal criterion unavailable')),technical_pair_denominator=r.get('technical_pair_denominator',r.get('independently_judgeable')),strict_initial_effect_denominator=False,limit=r.get('confounding_or_unknown',r.get('limitations',r.get('scope'))),source_ledger=f'streams/{domain}/criteria.json')
        if cid=='GDAL-C1':
            c['analytical_discriminator']=r['expected_pair_discriminator']
        if cid=='GDAL-C2':
            c['expected_equal']=True
            c['equality_scope']='40x40 requested nearest-resampling result and stored checksum; historical full bytes unverified'
        elif cid=='PAN-C2':
            c['equality_scope']='exact saved native AST text'
        else:
            c['equality_scope']=None
        if fixed_run and cid in ['PAN-C1','PAN-C2']:
            name='parse-raw' if cid=='PAN-C1' else 'sloppypar'
            runs=[next(t for t in fixed_run['tests'] if t['test_id']==name+'-'+str(i)) for i in [1,2]]
            c['historical_execution_status']='researcher_performed_fixed_release'
            c['historical_execution_output1']=runs[0]['actual_stdout']
            c['historical_execution_output2']=runs[1]['actual_stdout']
            c['evidence_level']+='; actual fixed-release2.11.3.2 researcher execution in evidence/pandoc-fixed-run.json, exact stdout match; not historical-date CI'
            c['limit']='Expectation-informed selection remains; actual2.11.3.2 run confirms these fixtures only. Purpose-to-flag mapping caveat forPAN-C1. Logical criterion hashes omit final LF; actual stdout hashes include it.'
        criteria.append(c)
writecsv('criteria.csv',criteria)

events=[]; absences=[]
for domain in ['pandoc','gdal']:
    for r in read(f'streams/{domain}/events.json'):
        if r.get('event_type')=='no_comments_observed':
            absences.append(r); continue
        e=dict(event_id=r['event_id'],case_id=r['case_id'],url=r.get('url',r.get('source_url')),source_id=r.get('source_id',r['event_id']),actor=r['actor'],actor_role=r['actor_role'],created_utc=r.get('created_at',r.get('created_utc')),updated_utc=r.get('updated_at',r.get('updated_utc')),text_version=r.get('text_version',r.get('comment_version_status','current issue body; opening unverified')),event_kind=r.get('event_type',r.get('event_kind')),selected_field_value=r.get('chosen_field_value',r.get('selected_field_value')),new_selected_field_information=r.get('new_selected_field_value',r.get('new_selected_field_information')),observed_choice=r.get('observed_choice'),author_success_report=r.get('success_report',False),independent_success=r['independent_success'],summary=r['summary'],limitation=r.get('limitation','Current text may be edited; independent use outcome not established.'),actual_response_to_our_policy=False,source_ledger=f'streams/{domain}/events.json')
        eid=str(e['event_id'])
        if eid.startswith('GDAL-OPEN-'):
            e['source_id']='GDAL-I'+eid.rsplit('-',1)[1]
        if 'current' in str(e['event_kind']) and e['case_id'] in initial_review:
            ir=initial_review[e['case_id']]
            e['event_id']=ir['event_id'];e['created_utc']=ir['event_created_utc']
            e['source_id']=('PAN-S-OPENING-RETRY-' if domain=='pandoc' else 'GDAL-OPEN-RETRY-')+ir['issue_number']
            e['event_kind']='opening_event_current_body_concordance'
            e['text_version']='Opened event recovered after seal; current/initial goal-constraints match. Exact body equality='+ir['exact_body_equal']+'. Archive '+ir['archive_url']
            e['limitation']='Opening provenance confirmed after policy/followup exposure; independent use result remains absent. Body differences recorded in initial-version-review.csv.'
        responses={'758272588':'758267520','1236589386':'758788999','1237576087':'1237251161','1238273371':'1238230045','GDAL-COMMENT-755439157':'GDAL-COMMENT-755243851','GDAL-COMMENT-755455797':'GDAL-COMMENT-755454413'}
        if 'current' in str(e['event_kind']):
            e['elicitation_kind']='opening_current'
        elif eid in responses:
            e['elicitation_kind']='response_to_prior_public_question_or_advice_on_other_field'
            e['stimulus_event_id']=responses[eid]
        elif e['actor_role'] in ['OP','original_author']:
            e['elicitation_kind']='spontaneous_public_followup_or_new_goal; not response to selected-field question'
        else:
            e['elicitation_kind']='third_party_question_advice_or_test_report'
        events.append(e)
writecsv('events.csv',events)
dump('evidence/absence-observations.json',absences)

scores=[]; adjudications=[]
for domain in ['pandoc','gdal']:
    for r in read(f'streams/{domain}/scores.json'):
        cid=r['case_id']; branch=r.get('response_branch',r.get('branch'));branch={'none':'no_answer','no_response':'no_answer'}.get(branch,branch)
        rid=f"{cid}-{r['policy']}-{branch}"; p=packets[cid]; pr=policy[rid]
        rawstatus=r.get('status',r.get('verdict')); status=rawstatus
        tech=r.get('technical_denominator',r.get('independently_judgeable'))
        if p['stratum']=='natural':
            action=r.get('exploratory_action_class',rawstatus)
            status=action if action in ('hold','enumeration_unresolved') else 'unjudgeable'
            tech=False
        if cid=='PAN-C1' and r['policy']=='A' and branch=='no_answer':
            tech=False
            adjudications.append(dict(row_id=rid,change='technical judgment denominator true→false',reason='no target value supplied; safety of withholding is visible but completion criterion cannot select an output'))
        if cid=='GDAL-C2' and r['policy']=='B':
            status='correct_single'
            adjudications.append(dict(row_id=rid,change=rawstatus+'→correct_single',reason='sealed B explicitly normalizes both representations to K1; two references do not prevent a single usable action'))
        if r['policy']=='C':
            if cid in ['PAN-N1','PAN-N3','GDAL-N4','PAN-C2','GDAL-C2']:
                over=True; overbasis='current_body_already_states_purpose' if p['stratum']=='natural' else 'both_values_allow_same_action'
            elif p['stratum']=='natural':
                over=None; overbasis='not established; never infer false from no disclosure'
            else:
                over=False;overbasis='two values technically discriminate; this does not prove a dialogue is necessary'
        else:
            over=False;overbasis='policy does not ask'
        s=dict(row_id=rid,case_id=cid,stratum=p['stratum'],policy=r['policy'],response_branch=branch,scenario_value=pr['scenario_value'],status=status,original_stream_status=rawstatus,technical_judgment_denominator=bool(tech),strict_initial_effect_denominator=False,inconsistent_counterfactual=pr['conflicts_with_pre_known_value'].lower()=='true',criterion_id=cid+'-CR',criterion_urls=next(x['criterion_urls'] for x in criteria if x['case_id']==cid),reason=r.get('reason',r.get('rationale')),avoidable_question=over,avoidable_question_basis=overbasis,necessary_question_omitted=False if p['stratum']=='constructed' else None,necessary_condition_omitted=(cid=='GDAL-C1' and r['policy']=='A' and branch=='value2'),observed_user_selection=False,observed_independent_success=False,condition_identification=('irrelevant_same_action' if cid in ['PAN-C2','GDAL-C2'] else 'owner_requirement_unobserved' if p['stratum']=='constructed' else 'current_body_or_additional_inspection; completion criterion missing'),displayed_link_references=int(pr['displayed_link_references']),distinct_answer_documents=int(pr['distinct_answer_documents']),planned_question_rounds=int(pr['question_rounds_planned']),completed_reply_rounds_in_scenario=int(pr['completed_reply_rounds_in_scenario']),actual_dialogue_rounds=0,human_time='not_measured',response_probability='not_measured',source_ledger=f'streams/{domain}/scores.json')
        s['observed_user_selection']=None
        s['user_selection_scope']='A/B/C were not delivered to people; policy selection not measured. Public intentions/reports are separate events.csv observations.'
        if p['stratum']=='natural' and cid in initial_review:
            s['reason']='최초 opened 본문은 사후 회수하여 목적·제약이 봉인 때의 현재판과 같음을 확인. 같은 목표·같은 판의 양값 완성 산출물 기준이 없어 정오 분모는 여전히0. 원 시점의 판단 이유는 source_ledger에 보존.'
            if s['avoidable_question'] is True:s['avoidable_question_basis']='opening_and_current_body_already_state_purpose; provenance verified after policy seal'
        if cid=='PAN-N2':
            s['inconsistent_counterfactual']=False
            s['post_adjudication_note']='Initial must_retain inference withdrawn: desired Chinese quotation/font result is not mandatory literal lang key retention.'
        scores.append(s)
scores.sort(key=lambda r:(list(packets).index(r['case_id']),r['policy'],['value1','value2','no_answer'].index(r['response_branch'])))
writecsv('scores.csv',scores)
dump('evidence/root-adjudications.json',dict(changes=adjudications,global_rules=['Natural completion criteria remain unavailable; visible hold/enumeration classified separately from correctness.','Unknown natural avoidable-question flags normalized to null.','No necessary dialogue omission established: actionable B is an alternative to C.','PAN-N2 literal-language retention and inconsistent-counterfactual inference withdrawn post-seal.'],denominator_definition='technical_judgment_denominator means independent criterion is available for the scenario, not that policy completes it. Known-value holds stay in the criterion denominator and are reported as holds, not errors. Unanswered positive cases have no chosen target; B with a usable condition can still be assessed for conditional actionability.'))

summary=[]
statuses=['correct_single','conditional_actionable','wrong','hold','enumeration_unresolved','unjudgeable']
for stratum in ['natural','constructed']:
    for branch in ['value1','value2','no_answer']:
        for pol in ['A','B','C']:
            rr=[s for s in scores if (s['stratum'],s['response_branch'],s['policy'])==(stratum,branch,pol)]
            summary.append(dict(stratum=stratum,policy=pol,response_branch=branch,total_slots=len(rr),technical_judgment_denominator=sum(s['technical_judgment_denominator'] for s in rr),strict_initial_effect_denominator=0,**{x:sum(s['status']==x for s in rr) for x in statuses},avoidable_questions=sum(s['avoidable_question'] is True for s in rr),avoidable_question_unknown=sum(s['avoidable_question'] is None for s in rr),necessary_question_omitted=sum(s['necessary_question_omitted'] is True for s in rr),observed_user_selection='not_measured',row_ids=[s['row_id'] for s in rr]))
writecsv('policy-summary.csv',summary)

bycase=[]
for cid,p in packets.items():
    rr=[s for s in scores if s['case_id']==cid]
    b=dict(case_id=cid,stratum=p['stratum'],A_known_wrong=sum(s['status']=='wrong' for s in rr if s['policy']=='A' and s['response_branch']!='no_answer'),C_known_wrong=sum(s['status']=='wrong' for s in rr if s['policy']=='C' and s['response_branch']!='no_answer'),known_scenarios_per_policy=2,independent_criterion_available=p['stratum']=='constructed',valid_alternatives_no_answer=(2 if cid in ['PAN-C1','GDAL-C1'] else 1 if p['stratum']=='constructed' else None),C_avoidable_question=next(s['avoidable_question'] for s in rr if s['policy']=='C' and s['response_branch']=='no_answer'),human_time='not_measured',response_probability='not_measured')
    b['potentially_valid_candidate_commands_no_answer']=2 if p['stratum']=='constructed' else None
    b['distinct_valid_action_classes_no_answer']=b['valid_alternatives_no_answer']
    if p['stratum']=='natural':
        b['A_known_wrong']=None
        b['C_known_wrong']=None
    for pol in ['A','B','C']:
        no=next(s for s in rr if s['policy']==pol and s['response_branch']=='no_answer')
        b[pol+'_no_answer_status']=no['status'];b[pol+'_link_references_no_answer']=no['displayed_link_references'];b[pol+'_distinct_documents_no_answer']=no['distinct_answer_documents'];b[pol+'_planned_rounds']=no['planned_question_rounds']
    bycase.append(b)
writecsv('costs.csv',bycase)

counts=dict(source_rows=len(sources),minimum_independent_works=sum(s['minimum_count'] for s in sources),minimum_by_category=dict(collections.Counter(s['minimum_category'] for s in sources if s['minimum_count'])),direct_independent_works_conservative=len({s['work_id'] for s in sources if s['direct_independent_work']}),source_access_failures=sum(not s['direct_read'] for s in sources),frame_rows=len(list(csv.DictReader((P/'frame.csv').open()))),packet_rows=len(packets),policy_rows=len(policy_rows),criterion_rows=len(criteria),event_rows=len(events),empty_comment_observations=len(absences),score_rows=len(scores),summary_rows=len(summary),cost_rows=len(bycase),known_control_scenario_rows=sum(s['stratum']=='constructed' and s['response_branch']!='no_answer' for s in scores),natural_initial_verified=len(initial_review),natural_initial_exact_body_equal=sum(r['exact_body_equal']=='true' for r in initial_review.values()),natural_initial_goal_constraints_changed=sum(r['goal_constraints_changed']=='true' for r in initial_review.values()),natural_new_selected_field_events=sum(bool(e['new_selected_field_information']) for e in events),independent_success_events=sum(bool(e['independent_success']) for e in events),author_success_report_events=sum(bool(e['author_success_report']) for e in events),actual_user_experiments=0,historical_project_binary_executions=fixed_run['process_invocations'] if fixed_run else 0,historical_fixture_runs=fixed_run['test_count'] if fixed_run else 0,modern_gdal_execution_commands=5)
dump('evidence/ledger-counts.json',counts)
print(json.dumps(counts,ensure_ascii=False,indent=2))
