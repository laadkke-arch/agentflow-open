"""Apply pre-destination functional-section clarification to sealed v1 metadata."""
from pathlib import Path
import csv,json,re
P=Path(__file__).resolve().parent
def read(name):return list(csv.DictReader((P/name).open()))
def write(name,rows):
    with (P/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

v1p=read('pools.csv');v1g=read('groups.csv')
if len(v1p)!=6 or v1p[0]['section_id']!='PY-H01':
    raise SystemExit('Run only against preserved v1 worktree; v1 remote SHA cd940aa340a5396611d028002ffc7150981f853a')
diag=[]
for r in v1p:
    r=dict(r);r['slot_id']='D-P1';r['row_id']=r['row_id'].replace('P-S1','D-P1');diag.append(r)
write('diagnostic-pools.csv',diag)
diag=[]
for r in v1g:
    if r['slot_id']=='P-S1':
        r=dict(r);r['slot_id']='D-P1';r['row_id']=r['row_id'].replace('P-S1','D-P1');diag.append(r)
write('diagnostic-groups.csv',diag)

newp=[]
for r in v1p[:5]:
    r=dict(r);r['section_id']='PY-H02';r['heading']='bandersnatch';r['heading_kind']='functional_project';newp.append(r)
write('pools.csv',newp)
newg=[]
for r in v1g:
    r=dict(r)
    if r['slot_id']=='P-S1':
        gs=json.loads(r['all_groups']);gs=[g for g in gs if g['representative']<=5]
        for g in gs:g['members']=[x for x in g['members'] if x<=5]
        r['all_groups']=json.dumps(gs,ensure_ascii=False)
        r['representative_ranks']=json.dumps([g['representative'] for g in gs[:3]])
        r['hidden_sibling_ranks']=json.dumps([x for g in gs[:3] for x in g['members'][1:]])
        r['cut_group_ranks']=json.dumps([x for g in gs[3:] for x in g['members']])
        r['missing']='product versions/document roles absent; no independent user purpose; observed exhaustion at5'
    newg.append(r)
write('groups.csv',newg)

lines=(P/'cache/key_projects.rst').read_text().splitlines()
heads=[]
for i in range(1,len(lines)):
    if re.fullmatch(r'([=#])\1{1,}',lines[i]) and lines[i-1].strip() and not re.fullmatch(r'[=#]+',lines[i-1]):
        if lines[i-1]=='Project Summaries':continue
        heads.append({'heading':lines[i-1],'line':i,'level':1 if lines[i][0]=='#' else 2})
for i,h in enumerate(heads):h['end']=next((x['line']-1 for x in heads[i+1:] if x['level']<=h['level']),len(lines))
tokens=json.loads((P/'cache/catalog-token-audit.json').read_text())
uses={'bandersnatch':'PyPI package mirroring','build':'build Python distribution archives','cibuildwheel':'CI wheel builds across platforms','distlib':'packaging interoperability operations','distutils':'historical Python packaging system','flit':'create and upload Python distributions','hatch':'manage project environments and package builds','packaging':'parse and handle packaging metadata','pip':'find download and install packages','Pipenv':'manage environment and dependencies','pipx':'isolated command-line application installation','readme_renderer':'render and check package README markup','Setuptools':'build and distribute Python packages','trove-classifiers':'validate package classifier values','twine':'upload distributions and metadata','virtualenv':'create isolated Python environments','Warehouse':'serve Python Package Index','wheel':'build and handle wheel archives','buildout':'assemble and deploy multi-part applications','conda':'manage package dependency and environments'}
functional=0;scans=[]
for original,h in enumerate(heads,1):
    if functional>=20:break
    include=h['level']==2 and h['heading']!='Python Packaging User Guide'
    if include:functional+=1
    all_links=[t for t in tokens if h['line']<t['line']<=h['end']]
    links=[t for t in all_links if not t['exclusion']]
    exact={t['exact_url'] for t in links if t['exact_url']}
    pool=links[:6];seen=set();b=[]
    for rank,t in enumerate(pool,1):
        key=t['upstream'] or f'unknown{rank}'
        if key not in seen:seen.add(key);b.append(rank)
    scans.append({'row_id':f'PY-V2-H{original:02d}','original_heading_rank':original,'functional_rank':functional if include else '', 'heading':h['heading'],'heading_kind':'functional_project' if include else 'ownership_category' if h['level']==1 else 'self_navigation','included':include,'purpose_from_section_lead':uses.get(h['heading'],''),'source_start_line':h['line'],'source_end_line':h['end'],'information_link_count':len(links),'exact_distinct_urls':len(exact),'unresolved_count':sum(not t['exact_url'] for t in links),'first6_lines':json.dumps([t['line'] for t in pool]),'first6_urls':json.dumps([t['exact_url'] for t in pool]),'B_representatives':json.dumps(b[:3]),'B_early_promotion_opportunity':include and len(exact)>=4 and any(x>3 for x in b[:3]),'C_collision':False,'reason':'P-S1 selected; exactURL5; purpose unlinked' if functional==1 and include else 'C product_version missing' if include else 'not a processing purpose; excluded before destination opening','destination_opened':False})
write('functional-scan.csv',scans)
statuses=[]
for slot in ['P-N1','P-N2','P-S1','P-S2']:
    selected=slot=='P-S1';natural=slot.startswith('P-N')
    statuses.append({'row_id':slot+'-STATUS','slot_id':slot,'layer':'natural' if natural else 'supplemental','section':'bandersnatch' if selected else '', 'source_lines':'18-35' if selected else '', 'candidate_count':5 if selected else 0,'exact_url_count':5 if selected else 0,'observed_exhaustion':True if selected else '', 'purpose_id':'','selection_status':'selected metadata opportunity; purpose unmatched' if selected else 'no heading/alias match' if natural else 'no C collision among20 functional sections','missing':'no frozen user purpose; product versions and document roles' if selected else 'original issue revision unconfirmed' if natural else 'no product versions in catalog to satisfy strict C','counterfactual_fourth':'rank4 same bandersnatch, not independent implementation' if selected else '', 'promotion_rank':'5 AWS S3' if selected else '', 'raw_pool_complete_implementations':'unconfirmed purpose not linked' if selected else 'not applicable; no selected pool','v1_reference':'cd940aa340a5396611d028002ffc7150981f853a'})
write('slot-status.csv',statuses)
print('v2 primary P-S1=bandersnatch five URLs; A/C1,2,3 B1,5;20 functional scanned;3 excluded headings; no destination read')
