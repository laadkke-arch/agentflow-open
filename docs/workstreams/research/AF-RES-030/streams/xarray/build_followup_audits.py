"""Post-seal screening-window and direct-reading ledgers. No T0 rewrites."""
import json, datetime as dt, hashlib
from pathlib import Path
P=Path(__file__).resolve().parent
NOW=dt.datetime.now(dt.timezone.utc).isoformat()
I={r['case_id']:r for r in map(json.loads,(P/'initial.jsonl').read_text().splitlines())}
SEL={'XB03','XB06','XB08','XB13','XB14'}
def t(s):return dt.datetime.fromisoformat(s.replace('Z','+00:00'))
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def out(name,rows):(P/name).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n'for r in rows))
PAG={r['issue_number']:r for r in json.loads((P/'pagination-followup-receipts.json').read_text())}
SUMMARY={
'XB01':('region API 문서 안내 뒤 원 작성자 후속 없음.','최초 응답은 직접 안내이고 기존 환경/목표/입력을 묻지 않음.'),
'XB02':('tuple/object-array 진단과 과거 PR·중복 이슈 연결. 원 작성자는 tuple check 제거를 제안하지만 새 실행 결과 없음.','최초 응답은 tuple 처리 진단.'),
'XB03':('선정 B. 기존 핵심 목표 재진술·array API 맥락 보충·후속 선호 명확화. 원 작성자 새 실행 없음.','선정 B: 최초 목표 질문.'),
'XB04':('CF/netCDF 표준과 missing_value 정책 논의, 작성자가 표준 링크 제시. 실제 사용자 환경 회수나 실행 성공 아님.','최초 질문은 라이브러리 정책/표준 함의이며 사용자 환경·목표·입력 회수 아님.'),
'XB05':('과거 논의 중복 인정 뒤 기본 fillvalue 정책/옵션 설계 논의. 출력 코드는 screening에서 세부 실행 판독하지 않음.','최초 응답은 기존 기술 설계 논의 연결.'),
'XB06':('선정 B. root30/90에는 실질 타인 응답 없음. 최초 질문은 16개월 뒤이며 별도 chains의 late extension에 보존.','선정 B: 늦은 최초 기존원인 질문; 지연으로 제외하지 않음.'),
'XB07':('PR 환영 문구 외 후속 없음.','최초 응답은 기여/구현 초대.'),
'XB08':('선정 B. 작성자가 버전 표를 본문에 추가. 지원자 진단·벤치마크 뒤 감사만 있음.','선정 B: 최초 버전 질문.'),
'XB09':('외부 backend 문서와 tutorial 안내 뒤 작성자 후속 없음.','최초 응답은 문서 안내.'),
'XB10':('root30 밖/90 안에 PR로 해결됐는지 확인, 작성자는 exact joins만 고쳐졌다고 답함.','기존 환경/입력/목표가 아니라 공급자 패치 해결 여부 확인.'),
'XB11':('한 문서 링크 뒤 작성자가 완료했다고만 응답. 구체 새 호출/출력이 없어 엄격 실행 성공 미확인.','최초 응답은 string encoding 문서 링크.'),
'XB12':('없는 dimension 처리 정책/가상 동작을 질문, 작성자는 실제 차원명 변경 사연을 공개. 실행 결과는 없음.','최초 질문은 정책의 가상 사례이며 기존 환경/목표/입력 직접 질문 기준에 미달.'),
'XB13':('선정 B. local file·이름 직접 답과 같은 파일 독립 열기 실패, 나중에 다른 파일/다른 Python판 성공.','선정 B: 최초 입력 위치/파일명 질문.'),
'XB14':('선정 B. backend 직접 답; server/filesystem 용어 설명 후 두 번째 변수 답; 다른 지원자가 retry 코드 안내. 새 작성자 실행 없음.','선정 B: 최초 backend/원격대상 질문.'),
'XB15':('공급자가 버그이며 곧 수정 release 예정이라고 말함. 작성자 후속 없음.','최초 응답은 공급자 진단/수정 예고.'),
'XB16':('root90 내 인간 실질 댓글 없음.','최초 실질 응답 없음.'),
'XB17':('einsum callable/boolean 옵션, 자동 opt_einsum 사용과 debugging off 필요를 개발자들이 토론. 사용자 새 실행 없음.','최초 응답은 API 설계안 및 가상 질문.'),
'XB18':('root90 내 인간 실질 댓글 없음.','최초 실질 응답 없음.'),
'XB19':('where 인수 순서를 직접 설명하자 작성자가 의미를 재진술하고 역사/이유를 질문. 실행 결과 없음.','최초 응답은 함수 인수 사용 예제.'),
'XB20':('p0를 apply_ufunc positional args로 넘기라는 즉답 뒤 작성자가 PR7821 구현 및 아이디어 채택을 보고. bounds는 아직 미구현; 실행 성공과 구별.','최초 응답은 구현 제안.'),
'XB21':('entrypoints 및 BackendEntrypoint 직접 사용을 안내. 작성자는 이해했고 읽겠다고 응답. 실행 없음.','최초 응답은 문서 안내.'),
'XB22':('최초 nbytes 설명 뒤 작성자가 numpy의 sparse 값과 sparse.COO를 혼동. 뒤에 버전을 물으나 원 판 대신 main에서 재현 불가라는 새 결과만 답함.','최초 응답은 진단과 stack 조사 권유; 후발 명확화가 있어도 B 최초 기준에 넣지 않음.'),
'XB23':('netCDF4.Dataset 직접 시험 권유 뒤 작성자가 Ubuntu/Colab 실패를 보고하고 upstream 이슈1246 개설. root90 안에서 이후 dependency 논의가 이어짐.','최초 문장은 새 trial 요청이며 기존 환경/목표/입력 질문 아님.'),
'XB24':('root30/90 내 인간 실질 댓글 없음. 최초 타인 응답은 창 밖.','최초 응답은 typing 설명이며 직접 정보 질문 아님.'),
'XB25':('질문 없는 mask_and_scale 제안 뒤 작성자가 float 변환 해결/uint8 문제를 보고. 같은 지원자의 decode_cf 단계 제안 뒤 실제 동작 및 astype 시간 감소를 말함. 공급자 후속 정책 논의 별도.','최초 응답은 설정 안내. 질문 없는 실행의 반례지만 B8/A 분모 밖 감사 사례.'),
'XB26':('타인 응답 전에 작성자가 두 인수를 함께 주는 자체 해법을 찾아 작동 코드를 올림.','타인 첫 실질 응답 없음; 자기해결을 전략효과로 세지 않음.'),
'XB27':('처음 NaT encoding 안내에서 시작해 다수 재현·실패·환경차이와 NaN→int casting 문제를 추적. 작성자는 pandas 수준 확인을 보고했으나 전체 patch 적용 성공으로 확대할 수 없음.','최초 응답은 기술 설명; 뒤의 trial/명확화가 있어도 B 최초 기준에 넣지 않음.')
}
SC=[];UP=[]
for cid,i in I.items():
 n=i['issue_number'];fs=list((P/'retrieved').glob(f'comments-{n}*'));f=next((f for f in fs if'rawconnector'in f.name),fs[0]);raw=json.loads(f.read_text());cc=raw['data'];root=t(i['created_at']);h=[c for c in cc if not c['user']['login'].endswith('[bot]')]
 inside=[c for c in h if t(c['created_at'])<=root+dt.timedelta(days=90)]
 readmode='full selected commentary, code/output where used for judgement'if not cid.startswith('XB')or cid in SEL else'root+first response at T0; all root90 human prose at followup; fenced code omitted from screening prose audit'
 UP.append(dict(source_id=f'XT-FU-{cid}',case_id=cid,type='public_issue_followup_reading_update',publisher='pydata/xarray public participants',
  url=i['root_url'],version='current public comments, historical creation timestamps; edited bodies flagged',checked_utc=NOW,
  sections=[dict(comment_id=c['id'],url=c['html_url'],at=c['created_at'],updated_at=c['updated_at'],body_sha256=sha(c['body']or''))for c in inside],
  read_mode=readmode,observed=SUMMARY[cid][0]if cid.startswith('XB')else'chains.jsonl 및 initial-field-audit.jsonl에 후속/원본문 절 감사 기록',
  limitations='현재 공개 댓글 두 페이지를 확인. 삭제된 과거 내용은 복원 불능. 미열람 코드블록에서 결과를 주장하지 않음. root 원판 미복원은 유지.',
  linked_Q_cases=['Q2','Q3','Q5','Q6','Q7',cid],duplicate_group=f'pydata/xarray/issues/{n}',count_minimum=False,
  reason_not_counted='동일 thread의 후속 재열람; T0 source-ledger에 이미 원문 하나로 기록',pagination_receipt=PAG[n]))
 if not cid.startswith('XB'):continue
 human30=[c for c in inside if t(c['created_at'])<=root+dt.timedelta(days=30)]
 SC.append(dict(case_id=cid,sample='B_selected'if cid in SEL else'B_screening_only',in_B8_denominator=cid in SEL,root_url=i['root_url'],
  created_at=i['created_at'],goal=i['goal'],first_strategy=i['first_strategy'],first_response_url=i['first_response_url'],first_response_at=i['first_response_at'],
  first_information_question=i['b_question_eligible'],selection_reason=SUMMARY[cid][1],followup_summary=SUMMARY[cid][0],
  checked_utc=NOW,root30_end=(root+dt.timedelta(days=30)).isoformat(),root90_end=(root+dt.timedelta(days=90)).isoformat(),
  root30_status='public_visible_complete',root90_status='public_visible_complete',calendar_windows_closed=True,
  root30_human_comments=len(human30),root90_human_comments=len(inside),
  root90_root_author_comments=sum(c['user']['login']==i['author']for c in inside),
  read_comment_urls=[c['html_url']for c in inside],read_mode=readmode,last_read_in_window_url=inside[-1]['html_url']if inside else i['root_url'],
  last_endpoint=PAG[n]['url'],pagination=PAG[n],
  deleted_content='미확인: 현재 공개 API로 삭제 내용을 복원할 수 없으나 관측된 누락 흔적은 없음',
  unavailable_fact='원 작성자의 실제 비공개 실행·클릭·읽기 시간',next_evidence='같은 입력/판/목적의 공개 실행 로그; 새 사람에게 연락하지 않음'))
r=next(r for r in UP if r['case_id']=='XB08')
r['late_extension_sections']=[dict(comment_id=1709120441,at='2023-09-06T21:08:04Z',url='https://github.com/pydata/xarray/issues/7730#issuecomment-1709120441'),dict(comment_id=1709773599,at='2023-09-07T09:05:58Z',url='https://github.com/pydata/xarray/issues/7730#issuecomment-1709773599')]
r['late_extension_observed']='원 작성자의 engine=flox 성능 개선 보고는 root+153일 이후. root90 및 첫question30 분모 밖.'
out('screening-followups.jsonl',SC);out('reading-updates.jsonl',UP)

existing=[json.loads(l)for l in(P/'providers.jsonl').read_text().splitlines()]
receipts={r['source_id']:r for r in json.loads((P/'provider-followup-fetch-receipts.json').read_text())}
PROV=[
('XD06','official_source_code','pydata/xarray','https://github.com/pydata/xarray/blob/v2022.03.0/xarray/backends/api.py','v2022.03.0','dump_to_store L1104–1119','명시 encoding 항목은 기존 variable.encoding에 대입되어 대체됨. X01 보고판과 같은 tag로 기존2022.12 근거를 보강.','코드만으로 작성자의 실제 파일 저장/CRS 보존을 증명하지 않음.',['Q6','X01'],'xarray/backends/api.py',False),
('XD07','official_source_code','pydata/xarray','https://github.com/pydata/xarray/blob/a4c54a3b1085d7d8ab900f9a645439270327d2c3/xarray/backends/netCDF4_.py','a4c54a3b1085d7d8ab900f9a645439270327d2c3','L87–110; remote _getitem L102–106','remote datastore 인덱싱에서 RuntimeError를 잡는 robust_getitem을 선택.','open_dataset 전체의 connection timeout 보장이나 작성자 실행 성공은 아님.',['Q6','XB14'],'xarray/backends/netCDF4_.py',True),
('XD08','official_source_code','pydata/xarray','https://github.com/pydata/xarray/blob/a4c54a3b1085d7d8ab900f9a645439270327d2c3/xarray/backends/common.py','a4c54a3b1085d7d8ab900f9a645439270327d2c3','robust_getitem L61–83','기본 max_retries=6, initial_delay=500ms, exponential jitter/backoff. 주석의32–64초는 최대 delay 설명.','전체 API timeout이나 모든 backend에 대한 정책으로 일반화 불가; 사용자가 설정했는지 없음.',['Q6','XB14'],'xarray/backends/common.py',True),
('XD09b','official_backend_registration','rioxarray contributors','https://github.com/corteva/rioxarray/blob/0.13.3/setup.cfg','0.13.3; PyPI2022-12-19 upload verified','setup.cfg L1–5,35–39,48–50; PyPI release file timestamps','당시 배포본이 rasterio를 xarray.backends entrypoint로 등록함. X04의 backend 발견 설명을 직접 지지.','요청자가 실제 설치한 rioxarray 판은 미확인; 모든 GeoTIFF/CRS 보존을 보장하지 않음.',['Q6','X04'],'rioxarray/setup.cfg',True),
('XD10','official_source_code','pydata/xarray','https://github.com/pydata/xarray/blob/2657787f76fffe4395288702403a68212e69234b/xarray/conventions.py','2657787f76fffe4395288702403a68212e69234b','decode_cf_variable L215–282, especially266–272','mask_and_scale 조건 안에 UnsignedIntegerCoder와 CFMaskCoder/CFScaleOffsetCoder가 함께 있음. XB25의 uint8 후속 반례를 기술적으로 지지.','새 코드 실행은 하지 않았으며 전체 데이터 변환 정합은 작성자 보고에 의존.',['Q6','Q7','XB25'],'xarray/conventions.py',False),
]
ids={r['source_id']for r in existing}
for sid,typ,pub,url,ver,sect,obs,lim,links,dup,count in PROV:
 r=receipts[sid]
 if sid not in ids:existing.append(dict(source_id=sid,type=typ,publisher=pub,url=url,version=ver,checked_utc=r['checked_utc'],sections=sect,observed=obs,limitations=lim,linked_Q_cases=links,duplicate_group=dup,count_minimum=count,body_sha256=r['sha256'],direct_read=True))
if 'XD11'not in ids:
 f=json.loads((P/'retrieved/array-api-399.json').read_text());existing.append(dict(source_id='XD11',type='official_standards_decision_thread',publisher='data-apis/array-api participants',url='https://github.com/data-apis/array-api/issues/399',version='2022-02-28 root/comments; 2023-03-09 closure rationale',checked_utc=f['checked_utc'],sections='root and comments1054694689,1055095363,1461782239',observed='혼합 라이브러리 연산을 표준 non-goal로 설명하고 runtime type check/예외를 강제하지 않는다고 논의. 2023-03에 기존문구로 충분하다고 닫음.',limitations='논쟁의 현재 본문은 읽었으나 각 댓글 원판 이력은 미복원. xarray의 하위호환 목표에 어떤 실행이 최적인지는 정하지 않음.',linked_Q_cases=['Q6','XB03'],duplicate_group='data-apis/array-api/issues/399',count_minimum=True,direct_read=True,body_sha256=sha(f['data']['body'])))
out('providers.jsonl',existing)
print(json.dumps({'screening_cases':len(SC),'selected_B':sum(r['in_B8_denominator']for r in SC),'reading_updates':len(UP),'providers_total':len(existing),'provider_minimum_flagged':sum(r['count_minimum']for r in existing)},ensure_ascii=False,indent=2))
