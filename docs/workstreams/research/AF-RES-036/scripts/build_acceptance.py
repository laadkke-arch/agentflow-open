"""Record evidence-backed acceptance without converting known design gaps into passes."""
import json
from pathlib import Path

P = Path(__file__).resolve().parents[1]
conditions = []


def add(id_, condition, met, evidence, scope, next_minimum, origin='user brief / presealed SCOPE'):
    conditions.append({'id': id_, 'condition': condition, 'met': met,
                       'evidence': [{'file': f, 'rows_or_location': loc} for f, loc in evidence],
                       'fulfilled_scope_or_unmet_reason': scope, 'next_minimum_check': next_minimum, 'origin': origin})


add('C01', '최신 원격·기존 작업판·공통 지침·고정 의존 인계를 실제 읽고 재개', True,
    [('evidence/resume-context.json', 'requested/observed SHA, environment'), ('manifest.json', 'base/integration/dependencies'), ('review/exclusions.json', 'prior inputs')],
    '작업판f403243과최신integration8dd88b7을별도기록. 원manifest9668632유지. AF-RES-023/032고정SHA읽기.', '최종고정판의원격재독은HANDOFF단계영수증에서확인.')
add('C02', '기존 브랜치·커밋을 보존하고 소유 경로만 수정', True,
    [('PROGRESS.md', 'commit chronology'), ('evidence/checks/session-precommit.stdout.json', 'outside_paths/errors')],
    'main/통합/공통계약/dot-control미수정. 기존봉인입력/판독불변.', '최종결과SHA에서같은session check --fetch.')
add('C03', '원배포 선정 전 규칙·제외·목적·판독·비용 계획을 봉인', True,
    [('SCOPE.md', 'sampling / truncation / reading'), ('ANALYSIS_PLAN.md', 'scoring / cost'), ('reading-plan.json', 'seed360032')],
    '범위bdc4135·배정f5be649·원B bd3c17e·집계계약f26232b·N/H442292b·판독5fbde38의순서를보존.', '사전노출편차는C05에별도.')
add('C04', '두 경로 각6,서로 다른 출판12,최소6프로젝트·프로젝트상한2', True,
    [('references.jsonl', 'all12'), ('frame.csv', 'all58'), ('review/base-audit.json', 'document/project counts')],
    'G6/R6·9프로젝트·9공유배포물·12출판문서. 장분할중복없음.', '새표본을추가하면별도사전봉인;현재분모교체금지.')
add('C05', '모든 12참조의 선택이 현재 목적지 사전 열람 전에 이루어짐', False,
    [('references.jsonl', 'G06/R04'), ('review/base-audit.md', '4. 배정 검산과 노출')],
    'G06목록및R04 DESeq2 landing이선정전읽힘. 전체12완전비노출표집주장불가;제외후10계산.', '현재편차는사후복구불가. 새로운다음묶음에서는배포소비자href선정과target조회주체를분리.')
add('C06', '이전 소비자·목적 및 기존 보조 사례 중복 제외', True,
    [('review/exclusions.json', 'AF-RES-023/032 consumers and goals'), ('review/base-audit.json', 'overlap checks')],
    '고정 prior소비자/목적과새12 중복0. prior판정은교정용이며새정답으로사용하지않음.', '새원장추가시고정exclusions와조인.')
add('C07', '봉인된 후보 기간·순서·fallback의 완전 소진', False,
    [('review/base-audit.md', '3. 최초판·후보 소진 범위'), ('frame.csv', 'GNU and Bioc candidate rows')],
    '초기GNU안정판순서는확인. 그러나Debian coreutils9.1-1과R중간patch전부미확인;한정탐색을전역HTML부재로확대불가.', '공식Debian9.1-1 doc artifact HTML부터읽고Rpatch목록범위를추가기록. 봉인12는그대로.')
add('C08', '문장에 따른 목적 층과 빈 층 보존', True,
    [('references.jsonl', 'purpose_stratum / basis'), ('sensitivity.csv', 'all_presealed by strata')],
    '현재7/특정판1/애매4;R특정판0. current는최신판명시7이아님.', '새판재현목적이명시된소비자는새사전표본으로만추가.')
add('C09', '모든 최소 목적 한정이 원 문장에 직접 있음', False,
    [('references.jsonl', 'G06 minimal_purpose/context'), ('review/base-audit.md', 'stable qualifier')],
    'G06 stable한정은원문newest보다강한수집자해석. 원봉인불변·해당제외민감도11.', '다음실험은원문newest만을목적으로명시하고stable추정은별도flag.')
add('C10', 'B 원 href·텍스트·문맥·판·멤버·해시·위치 재현', True,
    [('references.jsonl', 'all12'), ('review/base-audit.json', 'reconstruction'), ('adjudicators/gnu/sources.jsonl', 'GNU-C-G01..G06'), ('adjudicators/bioc/sources.jsonl', 'BC-consumer')],
    '원소비자멤버를수집·기준확인에서재취득/hash대조. 전체원문영구Git보관은주장하지않음.', '원URL변경시저장hash와불일치를실패로남기고기존카드보존.')
add('C11', '직접 본 고유 원문과 각 범주 최소수 충족', True,
    [('sources.jsonl', 'count_minimum=true records'), ('evidence/source-counts.json', 'categories')],
    '적격하한50;소비자12/current10(history와중복제거)/history10/cross16/other2. current코드·목록제외설명본문8.', '재독·미러·검색·실패는추가최소수에산입하지않음.')
add('C12', '현재 목적지12개 전부 시도하고 실패도 기록', True,
    [('components.jsonl', 'N original_get_attempt_id'), ('attempts.jsonl', 'original href GETs'), ('adjudication.csv', 'all12')],
    'R01 404를적격본문으로세지않음. 나머지11은최종200이며필요본문추가확인.', '새질의에서는원도착절을같은목적·판과재확인.')
add('C13', 'N/H의 정확 발췌·위치·hash·사건일/조회UTC 구별', True,
    [('components.jsonl', 'spans / metadata / codepoints'), ('ERRATA.md', 'E02/E06')],
    '원문발췌24개1600자이내. wrapper전체길이는G04/R04초과를공개. 발행일과FTP수정일혼동정정.', '전체카드한도를원한다면새실험으로별도고정;봉인입력조용한절단금지.')
add('C14', '동일 N/H/B 바이트·순서와48 보기 보존', True,
    [('packets.jsonl', 'all48'), ('evidence/packet-verification.json', 'all_identical'), ('review/resume-quant/audit.json', 'sealed hash comparisons')],
    'BN/BNH의N,BH/BNH의H,모든B 12/12동일.442292b원packet불변.', '최종검산에서다시hash조인.')
add('C15', '모든 사례에서 현재 N과 과거 H의 의미가 완전히 비중복', False,
    [('components.jsonl', 'N history flags / R03,R04,R05'), ('evidence/analysis-summary.json', 'history_flags')],
    'N카드에이력5건,동일함수/reference군/intro중복있음. 이를원문이력및카드이력제외로공개;미달을독립효과로포장하지않음.', '현원문에과거관계가없는새사례를다음표본에서사전분리;현재카드재편집으로음성결과변경금지.')
add('C16', 'H에 오늘관측·수집자 권고·정답을 넣지 않음', True,
    [('components.jsonl', 'H flags / metadata'), ('review/resume-sources/notes.md', 'H scope')],
    'H의관측대상은과거발표/판/멤버. 수집자는노출되어있지만카드에판정권고는없음. 약한관련배경H도한계공개.', '공식과거발표를목적지당시snapshot으로오인하지않음.')
add('C17', '배치·seed 고정과48결정의 선행 봉인', True,
    [('reading-plan.json', '48 assignments'), ('decisions.csv', 'all48'), ('evidence/decision-verification.json', 'reader receipts'), ('PROGRESS.md', '5fbde38 seal')],
    '4문맥×12,보기각3,같은사례다른보기재노출보고0. 기준전에48결정커밋.', '후기평가자가수정하지않고새판독은다른실험으로표시.')
add('C18', '노출·배경·해석·미노출분모를 구별하고0을 보존', True,
    [('sensitivity.csv', '17filters×3contrasts×12'), ('evidence/analysis-summary.json', '255summaries'), ('RESULT.md', 'Q3/Q5')],
    '수집사전노출10·프로젝트/target제외3·결합2·reported/nohistory1·모든목적해석0·외부gold0을별도로표시.', '같은모델계열내부판독을사람/외부독립인과효과로부르지않음.')
add('C19', '결정 뒤 날짜자료·배포물·실제절로 기준판정', True,
    [('adjudication.csv', 'all12 criterion rows'), ('evidence/adjudicator-launch.json', 'post-seal launch'), ('adjudicators/gnu/notes.md', 'source checks'), ('adjudicators/bioc/notes.md', 'source checks')],
    '별도문맥이추가원문및배포hash를읽음. 단독외부gold없음을공개. 기준11KEEP/1REPLACE,보류0.', '외부독립기준이필요하면같은자료를복사한자체다수결이아닌별도판독/원자료필요.')
add('C20', '원URI 전달과 대체URI의 목적·판·정확절을 구별', True,
    [('adjudication.csv', 'R01 replacement fields'), ('evidence/analysis-summary.json', 'candidate_uri_changes_at_fixed_N')],
    'R01 원404·판독후보tarball미검증·기준의3.11HTML exactanchor검증을분리.', '대체HTML의살아있는해당절을새조회시재확인.')
add('C21', '옛판보존·200잘못된내용·새anchor실패·보류를 실제 탐색', True,
    [('adjudicators/gnu/notes.md', 'three counterexamples'), ('adjudicators/bioc/notes.md', 'S4Vectors PDF'), ('collectors/cross/notes.md', 'R13935 conflict')],
    'G03옛2018보존;새2024tag_18없음;completions폴더/PDF200불충분. 원12기준보류0이나보조서지귀속보류존재. 보조를소프트웨어분모에추가하지않음.', '부족한유형을채우려기존판정을바꾸지않고새표본은별도봉인.')
add('C22', '주/보조 짝비교·목적층·모든전이·기준미확정 분리', True,
    [('sensitivity.csv', '612rows'), ('evidence/analysis-summary.json', 'views/comparisons')],
    'BN→BNH0/12;B→BH0/12;B→BN보류해소12. 기준보류를분자에추가한행0. 이유/후보URI변화를행동변화와구별.', '원장고정뒤별도결과재계산.')
add('C23', '동일 N에서 H필요사례와 이력 없이충분한반례를 찾고음성보존', True,
    [('RESULT.md', 'Q5'), ('components.jsonl', 'G03/G05/R03'), ('decisions.csv', 'R01 BN/BNH')],
    'H필요행동변화양성0을보존. G05/R03은현규칙/함수충분. G03은원판중요하지만B/N에이미있음.', '양성건수는종료기준아님. 새로운원판의도소비자를사전봉인한후반복.')
add('C24', '실측 요청·실패·바이트·재사용·경과와부담주체 기록', True,
    [('costs.csv', 'measured and unmetered phases'), ('attempts.jsonl', 'GET / tool attempts'), ('evidence/cost-summary.json', 'collection/criterion'), ('evidence/resume-cost-summary.json', 'resume audit')],
    '기준자료누락을보완. 실측최종body,임시보관,직렬화저장분리;실패/재시도/공유archive논리재사용포함.', 'wirebytes·사람시간·실서비스원가는미측정으로유지.')
add('C25', '고정예산2회차실제/모의와 C0미측정 구별', True,
    [('ANALYSIS_PLAN.md', 'second-visit model'), ('replay-costs.csv', '48 simulations'), ('evidence/replay-summary.json', 'count feasibility')],
    '실제2회차0. 같은URL/응답/locatororacle가정과2GET/30초예산실패공개. 현재N과동일NH재구성과업분리.', 'R01/G05 구성별파일만제공한실제예산재생이첫최소실행.')
add('C26', '지리 발행자·실제소비자쌍과 소급반례', True,
    [('sources.jsonl', 'CX-G01..04'), ('review/resume-cross-costs/REVIEW.md', 'Census/BLS/ONS')],
    'Census→BLS실제href비소급쌍;ONS과거연도에새경계적용반례. 통계수치·피해율미관측.', 'BLS2023Q4/2024Q1원데이터같은질의재현이추가영향검증.')
add('C27', '서지의실제정정·명시적판/번역인용을원자료로구별', True,
    [('sources.jsonl', 'CX-B03/B04/B16/B17'), ('collectors/root/notes.md', 'Takano-to-catalog correction'), ('collectors/cross/notes.md', 'edition pair')],
    'Nagoya는Takano2016정정명시,SEP는1953p222/Anscombe명시. 서로다른사례이며같은전파사슬아님. 요구필드의원문쌍은확인.', '같은catalog의날짜있는전후기록은C28에별도.')
add('C28', '동일 서지레코드의 날짜있는 정정전후와소비자전파사슬', False,
    [('collectors/cross/notes.md', 'bibliographic gaps'), ('collectors/root/notes.md', 'B16/B17 limit'), ('RESULT.md', 'Q7')],
    '현재정정문구와근거논문은있지만이전record/변경UTC없음. ornaments판귀속충돌원논문일부접근실패.', 'NULDL000040/ESTCR17253의Norton표기고정이전record·수정영수증;R13935연구는별도.', 'stronger historical-chain check, reported limit beyond the observed correction pair')
add('C29', 'C0/C1/C2의매칭가능과업·역할·상반목적조건·폐기재구성2사례', True,
    [('RESULT.md', 'Q6/Q8 alternatives, G05/R01'), ('retention-options.jsonl', '36records')],
    'C1B12,153B와C2BHprovenance38,145B하위구성비교;판정이력전체원가미측정. 동일NH재구성에만조건부조회차이.', '원N시각·전체문서·판정이력도필요하면별도객체비용을추가계측.')
add('C30', '원장 모든근거ID·판독hash·중복·분자분모재검산', True,
    [('review/resume-quant/audit-final.json', '81 phase-aware final working-tree checks'), ('review/resume-quant/integration-applied.json', 'source mapping / hashes'), ('evidence/final-counts.json', 'counts')],
    '64기준source와18재독source를canonicalalias연결;기존원문50유지. 최종작업트리의81검사통과;기존69영수증보존.', '결과고정SHA의동일입력hash를원격재독과대조.')
add('C31', 'RESULT 첫3표·마지막약점3행·Q1–Q8 SELF_CHECK', True,
    [('RESULT.md', 'first tables12/14/18;last3rows'), ('SELF_CHECK.md', 'Q1..Q8'), ('evidence/document-check.json', '21 structural/pointer/ownership checks'), ('review/resume-cross-costs/report-review.md', 'table dimensions')],
    '각행URL/원장ID,0분모해당없음,미확인사유,다음구체자료포함. 검토에서위치/날짜/열의포함제외표시정정.', '최종파일형식·로컬링크·ID체크영수증을남김.')
add('C32', '기계검사·원문확인·동일팀검토·외부독립성을 구별', True,
    [('SELF_CHECK.md', 'opening / verification scope'), ('RESULT.md', 'Q3/Q4/Q5'), ('evidence/criterion-dependence.json', 'external gold flags')],
    '외부독립gold0을보존. 범위검사통과로연구gap을충족처리하지않음.', 'HANDOFF에서실제검사SHA/hash/exit와미실시실행분리.')
pre = P / 'evidence/checks/session-precommit-execution.json'
passed = pre.exists() and json.loads(pre.read_text())['exit_code'] == 0
add('C33', '사용 가능한 셸에서 workbench.session check --fetch 실제 실행', passed,
    [('evidence/checks/session-precommit-execution.json', 'actual command/head/exit'), ('evidence/checks/session-precommit.stdout.json', 'contract/dependencies/ownership')],
    '현재는precommit작업트리대상. 결과원격고정SHA의인계직전실행은HANDOFF단계추가영수증으로구분.' if passed else '실행영수증통과없음;원인확인필요.',
    '고정결과원격재독뒤같은명령을다시실행하고그대상SHA를HANDOFF에기록.')

out = {'schema': 1, 'task_id': 'AF-RES-036', 'status': 'REVIEW_READY_WITH_GAPS',
       'result_path': 'RESULT.md', 'resume_from_commit': 'f403243dbf5f097536a1fd9fda55dfce4382329a',
       'conditions': conditions,
       'summary': {'total': len(conditions), 'met': sum(c['met'] for c in conditions),
                   'unmet': sum(not c['met'] for c in conditions), 'unmet_ids': [c['id'] for c in conditions if not c['met']]},
       'delivery_gates': {'fixed_result_remote_reread': 'recorded after result commit in evidence/result-remote-reread.json and HANDOFF.md',
                          'fixed_result_session_check': 'recorded after result commit in evidence/checks/session-result-execution.json and HANDOFF.md',
                          'handoff_write_order': 'write only after those actual receipts; no self-referential SHA fabricated'},
       'meaning': 'met is condition-specific evidence; status retains sampling, interpretation, semantic overlap and historical-chain gaps. No human outcome or causal effect implied.'}
(P / 'evidence/acceptance-evidence.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out['summary'],ensure_ascii=False))
