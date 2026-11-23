"""Reproduce AF-RES-052 Python catalogue metadata; no network or destination reads."""
from pathlib import Path
import ast, csv, hashlib, json, re
from datetime import datetime, timezone

P = Path(__file__).resolve().parent
C = P / 'cache'
SHA = '5ecbc0db967843e64d55da165b72e773888860c5'
BASE = f'https://github.com/pypa/packaging.python.org/blob/{SHA}/source/key_projects.rst'
s = (C/'key_projects.rst').read_text()
lines = s.splitlines()
tree = json.loads((C/'catalog-tree.json').read_text())['tree']
blobs = {x['path']:x['sha'] for x in tree}
headings = []
for i in range(1, len(lines)):
    if re.fullmatch(r'([=#])\1{1,}', lines[i]) and lines[i-1].strip() and not re.fullmatch(r'[=#]+',lines[i-1]):
        title=lines[i-1].strip()
        if title=='Project Summaries': continue
        headings.append({'title':title,'line':i,'level':1 if lines[i][0]=='#' else 2})
for j,h in enumerate(headings):
    h['end']=next((x['line']-1 for x in headings[j+1:] if x['level']<=h['level']),len(lines))
    h['id']=f'PY-H{j+1:02d}'
    h['kind']='organizational' if h['level']==1 else 'project'

refs={}
for m in re.finditer(r'^\.\. _`?([^`:\n]+)`?:\s*(https?://\S+)',s,re.M): refs[m[1].lower()]=m[2]
tokens=[]
pat=re.compile(r':(?P<role>any|doc|pypi|gh|ref|term|pep):`(?P<rolebody>[^`]+)`|(?<!`)`(?P<inline>[^`]+?<[^>]+>)`_{1,2}|(?<!`)`(?P<named>[^`]+)`_',re.S)
for m in pat.finditer(s):
    line=s[:m.start()].count('\n')+1
    role=m['role'] or 'inline' if m['inline'] else m['role'] or 'named'
    body=' '.join((m['rolebody'] or m['inline'] or m['named']).split())
    mt=re.fullmatch(r'(.*?)\s*<([^>]+)>',body)
    label,target=(mt[1].strip(),mt[2].strip()) if mt else (body,body)
    if role=='named': target=refs.get(target.lower(),target)
    if target.endswith('_'):target=refs.get(target[:-1].lower(),target)
    url='';resolution='unresolved_role'
    if target.startswith(('https://','http://')):url=target;resolution='literal_or_fixed_named_reference'
    elif role=='pypi':url='https://pypi.org/project/'+target;resolution='sphinx-issues6.0.0_pypi_role_L148'
    elif role=='gh':url='https://github.com/'+target;resolution='pinned_conf_extlinks'
    nearest=next((h for h in reversed(headings) if h['level']==2 and h['line']<line<=h['end']),None)
    upstream=nearest['title'] if nearest else ''
    if role in ['ref','term','pep']: upstream=target if role!='pep' else 'Python PEP '+target
    if label=='AWS S3':upstream='AWS S3'
    if label.lower()=='auditwheel':upstream='auditwheel'
    if label=='safety':upstream='Safety'
    if label=='Pipfile':upstream='Pipfile'
    if 'classifiers/' in url:upstream='PyPI classifiers'
    if label=='pypi.org':upstream='Warehouse'
    exclusion=''
    if 'discord.com/' in url:exclusion='account/community invitation, not information document'
    if 'github.com/Carreau' in url:exclusion='individual profile'
    if 'tidelift.com/lifter' in url:exclusion='funding/profile interface'
    tokens.append({'line':line,'label':label,'raw_target':target,'role':role,'exact_url':url,'resolution':resolution,'upstream':upstream,'exclusion':exclusion})
for i,t in enumerate(tokens,1):t['global_raw_rank']=i
(C/'catalog-token-audit.json').write_text(json.dumps(tokens,ensure_ascii=False,indent=2)+'\n')

def grp(pool,method):
    out=[];lookup={}
    for i,t in enumerate(pool,1):
        key=t['exact_url'] or f'unresolved:{i}' if method=='A' else t['upstream'] or f'unknown:{i}' if method=='B' else f'singleton_unknown_product_version:{i}'
        if key not in lookup:
            lookup[key]=len(out);out.append({'key':key,'representative':i,'members':[]})
        out[lookup[key]]['members'].append(i)
    return out

scans=[]
for pos,h in enumerate(headings[:20],1):
    all_links=[t for t in tokens if h['line']<t['line']<=h['end']]
    links=[t for t in all_links if not t['exclusion']]
    pool=links[:6];b=grp(pool,'B');a=grp(pool,'A');c=grp(pool,'C')
    a_reps=[x['representative'] for x in a[:3]];b_reps=[x['representative'] for x in b[:3]]
    exact=set(t['exact_url'] for t in links if t['exact_url'])
    opportunity=len(exact)>=4 and any(r>3 for r in b_reps) and any(len(x['members'])>1 and x['representative']<=3 for x in b[:3])
    scans.append({'row_id':h['id'],'scan_rank':pos,'heading':h['title'],'heading_kind':h['kind'],'start_line':h['line'],'end_line':h['end'],'catalog_url':BASE,'catalog_commit':SHA,'catalog_blob':blobs['source/key_projects.rst'],'information_links':len(links),'exact_distinct_urls':len(exact),'unresolved_link_count':sum(not t['exact_url'] for t in links),'excluded_links':len(all_links)-len(links),'first6_lines':';'.join(str(t['line']) for t in pool),'first6_exact_urls':json.dumps([t['exact_url'] for t in pool]),'first6_raw_targets':json.dumps([t['raw_target'] for t in pool]),'first6_upstreams':json.dumps([t['upstream'] for t in pool]),'A_first3':json.dumps(a_reps),'B_first3':json.dumps(b_reps),'B_early_promotion_opportunity':opportunity,'C_collision':False,'product_version_missing':True,'screening':'P-S1 selected' if pos==1 else 'C fail: product version absent; section1 already selected for B','unread_destination':True})

def csvwrite(name,rows):
    with (P/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
csvwrite('section-scan.csv',scans)
pool=[t for t in tokens if headings[0]['line']<t['line']<=headings[0]['end'] and not t['exclusion']][:6]
desc_lines={1:(26,31),2:(26,31),3:(26,31),4:(26,31),5:(31,31),6:(44,45)}
public_use={1:'PyPI mirror',2:'PyPI mirror',3:'PyPI mirror',4:'PyPI mirror',5:'serve files',6:'Python package builder'}
rows=[]
for rank,t in enumerate(pool,1):
    lo,hi=desc_lines[rank];description='\n'.join(lines[lo-1:hi])
    rows.append({'row_id':f'P-S1-U{rank}','slot_id':'P-S1','section_id':'PY-H01','heading':'PyPA Projects','heading_kind':'organizational','catalog_url':BASE,'catalog_commit':SHA,'catalog_blob':blobs['source/key_projects.rst'],'original_rank':rank,'global_raw_rank':t['global_raw_rank'],'source_line':t['line'],'display_name':t['label'],'description_source_lines':f'{lo}-{hi}','description_characters':len(description),'description_sha256':hashlib.sha256(description.encode()).hexdigest(),'raw_target':t['raw_target'],'exact_url':t['exact_url'],'resolution':t['resolution'],'upstream':t['upstream'],'component':t['upstream'],'public_use':public_use[rank],'product_version':'','document_role':'','missing_fields':'product_version;document_role'+(';exact_url' if not t['exact_url'] else ''),'purpose_id':'','purpose_linkage':'unmatched frozen requirements; none requests PyPI mirroring or cloud serving','metadata_exposed':True,'destination_opened':False})
csvwrite('pools.csv',rows)
groups=[]
for slot in ['P-N1','P-N2','P-S1','P-S2']:
    for method in ['A','B','C']:
        gs=grp(pool,method) if slot=='P-S1' else []
        reps=[g['representative'] for g in gs[:3]]
        hidden=[m for g in gs[:3] for m in g['members'][1:]]
        cut=[m for g in gs[3:] for m in g['members']]
        groups.append({'row_id':f'{slot}-{method}','slot_id':slot,'method':method,'representative_ranks':json.dumps(reps),'hidden_sibling_ranks':json.dumps(hidden),'cut_group_ranks':json.dumps(cut),'all_groups':json.dumps(gs,ensure_ascii=False),'status':'metadata opportunity; purpose unlinked' if slot=='P-S1' else 'observed no matching heading' if slot.startswith('P-N') else 'observed no strict C collision in 20 headings','missing':'rank6 exact URL unresolved; product versions missing; no independent purpose' if slot=='P-S1' else 'none for heading matching; destinations not applicable' if slot.startswith('P-N') else 'product versions absent; no selected section','natural_or_supplemental':'natural' if slot.startswith('P-N') else 'supplemental'})
csvwrite('groups.csv',groups)
csvwrite('link-exclusions.csv',[{'line':t['line'],'raw_target':t['raw_target'],'reason':t['exclusion']} for t in tokens if t['exclusion']])

utc=datetime.now(timezone.utc).isoformat()
source_specs=[
('PY-LIST','source/key_projects.rst','key_projects.rst','official_catalog','official_list_rule','L5-14; L13-370 scan','프로젝트별 설명과 정보 링크를 묶은 공식 목록; 조직 범주와 프로젝트 제목의 원순서를 확인','목록은 제품판을 제공하지 않는다. 본문 Issues 링크도 정보 링크로 포함한다.'),
('PY-RULE','source/contribute.rst','contribute.rst','official_authoring_rules','official_list_rule','Documentation types; Style guide/Scope; Headings','공식 가이드는 완전 목록을 목표로 하지 않으며 개별 제품 문서를 대체하지 않는다; 작업 목표 중심 제목과 교차링크 원칙을 제시','이 편집 규칙은 목록 후보 순위의 품질이나 요구 충족을 보장하지 않는다.'),
('PY-INDEX','source/index.rst','catalog-index.rst','official_routing','routing_metadata','L13-22,L88-94','index가 key_projects를 프로젝트 목록으로 명시하여 주목록 선택에 사용','앞선 overview는 선택 안내이며 별도 목록을 주분석으로 바꾸지 않았다.'),
('PY-OVERVIEW','source/overview.rst','overview.rst','official_scope_discussion','context_not_quota','document introduction and Editing notes','대상 환경과 사용자에 따라 배포 방식을 선택하는 결정 안내; 카탈로그와 문서 역할이 다름','주목록 표본으로 교체하지 않았으며 여기에 소개된 대안을 자연 적중에 넣지 않음.'),
('PY-CONF','source/conf.py','conf.py.txt','declarative_link_configuration','catalog_dependency','intersphinx_mapping and extlinks','build/distlib/packaging/pipenv의 inventory base 및 gh 역할 매핑 확인','base만으로 개별 index URI를 추정하지 않음; inventory GET 모두403.'),
('PY-DEPS','requirements.txt','catalog-requirements.txt','build_dependency_pin','catalog_dependency','L2,L6','Sphinx9.2.0 및 sphinx-issues6.0.0 고정으로 PyPI 역할 구현판 식별','이 버전들은 목록 생성 도구의 판이며 후보 제품판이 아님.')]
sources=[];receipts=[]
for sid,path,cachefile,typ,allocation,locator,finding,lim in source_specs:
    text=(C/cachefile).read_text()
    row={'id':sid,'question_ids':['Q2','Q3'],'publisher':'PyPA','work_id':'pypa/packaging.python.org:'+path,'type':typ,'allocation':allocation,'url':f'https://github.com/pypa/packaging.python.org/blob/{SHA}/{path}','checked_utc':utc,'version':SHA,'sha':blobs.get(path,''),'locator':locator,'finding':finding,'limitations':lim,'stance':'support','duplicate_of':None,'directly_opened':True}
    sources.append(row);receipts.append({'id':sid,'url':row['url'],'checked_utc':utc,'commit':SHA,'commit_time':'2026-11-18T11:35:18Z','blob':row['sha'],'sha256_local_text':hashlib.sha256(text.encode()).hexdigest(),'line_count':len(text.splitlines())})
sources.append({'id':'PY-PYPI-ROLE','question_ids':['Q2'],'publisher':'sphinx-issues author','work_id':'sloria/sphinx-issues:src/sphinx_issues/__init__.py','type':'declarative_link_implementation','allocation':'catalog_dependency','url':'https://github.com/sloria/sphinx-issues/blob/6.0.0/src/sphinx_issues/__init__.py','checked_utc':utc,'version':'6.0.0','sha':'e76dbbd5d86465a92e4d1e8cf31fcfa4254ab9be','locator':'L134-151,L350','finding':'PyPI role target is https://pypi.org/project/ plus package name, without trailing slash','limitations':'Only link-generation code read; no candidate product body; no execution','stance':'support','duplicate_of':None,'directly_opened':True})
for inv in json.loads((P/'inventory-resolution.json').read_text()):
    sources.append({'id':inv['id'],'question_ids':['Q2'],'publisher':inv['id'].removeprefix('PY-INV-'),'work_id':inv['url'],'type':'failed_inventory_resolution','allocation':'failure_not_counted','url':inv['url'],'checked_utc':inv['utc'],'version':None,'sha':None,'locator':'GET objects.inv','finding':'No metadata body obtained','limitations':inv.get('error',''),'stance':'unconfirmed','duplicate_of':None,'directly_opened':False,'minimum_to_change_answer':'public inventory index record with checksum or pinned generated URI'})
(P/'catalog-sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
(P/'catalog-receipts.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in receipts))
print(json.dumps({'first20':len(scans),'P-S1':[x['raw_target'] for x in pool],'A':[g['representative'] for g in grp(pool,'A')[:3]],'B':[g['representative'] for g in grp(pool,'B')[:3]],'C':[g['representative'] for g in grp(pool,'C')[:3]],'S1_exact_urls':len(set(x['exact_url'] for x in pool if x['exact_url'])),'first_project_only':scans[1]},ensure_ascii=False))
