"""Independent offline checks of AF-RES-036 preserved evidence and aggregation.

This verifier reads the recorded inputs; it does not rerun readers, fetch sources,
or treat successful structural checks as an independent semantic gold standard.
Writes only its requested receipt under review/resume-quant/.
"""
from __future__ import annotations
import argparse, collections, csv, datetime, hashlib, json, math, re, subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
P=HERE.parents[1]
REPO=P.parents[3]

def digest(data):return hashlib.sha256(data if isinstance(data,bytes) else data.encode()).hexdigest()
def jl(name):return [json.loads(x) for x in (P/name).read_text().splitlines() if x.strip()]
def js(name):return json.loads((P/name).read_text())
def cs(name):return list(csv.DictReader((P/name).open()))
def truth(x):return x is True or str(x).lower()=='true'
def jval(x):return json.loads(x) if isinstance(x,str) else x
def num(x):return float(x) if x not in ['',None] else 0
def normalized(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--receipt',default='audit.json');args=ap.parse_args()
    out=HERE/args.receipt
    if HERE not in out.resolve().parents:raise SystemExit('receipt must be inside this audit directory')
    checks=[]
    def check(name,condition,details=None):
        checks.append({'id':name,'passed':bool(condition),'details':details})
    refs=jl('references.jsonl');comps=jl('components.jsonl');packs=jl('packets.jsonl')
    dec=cs('decisions.csv');adj=cs('adjudication.csv');sources=jl('sources.jsonl');ats=jl('attempts.jsonl')
    costs=cs('costs.csv');sim=cs('replay-costs.csv');sens=cs('sensitivity.csv')
    R={x['ref_id']:x for x in refs};C={x['ref_id']:x for x in comps}
    PK={(x['ref_id'],x['view']):x for x in packs};D={(x['ref_id'],x['view']):x for x in dec}
    J={x['ref_id']:x for x in adj};A={x['attempt_id']:x for x in ats}
    expected={f'{p}{i:02}' for p in 'GR' for i in range(1,7)}
    V=['B','BN','BH','BNH']; expected_cells={(r,v) for r in expected for v in V}
    check('reference_cases_exact12',len(refs)==12 and set(R)==expected)
    check('components_exact12',len(comps)==12 and set(C)==expected)
    check('packet_cells_exact48',len(packs)==48 and set(PK)==expected_cells)
    check('decision_cells_exact48',len(dec)==48 and set(D)==expected_cells)
    check('criterion_rows_exact12',len(adj)==12 and set(J)==expected)
    projects=collections.Counter(x['project'] for x in refs)
    publications={(x['project'],x.get('publication_id',x.get('consumer_title',x.get('member')))) for x in refs}
    check('two_routes_six_each',collections.Counter(x['route'] for x in refs)=={'G':6,'R':6})
    check('twelve_distinct_publications',len(publications)==12)
    check('at_least_six_projects_max2',len(projects)>=6 and max(projects.values())<=2,dict(projects))
    check('reference_context_hashes',all(digest(x['context'])==x['context_sha256'] and ('context_bytes' not in x or len(x['context'].encode())==x['context_bytes']) for x in refs))
    check('reference_context_char_cap',all(len(x['context'])<=1200 for x in refs))
    check('packet_whole_hashes',all(digest(x['input_text'])==x['input_text_sha256'] and len(x['input_text'].encode())==x['input_utf8_bytes'] for x in packs))
    check('packet_part_hashes',all(all(digest(text)==x['part_sha256'][part] and len(text.encode())==x['part_utf8_bytes'][part] for part,text in x['parts'].items()) for x in packs))
    check('packet_input_reconstruction',all(x['input_text']=='\n\n'.join('['+k+']\n'+x['parts'][k] for k in ['B','N','H'] if k in x['parts']) for x in packs))
    check('identical_B_all_views',all(len({PK[r,v]['parts']['B'] for v in V})==1 for r in expected))
    check('identical_N_BN_BNH',all(PK[r,'BN']['parts']['N'].encode()==PK[r,'BNH']['parts']['N'].encode()==C[r]['N']['text'].encode() for r in expected))
    check('identical_H_BH_BNH',all(PK[r,'BH']['parts']['H'].encode()==PK[r,'BNH']['parts']['H'].encode()==C[r]['H']['text'].encode() for r in expected))
    check('component_text_hashes',all(digest(c[k]['text'])==c[k]['sha256'] and len(c[k]['text'].encode())==c[k]['utf8_bytes'] for c in comps for k in ['N','H']))
    check('component_raw_hashes',all(digest(c[k]['raw_excerpt'])==c[k]['raw_sha256'] and len(c[k]['raw_excerpt'].encode())==c[k]['raw_utf8_bytes'] for c in comps for k in ['N','H']))
    check('component_raw_char_cap',all(len(c[k]['raw_excerpt'])<=1600 for c in comps for k in ['N','H']))
    wrapped_over_limit=[{'ref_id':c['ref_id'],'part':k,'full_chars':len(c[k]['text']),'raw_chars':len(c[k]['raw_excerpt'])} for c in comps for k in ['N','H'] if len(c[k]['text'])>1600]
    check('wrapped_vs_excerpt_length_distinction_recorded',[(x['ref_id'],x['part']) for x in wrapped_over_limit]==[('G04','N'),('R04','N')],wrapped_over_limit)
    check('all12_current_requests_join',all(C[r]['N']['original_get_attempt_id'] in A for r in R))
    check('all12_original_gets_attempted',all(A[C[r]['N']['original_get_attempt_id']]['operation']=='GET' for r in R))

    plan=js('reading-plan.json')['rows'];actualplan={(x['reader_id'],x['case_id']):(x['view'],int(x['case_order'])) for x in plan}
    check('assignment_matches_sealed_plan',all(actualplan[d['reader_id'],d['ref_id']]==(d['view'],int(d['case_order'])) for d in dec))
    reader_checks=[]
    for rid in [f'fresh-{i}' for i in range(1,5)]:
        assignment=js(f'readers/{rid}/assignment.json');receipt=js(f'readers/{rid}/run-receipt.json')
        rows=jl(f'readers/{rid}/output.jsonl');view_counts=collections.Counter(x['view'] for x in rows)
        ok=len(rows)==12 and len({x['ref_id'] for x in rows})==12 and all(view_counts[v]==3 for v in V)
        check(rid+'_balanced_once_each_case',ok)
        check(rid+'_receipt_hash',digest((P/f'readers/{rid}/output.jsonl').read_bytes())==receipt['output_sha256'])
        match=[]
        for a in assignment['assignments']:
            f=P/f'readers/{rid}'/a['file'];raw=f.read_bytes();data=json.loads(raw)
            d=D[data['ref_id'],data['view']];packet=PK[data['ref_id'],data['view']]
            match.append(digest(raw)==a['file_sha256']==d['input_sha256'] and data['input_text']==packet['input_text'] and digest(data['input_text'])==a['input_text_sha256'])
        check(rid+'_input_file_and_packet_hashes',all(match))
        check(rid+'_reported_no_parent_or_other_views',assignment['parent_history']=='none' and all(not truth(d['saw_same_case_other_view']) and not truth(d['saw_prior_outcome']) for d in dec if d['reader_id']==rid))
        ordered=sorted((d for d in dec if d['reader_id']==rid),key=lambda d:int(d['case_order']))
        times=[datetime.datetime.fromisoformat(d['decided_utc']) for d in ordered]
        check(rid+'_decision_times_monotonic',times==sorted(times))
        reader_checks.append({'reader_id':rid,'rows':len(rows),'view_counts':dict(view_counts)})

    aliases=js('evidence/source-aliases.json');sids={r['source_id'] for r in sources}
    check('source_canonical_ids_unique',len(sids)==len(sources))
    check('source_groups_unique',len({r['duplicate_group'] for r in sources})==len(sources))
    check('all_source_aliases_join',all(aliases[a]==s['source_id'] for s in sources for a in s['source_aliases']) and all(v in sids for v in aliases.values()))
    check('all_reference_source_ids_join',all(x['source_id'] in aliases for x in refs))
    component_ids=set(s for c in comps for k in ['N','H'] for s in c[k]['source_ids'])
    check('all_component_source_ids_join',component_ids<=set(aliases),sorted(component_ids-set(aliases)))
    criterion_ids=set(s for j in adj for s in jval(j['primary_source_ids']))
    check('all_criterion_source_ids_join',criterion_ids<=set(aliases),sorted(criterion_ids-set(aliases)))
    check('all_source_raw_records_recoverable',all(v['raw_record'] in jl(v['raw_record_path']) for s in sources for v in s['variants']))
    source_counts=js('evidence/source-counts.json')
    eligible=sum(s['count_minimum'] for s in sources)
    categories=dict(collections.Counter(c for s in sources if s['count_minimum'] for c in s['count_categories']))
    check('source_counts_recomputed',eligible==source_counts['unique_eligible_sources'] and categories==source_counts['categories'],{'eligible':eligible,'categories':categories})
    check('source_minima_counts',eligible>=30 and categories.get('original_consumer',0)>=12 and categories.get('current_destination',0)>=8 and categories.get('independent_historical',0)>=6)
    check('adjudicator_no_minimum_inflation',source_counts.get('post_decision_added_minimum_credit')==0)

    cats=['correct_keep','correct_replace','wrong_replace','wrong_keep','hold','criterion_unresolved']
    def score(r,v):
        key=J[r];a=D[r,v]['action']
        if not truth(key['confirmed']) or key['criterion_action'] not in ['KEEP','REPLACE']:return 'criterion_unresolved'
        if a=='HOLD':return 'hold'
        if key['criterion_action']=='KEEP':return 'correct_keep' if a=='KEEP' else 'wrong_replace'
        return 'correct_replace' if a=='REPLACE' else 'wrong_keep'
    def tally(ids,v):
        c=collections.Counter(score(r,v) for r in ids);return {k:c[k] for k in cats}
    summary=js('evidence/analysis-summary.json')
    calculated_views={v:tally(R,v) for v in V}
    check('view_scores_recomputed',calculated_views==summary['views'],calculated_views)
    check('criterion_confirmed_values_boolean',all(j['confirmed'] in ['True','False'] for j in adj))
    comparison_errors=[]
    for row in summary['comparisons']:
        before,after=row['comparison'].split('→');ids=row['ref_ids']
        confirmed=sum(truth(J[r]['confirmed']) and J[r]['criterion_action'] in ['KEEP','REPLACE'] for r in ids)
        cb,ca=tally(ids,before),tally(ids,after)
        def grp(s):return 'correct' if s.startswith('correct_') else ('wrong' if s.startswith('wrong_') else s)
        transitions=dict(collections.Counter(grp(score(r,before))+'_to_'+grp(score(r,after)) for r in ids))
        changes=[r for r in ids if D[r,before]['action']!=D[r,after]['action']]
        expected_ids=set(summary['filter_sets'][row['filter']])
        if row['stratum']=='R_historical':expected_ids={r for r in expected_ids if r.startswith('R') and R[r]['purpose_stratum']=='historical'}
        elif row['stratum']!='all':expected_ids={r for r in expected_ids if R[r]['purpose_stratum']==row['stratum']}
        ok=(set(ids)==expected_ids and len(ids)==row['paired_refs'] and confirmed==row['confirmed_criterion_refs'] and cb==row['before'] and ca==row['after'] and changes==row['action_change_ids'] and transitions==row['transition_counts'])
        for label,counts in [('before',cb),('after',ca)]:
            acc=(counts['correct_keep']+counts['correct_replace'])/confirmed if confirmed else None
            ok &= acc==row['conditional_accuracy_'+label]
        if not ok:comparison_errors.append([row['comparison'],row['filter'],row['stratum']])
    check('all255_comparison_summaries_recomputed',len(summary['comparisons'])==255 and not comparison_errors,comparison_errors)
    detail_errors=[]
    for r in sens:
        rid=r['ref_id'];a=r['before_view'];b=r['after_view']
        if not (r['before_action']==D[rid,a]['action'] and r['after_action']==D[rid,b]['action'] and r['before_score']==score(rid,a) and r['after_score']==score(rid,b) and truth(r['included'])==(rid in summary['filter_sets'][r['filter']]) and r['before_input_sha256']==D[rid,a]['input_sha256'] and r['after_input_sha256']==D[rid,b]['input_sha256']):detail_errors.append([r['comparison'],r['filter'],rid])
    check('all612_sensitivity_rows_recomputed',len(sens)==612 and not detail_errors,detail_errors)
    check('N_history_filter_recomputed',set(summary['filter_sets']['exclude_N_card_history'])=={r for r in R if not C[r]['N'].get('card_contains_history')})
    check('no_reported_prior_filter_recomputed',set(summary['filter_sets']['no_any_reported_prior_related_case'])=={r for r in R if all(not jval(D[r,v]['prior_related_case_ids']) for v in V)})
    check('strict_purpose_and_external_gold_denominators_zero',summary['filter_sets']['exclude_all_collector_purpose_paraphrase']==[] and summary['filter_sets']['external_independent_gold_only']==[])

    check('attempt_ids_unique',len(A)==len(ats))
    actual=[x for x in costs if str(x['round'])=='1'];getcost={x['cost_id']:x for x in actual if int(x.get('actual_requests') or 0)==1}
    getats={x['attempt_id']:x for x in ats if x.get('operation')=='GET' and x.get('phase')!='resume_audit'}
    check('one_actual_cost_per_GET',set(getcost)==set(getats) and len(getcost)==len(getats))
    cost_errors=[]
    for aid,a in getats.items():
        row=getcost[aid]
        same=(num(row['received_body_bytes'])==(a.get('received_body_bytes') or 0) and num(row['temporary_stored_bytes'])==(a.get('stored_bytes') or 0) and abs(num(row['elapsed_seconds'])-(a.get('elapsed_seconds') or 0))<1e-9 and int(row['http_exchanges_minimum'])==1+len(a.get('redirect_chain',[])))
        if not same:cost_errors.append(aid)
    check('all_actual_cost_units_match_attempts',not cost_errors,cost_errors)
    calc={'actual_get_operations':len(getats),'minimum_http_exchanges':sum(1+len(x.get('redirect_chain',[])) for x in getats.values()),
      'transport_failures':sum(bool(x.get('error')) or (x.get('status') is not None and x['status']>=400) for x in getats.values()),
      'received_final_body_bytes':sum(x.get('received_body_bytes') or 0 for x in getats.values()),
      'temporary_fetch_stored_bytes':sum(x.get('stored_bytes') or 0 for x in getats.values()),
      'sum_request_elapsed_seconds':round(sum(x.get('elapsed_seconds') or 0 for x in getats.values()),6)}
    cost_summary=js('evidence/cost-summary.json')
    check('whole_task_cost_summary_recomputed',all(calc[k]==cost_summary[k] for k in calc),calc)
    resume_summary=None
    if (P/'evidence/resume-cost-summary.json').exists():
        resume_summary=js('evidence/resume-cost-summary.json')
        resume_ats={a['attempt_id']:a for a in ats if a.get('phase')=='resume_audit'}
        resume_costs={r['cost_id']:r for r in costs if r.get('phase')=='resume_audit'}
        resume_get={k:a for k,a in resume_ats.items() if a.get('operation')=='GET'}
        def phase_stats(items):
            gs=[a for a in items if a.get('operation')=='GET']
            return {'actual_get_operations':len(gs),'minimum_http_exchanges':sum(1+len(a.get('redirect_chain',[])) for a in gs),
              'failed_GETs':sum(bool(a.get('error')) or (a.get('status') is not None and a['status']>=400) for a in gs),
              'received_final_body_bytes':sum(a.get('received_body_bytes') or 0 for a in gs),
              'temporary_full_body_stored_bytes':sum(a.get('stored_bytes') or 0 for a in gs),
              'sum_request_elapsed_seconds':round(sum(a.get('elapsed_seconds') or 0 for a in gs),6)}
        check('resume35_attempts_and_costs_join',len(resume_ats)==35 and set(resume_ats)==set(resume_costs))
        check('resume10_measured_GET_and25_unmetered_actions',len(resume_get)==10 and len(resume_ats)-len(resume_get)==25)
        check('resume_measured_cost_units_match',all(num(resume_costs[k]['received_body_bytes'])==(a.get('received_body_bytes') or 0) and num(resume_costs[k]['temporary_stored_bytes'])==(a.get('stored_bytes') or 0) and abs(num(resume_costs[k]['elapsed_seconds'])-(a.get('elapsed_seconds') or 0))<1e-9 and int(resume_costs[k]['actual_requests'])==1 for k,a in resume_get.items()))
        check('unmetered_resume_not_invented_as_GET_or_zero_bytes',all(resume_costs[k]['actual_requests']=='' and resume_costs[k]['received_body_bytes']=='' and resume_costs[k]['elapsed_seconds']=='' for k in set(resume_ats)-set(resume_get)))
        check('resume_phase_summary_recomputed',phase_stats(resume_ats.values())==resume_summary['measured_GET_scope'])
        check('combined_measured_scope_recomputed',phase_stats(ats)==resume_summary['combined_measured_GET_scope'])
        check('all_resume_source_aliases_join',all(a.get('source_id') is None or a['source_id'] in aliases for a in resume_ats.values()) and all(x['source_id'] in aliases for x in resume_summary['reread_source_aliases']))
        check('resume_no_source_minimum_inflation',source_counts['resume_audit_added_minimum_credit']==0 and source_counts['resume_audit_source_records']==18 and len(aliases)==144)
        ons=next(s for s in sources if s['source_id']=='CX-G02')
        check('CX_G02_locator_corrected_original_preserved','Overview of main changes' in ons['read_location'] and '87–90' in ons['read_location'] and ons['variants'][0]['read_location']==ons['read_location_correction']['previous'])
    check('all48_simulation_rows_unmeasured',len(sim)==48 and all(int(x['actual_requests'])==0 and x['received_body_bytes']=='unmeasured_second_visit' and 'SIMULATION' in x['measurement'] for x in sim))
    sim_errors=[]
    for row in sim:
        ids=row['unit_attempt_ids'].split('|') if row['unit_attempt_ids'] else []
        gs=[A[i] for i in ids]
        ok=(len(gs)==int(row['modeled_request_operations']) and sum(1+len(x.get('redirect_chain',[])) for x in gs)==int(row['modeled_http_exchanges']) and sum(x.get('received_body_bytes') or 0 for x in gs)==int(row['modeled_body_bytes']) and abs(sum(x.get('elapsed_seconds') or 0 for x in gs)-float(row['first_visit_elapsed_proxy_seconds']))<1e-5 and truth(row['operation_count_within_budget'])==(len(gs)<=int(row['request_operation_budget'])) and truth(row['strict_exchange_count_within_budget'])==(sum(1+len(x.get('redirect_chain',[])) for x in gs)<=int(row['request_operation_budget'])))
        if not ok:sim_errors.append(row['cost_id'])
    check('simulation_units_and_budget_recomputed',not sim_errors,sim_errors)
    replay_errors=[]
    for summ in js('evidence/replay-summary.json'):
        rows=[r for r in sim if r['task']==summ['task'] and r['configuration']==summ['configuration']]
        unique={i for r in rows for i in r['unit_attempt_ids'].split('|') if i};physical=summ['shared_source_physical_lower_bound']
        ok=len(rows)==summ['cases'] and sum(int(r['modeled_request_operations']) for r in rows)==summ['logical_operations'] and sum(int(r['modeled_body_bytes']) for r in rows)==summ['logical_body_bytes'] and len(unique)==physical['operations'] and sum(A[i].get('received_body_bytes') or 0 for i in unique)==physical['body_bytes'] and sum(truth(r['operation_count_within_budget']) for r in rows)==summ['operation_count_feasible_cases'] and sum(truth(r['strict_exchange_count_within_budget']) for r in rows)==summ['strict_exchange_count_feasible_cases']
        if not ok:replay_errors.append([summ['task'],summ['configuration']])
    check('replay_summary_shared_physical_counts',not replay_errors,replay_errors)
    retention=js('evidence/retention-summary.json');lines=(P/'retention-options.jsonl').read_bytes().splitlines(keepends=True)
    group_bytes=collections.Counter()
    retention_units={(u['ref_id'],k):v for u in retention['record_units'] for k,v in u['serialized'].items()}
    retention_ok=True
    for line in lines:
        r=json.loads(line);key=(r['ref_id'],r['configuration']);u=retention_units[key]
        retention_ok &= len(line)==u['bytes'] and digest(line)==u['sha256'];group_bytes[r['configuration']]+=len(line)
    check('retention_serialized_bytes_hashes',retention_ok and dict(group_bytes)==retention['configuration_bytes'] and sum(map(len,lines))==retention['physical_serialized_file_bytes'])

    report_tables=[]
    if (P/'RESULT.md').exists():
        current=[]
        for line in (P/'RESULT.md').read_text().splitlines():
            if line.startswith('|'):current.append([c.strip() for c in line.split('|')[1:-1]])
            elif current:report_tables.append(current);current=[]
        if current:report_tables.append(current)
        headers=[['참조 ID·원배포/목적','원 href·버전','현재 절 URL·확인 내용','과거 근거 URL·판','네 보기의 행동(B·B+N·B+H·B+N+H)','기준판정·독립성','미확인'],
          ['대조·목적 층','짝지은 참조 수','옳은 유지·교체','오교체·잘못 유지·보류','N 고정 후 H로 바뀐 사건 ID','노출 제외·판정 불가'],
          ['참조·조회 회차·구성','실제 요청·실패','받은 바이트·저장 바이트','같은 판 재사용·재열람·경과','실제·모의·미계측','결론을 바꿀 다음 자료']]
        check('RESULT_first_three_headers_exact',len(report_tables)>=3 and [t[0] for t in report_tables[:3]]==headers)
        check('RESULT_first_table12_final_weaknesses3',len(report_tables[0])-2==12 and len(report_tables[-1])-2==3)
        units={x['ref_id']:x for x in js('evidence/replay-units.json')};ret={x['ref_id']:x for x in retention['record_units']}
        errors=[]
        for row in report_tables[2][2:14]:
            rid=row[0][:3];u=units[rid];ids=list(dict.fromkeys([u['base_acquisition_attempt_id']]+u['N_attempt_ids']+u['H_attempt_ids']));aa=[A[i] for i in ids]
            n=re.match(r'(\d+) GET / 실패 (\d+)',row[1]);b=re.search(r'([\d,]+)B 수신',row[2]);t=re.search(r'합 ([\d.]+)s',row[3])
            retained=[int(x.replace(',','')) for x in re.findall(r'C[12](?:\(B\))? ([\d,]+)B',row[2])]
            fails=sum(bool(a.get('error')) or (a.get('status') is not None and a['status']>=400) for a in aa)
            ok=(n and b and t and int(n[1])==len(ids) and int(n[2])==fails and int(b[1].replace(',',''))==sum(a['received_body_bytes'] for a in aa) and abs(float(t[1])-sum(a['elapsed_seconds'] for a in aa))<1e-6 and retained==[ret[rid]['serialized'][k]['bytes'] for k in ['C1_B_presealed','C2_BH_with_provenance']])
            if not ok:errors.append(rid)
        check('RESULT_table3_case_arithmetic',not errors,errors)

    # Prove packet/decisions still have the bytes published at their seal commits.
    sealed_checks=[]
    for commit,filename in [('442292b34237fa7aa2d68493e2a96802f52ed728','packets.jsonl'),('5fbde38a04613fbd6f057fd562bd173b7193f2c9','decisions.csv')]:
        rp=str((P/filename).relative_to(REPO))
        proc=subprocess.run(['git','show',commit+':'+rp],cwd=REPO,capture_output=True)
        sealed_checks.append(proc.returncode==0 and proc.stdout==(P/filename).read_bytes())
    check('git_seal_packet_and_decisions_bytes',all(sealed_checks),sealed_checks)
    proc=subprocess.run(['git','rev-parse','HEAD'],cwd=REPO,capture_output=True,text=True)
    inputs=['references.jsonl','components.jsonl','packets.jsonl','decisions.csv','adjudication.csv','sources.jsonl','attempts.jsonl','costs.csv','replay-costs.csv','sensitivity.csv','retention-options.jsonl','evidence/analysis-summary.json','evidence/source-counts.json','evidence/cost-summary.json','evidence/replay-summary.json','evidence/retention-summary.json','reading-plan.json']
    inputs += [f for f in ['evidence/resume-cost-summary.json','RESULT.md'] if (P/f).exists()]
    report={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'head_commit':proc.stdout.strip(),'working_tree_input_sha256':{f:digest((P/f).read_bytes()) for f in inputs},
      'checks':checks,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),
      'views':calculated_views,'strata':dict(collections.Counter(r['purpose_stratum'] for r in refs)),
      'source_minimum':{'eligible':eligible,'categories':categories},'actual_costs':calc,
      'actual_costs_scope':'Completed experimental collection plus adjudication; excludes separately measured resume_audit phase.',
      'resume_costs':resume_summary,'report_table_shapes':[[len(t)-2,len(t[0])] for t in report_tables],
      'reader_assignment_checks':reader_checks,
      'limitations':['Offline structural/arithmetic audit; not a new blinded decision or external gold.',
      'Minimum50 uses preserved conservative eligibility labels, not an independent semantic reclassification of all sources.',
      'Same-model family and prior-related source exposure remain; zero strict-purpose/external-gold denominators are not observations of no effect.',
      'Tool elapsed sum is not wall time or labor; all second-visit quantities are simulated.']}
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'receipt':str(out.relative_to(P)),'passed':report['passed'],'failed':report['failed'],'failed_checks':[c for c in checks if not c['passed']]},ensure_ascii=False))
    raise SystemExit(bool(report['failed']))

if __name__=='__main__':main()
