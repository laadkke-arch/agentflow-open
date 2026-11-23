"""Read-only AF-RES-069 delivery audit. Output is a receipt, not product efficacy."""
from pathlib import Path
import collections
import csv
import datetime
import hashlib
import io
import json
import re
import shlex
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[5]
OWN = "docs/workstreams/research/AF-RES-069/"
P = ROOT / OWN
FREEZE = "03d1e436cfa7dc209b57b19508ef4b2e75942824"
SEAL = "de1727aada52835ebcde4ff1c92c3940db215476"
BASE = "76b8c1d15812fbf91b879f8444fd188ae7445802"
checks = []

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)

def check(name, ok, detail=None):
    checks.append({"check": name, "pass": bool(ok), "detail": detail})

def jl(name):
    return [json.loads(x) for x in (P / name).read_text().splitlines()]

head = git("rev-parse", "HEAD").decode().strip()
required = ["SCOPE.md", "frame.csv", "problems.jsonl", "queries.jsonl", "runs.jsonl", "sources.jsonl", "judgments.csv", "decisions.md", "RESULT.md", "SELF_CHECK.md", "manifest.json", "evidence/acceptance-evidence.json"]
check("required result files exist (HANDOFF intentionally later)", all((P / f).is_file() for f in required), required)

json_errors=[]
for f in sorted(P.rglob("*.jsonl")):
    for line_num, line in enumerate(f.read_text().splitlines(),1):
        try:
            if not line.strip():
                raise ValueError("blank JSONL line")
            json.loads(line)
        except Exception as e:
            json_errors.append({"file":str(f.relative_to(P)),"line":line_num,"error":str(e)})
for f in sorted(P.rglob("*.json")):
    try:
        json.loads(f.read_text())
    except Exception as e:
        json_errors.append({"file":str(f.relative_to(P)),"error":str(e)})
check("JSON and strict JSONL parse",not json_errors,json_errors)

csv_shapes={}
for name in ["frame.csv","judgments.csv"]:
    rr=list(csv.reader((P/name).open(newline="")))
    width=len(rr[0]); bad=[i for i,r in enumerate(rr,1) if len(r)!=width]
    csv_shapes[name]={"rows_without_header":len(rr)-1,"columns":width,"bad_lines":bad}
    check(name+" rectangular",not bad,csv_shapes[name])
check("75 metadata rows and 90 judgment rows",csv_shapes["frame.csv"]["rows_without_header"]==75 and csv_shapes["judgments.csv"]["rows_without_header"]==90)

queries=jl("queries.jsonl"); runs=jl("runs.jsonl"); sources=jl("sources.jsonl")
js=list(csv.DictReader((P/"judgments.csv").open(newline="")))
problems=jl("problems.jsonl")
counts=json.loads((P/"evidence/counts.json").read_text())
final=json.loads((P/"evidence/final-counts.json").read_text())
check("3 problems,18 queries,90 ranks,99 source records",(len(problems),len(queries),len(runs),len(sources))==(3,18,90,99))
for name,key,rows in [("problems","problem_id",problems),("runs","rank_id",runs),("sources","source_id",sources),("judgments","rank_id",js)]:
    ids=[x[key] for x in rows]
    check(name+" unique keys",len(ids)==len(set(ids)),len(ids))
sids={x['source_id'] for x in sources}; rids={x['rank_id'] for x in runs}
check("rank/source/judgment joins", all(x['source_id'] in sids for x in runs) and all(x['source_id'] in sids and x['rank_id'] in rids for x in js) and {x['rank_id'] for x in js}==rids)
group=collections.defaultdict(list)
for r in runs:group[r['query_id']].append(r)
check("18 groups each retain original ranks1..5",len(group)==18 and all(sorted(x['original_rank'] for x in g)==[1,2,3,4,5] for g in group.values()))
check("no missing returned slots",all(x['slot_present'] for x in runs))
check("each arm has three fixed queries",all(sum(qid.startswith(p+'-'+a+'-Q') for qid in group)==3 for p in ['P1','P2','P3'] for a in ['A','B']))

for f in ['problems.jsonl','queries.jsonl','arms/A/input.json','arms/B/input.json']:
    check("input bytes unchanged "+f,(P/f).read_bytes()==git('show',FREEZE+':'+OWN+f))
for f in ['runs.jsonl','judgments.csv','evidence/counts.json','evidence/costs.jsonl']:
    check("trial bytes unchanged "+f,(P/f).read_bytes()==git('show',SEAL+':'+OWN+f))
original=git('show',SEAL+':'+OWN+'sources.jsonl')
check("sealed source prefix byte-preserved",(P/'sources.jsonl').read_bytes().startswith(original),{"sealed_rows":len(original.splitlines()),"current_rows":len(sources)})
check("postseal sources excluded from trial hits",all(x.get('trial_hit') is False and x.get('phase')=='postseal' for x in sources[85:]))

required_fields=['source_id','lineage_id','original_url','author','version','checked_utc','sections_read','confirmed_claims','cannot_determine','counterexample_or_unknown','direct_read','count_toward_minimum']
missing={x['source_id']:[k for k in required_fields if k not in x] for x in sources}
missing={k:v for k,v in missing.items() if v}
check("source claim and limitation fields explicit",not missing,missing)
counted=[x for x in sources if x.get('count_toward_minimum')]
check("26 independent counted families and all direct",len(counted)==26 and len({x['lineage_id'] for x in counted})==26 and all(x['direct_read'] for x in counted))
check("frozen minimum25, source roles3+6+16, auxiliary increment1",counts['independent_works_counted']==25 and counts['counted_works_by_first_role']=={'selected_problem':3,'screening':6,'trial_return':16} and final['postseal_new_counted_independent_families']==1)
arm=counts['arm_stats']
check("same caps, unequal actual costs preserved",all(x['query_attempts']==3 and x['new_url_open_attempts']==5 for x in arm) and sum(x['research_operations'] for x in arm if x['arm']=='A')==25 and sum(x['research_operations'] for x in arm if x['arm']=='B')==33 and sum(x['same_document_extra_accesses'] for x in arm)==10)
check("coverage27/76 URLs and18/52 lineages",(counts['trial_direct_read_url_union'],counts['trial_return_url_union'],counts['trial_direct_read_lineage_union'],counts['trial_return_lineage_union'])==(27,76,18,52))
check("strict empty, observed3, no confirmed full fit",counts['strict_pair_denominator']==0 and counts['observed_pair_denominator']==3 and all(str(x['confirmed_fit']).lower()=='false' for x in js))

report=(P/'RESULT.md').read_text(); lines=report.splitlines(); tables=[]; current=[]; errors=[]
for lineno,line in enumerate(lines+[""],1):
    if line.startswith('|'):
        current.append((lineno,line))
    elif current:
        sizes=[len(re.split(r'(?<!\\)\|',s))-2 for _,s in current]
        tables.append({'start_line':current[0][0],'lines':len(current),'columns':sizes[0]})
        errors += [{'line':n,'columns':k,'expected':sizes[0]} for (n,_),k in zip(current,sizes) if k!=sizes[0]]
        current=[]
check("RESULT table rows rectangular",not errors,{'tables':tables,'errors':errors})
all_md_errors=[]
for f in sorted(P.rglob('*.md')):
    group_rows=[]
    for n,line in enumerate(f.read_text().splitlines()+[''],1):
        if line.startswith('|'):
            group_rows.append((n,len(re.split(r'(?<!\\)\|',line))-2))
        elif group_rows:
            expected=group_rows[0][1]
            all_md_errors.extend({'file':str(f.relative_to(P)),'line':i,'columns':w,'expected':expected} for i,w in group_rows if w!=expected)
            group_rows=[]
check("all delivered Markdown tables rectangular",not all_md_errors,all_md_errors)
check("top three tables before Q1",report.index('## 표 1')<report.index('## 표 2')<report.index('## 표 3')<report.index('## Q1'))
check("Q1..Q8 present",all('## Q'+str(i)+' ' in report for i in range(1,9)))
check("every fixed query appears in report",all(g[0]['query'] in report for g in group.values()))
check("all30 initial sources have detailed report rows",all(f'{a}-{p}-S{n:02}' in report for p in ['P1','P2','P3'] for a in ['A','B'] for n in range(1,6)))
check("no false first-body or header-renderer wording",'P2는 최초 본문에서' not in report and '제목 셀 renderer 폭24' not in report)
last=report[report.index('## 남은 약점 3건'):]
check("last section three weaknesses with contrary observations",all(re.search(r'^'+str(i)+r'\. ',last,re.M) for i in range(1,4)) and last.count('최소')>=3)

coverage=json.loads((P/'evidence/question-coverage.json').read_text())
check("Q1..Q8 evidence and counterexample coverage",{x['question'] for x in coverage}==set(range(1,9)) and all(x.get('result_location') and x.get('evidence_ids') and x.get('evidence_sections') and x.get('counterexample_selection_and_result') and x.get('unknown_and_resume') for x in coverage))

changed=set(git('diff','--name-only',BASE,'HEAD').decode().splitlines())
changed.update(git('diff','--name-only').decode().splitlines())
changed.update(git('diff','--cached','--name-only').decode().splitlines())
changed.update(git('ls-files','--others','--exclude-standard').decode().splitlines())
check("all tracked/untracked changes owned",all(x.startswith(OWN) for x in changed),sorted(changed))
check("dot-control unchanged from assignment",git('show','HEAD:docs/automation/dot-control.json')==git('show',BASE+':docs/automation/dot-control.json'))

bad=sum(not x['pass'] for x in checks)
out={"task_id":"AF-RES-069","command":shlex.join(["python","-B","docs/workstreams/research/AF-RES-069/evidence/verify.py",*sys.argv[1:]]),"cwd":str(ROOT),"head_sha":head,"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"scope":"record consistency, table shape, frozen bytes, allowed paths; not product execution or source truth","check_count":len(checks),"failed_count":bad,"exit_code":1 if bad else 0,"checks":checks}
if len(sys.argv)==3 and sys.argv[1]=='--output':
    dest=Path(sys.argv[2]).resolve()
    if not dest.is_relative_to(P):
        raise ValueError('receipt output must be in owned_path')
    dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
raise SystemExit(1 if bad else 0)
