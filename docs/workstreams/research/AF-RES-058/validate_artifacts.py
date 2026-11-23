"""Check the specific linkage, denominator, and reporting risks of AF-RES-058."""
from __future__ import annotations
import csv,hashlib,json,re,subprocess,sys
from collections import defaultdict
from datetime import datetime,timezone
from pathlib import Path

B=Path(__file__).resolve().parent
def j(f):return json.loads((B/f).read_text())
def csvrows(f):
    with (B/f).open() as h:return list(csv.DictReader(h))
errors=[];checks=[]
def require(ok,label):
    checks.append({'check':label,'passed':bool(ok)})
    if not ok:errors.append(label)

sources=[json.loads(s) for s in (B/'sources.jsonl').read_text().splitlines() if s]
source_ids={r['source_id'] for r in sources}
require(len(sources)==len(source_ids),'source IDs unique')
required_source_fields={'source_id','work_id','kind','lineage','questions','cases','original_url','fixed_version_url','version_date_or_hash','read_utc','locations','verified','scope_and_limits','evidence_mode','counterevidence_ids','read_status'}
require(all(required_source_fields<=r.keys() for r in sources),'source ledger required provenance and read-scope fields present')
require(all(set(r['counterevidence_ids'])<=source_ids for r in sources),'source counterevidence references resolve')
deep={r['work_id'] for r in sources if r['counts_for_deep_20']}
read={r['work_id'] for r in sources if r['external_primary_eligible']}
counts=j('evidence/source-counts.json')
require(len(deep)==counts['unique_deep_primary_works']==28,'deep sources independently recounted by work_id')
require(len(read)==counts['unique_read_primary_works'],'all read eligible work IDs match report')
require(len(sources)==counts['source_records'],'source record count matches report')
works=csvrows('evidence/works.csv')
require({r['work_id'] for r in works if r['counts_for_deep_20']=='True'}==deep,'work ledger agrees with deep source set')
require(sum(counts['deep_categories'].values())==len(deep),'deep material categories do not double count')

frame=csvrows('frame.csv');stim=csvrows('stimuli.csv')
require(len(frame)==60 and sum(r['stratum']=='A' for r in frame)==30 and sum(r['stratum']=='B' for r in frame)==30,'frozen review budget 30 per stratum')
for s in ('A','B'):
    require(sorted(int(r['recruit_rank']) for r in frame if r['stratum']==s)==list(range(1,31)),f'{s} original ranks kept')
    require(len({r['doi'].lower() for r in frame if r['stratum']==s})==30,f'{s} DOI deduplication')
require(all(r['source_id'] in source_ids or r['source_id']=='미확인' for r in frame),'frame source IDs resolve')
require(all(set(json.loads(r['source_ids']))<=source_ids for r in stim),'stimulus source IDs resolve')

out=j('evidence/outcome-ledger.json');con=j('evidence/contrast-ledger.json');acc=j('evidence/acceptance-evidence.json')
require(len(out)==246 and len(con)==84,'expected outcome and contrast row inventory')
require(len({r['record_id'] for r in out})==len(out),'outcome IDs unique')
require(len({r['contrast_id'] for r in con})==len(con),'contrast IDs unique')
require(all(set(r['source_ids'])<=source_ids for r in out+con),'outcome/contrast source references resolve')
groups=defaultdict(set)
for r in out:
    if r['row_type']=='outcome':groups[(r['case_id'],r['condition'],r['analysis_set'],r['dataset'])].add(r['advice_truth'])
require(all(g=={'correct','wrong'} for g in groups.values()),'each reported condition/analysis set has both correctness strata')
require(all(r['advice_provided'] is None for r in out if r['case_id'] in ('A03','A04')),'unfilled slots are not offered-advice observations')
require(all(r['accept_n'] is None and r['accept_D'] is None and r['advice_provided'] is False for r in out if r['condition']=='Human'),'Human no-advice records not interpreted as acceptance')
require(all(r['planned_D']==0 and r['observed_D'] is None and r['accept_n'] is None and r['status']=='not_applicable_design_zero' for r in out if r['case_id']=='B01' and r['advice_truth']=='wrong'),'B01 structural absence separated from observed zero')
primary=[r for r in out if r['stratum'] in 'AB' and r['row_type']=='outcome']
require(len(primary)==44 and all(r['accept_n'] is None and r['observed_D'] is None for r in primary),'primary unknown integer cells remain unknown; no plan inversion')
observed=[r for r in out if r['row_type']=='outcome' and r['accept_n'] is not None]
require(len(observed)==66,'diagnostic integer cells counted separately from studies')
for r in observed:
    a,d,c=r['accept_n'],r['accept_D'],r['final_correct_n']
    require(all(isinstance(v,int) and not isinstance(v,bool) for v in (a,d,c)) and 0<=a<=d and 0<=c<=d,f"{r['record_id']} integer counts within denominator")
    if r['advice_truth']=='correct':require(a==c,f"{r['record_id']} correct advice A=C")
    else:require(a+c+r['third_wrong_n']==d,f"{r['record_id']} wrong A+C+third_wrong=D")
raw=[r for r in con if r['delta_accept_pp_observed'] is not None]
require(len(raw)==52,'raw observed contrasts separated from model-only contrasts')
for r in raw:
    calc=100*(r['intervention_accept_n']/r['intervention_D']-r['control_accept_n']/r['control_D'])
    require(abs(calc-r['delta_accept_pp_observed'])<1e-9,f"{r['contrast_id']} observed difference recount")
require(all(r['delta_accept_pp_observed'] is None for r in con if r['delta_accept_pp_model'] is not None),'model percentages never relabelled as raw differences')
require(acc['research_status']=='PARTIAL' and acc['all_requirements_satisfied'] is False,'storage success distinct from research acceptance')
require(len(acc['conditions'])==164 and len(acc['missingness_records'])==82,'acceptance ledger covers each outcome and missingness record')
lookup={r['record_id']:r for r in out}
require(all(all(a['actual'][k]==lookup[a['outcome_id']][k] for k in ['accept_n','accept_D','final_correct_n','final_correct_D']) for a in acc['conditions']),'acceptance file counts match outcome ledger')
require(len(csvrows('outcomes.csv'))==len(out) and len(csvrows('contrasts.csv'))==len(con),'CSV row counts match JSON ledgers')

result=(B/'RESULT.md').read_text();prefix=result.split('<!-- END_REQUIRED_TABLES -->')[0]
require('연구·층·배정 단위 | 원과제·조건 N | 같은 후보·순위·권고의 증거 | 설명의 차이·원 자극 주소 | 정답 원천 | 최종 응답 원천·연결 수 | 가능한 해석·미확인' in prefix,'first table exact required columns')
require('연구·조건·대비 | 맞는/틀린 권고 | 배정·판정 가능·결측 분모 | 권고 수락 수/분모 | 최종 정답 수/분모 | 조건 간 차이·가능 범위 | 원행/저자 집계/미확인 | 근거 주소·표·열' in prefix,'second table exact required columns')
pout=[r for r in out if r['stratum'] in 'AB'];pcon=[r for r in con if r['stratum'] in 'AB']
require(all(prefix.count('('+r['record_id']+')')==1 for r in pout),'all 66 primary outcome/missingness row IDs appear exactly once in table2')
require(all(prefix.count('('+r['contrast_id']+')')==1 for r in pcon),'all 32 primary contrasts appear exactly once in table2')
tail=result.rsplit('| 불일치·약점 | 영향받는 주장 | 근거 주소·위치 | 다음 최소 조사 | 판정이 바뀔 조건 |',1)
require(len(tail)==2 and len([s for s in tail[-1].splitlines() if s.startswith('|')])==4,'last weakness table has separator plus exactly three data rows and no later content')
require(all(f'## Q{i}.' in result for i in range(1,8)),'all seven question sections present')
proc=subprocess.run([sys.executable,'-B',str(B/'build_tables.py'),'--check'],capture_output=True,text=True)
require(proc.returncode==0,'required tables regenerate identically from ledgers')

ind=j('streams/root/independent-calculation.json')
for r in ind['study_tables']:
    matches=[x for x in observed if x['case_id']=='D04' and x['condition']==r['condition']]
    require(len(matches)==2,f"D04 {r['condition']} independent root condition exists")
    for x in matches:
        g=x['advice_truth'];require(x['accept_n']==r['accept_correct' if g=='correct' else 'accept_wrong'] and x['accept_D']==r['correct_advice_D' if g=='correct' else 'wrong_advice_D'],f"D04 {r['condition']} {g} independent same-input recount")
tracked=['RESULT.md','SELF_CHECK.md','sources.jsonl','frame.csv','stimuli.csv','outcomes.csv','contrasts.csv','reproduce.md','evidence/source-counts.json','evidence/acceptance-evidence.json','evidence/outcome-ledger.json','evidence/contrast-ledger.json']
receipt={'actor':'root assistant in provided workspace','executed_utc':datetime.now(timezone.utc).isoformat(),
 'command':'python -B docs/workstreams/research/AF-RES-058/validate_artifacts.py','scope':'specific source-lineage, data-linkage, count, model-vs-raw and required-table invariants; not author model reruns or proof of research completion',
 'status':'PASS' if not errors else 'FAIL','checks':checks,'errors':errors,
 'actual_counts':{'source_records':len(sources),'deep_works':len(deep),'frame_rows':len(frame),'stimulus_rows':len(stim),'outcome_rows':len(out),'contrast_rows':len(con),'primary_integer_cells':sum(r['accept_n'] is not None for r in primary),'raw_diagnostic_cells':len(observed),'raw_diagnostic_contrasts':len(raw)},
 'checked_files_sha256':{p:hashlib.sha256((B/p).read_bytes()).hexdigest() for p in tracked},
 'table_check_stdout':proc.stdout,'table_check_stderr':proc.stderr}
(B/'evidence/artifact-validation.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'checks':len(checks),'errors':errors,'actual_counts':receipt['actual_counts']},ensure_ascii=False))
sys.exit(bool(errors))
