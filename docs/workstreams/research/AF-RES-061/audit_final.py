"""Check the requested artifact contract; this does not verify external truth.

Usage from repository root:
  python -B docs/workstreams/research/AF-RES-061/audit_final.py
  python -B docs/workstreams/research/AF-RES-061/audit_final.py --require-handoff
Only the audit receipt inside this workstream is written. No source runs occur.
"""
from pathlib import Path
from urllib.parse import unquote
import argparse
import csv
import datetime
import hashlib
import io
import json
import re
import subprocess

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
OWN = str(P.relative_to(ROOT)) + '/'
SEAL = '02359364000057f69b00594d8b43571ac72df298'
BASE = '1e741fd0def88ef56b1060a478d81f1985a4e760'
CASES = ['D3-N', 'D3-B', 'GV-N', 'GV-B', 'AN-N', 'AN-B', 'RS-N', 'RS-B']


def csvrows(path):
    return list(csv.DictReader(path.open(newline='', encoding='utf-8')))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--require-handoff', action='store_true')
    args = ap.parse_args()
    checks = []
    def check(name, ok, detail):
        checks.append({'check': name, 'passed': bool(ok), 'detail': detail})

    manifest = json.loads((P / 'manifest.json').read_text())
    check('original_contract_and_scope', manifest['task_id'] == 'af-res-061' and manifest['base_commit'] == BASE and manifest['allowed_paths'] == [OWN], manifest['base_commit'])
    check('dependency_pin', manifest['dependencies'] == [{'branch':'work/research-af-res-057', 'commit':'71d13fea95bae733939d36463a671f659a5651d2'}], manifest['dependencies'])
    required = ['SCOPE.md', 'frame.csv', 'transfer.csv', 'predictions.csv', 'observations.csv', 'cards.md', 'sources.jsonl', 'SELF_CHECK.md', 'RESULT.md', 'evidence/acceptance-evidence.json']
    check('required_deliverables_before_handoff', all((P / f).is_file() for f in required), required)
    frame = csvrows(P / 'frame.csv')
    check('four_fixed_components', [(r['implementation_id'], r['version']) for r in frame] == [('D3','3.0.0'), ('GV','14.1.1'), ('AN','1.1.0'), ('RS','10.0.3')], len(frame))
    check('cutoff_metadata', all(r['release_cutoff_utc'] == '2025-12-31T23:59:59Z' and r['source_sha'] and r['release_url'] for r in frame), 'Component release rule and pinned sources recorded, not re-fetched here.')
    pred = csvrows(P / 'predictions.csv')
    obs = csvrows(P / 'observations.csv')
    check('24_predictions_eight_cases_three_views', len(pred) == 24 and {r['case_id'] for r in pred} == set(CASES) and all({r['view'] for r in pred if r['case_id']==c} == {'API','A','B'} for c in CASES), len(pred))
    check('only_gv_A_missing', {r['case_id'] for r in pred if r['treatment_available']=='false'} == {'GV-N','GV-B'} and all(r['view']=='A' for r in pred if r['treatment_available']=='false'), '2 missing A rows are not ties.')
    check('eight_observation_rows', len(obs)==8 and {r['case_id'] for r in obs}==set(CASES), len(obs))
    check('observation_raw_paths', all((P/r['raw_file']).is_file() for r in obs), [r['raw_file'] for r in obs])
    check('no_original_output_upgrade', all('미확인' in r['independent_original_same_version_input'] and '0' in r['independent_original_same_version_input'] for r in obs), 'Eight main rows retain unconfirmed original evidence.')

    immutable = ['predictions.csv', 'streams/graph/baseline.json', 'streams/android/baseline.json', 'streams/react/baseline.json', 'streams/graph/a-predictions.json', 'streams/android/a-predictions.json', 'streams/react/a-predictions.json', 'streams/donor-reader/b-predictions.json', 'evidence/b-windows.json', 'evidence/comparison-rule.json', 'evidence/reader-amendment.md']
    immutable_results=[]
    for f in immutable:
        seal_bytes=git('show', SEAL+':'+OWN+f)
        immutable_results.append({'path':f, 'same':seal_bytes==(P/f).read_bytes(), 'sha256':sha(P/f)})
    check('sealed_content_unchanged', all(x['same'] for x in immutable_results), immutable_results)
    seal_files = git('ls-tree', '-r', '--name-only', SEAL, OWN).decode().splitlines()
    prohibited = [f for f in seal_files if f.rsplit('/',1)[-1] in {'RESULT.md','HANDOFF.md','observations.csv','observations.json','d3-run.json','raw-outputs.json','probe-output.csv'}]
    check('seal_tree_has_no_outcome_or_result', not prohibited, prohibited)
    original_transfer = list(csv.DictReader(io.StringIO(git('show', SEAL+':'+OWN+'transfer.csv').decode())))
    transfer=csvrows(P/'transfer.csv')
    check('four_sealed_plus_four_postseal_transfers', len(transfer)==8 and transfer[:4]==original_transfer and all(r['transfer_id'].endswith('-POST') for r in transfer[4:]), len(transfer))

    sources=[json.loads(s) for s in (P/'sources.jsonl').read_text().splitlines() if s.strip()]
    ids={r['source_id'] for r in sources}
    eligible={r['work_id'] for r in sources if r['count_eligible']}
    fields=['source_id','work_id','kind','author','original_url','fixed_url','version_date','read_utc','reader','sections','confirmed','limits','qs','cases','count_eligible','read_status','canonical_cases','acquisition_refs']
    check('source_schema_and_unique_ids', len(ids)==len(sources) and all(all(k in r for k in fields) for r in sources), {'records':len(sources),'ids':len(ids)})
    check('primary_work_minimum', len(eligible)==31 and len(eligible)>=20, sorted(eligible))
    check('canonical_case_keys', all(set(r['canonical_cases'])<=set(CASES) for r in sources), 'Original ANDROID aliases preserved; canonical AN keys appended.')
    counts=json.loads((P/'evidence/final-counts.json').read_text())
    quota=counts['disjoint_allocation']
    allocations=[w for q in quota.values() for w in q['work_ids']]
    minimums={'component_lineage':4,'independent_issue_or_design':4,'original_source_astronomy':2,'original_source_oscillator':2,'independent_output_study':4,'additional_boundary_or_accessibility':4}
    check('disjoint_primary_source_quotas', set(allocations)==eligible and len(allocations)==len(set(allocations)) and all(quota[k]['count']>=n for k,n in minimums.items()), quota)
    check('derived_counts_and_ledger_hash', counts['canonical_source_records']==len(sources) and counts['source_sha256']==sha(P/'sources.jsonl') and counts['eligible_unique_primary_works']==len(eligible), counts['source_sha256'])
    check('separate_case_effect_denominators', counts['retained_cases']==8 and counts['available_A_B_case_count']==6 and counts['differing_prediction_only_denominator']==0 and counts['independent_original_outputs_main_frame']['located']==0 and counts['auxiliary_execution_main_rows']==6, 'Operational difference0/6; exact original found0/8; auxiliary6/8; conditional accuracy N/A.')

    aw=json.loads((P/'streams/graph/a-windows.json').read_text())
    an=json.loads((P/'streams/android/a-window.json').read_text())
    rs=json.loads((P/'streams/react/a-window.json').read_text())
    bw=json.loads((P/'evidence/b-windows.json').read_text())
    lengths=[aw[0]['word_count'], an['displayed_words'], rs['word_count']]+[x['display_word_count'] for x in bw]
    check('recorded_window_caps_and_missing_GV', lengths==[37,239,63,247,195,213] and all(0<n<=250 for n in lengths) and aw[1]['status']=='missing_eligible_section', 'Recorded metadata caps checked; original display text is not reconstructed or recounted by this checker.')
    check('window_nonword_metadata', all(k in x for x in bw for k in ['equation_displays','code_lines','figures_displayed','sha256']) and all(k in an and k in rs for k in ['code_lines','equations','figures']), 'Code/equations/figures recorded separately.')

    result=(P/'RESULT.md').read_text()
    blocks=re.findall(r'(?:^\|.*\n)+',result,re.M)
    tables=[b.strip().splitlines() for b in blocks]
    check('first_two_required_tables_and_last_three', result.startswith('| 구현·판 |') and len(tables[0])-2==8 and len(tables[1])-2==4 and len(tables[-1])-2==3, [len(t)-2 for t in tables])
    check('two_exact_table_headers', tables[0][0]=='| 구현·판 | 사용 목적·입력 | 명시 차용 원문·절 URL | 대응 변수·달라진 가정 | 공통 API 예측 | 동종 보기 예측 | 원전 보기 예측 | 기대·실측 출처 URL | 판정·미확인 |' and tables[1][0]=='| 구현 | 동종 자료만으로 확인한 것 | 원전으로 새로 확인·반박한 것 | 원식이 깨지는 조건 | 반환할 첫 링크·그 이유 | 결정을 바꿀 자료 |', 'User-specified columns preserved.')
    check('Q1_through_Q7_in_result_and_selfcheck', all(f'## Q{i}.' in result and f'## Q{i}.' in (P/'SELF_CHECK.md').read_text() for i in range(1,8)), '7 questions in each document.')
    cards=(P/'cards.md').read_text()
    check('four_return_cards_with_stakeholders', all(f'## {k} ·' in cards for k in ['D3','GV','AN','RS']) and cards.count('**첫 링크')==4, 4)
    check('final_documents_preserve_partial_and_no_human_effect', '부분 인계' in result and '부분 인계' in (P/'SELF_CHECK.md').read_text() and '미실시' in cards and '미실시' in result, 'Document assertion checks; semantic audit is separately recorded.')
    check('corrected_d3_first_anchor', '#many-body-forces' not in cards and 'README.md#many-body)' in cards, 'Historical stream wrong anchor remains with audit correction; new cards use pinned heading.')

    missing=[]; planned=[]
    docs=['RESULT.md','cards.md','SELF_CHECK.md','PROGRESS.md']
    if (P/'HANDOFF.md').exists(): docs.append('HANDOFF.md')
    for name in docs:
        txt=(P/name).read_text()
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',txt):
            target=target.split('#',1)[0]
            if not target or re.match(r'[A-Za-z][\w+.-]*:',target):continue
            target=unquote(target)
            if not (P/target).is_file():
                missing.append({'from':name,'target':target})
    check('final_document_local_links', not missing, {'missing':missing,'planned_final_handoff_links':planned})
    cited=set(re.findall(r'\b[AGRDVE]\d{3}\b','\n'.join((P/f).read_text() for f in docs)))
    check('referenced_source_ids_exist', cited<=ids, sorted(cited-ids))
    parse_errors=[]
    for f in P.rglob('*.json'):
        if any(x.startswith('.') for x in f.relative_to(P).parts): continue
        try: json.loads(f.read_text())
        except Exception as e: parse_errors.append({'path':str(f.relative_to(P)),'error':str(e)})
    for f in P.rglob('*.jsonl'):
        if any(x.startswith('.') for x in f.relative_to(P).parts): continue
        try:
            for s in f.read_text().splitlines():
                if s.strip(): json.loads(s)
        except Exception as e: parse_errors.append({'path':str(f.relative_to(P)),'error':str(e)})
    check('JSON_and_JSONL_parse', not parse_errors, parse_errors)
    changed=git('diff','--name-only',BASE).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines()
    outside=sorted({s for s in changed if not s.startswith(OWN)})
    check('owned_paths_only',not outside,outside)
    a=json.loads((P/'evidence/acceptance-evidence.json').read_text())
    check('acceptance_plan_actual_gap_actions', all(all(k in r for k in ['id','planned','actual','unit','evidence','status','gap','minimum_resume']) for r in a['criteria']),len(a['criteria']))
    check('acceptance_and_result_status_agree',a['overall_status']=='부분 인계','PARTIAL due unresolved source/input gaps, not an execution success claim.')
    review=json.loads((P/'streams/final-audit/report-review.json').read_text())
    check('final_report_review_recorded',bool(review),'Independent same-model document review, not independent original output.')
    if args.require_handoff:
        check('handoff_exists',(P/'HANDOFF.md').is_file(),'Last-file requirement; Git commit isolation checked after publish.')
    receipt={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'executor':'/root cloud Python; no component experiments rerun','checkout_sha':git('rev-parse','HEAD').decode().strip(),'working_tree_changes_included':True,'mode':'final_with_handoff' if args.require_handoff else 'pre_handoff','scope':'Artifact structure, count consistency, file references, sealed bytes and owned-path checks; not external truth or runtime verification','passed':sum(r['passed'] for r in checks),'total':len(checks),'failed':[r for r in checks if not r['passed']],'checks':checks,'document_sha256':{f:sha(P/f) for f in docs}}
    dest=P/'evidence'/('audit-with-handoff.json' if args.require_handoff else 'audit-final.json')
    dest.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:receipt[k] for k in ['mode','checkout_sha','passed','total','failed']},ensure_ascii=False))
    raise SystemExit(0 if not receipt['failed'] else 1)


if __name__=='__main__':
    main()
