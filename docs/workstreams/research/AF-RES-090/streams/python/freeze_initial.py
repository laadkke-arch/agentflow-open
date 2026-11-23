import json,re,html,hashlib,sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin
sys.path.insert(0,str(Path(__file__).parents[2]/'tools'))
from http_evidence import now,save_excerpt
R=Path(__file__).parent;E=R/'evidence'
if (R/'freeze.json').exists():
 raise SystemExit('Existing candidate freeze must not be overwritten. Preserve it and record a new, explicitly versioned observation instead.')
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.events=[]
 def handle_starttag(self,tag,attrs):self.events.append({'line':self.getpos()[0],'tag':tag,**dict(attrs)})
def body(sid):return (E/'raw'/(sid+'.bin')).read_text()
def receipt(sid):return json.loads((E/(sid+'.receipt.json')).read_text())
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def parse(s):
 p=Parser();p.feed(s);return p.events
def section(s,anchor):
 m=re.search(r'<h(?P<level>[1-6])[^>]*\bid="'+re.escape(anchor)+r'"[^>]*>.*?(?=<h(?P=level)\b|$)',s,re.S)
 return m.group(0) if m else ''
def compact(s):return ' '.join(html.unescape(re.sub('<[^>]+>',' ',s)).split())

stamp=now()
p1=body('PY-P1-CONFIG-SOURCE');example=p1.split('### Minmal\n',1)[1].split('### Alternative Download Source',1)[0]
code=re.search(r'```ini\n(.*?)```',example,re.S).group(1)
root=body('PY-P1-START-A');ev=parse(root)
starts={
 'P3':{'A':'https://cibuildwheel.pypa.io/en/stable/options/#enable','B':'https://cibuildwheel.pypa.io/en/v3.3.0/options/#enable'},
 'P1':{'A':'https://bandersnatch.readthedocs.io/en/latest/','B':'https://bandersnatch.readthedocs.io/en/7.0.1/'}}
targets=[
 {'purpose_id':'P3-body','case_id':'P3','purpose_kind':'body','reader':'3.3.0의 free-threading 설정을 인용하는 독자','target_version':'3.3.0','target_section':'enable','source_ids':['PY-P3-README','PY-P3-OPTIONS-SOURCE','PY-P3-START-B'],'publisher_promise':'고정 README는 CPython 3.13 free-threading opt-in 설명에 stable/options/#enable을 연결한다. 영구 고정판 보존 약속은 없음.','research_condition':'3.3.0의 enable 본문·값을 지금 식별','starts':starts['P3'],'sealed_next_resource':None,'anchor':'enable','success_criterion':'지정판 메타데이터와 cpython-freethreading 3.13 / 3.14+ 차이를 실제 본문에서 확인','unconfirmed':'영구보존·실행성은 조사하지 않음'},
 {'purpose_id':'P3-next','case_id':'P3','purpose_kind':'next','reader':'Python2 등 현행 미지원 Python용 구계열 안내가 필요한 독자','target_version':'1.x (3.3.0과 별도 목적판)','target_section':'1.x root 지원 Python 표','source_ids':['PY-P3-README'],'publisher_promise':'고정 README L53은 unsupported Python/Python2 독자에게 1.x 문서를 명시한다.','research_condition':'options 시작점에서 최대2문서 열람으로 1.x 지원표에 도착하는지','starts':starts['P3'],'sealed_next_resource':'https://cibuildwheel.pypa.io/en/1.x/','anchor':None,'raw_uri':'https://cibuildwheel.pypa.io/en/1.x/','explicit_link_in_entry_static_html':False,'candidate_second_views':{'A':'https://cibuildwheel.pypa.io/en/stable/','B':'https://cibuildwheel.pypa.io/en/v3.3.0/'},'candidate_link':'Home href=".."; 1.x는 options의 정적 링크에 없음. 동적 widget는 주작성자 별도 관측.','success_criterion':'1.x 표 실제 payload와 목적판 확인. 3.3.0과 같은 릴리스로 채점하지 않음','unconfirmed':'동적 버전 선택기의 현재 링크 형태는 별도 브라우저 증거 필요'},
 {'purpose_id':'P1-body','case_id':'P1','purpose_kind':'body','reader':'bandersnatch 7.0.1 첫 설정 예제를 읽는 독자','target_version':'7.0.1','target_section':'Mirror Configuration / Examples / Minmal (원문 철자)','source_ids':['PY-P1-README','PY-P1-INDEX-SOURCE','PY-P1-CONFIG-SOURCE'],'publisher_promise':'7.0.1 README는 latest 문서로 연결. named7.0.1 보존 약속은 발견되지 않음.','research_condition':'첫 설정 예제 = docs/mirror_configuration.md L13–39; index.rst의 CLI synopsis는 설정 예제 아님','starts':starts['P1'],'sealed_next_resource':None,'anchor':'minmal','example_code_sha256':sha(code),'example_values':{'directory':'/srv/pypi','master':'https://pypi.org','workers':'3','timeout':'15','global-timeout':'18000','stop-on-error':'false'},'candidate_second_views':{'A':'https://bandersnatch.readthedocs.io/en/latest/mirror_configuration.html#minmal','B':None},'success_criterion':'7.0.1 판과 첫설정 본문을 같이 확인. 최신판에서 동일 예제만 발견하면 판 일치로 승격하지 않음','unconfirmed':'named 시작404이면 target본문에 독자도달 실패'},
 {'purpose_id':'P1-next','case_id':'P1','purpose_kind':'next','reader':'첫 설정 예제에서 지목한 최초 동작관련 원URI를 확인할 독자','target_version':'7.0.1 예제의 외부 upstream URI (endpoint자체는 unversioned)','target_section':'Minmal의 master 값','source_ids':['PY-P1-CONFIG-SOURCE'],'publisher_promise':'첫예제 L22 upstream 주석 아래 L23 master=https://pypi.org. 예제 실행/모든API 성공 약속은 아님.','research_condition':'첫 codeblock의 최초 URI를 선택. 뒤 filtering 링크로 교체하지 않음.','starts':starts['P1'],'sealed_next_resource':'https://pypi.org','raw_uri':'https://pypi.org','uri_source_line':23,'uri_role':'운영 upstream endpoint; 설정문서 링크 아님','clickable_in_source':False,'candidate_second_views':{'A':'https://bandersnatch.readthedocs.io/en/latest/mirror_configuration.html#minmal','B':None},'manual_reconstruction_required_if_followed':'문자 URI를 주소창에 복사해야 함; root→설정으로2회 소진 후이면3번째문서','excluded_candidates':[{'candidate':'[mirror filtering plugins][filter-plugins]','location':'첫 예제 뒤 L38','reason':'첫 codeblock의 upstream URI보다 뒤. Examples 공통도입 L11은 첫하위예제 L13~39 밖.'},{'candidate':'/srv/pypi','location':'L20','reason':'로컬 출력경로이며 열람 가능한 웹 URI가 아님'}],'success_criterion':'고정된 master URI의 실제 응답을2열람 안에 읽음. 응답의 package7.0.1 귀속은 따로 미확인/적용불가','unconfirmed':'URI가 존재해도 mirror API 전체·실행성·7.0.1 당시endpoint내용은 증명하지 않음'}]

entry=[]
for case in ['P3','P1']:
 for ab in ['A','B']:
  sid=f'PY-{case}-START-{ab}';s=body(sid);events=parse(s);r=receipt(sid)
  record={'case_id':case,'route':ab,'source_id':sid,'receipt_path':str(E/(sid+'.receipt.json')),'url':r['requested_url'],'status':r['status'],'title':html.unescape(re.search(r'<title>(.*?)</title>',s,re.S).group(1)),'html_sha256':r['sha256'],'base_elements':[x for x in events if x['tag']=='base'],'one_x_links':[x for x in events if '1.x' in x.get('href','')],'candidate_links':[x for x in events if x['tag']=='a' and (x.get('href')=='..' or x.get('href')=='mirror_configuration.html#minmal')],'rtd_meta':[x for x in events if x['tag']=='meta' and x.get('name','').startswith('readthedocs')]}
  if case=='P3':
   sec=section(s,'enable');record.update({'anchor_exists':bool(sec),'section_sha256':sha(sec),'section_values':{'cpython-freethreading':'cpython-freethreading' in sec,'pyodide-eol':'pyodide-eol' in sec,'pyodide-prerelease':'pyodide-prerelease' in sec},'section_text_excerpt':compact(sec)[:250]})
  entry.append(record)

freeze={'frozen_utc':stamp,'state':'ready_for_parent_commit_before_followup_requests','source_commit':'63fd63b352a9a8bdcc24791c9dbee952ee9a8abc (P3); 7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74 (P1)','targets':targets,'entry_documents':entry,'p1_selection_note':'Before any destination request and before freeze commit, selecting filtering_configuration was considered then rejected: task includes literal original operational URI. Parent and investigator fixed first URI master=https://pypi.org at L23. No earlier committed target was replaced. First example boundary L13–39.','prior_dependency':'AF-RES-086 result e6a79c3ac05b84ea1c7db313233df1717cade756: cards,claims,comparison,routes Python rows directly read; no build/history requests repeated.','post_freeze_rule':'Any change is additive with UTC and prior values; current records cannot count auxiliary reads as reader success.'}
(R/'targets.json').write_text(json.dumps(targets,ensure_ascii=False,indent=2)+'\n')
(R/'freeze.json').write_text(json.dumps(freeze,ensure_ascii=False,indent=2)+'\n')

defs={
 'PY-P3-README':('project_guidance','3.3.0 / 63fd63b352a9a8bdcc24791c9dbee952ee9a8abc','README.md L44,53; first release v3.3.0','3.13 opt-in은 stable/options, unsupported Python2에는1.x 링크를 명시. 예제pip핀은3.3.0.','See the cibuildwheel 1 documentation','고정 원문 링크는 이동 서비스 주소. 영구보존 약속 없음.',True),
 'PY-P3-START-A':('project_guidance','stable metadata; exact release not yet independently named','options/#enable','200의 enable에는 cpython-freethreading 항목이 없고 pyodide-eol이 있다. 목표3.3.0본문과 다름.','Enable building with extra categories of selectors present.','HTTP/HTML 직접관측. 브라우저JS/사람 독해시간 미측정.',True),
 'PY-P3-START-B':('project_guidance','v3.3.0','options/#enable','meta version v3.3.0과 enable의 CPython3.13 free-threading opt-in,3.14+기본포함. 한HTML본문만으로 이 구별을 읽을 수 있다.','Enable experimental free-threaded builds for CPython 3.13.','당시제공/실행성/전체자원 일치 미확인.',True),
 'PY-P3-OPTIONS-SOURCE':('project_guidance','3.3.0 / 63fd63b352a9a8bdcc24791c9dbee952ee9a8abc','docs/options.md enable','고정소스의 enable 값과 생성HTML을 대조. 옵션 예제는인라인TOML/YAML이며 추가파일 없이 읽음.','enable = ["cpython-freethreading"]','동일 저작의 생성HTML과 원소스; 보수적최소량에서는 생성HTML과 중복 제외.',False),
 'PY-P1-README':('project_guidance','7.0.1 / 7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74','README.md Documentation,Quickstart','문서 링크latest. Quickstart는초기설정 파일생성·사용자수정을 지시하며 고정7.0.1문서 주소는 약속하지 않음.','Review `/etc/bandersnatch.conf` and adapt to your needs.','named7.0.1보존·현재응답 보장아님.',True),
 'PY-P1-TREE':('file_manifest','7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74','recursive Git tree','docs/mirror_configuration.md, docs/filtering_configuration.md와 index.rst의 blobSHA/경로를 확인.','', '파일목록은 실제 해당내용 열람/웹독자도달이 아님. 최소량에서 제외.',False),
 'PY-P1-START-A':('project_guidance','8.2.0; latest','title/nav; Contents→mirror_configuration.html#minmal','현재입구200. title/nav8.2.0. 본문CLI synopsis와목차는있고 첫설정예제는별도 mirror_configuration 링크.','bandersnatch 8.2.0 documentation','7.0.1목표판으로 식별할 수 없음. 200은지정판성공아님.',True),
 'PY-P1-START-B':('failed_target','named7.0.1','root','404 Project not found/Documentation page not found 응답.','', '현재404를과거미생성/영구손실로 해석하지 않음.',False),
 'PY-P1-CONFIG-SOURCE':('project_guidance','7.0.1 / 7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74','docs/mirror_configuration.md L13–39','첫 Minmal 예제값:directory=/srv/pypi, master=https://pypi.org,workers3,timeout15,global-timeout18000,stop-on-errorfalse. 최초원URI는master값.','master = https://pypi.org','고정source확인. 시작A/B의독자2열람성공은별도. example의 endpoint는unversioned.',True),
 'PY-P1-INDEX-SOURCE':('project_guidance','7.0.1 / 7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74','docs/index.rst L28–45','index는CLI synopsis를sphinx_argparse_cli로 생성하고 toctree에mirror_configuration을 연결. XMLRPC소개는현재latest의PEP691소개와다름.','Command line usage','설정본문이없으므로이를첫설정예제로대체하지않음.',True),
}
sources=[]
for sid,(category,version,location,observation,excerpt,limit,eligible) in defs.items():
 r=receipt(sid);case='P3' if '-P3-' in sid else 'P1';work='pypa/cibuildwheel documentation' if case=='P3' else 'pypa/bandersnatch documentation'
 row={'source_id':sid,'work_id':work,'lineage_id':work,'category':category,'original_url':r['requested_url'],'published_utc':'미확인; 고정commit/HTTP Last-Modified는 receipt에서 별도','retrieved_utc':r['retrieved_utc'],'version':version,'location':location,'questions':['Q1','Q2','Q3','Q4','Q6'],'cases':[case],'observation':observation,'excerpt':excerpt,'fingerprint':{'sha256':r['sha256'],'git_blob_sha1':r['git_blob_sha1'],'body_bytes':r['body_bytes'],'status':r['status'],'mime':r['content_type']},'support_refute':'supports limited claim; refutes HTTP200=>target version or fixed source=>reachable resource shortcuts','limitations':limit,'reread_url':r['requested_url'],'eligible':eligible,'receipt_path':str(E/(sid+'.receipt.json')),'excerpt_path':str(E/(sid+'.excerpt.json')),'counting_note':'동일파일재조회/미러는이행과중복산입하지않음'}
 sources.append(row);save_excerpt(E,sid,observation,[excerpt] if excerpt else [])
(R/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
print(json.dumps({'frozen_utc':stamp,'purposes':len(targets),'sources':len(sources),'eligible':sum(x['eligible'] for x in sources),'next_targets_not_requested':True},ensure_ascii=False))
