import json,re,html,hashlib,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[2]/'tools'))
from http_evidence import now,save_excerpt
R=Path(__file__).parent;E=R/'evidence'
def body(sid):return (E/'raw'/(sid+'.bin')).read_text()
def rec(sid):return json.loads((E/(sid+'.receipt.json')).read_text())
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def plain(s):return html.unescape(re.sub('<[^>]*>','',s))
def compact(s):return ' '.join(plain(s).split())
def title(s):return html.unescape(re.search(r'<title>(.*?)</title>',s,re.S).group(1))
def add_source(sid,category,version,location,observation,limit,eligible,duplicate=None,excerpt=''):
 r=rec(sid);case='P3' if '-P3-' in sid else 'P1';work=('pypa/cibuildwheel documentation' if case=='P3' else 'pypa/bandersnatch documentation')
 if sid=='PY-P1-UPSTREAM':work='Python Package Index public service'
 row={'source_id':sid,'work_id':work,'lineage_id':work,'category':category,'original_url':r['requested_url'],'published_utc':'미확인; HTTP Last-Modified/태그시각은 receipt에서 별도','retrieved_utc':r['retrieved_utc'],'version':version,'location':location,'questions':['Q2','Q3','Q4','Q5','Q6'],'cases':[case],'observation':observation,'excerpt':excerpt,'fingerprint':{'sha256':r['sha256'],'git_blob_sha1':r['git_blob_sha1'],'body_bytes':r['body_bytes'],'status':r['status'],'mime':r['content_type']},'support_refute':'지정한 범위만 지지; 본문보존/같은내용/2회도달/같은판/실행성의 자동등치를 반박','limitations':limit,'reread_url':r['requested_url'],'eligible':eligible,'receipt_path':str(E/(sid+'.receipt.json')),'excerpt_path':str(E/(sid+'.excerpt.json')),'duplicate_of':duplicate,'counting_note':'같은 파일 재요청은 한 번만 산입; source/HTML이 같은 저작인 경우 계보 유지'}
 save_excerpt(E,sid,observation,[excerpt] if excerpt else []);return row

rows=json.loads((R/'traversals.raw.json').read_text())
fixed=re.search(r'### Minmal.*?```ini\n(.*?)```',body('PY-P1-CONFIG-SOURCE'),re.S).group(1)
current_section=re.search(r'<section id="minmal">(.*?)(?=<section|$)',body('PY-READ-P1-body-A-2'),re.S).group(1)
current_code=plain(re.search(r'<pre>(.*?)</pre>',current_section,re.S).group(1))
samecode=fixed==current_code
root_table=re.findall(r'<table[^>]*>.*?</table>',body('PY-P3-LEGACY-ROOT'),re.S)[0]
option_table=re.findall(r'<table[^>]*>.*?</table>',body('PY-READ-P3-next-A-2'),re.S)[0]
comparison={'recorded_utc':now(),'p1_first_config':{'fixed_source':'PY-P1-CONFIG-SOURCE','current_source':'PY-READ-P1-body-A-2','method':'Extract Markdown first ini fence under Minmal; extract generated HTML Minmal pre text by stripping tags and decoding HTML entities. No whitespace normalization.','source_version':'7.0.1','served_version':'8.2.0','equal_extracted_text':samecode,'source_chars':len(fixed),'served_chars':len(current_code),'source_text_sha256':sha(fixed),'served_text_sha256':sha(current_code),'whole_documents_equal':False,'implication':'같은예제만으로판을식별하면실패; 본문예제충분성은긍정대조.'},'p3_legacy_tables':{'target_source':'PY-P3-LEGACY-ROOT','reader_destination':'PY-READ-P3-next-A-2','target_anchor':'what-does-it-do','reader_anchor':'build-skip','target_raw_table_sha256':sha(root_table),'reader_raw_table_sha256':sha(option_table),'same_table':root_table==option_table,'target_has_cp27':bool(re.search(r'CPython.{0,10}2\.7',plain(root_table))),'reader_has_cp27_identifiers':'cp27-manylinux_x86_64' in option_table,'reader_has_pp27_identifiers':'pp27-manylinux_x86_64' in option_table,'target_header_columns':9,'reader_group_columns':4,'implication':'정확한봉인root지원표는미도달. 그러나2회도착options의다른표로Python2.7/PyPy2.7지원identifier를읽을수있음. 사후대체성공으로세지않음.'}}
(E/'comparison.json').write_text(json.dumps(comparison,ensure_ascii=False,indent=2)+'\n')

for r in rows:
 p=r['purpose_id'];a=r['route'];first=r['views'][0];last=r['views'][-1];s=body(last['source_id']);r['final_url']=last['final_url'];r['final_title']=title(s);r['source_ids']=[v['source_id'] for v in r['views']];r['static_or_rendered']='HTML response read with DOM/text; parent browser verifies clickable UI paths';r['first_target_body_status']='confirmed' if p.startswith('P3') and a=='B' else ('inaccessible' if a=='B' else 'refuted')
 if p=='P3-body':
  r.update(target_body='confirmed',followup_resource='not_applicable',same_version='confirmed',outcome='target_body_confirmed',last_version='v3.3.0',primary_section_present=True,resource_success=True,reader_purpose_success=True,strict_target_reached=True,observations='A 첫화면stable본문은지정3.3.0과다름. A는동적메뉴v3.3.0으로2회째회복; B는1회. 최종enable에cpython-freethreading과3.13/3.14+구별.',version_evidence=['PY-P3-TAG','PY-P3-TAG-OBJECT','PY-P3-OPTIONS-SOURCE',last['source_id']],limitations='메뉴조작은추가문서0. HTML본문확인이지예제실행/영구불변증명이아님.')
 elif p=='P3-next':
  r.update(target_body='confirmed' if a=='B' else 'refuted',followup_resource='unconfirmed',same_version='confirmed',outcome='budget_exhausted_exact_target_not_reached',last_version='1.x',primary_section_present=a=='B',resource_success=False,reader_purpose_success=False,strict_target_reached=False,alternative_information_confirmed=True,observations='2회째1.x/options로도착. 봉인된root what-does-it-do지원표는없고Home링크뒤3회째에있음. 현재본문build-skip에는다른지원identifier표가있어cp27/pp27정보자체는읽힘.',version_relation='Publisher-declared legacy series; 1.x is not the same release as 3.3.0. same_version=destination is intended legacy-series version, not identical release.',version_evidence=['PY-P3-README',last['source_id'],'PY-P3-LEGACY-ROOT'],limitations='정확한표미도달을자원부재/접근불가로읽지않음. 별도root GET은연구예산. root표대신options표를사후성공판정에쓰지않음.')
 elif p=='P1-body' and a=='A':
  r.update(target_body='refuted',followup_resource='not_applicable',same_version='refuted',outcome='wrong_version_same_example',last_version='8.2.0',primary_section_present=True,resource_success=False,reader_purpose_success=False,strict_target_reached=False,example_text_equal_fixed_source=samecode,observations='latest root→mirror_configuration#minmal2회. title/nav8.2.0. 첫Minmal예제395문자는고정7.0.1원문에서추출한것과동일하지만목표판은아님.',version_evidence=['PY-P1-TAG','PY-P1-CONFIG-SOURCE',last['source_id']],limitations='예제동일성은파일전체동일성/7.0.1서비스판보증아님. 좁은예제읽기에는유용한반례.')
 elif p=='P1-next' and a=='A':
  r.update(target_body='refuted',followup_resource='unconfirmed',same_version='unconfirmed',outcome='budget_exhausted_literal_uri_not_followed',last_version='8.2.0',primary_section_present=True,resource_success=False,reader_purpose_success=False,strict_target_reached=False,first_literal_uri='https://pypi.org',selected_resource_clickable=False,manual_reconstruction_required=True,observations='2회째Minmal에master=https://pypi.org가span문자로있고href없음. 해당URI를주소창으로옮길3회째예산이없어독자는미열람. 별도조사는PyPI홈200을확인.',version_evidence=['PY-P1-TAG','PY-P1-CONFIG-SOURCE',last['source_id'],'PY-P1-UPSTREAM'],limitations='endpoint는unversioned. current홈의정적열람은7.0.1설정/API동작성공이아님. filter문서로목표교체안함.')
 else:
  r.update(target_body='inaccessible',followup_resource='not_applicable' if p=='P1-body' else 'inaccessible',same_version='unconfirmed',outcome='entry_404',last_version='unconfirmed',primary_section_present=False,resource_success=False,reader_purpose_success=False,strict_target_reached=False,observations='정확한named7.0.1 root가404. 후속본문/자원에도달하지못하고1회에서종료. 고정source비교는주경로밖.',version_evidence=['PY-P1-TAG','PY-P1-CONFIG-SOURCE'],limitations='현재정확한경로의실패; 과거미생성/영구손실/모든7.0.1파일부재아님.')
 r['response_bytes']=r['total_response_body_bytes'];r['actual_link_sequence']=[v['requested_url'] for v in r['views']];r['manual_reconstruction']=False
 save_excerpt(E,last['source_id'],r['observations'])
(R/'traversals.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')

sources=[json.loads(l) for l in (R/'sources.jsonl').read_text().splitlines()]
sources=[x for x in sources if not x['source_id'].startswith('PY-READ-') and x['source_id'] not in ['PY-P3-LEGACY-ROOT','PY-P1-UPSTREAM','PY-P1-FILTER-SOURCE','PY-P1-EXAMPLE-CONF','PY-P1-TAG','PY-P3-TAG','PY-P3-TAG-OBJECT']]
seen={x['fingerprint']['sha256']:x['source_id'] for x in sources if x['eligible']}
for r in rows:
 for v in r['views']:
  sid=v['source_id'];rr=rec(sid);duplicate=seen.get(rr['sha256']);eligible=rr['status']==200 and not duplicate
  cat='referenced_file' if 'P3-next-' in sid and sid.endswith('-2') else 'project_guidance'
  if rr['status']!=200:cat='failed_target';eligible=False
  obs=r['observations'] if v is r['views'][-1] else '해당판독의독립첫GET. 실제선행/현재수집과같은HTML인지해시로대조. 최종판정은traversals행.'
  if eligible:seen[rr['sha256']]=sid
  sources.append(add_source(sid,cat,r['last_version'] if v is r['views'][-1] else ('v3.3.0' if r['case_id']=='P3' and r['route']=='B' else 'stable/latest/named entry; see title'),'actual reader route '+r['traversal_id']+' view '+str(v['view']),obs,'실제독립응답. 반복원문은적격개수에서제외. '+r['limitations'],eligible,duplicate))

defs=[
 ('PY-P3-LEGACY-ROOT','referenced_file','1.x','what-does-it-do table','별도보조로고정목표root를직접200읽음. CPython2.7,PyPy2.7v7.3.3을포함한OS지원matrix.1.x/options의identifier표와다른표.','주독자경로에는추가되지않음.4개Python행중next2개를성공으로올리지않음.',True,'CPython 2.7; PyPy 2.7 v7.3.3'),
 ('PY-P1-UPSTREAM','referenced_file','unversioned current service','PyPI homepage','고정Minmal의첫원URI를연구예산에서수동요청.200,text/html,PyPI검색/패키지색인홈을받음.','주경로2회에는못열었다.동적서비스의현재홈은bandersnatch7.0.1판이나mirroring/API실행성공을입증하지않음.',True,'PyPI · The Python Package Index'),
 ('PY-P1-FILTER-SOURCE','referenced_file','7.0.1 / 7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74','docs/filtering_configuration.md / Plugins Enabling','선택되지않은후행설정문서후보를고정commit에서실제읽음.플러그인명시활성화와allowlist/blocklist설정예제.','고정Git트리에있고내용을읽었지만P1-next첫URI대체가아님.원래독자2회도달성공아님.',True,'[plugins] enabled = all'),
 ('PY-P1-EXAMPLE-CONF','referenced_file','7.0.1 / 7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74','src/bandersnatch/example.conf','고정설정문서말미literalinclude가참조하는실제다른파일을읽음. master pypi.org,timeout10,global-timeout1800,workers3. 최소예제timeout15/global18000과값이다름.','별도예제이므로최초Minmal목표를교체하지않음.파일보존과실행성공은별개.',True,'timeout = 10; global-timeout = 1800'),
 ('PY-P1-TAG','version_manifest','7.0.1','refs/tags/7.0.1','발행자Git ref가7.0.1을commit7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74로직접가리킴.','태그는내용판연결이지현재rendered7.0.1서비스가있다는증거가아님.최소량제외.',False,''),
 ('PY-P3-TAG','version_manifest','v3.3.0','refs/tags/v3.3.0','발행자annotated tag object45616d2b12f67573cd48b844c047f8cda2809f43를지목.','이ref만으로sourcecommit이라고표시하지않고tagobject별도읽음.최소량제외.',False,''),
 ('PY-P3-TAG-OBJECT','version_manifest','v3.3.0','tag object45616d2b12f67573cd48b844c047f8cda2809f43','v3.3.0태그object는sourcecommit63fd63b352a9a8bdcc24791c9dbee952ee9a8abc를지목. 태그시각2025-11-12T19:27:52Z.','고정소스연결.그때서비스제공/빌드귀속은조사범위밖.최소량제외.',False,''),
]
for sid,cat,version,loc,obs,lim,eligible,excerpt in defs:sources.append(add_source(sid,cat,version,loc,obs,lim,eligible,None,excerpt))
(R/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))

assets=[]
specs=[('AS-PY-P3-BODY','PY-P3-START-B','options/index.html','enable',True,False,'served version v3.3.0; corroborated fixed source/tag'),('AS-PY-P3-ROOT','PY-P3-LEGACY-ROOT','index.html','what-does-it-do',False,False,'auxiliary target 1.x; not reader two-view destination'),('AS-PY-P3-OPTIONS','PY-READ-P3-next-A-2','options/index.html','build-skip',True,False,'legacy version1.x but different table from sealed target'),('AS-PY-P1-CONFIG','PY-P1-CONFIG-SOURCE','docs/mirror_configuration.md','Minmal L13–39',False,False,'fixed7.0.1 source compared with current8.2.0 code;395char identical'),('AS-PY-P1-UPSTREAM','PY-P1-UPSTREAM','/','homepage',False,True,'unversioned URI; manual auxiliary access; no7.0.1resourceversion'),('AS-PY-P1-FILTER','PY-P1-FILTER-SOURCE','docs/filtering_configuration.md','Plugins Enabling',False,True,'same sourcecommit file; not selected firstURI'),('AS-PY-P1-EXAMPLE','PY-P1-EXAMPLE-CONF','src/bandersnatch/example.conf','whole file',False,True,'same sourcecommit literalinclude target; auxiliary')]
tree={e['path']:e for e in json.loads(body('PY-P1-TREE'))['tree']}
for aid,sid,path,anchor,reader,manual,note in specs:
 rr=rec(sid);entry=tree.get(path) if 'P1' in aid else None
 assets.append({'asset_id':aid,'source_id':sid,'file':path,'anchor':anchor,'url':rr['requested_url'],'hosting_location':rr['final_url'],'retrieved_utc':rr['retrieved_utc'],'mime':rr['content_type'],'body_bytes':rr['body_bytes'],'sha256':rr['sha256'],'git_blob_sha1':rr['git_blob_sha1'],'publisher_git_blob_sha1':entry['sha'] if entry else None,'publisher_file_match':rr['git_blob_sha1']==entry['sha'] if entry else None,'directly_read':True,'reader_two_view_read':reader,'manual_reconstruction':manual,'inline':False,'js_executed':False,'example_executed':False,'note':note,'receipt_path':str(E/(sid+'.receipt.json'))})
(R/'assets.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in assets))

for f in E.glob('*.receipt.json'):
 d=json.loads(f.read_text());red=[]
 for k in list(d.get('headers',{})):
  if k.lower() in ['set-cookie','authorization','proxy-authorization']:
   d['headers'][k]='[omitted: response credential/cookie not research evidence]';red.append(k)
 if red:d['redacted_headers']=red;f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

cost={'reader_traversals':len(rows),'paired_purposes':len(rows)//2,'reader_document_views':sum(r['view_count'] for r in rows),'reader_response_body_bytes':sum(r['response_bytes'] for r in rows),'all_recorded_http_requests':len(list(E.glob('*.receipt.json'))),'all_recorded_response_body_bytes':sum(json.loads(f.read_text())['body_bytes'] for f in E.glob('*.receipt.json')),'raw_entity_byte_measurement':'HTTP response content bytes excluding TLS/headers, no browser automaticsubresource sum','human_time':'미측정','sources_rows':len(sources),'eligible_unique_sources':sum(x['eligible'] for x in sources),'eligible_lineages':sorted(set(x['lineage_id'] for x in sources if x['eligible'])),'no_js_or_example_execution':True}
(R/'costs.json').write_text(json.dumps(cost,ensure_ascii=False,indent=2)+'\n');print(json.dumps(cost,ensure_ascii=False,indent=2))
