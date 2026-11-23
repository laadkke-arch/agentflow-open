import json,pathlib,csv,datetime,hashlib,subprocess,html,re
P=pathlib.Path(__file__).parent
D='1d399f630930d2763459e16509c5224b0cded9a0'
def gitjson(p):return json.loads(subprocess.check_output(['git','show',D+':docs/workstreams/research/AF-RES-096/'+p],text=True))
excluded=set(gitjson('evidence/intake/intake.json')['excluded_prior_question_ids'])|{x['question_id'] for x in gitjson('protocol.json')['cases']}
metadata=json.loads(P.joinpath('r0-metadata.json').read_text())
receipts={x['question_id']:x for x in json.loads(P.joinpath('selected-revision-receipts.json').read_text())}
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def span(body,start,end=None):
 a=body.index(start);b=a+len(start) if end is None else body.index(end,a)+len(end)
 return {'unit':'HTML body returned by frozen StackExchange revision; zero-based half-open Unicode characters and UTF-8 bytes','char_start':a,'char_end':b,'byte_start':len(body[:a].encode()),'byte_end':len(body[:b].encode())}
def condition(body,cid,requirement,start,end,kind='required'):
 return {'id':cid,'requirement':requirement,'role':kind,'r0_span':span(body,start,end)}
def common(x,cid,rank,stratum,adjacent,queries):
 b=P.joinpath('_cache',str(x['question_id'])+'.html').read_text();g=x['earliest_body_revision']['revision_guid']
 return {'case_id':cid,'question_id':x['question_id'],'tag':'pandoc','stratum':stratum,'original_rank':rank,'creation_utc':datetime.datetime.fromtimestamp(x['creation_date'],datetime.timezone.utc).isoformat(),'r0_url':'https://stackoverflow.com/revisions/'+g+'/view-source','r0_guid':g,'r0_api_url':receipts[x['question_id']]['url'],'r0_payload':'items[0].body','r0_body_sha256':x['body_sha256'],'r0_body_chars':len(b),'r0_body_bytes':len(b.encode()),'r0_cache_path':str(P/'_cache'/f"{x['question_id']}.html"),'r0_actual_version':1,'initial_creation_confirmed':x['initial_creation_confirmed'],'main_label':'PD','main_research_version':'3.6','adjacent_label':adjacent,'queries':queries,'query_origins':['original-body task/format wording','original-body boundary/error/configuration wording'],'source_id':'R0-'+cid,'checked_utc':now,'initial_tags':x['earliest_body_revision']['tags'],'recruitment_current_tags':x['tags'],'prior_id_excluded':x['question_id'] in excluded,'repost':'No explicit repost or same-question link in this R0; identity across external sites remains unverified.','independence':'Distinct question ID; original-person and original-problem-event independence unverified; no author metadata or later discussion opened.'}
selected=[]
x=metadata[0];b=P.joinpath('_cache',str(x['question_id'])+'.html').read_text();r=common(x,'P1',1,'boundary','KN',[['default','graphics','format','files','include_graphics'],['auto_pdf','pdf','svg','emf','output']]);r.update({
 'title_r0':html.unescape(x['earliest_body_revision']['title']),
 'main_tool_only_in_tag':True,'main_tool_absent_from_r0_tags':True,
 'input_summary':'R Markdown PowerPoint YAML와 knitr 설정·include_graphics 호출이 제시된다. 함수에는 external_figure.jpg라는 파일명만 전달한다. 실물 그래픽 파일이나 대체 파일은 없다.',
 'desired_output':'같은 이름의 여러 확장자 가운데 기본 선택을 PDF에 한정하지 않고 SVG 또는 EMF로 구성하여, 출력형식에 맞춘 vector/raster 전환을 쉽게 하고 싶다.',
 'conditions':[condition(b,'C1','include_graphics에 주어진 외부 파일의 기본 선택 형식을 구성하여 PDF 이외 SVG 또는 EMF를 기본으로 선택할 수 있어야 한다.','<p>Is there a way','</p>'),condition(b,'C2','제시한 R Markdown/PowerPoint 경계에서 해당 전역 선택 설정이 실제 함수 입력에 연결되는 근거가 있어야 한다. 파일마다 확장자를 수동 변경하는 예만으로 기본값 요구를 만족시키지 않는다.','<pre><code>---','</code></pre>')],
 'purpose_not_additional_requirement':'지원 형식에 따라 vector/raster를 쉽게 바꾸려는 목적은 명시됐으나 모든 출력형식의 자동 판별·fallback을 별도 필수 기능으로 추가하지 않는다.',
 'user_versions':{'pandoc':'R0 본문·최초 태그에 이름과 판 없음','knitr':'미제공','rmarkdown':'미제공','external_graphics':'JPEG filename only; SVG/EMF variants existence unknown'},
 'adjacency_evidence':'최초 본문 첫 명시 실행 라이브러리는 knitr이며 include_graphics가 외부 파일을 R Markdown 출력에 넣는 명시 경계다. Pandoc은 수집 당시 태그에만 있고 최초 태그에도 없다. Pandoc 연구판의 모집이라는 점은 약한 연결로 별도 표시한다.',
 'adjacency_spans':[span(b,"<code>knitr</code>","</p>"),span(b,"knitr::include_graphics('external_figure.jpg')")],
 'adjacent_candidates':[{'name':'knitr','role':'direct image selection/producer library','selected':True,'body_first_char':b.index('<code>knitr</code>')},{'name':'powerpoint_presentation','role':'named output declaration; library identity rmarkdown inferred, not an explicit independent first tool','selected':False,'body_first_char':b.index('powerpoint_presentation')}],
 'simple_relay':False,
 'missing':['실제 PNG/JPEG 및 SVG/EMF 파일','사용 knitr/R/Pandoc 판','기본 제공 option만 허용하는지 사용자 helper도 허용하는지'],
 'intent_interpretations':{'primary':'전역 설정 또는 한 번 등록한 helper가 파일 선택을 바꾸는 문서 근거를 허용하되, 각 호출에서 수동 확장자 변경만 하는 답은 불완결.','sensitivity':'knitr::include_graphics 자체의 내장 option만 허용하면 helper/외부 전처리는 미완결.','discriminating_observation':'질문자가 자체 helper 허용 여부를 확인하거나 같은 입력 호출로 SVG/EMF를 선택한 버전/출력 기록을 제시.'},
 'selection_reason':'current pandoc tag frame의 첫 boundary 요청. 실제 Rmd 입력과 기대 vector 선택이 있고 knitr 이름/함수가 직접 경계에 존재. 본문 main-tool 부재는 제외하지 않고 명시.'})
selected.append(r)
x=metadata[1];b=P.joinpath('_cache',str(x['question_id'])+'.html').read_text();r=common(x,'P2',2,'boundary','CE',[['convert','typst','markdown','imports','preview'],['pandoc','library','file','directory','cetz']]);r.update({
 'title_r0':html.unescape(x['earliest_body_revision']['title']),'main_tool_only_in_tag':False,'main_tool_absent_from_r0_tags':False,
 'input_summary':'test1.typ/relimport.typ는 로컬 a=123 import와 Markdown 결과를 포함한다. test2.typ는 같은 입력 앞에 @preview/cetz:0.3.4 import를 추가한다. Typst compile은 성공했다고 본문에서 보고하나 Pandoc은 패키지 경로를 파일로 열다 실패한다.',
 'desired_output':'원 test2.typ에서 외부 패키지를 import한 채 Pandoc이 성공 종료하고, test1.md와 같은 제목·본문·값123의 test2.md를 생성한다. 현재 예제는 CeTZ 그림을 그리지 않는다.',
 'conditions':[condition(b,'C1','명시된 @preview/cetz:0.3.4 라이브러리 import를 버리지 않고 제시한 test2.typ를 Pandoc으로 성공 변환할 근거가 있어야 한다.','<p>Now try importing a library','</code></pre>'),condition(b,'C2','상대 import의 a=123과 제목/본문을 보존해 test1.md와 동일한 test2.md를 생성해야 한다.','<p>Expected behavior:','</ul>')],
 'user_versions':{'pandoc':'3.1.3','typst':'0.13.1 (unknown hash)','cetz':'0.3.4','showman':'미제공'},
 'adjacency_evidence':'선택은 첫 직접 import 라이브러리 CeTZ. 앞선 Typst라는 말은 입력 언어/형식이고, 후반 typst compile은 별도 검증 실행으로 Pandoc과 직렬 경계를 이루지 않는다. Showman은 후반에 설명한 wrapper/최종 README 목적이며 실패한 재현 명령은 Pandoc 단독이다. CeTZ는 바로 읽어야 하는 명시 입력 의존이다.',
 'adjacency_spans':[span(b,'#import &quot;@preview/cetz:0.3.4&quot;: *'),span(b,'<p>My overall objective','</p>'),span(b,"<p>Check it's valid Typst:",'</code></pre>')],
 'adjacent_candidates':[{'name':'CeTZ','role':'first explicit imported external library; direct reader input dependency','selected':True,'body_first_char':b.index('@preview/cetz:0.3.4')},{'name':'showman','role':'wrapper/overall goal; absent from failing minimal command','selected':False,'body_first_char':b.index('showman')},{'name':'typst compile','role':'parallel validation of same source, not producer of Pandoc input','selected':False,'body_first_char':b.index('typst compile')}],
 'simple_relay':False,'missing':['사용한 Showman 및 새 패키지 전체 입력','실제로 내려받은 CeTZ 전체 패키지 hash','사용판3.1.3와 연구판3.6의 동일성은 미확인'],
 'intent_interpretations':{'primary':'제시된 외부 import와 의미를 보존하여 Pandoc 변환 경로를 설명해야 한다. import 제거·더미 빈 모듈로의 대체는 완결로 세지 않는다.','sensitivity':'로컬 vendoring과 import 경로 치환이 허용되고 실제 CeTZ 의미를 유지한다면 대체 경로도 인정한다. 새 라이브러리 그림 렌더링은 이 샘플의 요구가 아니다.','discriminating_observation':'같은 import/로컬a와 출력 Markdown을 보존한 실행 로그 또는 질문자의 로컬경로 변경 허용 확인.'},
 'selection_reason':'current frame 두 번째 boundary. 원 입력2개와 성공기준2개 및 외부 import 자원이 명시되어 있다.'})
selected.append(r)
x=metadata[2];b=P.joinpath('_cache',str(x['question_id'])+'.html').read_text();r=common(x,'P3',3,'boundary','EV',[['docker','script','template','pdf','markdown'],['pdflatex','eisvogel','custom','files','build']]);r.update({
 'title_r0':html.unescape(x['earliest_body_revision']['title']),'main_tool_only_in_tag':False,'main_tool_absent_from_r0_tags':False,
 'input_summary':'build.sh가 TEST-includes.txt의 여섯 Markdown 경로를 받아 custom TEST-eisvogel.tex, pdflatex, 두 Python계열 Pandoc filter를 이용하여 하나의 PDF를 생성한다. 파일 목록과 명령은 있지만 실제 Markdown 및 수정 template 본문은 없다.',
 'desired_output':'기존 스크립트·디렉터리 구조·수정 template을 Docker 실행으로 계속 사용하고 여러 Markdown을 한 PDF로 합친다. 동료가 호스트에 Pandoc/LaTeX/Python/Eisvogel을 각각 설치하지 않아도 되는 구성.',
 'conditions':[condition(b,'C1','기존 script/layout과 custom Eisvogel template을 입력으로 사용하는 여러 Markdown→단일 PDF 변환을 컨테이너에 연결해야 한다.','<p>I am currently using','</p>'),condition(b,'C2','명시된 pdflatex·두 filter·template 경로를 보존하며 동료가 호스트에 Pandoc/LaTeX/Python/Eisvogel을 각각 설치하지 않는 방법을 근거로 뒷받침해야 한다.','<p>The end goal','</p>')],
 'user_versions':{'pandoc_image':'pandoc/extra:latest-ubuntu; example run uses pandoc/extra without explicit tag','pandoc':'실행 당시 core 판/digest 미제공','eisvogel':'custom fork 본문·원판 미제공','pdflatex':'미제공','pandoc-latex-environment':'미제공','pandoc-latex-unlisted':'미제공'},
 'adjacency_evidence':'Docker는 실행 host이며 직접 들어가는 파일/언어를 생산·소비하는 라이브러리로 간주하지 않는다. 본문에서 그 다음 첫 직접 입력자원은 customized eisvogel.tex이다. 주 분석 인접은 Eisvogel template publisher이며 pdflatex와 두 filter는 뒤에 나오는 후보로만 기록한다. template 없는 원 환경을 upstream 기본본으로 메우지 않는다.',
 'adjacency_spans':[span(b,'customized <em>eisvogel.tex</em>','</p>'),span(b,'--pdf-engine pdflatex','--template &quot;./TEST-eisvogel.tex&quot;')],
 'adjacent_candidates':[{'name':'Docker','role':'execution host/packaging, excluded from immediate content-resource boundary','selected':False,'body_first_char':b.index('Docker')},{'name':'Eisvogel','role':'first named direct input template resource','selected':True,'body_first_char':b.index('eisvogel.tex')},{'name':'cat','role':'simple filename-list relay; appears later in script','selected':False,'body_first_char':b.index('cat ./TEST-includes')},{'name':'pdflatex','role':'downstream PDF executor, later mention','selected':False,'body_first_char':b.index('pdflatex')},{'name':'pandoc-latex-environment','role':'filter inside pipeline, later mention','selected':False,'body_first_char':b.index('pandoc-latex-environment')},{'name':'pandoc-latex-unlisted','role':'filter inside pipeline, later mention','selected':False,'body_first_char':b.index('pandoc-latex-unlisted')}],
 'simple_relay':False,'missing':['수정 TEST-eisvogel.tex 원문','실제 여섯 Markdown 파일','컨테이너 digest/실제판','두 filter 설치판과 주변 요구'],
 'intent_interpretations':{'primary':'Docker 기반 기존 스크립트/수정 template/명시 의존의 연결 방법이 대상이며 단순 built-in template 대체는 충분하지 않다.','sensitivity':'완전한 원 입력이 없어도 일반 mount/entrypoint recipe로 답할 수 있다고 좁히면 부분 연결 지지를 별도 보고한다; 원 PDF 실행성으로 승격하지 않는다.','discriminating_observation':'동일 custom template·Markdown·filter·이미지 digest로 회사 대상 플랫폼에서 결과 PDF를 확인한 실행 기록.'},
 'selection_reason':'세 번째 boundary. 명령·파일리스트 입력과 단일 PDF+Docker 목적이 구체적이며 최초 직접 template 입력자원을 선택.'})
selected.append(r)
x=metadata[3];b=P.joinpath('_cache',str(x['question_id'])+'.html').read_text();r=common(x,'P4',4,'control',None,[['title','heading1','heading2','yaml','mapping'],['semicolon','markdown','parse','error','pandoc']]);r.update({
 'title_r0':html.unescape(x['earliest_body_revision']['title']),'main_tool_only_in_tag':False,'main_tool_absent_from_r0_tags':False,
 'input_summary':'text.md의 YAML title 값은 Heading1: Heading2이다. Pandoc command가 markdown을 읽고 두 filter를 거쳐 text.pdf를 쓰도록 되어 있으나 YAML parse exception이 보고된다.',
 'desired_output':'제목 안의 콜론을 그대로 유지하면서 YAML parse 오류를 없애 원 명령이 입력을 읽을 수 있게 한다. 원문은 colon을 semicolon이라고 부르며 문자의 실제값(:)을 기준으로 삼는다.',
 'conditions':[condition(b,'C1','YAML title 의미값 Heading1: Heading2의 콜론을 보존하여 명시된 mapping parse 오류를 피해야 한다.','<p>In <code>text.md</code>','</code></pre>'),condition(b,'C2','제시된 Markdown 입력 경계에서 동작하는 수단이어야 한다. 이름만 등장한 두 filter를 바꾸거나 제거하여 다른 문제를 풀었다고 하지 않는다.','<p>Due to the semicolon','</code></pre>')],
 'user_versions':{'pandoc':'2.18','pandoc-types':'1.22.2','texmath':'0.12.5.1','skylighting':'0.12.3.1','citeproc':'0.7','ipynb':'0.2','hslua':'2.2.1','Lua':'5.4'},
 'adjacency_evidence':'mermaid-filter와 pandoc-eqnos는 원 command에 있으나 원문의 실패 메시지는 YAML parser가 title 값을 읽는 단계다. 요청은 외부 filter의 생산물·동작·설치가 아니라 주 도구 입력 metadata 해석으로 끝나는 첫 대조로 고정한다. command에 인접 이름이 있다는 이유만으로 경계3쿼터를 추가하지 않는다.',
 'adjacency_spans':[span(b,'pandoc text.md -f markdown','</code></pre>'),span(b,'YAML parse exception','</code></pre>')],
 'adjacent_candidates':[{'name':'mermaid-filter','role':'present in command but no failure attributed to it; unchanged','selected':False,'body_first_char':b.index('mermaid-filter')},{'name':'pandoc-eqnos','role':'present in command but no failure attributed to it; unchanged','selected':False,'body_first_char':b.index('pandoc-eqnos')}],
 'simple_relay':False,'missing':['전체 문서/외부 filter 실제판/최종 PDF 실행환경','PDF 렌더 결과 자체는 이 입력 parse 질문에서 별도 검증되지 않음'],
 'intent_interpretations':{'primary':'원 질문의 YAML title parsing 해결과 콜론 값 보존을 평가한다. 최종 PDF와 named filters 전체 실행성은 추가 요구로 발명하지 않는다.','sensitivity':'PDF 전체 원 실행 성공까지 필수로 읽으면 입력과 filter/TeX환경이 부족하므로 문서 근거 완결과 분리하여 미확인.','discriminating_observation':'동일 title의 AST/metadata 출력 및 사용판2.18 원 명령 종료값; PDF까지 요구했는지 후속 설명.'},
 'selection_reason':'생성순 네 번째이며 주 도구 metadata 입력 parsing으로 해결 범위가 끝나는 첫 대조. A=B 동일 후보를 사용한다.'})
selected.append(r)
# Pre-outcome correction after a second reader compared the same R0: Docker image is an explicit argv/volume execution boundary, not just an incidental host.
r=selected[2];b=P.joinpath('_cache',str(r['question_id'])+'.html').read_text()
previous={k:r[k] for k in ['adjacent_label','adjacency_evidence','adjacent_candidates'] if k in r}
r['adjacent_label']='DK'
r['adjacency_evidence']='Pandoc Dockerfiles/이미지는 첫 문단에서 명시되고 바로 뒤 docker run --volume $(pwd):/data와 image command가 실제 입력·출력 파일을 Pandoc argv에 연결한다. 요청의 핵심이 기존 build.sh를 같은 image 내부에서 실행하는 것이므로 단순 우연한 host가 아니라 직접 인접 실행 경계다. 주 인접은 공식 pandoc/dockerfiles로 고정한다. 이후 Eisvogel은 template 입력자원 후보로만 남긴다.'
r['adjacency_spans']=[span(b,'<p>Performed a','</p>'),span(b,'docker run --rm','</code></pre>'),span(b,'<p>Looking through','</p>')]
r['adjacent_candidates']=[{'name':'pandoc/dockerfiles','role':'first explicit official image/entrypoint and mounted I/O execution boundary','selected':True,'body_first_char':b.index('Pandoc Dockerfiles')},{'name':'Eisvogel','role':'custom template input, named later than image execution boundary','selected':False,'body_first_char':b.index('eisvogel.tex')},{'name':'cat','role':'filename-list relay, later script mention','selected':False,'body_first_char':b.index('cat ./TEST-includes')},{'name':'pdflatex','role':'PDF executor, later script mention','selected':False,'body_first_char':b.index('pdflatex')},{'name':'pandoc-latex-environment','role':'filter, later mention','selected':False,'body_first_char':b.index('pandoc-latex-environment')},{'name':'pandoc-latex-unlisted','role':'filter, later mention','selected':False,'body_first_char':b.index('pandoc-latex-unlisted')}]
r['selection_reason']='세 번째 boundary. 원 command의 official image가 mounted input/output와 argv/script 실행에 직접 붙는다. 기존 Eisvogel 우선 제안은 결과·공식 해결본문을 열기 전에 원문 대조로 정정.'
P.joinpath('preseal-adjacency-amendment.json').write_text(json.dumps({'case_id':'P3','question_id':r['question_id'],'amended_utc':now,'stage':'recruitment, before any corpus ranking/body exposure, judgments or public outcomes','previous_proposal':previous,'new_label':'DK','new_evidence':r['adjacency_evidence'],'reason':'Second R0 reader found explicit image-entrypoint/script and mounted-I/O boundary before Eisvogel; host-only classification would suppress requested execution requirement.','not_based_on_outcome':True},ensure_ascii=False,indent=2))
for r in selected:
 b=P.joinpath('_cache',str(r['question_id'])+'.html').read_text().lower()
 for q in r['queries']:
  for t in q:assert re.search(r'(?<![a-z0-9_])'+re.escape(t)+r'(?![a-z0-9_])',b), (r['case_id'],t)
 assert not r['prior_id_excluded']
P.joinpath('selected.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2))
notes={
79692729:('selected_boundary','P1','knitr 외부 파일 선택; Pandoc은 현재 태그만이며 최초 태그에도 없음'),
79701174:('selected_boundary','P2','CeTZ import를 포함한 Typst→Markdown 동일 출력'),
79703916:('selected_boundary','P3','official Docker image의 argv/script·volume 직접 실행경계; Eisvogel은 후순위 후보'),
79714790:('selected_control','P4','YAML title parsing; 두 명시 filter에 원 failure를 귀속하지 않음'),
79730937:('not_selected_quota_filled','','PDF code-block page break; 구체적인 원 Markdown snippet 없음'),
79733265:('not_selected_quota_filled','','XeLaTeX와 font/Polyglossia 경계; 실제 입력 예제 존재하나 boundary quota 선착순 충족 뒤'),
79760026:('not_selected_quota_filled','','Haskell monadic type context; source/error 존재, 첫 control 이후'),
79762478:('not_selected_quota_filled','','draw.io SVG/PDF text selectability; 실제 diagram asset 미제공'),
79771027:('not_selected_quota_filled','','R/exams input screenshot와 LaTeX table output; 이미지 내용은 열지 않음'),
79775836:('not_selected_quota_filled','','rmarkdown footnote citation; earlier answer links/diagnoses appear in R0, linked answers not opened'),
79782379:('not_selected_quota_filled','','R Markdown raw table/two-column LaTeX; source includes earlier discussion links, not opened'),
79808295:('not_selected_quota_filled','','Orgmode custom DOCX styles; custom reference binary absent'),
79810437:('not_selected_quota_filled','','R0 explicitly reposts from LaTeX site; link identity absent, event independence unverified'),
79829958:('not_selected_quota_filled','','R/exams image inclusion, original PNG private path absent'),
79856860:('not_selected_quota_filled','','custom DOCX styles question without original template/source snippet')}
frame=[]
for i,x in enumerate(metadata):
 q=x['question_id'];status,cid,note=notes[q];g=x['earliest_body_revision']['revision_guid'];frame.append({'tag':'pandoc','window':'2025-07-01/2025-12-31','creation_rank':i+1,'question_id':q,'creation_utc':datetime.datetime.fromtimestamp(x['creation_date'],datetime.timezone.utc).isoformat(),'r0_guid':g,'r0_url':'https://stackoverflow.com/revisions/'+g+'/view-source','r0_revision':x['earliest_body_revision']['revision_number'],'initial_tags':';'.join(x['earliest_body_revision']['tags']),'current_tags':';'.join(x['tags']),'body_sha256':x['body_sha256'],'body_read':True,'prior68_excluded':q in excluded,'status':status,'case_id':cid,'reason':note,'independence':'repost explicitly reported in R0; original event unknown' if q==79810437 else 'no explicit same-event proof; independence unverified','answers_comments_scores_acceptance_seen':False})
with P.joinpath('frame.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(frame[0]));w.writeheader();w.writerows(frame)
P.joinpath('sources.jsonl').write_text(''.join(json.dumps({'source_id':r['source_id'],'Q':['Q1','Q2','Q3'],'case_id':r['case_id'],'url':r['r0_api_url'],'fixed_url':r['r0_url'],'payload_identifier':r['r0_guid']+' items[0].body','checked_utc':receipts[r['question_id']]['finished_utc'],'author_publisher':'Original Stack Overflow question asker; publisher Stack Exchange; author identity withheld during blinded recruitment','lineage':{'question_id':r['question_id'],'revision_number':1,'creation_utc':r['creation_utc'],'independence':r['independence']},'version_section':'First preserved revision, API HTML body; exact condition char/byte spans in selected.json','observed':r['input_summary']+' '+r['desired_output'],'supports':'Frozen requirements, adjacent resource identity, and first eligible recruitment order','limits':r['missing']+[r['adjacency_evidence']],'count_in_minimum':True,'category':'new_original_question','unique_key':'stackoverflow-question-'+str(r['question_id'])+'-r0','duplicate_reason':'API GUID and view-source are one original revision; failed view-source is not another source','body_sha256':r['r0_body_sha256'],'response_payload_sha256':receipts[r['question_id']]['payload_sha256']},ensure_ascii=False)+'\n' for r in selected))
# Log every R0 body actually read, even when the predeclared quota was already filled.
source_path=P/'sources.jsonl'
source_rows=[json.loads(line) for line in source_path.read_text().splitlines()]
bulk_revision_url=next(x['url'] for x in json.loads(P.joinpath('retrieval-receipts.json').read_text()) if '/posts/' in x['url'])
for x,f in zip(metadata,frame):
 if x['question_id'] in receipts:continue
 source_rows.append({'source_id':'R0-P-FRAME-'+str(f['creation_rank']),'Q':['Q1'],'case_id':None,'url':bulk_revision_url,'fixed_url':f['r0_url'],'payload_identifier':'revision_guid='+f['r0_guid']+' body','checked_utc':x['body_retrieved_utc'],'author_publisher':'Original Stack Overflow question asker; publisher Stack Exchange; owner metadata masked','lineage':{'question_id':x['question_id'],'revision_number':1,'creation_utc':f['creation_utc'],'independence':f['independence']},'version_section':'First preserved HTML body, full temporary cache read','observed':f['reason'],'supports':'Q1 ordered frame and exclusions; not a scored trial case','limits':['Boundary3+control1 quotas were filled by ranks1-4','No answers, linked earlier solutions, comments or execution evidence opened','Original-user/problem-event independence unverified'],'count_in_minimum':False,'category':'recruitment_extra_original_question','unique_key':'stackoverflow-question-'+str(x['question_id'])+'-r0','duplicate_reason':'One question R0, batch API and canonical revision URL are one source','body_sha256':x['body_sha256']})
source_path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in source_rows))
P.joinpath('recruitment-summary.json').write_text(json.dumps({'checked_utc':now,'excluded_prior_id_count':len(excluded),'selected_ids':[r['question_id'] for r in selected],'frame_rows':len(frame),'frame_has_more':False,'read_r0_bodies':15,'selected_boundary':3,'selected_control':1,'supplement_window_used':False,'supplement_reason':'First window supplied required3 boundary+1 control','masked_fields':['answers','comments','scores','acceptance','owner metadata'],'screening_only_first4_needed_but_all15_r0_read':True,'initial_metadata_probe':'First API probe used default field response internally, immediately projected to question_id/creation_date/title/tags/link; no score/answer/acceptance/owner field emitted, stored, or read by model. Then safe custom filters used and persisted.','source_coordinate_representation':'HTML body returned by StackExchange API, not Markdown view-source; all selected source HTML ASCII hence char and UTF-8 byte offsets agree.','failures':'4 web search/open DisabledError and4 direct view-source HTTP403; exact GUID API succeeded4/4.','no_later_outcomes_opened':True},ensure_ascii=False,indent=2))
print(json.dumps({'selected':[{k:r[k] for k in ['case_id','question_id','stratum','adjacent_label','queries']} for r in selected],'frame_rows':len(frame),'excluded_ids':len(excluded)},ensure_ascii=False,indent=2))
