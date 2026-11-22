#!/usr/bin/env python3
"""Verify requested research ledger invariants, without inventing missing evidence."""
import csv
import datetime
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OWNED = 'docs/workstreams/research/AF-RES-047/'
REPO = ROOT.parents[3]


def load(name):
    return json.loads((ROOT / name).read_text())


def rows(name):
    with (ROOT / name).open() as f:
        return list(csv.DictReader(f))


def markdown_tables(text):
    tables, group = [], []
    for line in text.splitlines() + ['']:
        if line.startswith('|'):
            group.append(line)
        elif group:
            if len(group) >= 2 and re.fullmatch(r'[| :\-]+', group[1]):
                tables.append(group)
            group = []
    return tables


def main():
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    checks = []
    def check(name, condition, evidence):
        checks.append({'id':name,'passed':bool(condition),'evidence':evidence})
    cases, summary, counts = load('cases.json'), load('analysis-summary.json'), load('source-count-summary.json')
    sources = [json.loads(line) for line in (ROOT / 'sources.jsonl').read_text().splitlines()]
    readings, frame, sensitivity = rows('readings.csv'), rows('frame.csv'), rows('sensitivity.csv')
    expected = ['RJ01','RJ02','RJ03','N-E00','N-E01','N-E02','RUN01','RUN02']
    check('eight_primary_cases', [c['case_id'] for c in cases] == expected, 'cases.json; consumers.csv data rows1–8')
    check('eight_consumers', len(rows('consumers.csv')) == 8, 'consumers.csv')
    check('all_cases_have_run_slot', {r['case_id'] for r in rows('runs.csv')} == set(expected), 'runs.csv: 6 natural slots + 6 artifact-specific execution rows; cases remain8')
    check('24_configurations', Counter((r['case_id'],r['configuration']) for r in readings) == Counter((c,k) for c in expected for k in 'ABC'), 'readings.csv')
    check('90_real_metadata_exposures',len(frame)==90 and Counter(r['stratum'] for r in frame)=={'consumer_first_RJournal':30,'consumer_first_ESSD':30,'execution_first':30},'frame.csv and original collection row pointers')
    check('40_sensitivity_rows',len(sensitivity)==40 and all(n==5 for n in Counter(r['case_id'] for r in sensitivity).values()),'sensitivity.csv')
    by_case = {c['case_id']:c for c in cases}
    for case_id in expected:
        packet = {r['configuration']:r for r in readings if r['case_id']==case_id}
        check('cumulative_urls_'+case_id, set(json.loads(packet['A']['visible_urls'])) <= set(json.loads(packet['B']['visible_urls'])) <= set(json.loads(packet['C']['visible_urls'])), 'readings.csv visible_urls')
        check('C_axes_'+case_id, all((packet['C'][key]=='True') == by_case[case_id][case_key] for key,case_key in [('publisher_specific','publisher_exists'),('usage_specific','specific_usage'),('run_link','run_link'),('value_checked','value_checked')]), 'cases.json vs readings.csv C; external axes')
        check('C_slot_explicit_'+case_id, packet['C']['C_slot_status'] not in ('','not applicable') and not packet['C']['C_slot_status'].startswith('see evidence'), 'readings.csv C_slot_status')
    for r in readings:
        if r['case_id'].startswith('RUN') and r['configuration'] in 'AB':
            visible = json.dumps({k:v for k,v in r.items() if not k.startswith('audit_only_')},ensure_ascii=False)
            banned = ['63488','4096','CHROM1','END63267','DP0','chromosome1']
            check('no_C_payload_'+r['case_id']+'_'+r['configuration'],not any(v in visible for v in banned),'entire packet excluding audit_only_*; fixed probe field name allowed')
    admitted=[s for s in sources if s['count_toward_minimum']]
    allocation=Counter(s['minimum_category'] for s in admitted)
    check('source_ID_unique',len({s['source_id'] for s in sources})==len(sources),'sources.jsonl source_id')
    check('admitted_work_unique',len({s['work_id'] for s in admitted})==len(admitted),'sources.jsonl work_id with count=true')
    check('source_count_matches',len(sources)==counts['ledger_rows'] and len(admitted)==counts['conservative_unique_direct_works_admitted'] and dict(allocation)==counts['allocation'],'source-count-summary.json recomputed from actual ledger')
    check('minimum24_required_roles',sum(allocation[k] for k in counts['required_allocation'])>=24,'required roles only, excludes supplementary4')
    check('all_role_allocations',all(allocation[k]>=n for k,n in counts['required_allocation'].items()),'8 consumer +8 publisher +4 author +2 officialstatistics +2earthscience')
    check('failures_not_counted',not any(s['access_status'] in ['failed','access_failed','authentication_redirect','tool_fetch_failed','metadata_only'] for s in admitted),'sources.jsonl access_status')
    source_ids={s['source_id'] for s in sources}
    check('case_source_IDs_exist',all(set(c.get('source_ids',[]))<=source_ids for c in cases),'cases.json source_ids')
    required_source=['source_id','work_id','edition_id','source_url','final_url','publisher','kind','published_at','modified_at','opened_utc','checked_utc','locator','observation','limitation','questions','case_ids','duplicate_of','count_toward_minimum','minimum_category']
    check('source_schema',all(all(k in s for k in required_source) for s in sources),'sources.jsonl; unknowns explicit, precision not fabricated')
    for key,subset in [('natural_primary_after_A01',cases[:6]),('execution_supplement',cases[6:])]:
        check('case_counts_'+key,summary[key]['denominator']==len(subset) and all(summary[key][flag]==sum(bool(c.get(flag)) for c in subset) for flag in ['publisher_exists','specific_usage','run_link','local_run_link','value_checked','candidate_value_checked','strict_positive']),'analysis-summary.json vs cases.json')
    check('no_candidate_promotion',not by_case['RJ03']['value_checked'] and by_case['RJ03']['candidate_value_checked'],'RJ03 candidate2 match is not authentic used-edition verification')
    check('local_not_external_run',sum(c['local_run_link'] for c in cases)==2 and sum(c['run_link'] for c in cases)==1 and by_case['RUN02']['run_link'] and not by_case['RUN01']['run_link'],'R_local2; R_external1 after full archive/publisher fingerprint comparison; RUN01 remains unresolved')
    check('local_not_external_usage',not by_case['RUN01']['specific_usage'] and by_case['RUN01']['specific_usage_local'] and by_case['RUN02']['specific_usage'],'external U scope split')
    check('zero_denominator_NA',summary['natural_primary_after_A01']['strict_value_given_authenticated_run']=='해당 없음' and summary['execution_supplement']['strict_value_given_authenticated_run']=={'numerator':0,'denominator':1},'natural conditioning denominator0 is NA; run supplement now has one corroborated external-object connection, V0/1')
    full=load('collection/runs/wetlab-full-fastq-comparison.json')
    check('RUN02_full_content_and_fingerprints',full['archive_matches_declared_sha256'] and full['decoded_content_equal'] and full['archive']['stored_md5']=='52f3ed344d88278c703faa1280818ce1' and not full['publisher_matches_read_checksum_list'],'publisher list388 matches archived gzip; current gzip differs; entire decoded content matches')
    check('record_reread_separate',sum(r['record_reread']=='True' for r in readings if r['configuration']=='C')==4 and not any(r['value_checked']=='True' for r in readings),'C answer reread4, strict independentV0')
    sensitivity_summary=load('sensitivity-summary.json')
    check('sensitivity_counts',sum(r['decision_changed']=='True' for r in sensitivity)==sensitivity_summary['decision_changes'] and sum(r['new_information_loss']=='False' for r in sensitivity)==sensitivity_summary['already_missing_no_new_information_loss'],'sensitivity-summary.json counts derived from40actual rows')
    check('no_strict_success_from_removal',all(r['strict_positive_before']=='False' and r['strict_positive_after']=='False' for r in sensitivity),'missing record removal cannot create authentic-use success')
    result=(ROOT/'RESULT.md').read_text(); tables=markdown_tables(result)
    check('RESULT_first_table_8',len(tables[0])-2==8 and len(re.split(r'(?<!\\)\|',tables[0][0]))-2==8,'RESULT.md first table')
    check('RESULT_second_table_24',len(tables[1])-2==24 and len(re.split(r'(?<!\\)\|',tables[1][0]))-2==8,'RESULT.md second table')
    last_header='| 불일치 또는 약점 | 영향받는 결론 | 근거 주소·위치 | 다음 최소 조사 | 판정이 바뀌는 조건 |'
    check('RESULT_ends_exactly_3_rows',tables[-1][0]==last_header and len(tables[-1])-2==3 and result.rstrip().endswith(tables[-1][-1]),'RESULT.md last table, no content after it')
    check('table_rows_have_primary_URL',all(re.search(r'\]\(https?://',line) for tab in tables[:2] for line in tab[2:]),'every required table row has original-source URL and locator')
    check('RESULT_source_count_current',f"**{len(sources)} 접근/열람 행**" in result,'RESULT source summary matches final ledger')
    check('SELF_CHECK_Q1_Q7',all('## Q'+str(i)+' ' in (ROOT/'SELF_CHECK.md').read_text() for i in range(1,8)),'SELF_CHECK.md explicit7questions')
    manifest=load('manifest.json')
    changed=subprocess.check_output(['git','diff','--name-only',manifest['base_commit']],cwd=REPO,text=True).splitlines()
    changed+=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=REPO,text=True).splitlines()
    outside=sorted(set(p for p in changed if not p.startswith(OWNED)))
    check('owned_path_only',not outside,{'outside_paths':outside})
    check('dot_control_unmodified','docs/automation/dot-control.json' not in changed,'git diff from task starting integration')
    check('original_cohort_preserved',(ROOT/'collection/essd/cases-before-A01.json').exists() and (ROOT/'legacy-cases.json').exists(),'A01 original and corrected cohorts preserved')
    result={'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'command':'python -B docs/workstreams/research/AF-RES-047/scripts/validate.py',
            'status':'passed' if all(x['passed'] for x in checks) else 'failed',
            'checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks),
            'result_sha256':hashlib.sha256((ROOT/'RESULT.md').read_bytes()).hexdigest(),
            'boundary':'Structural and ledger consistency only. Research acceptance remains partial; no original scientific workflow rerun or external independent review.'}
    (ROOT/'evidence/validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','passed','total','result_sha256']},ensure_ascii=False))
    for x in checks:
        if not x['passed']:print(json.dumps(x,ensure_ascii=False))
    raise SystemExit(0 if result['status']=='passed' else 1)


if __name__=='__main__':main()
