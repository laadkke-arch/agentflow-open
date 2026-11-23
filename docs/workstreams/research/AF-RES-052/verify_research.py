"""Read-only checks for concrete AF-RES-052 ledger/report risks; not domain tests."""
from pathlib import Path
from collections import Counter
import csv
import json
import subprocess

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]
OWNED='docs/workstreams/research/AF-RES-052/'
BASE='522ea9092d4d56ef6db0bd4f707bfc90032e179e'
SEAL='ea4fa69f841dca2c470b62c3fdf1ee4d9029712e'
checks=[]
def require(condition, label):
    if not condition: raise AssertionError(label)
    checks.append(label)
def csv_rows(name):return list(csv.DictReader((ROOT/name).open()))
def js(name):return json.loads((ROOT/name).read_text())
def git(*args):
    return subprocess.check_output(['git',*args],cwd=REPO,text=True)

needed=['SCOPE.md','frame.csv','pools.csv','groups.csv','evidence.csv','paths.csv','cards.md',
        'manifest.json','sources.jsonl','RESULT.md','SELF_CHECK.md','evidence/acceptance-evidence.json',
        'REPRODUCE.md','evidence/markdown/REPLAY_PLAN.md']
require(all((ROOT/f).is_file() for f in needed),'all required pre-handoff deliverables exist')
slots=csv_rows('slots.csv'); groups=csv_rows('groups.csv'); pools=csv_rows('pools.csv')
ids=['P-N1','P-N2','M-N1','M-N2','P-S1','P-S2','M-S1','M-S2']
require([r['slot_id'] for r in slots]==ids,'eight primary slots in layer/order')
require([r['group_row_id'] for r in groups]==[i+'-'+m for i in ids for m in 'ABC'],'twenty-four primary method rows; no diagnostic replacement')
require(len(pools)==5 and {r['case_id'] for r in pools}=={'P-S1'},'only five observed primary pool rows')
require([int(r['original_rank']) for r in pools]==[1,2,3,4,5],'primary original rank order preserved')
require([r['exact_url'] for r in pools]==[
 'https://bandersnatch.readthedocs.io','https://github.com/pypa/bandersnatch/issues',
 'https://github.com/pypa/bandersnatch','https://pypi.org/project/bandersnatch','https://aws.amazon.com/s3/'],
 'exact URLs retain original trailing slash distinction')
by_group={r['group_row_id']:r for r in groups}
require(json.loads(by_group['P-S1-A']['representatives'])==[1,2,3] and
        json.loads(by_group['P-S1-B']['representatives'])==[1,5] and
        json.loads(by_group['P-S1-C']['representatives'])==[1,2,3], 'primary A/B/C representative arrays')
require(all(not r['product_version'] and not r['document_role'] for r in pools), 'unknown C fields not backfilled from arrivals')

frame=csv_rows('frame.csv')
require(Counter(r['record_kind'] for r in frame)=={'issue_screen':80,'catalog_section_screen':28,'slot_selection':8},'frame retains all screening and unfilled rows')
sources=[json.loads(s) for s in (ROOT/'sources.jsonl').read_text().splitlines()]
require(len({r['source_id'] for r in sources})==len(sources),'source IDs unique')
credited=[r for r in sources if r['counts_in_minimum']]
require(len(credited)==24 and len({r['work_id'] for r in credited})==24,'minimum twenty-four distinct authored works')
require(Counter(r['allocation'] for r in credited)=={'user_request':4,'catalog_rule':4,'supplier_doc':8,'release_test':4,'crossfield':4},'source allocation exactly meets each category')
require(all(r['direct_open'] and not r['duplicate_of'] and not r['failure'] for r in credited),'no failure or duplicate credited')
require(all(r['attempt'] and r['failure'] and r['minimum_material_to_change'] for r in sources if not r['direct_open']),'all failed arrivals have attempt, error, minimum recovery')
require(all(r['url'] and r['checked_utc'] and r['finding'] and r['limitations'] and r['locator'] for r in sources),'source findings/limits/locations retained')
source_ids={r['source_id'] for r in sources}
ev=csv_rows('evidence.csv'); paths=csv_rows('paths.csv')
require(len(ev)==37 and len({r['evidence_id'] for r in ev})==37,'evidence IDs/empty conditions retained')
require(all(set(json.loads(r['source_ids']))<=source_ids for r in ev),'condition evidence points to recorded sources')
require(len(paths)==177 and len({r['path_id'] for r in paths})==177,'path IDs unique; status rows separate')
require(sum(int(r['actions'])==0 for r in paths)==21,'twenty-one empty status rows not counted as trials')
require(all(0<=int(r['actions'])<=2 for r in paths),'all represented paths within two-action cap')
require(all(len(json.loads(r['steps']))==int(r['actions']) for r in paths),'action counts match actual recorded step lists')
require(all(not r['complete_current_ids'] and not r['complete_current_count'] for r in paths if r['case_id']=='P-S1'),'purpose-unlinked Python completion remains null')
md=[r for r in paths if r['case_id']=='D-M1']
require(Counter(r['method'] for r in md)=={'A':18,'B':14,'C':18},'diagnostic fifty paired paths, not primary sample')
require(all(r['complete_current_count']=='0' and json.loads(r['complete_current_ids'])==[] for r in md),'diagnostic current full-completion observed zero')
require([r['path_id'] for r in md if json.loads(r['current_supported_atoms'])]==['D-M1-B-P08'],'only C1 partial atom gain on B-P08')
require(all('미확인' in r['historical_status'] for r in md),'historical uncertainty never replaced by current gold')
require(sum(r['path_instantiated']=='False' for r in paths if r['case_id']=='D-P1')==8,'eight diagnostic unresolved paths retained')
py_arr=[json.loads(s) for s in (ROOT/'evidence/python/arrivals.jsonl').read_text().splitlines()]
pa={r['arrival_id']:r for r in py_arr}
require(pa['PY-A04']['window']['content_window_status']=='partial_snapshot_changed' and pa['PY-A04']['window']['word_count']==347,'initial PyPI snapshot is partial')
require(pa['PY-A17']['kind']=='later_snapshot' and pa['PY-A17']['product_version']!=pa['PY-A04']['product_version'],'later snapshot not spliced into first')
require(pa['PY-A10']['retrieval_status']=='access_failed' and pa['PY-A07']['retrieval_status']=='exact_fragment_unconfirmed','failed Compose and fragment remain incomplete')

for name in ['SCOPE.md','CORRECTIONS.md','frame.csv','slots.csv','pools.csv','groups.csv','manifest.json','evidence/diagnostic-pools.csv','evidence/diagnostic-groups.csv','evidence/path-plan.json','evidence/sensitivity-plan.json']:
    frozen=git('show',SEAL+':'+OWNED+name)
    require((ROOT/name).read_text()==frozen,'frozen input unchanged: '+name)
changed=git('diff','--name-only',BASE,'HEAD').splitlines()
worktree=git('diff','--name-only','HEAD').splitlines()
untracked=git('ls-files','--others','--exclude-standard').splitlines()
require(all(name.startswith(OWNED) for name in changed+worktree+untracked),'all branch changes and untracked deliverables stay in owned path')
require('docs/automation/dot-control.json' not in changed+worktree,'automation control untouched')
result=(ROOT/'RESULT.md').read_text()
expected=(ROOT/'evidence/required-tables.md').read_text()
require(result.startswith(expected),'RESULT starts with exact required eight and twenty-four row tables')
table_data=js('evidence/required-table-data.json')
require(len(table_data['table1']['rows'])==8 and len(table_data['table2']['rows'])==24,'required table row cardinality')
weak=(ROOT/'evidence/weaknesses.md').read_text()
require(result.endswith(weak),'RESULT ends with prescribed weakness table and no trailing prose')
require(len([s for s in weak.splitlines() if s.startswith('|')])==5,'weakness table has exactly three body rows')
require(len(csv_rows('counterexamples.csv'))==12 and len(csv_rows('sensitivity.csv'))==40,'counterexamples and sensitivities retained')
acc=js('evidence/acceptance-evidence.json')
require(acc['overall_status']=='partial_handoff','partial research status remains explicit')
require(acc['units']['supplemental_completion_rate']['denominator']==0 and acc['units']['supplemental_completion_rate']['display']=='해당 없음','zero conditional denominator displayed not applicable')
print(json.dumps({'status':'passed','check_count':len(checks),'checks':checks,
                  'limits':'Structural/provenance checks only; not domain execution or user study.'},ensure_ascii=False,indent=2))
