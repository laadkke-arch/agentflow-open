# REVIEW-27 · 설계 중인 부분에 쓸 자료를 발견하고, 근거와 함께 다음 사람에게 넘기는 법

같은 막대그림 주소를 추천해도 “묶음 막대의 그리는 법”에는 맞고 “옛 집단의 원 점수와 비교하는 예”에는 틀릴 수 있다. 한편 Blender 사용자가 처음 알았다고 확인한 대상은 답변 전체가 아니라 벡터를 비교하는 한 기능이었다. **이번 네 연구에서 되풀이된 차이는 링크를 어느 요청의 어느 조작에 쓰려는가였다.** 이것을 기록하면 이미 아는 도구의 다른 기능도 추천할 수 있고, 같은 URL을 여러 요청에 재사용하면서 각 답의 근거를 따로 확인할 수 있다. 가장 큰 미확인은 개발자가 혼자서는 찾지 못한 타 분야 선례를 이 탐색기가 찾아 주고, 그 결과 실제 설계 결정이나 시험이 달라지는가다. [105 원 제안과 후속][f105] · [106 원 목적과 일반 역할][l106] · [제품 목적][goal]

## 어떤 결과를 새로 인수했는가

2026-11-24 한국시간 기준. 계획 브랜치의 최신 [REVIEW-26][prev]을 먼저 읽었다. 그 검토가 사용한 [통합판 49f603a][old]과 이번 [c40ef77][reg]의 전체 작업을 ID로 비교했다. 102→106개, 중앙 DONE 100→104개, BLOCKED 2개다. 기존 102행은 모든 필드가 같았다. 현재 연구만 세면 104건 중 인계 등록 102건과 BLOCKED 2건(018·035)이다. 별도로 연결 시험 AF-DOT 두 건이 DONE이다. RUNNING은 0이다. DONE 104행의 중앙 수용 근거 배열은 모두 비어 있어 각 작업의 자체 판정과 결과 파일을 읽었다. 다음 표의 인계 커밋은 각 소유 브랜치의 확인 당시 끝과 일치했고 마지막 변경은 각각 HANDOFF.md 한 파일이다. 105는 중앙의 시도 번호가 2이고 고정 인계문에는 시도 1로 적혀 있다. 결과·인계 SHA는 대조됐고, 어느 세션이 최종 작성했는지는 이 차이만으로 확정하지 않았다. [연구 운영 규칙][rules]

| 새 DONE | 중앙의 인계 SHA | 작업자가 검사한 결과 SHA | 받아들일 수 있는 범위 |
| --- | --- | --- | --- |
| 105 · Blender·QGIS 사용자의 기존 지식과 다음 행동 | [1a9d75d][h105] | [9290320][r105] | REVIEW_READY. 시간순 질문 8건과 특정 발언을 찾아 선정한 4건을 각각 추적했다. 전체 조작을 새로 알았는지 판정할 수 있는 사건은 양쪽 모두 0건이다. |
| 106 · 문서 주소와 예제의 후계 | [eedd436][h106] | [506f2f6][r106] | COMPLETE_WITH_LIMITATIONS. 실제 8쌍과 결원 4쌍. 특정 원래 목적과 일반 시각 역할에서 경로 예측의 정오가 갈렸다. 당시 빌드 생성과 브라우저에서의 정확한 도착은 미확인이다. |
| 107 · 반복된 그림 가운데 하나만 바꾸기 | [54fccba][h107] | [8ae7aad][r107] | COMPLETE. 고정 원본 3개에서 두 목적·두 방식·두 반복의 24실행을 판독했다. 다른 판에서 같은 대상을 다시 찾는 능력과 실제 편집 시간은 미확인이다. |
| 108 · 같은 분량에서 예외 절을 남기는 효과 | [8b00aaa][h108] | [806cdff][r108] | PARTIAL. SQLite와 Flexbox 16입력에서 두 방식의 봉인된 답과 실행을 대조했다. 직접 열람의 세부 배당은 18/24이며 독립 판독자는 없었다. |

계획 검토에서 105의 요청·제안·후속·반환 12행씩, 106의 예측 12행과 전후 24판, 107의 실행 41행 중 본실험 24행과 요소 644행, 108의 대응 16행과 실행 32행을 원장에서 대조했다. 아래 실행 관측은 연구자가 보관한 기록이다. 옛 작업의 결과는 직전 REVIEW의 모집 범위와 분모를 인수했다. 누적 REVIEW만으로 알 수 없었던 현재 프로토타입의 색인·문구 연결 규칙에 한해 고정 코드 두 파일을 좁혀 읽었다. [105 반환][ret105] · [106 예측][p106] · [107 요소][el107] · [108 대응][p108] · [자료집 색인][indexcode] · [요청 연결 코드][reqcode]

## 설계자가 이 파일에서 이어받을 흐름

사용자가 건네려는 입력은 전체 소프트웨어 지도 또는 선택한 부분, 이루려는 목적, 지켜야 할 조건이다. 찾을 대상에는 OSS·서비스·사이트·부품, 같은 도구의 다른 기능, 다른 분야에서 옮겨 쓸 작동 원리가 있다. 목적은 설계 초기에 선택지를 발견해 뒤늦은 재작업을 줄이는 것이다. 링크 하나로 등록하고 세부 조사를 다음 사람에게 넘기는 안도 여전히 유효한 대안이다. 아래의 판단 단위는 특정 DB 제품·크롤러·고정 입력 양식을 요구하지 않는다. [연구 브리프][goal] · [앞선 연구의 분모와 정정][prev]

| 설계 판단 | 104까지 확인된 근거 | 이번 회차까지 남은 한계 |
| --- | --- | --- |
| 입력 원문·부분·금지 조건을 어떻게 쓰나 | 초기 요청에서는 부정 조건이 빠졌다. 020의 주장 전달은 72/73, 충돌 완전 해소는 2/16이었다. 070의 자연 요청에는 되물어서 정오가 달라졌는지 가를 분모가 없었다. 074의 구성 입력은 값을 받으면 8/8을 가를 수 있었다. | 105에서는 익숙한 조작의 어느 인자·입력·판이 달라지는지 확인해야 했다. 여섯 사례에 한 가지 확인 질문을 제안했으나 실제로 물어 얻은 이득·비용은 미측정이다. |
| 타 분야 선례를 찾아 설계에 옮길 수 있나 | 분야 단서가 있는 010은 원리 7군을 찾았다. 단서 없는 033의 144쌍은 넓은 지지 1쌍·당시판 지지 0쌍이었다. 069·073은 접수/적용, 접근권 이전/책임 수락을 나눌 시험 관점을 냈다. 077 보조 3건의 핵심 구현 변경은 0건이었다. | 105의 기능 신규 인지 2건과 107의 훌륭한 시험 입력도 원 사용자가 낯선 분야의 선례를 보고 설계를 바꿨다는 증거까지 제공하지 않는다. 022의 미인지→변경→시행은 0/24, 018의 범용 웹 검색 동예산 비교는 여전히 BLOCKED다. |
| 같은 링크를 합치거나 과거 답을 복원할 수 있나 | 055는 과거 판단 4/4를 복원해도 다음 판 판단은 0/4였다. 071에서 조각·설정 보관으로 과거 자료 소실 후 22/22를 복원했다. 075의 대표 원문은 양성 존재 15/15를 복원했고 유일성·공동 1위의 전체 집합은 각각 16/16 보류했다. | 101에서는 이미 쓴 제품이라는 이유로 빼면 실제 다른 유효 조작 셋도 사라졌다. 106에서 같은 주소로 바뀐 내용과 옛 주소를 떠난 같은 목적이 모두 나왔다. 기능·판·작업 조건이 다른 추천은 별도로 판정할 이유가 있다. |
| 후보가 어느 판의 어느 절과 연결되나 | 086의 역사적 제공 관측창은 0/9, 094에서는 남은 옛 그림이 새 절에서 빠졌다. 102는 실제 8쌍 모두 경로 예측이 맞았으나 음성이 0개였다. 거기서 파일 수록·본문 사용을 확인한 16판 모두 당시 생성은 미확인이었다. | 106에서는 원 목적 음성 1개와 이동 후 양성 2개가 생겼다. 현재 확인한 절, 현재 브라우저에서의 도착, 당시 빌드의 생성, 실제 독자가 원한 결과의 성립은 각각 다른 관측이다. |
| 링크 하나와 부품 조합 중 무엇을 권할 수 있나 | 076의 자연 6요구×20후보에는 직접 양성이 없었다. 080의 비교 가능 목록 확장에서는 자연 1/5·교정 3/5가 양성으로 바뀌었다. 078은 단독 성공한 부품 두 개도 같은 입력을 연결하면 실패함을 보였다. 096에서는 인접 자료가 경계 6/6에 노출돼도 단독 완결은 0/6이었다. | 후보를 찾음, 필요한 절을 보여 줌, 그 부분이 단독으로 충분함, 조합이 사용자 입력에서 실행됨까지의 분모를 따로 유지해야 한다. 새로 찾은 사이트의 전체 적합성은 한 기능의 성공에서 추정하기 어렵다. |
| 저장할 설명과 후속 열람의 비용은 얼마인가 | 021은 두 절 예산에서 주소 6/23, 절 목록 9/23, 조건에 맞춘 절 14/23, 잘못 연결한 절 8/23이었다. 034의 부분 시간은 380→57초, 전체는 849→847초였다. 104의 동일 74,400자 발췌에서 한 방식만 완결한 두 자리는 같은 진단 질문 하나였다. 최종 JOIN 성공을 요구하면 전용 완결은 0/15였다. | 108은 같은 1,200자에서 정상 근거를 얻은 입력과 잃은 입력을 모두 관측했다. 인덱스를 만드는 비용·읽은 원문 수·사용자 작업시간·실제 재작업은 서로 대체할 수 없다. |
| 부분을 가져와도 주변에 보존할 것이 남나 | 089는 선택색과 다음 편집 대상을, 091은 같은 위치의 점과 원래 Point 행을 구분했다. 095는 표가 나와도 옆 표의 선이 소실됐고, 103의 페이지 이미지 경로는 외관 10/10이었지만 문장이 있는 8자리에서 텍스트 선택이 안 됐다. | 107은 103이 남긴 “같은 각도의 두 그림 가운데 하나만 고칠 수 있는가”에 고정판 답을 줬다. 판이 바뀌어 그림 순서가 밀릴 때도 같은 발생을 가리킬지는 아직 모른다. |

## 새 원장에서 판정을 바꾼 네 가지

**105 · 사용자가 배웠다고 말한 기능의 크기.** Blender와 QGIS의 최초 글을 각각 80개씩 본 시간순 층에서 8건을 선정했다. 별도로 26개 질의를 사용해 얻은 일치 발언 22건에서 4건을 선정했다. 선정된 12건은 고유 질문이지만 시간순 Blender 두 건은 같은 작성자였다. 시간순 8건 모두 제안 전체의 인지와 실행이 미확인이다. 발언을 찾아 뽑은 네 건에서는 Blender의 Compare Direction과 GDAL의 `with` 지원을 처음 알았다는 표현이 두 건 있었다. 둘 다 후속 실행은 미확인이다. 다른 보조 사례의 같은 제안을 시도해 실패했다는 보고 한 건을 이 둘의 실행으로 연결할 수 없다. 반환 원장에는 기존 시도와 링크 3, 같은 링크의 다른 절 1, 확인 질문 6, 보류 2가 있다. 이는 연구자가 제안한 답이다. [원 제안][pr105] · [후속][f105] · [반환][ret105]

Blender 설명의 비교 조건은 90도 초과였는데 현재 내려받은 파일은 Not Equal/0이었다. 글에 적힌 3.6.5와 첨부 헤더도 달랐고 원 작성자의 정확한 설치판은 12건 모두 미확인이었다. 32개 독립 원자료를 읽었어도 “전체 해법을 처음 알아서 적용했다”는 사건의 분모는 양쪽 모두 0이다. 반대로 “아는 기능이니 같은 도구의 답은 필요 없다”는 단정도 이 두 기능과 101의 세 조작을 놓친다. [105 결과와 반례][r105] · [검산 기록][au105]

**106 · 유효한 주소, 남아 있는 목적, 살아 있는 방법.** ggplot2·Matplotlib의 기존 표본 밖 잔여 경로는 547개였다. 12쌍을 배정해 8쌍이 채워졌고 4쌍은 해당 층에 없었다. 원 목적 기준 새판 양성 7·음성 1이다. 경로 기반 예측은 ggplot2 네 쌍에서 맞았지만 Matplotlib에서 이전·통합 뒤 살아난 후계 두 개를 놓쳤다. 같은 페이지·PNG 경로가 유지된 막대그림에서는 G1–G5 점수라는 특정 목적은 사라지고 일반 묶음 막대의 설명은 남았다. 일반 역할로 재집계하면 양성 8·음성 0이다. 소실된 옛 주소라도 공식 통합과 실제 새 원절이 확인되면 후계 링크를 제시할 수 있다. 특정 작성 방법까지 요구하면 옛 절도 필요할 수 있다. [봉인 예측][p106] · [원 목적과 일반 역할][l106] · [목적별 반환][ret106]

547개는 경로 확인 수다. ggplot2 새 본문 68개 중 9개, Matplotlib 일반층 새 본문 476개 중 6개를 상세 판독했다. 구체 목적의 거짓양성 한 건에서도 옛 경로는 새 절이 계속 썼다. “파일만 남고 새 절에서는 미사용”이라는 엄격한 반례는 이 표본에서 확보하지 못했다. 소스 범위와 일반 역할의 정의 일부는 새 경로를 본 뒤에 추가했다. 실제 16판의 역사적 생성은 전부 미확인이고 브라우저 이동도 실행하지 않았다. 이것이 102의 8/8과 이번 오류들이 서로 양립하는 이유다. [수정 시점][am106] · [층별 수치][co106] · [인계][h106]

**107 · 발생 하나를 고치는 답과 전체를 고치는 답.** PGFPlots·SVG·Graphviz의 고정 원본 3개에서 공유 정의를 고치는 A와 사용 위치를 구별한 B를 각각 두 번 실행했다. 단일 발생에서는 A 0/6·B 6/6, 전체 변경은 각각 6/6이다. 단일 A의 여섯 과정도 종료값은 전부 0이었다. TeX의 12번째와 21번째 그림은 각도가 같아서 공유 정의에 조건을 걸어도 둘 다 바뀌었다. 특정 회차를 가리키자 12번째만 바뀌었다. 같은 출력의 독자가 “보기”, “한 곳 편집”, “모두 변경” 중 무엇을 원하는지에 따라 필요한 소스 링크가 달라진다. [주 실행][run107] · [요소별 관측][el107]

반복의 의미 판정은 기준 3쌍을 포함해 15/15 일치했다. TeX PDF 원시 바이트는 같은 다섯 쌍 모두 달랐다. 24실행은 24개 독립 프로젝트가 아니다. 고정판의 회차·속성·간선 종점을 다음 판의 지속 ID로 써도 되는지, 다른 엔진·폰트에서 같은지, 원 사용자의 편집 시간이 줄었는지는 확인하지 않았다. [검산][au107] · [범위와 대조 원본][r107]

**108 · 예외를 하나 더 보이면 같은 비용에서 무엇이 밀리는가.** SQLite·CSS Flexbox 8문제의 정상/경계 16입력에 키워드 방식 K와 예외 문장을 우선한 E가 각각 1,200자를 제공했다. 32개 사전 답과 32회 로컬 실행을 기록했다. 각 방식은 16입력 중 8개 값을 확정했고 그 8개에 오답은 없었다. 그러나 발췌 안에서 근거까지 충분한 답은 K 4개, E 2개였다. E는 F2 정상에서 유보를 근거 있는 정답으로 바꿨고 F4 정상에서는 반대였다. 정렬 동률인 S3의 두 입력은 값이 맞아도 E에서 정렬 근거가 사라졌다. 원래 오답이 유보·정답으로 바뀐 주 사례는 0개였다. 독자가 다음에 할 판정을 모른 채 항상 예외 문장부터 저장하는 정책은 이 결과로 지지하기 어렵다. [짝 원장][p108] · [판정·비용][m108] · [실행][run108]

공개 1차 자료는 36개였으나 지정한 종류별 독해는 18/24였다. SQLite 시험 4개와 POSIX 2개 원출처 직접 개봉이 비었고, SQLite 시험은 일치하는 공식 미러 바이트를 썼다. SQLite 해당 판의 문서 동일성과 원 HTML 좌표, 독립 판독도 미확인이다. 결과가 같았던 두 방식을 동등하다고 일반화하거나 “더 안전한 답”을 주장할 수 있는 분모는 아니다. [자가검토][self108] · [부분 인계][h108]

## 무엇을 다음에 검증할 것인가

가장 큰 빈자리는 자명한 관련 후보를 다시 읽는 일보다 **생소한 선례를 처음 찾아서 설계 결정에 연결하는 일**에 있다. 동시에 현재 예제에서는 자료집이 URL·제목에 단어 색인을 두고, 특정 조건의 근거 연결은 공개 문서 두 개와 고정 한국어 문구에 의존한다. 외부에서 받아 온 새 자료·새 표현에서도 같은 흐름이 성립하는지 분리해 볼 수 있다. 다음 과제들은 하나의 최종 DB 설계를 전제하지 않는다. 공개·재사용 가능한 실제 요청과 연구용 대조를 구별하고, 개발자의 실제 채택은 같은 작성자·같은 조작의 후속 근거가 있을 때만 센다. [현재 색인][indexcode] · [실제 연결 경로][reqcode] · [출력 전 후보 범위][limitcode]

| 독립 작업 | 고정 운영 선행 | 이번에 완성할 산출물 | 서로 만날 필요가 없는 경계 |
| --- | --- | --- | --- |
| 109 · web-pro | [105][h105] | 공개된 부분 설계 요청에서 일반 웹 검색과 구조·원리 탐색을 같은 예산으로 비교한 발견 사례집 | 현재 웹에서 찾은 원자료와 사전 대안을 다룬다. 이미 공개된 실제 Studio 요청이 없으면 공석으로 두고 유사 프로젝트를 별도 층에서 비교한다. |
| 110 · codex-cloud | [106][h106] | 링크 메모와 목적·판을 조회에 쓸 때 유용한 후보·거짓 일치·저장 비용이 어떻게 바뀌는지 재생하는 색인 실험 | 고정 자료집 안의 검색까지만 다룬다. 두 방식의 후보 수와 표시 수를 따로 고정한다. |
| 111 · codex-cloud | [107][h107] | 같은 뜻의 새 문장에는 근거가 유지되고, 반대 조건·다른 대상에는 옮겨 붙지 않는지 확인하는 요청–근거 시험 묶음 | 후보 목록을 고정하고 문구·범위·판정 재생만 다룬다. 110의 색인을 사용하지 않는다. |
| 112 · web-pro | [108][h108] | 같은 후보 링크를 넘겨받은 후속 조사자가 제한된 원문 열람으로 어떤 답과 반례까지 복원하는지 기록한 인계 비교 | 신규 모집·별도 자료를 쓴다. 발견 순위와 과거의 SQLite·CSS 발췌를 다시 채점하지 않는다. |

네 작업 모두 자체 브랜치·경로에서 바로 시작할 수 있다. 109의 통상 웹 검색과 구조화 검색은 지정한 새 요청에 대한 비교이며 차단된 018의 인계 상태를 바꾸지 않는다. 110·111은 소유 경로 안의 비교 구현·시험만 만들어 원형과 실험을 구별한다. 112의 후속 판독자가 실제로 본 절과 예상만 가능한 결과도 별도 기록한다. 필요한 읽기 범위, 질문별 근거, 채울 수 없는 자리, 필수 표·커밋·검산 조건은 [배정용 JSON][next]에 있다.

[prev]: https://github.com/laadkke-arch/agentflow-open/blob/e7713b798f05908cb14badd9745caa7cdcd056bc/docs/workstreams/planning/REVIEW-26.md
[old]: https://github.com/laadkke-arch/agentflow-open/blob/49f603a98188fbf2009c4c490b0539f32d124e38/docs/automation/dot-control.json
[reg]: https://github.com/laadkke-arch/agentflow-open/blob/c40ef7723d851b628233bfb60dff8dfd292385cf/docs/automation/dot-control.json
[goal]: https://github.com/laadkke-arch/agentflow-open/blob/c40ef7723d851b628233bfb60dff8dfd292385cf/docs/product/RESEARCH_BRIEF.md
[rules]: https://github.com/laadkke-arch/agentflow-open/blob/c40ef7723d851b628233bfb60dff8dfd292385cf/docs/RESEARCH_WORKFLOW.md
[indexcode]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/catalog.py#L127-L145
[reqcode]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/roundtrip.py#L172-L189
[limitcode]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/roundtrip.py#L93-L122
[h105]: https://github.com/laadkke-arch/agentflow-open/blob/1a9d75dc7ae6a179522a5a56e99b002651a2f7bd/docs/workstreams/research/AF-RES-105/HANDOFF.md
[r105]: https://github.com/laadkke-arch/agentflow-open/blob/9290320c1e9de33f30857af87640926c4d0f8cff/docs/workstreams/research/AF-RES-105/RESULT.md
[f105]: https://github.com/laadkke-arch/agentflow-open/blob/9290320c1e9de33f30857af87640926c4d0f8cff/docs/workstreams/research/AF-RES-105/followup.csv
[pr105]: https://github.com/laadkke-arch/agentflow-open/blob/9290320c1e9de33f30857af87640926c4d0f8cff/docs/workstreams/research/AF-RES-105/proposals.csv
[ret105]: https://github.com/laadkke-arch/agentflow-open/blob/9290320c1e9de33f30857af87640926c4d0f8cff/docs/workstreams/research/AF-RES-105/returns.csv
[au105]: https://github.com/laadkke-arch/agentflow-open/blob/9290320c1e9de33f30857af87640926c4d0f8cff/docs/workstreams/research/AF-RES-105/evidence/reconciliation.json
[h106]: https://github.com/laadkke-arch/agentflow-open/blob/eedd436d25f80db51d96b7b9f3cf2284889fedab/docs/workstreams/research/AF-RES-106/HANDOFF.md
[r106]: https://github.com/laadkke-arch/agentflow-open/blob/506f2f6e597899e653d99ab021ed36df0f1e45d6/docs/workstreams/research/AF-RES-106/RESULT.md
[l106]: https://github.com/laadkke-arch/agentflow-open/blob/506f2f6e597899e653d99ab021ed36df0f1e45d6/docs/workstreams/research/AF-RES-106/lineage.csv
[p106]: https://github.com/laadkke-arch/agentflow-open/blob/506f2f6e597899e653d99ab021ed36df0f1e45d6/docs/workstreams/research/AF-RES-106/predictions.csv
[ret106]: https://github.com/laadkke-arch/agentflow-open/blob/506f2f6e597899e653d99ab021ed36df0f1e45d6/docs/workstreams/research/AF-RES-106/returns.csv
[am106]: https://github.com/laadkke-arch/agentflow-open/blob/506f2f6e597899e653d99ab021ed36df0f1e45d6/docs/workstreams/research/AF-RES-106/METHOD_AMENDMENT.md
[co106]: https://github.com/laadkke-arch/agentflow-open/blob/506f2f6e597899e653d99ab021ed36df0f1e45d6/docs/workstreams/research/AF-RES-106/counts.json
[h107]: https://github.com/laadkke-arch/agentflow-open/blob/54fccba38c764032f9ecc5fac5a676a9e2a898f5/docs/workstreams/research/AF-RES-107/HANDOFF.md
[r107]: https://github.com/laadkke-arch/agentflow-open/blob/8ae7aad97c7a4e958cdfe078ff49262b3717874e/docs/workstreams/research/AF-RES-107/RESULT.md
[run107]: https://github.com/laadkke-arch/agentflow-open/blob/8ae7aad97c7a4e958cdfe078ff49262b3717874e/docs/workstreams/research/AF-RES-107/runs.jsonl
[el107]: https://github.com/laadkke-arch/agentflow-open/blob/8ae7aad97c7a4e958cdfe078ff49262b3717874e/docs/workstreams/research/AF-RES-107/elements.csv
[au107]: https://github.com/laadkke-arch/agentflow-open/blob/8ae7aad97c7a4e958cdfe078ff49262b3717874e/docs/workstreams/research/AF-RES-107/evidence/verification.json
[h108]: https://github.com/laadkke-arch/agentflow-open/blob/8b00aaa2eada69044c15784590956eecf5ea6268/docs/workstreams/research/AF-RES-108/HANDOFF.md
[r108]: https://github.com/laadkke-arch/agentflow-open/blob/806cdff845acfb965a1b2f2a641010c2e9604498/docs/workstreams/research/AF-RES-108/RESULT.md
[p108]: https://github.com/laadkke-arch/agentflow-open/blob/806cdff845acfb965a1b2f2a641010c2e9604498/docs/workstreams/research/AF-RES-108/pairs.csv
[m108]: https://github.com/laadkke-arch/agentflow-open/blob/806cdff845acfb965a1b2f2a641010c2e9604498/docs/workstreams/research/AF-RES-108/metrics.json
[run108]: https://github.com/laadkke-arch/agentflow-open/blob/806cdff845acfb965a1b2f2a641010c2e9604498/docs/workstreams/research/AF-RES-108/runs.jsonl
[self108]: https://github.com/laadkke-arch/agentflow-open/blob/806cdff845acfb965a1b2f2a641010c2e9604498/docs/workstreams/research/AF-RES-108/SELF_CHECK.md
[next]: NEXT_TASKS-27.json
