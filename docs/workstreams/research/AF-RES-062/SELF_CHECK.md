# 자체 검토 — 부분 인계

## 판정과 검사 범위

원문 제공이 오판을 줄이는 보편 효과는 식별하지 못했다. 같은 답 템플릿에 링크를 붙인 Kim의 **저자 평균 보고**와, 같은 뉴스에 검색을 권유한 Aslett의 **공개 관측 원개수 반대 방향**을 함께 보존한다. 최초 배정 전체를 정오별 수락 정수까지 복원한 코호트는 확인되지 않았다. 자료를 못 찾았다는 사실을 데이터가 세상에 없다는 주장으로 바꾸지 않았다.

엄격 최소량은 [source-counts.json](evidence/source-counts.json)에서 재계수한다. 현재47저작(사람 원연구보고서32/독립 과제·사전등록4/저자 데이터·코드 패키지4/독립 참값원전7)이며 정보검색15와 사실확인·정보문해력14의 사람 보고서가 포함된다. 이 저작 수는 적격 연구·독립 참가자·비교 셀 수와 다르다. 보고서·원장 생성물 자체는 외부 독해 수에 넣지 않았다.

## Q별 자기 반증

| 질문 | 관측 범위와 결론 | 직접 읽은 근거/위치 | 자기 결론을 깨는 자료를 찾은 경로·결과 | 뒤집힐 조건·부족한 최소 입력 |
| --- | --- | --- | --- | --- |
| Q1 동일한 것은 무엇인가 | A01의10문항 본문은 두 시각조건 쌍에서 정확히 같음.단서 묶음과 조건배정 한계는 남음.A02동일성은 제작규칙/전체AppendixF로 지지되나 실행앱은 미회수.B01은기사풀 동일,검색결과는 다름 | [A raw감사](streams/a/transparent-cis-audit.json) same_answer_text_comparisons;[A 방법](streams/a/methods.md);[B stimuli](streams/b/stimuli.csv) | 클릭가능링크라고 생각하기 쉬운TraceableTexts·Panizza·Fendt·GuidanceSource를 원과제/방법으로 확인:두군같은원문/교육/권고자명 조작으로 제외.단순screen예시를 전체동일성으로 확대하지 않음 | A01배포app/assignmentcode,A02문항별배정·화면hash,접근만조작한동일라벨대비가 있으면 I1식별범위 확대 |
| Q2 원문이 실제 지지하는가 | USGS/NLM은 오권고를 반박,NASA는 비교 한쪽만 확인.뇌크기에는 논쟁.72URL자리는 목록이며 직접독해수 아님 | [root sourceaudit](streams/root/source-audit.md),R-S02/03/05–09/13/14/17;[보강truthaudit](streams/supplement/truth-audit.md) | 링크도착원저→2022비판→2023응답/정정→2024논평을 추가열람.실험전Wayback본문도3건 확인하여현재페이지변경대안 점검.NASA오타/권고방향오류는실제PDF72링크와교차검토해정정 | 정확한당시도착판·주장절·정답키근거를전문으로확인하면 support/refute/insufficient판정수정.참가자실제노출은여전히별도 |
| Q3 배정과실제열람 | A02click사건은1+클릭,Time은문항전체.A01비공백필드35/128은독해아님.AslettS1검색어/URL은자기보고 | [사전등록](https://aspredicted.org/bg22-yfw7.pdf)Q3–4;[클릭원장](streams/a/voluntary-clicks.json);[Ding감사](streams/supplement/ding-schema-audit.json) | 원저의‘checking’을그대로읽지않고Ding원Methods+XLS의mouseover변수를대조:URLhover이지외부pageopen아님.실제노출개수와원배정이혼동된303/305도보존 | load성공/최종URL/scroll/dwell이벤트사전·문항키·이해측정 필요.클릭을무작위로가정하지않음 |
| Q4 같은시행결합 | B01의3966FM행1:1조인과49키복원;T10783행키유일.A02원행미회수,A01수락종점해당없음 | [S aggregate](streams/supplement/aslett-aggregates.json)join_audit/truth_items;[재현](reproduce.md) | 이진0를정답으로해석하는가를원3범주와대조:CND존재확인.S5중복키3개/0범주합침확인.다른서열척도와원범주도대체불가.저자사이트·OSF/Dataverse/Zenodo·고정repo를확인했으나A02행은회수실패 | participant×item×condition×truth×final+inclusionmask공개.사전답이없으면초기일치/변경식별은계속미확인 |
| Q5 조건별정오수락 | B01우선관측오수락+6.20938%p,정수락+8.00189%p,오주장정답−0.96508%p. A02저자평균오수락감소는J3로유지 | [root 독립계산](streams/root/independent-calculation.json)groups/contrasts;[Kim Table1](https://arxiv.org/pdf/2502.08554v1#page=10) | 첫계산에서멈추지않고원저complete-case도복원:오수락+6.41535%p.서로다른코드로8Study1행대조,불일치관측0.제3선택거절=정답오류를손검산 | 원배정N/m확인시ITT/범위재계산.현재NA는미제시문항이섞여bounds불가.반복군집무시p값생성은미실시 |
| Q6 반대/null/과잉거절 | 검색권유군에서오수락증가,Kim에서는감소.설명추가는Kim오수락을증가.동일고정절접근에서정주장수락감소의직접정수는회수못함 | [B Q6](streams/b/B_REPORT.md);[S 제외](streams/supplement/frame.csv);[A 반례](streams/a/methods.md) | A/B첫25+S7및저자후속/정정·archive에서악화/null을탐색.Vraga source대source-free p=.24;유의control은오정보post자체가없어대체불가.Kobayashi감소방향은검색주장차이로주제외.Panizza/Fendt는접근같음 | 동일참주장·같은권고·접근차이·최종범주가연결된새공개정수대비면정권고거절미관측결론변경.지금의‘못찾음’을‘없음’으로쓰지않음 |
| Q7 허용문장 | 제공/클릭/독해/주장일치/오류선별을분리.설계자·교사·팩트체커·방법론자의관점모두제품인과문장확대제한 | [claimlimits](claim-limits.md)관점/수준표;[RESULT](RESULT.md)Q7 | 전체정확도증가가오수락감소를뜻하는지새Aslett공개행에서반증:정오키확인관측정확도+5.60295%p와오수락증가동시존재.임상hover·역사사진·식물/의학원전까지비교 | 실제부품후보/권고정오/초기최종선택/원문판/실제재작업을가진공개시행이필요.현재자료로시간/재작업수치외삽불가 |

## 선정·결손 규칙 이행

R0은 `27dc28648c125186d1b79c5e629c97210e57b23e`, A메타데이터 `fd80a75d5ee3a77f89291f82fd3fb2b90975be3b`, B메타데이터 `10de6313282ba8cfeeec75057050056ef8b74bad`, 보강 메타데이터 `6ce6976dac1758109ca6678bb1aa5a19f953d175`에서 방법/결과 선택 전에 고정했다. 결과 방향·자료공개 여부는 주 적격 요건으로 사용하지 않았다. 보강에만 공개 원행 요건을 적용했다. 검색 스니펫 노출은 숨기지 않는다.

A첫25 중 원저방법22/포스터1/미회수2, B첫25 중 원저방법14/전구부분2/질문지1/리뷰본문1/리뷰metadata1/실패6이다.50대상 중36건의 원저방법,4건의 부분/과제 방법,2리뷰 판별,8본문 실패다. 방법검토 시도를50건 했다는 말과50건 원저 방법을 완독했다는 말은 다르다. A01순위확정,A02/B01잠정,공석3을 유지한다. [frame.csv](frame.csv).

독립S신규0은 공개자료를몰라서무시한0이아니다.7후보(연도내6)를 고정한뒤 적격Aslett의B중복을 제거하고 다른5연도내후보는같은접근·다른주장·평정종점으로제외했다.2026완료논문은연도밖이다.다만repository전체모집은아니므로발견범위밖연구가없다는주장은하지않는다.

## 검사 주체·실제 수행·정정

root와세 AI 보조담당은 같은 세션의 공개 원문을 직접 읽고 분리된 stream에서 기록했다. 사람 독립 심사나 새 참가자 실험이 아니다. root가 Aslett를 별도 stdlib 코드로 재계수하고 양 군의 원행1건씩을 확인했다. A·B·S의 자체검사와 root의 내용 교차검토는 다음 파일에 있다.

- [A Boolean감사 정정](streams/a/audit-corrections.md):대문자TRUE처리를바로잡아1600평정의단일선택을확인.원개수수락에는영향없음.
- [B 검사](streams/b/validation-receipt.json):정주장의정답/수락동일분자를이중으로더한검사기오류를수정·재실행.원집계수치변경없음.
- [S 검사](streams/supplement/validation.json):입력해시·범주·키·로컬링크·개인원행비게시검사.
- [root 정정](streams/root/counting-corrections.json):NASA URL·권고방향을정정하고올바른2024보관판확인. [검색원장정리](streams/root/search-log-curation.json)는URL없는본문조각을metadata로재게시하지않은수정이며후보순위불변.
- [교차검토](evidence/cross-review.json):미회수를부재로단정한문구,클릭분모직접보고vs산술합계,3006명원저표현,검색행위인과문장을수정.

통합 구조·수치·로컬링크 검사는 `evidence/artifact-validation.json`, 실제 계약 검사 SHA/출력은 `evidence/session-check.json`, 고정판 재열람은 `evidence/fixed-result-review.json`에 기록한다. 해당 검사가 생성되기 전에는 통과로 간주하지 않는다. HANDOFF는 이 검사와 고정판 재열람 이후 마지막 단독 커밋으로 작성한다.

## 미실시와 재개

새 참가자 모집, AF058기존 원행/D04 재집계, AF054시간연구 재모집, B03분모추정은 미실시다. 새B03포함mask/정오표를 회수한 사실이 없어 별도정정으로 연결하지 않았다. 그 신규공개 여부의 전수확인은 미실시다. 원 배정 N·m을 몰라 결측 범위 계산은 미실시이며, 정수로 역산할 수 없는 평균의 반올림복원도 미실시다. 원 실험을 현재웹에서 새 참가자로 실행하지 않았다.

우선 재개는 A-F17/F21 및 B6본문/부분 방법을 회수해 선정순서를 확정하는 일과, Kim Study2 공개시행원행·Aslett 배정/제시/탈락명부를 확보하는 일이다. 세부 명령·입력·막힌 경로는 [재현](reproduce.md), [수용 원장](evidence/acceptance-evidence.json)에 있다. 결손이남은상태에서자료최소량충족이나Git검사PASS를연구전체완료로바꾸지않는다.
