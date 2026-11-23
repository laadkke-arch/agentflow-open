"""Independent, descriptive audit of Aslett Study 1 author files.

Uses only stdlib; does not import the supplement agent's extraction code.
Inputs must already have been fetched from author commit
7b4ffee080be622e06f6197bfd095a3e4faebd16 by its documented retrieval command.
No participant identifiers or verbatim participant answers are emitted.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
import csv
import hashlib
import json

BASE = Path(__file__).resolve().parent
DATA = BASE.parent / 'supplement' / 'cache' / 'aslett'
SHA = '7b4ffee080be622e06f6197bfd095a3e4faebd16'


def read(name):
    content = (DATA / name).read_bytes()
    try:
        text = content.decode('utf-8-sig')
    except UnicodeDecodeError:
        text = content.decode('cp1252')
    return list(csv.DictReader(text.splitlines())), {
        'file': name, 'sha256': hashlib.sha256(content).hexdigest(),
        'url': f'https://github.com/SMAPPNYU/Do_Your_Own_Research/blob/{SHA}/Data/{name}'}


def identity(r):
    return r['ResponseId'], r['Article_day']


def run():
    reduced, reduced_receipt = read('Study_1_df_FM.csv')
    original, original_receipt = read('Search_Exp_Misl_False.csv')
    true, true_receipt = read('Study_1_df_T.csv')
    reduced_keys = {identity(r) for r in reduced if all(v not in ('', 'NA') for v in r.values())}
    false_complete = [r for r in original if identity(r) in reduced_keys]
    true_fields = ('True_Dummy', 'Treat_Search', 'Age', 'Dummy_Congruence',
                   'Education_Score', 'Gender', 'Income_Score', 'Article_day', 'ResponseId')
    true_complete = [r for r in true if r['Article'] in ('1','2','3','4','5')
                     and all(r[f] not in ('', 'NA') for f in true_fields)]
    groups = []
    for sample, false_rows, true_rows in (
            ('all_observed_categorical_response', original, true),
            ('author_complete_case', false_complete, true_complete)):
        for truth, rows in (('FM', false_rows), ('T', true_rows)):
            for arm in ('0', '1'):
                subset = [r for r in rows if r['Treat_Search'] == arm]
                counts = Counter({'True': 'T', 'Misl/False': 'FM'}.get(r['Evaluation'],r['Evaluation']) for r in subset)
                n = sum(counts[x] for x in ('T','FM','CND'))
                groups.append(dict(sample=sample,truth=truth,arm=arm,
                    T=counts['T'],FM=counts['FM'],CND=counts['CND'],observed=n,
                    file_NA=counts['NA']+counts[''],people_observed=len({r['ResponseId'] for r in subset if r['Evaluation'] not in ('','NA')}),
                    accepted=counts['T'],correct=counts[truth]))
    contrasts = []
    for i in range(0,len(groups),2):
        c,t = groups[i:i+2]
        acc = 100*(Fraction(t['accepted'],t['observed'])-Fraction(c['accepted'],c['observed']))
        corr = 100*(Fraction(t['correct'],t['observed'])-Fraction(c['correct'],c['observed']))
        contrasts.append(dict(sample=c['sample'],truth=c['truth'],acceptance_difference_pp=float(acc),
            acceptance_exact_fraction=str(acc),final_accuracy_difference_pp=float(corr),final_accuracy_exact_fraction=str(corr)))
    combined = []
    for sample in ('all_observed_categorical_response','author_complete_case'):
        for arm in ('0','1'):
            rows=[r for r in groups if r['sample']==sample and r['arm']==arm]
            n=sum(r['observed'] for r in rows);a=sum(r['correct'] for r in rows)
            combined.append(dict(sample=sample,arm=arm,correct=a,observed=n,accuracy_pct=100*a/n,
                interpretation='Only author-classified T/FM observed trials; original randomized population and indeterminate-truth items are not this denominator.'))
    witnesses=[]
    for record in (155,16):
        r=original[record-1]
        witnesses.append(dict(file='Search_Exp_Misl_False.csv',record_excluding_header=record,
            person_item_key_sha256=hashlib.sha256(('\t'.join(identity(r))).encode()).hexdigest(),
            Article_day=r['Article_day'],assigned_Treat_Search=r['Treat_Search'],author_truth=r['mode'],
            categorical_final=r['Evaluation'],author_Susc_FN=r['Susc_FN'],in_complete_case=identity(r) in reduced_keys,
            manually_checked_acceptance=1,manually_checked_final_correct=0,
            check='False/misleading author key + True final = acceptance1, correct0; original key joins reduced file.'))
    expected=json.loads((BASE.parent/'supplement'/'aslett-aggregates.json').read_text())
    disagreement=[]
    for g in groups:
        match=next(r for r in expected['groups'] if r['cohort']=='ASLETT2024-STUDY1' and r['sample']==g['sample'] and r['truth_key']==g['truth'] and r['assigned_condition']==('control' if g['arm']=='0' else 'search_encouragement'))
        for a,b in (('accepted','acceptance_n'),('observed','acceptance_N'),('correct','final_correct_n'),('CND','CND_n')):
            if g[a]!=match[b]:disagreement.append(dict(group=g,field=a,other=match[b]))
    result=dict(verified_utc=datetime.now(timezone.utc).isoformat(),reader='root AI independent coding pass',
        author_commit=SHA,inputs=[reduced_receipt,original_receipt,true_receipt],groups=groups,contrasts=contrasts,
        combined_observed_accuracy=combined,witnesses=witnesses,aggregate_disagreements=disagreement,
        assigned_N='미확인',assigned_missing_m='미확인',assigned_acceptance_bounds='미확인',
        inference='No new p-values or cluster-ignorant intervals. Complete-case and all-observed comparisons remain distinct.')
    assert not disagreement, disagreement
    assert all(w['in_complete_case'] and w['categorical_final']=='True' and w['author_truth']=='Misl/False' for w in witnesses)
    (BASE/'independent-calculation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(groups=groups,contrasts=contrasts,combined=combined,disagreements=len(disagreement)),ensure_ascii=False,indent=2))


if __name__ == '__main__':
    run()
