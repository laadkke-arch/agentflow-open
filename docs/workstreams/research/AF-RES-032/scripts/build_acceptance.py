"""Record task acceptance, preserving research and procedure gaps explicitly."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess

P=Path(__file__).resolve().parents[1]
ROOT=P.parents[3]
C=json.loads((P/'evidence/counts.json').read_text())
def read(path):
    p=P/path
    return json.loads(p.read_text()) if p.exists() else {}
conditions=[]
def add(cid,condition,met,evidence,note):
    conditions.append({'id':cid,'condition':condition,'met':bool(met),'evidence':evidence,'note':note})
add('C01','지정 foundation/의존 고정 SHA와 절차를 읽고 실제 시작을 기록',True,['SCOPE.md','evidence/start.json','manifest.json'],'계획478c… 대신 착수 시 최신172c6bc…; 의존027은42dadeeb…. 실제 세션 선언 모델과 UI 미확인을 구분.')
add('C02','workbench.session start 및 인계 전 check --fetch 실제 실행',read('evidence/checks/session-pre-result-execution.json').get('exit_code')==0,['evidence/start.json','evidence/checks/session-pre-result-execution.json','evidence/checks/session-pre-result.stdout.json'],'6ac3d4d HEAD+작업 트리 검사. 고정 결과 commit 이후 재검은 HANDOFF와 별도 영수증으로 기록하며 이 검사에 소급하지 않음.')
add('C03','소유 경로 안에서만 산출물 작성, dot-control 불변',True,['manifest.json','evidence/checks/session-pre-result.stdout.json'],'session scope 통과. 공통 gate는 owned_path/cache의 별도 checkout에서 실행하여 .workbench/temp도 소유 경로 안에 둠. 최종 fixed SHA diff는 인계 단계 재검.')
add('C04','A 두 유통 경로 각6·서로 다른 배포 HTML12·6프로젝트·각≤2',C['A_references']==12 and C['A_distinct_documents']==12 and C['A_projects']==6 and C['A_routes']=={'D':6,'R':6},['references.jsonl','evidence/a-sealed.jsonl','evidence/counts.json','collectors/cran/integration-audit.json'],'실제 archive member의 원 href. PostgreSQL source archive도 prebuilt HTML을 직접 확인. B로 A최소수를 대체하지 않음.')
add('C05','A 출발판 2020–2024 및 최소12개월 후속 조사창',True,['references.jsonl','SCOPE.md','editions.csv'],'최종 A원판은 모두2020. 관측창 종료까지12개월 이상이지만 전 기간의 연속 관측을 뜻하지 않음.')
add('C06','A 목적·href·hash를 상류와 후속판을 읽기 전에 원격 봉인',True,['evidence/a-seal-remote.json','evidence/a-sealed.jsonl','collectors/cran/integration-audit.json'],'A봉인168d90b… 재독07:18:08Z. 최초12행50,326bytes/prefix SHA b3c2f68… 보존. 후발 보강은 amendments로 구분.')
add('C07','표집 순서 수정은 결과를 보기 전에 수행하고 잠정 표본을 보존',True,['evidence/preseal-order-correction.md','evidence/scope-deviations.md','collectors/cran/final/candidate-archives.json'],'최초 R초안은 날짜 우선 요구를 잘못 옮김. 봉인·상류 열람 전에 고쳤고 잠정6을 제외. 공개 모집단 대표 표본이라는 주장은 하지 않음.')
add('C08','모든 제외 유형의 완전한 수를 기록',False,['frame.csv','collectors/python/frame.csv','collectors/offline/frame.csv'],'선택12/외부URL없는문서27/같은문서추가링크11/미도달R후보7은 기록. PG/SQLite의 모든 nav/footer·가상URL 제외 총수는 미완성. 다음 자료: 봉인한 원 archive에 같은DOM 제외규칙을 적용한 완전 후보 inventory; A선정은 바꾸지 않음.')
add('C09','명시적으로 제외한 이전 소비자 탐색에 들어가지 않음',False,['evidence/scope-deviations.md','collectors/cross/b/attempts.jsonl'],'B01-C4 JupyterLab 과거HTMLzip GET3회(CB-GET30/33/34)는 범위 위반. 전부404, 직접원문/수정분자0. 지우지 않고 후보비용에 포함. 재개 시 해당 소비자를 제외한 이미 봉인된 B사건만 검토.')
add('C10','B6 사건을 시점 순으로 소비자 검색 전에 봉인',True,['collectors/b/b-sealed.jsonl','collectors/b/remote-seal-receipt.json','collectors/b/SELECTION.md'],'봉인ffbce62…; 성공 여부로 사건을 재선정하지 않음. 제한된 공지 탐색의 날짜순이며 세계 전체 사건의 완전한 목록은 아님.')
add('C11','B6 실패 포함·질의≤3/후보문서≤5 상한과 A중복을 보존',C['B_attempts']==6 and C['B_queries']==18 and C['B_candidate_documents']==17 and C['B_A_duplicates']==1,['references.jsonl','collectors/b/root-consumer-attempts.jsonl','collectors/cross/b/attempts.jsonl','collectors/offline/b05/attempts.jsonl','collectors/cran/integration-audit.json'],'후보4/5/2/2/1/3. B05=A-D04; B04과거HTML미확인. 이미새URI·다른목적추가·old유지를 모두 보존.')
add('C12','A 원 인용의 배포 ID/hash/member/raw href/base/resolved/anchor/문맥/목적 고정',True,['references.jsonl','evidence/rows/','collectors/cran/integration-audit.json'],'선택 A href는 전부절대URI. 상대URI 해소의 실증 사례는 없음. B04 문자열은 source reST이며 과거 HTML href로 가장하지 않음.')
add('C13','고유 직접 원문 최소30과 범주별 최소12/8/6/4 충족',C['unique_minimum_originals']>=30 and all(C['unique_minimum_by_category'][k]>=v for k,v in [('A_original',12),('upstream',8),('consumer_followup',6),('cross_field',4)]),['sources.jsonl','evidence/counts.json','evidence/source-deduplication.json','collectors/cran/integration-audit.json'],'75=12+34+8+8+1+5+7. 후속8=변경HTML6(목적대체1포함)+독립공표2. 접근실패/검색요약/동일원고미러 제외.')
add('C14','원문마다 발행자·원주소·판/날짜·UTC·읽은 위치·발견·한계·Q/행·중복/산입 기록',True,['sources.jsonl','collectors/cran/integration-audit.json'],'395고유 source ID. 미확인 발행일은 현재 관측시각으로 채우지 않음. 원 수집의 전체 metadata는 collector_record 포인터에 보존.')
add('C15','같은 원고와 보수적 최소수 선택을 분리',True,['evidence/source-deduplication.json','sources.jsonl','collectors/cran/INTEGRATION_AUDIT.md'],'duplicate_group은 같은 member바이트/원고URI; minimum_counting_group은 넓은 보수적 선택. 다른 의미 상태나 부재를 같은본문이라고 주장하지 않음.')
add('C16','HTTP status/final URL/fragment/필요절/용도와 과거 관측을 구분',True,['chains.csv','evidence/cases-normalized.json','RESULT.md'],'BTS200다른대상, httr200anchor없음, RFC같은내용이동, Posit도착anchor존재 반례. 현재상태를2020/2022에소급하지 않음.')
add('C17','모든 A 상류의 역사 전후 본문과 정확 시행시각 확보',False,['chains.csv','evidence/rows/A-D03.md','evidence/rows/A-D05.md'],'Wikipedia2020 revision본문403, 다수 redirect시행기록 부재. 마지막 위치/다음자료는 행별unknowns. 다음 우선자료: 날짜 고정 해당URI 전후본문/공식배포영수증. 현재200으로 역사공백을 채우지 않음.')
add('C18','최초 수정 주장에는 같은 계열 완전 판 목록·중간 실제 HTML 확인',True,['editions.csv','collectors/python/followup/editions.csv','collectors/cran/followup/verification.json','collectors/offline/followup/editions.csv','collectors/offline/AUDIT_ROOT.md'],'Python3.8.2–20/PG12.2–22/선택CRAN계열/httr1.4.1–8 안의 최초로만 한정. source commit만의 변화·문서폐기는 정정에서 분리.')
add('C19','A/B 모든 후속 판과 HTML 노출을 연속 확인',False,['editions.csv','evidence/counts.json','evidence/rows/B04.md'],'SQLite5/51로46판미열람, B03성긴3판, B01/B06versionedweb만, B04과거HTML없음. 다음자료는 sqlite-doc-3310100.zip의 두멤버와 SphinxSitemap2.2.0날짜있는HTML. 표본교체하지 않음.')
add('C20','날짜 역할·정밀도·동일 목적/매체 조건으로만 지연 산술',True,['intervals.csv','chains.csv','evidence/postseal-amendments.jsonl','collectors/offline/AUDIT_ROOT.md'],'strict A0/12 B0/6; 조건부분모0=해당없음. A보조3참조/2소스사건 B1. Python156일은보고→committer nominal; 시행bound null. author/committer/Packaged/mtime을별도시계로유지.')
add('C21','미확인·우측검열·독자실패를 구분하고 양성0을 보존',C['right_censored']==0 and C['same_medium_reader_failure_chains']==0,['intervals.csv','evidence/rows/A-D02.md','RESULT.md'],'시작미상은검열이아님. live/3/당사자1건은offline3.8독자사슬아님. 양성0은조건불충족으로취급하지않으며 표본을바꾸지않음.')
add('C22','서로 다른 분야2쌍·실제 인용 목적과 원자료 최소4개',C['cross_field_pairs']==2 and C['unique_minimum_by_category']['cross_field']>=4,['collectors/cross/REVIEW.md','collectors/cross/citations.json','collectors/cross/sources.jsonl','RESULT.md'],'통계/박물관8원문. ONS7.5/7.6/8.7vintage구분. Lowry는1936표지도식인용이며 작품152연대정정사슬로합치지않음. software분모에합산하지않음.')
add('C23','유지·교체·보류 및 다른 추천/원판 목적의 반례 탐색',True,['RESULT.md','SELF_CHECK.md','evidence/cases-normalized.json'],'유지R03/RFC, 교체D02/R06/B02, 보류R04/B04. dplyrsource수정뒤0.8.5옛본문으로다음릴리스추정반증. 공지예정과실제시행도분리.')
add('C24','A/B 세 보기의 가림 판단·사후원문 대조·비용을 분리 저장',True,['comparisons.csv','evidence/masked/','collectors/cross/L1-receipt.json','collectors/cross/L2-receipt.json','collectors/cross/L3-receipt.json','collectors/cran/B-L1-receipt.json','collectors/cran/B-L2-receipt.json','collectors/cran/B-L3-receipt.json'],'L1/2 A12/B6보류, L3 A11/12행동일치+1보류/B5/6+1보류. 보류를정답으로올리지않음. 재열람0/card50·23을구분.')
add('C25','세 보기 비교가 완전 비노출이며 배포이력만의 효과를 분리',False,['evidence/comparison-protocol-note.md','comparisons.csv'],'A-D04공지요약노출, B03기존curl배경; L3현재상태와이력을동시추가하고수집자카드해석포함. 새비노출판독자에게같은현재증거의current-only/이력추가카드를분리하는것이첫재개행동. 인과효과/실사용자정확도주장금지.')
add('C26','RESULT 첫3표 전표본·필수열, SELF_CHECK Q1–Q8, 마지막약점3행',True,['RESULT.md','SELF_CHECK.md','evidence/rows/'],'첫3표18행씩. RESULT최종약점3행. HANDOFF최종3행은후속인계단계검사. 줄수/로컬링크는deliverable검사에서확인.')
add('C27','핵심 양성·음성·보류 원문 재독 및 내부 독립성 한계 기록',True,['evidence/primary-reread.json','collectors/offline/audit-root.json','collectors/cran/integration-audit.json','SELF_CHECK.md'],'root freshGET4/4. 별도내부archive27/HTML46/description8 재독. 통합27/27. 동일수집자·별도내부판독·외부사람검토를구분.')
common=read('evidence/checks/common-retry-execution.json')
add('C28','저장소 공통 gate를 실제 실행하고 실패도 보존',common.get('exit_code')==0,['evidence/checks/common-check-execution.json','evidence/checks/common-check-receipt.json','evidence/checks/common-retry-execution.json','evidence/checks/common-retry-receipt.json'],'첫localclone에서누락Gitobject로bundle검사실패. 동일고정6ac3d4d를공식원격에서새로clone하여재실행. 코드/검사기변경없음. 후기RESULT문서는별도검산대상. retry영수증이없거나실패면false그대로유지.')
add('C29','제품 실행·설치·부팅·원 독자의 실제 클릭까지 검증',False,['evidence/rows/A-R04.md','evidence/rows/A-D06.md','chains.csv'],'해당실행은미실시. 이연구의출판/본문판정으로그성공을주장하지않음. HANDOFF에고정IDE/Pandoc/rmarkdown입력과필요명령을남긴다. 바이너리판선택자료가먼저필요.')
add('C30','묶음별 원격 커밋과 봉인/관측 입력의 재독 영수증',True,['PROGRESS.md','evidence/a-seal-remote.json','collectors/b/remote-seal-receipt.json'],'①f18b6f8…②168d90b…③ffbce62…④6ac3d4d…고정. 현재결과·수용의원격재독과마지막HANDOFF는이파일을먼저커밋한뒤수행할단계이며완료로소급하지않음.')
receipt={
 'schema':1,'task_id':'AF-RES-032','status':'REVIEW_READY_WITH_GAPS',
 'prepared_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'target_HEAD_before_result_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
 'scope':'Research acceptance on stated working-tree hashes before result commit. Fixed result SHA reread and last HANDOFF commit have separate later receipts.',
 'input_sha256':{n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ['references.jsonl','sources.jsonl','editions.csv','intervals.csv','comparisons.csv','RESULT.md','SELF_CHECK.md'] if (P/n).exists()},
 'counts':C,'conditions':conditions,
 'met_count':sum(x['met'] for x in conditions),'unmet_count':sum(not x['met'] for x in conditions),
 'strict_positive_count_is_not_an_exit_requirement':True,
 'later_handoff_gates':['commit RESULT/SELF_CHECK/acceptance','reread those files at fixed remote SHA','check fixed result HEAD --fetch; record actual exit','only then final separate HANDOFF commit'],
}
(P/'evidence/acceptance-evidence.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'conditions':len(conditions),'met':receipt['met_count'],'unmet':receipt['unmet_count'],'status':receipt['status']},ensure_ascii=False))
