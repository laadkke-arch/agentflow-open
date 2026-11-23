"""Aggregate public author records without publishing any participant identifiers.

Run from the repository root. Uses only Python standard library. --download
retrieves exact pinned author files. Does not run author experimental software.
"""
import argparse
import collections
import csv
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / '_cache' / 'inputs'
INPUTS = {
 'bansal-filter.csv': ('https://raw.githubusercontent.com/uw-hai/Complementary-Performance/6cebab4ffd2b332ebec5e27e7632e7bf1c36ba5f/experiment-data/decision-result-filter.csv', ROOT/'_cache/bansal-data/experiment-data/decision-result-filter.csv'),
 'bansal-prefilter.csv': ('https://raw.githubusercontent.com/uw-hai/Complementary-Performance/6cebab4ffd2b332ebec5e27e7632e7bf1c36ba5f/experiment-data/decision-result-prefilter.csv', ROOT/'_cache/bansal-data/experiment-data/decision-result-prefilter.csv'),
 'lai-label.jsonlist.gz': ('https://raw.githubusercontent.com/vivlai/deception-machine-in-the-loop/7c5ae6bb4b7dcd5613e620e4731b9c3c67ed8285/label.jsonlist.gz', ROOT/'_cache/lai-data/label.jsonlist.gz'),
}
EXPECTED_SHA256 = {
 'bansal-filter.csv': '0cc48875d451e095db8307e7b2cf616d5ad2277e200c8d2579e07db174c1f9f0',
 'bansal-prefilter.csv': '1074a05e0a4f113a1f8b8bfe8a887f455ad57dec5a4838fbe5357c85e3e84af6',
 'lai-label.jsonlist.gz': 'd3616e73d4db03d6e21f574246d318e7f0300facdfe6ff88aa2630cef8364c5f',
}

def write(name, data):
    (ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def read_inputs(download):
    CACHE.mkdir(parents=True,exist_ok=True)
    receipt=[]; data={}
    for name,(url,existing) in INPUTS.items():
        t=dt.datetime.now(dt.timezone.utc).isoformat(); path=CACHE/name
        if download:
            with urllib.request.urlopen(url,timeout=60) as r:
                content=r.read();status=r.status
            path.write_bytes(content);method='pinned URL download'
        else:
            path=existing if existing.exists() else path
            content=path.read_bytes();status=None;method='read previously cloned pinned repository'
        assert hashlib.sha256(content).hexdigest()==EXPECTED_SHA256[name], name+' content changed'
        data[name]=content
        receipt.append({'name':name,'url':url,'utc':t,'method':method,'http_status':status,'bytes':len(content),'sha256':hashlib.sha256(content).hexdigest()})
    write('input-receipt.json',receipt)
    return data

def count_groups(rows, cohort, keyfn):
    grouped=collections.defaultdict(list)
    for r in rows:grouped[(r['task'],r['condition'])].append(r)
    result=[]
    for (task,cond),xs in sorted(grouped.items()):
        people=len({r['person'] for r in xs})
        for correctness in [True,False]:
            ys=[r for r in xs if (r['prediction']==r['truth'])==correctness]
            has_advice=cond not in ['Human','control','examples','heatmap','highlight']
            a=sum(r['final']==r['prediction'] for r in ys) if has_advice else None
            c=sum(r['final']==r['truth'] for r in ys)
            third=sum(r['final']!=r['prediction'] and r['final']!=r['truth'] for r in ys) if has_advice else None
            result.append({'study_id':cohort.split(':')[0],'dataset':task,'analysis_set':cohort,'condition':cond,'advice_correct':correctness,'unit':'published final-response record','unique_anonymous_person_keys':people,'denominator':len(ys),'accept_count':a,'correct_count':c,'other_wrong_count':third,'accept_rate':a/len(ys) if a is not None and ys else None,'final_accuracy':c/len(ys) if ys else None,'missing_final_in_this_file':0,'original_assigned_missing':'unknown','preanswer_switch':'not recorded','actual_explanation_reading':'unknown','source_id':'DI-BAN-DATA' if cohort.startswith('D01') else 'DI-LAI-DATA'})
    return result

def bansal(content):
    raw=list(csv.DictReader(content['bansal-filter.csv'].decode().splitlines()))
    pre=list(csv.DictReader(content['bansal-prefilter.csv'].decode().splitlines()))
    def key(r):return tuple(r[k] for k in ['task','condition','assignmentId','questionId'])
    by=collections.defaultdict(list)
    for r in raw:by[key(r)].append(r)
    dup={k:v for k,v in by.items() if len(v)>1}
    normalized=[dict(task=r['task'],condition=r['condition'],person=r['assignmentId'],question=r['questionId'],prediction=r['pred'],truth=r['y'],final=r['choice']) for r in raw]
    unique_only=[n for r,n in zip(raw,normalized) if len(by[key(r)])==1]
    itemmap=collections.defaultdict(set)
    for r in raw:itemmap[(r['task'],r['questionId'])].add(tuple(r[k] for k in ['y','pred','conf','pred2','conf2']))
    audit={'filtered_rows':len(raw),'prefilter_rows':len(pre),'filtered_key_duplicates':len(raw)-len(by),'ambiguous_key_groups':len(dup),'ambiguous_records':sum(len(v) for v in dup.values()),'ambiguous_person_keys':len({k[2] for k in dup}),'duplicate_choice_conflicts':sum(len({r['choice'] for r in v})>1 for v in dup.values()),'duplicate_time_conflicts':sum(len({r['time'] for r in v})>1 for v in dup.values()),'complete_same_row_core_columns':all(r[k]!='' for r in raw for k in ['assignmentId','questionId','task','condition','choice','y','pred','conf']),'task_question_recommendation_truth_confidence_conflicts':sum(len(v)>1 for v in itemmap.values()),'filtered_keys_not_in_prefilter':len(set(by)-{key(r) for r in pre}),'no_arbitrary_deduplication':True,'cohort_not_recruitment_roster':True,'duplicate_conditions':[{ 'task':t,'condition':c,'ambiguous_keys':sum(k[:2]==(t,c) for k in dup)} for t,c in sorted({k[:2] for k in dup})]}
    bycond=[]
    for t,c in sorted({(r['task'],r['condition']) for r in raw}):
        xs=[r for r in raw if (r['task'],r['condition'])==(t,c)];ps=[r for r in pre if (r['task'],r['condition'])==(t,c)]
        bycond.append({'task':t,'condition':c,'filtered_records':len(xs),'filtered_person_keys':len({r['assignmentId'] for r in xs}),'prefilter_records':len(ps),'prefilter_person_keys':len({r['assignmentId'] for r in ps}),'excluded_records':len(ps)-len(xs),'excluded_person_keys':len({r['assignmentId'] for r in ps})-len({r['assignmentId'] for r in xs}),'assigned_N':'unknown; screening roster unavailable'})
    audit['denominators']=bycond
    write('bansal-audit.json',audit)
    return count_groups(normalized,'D01:author-filtered-records',key)+count_groups(unique_only,'D01:unambiguous-key-subset',key)

def lai(content):
    raw=[json.loads(x) for x in gzip.decompress(content['lai-label.jsonlist.gz']).decode().splitlines()]
    core=['experiment','anonymized_worker_id','review_num','actual_label','user_label','predicted_label']
    assert all(r[k] is not None for r in raw for k in core)
    ks=[(r['experiment'],r['anonymized_worker_id'],r['review_num']) for r in raw]
    bytext=collections.defaultdict(list)
    for r in raw:bytext[hashlib.sha256(r['review_text'].encode()).hexdigest()].append(r)
    audit={'rows':len(raw),'people':len({r['anonymized_worker_id'] for r in raw}),'duplicate_person_condition_order_keys':len(ks)-len(set(ks)),'unique_exact_review_texts':len(bytext),'truth_conflicts_by_exact_text':sum(len({r['actual_label'] for r in g})>1 for g in bytext.values()),'prediction_conflicts_by_exact_text':sum(len({r['predicted_label'] for r in g if r['predicted_label']!='N.A.'})>1 for g in bytext.values()),'N_A_prediction_rows':sum(r['predicted_label']=='N.A.' for r in raw),'assigned_roster':'unknown; published analysis table only','no_positional_join':True,'text_hash_use':'only content consistency audit, not manufactured participant key','denominators':[]}
    for c in sorted({r['experiment'] for r in raw}):
        xs=[r for r in raw if r['experiment']==c]
        audit['denominators'].append({'condition':c,'rows':len(xs),'person_keys':len({r['anonymized_worker_id'] for r in xs}),'unique_texts':len({r['review_text'] for r in xs}),'per_text_count_distribution':dict(collections.Counter(collections.Counter(r['review_text'] for r in xs).values()))})
    audit['columns']=list(raw[0])
    audit['label_values']={k:sorted({str(r[k]) for r in raw}) for k in ['actual_label','user_label','predicted_label']}
    person_conditions=collections.defaultdict(set)
    for r in raw:person_conditions[r['anonymized_worker_id']].add(r['experiment'])
    audit['maximum_conditions_per_person_key']=max(map(len,person_conditions.values()))
    audit['record_count_distribution_per_person_key']=dict(collections.Counter(collections.Counter(r['anonymized_worker_id'] for r in raw).values()))
    write('lai-audit.json',audit)
    # No prediction displayed/recorded for four conditions: do not manufacture advice correctness.
    norm=[dict(task='deception',condition=r['experiment'],person=r['anonymized_worker_id'],question=r['review_num'],prediction=str(r['predicted_label']),truth=str(r['actual_label']),final=str(r['user_label'])) for r in raw if r['predicted_label']!='N.A.']
    return count_groups(norm,'D04:published-analysis-records',lambda r:None)

def contrasts(outcomes):
    out=[]
    for setname,task in sorted({(r['analysis_set'],r['dataset']) for r in outcomes}):
        allrows=[r for r in outcomes if (r['analysis_set'],r['dataset'])==(setname,task)]
        base='Conf.' if setname.startswith('D01') else 'machine'
        for cond in sorted({r['condition'] for r in allrows}-{base,'Human'}):
            for correct in [True,False]:
                i=next(r for r in allrows if r['condition']==cond and r['advice_correct']==correct)
                b=next(r for r in allrows if r['condition']==base and r['advice_correct']==correct)
                out.append({'study_id':i['study_id'],'dataset':task,'analysis_set':setname,'intervention':cond,'control':base,'advice_correct':correct,'intervention_accept':i['accept_count'],'intervention_D':i['denominator'],'control_accept':b['accept_count'],'control_D':b['denominator'],'delta_accept_percentage_points':100*(i['accept_rate']-b['accept_rate']),'delta_final_accuracy_percentage_points':100*(i['final_accuracy']-b['final_accuracy']),'unit':'descriptive response-record ratio; no iid participant inference','source_id':i['source_id']})
    return out

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--download',action='store_true');args=a.parse_args()
    started=dt.datetime.now(dt.timezone.utc).isoformat()
    inputs=read_inputs(args.download);result=bansal(inputs)+lai(inputs)
    write('outcomes.json',result);write('contrasts.json',contrasts(result))
    write('execution.json',{'command':'python -B docs/workstreams/research/AF-RES-058/streams/diagnostics/reproduce_diagnostics.py'+(' --download' if args.download else ''),'started_utc':started,'ended_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actor':'diagnostics assistant; Python standard library in provided cloud workspace','outcome_rows':len(result),'contrast_rows':len(contrasts(result)),'no_person_rows_emitted':True,'status':'completed'})
    print(json.dumps({'outcome_rows':len(result),'contrast_rows':len(contrasts(result)),'status':'completed'}))
