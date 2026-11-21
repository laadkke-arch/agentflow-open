#!/usr/bin/env python3
"""Join frozen external answers, real outputs and later independent audits.

No missing run, judgment, identity decision or claim verdict is manufactured.
The external gold is never enlarged from newly useful discovered candidates.
"""
import collections,csv,hashlib,json
from common import ROOT,load,save,ratio,run_costs,check_decision,elapsed,temporal_category

def row_id(q,c,kind,index):
    return 'R'+hashlib.sha256(f'18018|{q}|{c}|{kind}|{index}'.encode()).hexdigest()[:16]
def records(value):return value['rows'] if isinstance(value,dict) and 'rows' in value else value
def verdict(v):
    table={'true':'true','참':'true','false':'false','거짓':'false',
           'unverifiable':'unknown','unknown':'unknown','확인 불가':'unknown','확인불가':'unknown'}
    assert str(v) in table,('unsupported claim verdict',v)
    return table[str(v)]
def main():
    order=load('questions/dispatch.json')['order'];meta={r['id']:r for r in load('questions/metadata.json')}
    states={r['dispatch_index']:r for r in load('runs/DISPATCH_STATE.json')['assigned']}
    gold=load('gold/answers.json');gold_by_q=collections.defaultdict(list);grade_by_id={}
    for g in gold:
        gold_by_q[g['query_id']].append(g);grade_by_id[g['entity_id']]=str(g['grade'])
    mapping={r['row_id']:r for r in load('analysis/candidate-mapping.json')}
    nscope=load('analysis/n-scope.json',{})
    checks={q['qid']:q['checks'] for q in load('gold/checks.json')['questions']}
    reason_audit={r['row_id']:r for r in records(load('judging/reason-audit.json'))}
    probe_truth={}
    for q,probes in checks.items():
        for i,g in enumerate(probes):
            if not g['eligible_current_strict_N_denominator']:continue
            ids=[row_id(q,c,'check',i) for c in ['A','P']]
            values=[str(reason_audit[rid]['frozen_violation_supported']).lower() for rid in ids]
            assert all(v in ['true','false','unknown'] for v in values),(q,values)
            status='supported' if values==['true','true'] else 'unsupported' if values==['false','false'] else 'unclear' if 'unknown' in values else 'inconsistent'
            probe_truth[q]={'qid':q,'candidate':g['name'],'status':status,'row_ids':ids,
                            'auditor_truth_values':values,'source_files':[reason_audit[rid]['source_file'] for rid in ids]}
    claims=records(load('claims/CLAIMS.json'));sample=load('claims/SAMPLE.json')['claims']
    assert {c['id'] for c in claims}=={c['id'] for c in sample} and len(claims)==len(sample)
    claim_groups=collections.defaultdict(list);pool_groups=collections.defaultdict(list);uncertain_groups=collections.defaultdict(list)
    for c in claims:claim_groups[(c['condition'],c['qid'])].append(c)
    for c in load('claims/pool.json'):pool_groups[(c['condition'],c['qid'])].append(c)
    for c in load('claims/uncertainty.json'):uncertain_groups[(c['condition'],c['qid'])].append(c)
    key=load('judging/key.json')['rows'];judgments=collections.defaultdict(dict)
    for f in sorted((ROOT/'judging/blind-raw').glob('*.json')):
        j=json.loads(f.read_text());jid=j['judge_id']
        for r in j['rows']:
            assert r['row_id'] not in judgments[jid],('duplicate blind row',jid,r['row_id'])
            judgments[jid][r['row_id']]=r
    assert 'primary' in judgments
    # Pools contain discovery proposals only. Seeded check probes never enlarge them.
    useful_pools=collections.defaultdict(lambda:collections.defaultdict(set))
    for jid,jrows in judgments.items():
        for rid,r in jrows.items():
            k=key[rid]
            if k['kind']=='discovery' and str(r['relevance'])=='1':
                useful_pools[jid][k['qid']].add(mapping[rid]['pool_entity'])
    observations=[];check_rows=[];candidate_rows=[]
    for d in order:
        q,c=d['qid'],d['condition'];run=load(d['output']);assert run and len(run.get('checks',[]))==3
        assert states[d['dispatch_index']]['phase']=='completed'
        receipt=load(f'runs/freeze/{c}-{q}.json');m=meta[q]
        relgold={g['entity_id'] for g in gold_by_q[q] if str(g['grade']) in ['1','2'] and g.get('eligible_for_entity_recall',True)}
        gold2={g['entity_id'] for g in gold_by_q[q] if str(g['grade'])=='2' and g.get('eligible_for_entity_recall',True)}
        found=set();found2=set();pre_found=set();first=11;historical_n=0;current_n=0;n_scope_unknown=0
        disc_ids=[];retrieved_pool=set()
        for i,candidate in enumerate(run['candidates']):
            rid=row_id(q,c,'discovery',i);mp=mapping[rid];disc_ids.append(rid);retrieved_pool.add(mp['pool_entity'])
            matches=set(mp['gold_entity_ids']);hit=matches&relgold;found|=hit;found2|=matches&gold2
            if hit:first=min(first,candidate['rank'])
            if temporal_category(candidate)=='pre_decision':pre_found|=hit
            is_n=any(grade_by_id[e]=='N' for e in matches);historical_n+=is_n
            if is_n:
                assert rid in nscope,('historical N needs scope audit',rid)
                applicable=nscope[rid]['current_strict_N'];assert applicable in [True,False,None]
                current_n+=applicable is True;n_scope_unknown+=applicable is None
            candidate_rows.append({'row_id':rid,'condition':c,'qid':q,'rank':candidate['rank'],
                                   'candidate':candidate['name'],'gold_entity_ids':sorted(matches),
                                   'related_gold_hits':sorted(hit),'grade2_hits':sorted(matches&gold2),
                                   'historical_N_match':is_n,'current_N_scope':nscope.get(rid),
                                   'temporal_category':temporal_category(candidate),'pool_entity':mp['pool_entity']})
        obs={'condition':c,'qid':q,'cohort':m['cohort'],'source_subset':m['source_subset'],
             'question_date':m['date'],
             'input_mode':m['input_mode'],'whole_or_part':m['whole_or_part'],'I5':m['I5'],
             'must_present':bool(m['must']),'gold_relevant_count':len(relgold),'retrieved_relevant':len(found),
             'gold_recall':ratio(len(found),len(relgold)),'gold2_count':len(gold2),
             'grade2_hit':int(bool(found2)) if gold2 else None,'grade2_retrieved':len(found2),
             'first_known_related_rank':first,'first_known_related_rank_gold_eligible':first if relgold else None,
             'first_known_related_rank_hit_only':first if found else None,
             'pre_only_recall':ratio(len(pre_found),len(relgold)),
             'output_candidates':len(run['candidates']),'max_slots':10,
             'historical_N_candidates':historical_n,'current_scoped_N_candidates':current_n,
             'historical_N_scope_unknown':n_scope_unknown,
             'known_gold_unjudged_candidates':sum(not mapping[rid]['gold_entity_ids'] for rid in disc_ids),
             **run_costs(run,receipt)}
        for prefix in ['positive','strict_N','unrelated']:
            obs[prefix+'_denominator']=0;obs[prefix+'_excluded']=0
        obs['strict_N_correct_reject']=0;obs['positive_grade2_denominator']=0;obs['positive_grade2_excluded']=0
        obs['auditor_confirmed_N_denominator']=0;obs['auditor_confirmed_N_correct_reject']=0;obs['auditor_confirmed_N_excluded']=0
        obs['strict_N_audit_truth']=probe_truth.get(q,{}).get('status')
        obs['positive_kept_uncertain_by_primary']=0
        obs['positive_kept_uncertain_by_executor_label']=0
        obs['strict_N_origin']=None
        expected_ids=[x['check_id'] for x in checks[q]];assert [x['check_id'] for x in run['checks']]==expected_ids
        for i,(check,g) in enumerate(zip(run['checks'],checks[q])):
            rid=row_id(q,c,'check',i);excluded=check_decision(check)=='exclude'
            roles={'positive':g['eligible_positive_denominator'],'strict_N':g['eligible_current_strict_N_denominator'],
                   'unrelated':g['eligible_unrelated_denominator']}
            for role,eligible in roles.items():
                obs[role+'_denominator']+=int(eligible);obs[role+'_excluded']+=int(eligible and excluded)
            correct_reason=None
            if roles['strict_N']:
                provenance=g.get('provenance',{})
                obs['strict_N_origin']='historical011' if provenance.get('near_miss_id') else 'constructed'
                assert rid in reason_audit,('missing blind reason audit',rid)
                correct_reason=reason_audit[rid]['verdict']=='correct'
                obs['strict_N_correct_reject']+=int(excluded and correct_reason)
                confirmed=probe_truth[q]['status']=='supported'
                obs['auditor_confirmed_N_denominator']+=int(confirmed)
                obs['auditor_confirmed_N_correct_reject']+=int(confirmed and excluded and correct_reason)
                obs['auditor_confirmed_N_excluded']+=int(confirmed and excluded)
            if roles['positive'] and str(g['grade'])=='2':
                obs['positive_grade2_denominator']+=1;obs['positive_grade2_excluded']+=int(excluded)
            # Independently judged uncertainty is reported separately from actual rejection.
            j=judgments['primary'][rid]
            obs['positive_kept_uncertain_by_primary']+=int(roles['positive'] and not excluded and j['label']=='INSUFFICIENT')
            executor_label=check.get('label')
            obs['positive_kept_uncertain_by_executor_label']+=int(roles['positive'] and not excluded and executor_label=='INSUFFICIENT')
            check_rows.append({'row_id':rid,'condition':c,'qid':q,'check_id':g['check_id'],'candidate':g['name'],
                               'decision':check_decision(check),'frozen_grade':str(g.get('grade','unavailable')),
                               'executor_label':executor_label,'executor_reason':check.get('reason'),
                               'strict_N_origin':obs['strict_N_origin'] if roles['strict_N'] else None,
                               **roles,'correct_reason':correct_reason,'primary_relevance':str(j['relevance']),
                               'primary_label':j['label']})
        facts=pool_groups[(c,q)];sampled=claim_groups[(c,q)];vc=collections.Counter(verdict(x['verdict']) for x in sampled)
        obs.update(factual_claims=len(facts),uncertainty_items=len(uncertain_groups[(c,q)]),
                   claims_without_supplied_URL=sum(not x.get('supplied_urls') for x in facts),
                   claims_without_any_supplied_reference=sum(not x.get('supplied_urls') and not x.get('citation_refs') for x in facts),
                   claims_with_unresolved_citations=sum(bool(x.get('unresolved_citation_refs')) for x in facts),
                   claims_with_homepage_only=sum(x.get('reference_kind')=='homepage_only' for x in facts),
                   sampled_claims=len(sampled),claims_true=vc['true'],claims_false=vc['false'],claims_unknown=vc['unknown'],
                   claims_false_or_unknown=vc['false']+vc['unknown'],
                   claims_verifiable=vc['true']+vc['false'],claim_error_rate=ratio(vc['false'],vc['true']+vc['false']),
                   claim_unknown_rate=ratio(vc['unknown'],len(sampled)),
                   claim_error_lower_bound=ratio(vc['false'],len(sampled)),
                   claim_error_upper_bound=ratio(vc['false']+vc['unknown'],len(sampled)))
        obs['recorded_active_seconds']=(obs['stage1_wall_seconds']+obs['checks_wall_seconds']) if obs['stage1_wall_seconds'] is not None and obs['checks_wall_seconds'] is not None else None
        obs['parent_observed_wall_seconds']=elapsed(states[d['dispatch_index']].get('resumed_at_utc',states[d['dispatch_index']]['assignment_recorded_at_utc']),states[d['dispatch_index']]['completion_observed_at_utc'])
        for jid,jrows in judgments.items():
            if not all(rid in jrows for rid in disc_ids):continue
            # For zero-output runs use the plan to distinguish covered from absent judges.
            if not disc_ids and q not in next(x['qids'] for x in load('judging/plan.json')['judges'] if x['judge_id']==jid):continue
            pool=useful_pools[jid][q];valid={mapping[rid]['pool_entity'] for rid in disc_ids if str(jrows[rid]['relevance'])=='1'}
            counts=collections.Counter(str(jrows[rid]['relevance']) for rid in disc_ids)
            obs.update({jid+'_pool_relevant':len(pool),jid+'_pool_retrieved':len(retrieved_pool&pool),
                        jid+'_pool_recall':ratio(len(retrieved_pool&pool),len(pool)),
                        jid+'_row_valid_pool_recall':ratio(len(valid),len(pool)),
                        jid+'_related_rows':counts['1'],jid+'_N_rows':counts['N'],jid+'_unrelated_rows':counts['0'],
                        jid+'_unknown_rows':counts['U'],
                        jid+'_first_related_rank':min([mapping[rid]['rank'] for rid in disc_ids if str(jrows[rid]['relevance'])=='1'] or [11])})
        observations.append(obs)
    save('analysis/per_question.json',observations);save('analysis/candidate-observations.json',candidate_rows);save('analysis/check-observations.json',check_rows)
    save('analysis/probe-truth-sensitivity.json',{'probes':list(probe_truth.values()),
         'counts':dict(collections.Counter(r['status'] for r in probe_truth.values())),
         'limits':'Exploratory sensitivity added after a T023 execution raised a signup/authentication scope concern. Frozen primary denominators and H1 thresholds remain unchanged. The supported-only subset requires both condition-hidden reason rows to affirm the frozen violation; this is internal agreement, not independent human truth.'})
    columns=list(dict.fromkeys(k for row in observations for k in row))
    with (ROOT/'analysis/per_question.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=columns);writer.writeheader();writer.writerows(observations)
    print({'run_observations':len(observations),'candidate_observations':len(candidate_rows),'check_observations':len(check_rows),'sampled_claims':sum(r['sampled_claims'] for r in observations)})
if __name__=='__main__':main()
