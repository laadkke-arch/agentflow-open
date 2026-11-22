"""Offline evidence audit. Recomputes published summaries, never runs a human trial.

Run after aggregate.py and build_result.py. A pass means the stated extraction,
joins and arithmetic are internally consistent; it does not resolve unavailable
participant records, publication contradictions or incomplete index coverage.
"""
import argparse
import csv
import hashlib
import json
import math
import re
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, variance

from scipy.stats import t

R = Path(__file__).resolve().parents[1]
REPO = R.parents[3]
OWNED = R.relative_to(REPO).as_posix() + '/'
parser = argparse.ArgumentParser()
parser.add_argument('--phase', choices=['result', 'final'], default='result')
parser.add_argument('--output', default='evidence/validation.json')
args = parser.parse_args()
checks = []

def check(label, condition, detail=None):
    checks.append(dict(check=label, passed=bool(condition), detail=detail))

def jsonl(path):
    return [json.loads(x) for x in (R / path).read_text().splitlines() if x.strip()]

def csvrows(path):
    with (R / path).open(newline='') as f:
        return list(csv.DictReader(f))

def close(a, b):
    return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-8)

sources, attempts = jsonl('sources.jsonl'), jsonl('attempts.jsonl')
studies, effects, screens = (csvrows(p) for p in ['studies.csv', 'effects.csv', 'screening.csv'])
counts = json.loads((R / 'evidence/counts.json').read_text())
source = {x['source_id']: x for x in sources}
effect = {x['comparison_id']: x for x in effects}
experiments = {x['study_id']: x['study_family'] for x in studies}
attempt_ids = {x['attempt_id'] for x in attempts}
check('unique_source_ids', len(source) == len(sources))
check('unique_effect_ids', len(effect) == len(effects))
check('unique_study_arm_ids', len({x['study_row_id'] for x in studies}) == len(studies))
check('unique_attempt_ids', len(attempt_ids) == len(attempts))
check('unique_screening_ids', len({x['screening_id'] for x in screens}) == len(screens))
required_source = ['source_id','type','publisher','original_url','fixed_url','published',
                   'version','checked_utc','read_locator','verified_content','claim_ids',
                   'limitations','study_family','duplicate_group']
missing_source_fields = [(s['source_id'], k) for s in sources for k in required_source if not s.get(k)]
check('all_source_provenance_fields', not missing_source_fields, missing_source_fields)
eligible = [s for s in sources if s['count_minimum']]
category = dict(Counter(s['count_category'] for s in eligible))
check('minimum_unique_originals', len(eligible) >= 24, len(eligible))
check('minimum_categories', category.get('software_primary', 0) >= 10 and
      category.get('design_primary', 0) >= 3 and category.get('learning_primary', 0) >= 3 and
      category.get('artifact', 0) >= 8, category)
check('eligible_urls_not_double_counted', len({s['fixed_url'] for s in eligible}) == len(eligible))
check('eligible_primary_years', all(2005 <= int(re.search(r'20\d{2}', str(s['published'])).group()) <= 2025
      for s in eligible if s['count_category'] != 'artifact'))
join_errors = []
for row in studies + effects:
    rid = row.get('study_row_id', row.get('comparison_id'))
    for sid in json.loads(row['source_ids']):
        if sid not in source or source[sid]['study_family'] != row['study_family']:
            join_errors.append([rid, sid, 'source/family'])
    if row['study_id'] not in experiments or experiments[row['study_id']] != row['study_family']:
        join_errors.append([rid, row['study_id'], 'study/family'])
check('all_study_effect_source_family_experiment_joins', not join_errors, join_errors)
screen_errors = [(x['screening_id'], x['source_id'], x['attempt_id']) for x in screens
                 if (x['source_id'] and x['source_id'] not in source) or
                 (x['attempt_id'] and x['attempt_id'] not in attempt_ids)]
check('screening_source_attempt_joins', not screen_errors, screen_errors)
effect_required=['original_values','recalculation_inputs','formula','recalculated_result',
                 'denominator','calculation_status','noncompletion','locator','reversal_condition']
missing_effect_fields=[(e['comparison_id'],k) for e in effects for k in effect_required if e[k] in ('','{}','null','[]')]
check('all_effect_representative_fields_or_explicit_missing_reasons',not missing_effect_fields,missing_effect_fields)
claimmap = defaultdict(list)
for s in sources:
    for cid in s['claim_ids']:
        claimmap[cid].append(s)
effect_claim_errors = [(e['comparison_id'], c) for e in effects for c in json.loads(e['claim_ids']) if c not in claimmap]
check('effect_claim_join_complete', not effect_claim_errors and all(json.loads(e['claim_ids']) for e in effects), effect_claim_errors)
claimrows = []
for cid, ss in sorted(claimmap.items()):
    claimrows.append(dict(claim_id=cid, kind='existing strand claim evidence index, not a new claim',
        source_ids=[s['source_id'] for s in ss],
        evidence=[dict(source_id=s['source_id'], url=s['fixed_url'], locator=s['read_locator'],
                       verified_content=s['verified_content'], limitations=s['limitations']) for s in ss],
        effect_ids=[e['comparison_id'] for e in effects if cid in json.loads(e['claim_ids'])]))
(R / 'claims.jsonl').write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in claimrows))
core_studies = [s for s in studies if s['included_core'] == 'True']
famgrades = defaultdict(set)
expgrades = {}
for s in core_studies:
    famgrades[s['study_family']].add(s['comparison_grade'])
    expgrades[s['study_id']] = s['comparison_grade']
classes = Counter('direct_comparison' if 'R' in g else 'indirect_comparison' if g & {'Q','U'} else 'no_comparator' for g in famgrades.values())
check('counts_recomputed', counts['source_rows'] == len(sources) and counts['study_arm_rows'] == len(studies)
      and counts['effect_rows'] == len(effects) and counts['screening_rows'] == len(screens)
      and counts['attempt_rows'] == len(attempts) and counts['minimum_by_category'] == category
      and counts['eligible_primary_families'] == len(famgrades) and counts['eligible_experiments'] == len(expgrades)
      and counts['families_by_comparison_class'] == dict(classes)
      and counts['experiments_by_comparison_grade'] == dict(Counter(expgrades.values())))
check('screening_unique_url_count', counts['screening_unique_nonempty_urls'] == len({x['url'] for x in screens if x['url']}))
check('product_link_only_and_rework_zero_are_bounded_findings', counts['product_link_only_direct_families'] == 0
      and counts['post_adoption_rework_labor_compared_families'] == 0)

# Arithmetic is independently recalculated from the preserved inputs below.
numeric_checks = []
def numeric(label, ok, inputs=None):
    numeric_checks.append(dict(comparison=label, passed=bool(ok), inputs=inputs))

for e in effects:
    x = json.loads(e['detail_json'])
    cid = e['comparison_id']
    inp, result = x.get('input'), x.get('result')
    if isinstance(inp, dict) and isinstance(result, dict):
        a = inp.get('treatment', inp.get('intervention', inp.get('I')))
        b = inp.get('control', inp.get('C'))
        if a is not None and b is not None:
            expected = {'difference':a-b, 'delta':a-b, 'difference_min':a-b,
                        'difference_seconds':60*(a-b), 'ratio':a/b,
                        'relative_pct':100*(a-b)/b, 'change_pct':100*(a-b)/b,
                        'delta_pp':100*(a-b)}
            numeric(cid, all(close(result[k], v) for k,v in expected.items() if k in result), inp)
        elif 'EO' in inp and 'free' in inp:
            a, b = mean(inp['EO']), mean(inp['free'])
            numeric(cid, close(result['difference'],a-b) and close(result['ratio'],a/b), inp)
    if 'original_control' in x:
        a, b = x['original_intervention'], x['original_control']
        numeric(cid, close(x['absolute_difference'],a-b) and close(x['ratio'],a/b)
                and close(x['percent_change'],100*(a/b-1)), {'I':a,'C':b})
    if 'recalculated_interval' in x:
        beta, se = x['original_report']['coefficient'], x['original_report']['standard_error']
        numeric(cid+'-Wald', all(close(v,w) for v,w in zip(x['recalculated_interval'],
                [math.exp(beta-1.96*se),math.exp(beta+1.96*se)])), {'beta':beta,'SE':se})
    if 'time_result' in x:
        ni, nc = x['n_intervention'], x['n_control']
        for j, metric in enumerate([x['time_result']] + x['quality_results']):
            delta = metric['mean_intervention'] - metric['mean_control']
            ok = close(delta, metric['difference_intervention_minus_control'])
            if ni is None or nc is None:
                ok = ok and metric['ci95'] is None
            else:
                vi,vc = metric['sd_intervention']**2/ni, metric['sd_control']**2/nc
                se = math.sqrt(vi+vc)
                df = (vi+vc)**2/(vi*vi/(ni-1)+vc*vc/(nc-1))
                width = t.ppf(.975,df)*se
                ok = ok and all(close(a,b) for a,b in zip(metric['ci95'], [delta-width,delta+width]))
            numeric(cid+f'-metric{j}',ok,{'n_I':ni,'n_C':nc,'unit':metric['unit']})
check('published_aggregate_arithmetic', all(x['passed'] for x in numeric_checks),
      {'checks':len(numeric_checks),'failures':[x for x in numeric_checks if not x['passed']]})
eo = json.loads(effect['Ewa-05']['detail_json'])['input']
a,b = eo['EO'],eo['free']; va,vb = variance(a)/len(a), variance(b)/len(b)
df = (va+vb)**2/(va**2/(len(a)-1)+vb**2/(len(b)-1))
ci = [mean(a)-mean(b)-t.ppf(.975,df)*math.sqrt(va+vb),mean(a)-mean(b)+t.ppf(.975,df)*math.sqrt(va+vb)]
eo_receipt = json.loads((R/'streams/software-a/arithmetic-check.json').read_text())['exampleoverflow']['quality_welch95']['ci95']
check('EO_person_level_CI_recomputed', all(close(a,b) for a,b in zip(ci,eo_receipt)), ci)
check('McLaren_n_conflict_CI_withheld', sum(json.loads(e['detail_json']).get('time_result',{}).get('ci_missing_reason') is not None for e in effects) == 5)
check('CodeMend_completion_denominator_derived', close(json.loads(effect['Er-03']['recalculated_result'])['completion_delta_pp'],100*(46-41)/60))
for cid, expected in {
 'XD-LEAHY2020-firstphase':{'fixation_percentage_point_difference':100*(.24-.32)},
 'XL-WESENBERG2022-order':{'mental_load_difference':31.07-34,'calibration_pp_difference':-23.26-(-12.44)},
 'XD-CHAN2024-List_vs_Context':{'score_List_Context':90.4-92.7,'score_List_Dropdown':90.4-93.4}
}.items():
    rr=json.loads(effect[cid]['recalculated_result'])
    check('non_time_point_arithmetic:'+cid,all(close(rr[k],v) for k,v in expected.items()))
chan=[s for s in studies if s['study_family']=='XD-CHAN2011']
check('Chan_conflicting_denominator_not_imputed',all(s['people_assigned']=='' and s['people_completed']==''
      and '151' in s['time_denominator'] and '153' in s['time_denominator'] for s in chan))

result = (R/'RESULT.md').read_text()
lines = result.splitlines()
tables = []
for i,line in enumerate(lines):
    if line.startswith('|') and (i == 0 or not lines[i-1].startswith('|')):
        block=[]; j=i
        while j<len(lines) and lines[j].startswith('|'):
            block.append(lines[j]); j+=1
        tables.append(block)
headers = [
'| 연구군·원문 URL·표/쪽 | 사람 수·할당 단위 | 실제 과제·사전 지식 | 개입·대조·공동 변경 | 시간 정의·전체 분모 | 품질·완료율 | 후속 재작업 관측창·값 | 직접 지지·미확인 |',
'| 비교 ID | 원보고 값·단위 | 재계산 입력·식 | 시간차·품질차·불확실성 | 미완료 처리 | 해석이 뒤집히는 조건 | 데이터·프로토콜 URL |',
'| 제품 주장 | 가까운 직접 비교 | 반대 결과 또는 전이 한계 | 지금 말할 수 있는 범위 | 다음 사람 시험의 판별 기준 |']
check('required_three_tables_immediately_after_title', next(x for x in lines[1:] if x.strip()) == headers[0]
      and [b[0] for b in tables[:3]] == headers and [len(b)-2 for b in tables[:3]] == [22,16,5])
last_header='| 가장 중요한 불일치 또는 약점 | 근거 자료 주소 | 영향을 받는 결론 | 다음 조사 제안과 첫 자료 |'
check('last_table_exact_three_rows_and_no_postscript', tables[-1][0] == last_header and len(tables[-1])-2 == 3
      and result.rstrip().endswith(tables[-1][-1]))
check('Q1_through_Q8', all('## Q'+str(i)+'.' in result for i in range(1,9)))
for token in re.findall(r'\b(?:Rt-[AS]\d{2}|Swa-\d{2}|Swb-[PA]\d{2}|X[dl]-\d{2})\b',result):
    check('result_source_id:'+token, token in source)
required = ['SCOPE.md','manifest.json','screening.csv','studies.csv','effects.csv','measures.md',
            'future-study.md','RESULT.md','sources.jsonl','attempts.jsonl','SELF_CHECK.md','evidence/acceptance-evidence.json']
check('phase4_required_files', all((R/f).is_file() for f in required))
if (R/'SELF_CHECK.md').exists():
    selfcheck=(R/'SELF_CHECK.md').read_text()
    check('SELF_CHECK_Q1_Q8_rows', all(len(re.findall(r'^\| Q'+str(i)+r'\b',selfcheck,re.M)) == 1 for i in range(1,9)))
raw_outside_tmp=[str(p.relative_to(R)) for p in R.rglob('*') if p.is_file() and 'tmp' not in p.parts
                 and p.suffix.lower() in {'.pdf','.png','.jpg','.jpeg','.ipynb'}]
check('no_original_fulltexts_committed', not raw_outside_tmp, raw_outside_tmp)
changed=subprocess.run(['git','diff','--name-only','9668632e915d508e93ddfdc5e8fe4b88bcbfec56'],cwd=REPO,text=True,capture_output=True,check=True).stdout.splitlines()
untracked=subprocess.run(['git','ls-files','--others','--exclude-standard'],cwd=REPO,text=True,capture_output=True,check=True).stdout.splitlines()
outside=[p for p in changed+untracked if not p.startswith(OWNED)]
check('owned_path_only',not outside,outside)
if args.phase == 'final':
    check('handoff_and_receipts_exist',all((R/p).exists() for p in ['HANDOFF.md','evidence/remote-reread.json','evidence/session-check.json']))
    if (R/'evidence/remote-reread.json').exists():
        rr=json.loads((R/'evidence/remote-reread.json').read_text())
        check('fixed_remote_reread_passed',rr.get('all_files_match') is True)
hash_files=required+['claims.jsonl','tools/aggregate.py','tools/build_result.py','tools/verify.py']
receipt=dict(checked_utc=datetime.now(timezone.utc).isoformat(),phase=args.phase,
    command='python -B '+OWNED+'tools/verify.py --phase '+args.phase+' --output '+args.output,
    git_head=subprocess.run(['git','rev-parse','HEAD'],cwd=REPO,capture_output=True,text=True,check=True).stdout.strip(),
    counts=counts,checks=checks,numeric_checks=numeric_checks,
    input_sha256={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in hash_files if (R/p).exists()},
    limitations=['No study participant code or new human trial was executed.','No independent human double coding.',
                'Source version/denominator conflicts are recorded, not resolved by this audit.',
                'Artifact8 counts independent content; strict experimental-only subset7; individual timing raw0.',
                'Native index first30 coverage and some supplementary query provenance remain incomplete.'])
receipt['exit_code']=0 if all(x['passed'] for x in checks) else 1
(R/args.output).write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'exit_code':receipt['exit_code'],'checks':len(checks),'numeric_checks':len(numeric_checks),
                  'failures':[x for x in checks if not x['passed']],'receipt':args.output},ensure_ascii=False))
raise SystemExit(receipt['exit_code'])
