"""Validate research artifacts, source references, frozen coding, and arithmetic.

This validates what is present. It deliberately does not turn missing research
eligibility or causal evidence into a passing acceptance condition.
"""
import json,re,hashlib,collections,subprocess,datetime,argparse
from pathlib import Path
P=Path(__file__).resolve().parents[1];REPO=P.parents[3]
ap=argparse.ArgumentParser();ap.add_argument('--no-write',action='store_true');ap.add_argument('--check-handoff',action='store_true');args=ap.parse_args()
def read(f):return json.loads((P/f).read_text())
def sha(f):return hashlib.sha256((P/f).read_bytes()).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=REPO,text=True).strip()
checks=[]
def check(name,met,detail):checks.append({'check':name,'passed':bool(met),'detail':detail})
alljson=list(P.rglob('*.json'))
for f in alljson:json.loads(f.read_text())
check('All JSON parses',True,len(alljson))
c=read('cases/CASES.json');s=read('sources.json');sid={x['id']:x for x in s['sources']};a=read('coding/coder-a.json');b=read('coding/coder-b.json');g=read('coding/agreement.json');st=read('evidence/statistics.json')
check('Unique case/source IDs',len({x['id'] for x in c})==len(c) and len(sid)==len(s['sources']),{'cases':len(c),'sources':len(sid)})
required='id source_family primary_urls built missed missed_form missed_contribution missed_relation decision_date discovery_date existed_at_decision prominence_at_decision need_statement lexical_overlap cost_indicators discovery_path miss_reason outcome coder_b'.split()
missing=[{'id':x['id'],'missing':[k for k in required if k not in x]} for x in c if any(k not in x for k in required)]
check('Required case fields',not missing,missing)
reqs='id url accessed_at_utc source_type title version_or_date sections_read confirmed limits level used_in'.split()
missing=[{'id':x['id'],'missing':[k for k in reqs if k not in x]} for x in s['sources'] if any(k not in x for k in reqs)]
check('Required source fields',not missing,missing)
refs=[(x['id'],z) for x in c for z in x['source_ids'] if z not in sid]
check('All case source references resolve',not refs,refs)
badneed=[x['id'] for x in c if not 1<=len(x['need_statement']['text'].split())<=25]
badquote=[x['id'] for x in c if not 1<=len(x['official_description'].get('text','').split())<=25]
check('Need and official short-description word limits',not badneed and not badquote,{'needs':badneed,'descriptions':badquote})
exbad=[x['id'] for x in c if x['existed_at_decision'].get('verdict') not in ['yes','no','unknown'] or not x['existed_at_decision'].get('evidence_url') or (x['existed_at_decision']['verdict']=='unknown' and not any(x['existed_at_decision'].get(k) for k in ['reason','note']))]
check('Every existence judgment has evidence and unknown reason',not exbad,exbad)
check('No D0 credited as source',not any(x['level']=='D0' for x in s['sources']),{'excluded':len(s['excluded']),'level_counts':dict(collections.Counter(x['level'] for x in s['sources']))})
counts=read('evidence/methods/counts.json')
check('Methods minimum and site cap',counts['credited_after_site_cap']>=25 and counts['site_cap_met'] and all(x['met'] for x in counts['required_minima'].values()) and counts['q8_primary_mechanism_paths']['met'],{'credited':counts['credited_after_site_cap'],'subminima':counts['required_minima'],'provenance':counts['q8_primary_mechanism_paths']})
A={x['id']:x for x in a['labels']};B={x['id']:x for x in b['labels']};axes=['missed_form','missed_contribution','missed_relation','legacy_S1','late_discovery_status']
check('Forty complete independent-context coding rows',len(A)==len(B)==len(c)==40 and set(A)==set(B)=={x['id'] for x in c},b['model'])
check('Frozen A and raw B hashes',sha('coding/coder-a.json')=='84243b48d11f6cd60f3bf9576c0324b3c1446dc9aa68763df9cac58a630a21b4' and sha('coding/coder-b.json')==g['B_raw_sha256'] and sha('coding/blind-packet.json')==g['blind_packet_sha256'],{'A':sha('coding/coder-a.json'),'B':sha('coding/coder-b.json')})
check('Cases preserve original A labels and raw B labels',all(all(x[k]==A[x['id']][k] for k in axes) and x['coder_b']==B[x['id']] for x in c),'Cost-unit correction did not recode labels.')
for k in axes:
    n=sum(A[i][k]==B[i][k] for i in A);check('Agreement arithmetic '+k,n==g['axes'][k]['agree'] and abs(n/40-g['axes'][k]['agreement'])<1e-12,{'agree':n,'n':40})
order=subprocess.run(['git','merge-base','--is-ancestor','70fa1b691601a0cc9fb751db518fd4c5cad06bf8','d137422f1ff322f28bc09434cf50a7f31e31a591'],cwd=REPO).returncode==0
firstB=git('log','--reverse','--diff-filter=A','--format=%H','--','docs/workstreams/research/AF-RES-017/coding/coder-b.json').splitlines()[0]
check('A remote freeze precedes first committed B response',order and firstB=='d137422f1ff322f28bc09434cf50a7f31e31a591',{'A':'70fa1b691601a0cc9fb751db518fd4c5cad06bf8','B':firstB})
body=(P/'RESULT.md').read_text();heads=[
['사례 ID','출처 계열','원문 주소(고정 판·날짜)','만든 것','늦게 안 것','형태(S1)','기여(S2)','관계(013 분류)','결정일','발견일','결정 시점 존재(근거)','늦은 발견 비용 지표','발견 경로','결과(유지·되돌림·정당한 자체 구현)','미확인'],
['종류','사례 수(분모)','결정 시점 존재 확인 수','당시 유명했음 수','어휘 겹침 중앙값','비용 지표별 중앙값','대표 사례 ID','반례 사례 ID','미확인'],
['분야','늦은 발견·중복의 형태','측정 방식과 수치','우리 문제와 같은 점','다른 점','근거 주소','미확인'],
['주장','근거 자료 주소','확인한 내용','반증 시도','미확인']]
tables=[];lines=body.splitlines()
for i,l in enumerate(lines):
    if l.startswith('| ') and i+1<len(lines) and re.match(r'^\|\s*---',lines[i+1]):
        cols=[x.strip() for x in re.split(r'(?<!\\)\|',l)[1:-1]];rows=[];j=i+2
        while j<len(lines) and lines[j].startswith('| '):rows.append([x.strip() for x in re.split(r'(?<!\\)\|',lines[j])[1:-1]]);j+=1
        tables.append((cols,rows))
check('Required four tables and exact column names',len(tables)>=4 and all(tables[i][0]==heads[i] for i in range(4)),[x[0] for x in tables[:4]])
check('Required tables have no blank or malformed cells',all(all(len(row)==len(h) and all(row) for row in rows) for h,rows in tables[:4]),[len(rows) for h,rows in tables[:4]])
check('Case table has forty observations',len(tables[0][1])==40,len(tables[0][1]))
sections=re.findall(r'^## §(\d)',body,re.M);sec4=body.split('## §4',1)[1].split('## §5',1)[0]
check('Required section order and exactly three weaknesses',sections==['1','2','3','4','5'] and len(re.findall(r'^### 4\.\d',sec4,re.M))==3,sections)
check('All Q1–Q8 headings present',all(re.search(r'^### Q'+str(i)+r'\.',body,re.M) for i in range(1,9)),list(range(1,9)))
qd=read('evidence/q-evidence.json');qbad=[]
for row in qd:
    types={sid[z]['source_type'] for z in row['source_ids'] if z in sid}
    if len(types)<2 or any(z not in sid for z in row['source_ids']) or not row['disconfirmation']:qbad.append(row['question'])
check('Each question has two source kinds and a countercheck',not qbad,qbad)
files=git('diff','--name-only','0209117d8ec00af39bd25844d52a18edc7323207','HEAD').splitlines()
check('Committed writes stay in owned path',all(x.startswith('docs/workstreams/research/AF-RES-017/') for x in files),len(files))
check('Scope text unchanged since preregistration',git('show','9485f37a6b5fb78869468b425850fa49779de847:docs/workstreams/research/AF-RES-017/SCOPE.md')==(P/'SCOPE.md').read_text().strip(),'9485f37a6b5fb78869468b425850fa49779de847')
check('No public profile/login or full body fields retained',not any(k in f.read_text() for f in alljson for k in ['"avatar_url":','"profile_url":','"login":','"body":','"patch":']),'Professional publication author names and source URLs retained for attribution.')
check('Numeric-cost and unconfirmed-cost partitions cover forty',len(st['numeric_cost_ids'])+len(st['cost_unconfirmed_ids'])==40 and not set(st['numeric_cost_ids'])&set(st['cost_unconfirmed_ids']),{'numeric_related':len(st['numeric_cost_ids']),'unconfirmed':len(st['cost_unconfirmed_ids'])})
if (P/'SELF_CHECK.md').exists():
    sc=(P/'SELF_CHECK.md').read_text();ae=read('evidence/acceptance-evidence.json')
    check('Self-check has eight questions and exact requested columns','| 세부 질문 | 답 한 줄 | 붙은 출처 ID(종류 수) | 반증 시도(쓴 질의·자료와 결과) | 남은 불확실성 |' in sc and len(re.findall(r'^\| Q[1-8] \|',sc,re.M))==8,'SELF_CHECK.md §1')
    check('Ten substantive conditions retain the known failures',len(ae)==10 and [i+1 for i,x in enumerate(ae) if not x['met']]==[1,2,10] and all(x.get('evidence') and x.get('note') for x in ae),{'conditions':len(ae),'unmet':[i+1 for i,x in enumerate(ae) if not x['met']]})
    ce=read('evidence/counterexamples.json')
    check('Five counterexample searches have queries and results',len(ce)==5 and all(x['executed_queries'] and x['query_log'] and x['records'] and x['result'] for x in ce),len(ce))
    check('Remote A body equals the frozen local body',read('evidence/remote-coding-verification.json')['remote_file_read']['content_equal_to_local'],'Original GitHub file read and git blob identity')
if args.check_handoff:
    check('Handoff status explicitly records gaps',(P/'HANDOFF.md').read_text().splitlines()[0]=='REVIEW_READY_WITH_GAPS','The unmet research criteria are not converted to PASS.')
result={'run_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checked_head':git('rev-parse','HEAD'),'level':'D3-run','scope':'Artifact integrity and arithmetic only; substantive acceptance separately records unmet criteria.','all_structural_checks_passed':all(x['passed'] for x in checks),'checks':checks}
if not args.no_write:(P/'evidence/validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'all_structural_checks_passed':result['all_structural_checks_passed'],'checks':len(checks),'failed':[x for x in checks if not x['passed']]},ensure_ascii=False))
raise SystemExit(0 if result['all_structural_checks_passed'] else 1)
