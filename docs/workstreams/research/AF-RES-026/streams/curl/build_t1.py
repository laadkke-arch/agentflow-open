"""Assemble T1 coding from directly read artifacts; never edits sealed T0."""
from pathlib import Path
import json, csv, hashlib, datetime, urllib.parse
P=Path(__file__).resolve().parent
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
SEAL='68fc97fadceb46f9945a71fcc53730e29f6c62bf'
def dump(name,obj): (P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def csvout(name,rows):
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with (P/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
def dt(x): return datetime.datetime.fromisoformat(x.replace('Z','+00:00'))
def iso(x): return datetime.datetime.strptime(x,'%Y%m%d%H%M%S').replace(tzinfo=datetime.timezone.utc).isoformat().replace('+00:00','Z') if x else None
def hours(a,b): return round((dt(b)-dt(a)).total_seconds()/3600,6)
def U(n,m='01'): return f'https://curl.se/mail/archive-2022-{m}/{n}.html'
initial={x['case_id']:x for x in map(json.loads,(P/'initial.jsonl').read_text().splitlines())}
frozen={x['case_id']:x for x in map(json.loads,(P/'frozen-responses.jsonl').read_text().splitlines())}
roots={x['url']:x for x in json.loads((P/'root-metadata.json').read_text())}
meta={x['url']:x for x in json.loads((P/'t1-message-metadata.json').read_text())}
source0={x['id']:x for x in json.loads((P/'sources.json').read_text())}
sealed_files=['initial.jsonl','frozen-responses.jsonl','frame.csv','sources.json','root-metadata.json','provider-metadata.json','wiki-metadata.json','build_t0.py','notes.md','t0-receipt.json']
sealed_hashes={x:hashlib.sha256((P/x).read_bytes()).hexdigest() for x in sealed_files}

# Tuples: case, classification relative to frozen variable, role, observation.
JAN={
'0005':('C01','third_party','responder','브라우저 Copy as cURL, 쿠키 export, DevTools Protocol, headless를 조건별로 제시. 봉인 변수는 묻지 않음.'),
'0006':('C01','author_existing_fact','original_author','curl -c로 빈 cookiejar를 얻은 시도를 밝히고 XHR/Fetch가 만든 브라우저 쿠키 관측 목적을 반복. 성공 보고 없음.'),
'0008':('C02','third_party','maintainer_responder','NAT의 전형적 상황을 설명하고 외부 서비스 ip.me 예시를 제시. 작성자 NAT 여부를 확인한 것은 아님.'),
'0009':('C02','third_party','responder','외부 IP 관측과 접속 가능한 호스트라는 목적을 나누고 외부 서비스·Dynamic DNS를 제시. IPv4/IPv6·JS 서비스 제한 설명.'),
'0062':('C02','no_answer','original_author','Daniel에게 감사만 표함. NAT·명령 실행·주소 결과 없음.'),
'0063':('C02','no_answer','original_author','Timothe에게 감사만 표함. NAT·명령 실행·주소 결과 없음.'),
'0064':('C02','third_party','responder','IP 서비스 예시 및 네트워크에 따른 접근 제한·fallback을 제안. 원 작성자 환경값이 아님.'),
'0065':('C02','third_party','service_provider_responder','자신이 운영하는 IP 서비스의 IPv4/IPv6·HTTPS 조건을 설명. 원 작성자 실행 없음.'),
'0026':('C03','third_party','maintainer_responder','업로드/다운로드 별도 타이머가 없고 요청 전체 timer를 쓰므로 서버처리 지연이 평균을 낮춤을 확인. 추가 사실 질문 없음.'),
'0028':('C04','third_party','responder','od 등으로 실제 추가 문자를 특정할 수 있는지 묻고 줄바꿈을 추측. CR/LF 보존 요구에 대한 작성자 값이 아님.'),
'0033':('C05','third_party','maintainer_responder','서버 경로를 제거하고 현재 디렉터리/--output-dir에 저장함을 답함. Content-Disposition이 없으면 -O가 작동하여 제시한 오류23 분기가 검출법이 아님을 설명.'),
'0037':('C05','author_existing_fact','original_author','경로 설명을 수용하며 빈 임시 디렉터리·위험 symlink 없음·적절한 이름이면 move/rename하는 기존 workflow를 밝힘. 답을 받은 뒤 새 실행했다는 보고는 없음.'),
'0038':('C05','third_party','maintainer_responder','질문 때문에 man page의 경로제거와 저장위치 설명을 수정했다고 보고하고 문서 링크를 줌.'),
'0044':('C06','third_party','responder','좋은 생각으로 의견을 바꿨다고 말함. 원 작성자 요구나 사용 결과가 아님.'),
'0045':('C06','third_party','responder','JSON 지원을 curl 위의 별도 도구로 격리하자는 반대 설계 의견.'),
'0046':('C06','third_party','responder_user','자신은 jq로 JSON 구성·응답 분석 후 curl 전송하는 실제 스크립트를 제시. 원 질문자 채택 사건과 별개.'),
'0047':('C06','third_party','responder','jq를 companion tool로 안내하자는 의견. 별도 도구 복잡성 관점.'),
'0048':('C06','new_requirement','third_party_proposer','보내기 중심 원안에 응답 parsing·JSON Pointer/Path까지 추가하자는 제안. 원 질문자의 T0 필수 조건으로 소급하지 않음.'),
'0049':('C06','author_existing_fact','original_author_maintainer','이미 -F로 POST 본문 구성을 돕고 있다는 비교로 내장 기능 아이디어를 방어. 생성이 이번 필수범위라는 yes/no 답은 아님.'),
'0050':('C06','third_party','responder','별도 curlson 또는 jq면 충분하다는 의견. digest 인용으로 연결되고 In-Reply-To 링크는 없음.'),
'0051':('C06','author_existing_fact','original_author_maintainer','기존 -d 다중인자·-F·data-urlencode의 본문 구성 선례를 들음. 원래 필수범위 답은 없음.'),
'0052':('C06','third_party','responder_user','자신의 API 테스트 shell history를 근거로 준비된 JSON+헤더 shortcut을 지지하고 중첩 JSON 구성 복잡성을 반례로 제시.'),
'0053':('C06','third_party','responder','반대의 이유가 미학인지 실용 문제인지 묻고 낯선 환경에서 별도 도구 부담을 설명. 원 작성자 조건 확인 질문은 아님.'),
'0054':('C06','third_party','responder','JSON 파일/stdin과 header shortcut을 지지하고 pipeline 편의를 제안.'),
'0057':('C06','third_party','responder_user','자신의 HTTP status 확인 후 jq 분석이라는 2단계 사용을 제시. 원 질문자 요구로 옮기지 않음.'),
'0059':('C06','new_requirement','third_party_proposer','응답 JSON을 HTTP metadata와 감싸는 추가 설계 제안. T0에 불필요로 적힌 응답 처리를 필수로 소급하면 두 원안 모두 부적합해짐.'),
'0060':('C06','no_answer','original_author_maintainer','--json 감을 보기 위해 PR8314를 만들었다고 보고. 생성 필수성의 기존 사실은 답하지 않았고, 이는 T0 이후 개발행동이다.'),
'0056':('C07','third_party','responder','colon shortcut은 스크립트 읽기 인지부담이 있다는 반대 의견.'),
'0058':('C07','third_party','responder','localhost 기능의 대상 사용자 관련성과 빈 hostname 변수가 조용히 localhost로 연결되는 위험을 물음.'),
'0061':('C07','author_existing_fact','original_author_maintainer','개발자 사용자를 중요한 대상으로 제시하고, 제안을 시험 중이며 구현 확정이 아님을 재확인. 빈 변수와 0 주소의 기존 동작을 비교.'),
}
FEB={
'0008':('C06','no_answer','original_author_maintainer','--json이 반영됐다고 알리고 jo→curl→jq 사용 예시와 자신의 글을 연결. 실제 외부 사용자 채택 보고가 아닌 공급자 구현 보고.'),
'0009':('C06','third_party','responder','완전한 JSON 두 개를 단순 연결하면 invalid JSON이 된다는 반례와 이유 질문.'),
'0010':('C06','no_answer','original_author_maintainer','다중 --json에서 덮어쓰기보다 연결을 선택한 개발 판단 설명. T0 필수범위 답으로 사용하지 않음.'),
'0011':('C06','new_requirement','third_party_proposer','각 JSON을 배열 요소로 만들자는 새로운 의미론 제안.'),
'0012':('C06','no_answer','original_author_maintainer','--json에서 parsing 복잡성을 원치 않았고 가능한 미래 --jp로 남긴다고 설명. 구현 이후 선택의 설명이며 T0 필수성 회수가 아님.'),
'0013':('C06','third_party','responder','배열 구성을 단순 문자열 연결로 할 수 있다고 반론.'),
'0014':('C06','third_party','responder_user','기존 서비스를 소비하는 --json 사용자에게 자동 배열화가 유용한지 반론. 기존 API에 맞춰야 한다는 소비자 관점이며 원 작성자 요구 아님.'),
'0024':('C05','new_requirement','same_public_author_new_root','별도 root에서 확정 filename을 time-cond와 dump-header에 활용할 방법을 물음. January root와 명시 연결 없음; 30일 밖의 보조 비교만.'),
'0025':('C05','third_party','responder','write-out filename_effective는 가능하지만 다른 옵션에 그 변수를 바로 쓰지는 못한다고 답함. 별도 February root의 답.'),
'0026':('C05','author_existing_fact','same_public_author_new_root','filename_effective가 다운로드 실패 때도 보인다는 관측과 향후 보장 질문. January 해결의 후속 실행으로 합치지 않음.'),
'0027':('C05','third_party','responder','--head로 headers만 받는 대안을 제시. 뒤의 작성자 재현이 반박함.'),
'0028':('C05','author_existing_fact','same_public_author_new_root','--head와 --remote-header-name을 함께 쓰면 오류라는 실제 관측을 보고. 별도 root에서 추천 충돌을 보여 주는 보조 반례.'),
'0029':('C05','third_party','maintainer_responder','다른 옵션에 filename 변수를 쓰는 아이디어에 긍정적 반응. 구현 증거 아님.'),
'0030':('C05','author_existing_fact','same_public_author_new_root','두 번의 header 통과·기존 % 문법·변수 이용 가능 시점이라는 설계 문제를 제시.'),
'0048':('C08','unavailable','same_public_sender_unlinked_root','동일 표시 발신자의 extension/DOM 관측 질문이나 C08 Fetch404와 명시 연결 없음. 30일 밖이며 같은 구현으로 합치지 않음.'),
}
rows=[]; sources=[]
for month,table in [('01',JAN),('02',FEB)]:
  for n,(case,classification,role,observation) in table.items():
    u=U(n,month)
    if u not in meta: continue
    m=meta[u]; root=roots[initial[case]['root_url']]; t=iso(m.get('isoreceived'))
    section='primary_30d' if month=='01' else ('implementation_90d' if case=='C06' else 'adjacent_unlinked_90d')
    sid=f'C-F{month}{n}'
    locator='HTML body start/end; 해당 발신자의 새 본문(인용부 제외); id/isoreceived/isosent; In reply to/Reply links'
    if n=='0037' and month=='01': locator='body: 첫 답에 대한 두 thanks 문단, empty temp directory 및 move/rename 문장; HTML metadata'
    if n=='0060' and month=='01': locator='body: To get a feel 문단과 PR8314 링크; HTML metadata'
    if n=='0012' and month=='02': locator='body: parse/understand 복잡성 및 future --jp 두 문단; HTML metadata'
    row={'case_id':case,'message_id':m.get('id'),'url':u,'occurred_utc':t,'date_header_utc':iso(m.get('isosent')),
         'actor':m.get('name'),'role':role,'reply_to':'|'.join(urllib.parse.urljoin(u,x) for x in m.get('parent_hrefs',[])),
         'classification':classification,'variable':initial[case]['missing_variable'],
         'value':'미확인','within_30_days':t is not None and hours(root['received_utc'],t)<=720,
         'action':observation,'locator':locator,'censoring':'observed_message','section':section,
         'q_value_fill_eligible':False,'source_id':sid,'body_sha256':m.get('body_sha256'),
         'lineage_status':'original_thread' if month=='01' and n!='0050' else ('quoted_digest_same_subject' if month=='01' else ('same_feature_author_implementation' if case=='C06' else 'no_explicit_link_to_january_root'))}
    if case in ['C01','C03','C07']: row['value']='최초판에 이미 있음; 이 발화를 새로운 Q 값 회수로 세지 않음'
    if month=='01' and n=='0037': row['value']='기존 workflow가 필요시 move/rename; basename 보존 필수성 yes/no는 명시되지 않음(부분값)'
    if month=='02' and n=='0012': row['value']='새 구현 --json에는 parsing을 넣지 않은 선택; January20 필수범위는 미확인'
    rows.append(row)
    sources.append({'id':sid,'related_q':['Q4','Q5','Q6','Q8'],'case_ids':[case],'url':u,
      'published_or_revised':t,'fixed_version':m.get('id'),'checked_utc':m.get('checked_utc'),
      'read_locations':locator,'observed':observation,
      'limitations':'공개 발신자와 응답 관계만 확인; 독립 실명 검증 없음. 원문의 직접/새 제안/제3자 발언을 구분하며 q_value_fill_eligible=false. '+('주 원장 대화의 답글.' if month=='01' else '별도 후속/인접 root; section의 계보 제한 적용.'),
      'producer':m.get('name'),'lineage':'C-R'+case[1:] if month=='01' else ('C-R06 -> PR8314/32160cae -> February --json announcement' if case=='C06' else 'adjacent_public_sender_only:'+case),
      'count_in_minimum':False,'count_reason':'대화의 답글/같은 구현 계보 또는 모집 표본 밖 인접 사례이므로 원문 최소수에 중복 산입하지 않음','kind':'followup_conversation'})

# Explicit censoring rows are observations of the bounded archive, not refusals/failures.
for case in ['C03','C04','C08']:
    root=roots[initial[case]['root_url']]
    deadline=(dt(root['received_utc'])+datetime.timedelta(days=30)).isoformat().replace('+00:00','Z')
    rows.append({'case_id':case,'message_id':'','url':initial[case]['root_url'],'occurred_utc':deadline,'date_header_utc':'','actor':'미관측','role':'original_author','reply_to':'',
      'classification':'no_answer','variable':initial[case]['missing_variable'],'value':'미확인' if case!='C03' else '최초판에 이미 있음',
      'within_30_days':True,'action':'30일 창에서 원 작성자의 추가 답/실행 보고가 연결되지 않음','locator':'root reply chain + January/February/March/April monthly ledgers',
      'censoring':'right_censored_30d_no_linked_author_reply','section':'primary_30d','q_value_fill_eligible':False,'source_id':'C-R'+case[1:],'body_sha256':'','lineage_status':'bounded_negative_observation'})
csvout('followups.csv',sorted(rows,key=lambda x:(x['case_id'],x['occurred_utc'] or '')))

# Receipt, code, and bounded-ledger sources; post-T0 code never substitutes a frozen candidate.
for ident,url,date,loc,obs,lim,kind,count in [
 ('C-IM01','https://github.com/curl/curl/commit/32160cae847b4e42d52edb033615f88b12ce5c05','2022-02-01T09:39:55Z','docs/cmdline-opts/json.d; src/tool_getparam.c getparameter; src/tool_paramhlp.c get_args; tests/data/test383–386','--json 구현, binary file read, headers, 조각 연결 및 test383–386이 추가됨. --jp 생성 기능은 이 diff에 없음.','이 실행에서 컴파일/테스트 실행 안 함. 공개 diff는 새 개발행동 증거이며 T0 기능 또는 요구 증거가 아님.','provider_implementation',True),
 ('C-IM02','https://github.com/curl/curl/commit/a6f227252cfc80c7c44be395f5a6952221313b74','2022-01-09T15:04:05Z','docs/cmdline-opts/remote-header-name.d diff L8–23; commit message Ref','C05 원 요청을 직접 참조하며 경로제거/저장위치를 문서에 추가.','기존 동작의 문서 보완이지 기능 변경이 아님. 같은 remote-header-name.d 계보가 C-D06에 이미 산입됨.','provider_correction',False),
 ('C-PR01','https://github.com/curl/curl/pull/8314','created 2022-01-21T09:59:38Z','API title/body/created_at/commits; closed PR','작성자 --json PR의 존재와 생성시각; binary 입력+JSON headers shortcut 범위.','현재 PR 본문은 수정 가능. 최초판 확정으로 쓰지 않고 01/0060 보존 메일과 고정 구현 commit으로 개발행동 교차확인.','implementation_metadata',False),
 ('C-B01','https://daniel.haxx.se/blog/2022/02/02/curl-dash-dash-json/','2022-02-02 displayed','JSON in curl; Introducing --json; Details; Ships; Future JSON stuff; jo+curl+jq','단순 --json을 첫 단계로 내고 JSON 생성 실험은 아직 논의 중이라는 공급자 설명.','현재 표시 본문은 역사적 revision 미확보. --data 설명과 구현의 binary 입력 차이가 있어 코드/테스트가 기술판정 우선. 독립 사용자 채택 아님.','maintainer_account',False),
]:
    sources.append({'id':ident,'related_q':['Q4','Q5','Q6','Q8'],'case_ids':['C05'] if ident=='C-IM02' else ['C06'],'url':url,'published_or_revised':date,'fixed_version':url.rsplit('/',1)[-1] if '/commit/' in url else 'current artifact with historical date; limitations apply','checked_utc':NOW,'read_locations':loc,'observed':obs,'limitations':lim,'producer':'curl project / Daniel Stenberg','lineage':'curl/curl:docs/cmdline-opts/remote-header-name.d' if ident=='C-IM02' else 'C-R06 -> PR8314 -> 32160cae847b4e42d52edb033615f88b12ce5c05','count_in_minimum':count,'count_reason':'고유 구현 commit 한 건; 포함 파일·테스트를 별도 더하지 않음' if count else '기존 파일 계보/부가 증거/현재 본문이므로 최소수 밖','kind':kind})
for month,n in [('02',52),('03',72),('04',38)]:
    sources.append({'id':'C-T1L'+month,'related_q':['Q1','Q4','Q6'],'case_ids':list(initial),'url':f'https://curl.se/mail/archive-2022-{month}/','published_or_revised':'2022-'+month+' archive','fixed_version':'official monthly thread ledger; currently rendered','checked_utc':NOW,'read_locations':'전체 제목·발신자·날짜·thread 계층','observed':'원 8개 root의 직접 reply chain에 더해 90일 안의 같은 제목/기능/발신자 후속 후보를 점검. JSON 구현 공지와 remote-header-name/브라우저 인접 root를 직접 열어 계보 분리.','limitations':'월별 제목·링크를 기준으로 한 제한 검색; 모든 다른 제목 메일 본문·GitHub 전역·삭제 메일은 열람하지 않음. 원장에 없다는 것만으로 무실행/거절을 뜻하지 않음.','producer':'curl official mail archive','lineage':'curl-users monthly ledger','count_in_minimum':False,'count_reason':'모집/후속 검색 원장, 고유 사례나 독립 기술 원문으로 산입하지 않음','kind':'ledger'})
sources.extend([
 {'id':'C-X0215','related_q':['Q4'],'case_ids':[],'url':U('0015','02'),'published_or_revised':'2022-02-08T19:00:03Z','fixed_version':'official archive current rendering','checked_utc':NOW,'read_locations':'L30–43 and thread links; Python UTF-8 decoding first failed, then web reader opened full mail','observed':'인접 번호를 점검했으나 JSON 후속이 아닌 AIX SSH key-exchange 질문. 범위 밖으로 제외.','limitations':'Python parser가 UTF-8로 가정하여 0x96에서 실패; 공개 web reader로 본문을 확인해 접근 실패를 회복. 표본에 추가/대체하지 않음.','producer':'Werner L. Stolz via curl-users','lineage':'unrelated February root','count_in_minimum':False,'count_reason':'8건 상한 뒤의 관련 없는 탐색 자료','kind':'exploration'},
 {'id':'C-X0216','related_q':['Q4'],'case_ids':[],'url':U('0016','02'),'published_or_revised':'2022-02-08T21:19:24Z','fixed_version':meta[U('0016','02')]['id'],'checked_utc':meta[U('0016','02')]['checked_utc'],'read_locations':'새 본문 및 In reply to 0015','observed':'AIX SSH 질문에 curl/libssh2 갱신을 제안하는 답. JSON 후속이 아니므로 제외.','limitations':'제3자 추정이며 환경 변경/성공을 확인하지 않음. 이 연구 사례의 근거로 사용하지 않음.','producer':'Ray Satiro via curl-users','lineage':'C-X0215','count_in_minimum':False,'count_reason':'범위 밖 탐색 대화의 답글','kind':'exploration'}
])
dump('sources-t1.json',sources)

# Corrections are separate from the sealed initial/frozen material.
corrections=[{'case_id':'C01','type':'original_reread','sealed_field':'C01-R2 / question_utility','sealed_value':'unknown / requires_answer_to_disambiguate','audited_value':'already_in_T0','source_id':'C-R01','url':U('0002'),'locator':'root L33–42: browser devtools Request cookies, cleared cookies, extension XHR/Fetch','reason':'브라우저 원 요청을 관측하려는 목적이 적혀 있음. curl 재현을 또 하나의 목표로 제시하는 Q는 목적을 바꿀 위험. 원판의 부족은 쿠키 획득법/후보이지 요청 주체가 아니다.','new_author_fact':False,'independent_reader':False,'review_context':'root 통합자의 봉인 전 이견 + 같은 작성자의 T1 자기점검. 독립 가림 판독 아님.'}]
dump('t0-corrections.json',corrections)

AN={
'C01':dict(q_variable_status='already_in_T0',q_value_fill_eligible=False,q_value_partial=False,q_note='브라우저의 실제 Request cookies가 원 목적. 후속의 빈 cookiejar는 실패한 다른 시도이지 새로운 목표 선택값이 아니다.',I='hold',C='hold',goal_enough=False,narrow_enough=True,change='original_reread_correction_only',decision='브라우저 주체는 이미 충분; curl -v의 자기 요청 관측은 원 목적 대체가 아님.',progress=False,progress_kind='none',progress_url='',first='0005',author_replies=1,alternatives=['보류: 브라우저 cookie 접근의 당시 공식 후보를 확보','즉답: curl -v 범위만 설명 가능하되 원 목표 해결로 승인하지 않음'],counter='Q가 새로운 curl 재현 목적을 만들어 버림; 조건분기의 기술적 정확성만으로 질문 유용성을 인정할 수 없음.'),
'C02':dict(q_variable_status='no_author_value',q_value_fill_eligible=False,q_value_partial=False,q_note='NAT 추정은 제3자. 작성자 두 감사 답에는 값이나 실행 결과 없음.',I='hold',C='hold',goal_enough=False,narrow_enough=True,change='still_unknown',decision='local_ip의 의미 설명은 가능하지만 공인IP 서비스 후보는 T0에서 검증되지 않았다. NAT 답이 와도 외부관측 경로는 그대로이며 주소군/프록시는 남음.',progress=False,progress_kind='thanks_only',progress_url='',first='0008',author_replies=2,alternatives=['보류: 같은 당시 서비스 문서 후보가 없어 즉시 명령 승인 불가','조건부 설명: NAT 유무와 local_ip의 범위를 설명하되 실제 외부 서비스 검증 필요'],counter='알아도 robust 외부관측 선택을 바꾸지 않는 질문. 다만 두 후보에 완전히 무관하다는 강한 반례는 아님(local_ip 해석에는 관련).'),
'C03':dict(q_variable_status='already_in_T0',q_value_fill_eligible=False,q_value_partial=False,q_note='root가 요청 전체와 첫~마지막 byte 구간을 이미 대비.',I='supported_limited',C='supported_limited',goal_enough=True,narrow_enough=True,change='selection_maintained',decision='7.55.1 timer와 bar 의미를 설명하는 데 추가 질문이 불필요. 실제 사용자가 수정했는지는 별도 미확인.',progress=False,progress_kind='none',progress_url='',first='0026',author_replies=0,alternatives=['즉답+당시 코드 링크: 전체 경과시간 분모 설명','조건부 답은 가능하지만 이미 표현된 구간을 다시 고르게 할 필요 없음'],counter='응답자가 첫 글만으로 같은 동작을 설명; 질문 없음을 구현 성공과 동일시하지 않음.'),
'C04':dict(q_variable_status='no_author_value',q_value_fill_eligible=False,q_value_partial=False,q_note='실제 응답자가 추가 문자 정체를 질문했으나 저희 Q는 CR/LF 보존이다. 원 작성자 재응답 없음.',I='hold',C='supported_limited',goal_enough=False,narrow_enough=True,change='still_unknown',decision='-d와 --data-binary 구분은 조건부 설명 가능하나 추가 문자 진단은 양쪽 모두 미확인.',progress=False,progress_kind='none',progress_url='',first='0028',author_replies=0,alternatives=['조건부 답 두 링크: CR/LF 제거/보존의 차이','진단은 보류; 실제 파일/request 바이트라는 다른 최소 입력 필요'],counter='봉인한 한 변수의 답을 얻어도 원인 판정이 안 끝남. 실제 응답자가 물은 것은 다른 변수.'),
'C05':dict(q_variable_status='author_existing_fact',q_value_fill_eligible=False,q_value_partial=True,q_note='기존 빈 tempdir와 move/rename은 자발 고지. basename 그대로 보존 필수성의 완전한 yes/no 답은 아님. rename허용⇒비필수라고 넓게 해석하는 민감도만 +1.',I='supported_limited',C='supported_limited',goal_enough=False,narrow_enough=True,change='selection_maintained',decision='경로제거라는 핵심 질문은 첫 글+동시대 코드로 답할 수 있었다. 기존 workflow를 들어 설명을 충분하다고 수용했고 기술판정은 바뀌지 않음.',progress=True,progress_kind='decision_acceptance_existing_workflow_not_new_execution',progress_url=U('0037'),first='0033',author_replies=1,alternatives=['즉답+당시 parse_filename 링크: 해당판 경로제거','조건부 답: basename 필요/불필요일 때 -OJ/-o; 현재판 확인과 오류23 검출법 설명은 별도'],counter='실제 조건부 답은 Content-Disposition 부재시 -O fallback이며 질문 없이 수용됨. 새 구현 해결은 미확인; 봉인 C와 실제 답은 동일 문구 아님.'),
'C06':dict(q_variable_status='no_author_value',q_value_fill_eligible=False,q_value_partial=False,q_note='생성을 필수로 해야 하는지에 대한 T0 기존 사실 yes/no는 없음. --json 작은 범위 구현 및 --jp 미래안 설명은 이후 설계선택.',I='supported_limited',C='supported_limited',goal_enough=False,narrow_enough=True,change='proposal_use_selected_in_later_development_not_retroactive_fitness_change',decision='T0 두 안의 의미는 설명 가능. 후속 개발은 A(--json)를 구현했으나 같은 T0 wiki에서 A/B의 가능/불가 판정이 새 사실 때문에 뒤집힌 것은 아님.',progress=True,progress_kind='original_author_supplier_created_PR_and_commit',progress_url=U('0060'),first='0044',author_replies=3,alternatives=['조건부 답: 준비 JSON 전송/부분값 구성으로 두 제안 구분','즉답: 첫 단계 shortcut 범위 제안 가능; 출시 명령으로 승인하지 않음'],counter='제3자의 response parsing/배열 결합 요구를 원 질문자 T0 필수로 넣으면 모두 부당 탈락. 공급자 개발을 사용자 채택 효과로 바꾸지 않음.'),
'C07':dict(q_variable_status='already_in_T0',q_value_fill_eligible=False,q_value_partial=False,q_note='현재판 사용법이 아니라 CLI 설계 제안이라는 점이 제목·본문에 이미 있음.',I='hold',C='hold',goal_enough=False,narrow_enough=True,change='still_unknown',decision='현재판 URL은 기준선이며 타이핑 감소안을 충족하는 구현 증거가 아님. 후속에 개발자 대상/스크립트 위험 논의가 있으나 구현 확정 없음.',progress=False,progress_kind='discussion_not_implementation',progress_url='',first='0056',author_replies=1,alternatives=['보류: 새 문법의 구현/시험과 사용자 이점 확인','즉답: 이미 새 제안임을 읽고 current-release URL을 기준선으로 설명'],counter='Q의 current/future 구분은 이미 적혀 있다. 실제 질문은 대상 사용자 관련성과 빈 hostname 위험으로 다른 변수.'),
'C08':dict(q_variable_status='no_author_value',q_value_fill_eligible=False,q_value_partial=False,q_note='30일 내 연결된 답이 없고 정확한 Fetch/curl URL도 없다. 같은 발신자의 2월25일 DOM 질문은 명시 계보 없음.',I='hold',C='hold',goal_enough=False,narrow_enough=False,change='still_unknown',decision='후보 없음. URL 같음/다름을 알아도 headers/body/server 차이가 남아 원인 승인은 불가.',progress=False,progress_kind='none',progress_url='',first=None,author_replies=0,alternatives=['한 변수 요청은 가능하지만 충분성은 제한적','해결책 보류; 실제 네트워크 요청의 동시 비교 입력 필요'],counter='무응답은 거절/실패가 아니라 30일 우측 검열. 동일 발신자의 다른 질문을 성공후속으로 연결하지 않음.'),
}

analyses=[]; chronology=[]
for case,a in AN.items():
    x=initial[case]; r=roots[x['root_url']]; first=meta.get(U(a['first'])) if a['first'] else None
    first_time=iso(first['isoreceived']) if first else None
    rt=[]
    if case=='C07':
        rt=[{'request':U('0058'),'response':U('0061'),'variable':'localhost 기능의 대상 사용자/관련성','same_as_frozen_variable':False,'wait_hours':hours(iso(meta[U('0058')]['isoreceived']),iso(meta[U('0061')]['isoreceived'])),'qualification':'추가 설계 목적/대상에 대한 질문→작성자 답. 숫자 사용자 규모는 작성자의 주장으로만 기록. 엄격한 기술입력 질문만 세는 민감도에서는 제외.'}]
    p30=(dt(r['received_utc'])+datetime.timedelta(days=30)).isoformat().replace('+00:00','Z')
    p90=(dt(r['received_utc'])+datetime.timedelta(days=90)).isoformat().replace('+00:00','Z')
    ch={'case_id':case,'root_message_id':r['message_id_display'],'root_date_header_utc':r['submitted_utc'],'root_server_received_utc':r['received_utc'],'first_reply_url':first['url'] if first else None,'first_reply_message_id':first.get('id') if first else None,'first_reply_server_received_utc':first_time,'root_precedes_first_reply':r['received_utc']<first_time if first_time else None,'status':'confirmed_root_before_reply' if first else 'root_artifact_confirmed_no_reply_in_30d','root_full_body_read_T0':True,'raw_MIME_obtained':False,'server_metadata_kind':'Hypermail id/isoreceived/isosent + archived body, not cryptographic original mail','global_seal_sha':SEAL}
    chronology.append(ch)
    analysis={'case_id':case,'global_seal_sha':SEAL,'original_confirmed':True,'strict_followup_unexposed_T0':True,
      'q_variable_status':a['q_variable_status'],'q_value_fill_eligible':a['q_value_fill_eligible'],'q_value_partial':a['q_value_partial'],'q_variable_note':a['q_note'],
      'q_direct_answer_count':0,'q_author_existing_complete_value_count':0,'q_same_variable_asked_in_actual_thread':False,
      'q_value_known_in_T0':a['q_variable_status']=='already_in_T0','q_value_gained_after_T0':False,'q_value_alone_sufficient_for_original_goal':False,'q_value_plus_frozen_evidence_sufficient':case=='C03',
      'T0_original_goal_fully_sufficient':a['goal_enough'],'T0_narrow_scoped_statement_supported':a['narrow_enough'],
      'original_goal_scope_note':a['decision'],'decision_change':a['change'],'technical_fitness_changed_by_eligible_new_author_fact':False,
      'I':{'technical_status':a['I'],'grounded_use_approval':False,'original_goal_complete':case=='C03','narrow_claim_supported':a['narrow_enough'],'links_count':frozen[case]['I'].count('https://')},
      'C':{'technical_status':a['C'],'grounded_use_approval':False,'conditional_branches_supported':a['narrow_enough'],'original_goal_complete':case=='C03','links_count':frozen[case]['C'].count('https://')},
      'Q':{'variable_already_known':a['q_variable_status']=='already_in_T0','public_complete_answer_observed':False,'counterfactual_expected_additional_roundtrips_minimum_if_answered':1,'actual_Q_sent':False},
      'actual_author_reports_progress':a['progress'],'actual_author_progress_kind':a['progress_kind'],'actual_author_progress_url':a['progress_url'],'actual_author_reports_new_execution_or_change':case=='C06','new_execution_on_frozen_candidate_observed':False,'new_development_of_proposal_use_observed':case=='C06',
      'actual_clarification_roundtrips':{'count':len(rt),'definition':'추가 목적/조건 확인 질문 뒤 원 작성자가 답한 공개 메시지쌍; 단순 감사·제3자 대화·설명후자발고지는 제외','pairs':rt,'strict_technical_input_only_count':0},
      'actual_general_author_replies_in_primary_thread':a['author_replies'],'wait_hours':rt[0]['wait_hours'] if rt else None,
      'root_to_first_reply_hours_server':hours(r['received_utc'],first_time) if first_time else None,
      'root_to_first_reply_hours_sender_date':hours(r['submitted_utc'],iso(first['isosent'])) if first else None,
      'window_30d_end_utc':p30,'window_90d_end_utc':p90,'actual_no_response_censoring':'30d right censor; not rejection/failure' if case in ['C03','C04','C08'] else 'public responses observed; missing frozen-variable value retained',
      'source_click_proxy':{'unique_primary_followup_pages':sum(1 for rr in rows if rr['case_id']==case and rr['section']=='primary_30d' and rr['censoring']=='observed_message'),'meaning':'연구자가 연 고유 페이지 수; 사용자 클릭/읽기시간 아님. 재시도·중복 열람 포함 총 호출 수는 미확인'},
      'implementation_90d':{'observed':case=='C06','url':'https://github.com/curl/curl/commit/32160cae847b4e42d52edb033615f88b12ce5c05' if case=='C06' else None,'note':'별도 구현 열. C05는 공급자 문서정정만 C-IM02, 새 사용자실행 아님.'},
      'postT0_requirement_retrofit_sensitivity':{'result':'C06-R3 불필요를 필수로 잘못 바꾸어 response parsing을 요구하면 A/B 둘 다 탈락; 실제 T0 판정에는 적용 안 함' if case=='C06' else ('February time-cond/dump-header 요구를 소급하면 A/B만으로 충분하지 않게 되지만 별도 root/30일 밖이므로 주 비교 제외' if case=='C05' else '해당 없음: 적격 원 작성자의 새 요구를 명확히 확인하지 못함'), 'eligible_for_main_comparison':False},
      'possible_alternatives':a['alternatives'],'counterexample_or_null':a['counter'],
      'public_sender_cluster':'bruce_C01_C04_C08' if case in ['C01','C04','C08'] else ('Daniel_C06_C07' if case in ['C06','C07'] else case),
      'possible_shared_context_cluster':'browser_extension_C01_C08' if case in ['C01','C08'] else None,
      'same_implementation_explicitly_linked':False,'supplier_also_questioner':case in ['C06','C07'],
      'self_check':'same researcher T0/T1; root review for C01; no blinded independent adjudication'}
    if case=='C04': analysis['unanswered_actual_question']={'url':U('0028'),'variable':'추가 문자 정체','q_same_variable':False,'observed_wait_hours':None,'right_censor_hours_from_question_to_root_plus_30d':hours(iso(meta[U('0028')]['isoreceived']),p30)}
    if case=='C05': analysis['actual_conditional_answer']={'url':U('0033'),'condition':'Content-Disposition header 없음','response':'-O URL 기반 이름 fallback','contains_source_link':False,'later_documentation_link':U('0038'),'extra_question_count':0,'acceptance_url':U('0037'),'implementation_resolution':False,'different_from_frozen_C':True}
    if case=='C06': analysis['implementation_conversation_extra_roundtrip']={'request':U('0009','02'),'response':U('0010','02'),'variable':'여러 --json을 이어 붙이는 이유','wait_hours':hours(iso(meta[U('0009','02')]['isoreceived']),iso(meta[U('0010','02')]['isoreceived'])),'not_frozen_variable':True,'section':'implementation_90d'}
    analyses.append(analysis)
(P/'case-analysis.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in analyses))
dump('chronology.json',chronology)

# Required and non-required conditions are judged separately; no non-required
# preference silently becomes a veto. Values concern stated use, not all uses.
VER={
'C01':{'A':['conflict','supported','supported'],'B':['unknown','supported','supported']},
'C02':{'A':['unknown','supported','unknown'],'B':['unknown','supported','unknown']},
'C03':{'A':['supported','supported','supported'],'B':['supported','supported','supported']},
'C04':{'A':['unknown','unknown','unknown'],'B':['unknown','unknown','unknown']},
'C05':{'A':['supported','unknown','unknown'],'B':['supported','unknown','unknown']},
'C06':{'A':['supported','supported','supported','unknown'],'B':['supported','supported','supported','unknown']},
'C07':{'A':['conflict','supported','unknown','supported'],'B':['unknown','unknown','unknown','supported']},
'C08':{'NONE':['unknown','unknown','unknown','unknown']},
}
judge=[]
for case,x in initial.items():
    candidates=x['candidate_uses'] or [{'id':'NONE','source_id':'C-R08','url':x['root_url'],'use':'후보 없음; 해결책 보류','version':'미확인'}]
    for c in candidates:
      s=source0[c['source_id']]
      for ri,r in enumerate(x['requirements']):
        for tp in ['T0','T1']:
          action='no_report'; au=''; al=''; ak=''
          if tp=='T1' and case=='C05' and c['id']=='A': action='reported_progress';au=U('0037');al='good enough + empty temp directory + move/rename';ak='decision_acceptance_only'
          if tp=='T1' and case=='C06' and c['id']=='A': action='reported_progress';au=U('0060');al='created PR8314';ak='postT0_development_not_T0_available_feature'
          note=AN[case]['decision']+' '+('C01-R2는 별도 original_reread 보정으로 이미 브라우저값이 명시됨. 이를 T1 새사실로 세지 않음. ' if case=='C01' and ri==1 else '')
          if case=='C03' and c['id']=='B': note+='bar는 진행량 표시라는 설명 범위에서 supported; 바이트구간 속도 대체로 승인한 것이 아님.'
          if case=='C01' and c['id']=='A': note+='브라우저 원요청 획득 목표에는 conflict이지만 frozen I/C는 이 사용을 승인하지 않았으므로 오승인 아님.'
          if case=='C07' and c['id']=='A': note+='명시적 전체URL은 타이핑 감소 요구를 충족하지 않지만 frozen은 원래 기능의 해결로 승인하지 않음.'
          if case=='C06': note+='supported는 미출시 제안의 설명/구분만 뜻함; 32160cae 구현을 같은 wiki판의 기술증거로 소급하지 않음.'
          judge.append({'case_id':case,'candidate_id':c['id'],'condition_id':r['id'],'condition_kind':r['kind'],'condition_text':r['text'],'condition_url':r['url'],'condition_locator':'L40, L43–44' if r['id']=='C04-R2' else r['locator'],'sealed_condition_locator':r['locator'],'timepoint':tp,'technical_verdict':VER[case][c['id']][ri],'technical_source_ids':c['source_id'],'technical_url':c['url'],'technical_locator':s['read_locations'],'comparison_version':c['version'],'action_verdict':action,'action_url':au,'action_locator':al,'action_kind':ak,'note':note})
csvout('judgments.csv',judge)

summary={'global_seal_sha':SEAL,'recorded_utc':NOW,'cases':8,'frozen_strategies':24,'confirmed_originals':8,'root_precedes_first_reply':7,'no_first_reply_30d':1,'already_known_Q_variables':3,'strict_complete_new_Q_values':0,'partial_author_existing_Q_value_cases':['C05'],'broad_rename_implies_optional_sensitivity_Q_values':1,'technical_fitness_changes_from_eligible_new_author_fact':0,'actual_author_progress_including_decision_acceptance':2,'actual_author_new_development':1,'actual_user_new_execution_of_suggested_existing_feature':0,'clarification_roundtrips_including_target_user_justification':1,'strict_technical_input_roundtrips':0,'conditional_response_decision_acceptance_cases':['C05'],'conditional_response_implementation_solution_confirmed':0,'contradicted_approvals_I':0,'contradicted_approvals_C':0,'unsupported_approvals_I':0,'unsupported_approvals_C':0,'I_supported_limited':3,'I_hold':5,'C_supported_limited':4,'C_hold':4,'grounded_use_approvals_I':0,'grounded_use_approvals_C':0,'source_rows_T1':len(sources),'unique_followup_mail_pages_read':len(JAN)+len(FEB),'exploratory_unrelated_mail_pages_read':1,'exploratory_access_failures':1,'primary_thread_followup_messages':len(JAN),'judgment_rows':len(judge),'followup_rows':len(rows),'T0_file_sha256_after_T1':sealed_hashes,'limitations':['분모는 서로 다른 8개 root이지 8명/8개 독립 구현 아님','C01/C04/C08 동일 표시 발신자; C06/C07 공급자 겸 질문자','원문 페이지 재방문 횟수는 저장하지 않아 전체 network-call 비용은 미확인','C05 결정수용과 C06 공급자 개발은 외부 사용자의 실행 성공과 구분','가상 Q의 인과효과/시간절감은 미확인','모든 T0/T1은 같은 연구자; root 검토는 가림 판독 아님']}
summary['exploratory_unrelated_mail_pages_read']=2
summary['exploratory_access_failures_recovered']=1
dump('t1-summary.json',summary)
receipt=json.loads((P/'t1-code-receipts.json').read_text());receipt['checked_utc']=NOW;receipt['timestamp_note']='source tool result inspected and receipt written at this checkpoint; original fetch seconds not separately retained';dump('t1-code-receipts.json',receipt)
print(json.dumps({k:v for k,v in summary.items() if k!='T0_file_sha256_after_T1'},ensure_ascii=False,indent=2))
