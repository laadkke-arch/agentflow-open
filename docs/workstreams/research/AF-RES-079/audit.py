"""Audit provenance links, ownership and denominators, not universal behavior.

No network and no source mutation. Exit nonzero on missing evidence or inconsistent
units. A completed audit may coexist with PARTIAL behavioral acceptance.
"""
import argparse
import csv
import datetime as dt
import hashlib
import json
import subprocess
import sys
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
OWNED = 'docs/workstreams/research/AF-RES-079/'
START = 'd73c8ec85d375f37451795b575dd7d0e6b2f3594'
parser = argparse.ArgumentParser()
parser.add_argument('--phase',choices=('ledgers','result'),default='result')
parser.add_argument('--output',help='Optional receipt path relative to this owned task directory')
args = parser.parse_args()
checks = []


def check(name, condition, detail):
    checks.append({'check':name,'passed':bool(condition),'detail':detail})


def j(path):
    return json.loads((B/path).read_text())


def jl(path):
    return [json.loads(x) for x in (B/path).read_text().splitlines() if x.strip()]


def csvrows(path):
    with (B/path).open() as f:
        return list(csv.DictReader(f))


def hashfile(path):
    return hashlib.sha256((B/path).read_bytes()).hexdigest()


required = ['SCOPE.md','frame.csv','sources.jsonl','observations.csv','relations.csv','manifest.json',
            'evidence/first-assessment.json','streams/review/blind-review.json','streams/review/review-comparison.json']
if args.phase == 'result':
    required += ['RESULT.md','SELF_CHECK.md','evidence/acceptance-evidence.json','REPRODUCE.md']
check('required_artifacts',all((B/p).is_file() for p in required),required)
sources = jl('sources.jsonl')
source_ids = {x['source_id'] for x in sources}
check('unique_source_ids',len(source_ids)==len(sources),len(sources))
counted = [x for x in sources if x['counts_minimum']]
works = {x['independent_work_id'] for x in counted}
check('minimum_original_works',len(works)>=20 and len(works)==len(counted),{'independent':len(works),'counted_rows':len(counted)})
check('counted_are_direct_reads',all(x['directly_read'] for x in counted),[x['source_id'] for x in counted if not x['directly_read']])
missing = []
for x in sources:
    for field in ('actually_opened_url','fixed_location','edition','section','checked_utc','finding','limitation','count_reason'):
        if not x.get(field):
            missing.append([x['source_id'],field])
check('source_required_fields',not missing,missing)
frame = csvrows('frame.csv')
natural = {r['event_id'] for r in frame if r['stratum']=='natural'}
controls = {r['event_id'] for r in frame if r['stratum']=='control'}
check('stratified_denominators',natural=={'G01','G02','G03','G04','O01','O02','O03','O04'} and controls=={'C01','C02','C03'}, {'natural':sorted(natural),'controls':sorted(controls)})
obs = csvrows('observations.csv')
obids = {x['observation_id'] for x in obs}
check('unique_observation_ids',len(obids)==len(obs),len(obs))
bad_sources=[];bad_paths=[];bad_times=[]
for x in obs:
    for sid in json.loads(x['source_ids'] or '[]'):
        if sid not in source_ids:bad_sources.append([x['observation_id'],sid])
    for path in json.loads(x.get('evidence_artifacts') or '[]'):
        if not (B/path.split('#')[0]).is_file():bad_paths.append([x['observation_id'],path])
    try:dt.datetime.fromisoformat(x['checked_utc'].replace('Z','+00:00'))
    except (ValueError,TypeError):bad_times.append(x['observation_id'])
check('observation_source_links',not bad_sources,bad_sources)
check('observation_artifact_links',not bad_paths,bad_paths)
check('observation_UTC',not bad_times,bad_times)
check('both_requirements_recorded',all(any(x['event_id']==eid and 'P1' in x['question'] for x in obs) and any(x['event_id']==eid and 'P2' in x['question'] for x in obs) for eid in natural|controls),'G01 applicability explicitly limited; rows are not success counts')
relations = csvrows('relations.csv')
bad=[]
for x in relations:
    for sid in json.loads(x['source_ids']):
        if sid not in source_ids:bad.append([x['relation_id'],'source',sid])
    for oid in json.loads(x['behavior_observation_ids']):
        if oid not in obids:bad.append([x['relation_id'],'observation',oid])
    if x['decision_code']=='3' and x['status']!='conditional_not_observed_production_repair':bad.append([x['relation_id'],'unobserved_split_promoted'])
check('relation_evidence_and_conditional_splits',not bad,bad)
check('old_evidence_retained',all(x['preserve_old_id']=='True' and x['preserve_old_citation']=='True' and x['reversible']=='True' for x in relations),len(relations))
url=j('evidence/url-policy-comparison.json')['rows']
check('URL_rule_denominators',len(url)==11 and len({x['event_id'] for x in url})==11, {'natural':sum(x['stratum']=='natural' for x in url),'control':sum(x['stratum']=='control' for x in url)})
check('no_historical_redirect_inference',all(not x['historical_redirect_verified'] for x in url),'current transport only')
check('no_HTTP_counted_as_native',all(x.get('historical_pair_executed')=='False' and x.get('current_supplement_executed')=='False' for x in obs if x['observation_id'].endswith('-HTTP-U')),'HTTP11 excluded from native functionality counts')
first=j('evidence/first-assessment.json')
review=j('streams/review/blind-review.json')
reconciliation=j('streams/review/review-comparison.json')
check('first_decision_lock_preserved',hashfile('evidence/first-assessment.json')==reconciliation['protocol']['first_assessment_sha256'],'first snapshot differs from later reconciled/native conclusions by design')
check('blind_review_original_preserved',hashfile('streams/review/blind-review.json')==reconciliation['protocol']['blind_review_sha256'],review['protocol']['reviewer_kind'])
check('mask_before_first_result',not first['blind_review_results_opened'] and review['protocol']['first_decisions_or_repair_plans_seen'] is False,'source selection was not blind; no statistical independent agreement claim')
counts=j('evidence/ledger-counts.json')
check('reported_ledger_counts',counts['source_rows']==len(sources) and counts['independent_works']==len(works) and counts['observations']==len(obs),counts)
native_events = {x['event_id'] for x in obs if x['historical_pair_executed']=='True'}
check('native_event_counts_recomputed',native_events=={'G02','G03','G04','O01','O02','O03','O04'} and counts['historical_native_event_pairs_current']==len(native_events),sorted(native_events))
check('frame_native_flags_agree',all((r['historical_native_pair']=='True')==(r['event_id'] in native_events) for r in frame),len(frame))
if (B/'streams/resume-gis/audit.json').exists():
    ga=j('streams/resume-gis/audit.json')
    check('GIS_recovered_receipts_validated',ga['audit_exit_code']==0 and len(ga['receipt_checks'])==65 and all(x['output_hash_matches'] for x in ga['receipt_checks']),{'receipts':len(ga['receipt_checks']),'expected_failure_exit_codes_are_not_success':True})
    damaged=[]
    for x in ga['artifact_manifest']:
        for field in ('prior_path','preserved_path'):
            if not (B/x[field]).is_file() or hashfile(x[field])!=x['sha256']:damaged.append([x[field],x['sha256']])
    check('GIS_immutable_inputs_and_outputs_preserved',len(ga['artifact_manifest'])==11 and not damaged,damaged)
    check('GIS_writer_output_hashes',len(ga['writer_hash_checks'])==6 and all(x['output_hash_matches'] for x in ga['writer_hash_checks']),6)
    rr=ga['targeted_replays']
    check('GIS_targeted_replay_semantics',len(rr)==7 and all(not x['semantic_differences'] and x['exact_recorded_input_equal'] for x in rr),{'replays':len(rr),'exit_codes':[x['exit_code'] for x in rr]})
    gn=[x for x in obs if x['observation_id'].startswith('GN')]
    check('GIS_temporal_and_same_edition_separated',len(gn)==11 and sum(x['historical_pair_executed']=='True' for x in gn)==9 and {x['observation_id'] for x in gn if x['historical_pair_executed']=='False'}=={'GN07','GN11'},'9 temporal groups,2 same-edition supplements;3 natural events')
oa=j('streams/resume-oss/audit.json')
check('OSS_targeted_replay_receipts',oa['resume_reexecution_scope']['public_api_calls']==18 and oa['resume_reexecution_scope']['exit_codes']==[0,0,0,0],oa['resume_reexecution_scope'])
if (B/'streams/oss/historical/paired-check.receipt.json').exists():
    receipt=j('streams/oss/historical/paired-check.receipt.json')
    pairs=jl('streams/oss/historical/paired-observations.jsonl')
    check('historical_pairs_are_validated',receipt['exit_code']==0 and receipt['paired_comparisons']==len(pairs) and all(x['native_pair_observed'] for x in pairs),{'event_pairs':len({x['event_id'] for x in pairs}),'comparisons':len(pairs),'exact_inputs':sum(x['exact_recorded_input_equal'] for x in pairs)})
    for version in ('1.4.1','1.5.0','1.5.4','1.6.0'):
        rr=j(f'streams/oss/historical/scipy-{version}.receipt.json')
        check('native_artifact_hash_'+version,rr['result_sha256']==hashfile(f'streams/oss/historical/scipy-{version}.jsonl') and rr['script_sha256']==hashfile('streams/oss/probe.py') and rr['exit_code']==0,rr['environment'])
if (B/'streams/pil_archive/archive-verification.json').exists():
    archive=j('streams/pil_archive/archive-verification.json')
    check('PIL_original_archive_consistency',archive['exit_code']==0 and all(x['matches_dsc'] for x in archive['checks']) and archive['image_py_matches_debian_sources_1_1_7_2'],{'scope':archive['provenance_scope'],'signature_verified':archive['pgp_signature_verified'],'original_runtime':archive['upstream_code_executed']})
changed=subprocess.check_output(['git','diff','--name-only',START],cwd=ROOT,text=True).splitlines()
untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=ROOT,text=True).splitlines()
outside=[p for p in set(changed+untracked) if not p.startswith(OWNED)]
check('owned_path_only',not outside,outside)
scope_original=subprocess.check_output(['git','show','dfdfe1b82ee1921f2f90c723dbd9fe8d22138ead:'+OWNED+'SCOPE.md'],cwd=ROOT)
check('prospective_scope_unchanged',hashlib.sha256(scope_original).hexdigest()==hashfile('SCOPE.md'),hashfile('SCOPE.md'))
if args.phase=='result':
    result=(B/'RESULT.md').read_text();selfcheck=(B/'SELF_CHECK.md').read_text()
    check('result_three_required_tables',all(x in result for x in ('사건ID·모집 원순위','입력/환경','원주소 수선')), 'table column labels inspected separately for substantive meaning')
    check('self_check_seven_questions',all('Q'+str(i) in selfcheck for i in range(1,8)),'presence only; substantive reading still required')
failed=[x['check'] for x in checks if not x['passed']]
report={'task_id':'AF-RES-079','phase':args.phase,'actor':'root via local Python','location':str(ROOT),'checked_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'command':'python -B '+OWNED+'audit.py --phase '+args.phase,'exit_code':1 if failed else 0,'failed_checks':failed,'checks':checks,'artifact_hashes':{p:hashfile(p) for p in required if (B/p).is_file()},'limit':'Structural/reference/ownership audit; source truth, universal compatibility and server availability are not proved by exit0.'}
out=(B/args.output).resolve() if args.output else B/'evidence'/('audit-'+args.phase+'.json')
if not out.is_relative_to(B):raise SystemExit('receipt must remain under owned_path')
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'phase':args.phase,'checks':len(checks),'failed':failed,'exit_code':report['exit_code']},ensure_ascii=False))
sys.exit(report['exit_code'])
