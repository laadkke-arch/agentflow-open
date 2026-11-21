#!/usr/bin/env python3
"""Calculate registered paired metrics and explicitly named sensitivities."""
import collections,csv,itertools,json,statistics
from fractions import Fraction
from common import ROOT,load,save
from bootstrap import paired_interval

METRICS={
 'grade2_hit_at10':('mean','grade2_hit',None,None,'question hit rate; grade2-eligible questions'),
 'grade2_entity_recall_at10_micro':('ratio',None,'grade2_retrieved','gold2_count','auxiliary: unique frozen grade2 entities retrieved / all frozen grade2 entities'),
 'gold_recall_at10_macro':('mean','gold_recall',None,None,'mean within-question known-gold recall'),
 'gold_recall_at10_micro':('ratio',None,'retrieved_relevant','gold_relevant_count','retrieved/frozen relevant entities'),
 'first_related_rank_median':('median','first_known_related_rank',None,None,'rank; no known hit=11, all questions'),
 'first_related_rank_gold_eligible':('median','first_known_related_rank_gold_eligible',None,None,'rank; gold-eligible questions only'),
 'first_related_rank_hit_only':('median','first_known_related_rank_hit_only',None,None,'rank; descriptive common hit-question pairs only'),
 'current_N_per_output':('ratio',None,'current_scoped_N_candidates','output_candidates','scope-verified knownN / returned candidates'),
 'current_N_per10slots':('ratio',None,'current_scoped_N_candidates','max_slots','scope-verified knownN / maximum10 slots per question'),
 'historical_N_per_output':('ratio',None,'historical_N_candidates','output_candidates','historicalN identity matches / returned candidates; scope sensitivity only'),
 'strict_N_correct_reject':('ratio',None,'strict_N_correct_reject','strict_N_denominator','excluded with correct reason / frozen current strictN probes'),
 'strict_N_exclude_only':('ratio',None,'strict_N_excluded','strict_N_denominator','excluded / frozen current strictN probes'),
 'auditor_confirmed_N_correct_reject':('ratio',None,'auditor_confirmed_N_correct_reject','auditor_confirmed_N_denominator','exploratory: correctly rejected / probes whose frozen violation is affirmed for both condition-hidden audit rows'),
 'auditor_confirmed_N_exclude_only':('ratio',None,'auditor_confirmed_N_excluded','auditor_confirmed_N_denominator','exploratory: excluded / probes whose frozen violation is affirmed for both audit rows'),
 'strict_N_audit_supported_fraction':('ratio',None,'auditor_confirmed_N_denominator','strict_N_denominator','internally re-affirmed frozen violations / all frozen strictN probes'),
 'positive_false_reject':('ratio',None,'positive_excluded','positive_denominator','excluded / external-record positive probes'),
 'grade2_probe_false_reject':('ratio',None,'positive_grade2_excluded','positive_grade2_denominator','excluded / external grade2 probes'),
 'unrelated_reject':('ratio',None,'unrelated_excluded','unrelated_denominator','excluded / frozen unrelated probes'),
 'claim_error':('ratio',None,'claims_false','claims_verifiable','false / (true+false), current official-document check'),
 'claim_unknown':('ratio',None,'claims_unknown','sampled_claims','unknown / all sampled assertions'),
 'claim_error_lower':('ratio',None,'claims_false','sampled_claims','false / all sampled assertions'),
 'claim_error_upper':('ratio',None,'claims_false_or_unknown','sampled_claims','(false+unknown) / all sampled assertions'),
 'claim_URL_missing_rate':('ratio',None,'claims_without_supplied_URL','factual_claims','assertions without a supplied URL / extracted assertions'),
 'pre_only_known_recall':('mean','pre_only_recall',None,None,'known-gold recall using only explicitly dated pre-question candidates'),
}
for label,field,unit in [
 ('queries_mean','queries','literal queries'),('declared_opens_mean','declared_open_budget','executor-declared open charges'),
 ('normalized_opens_mean','normalized_document_budget','unique opened URLs plus failed open attempts'),
 ('unique_urls_mean','unique_successfully_opened_urls','unique opened URLs, including partial responses'),
 ('failed_opens_mean','failed_open_attempts','failed/unreadable open attempts'),
 ('raw_words_mean','raw_response_words','English whitespace words, original raw_response'),
 ('uncertainty_items_mean','uncertainty_items','distinct explicitly uncertain candidate propositions'),
 ('URLless_assertions_mean','claims_without_supplied_URL','assertions without supplied URL'),
 ('referenceless_assertions_mean','claims_without_any_supplied_reference','assertions without supplied URL or printed tool citation'),
 ('unresolved_citation_assertions_mean','claims_with_unresolved_citations','assertions with printed but unresolved source references'),
 ('homepage_only_assertions_mean','claims_with_homepage_only','assertions with homepage-only linkage'),
 ('assertions_mean','factual_claims','all extracted atomic assertions before sampling'),
 ('candidates_mean','output_candidates','returned discovery candidates'),
 ('wall_seconds_mean','total_wall_seconds','recorded total wall seconds including parent waiting'),
 ('active_seconds_mean','recorded_active_seconds','sum of recorded discovery and check intervals'),
 ('parent_wall_seconds_mean','parent_observed_wall_seconds','parent assignment-to-completion observation seconds'),
 ('stage1_queries_mean','stage1_queries','discovery queries before checks'),
 ('stage1_opens_mean','stage1_document_budget','normalized discovery open charges'),
 ('post_documents_mean','post_question_document_count','document events explicitly after question date'),
 ('unknown_date_documents_mean','unknown_date_document_count','document events with unknown/mixed date')]:
    METRICS[label]=('mean',field,None,None,unit)
for judge in ['primary','secondary']:
    METRICS[judge+'_pool_recall']=('mean',judge+'_pool_recall',None,None,'mean recall of independently confirmed entities in discovery pool')
    METRICS[judge+'_row_valid_pool_recall']=('mean',judge+'_row_valid_pool_recall',None,None,'same pool denominator; only individually relevant rows retrieve')
    METRICS[judge+'_N_rate']=('ratio',None,judge+'_N_rows','output_candidates','blindN rows / returned candidates; judge-covered questions')
    METRICS[judge+'_useful_rate']=('ratio',None,judge+'_related_rows','output_candidates','blind1 rows / returned candidates; U retained in denominator')
    METRICS[judge+'_first_rank']=('median',judge+'_first_related_rank',None,None,'blind first useful rank; absent=11')

def groups(pairs):
    allq=sorted(pairs);out=[('all','all53 questions',allq)]
    for field,values in [('cohort',['011','new']),('input_mode',['original','summary']),
                         ('whole_or_part',['whole','part']),('must_present',[False,True]),('I5',['absent','present']),
                         ('strict_N_origin',['historical011','constructed'])]:
        for value in values:out.append((f'{field}={value}',f'{field}={value}',[q for q in allq if pairs[q]['A'][field]==value]))
    for cohort,scope,i5,must in itertools.product(['011','new'],['whole','part'],['absent','present'],[False,True]):
        qs=[q for q in allq if (pairs[q]['A']['cohort'],pairs[q]['A']['whole_or_part'],pairs[q]['A']['I5'],pairs[q]['A']['must_present'])==(cohort,scope,i5,must)]
        out.append((f'stratum:{cohort}/{scope}/{i5}/{must}',f'{cohort} × {scope} × I5 {i5} × must {must}',qs))
    out.append(('no_recorded_exposure','exploratory: both runs without recorded excluded-source exposure',[q for q in allq if pairs[q]['A']['exposure_count']==pairs[q]['P']['exposure_count']==0]))
    code_deviations={r['qid'] for r in load('analysis/code-search-audit.json',{'deviations':[]})['deviations']}
    out.append(('explicit_code_search_both','exploratory: exclude pairs with a missing explicit code-search attempt record',[q for q in allq if q not in code_deviations]))
    out.append(('exclude_changed_adoption_cases','frozen planned sensitivity excluding N004,N005,N010,N020',[q for q in allq if q not in ['N004','N005','N010','N020']]))
    out.append(('exclude_procedural_positive_T054','positive-probe sensitivity without procedural T054',[q for q in allq if q!='T054']))
    out.append(('011_main','original011 main sample30',[q for q in allq if pairs[q]['A']['cohort']=='011' and pairs[q]['A']['source_subset']=='main']))
    out.append(('calendar_before_2026_06_01','exploratory calendar-date sensitivity: before2026-06-01',[q for q in allq if pairs[q]['A']['question_date']<'2026-06-01']))
    out.append(('calendar_on_or_after_2026_06_01','exploratory calendar-date sensitivity: on/after2026-06-01',[q for q in allq if pairs[q]['A']['question_date']>='2026-06-01']))
    out.append(('exclude_recent_011_questions','exploratory: remove4 recent011 questions; do not relabel them as new',[q for q in allq if not(pairs[q]['A']['cohort']=='011' and pairs[q]['A']['question_date']>='2026-06-01')]))
    secondary=next(j['qids'] for j in load('judging/plan.json')['judges'] if j['judge_id']=='secondary')
    out.append(('secondary_common_questions','same20 questions for comparing judging-source order',secondary))
    return out

def eligible(pair,kind,field,numerator,denominator,metric):
    if metric.startswith(('primary_','secondary_')):
        prefix=metric.split('_')[0]
        if any(prefix+'_pool_relevant' not in pair[c] for c in ['A','P']):return False
    if kind=='ratio':return sum(pair[c].get(denominator,0) or 0 for c in ['A','P'])>0
    return all(pair[c].get(field) is not None for c in ['A','P'])

def main():
    data=load('analysis/per_question.json');pairs=collections.defaultdict(dict)
    for row in data:pairs[row['qid']][row['condition']]=row
    expected={q['id'] for q in load('questions/metadata.json')}
    assert set(pairs)==expected and all(set(v)=={'A','P'} for v in pairs.values())
    results=[]
    for gid,label,qs in groups(pairs):
        for metric,(kind,field,numerator,denominator,unit) in METRICS.items():
            selected=[q for q in qs if eligible(pairs[q],kind,field,numerator,denominator,metric)]
            estimate=paired_interval([pairs[q] for q in selected],kind,numerator,denominator,field)
            r={'group':gid,'group_label':label,'group_questions':len(qs),'metric':metric,'unit':unit,
               'kind':kind,'field':field,'numerator_field':numerator,'denominator_field':denominator,
               'eligible_qids':selected,**estimate}
            if kind=='ratio':
                for c in ['A','P']:
                    r['numerator_'+c]=sum(pairs[q][c].get(numerator,0) or 0 for q in selected)
                    r['denominator_'+c]=sum(pairs[q][c].get(denominator,0) or 0 for q in selected)
            else:
                r['denominator_A']=r['denominator_P']=len(selected)
                if kind=='mean' and field=='grade2_hit':
                    for c in ['A','P']:r['numerator_'+c]=sum(pairs[q][c][field] for q in selected)
            results.append(r)
    save('analysis/bootstrap_intervals.json',{'seed':18018,'iterations':10000,'difference_direction':'P minus A','rows':results})
    hit_descriptives=[]
    for gid,label,qs in groups(pairs):
        for c in ['A','P']:
            hit_qids=[q for q in qs if pairs[q][c]['first_known_related_rank_hit_only'] is not None]
            values=[pairs[q][c]['first_known_related_rank_hit_only'] for q in hit_qids]
            hit_descriptives.append({'group':gid,'condition':c,'hit_questions':len(values),'group_questions':len(qs),
                                    'median_rank':statistics.median(values) if values else None,'qids':hit_qids,
                                    'interpretation':'Condition-specific hit-only descriptive; A/P may contain different questions, so this is not a paired causal contrast.'})
    save('analysis/hit-only-descriptives.json',hit_descriptives)
    columns=['group','group_label','group_questions','metric','unit','questions','A','P','difference','ci_low','ci_high','numerator_A','denominator_A','numerator_P','denominator_P','valid_replicates','small_stratum']
    with (ROOT/'analysis/metrics.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=columns,extrasaction='ignore');w.writeheader()
        for r in results:w.writerow({**r,'ci_low':r['ci95'][0],'ci_high':r['ci95'][1]})
    primary={r['metric']:r for r in results if r['group']=='all'}
    c1=primary['strict_N_correct_reject'];c2=primary['gold_recall_at10_macro'];c3=primary['claim_error'];c4=primary['positive_false_reject']
    def exact_ratio_difference(r):
        return Fraction(r['numerator_P'],r['denominator_P'])-Fraction(r['numerator_A'],r['denominator_A'])
    recall_qs=c2['eligible_qids']
    exact_recall={c:sum((Fraction(pairs[q][c]['retrieved_relevant'],pairs[q][c]['gold_relevant_count']) for q in recall_qs),Fraction())/len(recall_qs) for c in ['A','P']} if recall_qs else None
    criteria=[{'criterion':'C1','observed_difference':c1['difference'],'met':None if c1['difference'] is None else exact_ratio_difference(c1)>=Fraction(1,5),'ci95':c1['ci95']},
              {'criterion':'C2','observed_difference':c2['difference'],'met':None if exact_recall is None else exact_recall['P']-exact_recall['A']>=Fraction(-1,20),'ci95':c2['ci95']},
              {'criterion':'C3','observed_difference':c3['difference'],'met':None if c3['difference'] is None else exact_ratio_difference(c3)<0,'ci95':c3['ci95']},
              {'criterion':'C4_aux','observed_difference':c4['difference'],'met':None if c4['difference'] is None else exact_ratio_difference(c4)<=Fraction(1,20),'ci95':c4['ci95']}]
    core=[r['met'] for r in criteria[:3]]
    conclusion='unjudgeable' if any(v is None for v in core) else 'narrow_operational_support' if all(core) else 'unsupported_in_this_setting' if not any(core) else 'mixed_results'
    save('analysis/H1.json',{'criteria':criteria,'point_threshold_status':conclusion,
                           'C1_ceiling_diagnostic':{'maximum_possible_P_minus_observed_A':None if c1['A'] is None else 1-c1['A'],
                                                    'threshold_reachable_given_observed_A':None if not c1.get('denominator_A') else 1-Fraction(c1['numerator_A'],c1['denominator_A'])>=Fraction(1,5),
                                                    'interpretation':'Descriptive ceiling conditional on the observed baseline. Does not relax C1 or assert equality; probe hardness and baseline strength limit attainable improvement.'},
                           'rule':'Registered point thresholds; intervals and judging-source reversals remain material qualifiers. No human review-time claim.'})
    print(json.dumps({'groups':len(groups(pairs)),'metric_rows':len(results),'H1_point_status':conclusion,'criteria':criteria},ensure_ascii=False))
if __name__=='__main__':main()
