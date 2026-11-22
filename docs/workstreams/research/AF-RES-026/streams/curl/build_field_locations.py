"""Post-seal field-location supplement. Reads, never changes, initial.jsonl."""
from pathlib import Path
import json, datetime
P=Path(__file__).resolve().parent
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
xs=list(map(json.loads,(P/'initial.jsonl').read_text().splitlines()))
# Per field: exact source location, nature, qualification.
D={
'C01':{
'goal':('L33–34, L41–42','explicit','브라우저에 표시된 Request cookies를 코드/test app/curl에서 얻으려는 목적.'),
'inputs':('L35–40, L43','explicit','JS extension, XHR/Fetch, browser cookie store 비움, test URL. 쿠키 삭제는 테스트 상태이며 전송 금지 아님.'),
'outputs':('L33–34, L38, L41–42','explicit','Request Cookies. response Set-Cookie나 curl 자체 cookiejar로 바꿔 읽지 않음.'),
'version':('본문 전체 L32–44 점검','unknown','사용자 curl/browser 버전 없음. 비교판7.80.0은 연구자가 고정한 C-D02/C-D12의 판.'),
'platform':('L36–38, L41–42; 본문 전체 L32–44','explicit_and_unknown','브라우저 확장/test app/명령줄은 명시, OS는 미상.'),
'actors':('L36–42','explicit_and_unknown','브라우저 확장이 XHR/Fetch 요청. curl은 획득 수단 후보. 동기/비동기 실행·await 주체는 미기재; XHR/Fetch라는 이름만으로 확정하지 않음.')},
'C02':{
'goal':('L32–36','explicit','내부 LAN Linux 서버의 public IP를 curl로 얻고 싶다는 문장.'),
'inputs':('L35–36','explicit','Linux 서버와 내부 LAN. NAT/프록시/주소군 값 없음.'),
'outputs':('L35–36','explicit','public IP address. reachable inbound address인지 external observer address인지는 원문에 세분하지 않음.'),
'version':('본문 전체 L32–41 점검','unknown','curl 버전 미기재. 7.80.0 비교판은 C-D03의 연구 선택.'),
'platform':('L33, L35–36','explicit','Linux 명시.'),
'actors':('L35–36; 본문 전체 L32–41 점검','researcher_interpretation_and_unknown','curl/Linux server는 명시. initial의 외부 HTTP 응답자는 원글 사실이 아니라 외부관측 후보의 연구자 해석. 동기/비동기·네트워크 세부 미상.')},
'C03':{
'goal':('L34–43','explicit','왜 meter가 요청완료 시간으로 업로드 속도를 계산하는지, bug인지 다른 논리인지 질문.'),
'inputs':('L33, L37–39','explicit','7.55.1 파일 업로드 POST 및 업로드 결과의 서버 후처리.'),
'outputs':('L34–43','researcher_interpretation','원문이 첫~마지막 byte 기간과 요청완료기간을 비교. initial의 속도/시간 출력은 관심 구간 요약이지 새 기능을 반드시 구현하라는 명시 요구가 아님.'),
'version':('L33','explicit','curl7.55.1 직접 명시. 비교 코드 C-D09/10과 같은 판.'),
'platform':('본문 전체 L32–45 점검','unknown','OS/platform 미기재.'),
'actors':('L33–39','explicit_and_unknown','curl 업로드→서버가 업로드 결과 작업→반환이라는 순서 명시. 클라이언트 await/비동기 인터페이스와 서버 내부 비동기성은 미상.')},
'C04':{
'goal':('L35–46','explicit','명령줄 -d와 파일 -d @tmp.dat에서 추가 문자가 생기는 차이 질문.'),
'inputs':('L35–42','explicit','Chrome extension XHR POST packet, 명령줄 inline -d, 복사한 임시파일, URL/JSON encoded 배열.'),
'outputs':('L38–40','researcher_interpretation','same postData를 복사했다는 대비에서 같은 POST 바이트/결과 기대를 읽음. 바이트 동등성은 아직 검증되지 않음.'),
'version':('본문 전체 L32–47 점검','unknown','curl/PHP/Chrome 버전 없음. 7.81.0은 C-D04/05 연구 비교판.'),
'platform':('L35–37, L43–44','explicit','Chrome extension, Linux cmdline, PHP test server 명시.'),
'actors':('L35–44','explicit_and_unknown','Chrome XHR와 curl 재현, PHP 처리. 동기/비동기 실행 세부는 미기재.')},
'C05':{
'goal':('L39–45','explicit','서버 제공 절대경로가 저장위치를 바꾸는지와 -OJ 기능을 검출/대체하는 방안 질문.'),
'inputs':('L41, L44–45','explicit','악성 filename=/etc/passwd 가정과 curl -OJ, 오류23 후 -o tempname 제안.'),
'outputs':('L42–45','explicit_and_researcher_interpretation','현재 디렉터리 저장 여부는 명시. 안전한 저장이라는 표현은 이 제한된 경로질문의 연구 요약이며 모든 보안을 보증하지 않음. tempname은 검토 중 대안.'),
'version':('본문 전체 L32–47 점검','unknown','실제 curl판 미상. 7.81.0 C-D13/11은 비교판이고 사용판과 같다고 간주하지 않음.'),
'platform':('L35–39; 본문 전체 L32–47','unknown','Windows 경고와 PATH 언급은 있으나 실제 OS는 확정 불가.'),
'actors':('L39–45','explicit_and_unknown','서버가 Content-Disposition을 제공하고 curl이 로컬 output을 선택. 실행 동기성은 미상; 코드 순차 예시는 시험 제안이지 관측 실행 아님.')},
'C06':{
'goal':('L46–59','explicit','혼자 설계하기 적합하지 않다고 밝히며 JSON 옵션의 유용성/필요조건 피드백 요청.'),
'inputs':('L42–45, L49–52; linked wiki revision 68fed966 --json 및 --jp 절','explicit','준비 JSON과 shell 변수/부분값 두 입력 방식. 당시 linked wiki만 사용.'),
'outputs':('L43–45, L49–52; linked wiki --json/--jp/JSON response 절','explicit_and_researcher_interpretation','전송 JSON 본문과 quoting 부담 감소. 사용자 실제 성공 출력은 아직 없음.'),
'version':('L33–36, L49–55; linked wiki revision 68fed966feefd6024aece196fc1be105a08a949f','explicit_and_unknown','새 제안/갱신 wiki라고 명시. wiki commit은 root 15분45초 전. 사용자 현재 curl판은 미상; 당시 연구 비교 릴리스7.81.0이며 --json 출시 기능으로 취급하지 않음.'),
'platform':('L36, L43–45, L49–52','explicit_and_unknown','CLI와 shell 명시; 특정 OS 없음.'),
'actors':('L30, L46–59; wiki author metadata','explicit_and_researcher_interpretation','Daniel은 원 질문자/설계자. 공급자 역할은 curl 공식 제안 및 wiki 계보의 연구자 역할 코딩. 응답 예정 사용자와 실제 후속 발화자는 구분. 동기/비동기 전송 세부는 미상.')},
'C07':{
'goal':('L35–37','explicit','반복 URL의 keystrokes 감소가 목적이라고 명시.'),
'inputs':('L38–43','explicit','콜론 선행 :80/, :8080/index.html, :/search.cgi 형태 제안.'),
'outputs':('L38–40, L48–50','explicit','http://localhost 접두를 붙여 사용 URL로 변환하는 설계.'),
'version':('제목 L24, L33–38, L46–50','explicit_and_unknown','PROPOSAL/추가할 CLI 기능임이 명시. 실행 중 curl판 없음;7.81.0은 C-D07 비교판.'),
'platform':('L35–37, L50','explicit_and_unknown','명령줄 도구만 대상. OS 미상.'),
'actors':('L30, L33–37','explicit_and_researcher_interpretation','Daniel이 타인의 제안을 가져와 설계 피드백을 요청. 공급자 겸 질문자는 역할 코딩. 동기/비동기 주체는 미기재.')},
'C08':{
'goal':('L33–43','explicit','curl POST는 되는데 Chrome extension Fetch가404인 차이를 해결하려는 질문.'),
'inputs':('L33–42','explicit','성공한 cmdline curl POST, 새 Chrome extension Fetch, 보안비활성 재시작 실패. 실제 URL/headers/body 미기재.'),
'outputs':('L35–43','researcher_interpretation','브라우저에서도 성공 기대를 연구자가 요약; 특정 성공 응답 body/코드는 미상.'),
'version':('L45; 본문 전체 L32–45 점검','explicit_and_unknown','Chrome97 명시; curl 버전 미기재.'),
'platform':('L45','explicit','Windows64bit Chrome97 명시.'),
'actors':('L33–42','explicit_and_unknown','명령줄 curl, Chrome extension Fetch, 응답404. JS await/서비스 worker/서버 내부 동기성은 미기재. 보안 원인이라는 설명은 OP가 읽은 자료의 주장으로 미검증.')},
}
rows=[]
for x in xs:
  cid=x['case_id']; fields={}
  for k,(loc,nature,note) in D[cid].items():
    fields[k]={'sealed_value':x[k],'url':x['root_url'],'source_id':'C-R'+cid[1:],'locator':loc,'value_nature':nature,'note':note}
    if cid=='C06' and 'wiki' in loc:
      fields[k]['linked_T0_source']={'source_id':'C-W01','url':'https://github.com/curl/curl/wiki/JSON/68fed966feefd6024aece196fc1be105a08a949f','locator':loc.split('wiki')[-1]}
  rows.append({'case_id':cid,'created_utc':NOW,'timing':'post-seal locator supplement; only T0 material used','initial_unchanged':True,'fields':fields,'requirements_existing_locations':[{'condition_id':r['id'],'url':r['url'],'sealed_locator':r['locator']} for r in x['requirements']], 'source_line_system':'web reader rendered L-lines; stable short text anchors and Message-ID also identify original; HTML line numbering can differ'})
(P/'field-locations.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
correction=[{'case_id':'C02','field':'actors','type':'provenance_clarification','sealed_value':next(x['actors'] for x in xs if x['case_id']=='C02'),'corrected_attribution':'외부 HTTP 응답자는 원 작성자가 명시한 주체가 아니라 frozen 외부관측 후보의 연구자 해석','url':'https://curl.se/mail/archive-2022-01/0007.html','locator':'L35–36','impact':'원 질문자가 외부 HTTP 서비스를 이미 선택했다고 코딩하지 않음; NAT/주소군은 그대로 미상'},
 {'case_id':'C04','field':'requirements.C04-R2.locator','type':'locator_correction','sealed_value':'L46–51','corrected_value':'L40, L43–44','url':'https://curl.se/mail/archive-2022-01/0027.html','reason':'현재 web reader에서 추가 문자·PHP trim 위치는 L40/L43–44. sealed L46–51은 마무리/서명으로 부정확. 본문 주장 자체는 수정하지 않음'},
 {'case_id':'C03','field':'outputs','type':'interpretation_boundary','sealed_value':next(x['outputs'] for x in xs if x['case_id']=='C03'),'corrected_attribution':'관심 있는 시간 구간의 연구자 요약. 원문은 bug/logic 설명 질문이며 새로운 속도 출력 기능의 구현을 필수로 요구했다고 해석하지 않음','url':'https://curl.se/mail/archive-2022-01/0024.html','locator':'L34–43','impact':'원래 설명 목표에 I가 충분하다는 판단 범위를 명확화'}]
(P/'field-corrections.json').write_text(json.dumps(correction,ensure_ascii=False,indent=2)+'\n')
print(len(rows),'field-location rows; ',len(correction),'separate corrections')
