"""Check cross-file research invariants and links, not scientific completeness."""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import json
import re
import subprocess
from urllib.parse import unquote

BASE=Path(__file__).resolve().parent
REPO=BASE.parents[3]
OWNED=BASE.relative_to(REPO).as_posix()+'/'
START='1e741fd0def88ef56b1060a478d81f1985a4e760'


def git(*args):
    return subprocess.check_output(['git',*args],cwd=REPO,text=True).strip()


def csvread(name):
    return list(csv.DictReader((BASE/name).open(newline='')))


def number(v):
    s=str(v)
    return int(s) if re.fullmatch(r'\d+',s) else None


def main():
    issues=[];checks={}
    def check(name,condition,detail=''):
        checks[name]=dict(pass_=bool(condition),detail=detail)
        if not condition:issues.append(name+': '+str(detail))
    names=git('ls-files','--cached','--others','--exclude-standard','--',OWNED).splitlines()
    paths=[REPO/n for n in names if (REPO/n).is_file()]
    parse_count=0
    for p in paths:
        try:
            if p.suffix=='.json':json.loads(p.read_text());parse_count+=1
            elif p.suffix=='.jsonl':
                for s in p.read_text().splitlines():
                    if s.strip():json.loads(s)
                parse_count+=1
            elif p.suffix=='.csv':
                rows=list(csv.DictReader(p.open(newline='')))
                check('CSV rectangular '+str(p.relative_to(BASE)),all(None not in r for r in rows))
        except Exception as e:check('parse '+str(p.relative_to(BASE)),False,str(e))
    check('structured documents parse',not any(x.startswith('parse ') for x in issues),parse_count)
    required=['SCOPE.md','frame.csv','stimuli.csv','outcomes.csv','reproduce.md','claim-limits.md',
              'sources.jsonl','SELF_CHECK.md','RESULT.md','manifest.json','evidence/acceptance-evidence.json']
    check('required pre-HANDOFF artifacts',all((BASE/n).is_file() for n in required),required)
    sources=[json.loads(s) for s in (BASE/'sources.jsonl').read_text().splitlines()]
    ids={r['source_id'] for r in sources};counted=[r for r in sources if r['minimum_count']]
    cats=Counter(r['minimum_count_category'] for r in counted)
    check('source IDs unique',len(ids)==len(sources),len(sources))
    check('counted work lineages unique',len({r['work_lineage_id'] for r in counted})==len(counted),len(counted))
    check('minimum direct works',len(counted)>=20,dict(total=len(counted),categories=dict(cats)))
    check('category minimums',cats['original_human_report']>=8 and cats['stimulus_task_preregistration']>=3
          and cats['author_data_code_package']>=3 and cats['independent_truth_source']>=2)
    source_fields=['source_id','work_lineage_id','cohort_or_event_lineage_id','source_type','author','original_url',
                   'fixed_url','version_or_sha_or_date','read_utc','direct_read_locations','confirmed','scope_and_limits',
                   'questions','case_ids','minimum_count']
    check('source required fields',all(all(k in r for k in source_fields) for r in sources))
    stats=json.loads((BASE/'evidence/source-counts.json').read_text())
    check('source count ledger equality',stats['minimum_distinct_primary_works']==len(counted)
          and stats['categories']==dict(cats) and stats['ledger_records']==len(sources))
    check('two IR and two literacy reports',len(stats['information_retrieval_human_reports'])>=2
          and len(stats['factchecking_literacy_human_reports'])>=2)
    frame=csvread('frame.csv');fc=Counter(r['frame'] for r in frame if r['in_first25'].lower()=='true')
    check('fixed first25 both frames',fc=={'A':25,'B':25},dict(fc))
    check('frame discovery row counts',Counter(r['frame'] for r in frame)=={'A':34,'B':33,'S':7})
    stimuli=csvread('stimuli.csv')
    missing_ids=[]
    for r in stimuli:
        for sid in r['source_ids'].split(';'):
            sid=sid.strip()
            if sid and sid not in ids:missing_ids.append((r['stimulus_id'],sid))
    check('stimulus source ID links',not missing_ids,missing_ids)
    check('source inventory separated from reading',sum(r['case_id']=='A02' for r in stimuli)==72)
    outcomes=csvread('outcomes.csv')
    check('outcome IDs unique',len({r['outcome_id'] for r in outcomes})==len(outcomes),len(outcomes))
    impossible=[]
    for r in outcomes:
        for a,n in [('acceptance_n','acceptance_N'),('final_correct_n','final_correct_N')]:
            v,d=number(r[a]),number(r[n])
            if v is not None and d is not None and not 0<=v<=d:impossible.append((r['outcome_id'],a,v,d))
        if r['acceptance_n']=='0/0' or r['final_correct_n']=='0/0':impossible.append(r['outcome_id'])
    check('outcome bounds and no fictitious zero cells',not impossible,impossible)
    independent=json.loads((BASE/'streams/root/independent-calculation.json').read_text())
    pri=[r for r in outcomes if r['sample_layer']=='B01-main-observed']
    comparisons=[]
    for r in pri:
        tr='FM' if r['truth_stratum']=='오주장' else 'T';arm='0' if r['condition']=='control' else '1'
        q=next(x for x in independent['groups'] if x['sample']=='all_observed_categorical_response' and x['truth']==tr and x['arm']==arm)
        comparisons.append(number(r['acceptance_n'])==q['accepted'] and number(r['acceptance_N'])==q['observed']
            and number(r['final_correct_n'])==q['correct'] and number(r['CND_or_abstention_n'])==q['CND'])
    check('primary integer cells match independent pass',len(pri)==4 and all(comparisons))
    check('independent calculation disagreements observed0',independent['aggregate_disagreements']==[])
    result=(BASE/'RESULT.md').read_text();blocks=result.strip().split('\n\n')
    check('first content is mandatory table1',blocks[0].startswith('| 연구·표본층 |'))
    check('second content is mandatory table2',blocks[1].startswith('| 코호트·조건·비교 |'))
    table_rows=[]
    for table_i,expected_columns in [(0,7),(1,8)]:
        lines=[s for s in blocks[table_i].splitlines() if s.strip()]
        counts=[len(s.strip().strip('|').split('|')) for s in lines]
        check('mandatory table columns '+str(table_i+1),all(x==expected_columns for x in counts),counts)
        table_rows.append(len(lines)-2)
    check('main6 plus separate supplement2 in table1',table_rows[0]==8,table_rows)
    check('Q1 through Q7 exactly once',re.findall(r'^## (Q[1-7])\.',result,re.M)==['Q1','Q2','Q3','Q4','Q5','Q6','Q7'])
    last=blocks[-1].splitlines()
    check('last weakness table exactly3rows',last[0].startswith('| 불일치·약점 |') and len(last)==5,
          dict(lines=len(last),header=last[0]))
    links=[];badlinks=[]
    for p in paths:
        if p.suffix!='.md':continue
        for href in re.findall(r'(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)',p.read_text()):
            href=href.strip().strip('<>')
            if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:',href) or href.startswith('#'):continue
            target=unquote(href.split('#')[0]);q=p.parent/target;links.append((str(p.relative_to(BASE)),href))
            if not q.exists():badlinks.append((str(p.relative_to(BASE)),href))
    check('local Markdown links exist',not badlinks,dict(checked=len(links),broken=badlinks))
    changed=git('diff','--name-only',START,'HEAD').splitlines()+git('diff','--name-only','HEAD').splitlines()
    check('all repository changes in owned path',all(n.startswith(OWNED) for n in changed),len(set(changed)))
    control=REPO/'docs/automation/dot-control.json'
    original=subprocess.check_output(['git','show',START+':docs/automation/dot-control.json'],cwd=REPO)
    check('dot-control unchanged',control.read_bytes()==original)
    check('assigned branch',git('branch','--show-current')=='work/research-af-res-062')
    leaks=[]
    for p in paths:
        if p.suffix not in ('.md','.json','.jsonl','.csv','.py'):continue
        s=p.read_text()
        if re.search(r'R_[A-Za-z0-9]{12,}',s):leaks.append(str(p.relative_to(BASE)))
        if re.search(r'https?://[^\s\"<>]*(?:X-Amz-Signature=|\?sig=)',s):leaks.append(str(p.relative_to(BASE))+':signedURL')
    check('no public participant IDs or temporary signed URLs republished',not leaks,leaks)
    if not issues:
        ap=BASE/'evidence/acceptance-evidence.json';a=json.loads(ap.read_text())
        for c in a['criteria']:
            if c['criterion_id']=='C11':
                c['status']='MET';c['evidence'].append(dict(path='evidence/artifact-validation.json',location='mandatory tables/links checks')) if not any(x['path']=='evidence/artifact-validation.json' for x in c['evidence']) else None
        ap.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
    output=dict(executed_utc=datetime.now(timezone.utc).isoformat(),actor='root AI, stdlib validator',
        command='python -B docs/workstreams/research/AF-RES-062/validate_artifacts.py',head_sha=git('rev-parse','HEAD'),
        scope='working-tree content before final commit; fixed SHA/hash equality checked separately',
        status='PASS' if not issues else 'FAIL',research_acceptance_status='PARTIAL_HANDOFF',
        checks=checks,issues=issues,table_rows=table_rows,
        content_sha256={n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in required})
    (BASE/'evidence/artifact-validation.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(status=output['status'],issues=issues,checks=len(checks),sourceworks=len(counted),
        sources=len(sources),frame_rows=len(frame),stimulus_rows=len(stimuli),outcome_rows=len(outcomes),
        mandatory_table_rows=table_rows,local_links=len(links)),ensure_ascii=False,indent=2))
    raise SystemExit(1 if issues else 0)


if __name__=='__main__':main()
