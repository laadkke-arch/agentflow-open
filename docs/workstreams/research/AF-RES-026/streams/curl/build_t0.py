"""Build the pre-follow-up curl packets from recorded public metadata.

No network and no follow-up input. Public originals remain at cited locations.
"""
from pathlib import Path
import json, hashlib, datetime, csv

P = Path(__file__).resolve().parent
META = json.loads((P / 'root-metadata.json').read_text())
DOCS = {r['id']: r for r in json.loads((P / 'provider-metadata.json').read_text())}
WIKI = json.loads((P / 'wiki-metadata.json').read_text())
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
PROTOCOL = 'cecbfb981b9a7ccfd59f7bc40a23445a19d020fa'

def req(kind, text, loc):
    return {'kind': kind, 'text': text, 'locator': loc}

def cand(cid, use, sid, version, status='historically_available'):
    return {'id': cid, 'use': use, 'source_id': sid,
            'url': WIKI['url'] if sid == 'C-W01' else DOCS[sid]['url'],
            'version': version, 'availability': status}

def short(sid):
    u = DOCS[sid]['url']
    for sha, tag in [('9e560d11aad028de74addc0d1edfefa5667884f4','curl-7_80_0'),
                     ('801bd5138ce31aa0d906fa4e2eabfc599d74e793','curl-7_81_0'),
                     ('8839c05fba1f8415eec17eff8ac60cc3a50eb51e','curl-7_55_1')]:
        u = u.replace(sha, tag)
    return u

DATA = [
dict(goal='브라우저의 요청 Cookie를 코드나 curl로 확인', inputs='쿠키 저장소를 비운 브라우저의 XHR/Fetch; 테스트 URL', outputs='Request Cookies', version='미상; 비교판 curl7.80.0', platform='브라우저/명령줄; OS 미상', actors='브라우저 확장과 XHR/Fetch가 요청; curl 대안 언급; 동기성 미상', requirements=[req('required','요청에 실린 쿠키를 얻음','L33–42'),req('unknown','브라우저가 실제 보낸 요청인가, curl 재현 요청인가','L41–42'),req('unnecessary','테스트에서 기존 브라우저 쿠키를 제거함; 쿠키사용 금지 아님','L39–40')], candidate_uses=[cand('A','curl 자신이 보내는 헤더를 -v로 관측','C-D02','7.80.0'),cand('B','브라우저 JS가 만든 요청을 그대로 얻는 curl 대체는 보류','C-D12','7.80.0','unsupported_for_JS_execution')], missing_variable='관측하려는 요청의 주체: 브라우저 원요청/curl 재현', question_utility='requires_answer_to_disambiguate', I='브라우저 원요청을 curl로 읽는 방법은 이 정보로 확정하기 어렵습니다. curl 자신이 보내는 요청 헤더는 -v로 볼 수 있습니다. '+short('C-D02'), C='curl 재현 요청이면 -v로 헤더를 확인할 수 있습니다. 브라우저가 JS로 만든 원요청이면 curl만으로 대체할 수 없어 보류합니다. '+short('C-D02')+' '+short('C-D12'), Q='확인하려는 쿠키는 브라우저가 실제 보낸 요청의 것인가요, curl이 재현해 보낸 요청의 것인가요?', initial_sufficient=False),
dict(goal='LAN 내부 Linux 서버의 공인 IP 확인', inputs='Linux 서버와 내부 LAN', outputs='공인 IP 주소', version='미상; 비교판 curl7.80.0', platform='Linux', actors='명령줄 curl과 외부 HTTP 응답자; 세부망 미상', requirements=[req('required','공인 IP를 알고 싶음','L35–36'),req('required','내부 LAN의 Linux 서버에서 실행','L35–36'),req('unknown','NAT/프록시와 주소군','본문 전체')], candidate_uses=[cand('A','외부 응답자가 관측한 주소를 HTTP 응답으로 조회; 서비스 주소 미정','C-D03','7.80.0','mechanism_only_endpoint_unverified'),cand('B','write-out local_ip는 해당 연결의 로컬 주소를 반환','C-D03','7.80.0')], missing_variable='외부 연결에 NAT를 거치는지', question_utility='does_not_change_robust_external_observer_route', I='local_ip는 연결의 로컬 주소여서 LAN 밖 공인 주소라는 보장은 없습니다. 공인 주소를 응답할 외부 서비스가 필요하며, 여기서는 그 서비스 검증을 보류합니다. '+short('C-D03'), C='NAT가 있으면 local_ip만으로 공인 주소를 알 수 없습니다. NAT가 없어도 프록시·주소군은 별도라, 외부 관측 응답과 비교해야 합니다. '+short('C-D03'), Q='그 서버의 외부 연결은 NAT를 거치나요?', initial_sufficient=True),
dict(goal='POST 후 서버처리 대기를 제외한 업로드 속도 해석', inputs='파일 업로드 POST; 응답 전에 서버 처리', outputs='첫 업로드 바이트부터 마지막 바이트까지의 속도/시간', version='OP curl7.55.1 명시', platform='미상', actors='curl 업로드와 POST 수신 서버의 후처리; 서버응답 후 완료', requirements=[req('required','실제 업로드 구간과 요청 완료시간을 구별','L33–39'),req('required','7.55.1의 progress meter 동작을 설명','L33–43'),req('preference','progress bar에서 같은 현상이 보이지 않는다고 보고; 숫자 속도 불필요라는 뜻 아님','L40–41')], candidate_uses=[cand('A','기본 meter의 전송시작 이후 경과시간 평균으로 해석','C-D09','7.55.1'),cand('B','progress bar로 진행량을 표시; 바이트구간 평균속도 대체는 아님','C-D10','7.55.1')], missing_variable='원하는 분모가 요청전체인지 바이트전송구간인지', question_utility='already_stated', I='7.55.1의 평균 업로드 속도는 업로드 바이트/시작 이후 경과시간입니다. 서버처리 대기를 뺀 속도라고 해석하면 안 됩니다. '+short('C-D09'), C='요청 경과시간 평균이면 기본 meter를 해석할 수 있습니다. 진행률만 원하면 progress bar가 가능하지만, 순수 업로드구간 속도는 별도 측정이 필요합니다. '+short('C-D09')+' '+short('C-D10'), Q='필요한 속도의 분모는 요청 전체 시간인가요, 첫 업로드 바이트부터 마지막 바이트까지인가요?', initial_sufficient=True),
dict(goal='명령줄 -d와 파일 -d @tmp.dat POST 차이 설명', inputs='URL-encoded JSON; 명령줄 성공; 임시파일 실패', outputs='같은 POST 데이터 전달', version='미상; 비교판 curl7.81.0', platform='Linux 명령줄, PHP 테스트서버', actors='Chrome XHR를 curl로 재현, 서버 PHP가 처리', requirements=[req('required','두 경로가 같은 데이터를 보내야 함','L38–48'),req('required','PHP trim으로 해결되지 않은 추가 문자 원인 확인','L46–51'),req('unknown','파일 실제바이트·생성법·정확한명령','본문 전체')], candidate_uses=[cand('A','-d @file은 CR/LF를 제거하여 POST','C-D04','7.81.0'),cand('B','--data-binary @file은 파일 바이트를 보존','C-D05','7.81.0')], missing_variable='파일 CR/LF도 전송 바이트로 보존해야 하는지', question_utility='changes_option_but_insufficient_for_diagnosis', I='-d @file은 CR/LF를 제거합니다. 파일·실제 요청 바이트가 없어 추가 문자 원인은 보류합니다. '+short('C-D04'), C='줄바꿈을 제거할 파일 입력이면 -d @file, 바이트를 그대로 보낼 입력이면 --data-binary @file입니다. 어느 쪽이든 추가 문자의 원인은 별도 확인이 필요합니다. '+short('C-D04')+' '+short('C-D05'), Q='임시파일의 CR/LF까지 원래 바이트 그대로 서버에 보내야 하나요?', initial_sufficient=False),
dict(goal='Content-Disposition의 경로 탈출 여부와 파일명 대체 처리', inputs='-OJ 요청, 서버 filename=/etc/passwd 가정', outputs='안전한 로컬 저장위치와 오류시 tempname', version='미상; 비교판 curl7.81.0', platform='실제OS 미상; Windows 경고 인용', actors='서버가 파일명 전달, curl이 로컬파일 생성', requirements=[req('required','서버가 임의 절대경로로 저장시킬 수 있는지 확인','L39–42'),req('preference','실패코드23 뒤 tempname 재시도를 고려','L43–45'),req('unknown','서버의 basename 보존이 필수인지','본문 전체')], candidate_uses=[cand('A','7.81.0 -OJ의 parse_filename이 슬래시/역슬래시 경로를 제거','C-D13','7.81.0'),cand('B','-o 고정 로컬파일로 서버 파일명 선택을 사용하지 않음','C-D11','7.81.0')], missing_variable='서버가 정한 basename을 보존해야 하는지', question_utility='changes_optional_use_not_existing_path_answer', I='7.81.0 구현은 서버 filename에서 슬래시·역슬래시 앞 경로를 버립니다. 다만 사용 중인 판과 오류23의 원인은 별도입니다. '+short('C-D13'), C='서버 basename이 필요하면 해당판 -OJ 경로제거를 확인하고, 필요 없으면 -o로 로컬이 이름을 정할 수 있습니다. '+short('C-D13')+' '+short('C-D11'), Q='서버가 Content-Disposition으로 준 파일의 basename을 그대로 보존해야 하나요?', initial_sufficient=True),
dict(goal='JSON 전송·작성 옵션 설계의 유용성 검토', inputs='이미 포맷된 JSON 또는 쉘 변수·JSON 부분값', outputs='JSON HTTP 요청; 따옴표 처리 부담 감소', version='새 기능 제안; root 전 wiki68fed966; 당시 릴리스7.81.0', platform='명령줄과 쉘; 특정OS 미상', actors='유지관리자 Daniel이 질문자; 사용자들이 용도/설계 피드백 제공 예정', requirements=[req('required','JSON 사용을 쉽게 하는 CLI 설계 검토','L37–58'),req('preference','기존JSON 전송 shortcut과 JSON본문구성 두아이디어','L49–52; wiki --json/--jp'),req('unnecessary','JSON 응답 특별처리는 제안하지 않음; 금지 아님','wiki JSON response'),req('unknown','JSON 생성까지 이번 기능의 필수범위인지','L49–58')], candidate_uses=[cand('A','제안 --json: 이미 만든 JSON을 -d와 Accept헤더로 전송','C-W01','68fed966feefd6024aece196fc1be105a08a949f','proposal_not_released'),cand('B','제안 --jp: 부분값에서 JSON본문 구성','C-W01','68fed966feefd6024aece196fc1be105a08a949f','proposal_not_released')], missing_variable='JSON본문 생성도 curl 내 필수범위인지', question_utility='clarifies_scope_but_no_usage_outcome', I='첫안은 완성된 JSON을 보내는 shortcut으로 범위를 한정할 수 있습니다. 이 문서는 출시기능이 아닌 제안이며 JSON 유효성은 검사하지 않습니다. '+WIKI['url'], C='완성된 JSON을 받으면 --json shortcut 안, 쉘의 부분값으로 본문까지 만들려면 --jp 안입니다. 둘 다 이 시점에는 제안입니다. '+WIKI['url'], Q='이번 범위에서 JSON 본문을 curl 안에서 생성하는 것까지 필수인가요?', initial_sufficient=False),
dict(goal='자주 쓰는 localhost URL의 타이핑 감소', inputs=':80/, :8080/path 같은 단축 입력 제안', outputs='http://localhost 접두를 갖는 실제 URL', version='새 CLI문법 제안; 비교판 curl7.81.0', platform='명령줄; OS 미상', actors='공급자/설계제안자인 Daniel이 피드백 질문자', requirements=[req('required','반복 URL 입력의 타이핑을 줄일 단일CLI기능 검토','L35–43'),req('preference','0주소 요령의 IPv4한정·hostname손실을 피함; 강제어 없음','L44–47'),req('unknown','추가 단축형 종류','L48–52'),req('unnecessary','라이브러리기능이 아니라 명령줄제안','L37')], candidate_uses=[cand('A','현재판에서 명시적 http://localhost URL 사용','C-D07','7.81.0'),cand('B','콜론 선행 단축 문법은 새 설계로 보류; 기존판 기능으로 승인하지 않음','C-D07','7.81.0','proposal_not_in_comparison_manual')], missing_variable='현행판 사용법인지 다음판 새문법 설계인지', question_utility='already_stated', I='이미 새 CLI문법 제안으로 읽힙니다. 7.81.0의 URL 규칙은 기준선이며, 제안 :port 문법이 구현됐다는 근거는 아닙니다. '+short('C-D07'), C='현행판 실행에는 명시적 http://localhost를 쓰고, 타이핑 단축이 목표라면 제안 문법의 구현·시험을 별도 보류합니다. '+short('C-D07'), Q='현재 출시판에서 실행할 사용법이 필요한가요, 다음판에 새 문법을 추가하려는 설계인가요?', initial_sufficient=True),
dict(goal='curl POST 성공과 Chrome 확장 Fetch404의 차이 확인', inputs='성공한 curl POST; Chrome확장 Fetch', outputs='브라우저에서도 같은 POST 성공', version='Chrome97 명시; curl미상', platform='Windows64bit Chrome97', actors='명령줄 curl과 Chrome확장 Fetch; 서버404 원인미상', requirements=[req('required','Chrome확장에서 요청이 작동','L33–43'),req('required','curl성공/Fetch404의 원인을 구별','L33–38'),req('preference','보안비활성 재시작을 시도했으나 실패; 보안해제 필수 아님','L39–43'),req('unknown','실제 Fetch URL·요청·오류응답','본문 전체')], candidate_uses=[], missing_variable='Fetch 실제최종 URL이 curl 성공URL과 같은지', question_utility='necessary_but_not_sufficient', I='curl 성공과 Chrome의 404만으로 원인을 정할 수 없습니다. 두 요청의 URL·헤더·본문과 서버응답이 없어 해결책 승인을 보류합니다.', C='실제 URL이 다르면 먼저 요청 대상을 맞춰 대조하고, 같다면 다른 요청조건을 더 확인해야 합니다. 어느 갈래도 현재는 해결책 승인 보류입니다.', Q='Fetch가 실제 요청한 최종 URL이 성공한 curl 요청의 URL과 완전히 같은가요?', initial_sufficient=False),
]

initial=[]; frozen=[]
for k,(m,d) in enumerate(zip(META,DATA),1):
    cid=f'C{k:02d}'
    rootloc=['L32–44','L32–41','L32–45','L34–56','L32–47','L32–59 + linked wiki','L32–52','L32–45'][k-1]
    author=['bruce','Turritopsis Dohrnii Teo En Ming','kifer lemet (signs Refik)','bruce','Paul Gilmartin','Daniel Stenberg','Daniel Stenberg','bruce'][k-1]
    r={'case_id':cid,'family':'C','title':m['title'],'root_url':m['url'],'root_locator':rootloc,
       'submitted_utc':m['submitted_utc'],'received_utc':m['received_utc'],
       'timestamp_kind':'Date header UTC; independent Hypermail isoreceived server field',
       'author':author,'author_role':'maintainer_as_questioner' if k in [6,7] else 'requester',
       'original_version':{'identifier':m['message_id_display'],'status':'confirmed',
          'evidence':'Official individual mail artifact: Message-ID, sent/isoreceived and complete root body; reply chronology checked after freeze.',
          'url':m['url'],'hash_method':'SHA256 bytes between exact HTML body start/end comments',
          'body_sha256':m['body_section_sha256'],'full_body_read':True,
          'limitation':'Official archived rendering; independent cryptographic signed raw MIME not obtained. Received UTC interpreted from archive isoreceived and cross-checked sent timezone.'},
       'first_reply_utc':None,'first_reply_status':'not_read_before_freeze',
       **{a:b for a,b in d.items() if a not in ['I','C','Q']},
       'frozen_question':d['Q'],'exposure':{'followup_body':False,'index_titles_and_reply_existence':True,'scope':'Monthly January/February indexes and root navigation titles; no reply body. Wiki history dates only, then T0 revision body.'},
       'sources':[f'C-R{k:02d}']+list(dict.fromkeys(x['source_id'] for x in d['candidate_uses'])),
       'preference_as_required_error':False,'unnecessary_as_prohibited_error':False}
    for j,q in enumerate(r['requirements'],1):q.update({'id':f'{cid}-R{j}','url':m['url'] if 'wiki' not in q['locator'] else WIKI['url']})
    if k==6:r['linked_attachment']=WIKI
    inp={'root_body_sha256':m['body_section_sha256'],'attachment_sha256':WIKI['body_sha256'] if k==6 else None,
         'candidate_sources':[{s: DOCS[s]['blob_sha'] if s in DOCS else WIKI['revision']} for s in r['sources'][1:]]}
    r['input_sha256']=hashlib.sha256(json.dumps(inp,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    r['input_hash_definition']='SHA256 of canonical JSON of root body hash, optional attachment body hash and candidate source Git blob/revision IDs'
    initial.append(r)
    f={'case_id':cid,'input_sha256':r['input_sha256'],'precommit_base_sha':PROTOCOL,
       'I':d['I'],'C':d['C'],'Q':d['Q'],'candidate_ids':[x['id'] for x in d['candidate_uses']],
       'candidate_source_ids':list(dict.fromkeys(x['source_id'] for x in d['candidate_uses'])),
       'created_utc':NOW,'reader':'/root/curl; same writer for later T1; no independent recoder',
       'followups_read_before_freeze':False,'link_policy':'Message uses readable release tag; source ledger binds exact full commit. Wiki uses exact revision.'}
    assert all(len(f[s])<=300 for s in ['I','C','Q']), (cid,{s:len(f[s]) for s in ['I','C','Q']})
    frozen.append(f)

for name,data in [('initial.jsonl',initial),('frozen-responses.jsonl',frozen)]:
    (P/name).write_text(''.join(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n' for x in data))

sources=[]
for k,r in enumerate(initial,1):
    sources.append({'id':f'C-R{k:02d}','related_q':['Q1','Q2','Q3','Q4','Q5','Q6','Q8'],'case_ids':[r['case_id']],
      'url':r['root_url'],'published_or_revised':r['submitted_utc'],'fixed_version':r['original_version']['identifier'],
      'checked_utc':META[k-1]['checked_utc'],'read_locations':r['root_locator']+'; HTML metadata id/isoreceived/isosent and body boundaries',
      'observed':r['goal']+'; '+r['inputs']+' → '+r['outputs'],
      'limitations':'후속 본문은 봉인 전 미열람. 메일의 공개 동일발신자만 확인하며 실명 동일성/현재 운영성과는 미확인. 서버 보존판이지만 signed raw MIME은 미확보.',
      'producer':r['author']+' via official curl-users archive','lineage':'thread:'+META[k-1]['message_id_display'],
      'count_in_minimum':True,'count_reason':'고유 원 요청/대화 1건; 같은 스레드 답글은 추가 산입하지 않음','kind':'conversation'})

doc_notes={
'C-D01':(['C01'],'whole option (L11–39)','쿠키파일/문자열을 보내며 cookie engine을 켜는 옵션; 브라우저 원요청 읽기는 아니다','실제 브라우저 쿠키나 JS 실행을 확인하지 않음'),
'C-D02':(['C01'],'L10–23','verbose의 >는 curl이 보낸 헤더, <는 수신 헤더','브라우저가 보낸 요청과 동일하다고 보증하지 않음'),
'C-D03':(['C02'],'local_ip, remote_ip, time_total entries','local_ip는 연결 로컬끝, remote_ip는 상대 끝; 공인IP 반사서비스를 제공하지 않음','NAT/프록시 실측 또는 외부주소서비스 당시 동작은 미검증'),
'C-D04':(['C04','C06'],'L14–34','-d는 form content type; @file에서 CR/LF 제거','OP 실제파일·추가바이트 원인은 미확인'),
'C-D05':(['C04'],'L10–23','--data-binary는 바이트와 줄바꿈 보존; 기본content type 설명','원데이터가 그대로인지와 서버의 역해석은 별도'),
'C-D06':(['C05'],'L10–24','-OJ 서버파일명; 기존파일 덮어쓰기 오류; Windows 경고','경로제거는 이 짧은 문서만으로 보이지 않아 구현을 별도 읽음'),
'C-D07':(['C07'],'L9–23','URL 스킴 생략의 추정규칙과 명시URL 기준','제안된 :port 문법이 이미 구현됐다는 증거가 아님'),
'C-D08':(['C06'],'L13–47','-H가 custom HTTP헤더를 추가/대체','JSON생성/유효성검사 기능과 별개'),
'C-D09':(['C03'],'Curl_pgrsUpdate L375–394, L560–570','7.55.1은 시작 이후시간으로 업로드 평균속도를 계산해 meter 표시','정적 구현 판독이며 실제 OP업로드 실행/측정 아님'),
'C-D10':(['C03'],'whole option L5–11','progress bar는 진행량/퍼센트 출력','바이트전송만의 속도측정 대안으로 승인할 수 없음'),
'C-D11':(['C05'],'L13–43','-o로 로컬이 출력파일명을 지정','안전한 디렉터리·실제권한·재시도정책은 확인되지 않음'),
'C-D12':(['C01','C08'],'FAQ3.14 L602–624;4.14 L959–975','curl은 JS실행/브라우저식 모든리다이렉트를 수행하지 않음','Chrome Fetch404의 원인을 직접 입증하지 않음'),
'C-D13':(['C05'],'parse_filename L219–289; header callback L125–180','서버파일명에서 / 및 역슬래시 경로를 제거하고 파일생성으로 전달','7.81.0 정적 코드; OP판 미상, 전체보안 보증 아님'),
'C-D14':(['C07'],'whole option L9–17','스킴 없는URL에 기본프로토콜 설정가능','colon shortcut 또는 hostname대체와 다름'),
}
for sid,d in DOCS.items():
    cases,loc,obs,limit=doc_notes[sid]
    u=d['url']; ver='7.80.0' if '9e560d' in u else ('7.55.1' if '8839c0' in u else '7.81.0')
    date={'7.80.0':'2021-11-10T06:33:35Z','7.55.1':'2017-08-14T06:04:32Z','7.81.0':'2022-01-05T07:48:46Z'}[ver]
    sources.append({'id':sid,'related_q':['Q2','Q3','Q5'],'case_ids':cases,'url':u,
      'published_or_revised':date+' (release tag timestamp, not file authorship)','fixed_version':ver+'; blob '+d['blob_sha'],
      'checked_utc':NOW,'read_locations':loc,'observed':obs,'limitations':limit,
      'producer':'curl project','lineage':'curl/curl:'+u.split('/blob/')[1].split('/',1)[1],
      'count_in_minimum':True,'count_reason':'고유 공급자 원 파일; 같은파일 반복절/태그는 중복 산입하지 않음','kind':'provider_source'})
sources.append({'id':'C-W01','related_q':['Q1','Q2','Q3','Q5'],'case_ids':['C06'],'url':WIKI['url'],
 'published_or_revised':WIKI['revision_date'],'fixed_version':WIKI['revision'],'checked_utc':NOW,
 'read_locations':'full wiki body: --json, --jp, examples, JSON response; history datetime',
 'observed':'T0 전15분45초 수정판: 기완성JSON shortcut과 JSON part생성을 구별. 당시 --json은 -d와 Accept를 뜻하고 검증 없음. 응답 특별처리는 제외.',
 'limitations':'질문자가 직접 작성한 제안의 첨부이므로 공급자 독립 근거나 실행기능이 아님. 질문 본문과 같은 사건계보로 최소수 중복산입 제외.',
 'producer':'Daniel Stenberg/curl wiki','lineage':'C-R06 linked proposal attachment','count_in_minimum':False,'count_reason':'동일 요청의 연결첨부; 독립 사건 아님','kind':'linked_t0_attachment'})
sources.extend([
 {'id':'C-L01','related_q':['Q1'],'case_ids':[x['case_id'] for x in initial],'url':'https://curl.se/mail/archive-2022-01/date.html','published_or_revised':'2022-01-01..2022-01-30','fixed_version':'68-message month archive','checked_utc':NOW,'read_locations':'whole date listing; thread view root hierarchy','observed':'68개목록,67개를8건상한까지 심사; root8포함,주제외3,답장56;상한뒤공지1','limitations':'현재 재생성된 원장; 모든 메일의본문을 읽었다는 뜻 아님. 삭제된메일의존재는 원장만으로 알수없음','producer':'curl official Hypermail','lineage':'curl-users January2022','count_in_minimum':False,'count_reason':'모집원장; 개별대화와중복','kind':'sampling_ledger'},
 {'id':'C-L02','related_q':['Q1'],'case_ids':[],'url':'https://curl.se/mail/archive-2022-02/','published_or_revised':'2022-02-01..2022-02-28','fixed_version':'59-message month archive','checked_utc':NOW,'read_locations':'index titles only','observed':'Jan 적격범위해석 확정 전 다음월 원장제목을 열었음; 표본추가없음','limitations':'후속본문없음; 답존재와제목만 노출','producer':'curl official Hypermail','lineage':'curl-users February2022','count_in_minimum':False,'count_reason':'탐색원장','kind':'exploration'},
 {'id':'C-X01','related_q':['Q1'],'case_ids':[x['case_id'] for x in initial],'url':'https://lists.haxx.se/pipermail/curl-users/2022-January.txt.gz','published_or_revised':'미확인','fixed_version':'not obtained','checked_utc':NOW,'read_locations':'HTTP response type; official raw .eml/.txt alternatives and curl-www API path','observed':'gz경로는text/html을 반환;개별0002.eml/.txt는404;curl-www내메일경로404','limitations':'raw MIME대체확보 실패; 원문산입하지 않음','producer':'curl/list archive routes','lineage':'same official root mail fallback','count_in_minimum':False,'count_reason':'접근/형식실패','kind':'access_failure'}
])
(P/'sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')

summary={'stage':'T0 only; followup bodies unopened','protocol_commit':PROTOCOL,'created_utc':NOW,
 'cases':len(initial),'strategies':len(frozen)*3,'original_message_id_and_server_timestamp':len(initial),
 'provider_distinct_files':len(DOCS),'conversation_distinct':8,
 'response_lengths':{r['case_id']:{s:len(r[s]) for s in ['I','C','Q']} for r in frozen},
 'file_sha256':{n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ['initial.jsonl','frozen-responses.jsonl','frame.csv','sources.json','root-metadata.json','wiki-metadata.json']}}
(P/'t0-receipt.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ['file_sha256']},ensure_ascii=False))
