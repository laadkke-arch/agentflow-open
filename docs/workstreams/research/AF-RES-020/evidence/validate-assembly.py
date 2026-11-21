"""Check AF-RES-020 structure, fixed provenance, and honestly declared gaps.
No earlier retrieval experiments, external sites, or other new tasks are read.
Exit 0 means no structural inconsistency, not that all research conditions were met.
"""
import argparse,collections,datetime,hashlib,itertools,json,re,subprocess,sys,urllib.parse
from pathlib import Path
P=Path(__file__).resolve().parents[1]
ROOT=next(x for x in P.parents if (x/'.git').exists())
OWN=P.relative_to(ROOT).as_posix()+'/'
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',help='Optional report path; must remain within owned_path')
parser.add_argument('--post-handoff',action='store_true')
args=parser.parse_args()
if args.post_handoff and args.output:
 parser.error('--post-handoff is read-only and cannot be combined with --output')
checks=[];errors=[];blob_cache={};fixed=json.loads((P/'evidence/fixed-inputs.json').read_text())
def check(name,value,detail=''):
 checks.append({'check':name,'passed':bool(value),'detail':detail})
 if not value:errors.append(name+(': '+str(detail) if detail else ''))
def read(n):return json.loads((P/n).read_text())
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,stderr=subprocess.PIPE)
def blob(sha,path):
 k=(sha,path)
 if k not in blob_cache:blob_cache[k]=git('show',sha+':'+path)
 return blob_cache[k]
def safe_ref(r,where):
 sha=r.get('sha');path=r.get('path');task=r.get('task',r.get('source_task'))
 check(where+' full SHA',isinstance(sha,str) and re.fullmatch(r'[0-9a-f]{40}',sha) is not None)
 if task in fixed['fixed']:
  check(where+' fixed SHA',sha==fixed['fixed'][task])
  check(where+' task path binding',isinstance(path,str) and path.startswith('docs/workstreams/research/'+task+'/'))
 elif task=='workspace-foundation':
  check(where+' fixed governance SHA/path',sha==fixed['source_commit'] and path in ['docs/automation/dot-control.json','docs/DOT_AUTOMATION.md'])
 else:check(where+' registered source task',False,task)
 try:raw=blob(sha,path)
 except Exception as e:check(where+' blob exists',False,str(e));return
 check(where+' blob exists',True)
 for frag in re.findall(r'L\s*(\d+(?:\s*[–-]\s*\d+)?(?:\s*[·,]\s*\d+(?:\s*[–-]\s*\d+)?)*)',r.get('locator','')):
  for part in re.split(r'[·,]',frag):
   ns=[int(x) for x in re.findall(r'\d+',part)];check(where+' line bounds',1<=ns[0]<=ns[-1]<=len(raw.splitlines()),part)
required_files=['SCOPE.md','PROGRESS.md','bundles.json','CLAIM_CHECK.json','RELATIONS.json','RELATIONS.md','CONFLICTS.md','CONFIGS.md','DECISIONS.md','GLOSSARY.md','INDEX_PROPOSAL.md','CROSSFIELD.md','RESULT.md','sources.json','SELF_CHECK.md','evidence/acceptance-evidence.json','evidence/NEXT_CHECKS.md']
for f in required_files:check('required file '+f,(P/f).is_file())
for f in P.rglob('*.json'):
 try:json.loads(f.read_text())
 except Exception as e:check('JSON parse '+f.name,False,str(e))
b=read('bundles.json');bundles=b['bundles'];ids=[x['id'] for x in bundles];claims=read('CLAIM_CHECK.json')
check('bundle count >=15',len(bundles)>=15,len(bundles));check('bundle IDs unique',len(set(ids))==len(ids));check('bundle files match metadata',set(ids)=={f.stem for f in (P/'bundles').glob('*.md')})
axes={'scope','identity','storage','retrieval','input','maintenance','evaluation','assembly'};check('eight brief axes',set(q for x in bundles for q in x['brief_questions'])==axes)
cc=collections.Counter(x['bundle_id'] for x in claims)
for x in bundles:
 text=(P/x['document']).read_text();heads=[l[3:].strip() for l in text.splitlines() if l.startswith('## ')]
 check(x['id']+' eight fields',all(any(h.startswith(p) for h in heads) for p in ['식별·질문','짧은 핵심','근거','대안','반례·한계','관계','검토','다음 확인']))
 check(x['id']+' >=3 claims',cc[x['id']]>=3,cc[x['id']])
 check(x['id']+' claim IDs exact',set(x['claim_ids'])=={c['claim_id'] for c in claims if c['bundle_id']==x['id']})
 for v in ['일치','불일치','확인 불가']:check(x['id']+' verdict '+v,x['claim_check_counts'][v]==sum(c['bundle_id']==x['id'] and c['verdict']==v for c in claims))
 for i,r in enumerate(x['source_refs']):safe_ref(r,x['id']+':source'+str(i))
fields=['claim_id','bundle_id','claim','source_task','sha','path','locator','second_hop_path','verdict','mismatch_type','note']
check('claim count >=60',len(claims)>=60,len(claims));check('claim IDs unique',len({c['claim_id'] for c in claims})==len(claims));check('distinct assertion groups >=60',len({c['assertion_group_id'] for c in claims})>=60)
second=[]
for c in claims:
 check(c['claim_id']+' required fields',all(k in c for k in fields));check(c['claim_id']+' allowed verdict',c['verdict'] in ['일치','불일치','확인 불가']);safe_ref(c,c['claim_id'])
 if c['verdict']=='불일치':check(c['claim_id']+' mismatch type',c['mismatch_type'] in ['수치 오류','분모 누락','관측 창 누락','과대 일반화','인용 위치 오류'])
 if c['second_hop_path']:
  second.append(c);check(c['claim_id']+' distinct second file',c['second_hop_path']!=c['path']);check(c['claim_id']+' second locator',bool(c.get('second_hop_locator')))
  safe_ref({'sha':c['second_hop_sha'],'path':c['second_hop_path'],'locator':c['second_hop_locator'],'task':c['source_task']},c['claim_id']+':second')
check('second-hop >=20 and >=1/3',len(second)>=20 and 3*len(second)>=len(claims),f'{len(second)}/{len(claims)}')
check('all12 tasks audited',set(c['source_task'] for c in claims)==set(fixed['fixed']))
r=read('RELATIONS.json');pairs=r['pairs'];expected=set(itertools.combinations(sorted(ids),2));actual=[(x['a'],x['b']) for x in pairs]
check('all pairs exactly once',len(actual)==len(set(actual)) and set(actual)==expected,len(actual));types=collections.Counter();adj={i:[] for i in ids}
for pair in pairs:
 check('relation nonempty '+pair['a']+pair['b'],bool(pair['relations']))
 for rel in pair['relations']:
  typ=rel['type'];types[typ]+=1;check('allowed relation '+rel['relation_id'],typ in ['함께 씀','충돌','선행','대체','무관'])
  if typ!='무관':
   check(rel['relation_id']+' condition/source',bool(rel['condition']) and bool(rel['source_refs']))
   for i,s in enumerate(rel['source_refs']):safe_ref(s,rel['relation_id']+':source'+str(i))
  if typ=='선행':
   check(rel['relation_id']+' direction',set([rel['from'],rel['to']])==set([pair['a'],pair['b']]));adj[rel['from']].append(rel['to'])
check('relation aggregate counts',dict(types)==r['relation_counts']);active=set();done=set()
def visit(v):
 if v in active:return False
 if v in done:return True
 active.add(v)
 for w in adj[v]:
  if not visit(w):return False
 active.remove(v);done.add(v);return True
check('declared prerequisite graph acyclic',all(visit(v) for v in ids))
cfs=read('evidence/conflicts-data.json');check('all review4 eleven IDs',set(f'CF{i:02}' for i in range(1,12))<=set(x['id'] for x in cfs))
for c in cfs:
 check(c['id']+' required conflict fields',all(c.get(k) for k in ['bundles','content','nature','status','minimum_evidence','unknown','source_refs','classification_reason']))
 check(c['id']+' allowed nature',c['nature'] in ['경험적','정의상','범위 차이']);check(c['id']+' allowed status',c['status'] in ['해소','부분 해소','미해소'])
 check(c['id']+' minimum question/data/scale',all(x in c['minimum_evidence'] for x in ['질문','자료','규모']))
 if int(c['id'][2:])<=11:check(c['id']+' review source retained',f"#{int(c['id'][2:])}," in c['review4_origin'])
 for i,s in enumerate(c['source_refs']):safe_ref(s,c['id']+':source'+str(i))
cfg=read('evidence/configs-data.json');check('three required starts',{'C0','C1','C2'}<=set(c['id'] for c in cfg))
for c in cfg:
 check(c['id']+' configuration fields',all(c.get(k) for k in ['included_bundles','principle','appropriate_conditions','day_one_preserve','hard_to_reverse','failure_signals','migration_path','major_costs','unknowns']))
 check(c['id']+' valid bundle IDs',set(c['included_bundles'])<=set(ids))
 missing=[]
 for v,ws in adj.items():
  for w in ws:
   if w in c['included_bundles'] and v not in c['included_bundles']:missing.append((v,w))
 check(c['id']+' active prerequisites addressed',not missing or (c['id']=='C0' and set(missing)=={('B12','B14')} and '역할별 성능 층화를 하지 않는다' in c['conditional_feature_policy']),str(missing))
check('no final design selected',b['final_design_selected'] is False)
dec=read('evidence/decisions-data.json');check('decisions >=10',len(dec)>=10)
for d in dec:check(d['id']+' decision fields',all(d.get(k) for k in ['decision','options','option_evidence','minimum_change_evidence','do_not_before','pending_input','unknowns']))
g=read('evidence/glossary-data.json');orig=json.loads(blob(fixed['fixed']['AF-RES-016'],'docs/workstreams/research/AF-RES-016/evidence/vocab-map-data.json'))
origrows=orig['rows'] if isinstance(orig,dict) else orig
check('016 original42 exact',g['base_016']['rows']==origrows and len(origrows)==42)
check('all vocab additions',len(g['additions_013_014_015'])==13 and len(g['additions_009'])==9);check('D3 retrofits cover001-012 tasks',len(g['d3_retrofit'])==13)
src=read('sources.json');source_ids={s['id']:s for s in src['sources']};check('source IDs unique',len(source_ids)==len(src['sources']))
req=['id','url','accessed_at_utc','source_type','title','version_or_date','sections_read','confirmed','limits','level','used_in']
for s in src['sources']+src['excluded']:check(s['id']+' source schema',all(k in s and s[k] not in [None,'',[]] for k in req))
check('original files >=30 all12',src['summary']['unique_fixed_original_files']>=30 and set(src['summary']['original_tasks'])==set(fixed['fixed']) and not src['summary']['required_primary_missing'])
ext=[s for s in src['sources'] if s['id'].startswith('X')];check('external actual bodies >=20',len(ext)>=20 and all(s['level']=='D1' and s.get('count_toward_minimum') is True for s in ext))
def site_key(s):
 host=urllib.parse.urlsplit(s['url']).hostname.removeprefix('www.')
 return 'amazon.com + investor-relations CDN' if host in ['aboutamazon.com','s2.q4cdn.com'] else host
sites=collections.Counter(site_key(s) for s in ext)
check('source record and exclusion counts',src['summary']['source_records']==len(src['sources']) and src['summary']['excluded']==len(src['excluded']))
check('external body count agrees',src['summary']['external_primary_bodies']==len(ext))
check('site counts recomputed',dict(sites)==src['summary']['external_site_counts']);check('site cap <=3',max(sites.values())<=3)
cat=collections.defaultdict(list)
for s in ext:
 for category in s.get('method_categories',[]):cat[category].append(s['id'])
check('external categories recomputed',dict(cat)==src['summary']['external_categories'])
internals=[s for s in src['sources'] if s['source_type'] in ['internal_result','internal_evidence','internal_fixed_code']]
originals=set();original_tasks=set()
for s in internals:
 rest=s['url'].split('/blob/',1)[1].split('#')[0];sha,path=rest.split('/',1);task=path.split('/research/',1)[1].split('/')[0]
 check(s['id']+' source fixed task binding',task in fixed['fixed'] and sha==fixed['fixed'].get(task) and s['version_or_date']==sha)
 check(s['id']+' original hash required',isinstance(s.get('content_sha256'),str) and re.fullmatch(r'[0-9a-f]{64}',s['content_sha256']) is not None)
 check(s['id']+' original blob/hash verified',hashlib.sha256(blob(sha,path)).hexdigest()==s.get('content_sha256'))
 originals.add((sha,path));original_tasks.add(task)
check('original count recomputed',len(originals)==src['summary']['unique_fixed_original_files'] and original_tasks==set(fixed['fixed']))
primary_names={'001':['HANDOFF.md','RESEARCH.md'],'002':['HANDOFF.md','RESEARCH.md'],'003':['HANDOFF.md','RESEARCH.md'],'004':['HANDOFF.md','PROTOCOL.md'],'009':['HANDOFF.md','GAP.md','LANDSCAPE.md'],'010':['HANDOFF.md','REPRESENTATIONS.md','TRANSFER_CASES.md'],'011':['HANDOFF.md','CODEBOOK.md','CASES.json'],'012':['HANDOFF.md','RESULTS.md'],'013':['HANDOFF.md','RESULT.md','SELF_CHECK.md'],'014':['HANDOFF.md','RESULT.md','SELF_CHECK.md'],'015':['HANDOFF.md','RESULT.md','SELF_CHECK.md'],'016':['HANDOFF.md','RESULT.md','VOCAB_MAP.md','evidence/vocab-map-data.json','CODEBOOK.md']}
primary_expected={(fixed['fixed']['AF-RES-'+t],'docs/workstreams/research/AF-RES-'+t+'/'+f) for t,fs in primary_names.items() for f in fs}
check('required33 original files actually logged',len(primary_expected)==33 and primary_expected<=originals)
check('alternative preservation >=3',len(set(cat['set_based']+cat['alternative_preservation']))>=3)
check('options/modularity >=3',len(set(cat['real_options']+cat['modularity']))>=3)
check('rationale >=3',len(cat['rationale'])>=3);check('evidence frameworks >=4',len(cat['evidence_decision'])>=4)
check('direct carrying cost reports >=2',{'X11','X18','X19'}<=set(s['id'] for s in ext))
check('crossfield >=4 named original domains',{'X01','X04','X09','X12','X14','X18','X22'}<=set(s['id'] for s in ext))
# Source hashes verify bytes, not content validity. Restrict to logged fixed objects.
for s in src['sources']:
 if s.get('content_sha256') and '/blob/' in s['url']:
  rest=s['url'].split('/blob/',1)[1].split('#')[0];sha,path=rest.split('/',1)
  check(s['id']+' source content hash',hashlib.sha256(blob(sha,path)).hexdigest()==s['content_sha256'])
qe=read('evidence/question-evidence.json');check('Q1-Q8 evidence rows',set(x['question'] for x in qe)==set('Q'+str(i) for i in range(1,9)))
for q in qe:
 check(q['question']+' IDs exist',set(q['source_ids'])<=set(source_ids))
 kinds={('external' if sid.startswith('X') else 'internal') for sid in q['source_ids']};check(q['question']+' two source kinds',len(kinds)>=2 and q['source_kind_count']>=2)
 check(q['question']+' falsification nonempty',bool(q['falsification_attempt']))
ce=read('evidence/counterexample-search.json');check('five counterexample records',len(ce['records'])==5);check('fifth honestly not found',ce['records'][-1]['found'] is False)
cs=read('evidence/claim-audit-summary.json');control=read('evidence/control-review-sol.json')
control_inputs=read('evidence/control-inputs.json')['controls'];control_key=read('evidence/control-key.json')['controls'];control_ids={f'T{i:02}' for i in range(1,19)}
for label,rows in [('input',control_inputs),('key',control_key),('review',control['controls'])]:check('control '+label+' IDs bijective',len(rows)==18 and {x['control_id'] for x in rows}==control_ids)
inputs_by_id={x['control_id']:x for x in control_inputs};key_by_id={x['control_id']:x for x in control_key};review_by_id={x['control_id']:x for x in control['controls']}
agreement=sum(review_by_id[i]['verdict']==key_by_id[i]['expected_verdict'] for i in control_ids if i in review_by_id and i in key_by_id)
control_counts=collections.Counter(x['verdict'] for x in control['controls'])
check('control verdicts directly agree',agreement==18 and cs['control_test']['expected_agreement']==agreement)
check('control direct 12/4/2 distribution',dict(control_counts)=={'불일치':12,'일치':4,'확인 불가':2} and dict(control_counts)==control['counts'])
check('control statements and fixed inputs unchanged',all(all(review_by_id[i].get(k)==v for k,v in item.items()) for i,item in inputs_by_id.items() if i in review_by_id))
check('controls excluded from main claims',cs['control_test']['counted_in_claim_check'] is False and control['counted_in_claim_check'] is False and not control_ids.intersection(c['claim_id'] for c in claims))
result=(P/'RESULT.md').read_text();schema=read('evidence/result-table-schema.json');positions=[result.find('## '+x) for x in schema['required_order']];check('five result sections correct order',all(x>=0 for x in positions) and positions==sorted(positions))
for t in schema['tables']:
 marker=f"### 표 {t['number']} —";check('table marker '+str(t['number']),marker in result)
 part=result.split(marker,1)[1].split('\n### 표 ',1)[0].split('\n## §2',1)[0];lines=part.splitlines();header=next(x for x in lines if x.startswith('| '));actual=[x.strip() for x in header.strip('|').split('|')]
 check('table headers '+str(t['number']),actual==t['headers']);row=[]
 for line in lines[lines.index(header)+2:]:
  if not line.startswith('|'):break
  row.append(line)
 check('table row count '+str(t['number']),len(row)==t['expected_rows'],len(row))
 separator=[x.strip() for x in re.split(r'(?<!\\)\|',lines[lines.index(header)+1].strip().strip('|'))]
 check('table separator '+str(t['number']),len(separator)==len(t['headers']) and all(re.fullmatch(r':?-{3,}:?',x) for x in separator))
 for i,line in enumerate(row):
  cells=re.split(r'(?<!\\)\|',line.strip().strip('|'))
  check(f"table {t['number']} row{i} column count",len(cells)==len(t['headers']),len(cells))
  check(f"table {t['number']} row{i} nonempty",all(x.strip() for x in cells))
sec4=result.split('## §4 ',1)[1].split('\n## §5 ',1)[0];check('exactly3 weaknesses',len(re.findall(r'^### ',sec4,re.M))==3)
for label in ['무엇이 어긋나거나 약한가','근거 위치','이것이 틀리면 바뀌는 결론','다음 조사 제안']:check('weakness field '+label,sec4.count('**'+label+':**')==3)
check('all Q answer headers',all(f'### Q{i}.' in result for i in range(1,9)))
accept=read('evidence/acceptance-evidence.json');check('acceptance schema',all(set(x)=={'condition','met','evidence','note'} and isinstance(x['met'],bool) for x in accept));check('original 13 condition truth',len(accept)>=13 and sum(x['met'] for x in accept[:13])==12 and accept[9]['met'] is False)
check('all unmet have reason/resume',all(x['note'] and x['evidence'] for x in accept if not x['met']))
check('all20 acceptance conditions retained',len(accept)==20 and len({x['condition'] for x in accept})==20)
check('four declared gaps remain false',{i for i,x in enumerate(accept) if not x['met']}=={9,17,18,19})
gap_names={9:'반례 다섯 가지 각각을 찾은 기록이 있다.',17:'이 작업에 필요한 호스트마다 익명 요청1회로 접근 여부와 응답 코드를 첫 커밋 전에 확인하고 PROGRESS.md에 기록한다.',18:'공통 작업 계약을 workbench.session start로 고정하고 인계 전 check --fetch를 통과한다.',19:'AF-RES-011 CASES.json은 구조와 집계만 읽는다.'}
check('gap condition identities retained',all(i<len(accept) and accept[i]['condition']==name for i,name in gap_names.items()))
check('reported state with gaps','REVIEW_READY_WITH_GAPS' in result and 'REVIEW_READY_WITH_GAPS' in (P/'SELF_CHECK.md').read_text())
# Check actual Markdown file links; external URLs and fragments do not imply new reads.
link_errors=[];local_links=0
for f in P.rglob('*.md'):
 for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',f.read_text()):
  u=m[1]
  if u.startswith(('http:','https:','mailto:','#','sandbox:')):continue
  target=u.split('#')[0]
  if not target:continue
  local_links+=1
  if not (f.parent/target).exists():link_errors.append(f.relative_to(P).as_posix()+':'+u)
check('relative Markdown files exist',not link_errors,link_errors)
changed=git('diff','--name-only',fixed['source_commit']).decode().splitlines();untracked=git('ls-files','--others','--exclude-standard').decode().splitlines();check('all writes in owned_path',all(x.startswith(OWN) for x in changed+untracked))
whitespace=subprocess.run(['git','diff',fixed['source_commit'],'--check'],cwd=ROOT,capture_output=True,text=True);check('git whitespace check',whitespace.returncode==0,whitespace.stdout+whitespace.stderr)
if args.post_handoff:
 check('handoff exists',(P/'HANDOFF.md').exists())
 if (P/'HANDOFF.md').exists():check('handoff status',(P/'HANDOFF.md').read_text().splitlines()[0]=='REVIEW_READY_WITH_GAPS')
 last=git('diff-tree','--no-commit-id','--name-only','-r','HEAD').decode().splitlines();check('last commit only handoff',last==[OWN+'HANDOFF.md'],last)
 check('selfcheck exists in handoff parent',bool(git('show','HEAD^:'+OWN+'SELF_CHECK.md')))
 previous=read('evidence/validation-report.json')
 check('pre-handoff validation recorded no structural errors',previous['status']=='VALID_WITH_DECLARED_GAPS' and not previous['errors'])
 expected_hash_keys={f.relative_to(P).as_posix() for f in P.rglob('*') if f.is_file() and f.suffix in ['.md','.json','.py'] and f not in [P/'HANDOFF.md',P/'evidence/validation-report.json']}
 check('validated input hash map complete',bool(expected_hash_keys) and set(previous['input_hashes'])==expected_hash_keys)
 check('validated inputs unchanged after selfcheck commit',all((P/f).is_file() and hashlib.sha256((P/f).read_bytes()).hexdigest()==h for f,h in previous['input_hashes'].items()))
 check('workingtree clean',not git('status','--porcelain').strip())
else:check('handoff not written before selfcheck',(not (P/'HANDOFF.md').exists()))
report={'status':'STRUCTURAL_ERRORS' if errors else 'VALID_WITH_DECLARED_GAPS','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'model':'GPT-6 Astra Pro','checked_git_head':git('rev-parse','HEAD').decode().strip(),'mode':'post_handoff_read_only' if args.post_handoff else 'workingtree_before_selfcheck_commit','checks_total':len(checks),'checks_passed':sum(x['passed'] for x in checks),'errors':errors,'research_end_conditions_met':sum(x['met'] for x in accept[:13]),'research_end_conditions_total':13,'unmet_conditions':[x for x in accept if not x['met']],'counts':{'bundles':len(bundles),'claims':len(claims),'assertion_groups':len({c['assertion_group_id'] for c in claims}),'second_hop':len(second),'pairs':len(pairs),'conditional_relationships':sum(n for t,n in types.items() if t!='무관'),'unrelated_pairs':types['무관'],'conflicts':len(cfs),'configs':len(cfg),'decisions':len(dec),'external_bodies':len(ext),'original_files':src['summary']['unique_fixed_original_files'],'local_links':local_links,'fixed_objects_checked':len(blob_cache)},'checks':checks,'limitations':['구조·근거위치·수치기록 일치 검사는 원판정의 진실성·제품효과를 새로 검증하지 않는다.','공통 manifest gate는 실패/미실시로 남으며 이 검사로 대체 PASS하지 않는다.','원 검색 파이프라인·외부 제품·D4·사람 평가를 재실행하지 않는다.']}
if args.output:
 out=Path(args.output).resolve()
 if not out.is_relative_to(P):raise ValueError('Report output outside owned_path')
 report['input_hashes']={f.relative_to(P).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in P.rglob('*') if f.is_file() and f!=out and f.suffix in ['.md','.json','.py']}
 out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['checks','input_hashes']},ensure_ascii=False))
sys.exit(1 if errors else 0)
