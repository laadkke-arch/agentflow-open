"""Join frozen decisions to later criterion rows; preserve unresolved rows and all filters."""
import collections,csv,json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def readl(n):return [json.loads(x) for x in (P/n).read_text().splitlines() if x.strip()]
def writej(n,v):(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def writecsv(n,rs):
    keys=list(dict.fromkeys(k for r in rs for k in r))
    with (P/n).open('w',newline='') as f:
        w=csv.DictWriter(f,keys,lineterminator='\n');w.writeheader()
        for r in rs:w.writerow({k:json.dumps(v,ensure_ascii=False,sort_keys=True) if isinstance(v,(dict,list)) else v for k,v in r.items()})
R={r['ref_id']:r for r in readl('references.jsonl')};C={r['ref_id']:r for r in readl('components.jsonl')}
D={(r['ref_id'],r['view']):r for r in csv.DictReader((P/'decisions.csv').open())}
assert len(D)==48
adj=[]
for group in ['gnu','bioc']:
    path=f'adjudicators/{group}/adjudication.jsonl'
    for r in readl(path):adj.append({**r,'criterion_raw_record':path,'criterion_agent':'criterion_'+group})
assert len(adj)==12 and {r['ref_id'] for r in adj}==set(R)
J={r['ref_id']:r for r in adj}
dep=json.loads((P/'evidence/criterion-dependence.json').read_text()) if (P/'evidence/criterion-dependence.json').exists() else {}
for r in adj:r.update(dep.get(r['ref_id'],{}))
writecsv('adjudication.csv',adj)
sameproject={'G01','G02','G03','G04','R01','R04','R05','R06'}
pre={'G06','R04'};provider={'G01'};interpretation={'G06'}
cardhistory={rid for rid,c in C.items() if c['N'].get('card_contains_history')}
sourcehistory={rid for rid,c in C.items() if c['N'].get('source_contains_history')}
# Edition/date-only conservative filter includes explicit source-edition metadata,
# but not observed-query UTC, a section number, or the unversioned GCC URL.
version_only={'G01','G03','G06','R02','R03','R04','R05','R06'}
allids=set(R)
def flag(v):return str(v).lower()=='true'
cleanreader={rid for rid in R if all(not any(flag(D[rid,v][f]) for f in ['background_used','saw_same_case_other_view','saw_prior_outcome']) for v in ['B','BN','BH','BNH'])}
no_related={rid for rid in R if all(not json.loads(D[rid,v]['prior_related_case_ids']) for v in ['B','BN','BH','BNH'])}
same_excerpt={rid for rid in R if dep.get(rid,{}).get('criterion_only_same_excerpt',True)}
filters={
 'all_presealed':allids,
 'reader_same_case_unexposed':cleanreader,
 'exclude_collector_preexposure':allids-pre,
 'exclude_project_target_overlap':allids-sameproject,
 'exclude_project_target_and_preexposure':allids-sameproject-pre,
 'exclude_N_card_history':allids-cardhistory,
 'exclude_N_source_history':allids-sourcehistory,
 'exclude_even_edition_date_markers':allids-version_only,
 'exclude_provider_background':allids-provider,
 'exclude_unstated_qualifier':allids-interpretation,
 'exclude_criterion_same_excerpt_only':allids-same_excerpt,
 'combined_disjoint_no_preexposure_no_card_history':allids-sameproject-pre-cardhistory-provider-interpretation,
 'no_any_reported_prior_related_case':no_related,
 'no_reported_prior_and_no_card_history':no_related-cardhistory,
 'exclude_all_collector_purpose_paraphrase':set(),
 'all_controls_combined':cleanreader-sameproject-pre-cardhistory-provider-interpretation-same_excerpt,
 'external_independent_gold_only':{rid for rid in R if dep.get(rid,{}).get('criterion_external_independent_gold',False)},
}
strata={'all':allids,**{s:{rid for rid,r in R.items() if r['purpose_stratum']==s} for s in ['current','historical','ambiguous']},
        'R_historical':{rid for rid,r in R.items() if rid.startswith('R') and r['purpose_stratum']=='historical'}}
cats=['correct_keep','correct_replace','wrong_replace','wrong_keep','hold','criterion_unresolved']
def score(rid,view):
    j=J[rid];a=D[rid,view]['action'];c=j['criterion_action']
    if not j['confirmed'] or c=='HOLD':return 'criterion_unresolved'
    if a=='HOLD':return 'hold'
    return ('correct_keep' if a=='KEEP' else 'wrong_replace') if c=='KEEP' else ('correct_replace' if a=='REPLACE' else 'wrong_keep')
def counts(ids,view):
    cnt=collections.Counter(score(rid,view) for rid in ids)
    return {c:cnt[c] for c in cats}
def transition(rid,a,b):
    ca,cb=score(rid,a),score(rid,b)
    def group(c):return 'correct' if c.startswith('correct_') else ('wrong' if c.startswith('wrong_') else c)
    return group(ca)+'_to_'+group(cb)
summ=[];detail=[]
for a,b in [('BN','BNH'),('B','BH'),('B','BN')]:
    for fn,fset in filters.items():
        for sn,ss in strata.items():
            ids=sorted(fset&ss)
            ca,cb=counts(ids,a),counts(ids,b)
            confirmed=sum(J[rid]['confirmed'] and J[rid]['criterion_action']!='HOLD' for rid in ids)
            changes=[rid for rid in ids if D[rid,a]['action']!=D[rid,b]['action']]
            row={'comparison':a+'→'+b,'filter':fn,'stratum':sn,'paired_refs':len(ids),'ref_ids':ids,
                 'confirmed_criterion_refs':confirmed,'unresolved_criterion_refs':len(ids)-confirmed,
                 'before':ca,'after':cb,'action_change_ids':changes,
                 'transition_counts':dict(collections.Counter(transition(rid,a,b) for rid in ids)),
                 'conditional_accuracy_before':(ca['correct_keep']+ca['correct_replace'])/confirmed if confirmed else None,
                 'conditional_accuracy_after':(cb['correct_keep']+cb['correct_replace'])/confirmed if confirmed else None,
                 'zero_denominator_label':'해당 없음' if not ids or not confirmed else None}
            summ.append(row)
            if sn!='all':continue
            for rid in sorted(R):
                detail.append({'comparison':a+'→'+b,'filter':fn,'ref_id':rid,'included':rid in ids,
                    'stratum':R[rid]['purpose_stratum'],'before_view':a,'after_view':b,
                    'before_action':D[rid,a]['action'],'after_action':D[rid,b]['action'],
                    'criterion_action':J[rid]['criterion_action'],'criterion_confirmed':J[rid]['confirmed'],
                    'before_score':score(rid,a),'after_score':score(rid,b),'transition':transition(rid,a,b),
                    'action_changed':D[rid,a]['action']!=D[rid,b]['action'],
                    'before_reader':D[rid,a]['reader_id'],'after_reader':D[rid,b]['reader_id'],
                    'before_input_sha256':D[rid,a]['input_sha256'],'after_input_sha256':D[rid,b]['input_sha256']})
writecsv('sensitivity.csv',detail)
writej('evidence/analysis-summary.json',{'views':{v:counts(sorted(R),v) for v in ['B','BN','BH','BNH']},'comparisons':summ,
    'candidate_uri_changes_at_fixed_N':[{'ref_id':rid,'BN_uri':D[rid,'BN']['replacement_url'] or None,'BNH_uri':D[rid,'BNH']['replacement_url'] or None,'BN_verified_in_packet':flag(D[rid,'BN']['replacement_verified_in_packet']),'BNH_verified_in_packet':flag(D[rid,'BNH']['replacement_verified_in_packet']),'criterion_uri':J[rid]['replacement_url'],'not_a_verified_URI_gain_in_reader_task':True} for rid in R if D[rid,'BN']['replacement_url']!=D[rid,'BNH']['replacement_url']],
    'filter_sets':{k:sorted(v) for k,v in filters.items()},'history_flags':{'card':sorted(cardhistory),'whole_source':sorted(sourcehistory),'including_edition_markers':sorted(version_only)},
    'inference_limits':['one internally related model family','one reading per case/view','source-authority dependence retained','no human click/task completion outcome','filters are descriptive; no effect estimate or generalization']})
writej('evidence/case-overlap.json',{'preexposed_collector_cases':sorted(pre),'same_project_or_target_graph_cases':sorted(sameproject),
    'edges':[{'cases':['G01','G02'],'reason':'same original Bash distribution'},
             {'cases':['G03','G04'],'reason':'same original gawk-doc distribution and historical gawk manual'},
             {'cases':['G01','G03'],'reason':'same POSIX2018 target manuscript'},
             {'cases':['R01','R04'],'reason':'DESeq2 original consumer and another case target'},
             {'cases':['R04','R05','R06'],'reason':'SingleCellExperiment original distribution and target; scater reciprocal consumer/target'}],
    'source':'review/base-audit.json AUD-D03/D04; collectors/bioc/overlap-evidence.json',
    'conservative_graph_filter_is_not_measured_contamination':True,
    'prior_related_self_reports_are_broader_than_this_graph':True})
print(json.dumps({'views':{v:counts(sorted(R),v) for v in ['B','BN','BH','BNH']},'filters':{k:len(v) for k,v in filters.items()}},ensure_ascii=False))
