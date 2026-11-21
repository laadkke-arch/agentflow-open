#!/usr/bin/env python3
"""Rebuild draft-B from frozen gold plus manually read evidence summaries.

Writes only this directory. Does not fetch pages or run A/P experiments.
Full source bodies and user names are deliberately absent.
"""
import collections
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
OWNED = HERE.parent.parent
REPO = OWNED.parents[3]
SHA011 = '478c301b693896e2c6d777f46ac441f071bfdfe8'
SHA014 = '42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9'
OBSERVED = '2026-11-21T04:01:50Z/2026-11-21T04:17:47Z'
IDS = ['T033','T036','T037','T040','T043','T044','T046','T048','T049','T054','T057','T058','T059','T061','SX01','SX08','SXR05']
metadata = {x['id']:x for x in json.loads((OWNED/'questions/old-metadata.json').read_text())}
old_answers = json.loads((OWNED/'gold/old-answers.json').read_text())
inputs = {q:json.loads((OWNED/f'questions/inputs/{q}.json').read_text()) for q in IDS}

def fixed(sha, name):
    return json.loads(subprocess.check_output(['git','show',f'{sha}:docs/workstreams/research/AF-RES-011/{name}'],cwd=REPO))

cases = {x['id']:x for x in fixed(SHA011,'CASES.json')['cases']}
nm = {x['id']:x for x in fixed(SHA011,'evidence/near-misses.json')['pairs']}

# Each entry below records text actually displayed and read in this subtask.
# A body read proves only the stated scope, not all candidate requirements.
SOURCE_ROWS = [
('pages','https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages','What is GitHub Pages?','live','L19,24,37','GitHub Pages는 저장소의 HTML·CSS·JavaScript를 게시하는 정적 사이트 호스팅 서비스다. github.io 서비스와 Enterprise Server 제공 범위를 구별한다.','블로그 엔진과 호스팅을 구별하는 근거다. Enterprise Server에도 제공되므로 모든 Pages가 자체 호스팅 불가능하다고 일반화하지 않는다.','turn702454932view0'),
('lambda','https://docs.aws.amazon.com/lambda/latest/dg/configuration-timeout.html','Configure Lambda Event Function timeout','live','L5–8,20–29,43–45','기본 Lambda 실행 제한은 최대900초다. Managed Instances의 비동기 및 일부 이벤트 소스 매핑 호출은 최대5400초라는 별도 범위가 명시되어 있다.','표준 함수 한 번에1시간 작업을 수행하는 범위만 N으로 판단한다. 모든 Lambda 상품·분할 작업·외부 작업 위임의 한계로 확장하지 않는다.','turn702454932view1;turn596773315view0'),
('mremoteng','https://mremoteng.org/','mRemoteNG','live','L14–16','RDP·VNC·SSH 등을 관리하는 공개 소스 탭형 원격 연결 관리자라고 명시한다.','이 소개만으로 모든 NAT/방화벽 우회 구성을 불가능하다고 증명하지 못한다. 현재 엄격 N의 공식 문서 입증은 미완료다.','turn702454932view2'),
('mime','https://pkg.go.dev/mime','Go mime package: TypeByExtension','go1.27.4, 2026-11-10','TypeByExtension L304–323','TypeByExtension은 확장자 문자열을 입력받아 그 확장자에 대응하는 MIME 형식을 조회한다. 이미지 본문 바이트의 실제 형식을 판별하는 함수가 아니다.','TypeByExtension 단독 사용만 판단한다. 다른 디코더·내용 검사와 결합한 Go 구현 또는 mime 패키지 전체를 부정하지 않는다.','turn702454932view3'),
('mycroft','https://github.com/MycroftAI/mycroft-core','Mycroft Core','live; archived 2024-09-08','repository description L120; archive notice L93','저장소의 제품 정체성은 Mycroft 음성 비서 플랫폼이다. 같은 제품을 다시 제시하는 것은 다른 Mycroft 대안을 찾는 요약 입력에 대응하지 않는다.','보관 상태는 현재 문서의 부가 관측이며 과거 반박 사유가 아니다. 원 반박자의 삭제 계정 신원은 확인되지 않는다.','turn486135429view3'),
('markovify','https://github.com/jsvine/markovify','Markovify README','live','README L187–240,241–255','기본 사용법은 입력 코퍼스로 모델을 만들고 make_sentence로 새 문장을 생성한다. 문장 길이 상한과 겹침 방지 설정이 설명되며 원문 단어 위치별 길이를 복제하는 기본 변환은 아니다.','수정하지 않은 기본 make_sentence 범위다. 확장 가능한 라이브러리이므로 사용자 코드로 제약을 추가할 수 없다는 주장이 아니다.','turn486135429view2;turn837421876view6;turn596773315view1'),
('nixnote','https://github.com/baumgarr/nixnote2','NixNote2 README','live','README L232–236','NixNote2는 Linux용 비공식 Evernote 클라이언트로 소개된다.','클라이언트라는 정체성만으로 로컬 사용·오프라인 사용·내보내기 전체를 불가능하다고 할 수 없다. 현재 원문 조건에 대한 엄격 위반 입증은 보류한다.','turn486135429view1;turn837421876view7'),
('jekyll','https://jekyllrb.com/docs/','Jekyll documentation','4.4.1','L24; overview','마크업과 레이아웃을 결합해 정적 웹사이트를 생성하는 도구라고 설명한다.','소개에 인증·큐가 없다는 이유만으로 외부 서비스와의 조합 가능성까지 배제할 수 없다. T037의 엄격 N으로 확정하지 않는다.','turn486135429view0;turn837421876view8'),
('jcommander','https://jcommander.org/','JCommander documentation','live','overview L51–101','Java 주석과 String[] 입력으로 옵션을 파싱하는 사용법 및 긴 옵션 예가 있다.','공식 본문에서 묶은 짧은 옵션의 불지원 범위를 명시적으로 확인하지 못했다. 경쟁 라이브러리의 비교 주장은 대신 쓰지 않는다.','turn307696399view7'),
('ghost','https://docs.ghost.org/','Ghost developer documentation','live','installation and developer overview','직접 설치와 로컬 개발, Docker 설치 등 Ghost 운영 경로를 안내한다.','고정014의 실제 답 후보 정체성을 확인했으며 이 소개만으로 모든 SEO·운영 부담 조건을 실험한 것은 아니다.','turn775581791view0'),
('padstart','https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/padStart','String.prototype.padStart','live','L183,214–219','문자열 앞에 패딩을 붙여 목표 길이를 맞추는 표준 메서드의 동작과 인자를 설명한다.','특정 프로젝트에서 의존성 사용보다 항상 유리하다는 인과 결론은 낼 수 없다. 고정014 양성은 답 후보이지 사용 성공 보증이 아니다.','turn775581791view1;turn837421876view5'),
('django','https://www.djangoproject.com/start/overview/','Django at a glance','live','L18,27 and overview','공개 웹 프레임워크이며 인증·관리자 등 웹 응용 기능을 안내한다.','1–3인 팀의 동일 숙련도 조건에서 대안보다 생산성이 높다는 비교 실험은 아니다.','turn775581791view2'),
('slurm','https://slurm.schedmd.com/overview.html','Slurm workload manager overview','live','L4–10','클러스터 자원 할당·작업 실행·대기열 관리를 담당하는 작업 관리 시스템이다.','사용자 제출의 정확히 한 번 등록·실행 보장은 이 개요만으로 확인되지 않는다.','turn775581791view3'),
('rhasspy','https://rhasspy.readthedocs.io/en/latest/','Rhasspy voice assistant','live','L7,14–38','오프라인 공개 소스 음성 비서 서비스와 JSON 명령·홈 자동화 통합을 설명한다.','당시 또는 현재 유지보수의 지속성을 보증하지 않는다.','turn775581791view4'),
('meshcentral','https://meshcentral.com/','MeshCentral','live','L11,19','자체 호스팅 원격 관리와 서버·에이전트 구조, Windows·Linux·macOS·FreeBSD 대상 지원을 소개한다.','모든 실제 방화벽 정책에서 개별 설정 없이 작동한다고 검증한 것은 아니다.','turn837421876view0'),
('authentik','https://docs.goauthentik.io/','authentik documentation','live','L34–36','IdP와 SSO 및 인증 프로토콜 지원을 설명한다.','이 자료로 통합 인증이 개별 비밀번호보다 항상 안전하거나 위험하다고 단정하지 않는다.','turn775581791view5'),
('openzfs','https://openzfs.github.io/openzfs-docs/','OpenZFS documentation','live','documentation index and platform/pool topics','저장 풀과 파일 시스템을 다루는 OpenZFS 문서와 플랫폼별 설치 경로가 제시되어 있다.','7디스크 ESXi 구성의 이행·성능·복구를 직접 실행하지 않았다.','turn775581791view6'),
('owasp','https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html','OWASP File Upload Cheat Sheet','live','file signature validation L271–275 and validation guidance','파일 업로드의 형식·시그니처 등 여러 확인을 조합하며 단일 시그니처 확인만으로 충분하지 않다는 지침이다.','실제 채택 라벨은 고정014에서 왔다. 이 문서는 Go 라이브러리나 리사이즈 함수 하나를 지정하는 것이 아니다.','turn837421876view1;turn107385175view8'),
('gemini','https://geminiprotocol.net/','Project Gemini','live','L2–3','연결된 텍스트 문서와 가벼운 웹 공간을 위한 프로토콜·생태계를 소개한다.','공간의 모든 참여자가 비상업적이거나 깊이 있는 내용을 쓴다고 증명하지 않는다.','turn837421876view2'),
('softserve','https://github.com/charmbracelet/soft-serve','Soft Serve README','live','README L215–219','명령줄 중심의 자체 호스팅 Git 서버로 소개한다.','GitHub 기능 전체의 대체나 이행 비용 비교 자료는 아니다.','turn837421876view4;turn107385175view2'),
('selenium','https://www.selenium.dev/','Selenium','live','L1–10','브라우저 자동화를 제공하며 Java와 Python을 포함한 언어 생태계를 안내한다.','질문의 특정 크롤링 사이트나 규모가 없어 언어 간 성능 우열을 이 자료로 정할 수 없다.','turn775581791view7'),
('tinymedia','https://www.tinymediamanager.org/','tinyMediaManager','live','L17 and overview','Java Swing 기반의 미디어 메타데이터 관리와 Kodi·Emby·Plex용 정보 및 파일 이름 관리를 소개한다.','질문의 seedbox 연동 전체나 모든 자막 조건은 이 소개만으로 확인되지 않는다.','turn837421876view3'),
('kicadmcp','https://github.com/mixelpixx/KiCAD-MCP-Server','KiCAD MCP Server','live','repository description and README introduction','LLM 도구와 KiCAD의 회로·PCB 작업을 연결하는 MCP 서버라는 제품 범위를 확인했다.','고정011 답의 모델 선택 절차를 정식 제품 기능이나 검증된 성능으로 바꾸어 읽지 않는다.','turn414639488view8;turn107385175view7'),
('lodash','https://lodash.com/docs/','Lodash Documentation: padStart','live; method since4.0.0','L9477–9512','padStart는 목표 길이보다 짧은 문자열 앞에 지정 문자를 덧붙이는 함수이며 예와 인자가 제시되어 있다.','실제 스레드의 채택 후보로 추가하지 않는다. 필수 조건 없는 질문에서 비교용 미판정 후보일 뿐이다.','turn455720473view1'),
('authelia','https://www.authelia.com/','Authelia','live','L3 and overview','SSO·MFA·OpenID Connect를 제공하는 인증·접근 관리 도구로 소개된다.','T046 실제 답 정답이 아니며 보안 우열이나 필수 조건 위반을 판정하지 않았다.','turn307696399view8'),
('unraid','https://unraid.net/','Unraid','live','L9,67','NAS와 자체 호스팅 서버 운용을 위한 운영 체제로 소개된다.','T048의 기존 RAID5가 새 후보의 필수 아키텍처라고 가정하지 않았다. 후보의 위반 또는 적합성을 확정하지 않는다.','turn414639488view1'),
('qwen','https://github.com/QwenLM/Qwen3-Coder','Qwen3-Coder README','live','README L205–216','코딩 에이전트와 도구 호출 관련 모델 프로젝트를 소개한다.','KiCAD 회로 직접 배선·PCB 라우팅의 특정 성공 또는 실패를 확인한 자료가 아니다. 고정011의 Qwen3.8 언급과 같은 모델로 합치지 않는다.','turn307696399view3;turn107385175view6'),
('neocities','https://neocities.org/','Neocities','live','L4 and overview','개인 웹사이트 창작을 위한 정적 호스팅과 사회적 발견 공간을 소개한다.','T057의 실제 답 정답으로 추가하지 않았으며 그 공간의 모든 글의 품질을 판정하지 않았다.','turn414639488view2'),
('codeberg','https://docs.codeberg.org/getting-started/what-is-codeberg/','What is Codeberg?','live','L42–45','Forgejo 기반의 비영리 코드 협업 호스팅을 설명한다.','T058의 새 양성 정답으로 만들지 않으며 장애·협업 기능의 상대 우열을 입증하지 않는다.','turn414639488view3'),
('jsoup','https://jsoup.org/','jsoup: Java HTML Parser','1.24.1 shown','L10–17','Java에서 HTML을 가져오고 파싱하며 데이터를 추출하는 라이브러리다.','대상 사이트가 주어지지 않아 브라우저 실행이 필요한지 판단하지 않았다. 미판정 비교 후보다.','turn414639488view4'),
('tautulli','https://tautulli.com/','Tautulli','live','L12 and overview','Plex 서버의 시청 활동과 통계·알림을 다루는 도구다.','알림 스크립트나 외부 조합까지 포함해 자막·seedbox 작업이 불가능하다고 증명하지 못한다. 엄격 N이 아니다.','turn414639488view5'),
('joplin','https://joplinapp.org/','Joplin','live','L31,64,72,77','공개 소스 노트 앱, Markdown, 데스크톱·모바일과 개방형 형식에 대한 설명을 확인했다.','질문 스레드의 실제 답이나 채택은 아니다. 부족한 양성 정답을 이 제품으로 대체하지 않는다.','turn307696399view6'),
('translate','https://docs.python.org/3/builtins/stdtypes.html','Python built-in types: str.translate and str.maketrans','3.15.2 displayed','L1317–1325,1617–1628','문자별 변환 표로 원문을 변환하며 매핑하지 않은 문자를 유지할 수 있다. 일대일 매핑을 구성하면 서식 문자 보존을 시도할 수 있다.','질문 스레드의 실제 답이 아니다. 작업자가 제안한 미판정 절차이며 원문 의미 은닉 강도나 출력 시각 효과를 실행하지 않았다.','turn455720473view0;turn596773315view2'),
('ghostscript','https://ghostscript.readthedocs.io/en/latest/','Ghostscript documentation','10.09.0 displayed','L11 and overview','PostScript·PDF 해석 및 처리 도구를 설명한다.','블로그 엔진 후보와 이름만 유사한 무관 후보다.','turn307696399view0'),
('padlet','https://padlet.com/','Padlet','live','L4–27','시각적 협업 보드·캔버스 제품으로 소개된다.','padStart 의존성·함수 선택 문제의 해결 후보가 아니다.','turn896216904view1'),
('springrts','https://github.com/spring/spring','Spring RTS engine README','live','README L207–211','실시간 전략 게임 엔진임을 명시한다.','Spring 웹 프레임워크와 혼동하지 않는다. 숙박 예약 서비스용 CRUD 프레임워크로 채점하지 않는다.','turn307696399view1;turn107385175view4'),
('s3browser','https://s3browser.com/','CS Browser, formerly S3 Browser','live','L17–19','Windows용 S3 호환 스토리지 관리 GUI이며 CS Browser로 이름이 변경되었다고 안내한다.','파일 관리용 도구라는 범주만 확인했다. CLI 자동화가 전혀 없다는 주장을 하지 않는다. 일반 작업 스케줄러 후보와 구별한다.','turn896216904view3'),
('rhino','https://www.rhino3d.com/','Rhino 3D','live','L24–38','3D 형상 모델링 소프트웨어를 소개한다.','음성 비서 후보인 Rhasspy 또는 다른 Rhino 음성 도구와 동일시하지 않는다.','turn896216904view4'),
('meshlab','https://www.meshlab.net/','MeshLab','live','L0–1','3D 삼각형 메시 처리·편집 도구임을 설명한다.','MeshCentral과 이름 일부만 비슷하며 Windows 원격 관리 도구가 아니다.','turn896216904view5'),
('autohotkey','https://github.com/AutoHotkey/AutoHotkey','AutoHotkey','live','repository description L119','Windows 매크로와 자동화 스크립트 도구임을 명시한다.','인증 IdP·SSO 제품으로 판단하지 않는다. 브라우저를 자동화하는 가능성과 인증 서비스 역할을 구별한다.','turn414639488view6;turn107385175view5'),
('openshot','https://www.openshot.org/','OpenShot Video Editor','live','L24–36','동영상 편집기를 소개한다.','OpenZFS와 이름 일부만 유사하며 저장 계층 대안이 아니다.','turn896216904view7'),
('imgui','https://github.com/ocornut/imgui','Dear ImGui','live','README L222–224','C++ 사용자 인터페이스 라이브러리와 렌더링 용도를 설명한다.','Go 업로드 이미지 파일의 검증 라이브러리와 구별한다. 이미지처럼 보이는 이름만으로 적합성을 주지 않는다.','turn888243950view0;turn107385175view3'),
('kibana','https://www.elastic.co/kibana','Kibana','live','L18 and product introduction','Elasticsearch 데이터의 시각화·대시보드를 위한 제품을 소개한다.','KiCAD PCB 설계·배선 도구가 아니다.','turn888243950view1'),
('geminiexchange','https://www.gemini.com/','Gemini financial platform','live','L53–54','금융 시장 및 디지털 자산 거래 플랫폼임을 확인했다.','Project Gemini 문서 생태계와 다른 대상이다. 금융 제품에 대한 추천이나 안전성 평가는 하지 않았다.','turn888243950view2'),
('gitbook','https://www.gitbook.com/','GitBook','live','L28–30','문서 작성·게시 플랫폼임을 확인했다.','Git 호스팅 코드 협업 대안과 문서 호스팅을 구별한다. 통합 기능이 전혀 없다는 주장은 아니다.','turn888243950view3'),
('element','https://periodic-table.rsc.org/element/34/selenium','Selenium element information','live','factbox L62–71','Selenium은 원자번호34의 화학 원소로 제시된다.','브라우저 자동화 소프트웨어와 동명이지만 이 페이지는 개발 도구가 아니다.','turn888243950view4;turn107385175view9'),
('mediawiki','https://www.mediawiki.org/wiki/MediaWiki','MediaWiki','live','L59','협업과 문서화를 위한 위키 소프트웨어라고 소개한다.','MediaManager·tinyMediaManager와 이름 일부만 유사한 무관 후보다.','turn888243950view5'),
('noteperformer','https://www.noteperformer.com/','NotePerformer','live','L6,35–43','악보 재생과 오케스트라 음향 엔진을 제공한다.','개인 노트·Markdown 관리 앱과 같은 note 단어를 쓴다는 이유로 관련성을 주지 않는다.','turn888243950view6'),
('picsum','https://picsum.photos/','Lorem Picsum','live','L0–8','너비·높이를 지정해 자리표시자 사진을 가져오는 서비스를 설명한다.','원문 글자·단어 외형을 유지하는 텍스트 변환과 다른 입력·출력이다.','turn888243950view7'),
('javaparser','https://javaparser.org/','JavaParser','live','L10–20,60','Java 소스 코드의 구문 분석·변형과 AST를 다룬다.','명령줄 옵션 파서와 Java 소스 언어 파서를 구별한다.','turn888243950view8'),
]

sources = []
for key,url,title,version,sections,confirmed,limits,refs in SOURCE_ROWS:
    sources.append(dict(id='GB-'+key,url=url,accessed_at_utc=OBSERVED,source_type='official_documentation',title=title,version_or_date=version,sections_read=sections,confirmed=confirmed,limits=limits,level='D1',used_in=['Q3'],body_read=True,web_refs=refs.split(';'),timestamp_semantics='UTC interval covering this subtask body reads; exact per-open second was not exposed',count_as_method_literature=False))

S = {x['id'][3:]:x for x in sources}

def evidence(key, scope=None):
    s=S[key]
    return {'source_id':s['id'],'url':s['url'],'scope':scope or s['title'],'accessed_at_utc':s['accessed_at_utc'],'confirmed':s['confirmed'],'limits':s['limits']}

supplemental = []
for a in cases['T054']['answers']:
    # A003 names a model without a verified model identity. Preserve the source
    # record but do not manufacture a canonical entity or a grade2 outcome.
    label = {'T054.A001':'Use a less compressed local model with fewer tools and inspect warnings', 'T054.A002':'Compare 4–6-bit models on the same KiCAD task with a reduced tool set', 'T054.A003':'Model-selection anecdote in T054.A003 (model identity unverified)'}[a['analysis_id']]
    supplemental.append({'query_id':'T054','answer_id':a['analysis_id'],'candidate':label,'candidate_url':None,'grade':'1','mapping':'answer_principle' if a['role']=='principle' else 'answer_experience_unresolved_entity','source_url':a['evidence'],'gold_provenance':'fixed011 actual answer, newly graded by worker under fixed014 RULES','source_sha':SHA011,'source_path':'docs/workstreams/research/AF-RES-011/CASES.json#T054.answers','gold_judge':'작업자; 외부 답 기록의 새 등급화','reason':a['summary'],'eligible_for_entity_recall':False,'eligible_for_answer_unit_recall':True,'accepted_or_used':False,'limits':'특정 모델을 공식 시험한 결과가 아니다. 제품명 후보와 별개인 절차·경험 단위이며 URL/실체 일치 평가와 분리한다.'})

supplemental.append({'query_id':'SXR05','answer_id':'SE38872','candidate':'FeSimpleArgs','candidate_url':'https://bitbucket.org/ccperkins/fesimpleargs','grade':'2','mapping':'actual_answer_external_url','source_url':'https://softwarerecs.stackexchange.com/a/38872','gold_provenance':'public Stack Exchange answer API accepted field; fixed011 supplementary context','source_sha':SHA011,'gold_judge':'외부 채택 기록; 작업자 추출','accepted_or_used':True,'evidence_url':'https://api.stackexchange.com/2.3/answers/38872?site=softwarerecs&filter=withbody','checked_at_utc':'2026-11-21T04:07:45.424747+00:00','observed_api_fields':{'answer_id':38872,'question_id':26907,'is_accepted':True},'reason':'공개 답 API에서 is_accepted=true를 확인했다. 감사 표현을 사용 채택으로 추정하지 않았다.','limits':'현재 Bitbucket 프로젝트는 열었지만 본문이0줄이어서 현행 제품 기능은 미확인이다. 답은 질문일 이후 게시된 정답 사건이다.'})

no_positive = [
 {'qid':'SX01','positive_status':'unavailable','reason':'형식상 답3개의 후보 Laverna·Turtl·NixNote에 질문자 반박이 있고 채택 답이 없다. 새 제품을 찾아 grade1을 보충하지 않았다.','rejection_evidence':[{'answer_id':35399,'candidate':'Laverna','comment_ids':[51257,51263,51286,51287,102560],'confirmed':'동기화 인증 후 빈 화면 반박. 일시적으로 작동한다는 다른 댓글도 다음 댓글에서 저장·새 문서 실패로 정정했다.'},{'answer_id':35564,'candidate':'Turtl','comment_ids':[51402,51403],'confirmed':'UI 및 다른 도구로 읽기 어려운 데이터 형식에 대한 반박.'},{'answer_id':35551,'candidate':'NixNote/NeverNote','comment_ids':[51364,57358],'confirmed':'질문자는 Evernote 서버에서 벗어나려는 목적을 재확인했고 동기화 의존 반박이 남아 있다.'}],'source_url':inputs['SX01']['question_url_excluded_from_search'],'checked_at_utc':OBSERVED,'judge':'작업자; 외부 답/댓글 기록 대조'},
 {'qid':'SX08','positive_status':'unavailable','reason':'형식상 답2개 모두 질문자의 명시 반박을 받았으며 채택 답이 없다. 공식 문서에서 찾은 Python 변환 절차는 실제 정답으로 추가하지 않았다.','rejection_evidence':[{'answer_id':84081,'candidate':'Markov-chain generators','comment_ids':[103657],'confirmed':'원문 대응 단어 길이를 보존하지 않는다는 반박.'},{'answer_id':84073,'candidate':'Fillerama/Smodin','comment_ids':[103656],'confirmed':'원문을 보존하는 변환 대신 무제약 새 텍스트를 만드는 답이라는 반박.'}],'source_url':inputs['SX08']['question_url_excluded_from_search'],'checked_at_utc':OBSERVED,'judge':'작업자; 외부 답/댓글 기록 대조'},
]

positive_map = {
 'T033':('T033.A003','Ghost','ghost'),'T036':('T036.A042','JavaScript padStart','padstart'),
 'T037':('T037.A001','Django','django'),'T040':('T040.A011','Slurm','slurm'),
 'T043':('T043.A001','Rhasspy Voice Assistant','rhasspy'),'T044':('T044.A005','MeshCentral','meshcentral'),
 'T046':('T046.A001','Authentik','authentik'),'T048':('T048.A001','OpenZFS','openzfs'),
 'T049':('T049.A001','OWASP File Upload Cheat Sheet','owasp'),'T057':('T057.A016','Project Gemini','gemini'),
 'T058':('T058.A021','soft-serve','softserve'),'T059':('T059.A006','Selenium','selenium'),
 'T061':('T061.A027','tinyMediaManager','tinymedia')}

def base(q,slot,name,url,grade,reason,key=None):
    return {'check_id':q+'-'+{'positive':'POS','near_miss':'N','unrelated':'ZERO'}[slot], 'slot':slot,'name':name,'url':url,'grade':grade,'reason':reason,'provenance':{},'violated_condition':None,'official_evidence':[evidence(key)] if key else [],'eligible_positive_denominator':False,'eligible_strict_n_denominator':False,'eligible_unrelated_denominator':False,'expected_action':'unjudged','judgment_status':'unjudged','limitations':[]}

def condition(q,target,location=None,polarity='positive'):
    original = inputs[q]['input_mode']=='original'
    return {'target':target,'polarity':polarity,'location':location or f'questions/inputs/{q}.json#question_summary','question_sha256':inputs[q]['question_sha256'],'original_available':original,'location_status':'first revision verified' if original else 'fixed011 summary only; original position unavailable'}

checks=[]
for q in IDS:
    if q in positive_map:
        aid,name,key=positive_map[q]
        g=next(a for a in old_answers if a['query_id']==q and a['answer_id']==aid and a['candidate']==name)
        row=base(q,'positive',name,g['candidate_url'],g['grade'],'고정014의 실제 답 정답을 그대로 사용한다. 공식 자료는 후보 정체성·범위 확인용이며 현재 모든 조건 충족을 보증하지 않는다.',key)
        row.update(provenance=g,eligible_positive_denominator=True,expected_action='retain',judgment_status='external_gold_fixed014')
    elif q=='T054':
        g=next(x for x in supplemental if x['query_id']==q and x['answer_id']=='T054.A002')
        row=base(q,'positive',g['candidate'],None,'1','실제 답이 제시한 같은 과제·4–6비트·축소 도구 집합 비교 절차다. 특정 모델명의 정답으로 바꾸지 않는다.','kicadmcp')
        row.update(provenance=g,eligible_positive_denominator=True,expected_action='retain',judgment_status='worker_grade_of_actual_answer')
        row['candidate_url_status']='No independent artifact URL in the actual answer; source-thread URL withheld from candidate input'
        row['limitations'].append('정답1은 절차에 붙인 것이며 제품명 entity recall에는 제외한다. 후보 거절 평가에서 이 형태를 허용하는지 별도 민감도 분석이 필요하다.')
    elif q=='SXR05':
        g=next(x for x in supplemental if x['query_id']==q)
        row=base(q,'positive',g['candidate'],g['candidate_url'],'2',g['reason'])
        row.update(provenance=g,eligible_positive_denominator=True,expected_action='retain',judgment_status='external_accepted_api')
        row['official_evidence']=[{'source_id':'GB-excluded-fesimpleargs','url':g['candidate_url'],'scope':'project page','accessed_at_utc':OBSERVED,'confirmed':'열기 응답에 읽을 수 있는 본문이0줄이었다.','limits':'현행 기능·라이선스·작동 여부 unavailable; accepted 정답 증거와 별개.'}]
        row['limitations'].append('채택 사실은 확인됐지만 공식 프로젝트의 현재 기능은 미확인이다.')
    else:
        key,name=('joplin','Joplin') if q=='SX01' else ('translate','Python str.translate with a one-to-one letter mapping')
        row=base(q,'positive',name,S[key]['url'],'0','양성 정답 unavailable 자리의 그럴듯한 미판정 후보다. 실제 답 정답 또는 알려진 오답으로 취급하지 않는다.',key)
        row['provenance']={'selection':'작업자 구성 보조 후보','gold_status':'unjudged; not an actual unrefuted answer','missing_gold_record':q}
        row['limitations'].append('grade0은 미판정 코딩값이다. 무관0이나 양성1과 합치지 않으며 양성 거절률의 분모에서 제외한다.')
    checks.append(row)

def strict(q,name,key,nmid,target,reason,scope=None):
    r=base(q,'near_miss',name,S[key]['url'],'N',reason,key)
    r.update(eligible_strict_n_denominator=True,expected_action='exclude',judgment_status='historical_N_current_scope_verified' if nmid else 'worker_constructed_strict_N')
    r['provenance']={'selection':'기존011 엄격 N의 명시된 범위 재검증' if nmid else '작업자 구성','source_sha':SHA011 if nmid else None,'near_miss_id':nmid,'historical_record':nm[nmid] if nmid else None,'judge':'작업자; 공식 문서 대조'}
    r['violated_condition']=condition(q,target)
    if scope:r['official_evidence'][0]['scope']=scope
    return r

near={
 'T033':strict('T033','GitHub Pages (github.io hosted service; not a blog engine)','pages','NM05','자가 호스팅할 오픈소스 블로그 시스템','공식 설명은 정적 웹 호스팅이다. github.io 호스팅 자체를 설치할 블로그 시스템의 대안으로 제시하는 범위는 실제 질문자의 반박 및 현재 범주와 어긋난다.','GitHub-hosted github.io service only; excludes GitHub Enterprise Server and a separate blog generator'),
 'T040':strict('T040','Amazon S3 events + AWS Lambda standard function (Managed Instances 제외)','lambda','NM06','30초–1시간 작업','한 작업을 표준 Lambda 함수의 단일 호출에서 실행하면 최대900초 제한 때문에1시간 작업을 처리하지 못한다. Managed Instances의90분 범위는 이 검사 후보에 포함하지 않는다.','single standard Lambda function invocation; excludes Managed Instances, external worker delegation and task splitting'),
 'T043':strict('T043','Mycroft / Mycroft Core','mycroft','NM07','Mycroft 외의 다른 자가 호스팅 음성 비서','이미 비교 대상인 Mycroft를 그대로 대안으로 다시 제시한다. 현재 공식 저장소로 동일 제품 정체성을 확인했다.','same Mycroft product, not a separately named fork'),
 'T049':strict('T049','Go mime.TypeByExtension as the sole uploaded-image validator','mime',None,'파일 확장자를 대신하는 실제 형식 판별','공식 정의가 파일 확장자 문자열에 따른 MIME 조회다. 내용 바이트의 실제 형식 확인을 요청한 문제를 확장자 조회만으로 해결한다고 하면 명시 입력·작동 범위가 위반된다.','mime.TypeByExtension alone; no image decoder/content inspection added'),
 'SX08':strict('SX08','Markovify default make_sentence (unmodified corpus-to-new-sentence generation)','markovify','NM15','원문의 순서에 대응하는 단어 길이·문장부호·줄바꿈 보존','새 문장 생성은 원문 위치별 단어 길이와 문장부호를 보존하는 변환이 아니다. 실제 반박과 기본 API 작동 범위가 일치한다.','default make_sentence only; excludes custom constraints/subclasses/post-processing'),
}
near['T043']['limitations'].append('고정011 반박자는 삭제 계정으로 원질문자 신원을 확정하지 못한다. 다른 대안이라는 현재 요약 입력과의 동일성 검사가 현재 판단 근거다.')
near['SX08']['violated_condition']=condition('SX08','단어 순서·비슷한 길이·문장부호·줄바꿈 보존','first revision: first body paragraph; questions/inputs/SX08.json#question_source')

unavailable={
 'T036':('Lodash padStart','lodash','필수 조건 없음. 의존성 선택의 비교 문제에 사후 금지 조건을 만들지 않는다.'),
 'T037':('Jekyll without an additional backend','jekyll','같은 범주의 정적 사이트 생성기는 찾았으나 질문이 조합을 금지하지 않는다. 개요에서 인증·큐가 언급되지 않는 것을 공식 불지원으로 바꿀 수 없다.'),
 'T046':('Authelia','authelia','필수 조건 없음. OAuth/SSO의 위험 비교에서 다른 IdP를 엄격 위반 후보로 만들 수 없다.'),
 'T048':('Unraid','unraid','새 저장 계층이라는 조건만으로 Unraid의 엄격 위반을 확정할 수 없다. 기존 RAID5 구조를 새 후보의 필수 요구로 소급하지 않는다.'),
 'T054':('Qwen3-Coder','qwen','공식 자료에서 KiCAD 직접 배선·PCB 라우팅 조건의 명시적 불지원 또는 범위가 확인되지 않았다. 검증 없이 모델의 실패를 가정하지 않는다.'),
 'T057':('Neocities','neocities','필수 조건 없음. 개인적·비상업적 공간이라는 선호를 객관적 금지 조건으로 만들지 않는다.'),
 'T058':('Codeberg','codeberg','필수 조건 없음. GitHub 대안에 CI·예산·자가 호스팅 조건을 덧붙이지 않는다.'),
 'T059':('jsoup','jsoup','필수 조건 없음. 대상 사이트의 JavaScript 실행 필요를 추정해 Java HTML 파서를 실패로 만들지 않는다.'),
 'T061':('Tautulli','tautulli','자막·seedbox 필수성은 메타데이터에 있으나 공식 소개의 비언급은 불지원 증거가 아니다. 기존011 NM11은 다른 독자의 후속 필수 조건으로 이미 엄격 N에서 제외됐다.'),
 'SXR05':('JCommander','jcommander','최초판에는 임의 옵션 이름 조건이 없다. 기존 picocli/args4j의 후속 수정판 N을 이 입력에 재사용하지 않는다. 묶은 짧은 옵션의 불지원을 자기 공식 문서로 입증하지 못했다.'),
}
for q,(name,key,why) in unavailable.items():
    r=base(q,'near_miss',name,S[key]['url'],'0',why,key)
    r['provenance']={'selection':'작업자 구성 보조 후보','strict_N_status':'unavailable','grade_semantics':'0/unjudged, not known irrelevant'}
    r['limitations'].append('엄격 N 역할이 결측이다.3행 형태를 채우기 위한 미판정 보조 후보이며 올바른 N 거절률 분모에 포함하지 않는다.')
    if q=='SXR05':r['provenance']['excluded_historical_near_misses']=[nm['NM18'],nm['NM19']]
    if q=='T061':r['provenance']['excluded_historical_near_miss']=nm['NM11']
    near[q]=r

for q,key,nmid,name,why in [
 ('T044','mremoteng','NM10','mRemoteNG','기존011에서 다른 독자가 연결 관리 UI가 도달성을 해결하지 않는다고 반박했다. 현재 공식 소개는 연결 관리자라는 범위만 확인하며, 정확한 방화벽/NAT 구성별 불가능을 입증하지 못한다.'),
 ('SX01','nixnote','NM12','NixNote2 with Evernote synchronization','기존011은 Evernote 서버 의존 반박을 N으로 코딩했다. 최초판의 데이터 개방성·앱 독립성 조건과 현재 NixNote의 로컬 저장·내보내기 범위를 공식 문서로 완전히 대조하지 못했다.')]:
    r=base(q,'near_miss',name,S[key]['url'],'N',why,key)
    r.update(judgment_status='historical_N_current_unverified',expected_action='unjudged')
    r['provenance']={'selection':'기존011 N 보존; 현재 엄격 N 분모 제외','source_sha':SHA011,'near_miss_id':nmid,'historical_record':nm[nmid]}
    r['violated_condition']=condition(q,'대상 PC별 방화벽 설정 없는 중앙 원격 접속' if q=='T044' else '공개 형식과 앱에서 독립한 데이터 소유',None if q=='T044' else 'first revision requirement1; questions/inputs/SX01.json#question_source')
    r['limitations'].append('역사적 N 등급을 삭제하거나 현재 확정 N으로 오해하지 않도록 별도 상태를 둔다. 현재 범위 공식 근거 부족으로 strict-N 분모 제외.')
    near[q]=r

unrelated={
 'T033':('Ghostscript','ghostscript'),'T036':('Padlet','padlet'),'T037':('Spring RTS engine','springrts'),
 'T040':('CS Browser (formerly S3 Browser)','s3browser'),'T043':('Rhino 3D','rhino'),'T044':('MeshLab','meshlab'),
 'T046':('AutoHotkey','autohotkey'),'T048':('OpenShot Video Editor','openshot'),'T049':('Dear ImGui','imgui'),
 'T054':('Kibana','kibana'),'T057':('Gemini exchange','geminiexchange'),'T058':('GitBook','gitbook'),
 'T059':('Selenium chemical element reference','element'),'T061':('MediaWiki','mediawiki'),
 'SX01':('NotePerformer','noteperformer'),'SX08':('Lorem Picsum','picsum'),'SXR05':('JavaParser','javaparser')}

for q in IDS:
    checks.append(near[q])
    name,key=unrelated[q]
    row=base(q,'unrelated',name,S[key]['url'],'0',S[key]['confirmed']+' '+S[key]['limits'],key)
    row.update(provenance={'selection':'작업자 구성; 이름·범주 혼동 검사','source_id':S[key]['id'],'judge':'작업자; 공식 설명으로 역할 대조'},eligible_unrelated_denominator=True,expected_action='exclude',judgment_status='worker_confirmed_unrelated')
    checks.append(row)

checks.sort(key=lambda x:(IDS.index(x['check_id'].split('-')[0]),['positive','near_miss','unrelated'].index(x['slot'])))
questions=[]
for q in IDS:
    rows=[x for x in checks if x['check_id'].startswith(q+'-')]
    nr=next(x for x in rows if x['slot']=='near_miss')
    questions.append({'qid':q,'input_mode':inputs[q]['input_mode'],'question_sha256':inputs[q]['question_sha256'],'positive_status':'available' if rows[0]['eligible_positive_denominator'] else 'unavailable','strict_n_status':'available' if nr['eligible_strict_n_denominator'] else ('historical_only' if nr['grade']=='N' else 'unavailable'),'checks':rows})

sources.extend([
 {'id':'GB-fixed011-cases','url':f'https://github.com/laadkke-arch/agentflow-open/blob/{SHA011}/docs/workstreams/research/AF-RES-011/CASES.json','accessed_at_utc':'2026-11-21','source_type':'frozen_research_artifact','title':'AF-RES-011 CASES assigned records','version_or_date':SHA011,'sections_read':'assigned IDs; T054 answers and constraints','confirmed':'기존 질문 요약·조건·실제 답 기록을 읽었다. T054의 실제 답3개는 특정 모델의 성공 보증보다 평가 절차·경험을 제시한다.','limits':'기존 코딩을 독립적으로 다시 검증한 것이 아니며 제품 직접 실행 자료가 아니다.','level':'D1','used_in':['Q2','Q3'],'body_read':True,'access_method':'git show','count_as_method_literature':False},
 {'id':'GB-fixed011-nearmiss','url':f'https://github.com/laadkke-arch/agentflow-open/blob/{SHA011}/docs/workstreams/research/AF-RES-011/evidence/near-misses.json','accessed_at_utc':'2026-11-21','source_type':'frozen_research_artifact','title':'AF-RES-011 near misses','version_or_date':SHA011,'sections_read':'NM05–NM19; qualified cases','confirmed':'과거 엄격 N과 후속 조건 때문에 제외된 NM11·NM16·NM17을 구별했다. N은 당시 조건·후보 범위가 붙은 사건이다.','limits':'현재 기능과 최초 질문판의 적합성을 자동으로 보증하지 않는다.','level':'D1','used_in':['Q3'],'body_read':True,'access_method':'git show','count_as_method_literature':False},
 {'id':'GB-fixed014-rules','url':f'https://github.com/laadkke-arch/agentflow-open/blob/{SHA014}/docs/workstreams/research/AF-RES-014/qrels/EXCLUSIONS.md','accessed_at_utc':'2026-11-21','source_type':'frozen_research_artifact','title':'AF-RES-014 exclusions','version_or_date':SHA014,'sections_read':'scope/unknown/defer rules; 클라이언트PC mapping','confirmed':'문서에 없는 기능을 불지원으로 추정하지 않으며 적용 범위·버전이 불명확하면 보류한다. 클라이언트PC라는 표기는 비교를 보류하도록 되어 있다.','limits':'모든 자연어 조건에 대한 자동 판정 규칙이 아니며 실제 공식 문서 대조가 필요하다.','level':'D1','used_in':['Q3'],'body_read':True,'access_method':'git show','count_as_method_literature':False},
])
for q,ref,secs,conf in [
 ('SX01','turn768670035view0;turn955930541view0','answers/comments L116–277','Laverna·Turtl·NixNote의 실제 답과 반박을 읽었다. 본문만으로 생긴 Laverna 긍정 착시는 댓글 API에서 저장 실패 정정을 확인해 해소했다.'),
 ('SX08','turn768670035view1','answers/comments, full displayed241 lines','두 실제 답과 원문 길이 대응·무제약 생성에 대한 질문자 반박을 읽었다. 사용·채택 양성 답은 확인되지 않았다.'),
 ('SXR05','turn768670035view2;turn955930541view1','answers/comments including FeSimpleArgs and parser revisions','FeSimpleArgs 답과 후속 댓글을 읽었다. 임의 옵션 조건의 추가 시점과2017/2019 picocli 상태를 구별했다.')]:
    sources.append({'id':'GB-thread-'+q,'url':inputs[q]['question_url_excluded_from_search'],'accessed_at_utc':OBSERVED,'source_type':'public_QA_thread','title':q+' answer and rebuttal evidence','version_or_date':'live current answers; original input separately verified','sections_read':secs,'confirmed':conf,'limits':'실제 답 정답의 관측 자료이며 후보 공식 기능 시험이 아니다. 이 URL은 실행 검색에서 제외한다.','level':'D1','used_in':['Q3'],'body_read':True,'web_refs':ref.split(';'),'count_as_method_literature':False})
    rev=inputs[q]['question_source']
    sources.append({'id':'GB-revision-'+q,'url':rev['url'],'accessed_at_utc':{'SX01':'2026-11-21T04:01:56.625741+00:00','SX08':'2026-11-21T04:01:58.818019+00:00','SXR05':'2026-11-21T04:01:56.305457+00:00'}[q],'source_type':'public_QA_original_revision','title':q+' original question revision','version_or_date':rev['revision_guid'],'sections_read':'first question title and body, transient only','confirmed':{'SX01':'공개 형식·앱 독립성·태그·플랫폼·편집 가능한 형식 요구를 최초판에서 확인했다.','SX08':'원문 순서·비슷한 단어 길이·문장부호·줄바꿈과 FOSS/Linux를 최초판에서 확인했다.','SXR05':'묶은 짧은 옵션·긴 옵션·--·공백·플랫폼 요구는 있지만 임의 옵션 이름 수용 조건은 최초판에 없다.'}[q],'limits':'본문 전문은 저장하지 않았다. 후속 수정판의 조건을 최초 입력으로 소급할 수 없다.','level':'D3-fetch','used_in':['Q2','Q3'],'body_read':True,'http_status':200,'question_sha256':inputs[q]['question_sha256'],'read_command':f'python docs/workstreams/research/AF-RES-018/questions/generate.py --emit {q}','count_as_method_literature':False})

API_ANSWERS='https://api.stackexchange.com/2.3/questions/35392;84072;26907/answers?site=softwarerecs&filter=withbody&pagesize=100'
API_COMMENTS='https://api.stackexchange.com/2.3/posts/84081;84073;35564;45082;38872;35551;35399;26910;27555/comments?site=softwarerecs&filter=withbody&pagesize=100'
for sid,url,title,confirmed in [
 ('GB-api-answers',API_ANSWERS,'Supplemental questions actual answers','공개 API가 반환한 답9개의 채택 여부와 후보 링크를 확인했다. SX01·SX08은 채택 답이 없고 FeSimpleArgs 답38872는 채택됐다.'),
 ('GB-api-comments',API_COMMENTS,'Supplemental answer comments','Laverna의 일시 긍정 댓글51286은51287에서 정정된다. SX08 반박103656·103657 및 SXR05 임의 옵션 조건 추가 댓글38049·38056·38060을 확인했다.'),
 ('GB-api-accepted','https://api.stackexchange.com/2.3/answers/38872?site=softwarerecs&filter=withbody','FeSimpleArgs accepted answer API','answer_id38872, question_id26907의 is_accepted=true를 확인했다.')]:
    sources.append({'id':sid,'url':url,'accessed_at_utc':'2026-11-21T04:07:45.424747+00:00' if sid=='GB-api-accepted' else OBSERVED,'source_type':'public_QA_API','title':title,'version_or_date':'live APIv2.3','sections_read':'returned answer fields / comment content; user identity omitted','confirmed':confirmed,'limits':'현재 공개 API에 남은 기록이다. 삭제된 기록 전체를 복원하지 못하며 채택은 제품의 현재 공식 기능 보증이 아니다.','level':'D3-fetch','used_in':['Q3'],'body_read':True,'http_status':200,'count_as_method_literature':False})

excluded=[
 {'id':'GB-excluded-ghostscript','url':'https://ghostscript.com/about.html','web_ref':'turn896216904view0','status':'InternalError','alternative':'https://ghostscript.readthedocs.io/en/latest/'},
 {'id':'GB-excluded-spring','url':'https://springrts.com/','web_ref':'turn896216904view2','status':'Timeout','alternative':'https://github.com/spring/spring'},
 {'id':'GB-excluded-authorea','url':None,'host':'authorea.com','requested_page':'homepage; exact requested URL not preserved in working note; retain web_ref','web_ref':'turn896216904view6','status':'403','alternative':None},
 {'id':'GB-excluded-autohotkey','url':None,'host':'autohotkey.com','requested_page':'homepage; exact requested URL not preserved in working note; retain web_ref','web_ref':'turn307696399view2','status':'403','alternative':'https://github.com/AutoHotkey/AutoHotkey'},
 {'id':'GB-excluded-fesimpleargs','url':'https://bitbucket.org/ccperkins/fesimpleargs','web_ref':'turn307696399view4','status':'opened; zero readable body lines','alternative':None},
 {'id':'GB-excluded-gnutr','url':None,'host':'www.gnu.org','requested_page':'GNU tr manual; exact requested URL not preserved in working note; retain web_ref','web_ref':'turn307696399view5','status':'Timeout','alternative':'Python str.translate used as unjudged auxiliary instead'},
 {'id':'GB-excluded-leftpad','url':'https://github.com/stevemao/left-pad','web_ref':'turn414639488view0','status':'DisabledError','alternative':'Lodash official docs used instead'},
 {'id':'GB-excluded-jcommander-comparison','url':None,'web_ref':'turn315691838search1','status':'competitor comparison search result; no own official negative proof','alternative':None},
]
for x in excluded:x.update(body_read=False,accessed_at_utc=OBSERVED,count_as_source=False,level='D0',limits='실패·snippet·본문 부재를 내용 증거로 계상하지 않는다.')

queries=[
 ('system2','site.jekyllrb.com static site no databases server side','정적 생성기 소개는 확인했으나 외부 조합까지 불가능하다는 명시 근거는 없어 N 보류'),
 ('system2','site.github.com nixnote2 local notebooks Evernote sync database','비공식 Evernote 클라이언트 정체성만 확인; 로컬 사용 불가능으로 일반화하지 않음'),
 ('system2','site.gnu.org getopt long options Java gnu getopt','최초판 조건에 맞는 파서의 공식 불지원 근거를 확정하지 못함'),
 ('system2','site.docs.oracle.com getopt parser long options','엄격 N을 확정할 공식 범위 증거를 확보하지 못함'),
 ('system1','site.jcommander.org "concatenated"','자기 공식 문서에서 명시적 묶은 짧은 옵션 불지원 확인 실패'),
 ('system1','site.jcommander.org "combined" "short"','자기 공식 문서의 부정 근거 확인 실패'),
 ('system1','site.github.com/cbeust/jcommander "-abc"','원문 최초판의 필수 조건 위반 확정 실패'),
 ('system2','"JCommander" "short options" "not"','경쟁 파서 비교는 직접 공식 문서의 대용으로 쓰지 않음'),
 ('system2','"JCommander" "combined" options','엄격 N 미확정'),
 ('system2','"JCommander" "grouped" options','엄격 N 미확정'),
]

def write(name,obj):
    (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

counts={'questions':len(questions),'check_rows':len(checks),'positive_eligible':sum(x['eligible_positive_denominator'] for x in checks),'strict_N_eligible':sum(x['eligible_strict_n_denominator'] for x in checks),'unrelated_eligible':sum(x['eligible_unrelated_denominator'] for x in checks),'historical_N_current_unverified':sum(x['judgment_status']=='historical_N_current_unverified' for x in checks),'unjudged_auxiliaries':sum(x['judgment_status']=='unjudged' for x in checks),'body_sources':len(sources),'official_body_sources':len(SOURCE_ROWS)}
write('checks-draft.json',{'status':'DRAFT_NOT_EXPERIMENT_RUN','prepared_by':'내부 별도 준비 작업자; 같은 모델 계열','observation_window_utc':OBSERVED,'source_shas':{'AF-RES-011':SHA011,'AF-RES-014':SHA014},'grade_semantics':'grade is separate from eligibility/status; unjudged0 is not confirmed irrelevant0; historical N is not automatically current eligible N','counts':counts,'questions':questions})
write('supplemental-answers.json',{'status':'worker_adjudication_from_actual_external_answers','rules_source_sha':SHA014,'answers':supplemental,'missing_positive':no_positive,'limits':['T054의 절차 답과 제품 실체 후보의 recall을 분리한다.','정답이 없는 질문에 새 검색 후보를 grade1로 만들지 않는다.','FeSimpleArgs 채택과 현행 공식 페이지의 접근 불가를 구별한다.']})
write('sources.json',{'recording_notes':['공식 문서 요약은 후보 범위 검증용이고 방법 문헌25편 분모에 넣지 않는다.','본문·사용자 이름·장문 인용을 보관하지 않는다.','정확한 개별 열람 초가 노출되지 않은 웹 도구 열람은 UTC 구간으로 기록한다.','git show로 읽은 고정 파일은 고정 SHA의 웹 주소와 접근 방법을 함께 남긴다.'],'sources':sources,'excluded':excluded})
write('SEARCH_LOG.json',{'task':'AF-RES-018 gold draft B; not A/P execution','query_count':len(queries),'queries':[{'id':f'GB-Q{i:02d}','engine':e,'query':q,'accessed_at_utc':OBSERVED,'result':r} for i,(e,q,r) in enumerate(queries,1)],'opened_documents':[{'source_id':s['id'],'url':s['url'],'web_refs':s.get('web_refs',[]),'accessed_at_utc':s['accessed_at_utc'],'body_read':s['body_read'],'http_status':s.get('http_status','web tool did not expose numeric HTTP status')} for s in sources],'excluded':excluded,'original_commands':[{'qid':q,'command':f'python docs/workstreams/research/AF-RES-018/questions/generate.py --emit {q}','result':'HTTP200; SHA256 verified; original body read transiently; no full body saved'} for q in ['SX01','SX08','SXR05']],'network_notes':'Web tool first public opens and failures are recorded here. Numeric anonymous executor probes, when possible, are separately recorded in NETWORK.json; do not treat a successful web read as an invented HTTP200.'})
write('VALIDATION.json',{'counts':counts,'checks':[{'name':'17 assigned questions only','passed':set(q['qid'] for q in questions)==set(IDS)},{'name':'exactly3 check rows per question','passed':all(len(q['checks'])==3 for q in questions)},{'name':'unique check IDs','passed':len({x['check_id'] for x in checks})==51},{'name':'unjudged positives excluded','passed':all(not x['eligible_positive_denominator'] for x in checks if x['check_id'] in ['SX01-POS','SX08-POS'])},{'name':'all no-must N slots excluded','passed':all(not near[q]['eligible_strict_n_denominator'] for q in ['T036','T046','T057','T058','T059'])},{'name':'SXR05 later-revision N excluded','passed':not near['SXR05']['eligible_strict_n_denominator']},{'name':'T040 scoped standard Lambda only','passed':'Managed Instances 제외' in near['T040']['name']},{'name':'strict N requires evidence and condition','passed':all(x['official_evidence'] and x['violated_condition'] for x in checks if x['eligible_strict_n_denominator'])}],'note':'Draft data integrity checks only. No candidate software executed; no A/P run; parent owns integration and commits.'})
print(json.dumps(counts,ensure_ascii=False))
