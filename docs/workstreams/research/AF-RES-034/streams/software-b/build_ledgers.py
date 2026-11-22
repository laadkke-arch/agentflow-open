"""Rebuild strand B extraction ledgers from manually read public primary sources.

This performs arithmetic and serialization only. It does not rerun a human study.
The source texts are temporary downloads in tmp/ and are not copied into git.
"""
from pathlib import Path
import json
import math
from datetime import datetime, timezone

P = Path(__file__).resolve().parent
CHECKED = datetime.now(timezone.utc).isoformat()
NCQ_SHA = 'ce14f193f7014c120f04619826cb251818d99b0e'
NCQ_BASE = f'https://github.com/Brittany-Reid/node_code_query/blob/{NCQ_SHA}/'
URLS = {
    'Swb-P01': 'https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf',
    'Swb-P02': 'https://www.cs.mcgill.ca/~martin/papers/vlhcc2017.pdf',
    'Swb-P03': 'https://userlab.utk.edu/files/papers/kim/2016/acar2016you.pdf',
    'Swb-P04': 'https://cs.uwaterloo.ca/~rtholmes/papers/icse_2005_holmes.pdf',
    'Swb-P05': 'https://lucaponzanelli.gitlab.io/assets/publications/Ponz2013a.pdf',
    'Swb-P06': 'https://lucaponzanelli.gitlab.io/assets/publications/Ponz2015c.pdf',
    'Swb-P07': 'https://brittany-reid.github.io/publication/reid-2023-ncq/reid-2023-ncq.pdf',
    'Swb-A01': NCQ_BASE+'docs/instructions.md',
    'Swb-A02': NCQ_BASE+'data/user-study/codesnippets1.csv',
    'Swb-A03': NCQ_BASE+'data/user-study/codesnippets2.csv',
    'Swb-A04': NCQ_BASE+'data/scripts/user-study-snippets.js',
}
receipts = {r['file']: r for r in json.loads((P/'download-receipts.json').read_text())['files']}

def source(sid, family, title, publisher, date, loc, verified, limits, cat, filename=None, doi=None, version=None):
    r = dict(source_id=sid, study_family=family, title=title,
             material_type='primary_human_study' if cat=='software_primary' else 'original_artifact' if cat=='artifact' else 'primary_nonhuman_evaluation',
             publisher=publisher, original_url=URLS[sid], fixed_url=URLS[sid], published_date=date,
             version=version or ('author_publication_copy; content hash fixed below' if filename else NCQ_SHA),
             checked_utc=CHECKED, read_locator=loc, verified_content=verified,
             questions=['Q1','Q2','Q3','Q4','Q5','Q6','Q8'], claim_ids=['C-'+family],
             limitations=limits, duplicate_group=family, count_category=cat,
             count_minimum=(cat in ('software_primary','artifact')), opened_full_text=True,
             required_content_verified=True, observation_grade='D2' if cat=='artifact' else 'D1')
    if doi: r['doi']=doi
    if filename:
        r.update(content_sha256=receipts[filename]['sha256'], bytes=receipts[filename]['bytes'], local_temporary_path='tmp/'+filename)
    return r

sources = [
source('Swb-P01','SWB-EXO','Enriching Documents with Examples: A Corpus Mining Approach','ACM TOIS 31(1), Article 1','2013-01',
       ['§1–3 pp1–12 intervention/interface','§5.1–5.3 pp19–22; Tables X–XII','§6–7 pp23–26 limitations and references'],
       'POSTECH 학부생 24명을 Java 실력 4수준별 무작위로 12명씩 배정. java.sql 무경험. 같은 서버의 원 JavaDocs 대 eXoaDocs. 40분 네 JDBC 과제. Table X 시간은 완료자만의 누적 문서 탐색 기반 추정값: 8:53/14:40,23:34/25:03,30:32/32:03. Table XII 테스트 통과자 eXo11,11,3,3 대 원문10,8,4,1. 전체 과제 통과3/12 대1/12.',
       '시간의 정확한 n은 Table X에 없음; Table XII의 테스트 분모와 자동으로 동일시하지 않음. 다음 과제 문서를 30초 이상 본 시점으로 전이를 추정. UI·API 인기도·예제 요약 함께 변경. 기존 JavaDocs에도 수작업 예제 있음. 장기 재작업 미관측. 2009/2010 선행판은 같은 연구군으로 연결하고 별 표본으로 세지 않음.',
       'software_primary','exo.pdf','10.1145/2414782.2414783'),
source('Swb-P02','SWB-REST','A Study of the Effectiveness of Usage Examples in REST API Documentation','IEEE VL/HCC pp53–61','2017',
       ['§III pp54–57 recruitment, task table, allocation, protocol and coding','§IV pp57–59 Fig4 and observations','§V–VI pp59–61 validity and references'],
       '26명 경력 개발자: 원 문서16명, 예제 강화 문서10명. 사용자 정의 explorer가 불균등 무작위 배정. WordPress REST API 신규 사용자, 다섯 본과제와 연습1개, 한 시간. 두 군 모두 자유 인터넷 허용. cURL 요청·응답·헤더 예제3개 추가. 과제당 성공·시간을 사람 수로 나눔. 시간 Wilcoxon p=.051, API 시도 p=.017, 성공 Fisher p=.0003. 형식 오류는 원군에서 더 자주 관측.',
       '그림4 정확한 평균 수치와 개인별 시간 원자료는 공개 본문 텍스트에서 미확인. 반복 과제 의존성 및 T6의 T5 의존. 539 API calls라 쓰나 385+152=537로 불일치. 시간차 유의확정 또는 동등 품질 시간절감으로 단정 불가. 후속 재설계 관측 없음.',
       'software_primary','rest.pdf','10.1109/VLHCC.2017.8103450'),
source('Swb-P03','SWB-ACAR','You Get Where You’re Looking For: The Impact of Information Sources on Code Security','IEEE S&P pp289–305','2016',
       ['§IV pp293–295 recruitment/allocation/tasks/scoring','§V pp295–299; Table II; functionality/security result tables and figures','§VIII–IX pp301–303 limitations/conclusion; refs pp303–305'],
       '참가56 중 배정오류·거부 각1명을 제외하여 분석54명. 공식13,SO13,책14,자유14. 네 Android 과제216시행. 방법에는 round-robin, 결과에는 randomly assigned라 배정 서술 충돌. 기능성 SO35/52,공식21/52,책37/56,자유29/56. 기능 완료자 안의 보안 SO18/35,공식18/21,책27/37,자유19/29. 사람당 반복 과제 CLMM. 실제 완료시간의 군별 값은 보고되지 않고 약20–30분 예산만 있음.',
       '보안 분모가 성공자에 조건부. SO와 공식의 기능+보안 동시달성은 모두18/52지만 표본 작아 등가 입증이 아님. 원56 전원 ITT 결과 미공개. 자료원 제한·검색가능성·정보품질이 함께 변함. 책/공식/온라인 효과를 링크 하나의 효과로 환산 불가. 장기 앱 정적분석은 같은 참가자의 추적이 아님.',
       'software_primary','acar.pdf','10.1109/SP.2016.25'),
source('Swb-P04','SWB-STRATH','Using Structural Context to Recommend Source Code Examples','ACM/IEEE ICSE pp117–125','2005',
       ['§2–4 pp118–121 tool and examples','§5 pp121–123 Table2 and task narratives','§6–8 pp123–125 limitations and references'],
       '개발자2명×4과제=8시행, 대조군 없는 사례 관찰. 모두 해법을 몰랐으며 Java/Eclipse 경험은 서로 다름. 같은 순서, 3시간 상한. 7성공+1부분성공. task3은 의도적으로 핵심예제 부재; 두 명은15분 이내 검색을 포기하고 표준IDE로 해결하되 Color 하위문제 예제는 사용. task4 한 사람은 잘못된 seed 질의 후 부분성공.',
       '전체 과제 완료시간 미보고. 15분 이내는 포기까지 관찰 상한이지 평균 절감 시간이 아님. 구조 요약·선택 이유·예제코드가 함께 제공됨. 4–12초 서버 응답시간을 사람 노동으로 세지 않음. Table2의 useful0은 핵심 query 결과이며 전체 하위문제 예제사용0과 같지 않음.',
       'software_primary','strathcona.pdf','10.1145/1062455.1062491'),
source('Swb-P05','SWB-SEA','Leveraging Crowd Knowledge for Software Comprehension and Development','IEEE CSMR pp57–66','2013',
       ['§II–III pp58–62 tool and illustrative scenario','§IV pp63–65 all three evaluations','§V–VI pp65–66 limits/references'],
       '세 실험은 35개 Java 연습문제,10개 스텁,7개 완성 메서드에 대한 관련성 평정. 실제 개발자 과제 수행/노동 측정 연구가 아님. Alice 사례는 실증 증거가 아니라고 §IV가 직접 설명. 간단한/일반적인 스텁에서는 관련문서가 거의 없고 맥락 풍부한 메서드에서는 관련도가 높음.',
       '사람 대상 비교 표본·실행 시간·품질 최종 제출 없음. 알고리즘 관련성 평가를 human experiment로 잘못 세지 않음. Prompter와 저자·목표가 겹치지만 별 도구/별원문. 인간 연구 최소수 제외.',
       'excluded_nonhuman','sea.pdf'),
source('Swb-P06','SWB-PROMPT','Prompter: Turning the IDE into a Self-confident Programming Assistant','Springer Empirical Software Engineering 21(5) pp2190–2231','2016',
       ['§2 tool/interface','§3 Study I and §5 replication: rating cohorts kept separate','§4 pp18–25 of 42-page author copy; Table4/5 and Fig8; quantitative §4.4 p23','§6–8 validity and related work'],
       'Study II: 학생6·산업개발자6 총12명이 서로 다른 유지보수/신규개발 과제를 도구 있음/없음으로 각각90분씩 수행. 경험을 분산한4군이 과제·도구순서를 균형화. 자유 인터넷 허용. 조건을 모르는 산업 평가자2명이 가중 체크리스트로24산출물을 평가,불일치4건 토론해소. 완성도 평균70% 대46%,중앙68% 대40%; paired p<.01. 유지보수 부분집합 p=.23,신규개발 p=.03.',
       '시간은 동일 상한90분이고 완료시각 차이를 보고하지 않음. 완성도 상승을 분 단위 절감으로 바꿀 수 없음. prior familiar solution 개별 측정 미확인. 사용 자기보고3+8+2=13인데 연구N12인 서술 불일치. StudyI33명·1년뒤평정18명은 새 노동표본으로 합산하지 않음. 별도 패키지URL 접근 실패.',
       'software_primary','prompter.pdf','10.1007/s10664-015-9397-1',version='42-page author publication copy; ©2015, journal volume2016'),
source('Swb-P07','SWB-NCQ','NCQ: Code Reuse Support for Node.js Developers','IEEE TSE 49(5) pp3205–3225','2023',
       ['§2 concrete workflows pp2–3','§7 pp7–11 first study tasks/assignment/logs/results','§10 pp13–17 second study and snippet coding','§11–13 pp17–20 discussion/threats/references'],
       '별 코호트10+10명,각2과제=40시행. 연구1 검색없는NCQBasic+웹 대 NCQRetrieval,연구2 VSCode+웹 대 개선NCQ. 두 연구 모두 baseline 먼저,다른 과제를 순환 배정. 전원 과제 성공. 연구1 중앙 총시간936→748초;연구2 849→847초. 연구2 최종 패키지 선택 중앙380→57초. 영상·명령 timestamp·웹열람 전사로 관측. 코드 조각 shown/attempted/successful use를 구분. 자동수정은 lint오류를 줄였지만 runtime오류 감소는 없었음.',
       '순서 균형 없음,같은 사람이 다른 과제를 풀어 paired duration 차이에는 난도 차이가 포함. 20분은 예상 소요이지 엄격한 censoring 상한으로 확인 안 됨. 단순 정해진 출력 충족만 평가. 개선판 대 구판 평균 비교1045→774초는 다른 코호트·기초실력·기준도구도 바뀌어 인과효과로 쓰지 않음. 기간후 재작업 미관측.',
       'software_primary','ncq.pdf','10.1109/TSE.2023.3248113',version='arXiv:2101.00756v3 dated2023-01-02, author-hosted 20-page manuscript'),
source('Swb-A01','SWB-NCQ','NCQ original command instructions','Brittany Reid, original GitHub repository','2020-08-31',
       ['docs/instructions.md complete file; CLI,REPL,Search Functionality,Keybindings'],
       '원도구 명령·키 사용 지시문을 직접 읽음. package검색은 상위25개를 제공하고 samples는REPL입력에코드를 삽입해 순환열람. install/uninstall/editor/save와 검색 모드가 같은 도구에 결합. 논문 §7.1.5가 실험 중 key/command문서를 제공했다고 명시.',
       '이 파일의 정확한 판이 각 실험 참가자에게 제시되었는지는 미확인. 실험용 task brief·채점표가 아닌 도구 조작지시문으로 구분. 명령동작·화면의 원산출물이며 시간 결과를 재계산할 데이터는 아님.',
       'artifact'),
source('Swb-A02','SWB-NCQ','NCQ study1 snippet observation dataset','Brittany Reid, original GitHub repository','2022-04-07',
       ['codesnippets1.csv header and all142parsed records; P1–P10,T1/T2; snippets and error labels inspected','Swb-A04 comments map filename to first study'],
       '142행,그중1행은P2,T1의 빈 snippet placeholder. 필드P,T,Package,Snippet,Used?,Runs?,Error. Used?1이41행,0이100행. 실제 노출/사용/실행 오류 코딩의 독립 원자료. author script가first user study 파일로 명시. byte hash로 고정.',
       '행은 사람이 아닌 코드 조각. 시간·군 이름·전체최종정답·successful reuse 별도열 없음. P번호를 논문과 조인할 때 연구ID 필요. cp1252로 해석;UTF-8엄격읽기 실패기록 보존. snippet수의 오류율을 사람 실패율로 바꾸지 않음.',
       'artifact','codesnippets1.csv',version=NCQ_SHA),
source('Swb-A03','SWB-NCQ','NCQ study2 snippet observation dataset','Brittany Reid, original GitHub repository','2022-04-07',
       ['codesnippets2.csv header and all156parsed records; P1–P10,T1/T2; snippets and error labels inspected','Swb-A04 comments map filename to second study'],
       '156행,Used?1이38행,0이118행. 첫 파일과 같은 필드이나 다른 코호트의 별개 관측. P1–P10이 재사용되므로 study2 식별자를 붙여야 함. author script가second user study파일로 명시해 두 파일의 대응을 해결.',
       '저자에 의해 원래 분리된 두 코호트 자료이며 분석자가 파일을 임의 분할한 것이 아님. 완결된 시간 raw자료나 평가 rubric은 아님. 화면에부분만보인snippet은 모 논문 규칙에 따라제외되므로 모든정보노출의분모가아님.',
       'artifact','codesnippets2.csv',version=NCQ_SHA),
source('Swb-A04','SWB-NCQ','NCQ original snippet lint analysis script','Brittany Reid, original GitHub repository','2022-04-07',
       ['data/scripts/user-study-snippets.js complete file; comments,filename mappings,lintFile,main'],
       '원분석 실행 코드가 CSV의4번째열을 LinterHandler.lint에 넣고 오류수 errors.length를 출력. 첫/둘째 study CSV를 명시하며 기본main은첫파일만실행,둘째는주석. 결과를Google sheet에옮겼다는저자주석. 두원자료의cohort매핑과lint평가산식을확인.',
       '전체 runtime 오류·최종 task정답·시간 검증 스크립트는아님. 외부패키지 설치/새실험은 실행하지않고 정적 판독만. 재실행시두파일을한번씩택해실행해야하며패키지판을고정해야함. 논문 Figure28 전수재생영수증으로 주장하지않음.',
       'artifact'),
]

def partial_source(sid, family, url, title, publisher, date, locator, verified, limitation, kind='primary_paper_partial'):
    return dict(source_id=sid,study_family=family,title=title,material_type=kind,publisher=publisher,
                original_url=url,fixed_url=url,published_date=date,version='public version observed2026-11-22',
                checked_utc=CHECKED,read_locator=locator,verified_content=verified,questions=['Q1'],
                claim_ids=['C-search-bounds'],limitations=limitation,duplicate_group=family,
                count_category='discovery_only',count_minimum=False,opened_full_text=(kind!='author_project_page'),
                required_content_verified=False,observation_grade='D1' if kind!='author_project_page' else 'D0',
                full_outcome_extraction_completed=False)

sources.extend([
 partial_source('Swb-X01','SWB-EXAM', 'https://tianyi-zhang.github.io/files/chi2018-examplore.pdf',
  'Visualizing API Usage Examples at Scale','ACM CHI','2018',
  ['PDFpp1–2abstract/introduction','pp9–10feedback/limitations','pp11–12references'],
  'API예제시각화와웹탐색을16명에게비교한관련후보. REST제목으로전방검색시반환되었으나논문reference에Sohan없음.',
  'Methods/정량원표전체추출을수행하지않았으므로원연구최소수에추가하지않음. 검색결과반환을실제인용관계로보지않음.'),
 partial_source('Swb-X02','SWB-GORSKI','https://pub.h-brs.de/frontdoor/deliver/index/docId/5631/file/Gorski2021_IJustLookedForTheSolution.pdf',
  'I just looked for the solution! On Integrating Security-Relevant Information in Non-Security API Documentation to Support Secure Coding Practices','IEEE TSE author postprint','2021',
  ['PDFpp1–2abstract/introduction; indexedreferences17/18 discovered','repeatfindreturnedbotpage'],
  '49명CSP문서3변형사람연구후보이며Acar2016을reference17로인용하는저자본경로발견. 최초PDF원문서두열림,재열람시봇확인문서로바뀜.',
  '세부배정·시간분모·원표미검증. 검색요약수치나abstract주장을효과행에넣지않음. 기관저장소접근복구후Methods/결과표가다음자료.'),
 partial_source('Swb-X03','SWB-NCQ','https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume14/issue04/24172/DagRep.14.4.108/DagRep.14.4.108.pdf',
  'Code Search: Dagstuhl Seminar24172 report','Schloss Dagstuhl','2024',
  ['pp108–110overview','§3.13p118','§3.18pp119–120'],
  '§3.13에서NCQ2023을Mainreference로명시. §3.18는로그만으로답발견과포기를구별하기어렵다고설명.',
  '세미나보고로별도의사람성과실험이아님. NCQ결과를재요약한부분을신규표본/원산출물로세지않음.'),
 partial_source('Swb-X04','SWB-APISONAR','https://onlinelibrary.wiley.com/doi/abs/10.1002/spe.2906',
  'APISonar: Mining API usage examples','Wiley Software: Practice and Experience','2021',
  ['publisherabstractlines87–91','reference16lines150–154'],
  'eXoaDocs2013의전방인용16을실제출판사참고문헌에서확인. 프로젝트코퍼스와사용자방문기록평가를개요로설명.',
  '본문Methods를전수심사하지않음;사용방문통계를사람노동효과로쓰지않음. 전문접근후평가방법재판독필요.'),
 partial_source('Swb-X05','SWB-CERIT','https://www.cs.cit.tum.de/fileadmin/w00cfj/sebis/thesis/190915_Cerit_Thesis.pdf',
  'Improving the Developer Experience of API Consumers using Usage Scenarios and Examples','Technical University of Munich master thesis','2019-09-06',
  ['abstractpIII;PDFp5','relatedworkprintedp19;PDFp31','reference43printedp113;PDFp125'],
  'Sohan2017에대한실제전방인용확인. 두군의개발자에게문서를달리제공하는연구를초록에서설명. API제공자와사용자의서로다른관점을다루는후속후보.',
  '126쪽전체방법/표를추출하지않음. 논문최소수/효과수치에미산입. 후속재심사첫자료는§5–6task/experiment.'),
 partial_source('Swb-X06','SWB-JAIN','https://winlab.rutgers.edu/~shubhamj/papers/USEC14apistudy.pdf',
  'Should I Protect You? Understanding Developers’ Behavior to Privacy-Preserving APIs','USEC2014 author manuscript','2014',
  ['PDFp1abstract/introduction;Acarreference21'],
  'Acar의후방인용원문을열어25명API재설계실험임을확인.',
  'API기능선택지자체를변경하므로선례/링크제공단독효과와다름. 전체원표심사미완료로human최소수에미산입.'),
 partial_source('Swb-X07','SWB-NCQ',NCQ_BASE+'README.md','NCQ README usage guide','Brittany Reid GitHub','2021-10-10',
  ['completeREADMEinstallation/dataset/example/usage'],
  'NCQ검색·설치·수정·REPL결합을확인. Zenodo5094598은NPMpackagecorpus이며사람시간rawdataset이라고주장하지않음.',
  '독립지시문A01과사용설명이겹쳐추가산출물최소수에산입하지않음.',kind='tool_documentation'),
 partial_source('Swb-X08','SWB-PROSPECTOR','https://homes.cs.washington.edu/~bodik/ucb/research/prospector.html',
  'Prospector project page','Rastislav Bodik author site','2005',
  ['projectdescription andpaperlink'],
  'Jungloid mining원논문경로발견. BerkeleyPDF링크는redirect후실패했고Washington복사경로도실패.',
  '논문전문미열람. querybenchmark와humanstudy를검색요약으로대체하지않음. CiteSeer원문이대체후보.',kind='author_project_page')
])

def study(sid,family,source_id,grade,n,trials,arms,**kw):
    return dict(study_id=sid,study_family=family,source_ids=[source_id],source_url=URLS[source_id],
                comparison_grade=grade,product_directness='B',participants_analyzed=n,trials_analyzed=trials,
                allocation_unit='person' if sid not in ('SWB-PROMPT-2','SWB-NCQ-1','SWB-NCQ-2') else 'person-period',
                arms=arms,post_adoption_rework_start=None,post_adoption_rework_window=None,
                post_adoption_rework_value=None,post_adoption_rework_reason='채택/최종 제출 후 다음 수정 시점으로 이어지는 비교 추적 없음',**kw)

studies=[
study('SWB-EXO-1','SWB-EXO','Swb-P01','R',24,96,
      [{'arm':'eXoaDocs','n_assigned':12,'test_pass_by_task':[11,11,3,3],'entire_task_pass':3}, {'arm':'JavaDocs','n_assigned':12,'test_pass_by_task':[10,8,4,1],'entire_task_pass':1}],
      n_enrolled=24,n_excluded=None,n_excluded_status='보고된 추가 제외 없음',
      task='JDBC 연결→statement생성→query실행→결과표시; 모든참가자4선형과제',prior_knowledge='설문Java4등급;java.sql개발경험 없음',experience='POSTECH CS학부생',
      assignment='Java4숙련층 내 무작위 배정; 각군수준분포동일',order='두군 동일 선형과제 순서',
      intervention='과제 전 eXoaDocs 문서접근; 원코드에서추출·요약·정렬한예제+API인기도bars',comparator='같은서버 원JavaDocs;ResultSet등 수작업예제 이미 포함',
      changed_together='예제존재·선택·요약·인기도·문서 UI',timing='주어진문서를필요시조회',
      shown='eXoaDocs문서할당12',opened='문서URL로그;각예제열람자수 미확인',adopted='자기보고 예제사용10/12 대4/12',
      time_measurement='자동 document-access log; next task문서를30초넘게본시점으로 tasktransition 추정',time_start='세션시작에대한누적값',time_end='다음과제문서접근/최종과제 완료 추정',time_budget_minutes=40,
      time_denominator='각과제 완료자만; TableX의정확한n 미명시',quality_definition='같은test suite 실행출력일치/불일치',quality_denominator='12/arm/task',quality_blinding='미확인',
      censoring='미완료자는시간평균에서제외;실패/미완료가대부분최종과제에남음',independent_reanalysis=False,
      limitations='TableX시간완료와TableXII테스트통과사람의조인 미공개; 속도이점이품질차/선택효과와분리안됨'),
study('SWB-REST-1','SWB-REST','Swb-P02','R',26,130,
      [{'arm':'G1 original','n_assigned':16},{'arm':'G2 enhanced','n_assigned':10}],n_enrolled=26,n_excluded=None,n_excluded_status='본연구제외 미보고;pilot4명/7명은 별도이며분모에서제외',
      task='WordPress RESTV2에서5본과제(T2–T6),연습T1별도;저자검색,ID제외,헤더총개수,날짜게시,수정',prior_knowledge='WP RESTV2무경험,업계/REST1년이상',experience='16개기업6개국 전문가;industry평균9.1/10.6yr,REST4.5/4yr',
      assignment='custom explorer unequal random allocation;G1더많이설정',order='공통과제순서;T6는T5결과에의존',
      intervention='과제시작전강화문서링크,cURL요청/응답/헤더현실값예제3개',comparator='원문서링크,동일explorer,인터넷자유사용',changed_together='예제정보량·구체형식/헤더가함께추가;barelink비교아님',
      timing='과제전문서링크제공후자유탐색',shown='강화문서할당10',opened='예제별조회로그미공개',adopted='피드백7/10예제도움;코드별채택정량은미확인',
      time_measurement='APIcalltimestamp있는exporttable',time_start='과제시작경계 세부구현미공개',time_end='만족/막힘에따른다음과제이동;첫정답call과완료시간구별',time_budget_minutes=60,
      time_denominator='task별합/군참가자수;정확시계값표없음',quality_definition='I1method,I2URL,I3headers,I4body로success/partial/failure;다중calltask부분성공',quality_denominator='16/10 per task;T5/T6실제시도원군15명관찰도별도',quality_blinding='코딩82/539crosscheck,27불일치조정;전체맹검미확인',
      censoring='포기/시간초과구분표없음;원군T5/T6미시도1명',independent_reanalysis=False,
      limitations='Figure4평균그래프뿐. p시간=.051,동등품질시간차미입증. 539 대537시도총계충돌'),
study('SWB-ACAR-1','SWB-ACAR','Swb-P03','Q',54,216,
      [{'arm':'SO','n_assigned_analyzed':13,'functional':35,'trial_n':52,'secure_among_functional':18}, {'arm':'official','n_assigned_analyzed':13,'functional':21,'trial_n':52,'secure_among_functional':18}, {'arm':'book','n_assigned_analyzed':14,'functional':37,'trial_n':56,'secure_among_functional':27}, {'arm':'free','n_assigned_analyzed':14,'functional':29,'trial_n':56,'secure_among_functional':19}],
      n_enrolled=56,n_excluded=2,n_excluded_status='배정오류1·과제거부1;각제외자의군/결과미공개',
      task='Android skeleton의HTTPS,ICC,credentialstorage,전화permission4과제',prior_knowledge='Androidcourse또는1년경력;screening3/5MCQ;각해법이미알았는지미측정',experience='professional14/nonprofessional40;48명이학생(일부직장겸업)',
      assignment='Methodsround-robin;Resultsrandomlyassigned불일치→보수적Q',order='4과제무작위순서;첫과제시간더허용',
      intervention='SO만/공식문서만/PDF책2권만/자유자료의4조건',comparator='모든조건간비교;SO대공식을대표로추출',changed_together='검색범위·인터페이스·예제품질·접근성',timing='작업중요청시검색',
      shown='자료원접근을허용/차단하는정책,특정링크노출아님',opened='브라우저URLJSON수집,책은동등로그없음',adopted='작성코드두독립코더가전략판독;단순열람≠채택',
      time_measurement='완료시간군별집계없음;deadline약20–30분만보고',time_start='과제지시',time_end='완료또는시간종료',time_budget_minutes='20–30 per task;first longer',time_denominator='실제time결과미보고',
      quality_definition='compile+task기능1/0;기능성공자만secure1/0;두코더독립판정후합의',quality_denominator='기능216분모;보안기능122분모;전등록224ITT미확인',quality_blinding='독립코더2이나조건맹검미확인',censoring='시간내미완료기능0;사후제외2명은분모밖',independent_reanalysis=False,
      limitations='반복측정CLMM원보고를사용;단순시행독립CI금지. joint18/52동률은등가결론아님'),
study('SWB-STRATH-1','SWB-STRATH','Swb-P04','O',2,8,
      [{'arm':'Strathcona','n_assigned':2,'completed_trials':7,'partially_completed_trials':1}],n_enrolled=2,n_excluded=None,n_excluded_status='추가제외미보고',
      task='Eclipse상태줄,AST생성,텍스트강조,메서드시그니처4과제',prior_knowledge='두명모두해법모름이라고명시',experience='Java>8yr/Eclipse<1mo 대 Java18mo/Eclipse>6mo',
      assignment='단일군편의표집',order='두명동일순서',intervention='skeleton구조로예제10개추천+구조요약+선택이유+코드',comparator='없음',changed_together='skeletonseed·도구·요약·선택이유',timing='작업중요청시',shown='query당10예제',opened='Table2sourceviewcount:[1,2,2,2]및[1,6,6,7]',adopted='Table2핵심예제사용수[1,1,0,1]대[1,1,0,0];task3Color예제별도사용',
      time_measurement='정량완료시간미보고',time_start='과제시작',time_end='과제완료/3시간상한',time_budget_minutes=180,time_denominator='해당없음;timecontrast없음',quality_definition='과제성공/부분성공실행관찰,독립채점표미공개',quality_denominator='8trials/2people',quality_blinding='미확인',censoring='task4한명부분성공',independent_reanalysis=False,
      limitations='3개과제저자도구개발경험에서선정. 잘못된queryseed에서실패. causal효과없음'),
study('SWB-PROMPT-2','SWB-PROMPT','Swb-P06','R',12,24,
      [{'arm':'Prompter','n_people':12,'n_trials':12,'mean_quality_percent':70,'median_quality_percent':68}, {'arm':'NoPrompter','n_people':12,'n_trials':12,'mean_quality_percent':46,'median_quality_percent':40}],n_enrolled=12,n_excluded=None,n_excluded_status='24산출물모두평가;제외미보고',
      task='2D게임유지보수4요구 대 HTML→PDF→email신규개발3요구',prior_knowledge='자기보고경력/실력만측정,구체해법미리앎미확인',experience='BSc3,MSc3,industrial6;Java경력중앙4yr;일반6.5yr',
      assignment='경험균형4group;두조건·두과제·두순서교차균형. 개별random여부미명시',order='Table4:A MT-Pr→DT-NoPr;B MT-NoPr→DT-Pr;C DT-Pr→MT-NoPr;D DT-NoPr→MT-Pr',
      intervention='IDE가현재코드맥락SO자료검색/순위/threshold알림',comparator='같은IDE에서Prompter없음,두조건모두자유인터넷',changed_together='context추천·랭킹·알림·검색자동화',timing='작업중자동알림;사전훈련별개task',shown='알림조건존재,실제개수전수표없음',opened='미확인',adopted='자기보고3+8+2=13 vsN12불일치,정확비율계산안함',
      time_measurement='90minfixedbudget;completiontime별도없음',time_start='세션시작',time_end='90min제출',time_budget_minutes=90,time_denominator='모든24시행동일허용시간,실제소요시간분포없음',
      quality_definition='조건/목적모르는독립산업평가자2명code-review가중체크리스트;MT15/25/35/25%;24중4불일치합의',quality_denominator='12scores/condition;6perconditionpertask',quality_blinding='평가자조건/목적맹검명시',censoring='미완성부분도완성도점수로유지',independent_reanalysis=False,
      limitations='일정시간내품질비교,노동절감시계가없음. MT p.23는효과없음입증아님'),
study('SWB-NCQ-1','SWB-NCQ','Swb-P07','Q',10,20,
      [{'arm':'NCQRetrieval','n_people':10,'n_trials':10,'completed_trials':10,'median_total_seconds':748}, {'arm':'NCQBasic+Web','n_people':10,'n_trials':10,'completed_trials':10,'median_total_seconds':936}],n_enrolled=10,n_excluded=None,n_excluded_status='탈락미보고',
      task='5개Node작업에서각인원서로다른2개:파일읽기,mergesort,CSV생성,MySQL조회,그래프DFS',prior_knowledge='기본Node자격요구하지만실력검사없음,특정package해법선행지식미확인',experience='온라인모집,평균Node2yr;다수학생',assignment='순환배정표2회반복;각task조건별2명. baseline항상먼저',order='NCQBasic먼저→NCQRetrieval나중',
      intervention='NCQ안의package/code검색',comparator='같은NCQ에서검색제거+자유웹',changed_together='검색내장/코퍼스/순위;둘째조건연습효과',timing='작업중검색;공통demo사전제공',shown='명령로그로samples의모든전체snippet',opened='웹영상에전체보인snippet전사',adopted='seen/attempted/successful-use구별;원CSV별도Swb-A02',
      time_measurement='화면/오디오·timestamp명령·영상웹행동전사',time_start='각과제시작',time_end='taskdescription충족JSfile제출',time_budget_minutes='각20분예상;엄격중단상한미확인',time_denominator='10/condition,전원완료',quality_definition='실행시과제설명출력충족',quality_denominator='10/10각조건',quality_blinding='instructorfirstauthor;맹검미확인',censoring='allcompleted;예상20분넘는time도그림에존재',independent_reanalysis=False,
      limitations='936/748은군중앙의차이지pairedmedian차이아님. 난도·학습교란'),
study('SWB-NCQ-2','SWB-NCQ','Swb-P07','Q',10,20,
      [{'arm':'NCQ','n_people':10,'n_trials':10,'completed_trials':10,'median_total_seconds':847,'median_final_package_seconds':57}, {'arm':'VSCode+Web','n_people':10,'n_trials':10,'completed_trials':10,'median_total_seconds':849,'median_final_package_seconds':380}],n_enrolled=10,n_excluded=None,n_excluded_status='탈락미보고;55명선행survey의subset10이므로추가55명합산안함',
      task='연구1과같은5task중2개/사람',prior_knowledge='Prolificscreeningprogrammingquestions;구체해법선행지식미확인',experience='평균Node3yr,실력검사;별코호트10명',assignment='연구1과동일task순환배정;baseline항상먼저',order='VSCode+Web먼저→NCQ나중',
      intervention='수정NCQ:검색·package설치·REPL·자동lint수정·ranking',comparator='확장없는깨끗한VSCode+자유인터넷+terminal',changed_together='IDE/인터페이스·자동수정·검색·순위·코퍼스',timing='작업중검색;공통demo',shown='samples로그',opened='웹영상의완전노출snippet',adopted='seen/attempted/successful사용단계;Swb-A03는Used?/Runs?가있으나success별도열없음',
      time_measurement='화면/오디오·timestamp명령·영상웹행동전사',time_start='각task시작',time_end='출력요구충족JSfile제출',time_budget_minutes='각20분예상;엄격중단상한미확인',time_denominator='10/condition,전원완료',quality_definition='동일task목표출력충족;lint/runtimesnippet오류별도분석',quality_denominator='10/10각조건',quality_blinding='조건맹검미확인',censoring='allcompleted',independent_reanalysis=False,
      limitations='중앙849→847초거의같음은등가검정아님. 검색단계380→57을총시간절감으로바꾸지않음. 장기rework없음'),
]

effects=[]
def effect(eid,family,sid,loc,measure,control,intervention,unit,denom,kind='mean',**kw):
    effects.append(dict(comparison_id=eid,study_family=family,source_ids=[sid],source_url=URLS[sid],read_locator=loc,
                        original_control=control,original_intervention=intervention,unit=unit,measure=measure,
                        statistic=kind,denominator=denom,formula='intervention-control;intervention/control;100*(intervention/control-1)',
                        absolute_difference=intervention-control,ratio=intervention/control if control else None,
                        percent_change=100*(intervention/control-1) if control else None,
                        calculation_status='recalculated_descriptive_from_reported_values',**kw))
for i,(c,t) in enumerate([(880,533),(1503,1414),(1923,1832)],1):
    effect(f'SWB-E{i:02}','SWB-EXO','Swb-P01','Table X p1:20',f'cumulative task completion time T{str(i) if i<3 else "3+4"}',c,t,'seconds','task completers only; exact TableX n unstated',
           quality_pair='TableXII separate pass counts per12;cannotlinkexactpersons',missingness='noncompleters omitted from time',
           uncertainty='T1 source arm90%CIs [644,1117]control,[269,796]intervention;SD/covariance absent,no CI difference;T2/3/4none',
           reversal_condition='누락된비완료자의노동/품질을고려하면완료자속도차와전체노동효과가달라질수있음')
effect('SWB-E04','SWB-EXO','Swb-P01','Table XII p1:21','all-task test-pass proportion',1/12,3/12,'proportion','12assigned/arm','risk',
       original_counts={'control':1,'intervention':3,'n_each':12},missingness='미완료·불통과분모유지',uncertainty='작은표본;시간완료자와joint원자료없음',reversal_condition='기능시험밖유지보수/보안품질을보면동등품질주장안됨')
for eid,meas,c,t,denom in [('SWB-E05','functional proportion',21/52,35/52,'52trials/arm =13analyzedpeople×4'),('SWB-E06','secure given functional',18/21,18/35,'21functional official;35functional SO'),('SWB-E07','functional and secure among analyzed assigned',18/52,18/52,'52trials/arm')]:
    effect(eid,'SWB-ACAR','Swb-P03','§V-B pp296–298',meas,c,t,'proportion',denom,'risk',
           missingness='56enrolled→54analyzed;excluded2unknownarms;securityconditionalonly',uncertainty='CLMMoriginalaccountsrepeats;noindependenttrialCIrecalculated',
           reversal_condition='조건부보안순위와배정전체의jointsuccess순위가다르다;18/52동률은populationequivalence아님')
effect('SWB-E08','SWB-PROMPT','Swb-P06','§4.4 Fig8 (author PDF p23)','completeness at90min',46,70,'percentage points','12people/condition;24pairedtasks','mean',
       missingness='partialartifactsretained',uncertainty='sourcepairedWilcoxonp<.01,Cliffd=.65;individualscoresabsent',
       reversal_condition='MT하위과제p=.23;품질상승을절감시간으로환산하려면같은품질까지의실제시간이필요')
effect('SWB-E09','SWB-PROMPT','Swb-P06','§4.4 Fig8 (author PDF p23)','completeness at90min',40,68,'percentage points','12people/condition','median',
       missingness='partialretained',uncertainty='mediancontrastnotpairedmedian;noCI',reversal_condition='MT/DT과제에따라효과크기다름')
effect('SWB-E10','SWB-NCQ','Swb-P07','§7.2.1 authorPDFp9;Fig11','total task completion',936,748,'seconds','10people/condition;allcompleted','median',
       missingness='noobservednoncompleters',uncertainty='no inferential uncertainty reconstructed;individualtimeCSVnotfound',reversal_condition='baseline항상먼저,각사람서로다른과제;학습/난도교란')
effect('SWB-E11','SWB-NCQ','Swb-P07','§10.2.1 authorPDFp14;Fig20','total task completion',849,847,'seconds','10people/condition;allcompleted','median',
       missingness='noobservednoncompleters',uncertainty='noequivalenceCI;differenceofmediansonly',reversal_condition='−2초는동등성입증도명확한절감도아님;분포넓고N10')
effect('SWB-E12','SWB-NCQ','Swb-P07','§10.2.2 authorPDFp14;Fig21','time to final package selection',380,57,'seconds','10people/condition','median',
       missingness='finalpackageusedforcompletionallcases',uncertainty='noCI;stagedurationonly',reversal_condition='최종제출총시간은849→847초;초기검색절감이이후개발/검증비용으로상쇄가능')
effects.extend([
 dict(comparison_id='SWB-E13',study_family='SWB-REST',source_ids=['Swb-P02'],source_url=URLS['Swb-P02'],read_locator='§IV-A p58 Fig4',measure='task-time/success',original_report={'time_Wilcoxon_p':0.051,'API_trials_Wilcoxon_p':0.017,'success_Fisher_p':0.0003},calculation_status='not_recalculable_exact_arm_means_from_text',denominator='G1=16,G2=10;5tasks/person',formula=None,absolute_difference=None,ratio=None,missingness='G1T5/T6one notattempted;tablebreakdownunavailable',uncertainty='sourcep=.051doesnotcross.05;exacteffectCIabsent',reversal_condition='소표본그래프차이를유의한동등품질시간절감으로과장할때'),
 dict(comparison_id='SWB-E14',study_family='SWB-STRATH',source_ids=['Swb-P04'],source_url=URLS['Swb-P04'],read_locator='§5.2 Table2',measure='single-arm completed tasks',original_report={'success':7,'partial':1,'trials':8,'people':2},calculation_status='no_comparator_no_time_effect',denominator='8trialsnestedin2people',formula=None,absolute_difference=None,ratio=None,missingness='onepartial',uncertainty='notcausal',reversal_condition='도구없어도해결가능;task3핵심예제없음에도둘다해결')
])

for eid,beta,se,reported_or,pvalue,measure,locator,denom in [
 ('SWB-E15',-1.535,0.634,0.215,0.015,'official vs SO functional outcome odds','Table III p296','216 analyzed trials clustered in54people'),
 ('SWB-E16',2.218,0.796,9.184,0.005,'official vs SO security odds conditional on functionality','Table IV p297','functional subset122trials;within-person clustering in original model')]:
    effects.append(dict(comparison_id=eid,study_family='SWB-ACAR',source_ids=['Swb-P03'],source_url=URLS['Swb-P03'],
      read_locator=locator,measure=measure,original_report={'coefficient':beta,'standard_error':se,'odds_ratio':reported_or,'p_value':pvalue,'reference':'SO','contrast':'official'},
      denominator=denom,unit='odds ratio',formula='approximate95%WaldCI = exp(beta +/-1.96*SE)',
      recalculated_interval=[math.exp(beta-1.96*se),math.exp(beta+1.96*se)],
      calculation_status='approximate_model_interval_from_rounded_reported_coefficients',absolute_difference=None,ratio=reported_or,
      uncertainty='unadjusted approximate95%Wald interval;roundedcoefficients;notoriginalreportedCI;notriskdifferenceCI',
      missingness='originalmodeluses54analyzedpeople;2excludedunavailable;securityconditionalonfunctionality',
      reversal_condition='기능성공을조건으로선택하면보안비교모집단이바뀜;모델OR구간을전체안전한성공의risk차이나링크효과로바꾸지않음'))

def write_jsonl(filename, rows):
    (P/filename).write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=False)+'\n' for r in rows),encoding='utf-8')

write_jsonl('sources.jsonl',sources)
write_jsonl('studies.jsonl',studies)
write_jsonl('effects.jsonl',effects)
summary={
 'sources_total':len(sources),'software_primary_originals':sum(x['count_category']=='software_primary' for x in sources),
 'independent_original_artifacts':sum(x['count_category']=='artifact' for x in sources),
 'excluded_nonhuman_originals':sum(x['count_category']=='excluded_nonhuman' for x in sources),
 'included_study_families':len({s['study_family'] for s in studies}),
 'included_experiments':len(studies),
 'experiments_by_grade':{g:sum(s['comparison_grade']==g for s in studies) for g in ['R','Q','O','U']},
 'controlled_families':len({s['study_family'] for s in studies if s['comparison_grade']!='O'}),
 'strict_R_families':len({s['study_family'] for s in studies if s['comparison_grade']=='R'}),
 'product_link_only_families':0,'comparative_post_adoption_rework_families':0,
 'effect_rows':len(effects),'source_join_missing':sorted({sid for e in effects for sid in e['source_ids']}-{s['source_id'] for s in sources}),
 'verification':'same extractor arithmetic and schema check; not independent human replication'
}
assert summary['software_primary_originals']==6
assert summary['independent_original_artifacts']==4
assert summary['included_study_families']==6
assert not summary['source_join_missing']
(P/'strand-counts.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
