# REVIEW-22 · 링크를 따라간 뒤 사용자가 원하는 결과까지 얻을 수 있는가

GeoPandas에서는 같은 GeoParquet 1.1 파일 형식이라도 인코딩에 따라 옛 reader가 데이터를 온전히 돌려주거나 명시적으로 거절했다. MuseScore에서는 복제한 요소의 색이 달라져도 뒤이어 누른 키가 편집한 객체는 같았다. 탐색기가 링크 옆에 쓸 수 있는 설명의 범위는 사용자의 **다음 동작과 기대 결과**에서 갈렸다. 이번 네 작업 중 085·087은 고정한 실행 조건에서 검토 가능한 결과를 냈다. 086은 과거 문서 제공 시점, 088은 판과 실행 근거가 빈 상태로 남아 두 작업 모두 PARTIAL이다. [085 실행][v85] · [087 실행][run87] · [086 경로][den86] · [088 대응쌍][pair88]

## 검토한 범위

2026-11-23 UTC, work/planning의 최신 파일인 [REVIEW-21][prev]을 먼저 읽었다. 그 검토의 중앙 진행표 184137d와 이번 62a80b9를 ID별로 대조했다. 등록 82→86행, DONE 80→84행, BLOCKED 2→2행이다. 기존 82행의 필드는 모두 같고, 018·035가 계속 BLOCKED다. 새 DONE은 085–088뿐이다. 네 등록 커밋은 각각 작업 브랜치 끝과 일치하며 네 커밋 모두 마지막에 HANDOFF.md 한 파일을 추가했다. 중앙의 DONE 84행 중 acceptance_evidence에 항목이 있는 행은 0이다. 아래 연구 판정은 각 고정 인계·결과·원장의 내용으로 판단했다. [직전 진행표][old] · [이번 진행표][reg]

| 새 DONE | 고정 인계와 결과판 | 이 검토에서 대조한 자료 | 수용 범위 |
| --- | --- | --- | --- |
| 085 · codex-cloud | [7fc799c 인계][h85] · [9ce697f 결과][r85] | 24회의 GUI와 별도 API 6회, G/L 8쌍의 단계별 값, X1·X3 원 로그 | REVIEW_READY. 실험한 조작의 표시와 실제 대상 |
| 086 · web-pro | [6907534 인계][h86] · [e6a79c3 결과][r86] | 고정 9경로, 4권고의 전후, 최초 12사건과 추가 4사건, 생성·응답 기록 | PARTIAL. 판별한 현재 내용과 생성 파일은 인용 가능 |
| 087 · codex-cloud | [36a76b3 인계][h87] · [263fe75 결과][r87] | 4파일의 지문과 16번 읽기의 종료값·계약, 별도 혼형 입력의 행별 결과 | REVIEW_READY. 두 reader와 동일 의존판에서의 보존·거절 |
| 088 · web-pro | [a4c5f21 인계][h88] · [e173b53 결과][r88] | 60질문 모집표, 32대응쌍의 판정, 8질문의 후속 기록과 정정 원장 | PARTIAL. 공개 본문 수정 전후의 문서 적합성 |

085·087의 실행 횟수는 작업자가 남긴 원 출력에 근거한다. 이번 검토에서 수행한 일은 GitHub의 고정 결과·원장 재열람과 재집계다. 앱이나 reader를 새로 실행했거나 과거 사이트의 응답을 새로 취득한 횟수로 세지 않았다. 084까지의 내용은 REVIEW-21의 누적 판단에서 이어받았다.

## 제품 연구가 여기까지 확인한 것

사용자는 만들 소프트웨어의 전체 또는 일부 구조와 목적을 준다. 탐색기는 이미 쓸 수 있는 오픈소스·서비스, 연결할 부품, 시험이나 설계에 옮길 타 분야의 원리를 **해당 부분을 읽을 수 있는 링크**로 돌려주는 것을 목표로 한다. 최종 설계자는 각 제안을 개별 채택하거나 교체할 수 있어야 한다. 링크에 저장할 정보량, 자료 수집 시점, DB와 검색 방식은 열린 결정이다. [제품 연구 브리프][product] · [연구·정리 규칙][workflow]

| 설계자가 내려야 할 결정 | 084까지 이어진 근거 | 085–088 이후 쓸 수 있는 판단 |
| --- | --- | --- |
| 부분 요청에서 한 가지를 더 물을 때 | 020은 주장 72/73을 전달했으나 충돌 완전 해소는 2/16이었다. 070의 자연 요청 24건에서는 응답 하나로 정오가 바뀌었다고 독립 판정할 분모가 0이었다. 074의 구성 대조에서는 조건을 주자 8/8에서 답이 하나로 좁혀졌다. 082의 cibuildwheel은 옛 Python 사용자 요구를 이미 명시했다. | 088의 JN1은 전체 JSON이 추가돼도 같은 map 절을 반환한다. 이어서 확인할 대상은 전체 입력에서 Bash가 배열을 소비하는 방식으로 바뀐다. 이미 받은 조건과 다음에 필요한 조건을 각각 보존할 이유다. [누적 검토][prev] · [JN1 대응쌍][pair88] |
| 타 분야의 선례를 어디에 쓸지 | 010은 분야 단서를 주고 원리군 7개를 얻었다. 033의 단서 없는 144쌍에서는 넓은 의미 지지 1, 당시판 지지 0이었다. 069·073은 요청 접수와 말단 적용, 저장소 이전과 유지 책임 인수를 분리할 선례를 찾았다. 077의 보조 사례는 핵심 구현 선택 변화 0/3이었고, 081은 MuseScore 두 안을 가르는 복제 입력을 찾았다. | 085는 ‘복제 뒤 누가 실제 편집 대상인가’라는 시험을 GUI에 옮겼고, 숨은 자식의 잘못된 표시를 발견했다. 이 발견을 외부 원전이 원 개발자의 선택을 바꾼 사례로 셀 자료는 없다. [누적 검토][prev] · [085 조작과 반례][r85] |
| 링크에 어떤 조건·설명을 붙일지 | 021에서 두 절을 열어 공식 근거를 회수한 수는 주소만 6/23, 절 목록 9/23, 조건과 절 대응 14/23, 잘못 대응하면 8/23이었다. 066에서는 같은 주소가 반대 권고에도 붙었다. 022의 결정 우선 표본에서 미인지→변경→시행의 완전한 사슬은 0/24였다. 034의 부분 시간은 380→57초였으나 전체 시간은 849→847초였다. 078은 두 기능의 단독 실행과 합성 실행이 갈리는 입력을 보였다. | 086에서는 독자 목적을 고정했을 때 4권고 중 1건이 바뀌었다. 생성 HTML로 당시판 본문을 읽을 수 있다는 판단이다. 링크를 누른 사람이 예제나 후속 자원까지 이용했는지, 시간이 줄었는지는 미측정이다. [누적 검토][prev] · [권고 전후][comp86] |
| 어떤 판·기능·파일을 같은 것으로 볼지 | 032의 배포 참조 12건은 유지 9·교체 2·보류 1이었다. 055는 과거 답 4/4를 복구했지만 다음 판은 0/4였다. 071에서 통제 22/22를 재계산했고 075에서 양성 존재 15/15를 복구해도 유일·공동 1위는 각각 16/16 보류였다. 079는 옛 GDAL의 geometry·CRS 손실을 봤고, 083이 찾은 실제 GeoPandas 안내 두 문단은 PyArrow를 사용했다. | 087에서 같은 1.1.0의 WKB와 native가 옛 GeoPandas에서 갈렸다. 086에서 같은 생성물과 현재 응답의 지문이 일치해도 당시 게시 기록은 비었다. 링크 근거에 판, 실제 호출 경로, 사용자가 보존하려는 값, 관측 시점을 붙일 수 있다. [누적 검토][prev] · [파일별 두 reader][run87] · [발행과 응답][routes86] |
| 검색 범위와 후보 단위를 어디까지 넓힐지 | 060·064·068은 기능명이나 첫 절을 개선해도 두 조건의 공동 지지가 자주 비었다. 076의 자연 6요구×20후보 직접 양성은 0이었다. 080의 참조판에서 범위 확대 뒤 양성으로 바뀐 사례는 비교 가능한 자연 1/5, 교정 3/5였다. 084의 선택된 네 요청에서는 같은 확보본에서 넓힌 범위가 양성 3건과 기본 조합 반박 1건을 제공했다. 084의 개설 본문은 0/4였다. | 088은 리비전을 공개한 별도 표본을 사용했다. 좁은 후보 안에서 수정 전후 문서 판정은 0/26 변화였으나 채택 주해법 세 개는 모두 풀 밖이었다. 원래 도구 안의 다른 기능과 전후 처리 도구 중 어느 쪽이 필요한지 아직 갈리지 않았다. [누적 검토][prev] · [088 모집표][frame88] · [사후 답][out88] |

## 새 결과에서 지지되는 주장과 빠진 관측

### 085 · 화면색이 다를 때 실제 편집도 달라지는가

G는 공통 복사 때 선택 비트를 지우는 병합안, L은 새 파트의 요소를 순회하며 지우는 연구안이다. 원본 U를 포함한 세 빌드에서 네 조작을 두 번씩 실행했다. G/L 8쌍 중 복제 직후 비트가 다른 것은 6쌍이다. X1의 다성부 Explode는 마지막 범위 재선택으로 두 안의 목록이 같아졌고, X2는 붙여넣기 직후부터 같았다. X3은 실험용 레이어에서 숨겨 둔 Fingering이 순회 대상에서 빠졌다. 다시 보인 뒤 두 반복의 청색 픽셀은 G에서 0·0, L에서 8·8이었으며 두 안 모두 실제 선택 목록은 비어 있었다. 같은 자식을 처음부터 보인 X4에서는 G와 L 모두 기본색이었다. [085 검산과 화면][v85] · [X1 재선택][x1] · [X3 L][x3l] · [X3 G][x3g]

주 키가 문서 값을 바꾼 경우는 0/24다. X1·X2에서 누른 음가 키는 단일 음을 요구했고, X3·X4에서 V를 받았을 때는 선택 목록이 비어 있었다. 별도로 음이나 자식을 다시 클릭한 뒤에는 양쪽 모두 목표 값 변경과 undo가 됐다(24/24). **G를 권할 근거는 X3의 잘못된 표시를 막은 것**이다. G가 사용자의 재클릭을 줄였거나, 작동하는 범위 명령에서도 두 안의 편집 대상이 늘 같다는 주장은 이 절차로 가를 수 없다. [실행 원장][run85] · [후속 편집의 조건][r85]

### 086 · 저장된 파일을 읽는 것과 당시 주소에서 제공된 판

이번에 받은 9개 경로 중 HTTP 200은 8개, 목표판 내용이 식별된 것은 4개다. 정한 역사 관측창에서는 9개 모두 미확인이었다. 지정한 Read the Docs 네 실행의 HTML 생성 성공과 GitHub Pages 두 배포의 남은 inactive 상태는 확인했다. 당시 별도 게시 거래를 확인한 수는 전자 0/4, 당시 success를 직접 읽은 수는 후자 0/2다. P3는 두 독자 조건을 실제로 약속한 유일한 곳이다(원 1/6, 이번 1/4). stable/options와 1.x의 보관 본문은 모두 2025-11-14였으나 각각 02:26:28와 11:28:00 UTC였고, 주 관측창은 11–13일이었다. 동시 제공은 0/1 확인·1 미확인이다. [고정 9경로와 분모][den86] · [응답과 생성 기록][routes86]

R1은 1.1.12의 archive_read 설명을 읽으려는 사람에게 고정 생성 HTML을 줄 수 있게 됐다. R2에서는 현재 대표 HTML 두 개가 선택 생성물과 바이트까지 같았고 기존 추천을 유지했다. R1의 후속 생성 트리와 현재의 inactive 기록은 같은 파일의 소실을 증명하지 않는다. ‘어떤 자료를 주는가’는 1/4에서 바뀌었지만 ‘당시 공개됐는가’에 관한 사전 판단의 반전은 0/4였다. 처음 12사건과 추가 4사건에는 생성·게시·잘못된 응답·회복 직후 지문이 모두 이어지는 사례가 없었다. 가장 가까운 typst 사례에도 회복 직후 응답 지문이 빠졌다. 파일 뷰어에서 실제 예제 자원을 따라가는 비용과 성공도 아직 측정하지 않았다. [네 반환 카드][cards86] · [권고 전후][comp86] · [사건 원장][inc86]

### 087 · 위상이 같아도 같은 행 타입과 속성이 보존되는가

동일한 의존판에서 GeoPandas 0.14.4와 1.0.0이 각각 같은 SHA의 파일을 읽었다. F1–F3의 WKB는 12/12회에서 공간·속성 계약을 모두 통과했다. 사양판만 1.1.0으로 올린 WKB(F3)는 옛 reader에서도 읽혔고, 같은 사양의 native polygon/point(F4)는 옛 reader 2/2회에서 명시적으로 거절됐다. 새 reader는 F4를 2/2회 보존했다. 주 시험의 무음 손실은 0/16이다. 079의 GDAL에서 관측한 무음 손실, 083의 문구 수선 제안과 함께 보면, 특정 안내를 반환하려면 실제 reader와 인코딩을 먼저 확인해야 한다. [파일과 footer][files87] · [실행과 예외][run87] · [두 안내의 적용 범위][r87]

F4의 주 표본은 동종 2D 열이었다. 별도 혼형 G에서 새 reader는 WKB의 Point와 MultiPoint를 각각 보존했지만 native에서는 첫 Point도 MultiPoint로 읽었다. 두 행 모두 위상 동등성은 참이었다. 또 보조 F에서 pandas 메타데이터를 제거하자 geometry와 CRS가 살아 있어도 nullable Int16이 float64가 됐다. 정확 타입으로 행을 고르는 하류 질의나 Z 좌표까지 보존하는지에는 주 시험의 14회 성공을 그대로 적용할 수 없다. 두 원 문구를 따랐다가 피해를 본 실제 소비자는 0건이며 필수 정정 적중률은 0/0으로 산출할 수 없다. [G의 WKB][gw] · [G의 native][gn] · [속성 대조][f87] · [087 검토 범위][h87]

### 088 · 같은 링크가 남아도 되물을 내용이 달라지는가

jq·Pandoc에서 시간순 30개씩 모집한 뒤 자연층 4건과 본문 편집층 4건을 선택했다. 최초 보존 본문과 30일 안의 마지막 본문에 같은 네 기능씩을 대조한 64판정이 32쌍을 이룬다. 문서로 비교 가능한 26쌍은 충족 1·명시 반박 8·범위 밖 17로, 판정 변화가 0이었다. 나머지 6쌍은 모두 Pandoc 구현·입력·출력이 부족했다. JN1의 전체 JSON 추가는 map 링크의 정오를 유지하면서 조사자가 다음에 물을 입력을 바꿨다(1/32). 자연층의 명시 조건 변화 0/4와 편집층의 본문 변화 4/4는 각각 다른 선정 조건을 갖는다. [판정쌍][pair88] · [분모][met88] · [실행 인계][exec88]

현재 채택 표지는 3/8이고 주해법은 각각 yq, grid_tables, raw LaTeX였다. 모두 사전 후보 풀 밖이다. PN1의 작성자는 원하는 모양이라고 했지만 기존 방법을 계속 쓰고 다음 작업에서 grid table을 쓰겠다고 했다. 완전 성공 보고와 정확판에서의 성공 확인은 모두 0/8이다. PE1의 옛 그림과 즉시 게시 본문(0/8)도 확보하지 못했다. 재개 때 JE1의 게시 출력이 실제로는 첫 식과 일치함을 보조 jq 1.7에서 확인해 불일치 주장을 철회했고, PE1의 자료 ID 혼동은 정정 원장에 남겼다. 참조판 jq 1.7.1·Pandoc 3.1.11의 변환 횟수는 0이다. **25개의 음성 대응쌍과 같은 조사자의 재판독은 검색 품질의 안정성이나 독자에게 준 도움을 입증하기에 부족하다.** [질문자 후속 기록][out88] · [정정 원장][corr88] · [재개 인계][h88]

## 서로 어긋나는 결론을 가를 최소 관측

| 함께 놓을 결과 | 지금 가능한 판단 | 판정을 바꿀 근거 |
| --- | --- | --- |
| 077에서 두 판독은 지역 수정을 골랐고 실제 병합은 전역 수정이었다. 081의 직접 복제에서는 두 안의 비트가 갈렸고 085의 일반 메뉴에서는 표시 차이가 남아도 주 키의 값은 같았다. | 구현 선택·사용자가 보는 표시·다음 편집 명령은 각각 다른 질문이다. 보이는 자식만 방문하는 수정은 X3에서 표시 요구를 놓쳤다. | 같은 메뉴에서 실제 범위 값을 바꾸는 명령의 대상 ID, 피어의 전후 값과 undo를 G/L 한 쌍으로 확보한다. [085 원 출력][run85] |
| 082·086에서 생성과 현재 도달을 확인하고도 역사 제공은 비었다. 079·083·087에서 포맷명이 같아도 무음 손실·명시 거절·보존이 모두 등장했다. | 링크나 이름을 동일시할 수 있는 범위는 독자의 목적에 달렸다. 본문 인용과 자원 열람, 공간 위치와 정확 행 타입은 각각 다른 증거를 요구한다. | 문서는 본문 뒤에 따르는 파일의 판과 응답을 확인한다. 공간 파일은 같은 입력에 대한 타입 필터와 위치 필터가 돌려주는 행 ID를 비교한다. [086 카드][cards86] · [087 혼형][gn] |
| 080·084의 범위 확대에서는 쓸 만한 답을 찾았고, 088의 후보를 고정한 개정 비교에서는 변화가 없었다. 그 표본의 채택 해법은 모두 풀 밖이었다. | 전자는 자료 범위의 효과, 후자는 보존 본문 두 판과 단일 후보의 적합성이다. 출판된 채택 해법이 주 도구의 다른 절에 있을 수도 있다. | 미채점 질문에서 동일 본문·기준판·열람 예산으로 주 도구 전체와 인접 처리 단계까지 허용한 탐색을 대조한 뒤 공개 후속 결과를 연다. [088 후보][cand88] · [088 사후 답][out88] |

## 다음 네 작업

| ID · 담당 | 유일한 선행 인계 | 확인할 차이와 사용자에게 돌려줄 결과 |
| --- | --- | --- |
| 089 · codex-cloud | [085][h85] | MuseScore 범위에 V를 보낸 8회와 양성·음성 대조 4회에서 실제 변경 객체를 추적한다. 표시 수정 링크와 편집 대상 지정 링크의 적용 조건을 남긴다. |
| 090 · web-pro | [086][h86] | 네 문서 프로젝트에서 본문만 읽는 목적과 예제의 후속 자원까지 읽는 목적을 최대 두 번의 열람으로 대조한다. 고정 HTML 한 파일로 충분한 자리와 두 번째 링크가 필요한 자리를 판별한다. |
| 091 · codex-cloud | [087][h87] | 타입·Z가 다른 네 입력을 WKB와 native로 기록한 뒤 행 선택을 16회 판독한다. 공간적으로 같은 결과와 사용자가 원하는 같은 레코드를 가르는 링크 조건을 정한다. |
| 092 · web-pro | [088][h88] | 기존 여덟 사례에서 제외된 jq·Pandoc 질문 여섯 건으로 주 도구와 인접 처리 단계의 검색을 비교한다. 두 경로의 답을 봉인한 뒤 사후 답·채택·질문자 행동을 읽는다. |

네 작업은 서로 다른 브랜치와 소유 경로에서 시작한다. 090은 찾지 못한 옛 배포 영수증을 다시 찾는 대신 고정 파일의 다음 자원이 오늘 읽히는지 조사한다. 092는 좁은 풀의 알려진 채택 사례 세 건을 대조 자료로 남기고 새 여섯 건의 성과와 별도로 센다. 각 brief에 세부 질문 일곱 개, 직접 열람할 고유 1차 자료 24–26건의 종류와 기록 양식, 필수 표의 열, 중간 커밋과 마지막 인계 기준을 넣었다. [다음 작업 네 건](NEXT_TASKS-22.json)

[prev]: https://github.com/laadkke-arch/agentflow-open/blob/a98b44bcdb94f3143e099a09bd59e7f20869a1b5/docs/workstreams/planning/REVIEW-21.md
[old]: https://github.com/laadkke-arch/agentflow-open/blob/184137d2f257f5d1a7ef584e0f3a6b35f3d280cd/docs/automation/dot-control.json
[reg]: https://github.com/laadkke-arch/agentflow-open/blob/62a80b9f111c695527a8ca87bcb867796d2e96bb/docs/automation/dot-control.json
[product]: https://github.com/laadkke-arch/agentflow-open/blob/62a80b9f111c695527a8ca87bcb867796d2e96bb/docs/product/RESEARCH_BRIEF.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/62a80b9f111c695527a8ca87bcb867796d2e96bb/docs/RESEARCH_WORKFLOW.md
[h85]: https://github.com/laadkke-arch/agentflow-open/blob/7fc799ccbd5e458c94a5e680cae986c74c4a8671/docs/workstreams/research/AF-RES-085/HANDOFF.md
[r85]: https://github.com/laadkke-arch/agentflow-open/blob/9ce697f2552133108861cc5504ed64722dfde427/docs/workstreams/research/AF-RES-085/RESULT.md
[h86]: https://github.com/laadkke-arch/agentflow-open/blob/6907534462af729f409c52ce08d3331de22c96e6/docs/workstreams/research/AF-RES-086/HANDOFF.md
[r86]: https://github.com/laadkke-arch/agentflow-open/blob/e6a79c3ac05b84ea1c7db313233df1717cade756/docs/workstreams/research/AF-RES-086/RESULT.md
[h87]: https://github.com/laadkke-arch/agentflow-open/blob/36a76b384810730b7d819a5ed469e6e8ded92f8a/docs/workstreams/research/AF-RES-087/HANDOFF.md
[r87]: https://github.com/laadkke-arch/agentflow-open/blob/263fe7581cf45eadd1f05139aacaadb27290b86e/docs/workstreams/research/AF-RES-087/RESULT.md
[h88]: https://github.com/laadkke-arch/agentflow-open/blob/a4c5f217313b5682d9d86c8507a7b5639dda89dd/docs/workstreams/research/AF-RES-088/HANDOFF.md
[r88]: https://github.com/laadkke-arch/agentflow-open/blob/e173b53f071aabfa749d33ab7da7ce970d5641b5/docs/workstreams/research/AF-RES-088/RESULT.md
[v85]: https://github.com/laadkke-arch/agentflow-open/blob/9ce697f2552133108861cc5504ed64722dfde427/docs/workstreams/research/AF-RES-085/evidence/verify.json
[run85]: https://github.com/laadkke-arch/agentflow-open/blob/9ce697f2552133108861cc5504ed64722dfde427/docs/workstreams/research/AF-RES-085/runs.jsonl
[x1]: https://github.com/laadkke-arch/agentflow-open/blob/9ce697f2552133108861cc5504ed64722dfde427/docs/workstreams/research/AF-RES-085/evidence/gui/X1-G-1/app.jsonl
[x3l]: https://github.com/laadkke-arch/agentflow-open/blob/9ce697f2552133108861cc5504ed64722dfde427/docs/workstreams/research/AF-RES-085/evidence/gui/X3-L-1/app.jsonl
[x3g]: https://github.com/laadkke-arch/agentflow-open/blob/9ce697f2552133108861cc5504ed64722dfde427/docs/workstreams/research/AF-RES-085/evidence/gui/X3-G-1/app.jsonl
[den86]: https://github.com/laadkke-arch/agentflow-open/blob/e6a79c3ac05b84ea1c7db313233df1717cade756/docs/workstreams/research/AF-RES-086/evidence/route-denominators.json
[routes86]: https://github.com/laadkke-arch/agentflow-open/blob/e6a79c3ac05b84ea1c7db313233df1717cade756/docs/workstreams/research/AF-RES-086/routes.jsonl
[comp86]: https://github.com/laadkke-arch/agentflow-open/blob/e6a79c3ac05b84ea1c7db313233df1717cade756/docs/workstreams/research/AF-RES-086/comparison.json
[cards86]: https://github.com/laadkke-arch/agentflow-open/blob/e6a79c3ac05b84ea1c7db313233df1717cade756/docs/workstreams/research/AF-RES-086/cards.md
[inc86]: https://github.com/laadkke-arch/agentflow-open/blob/e6a79c3ac05b84ea1c7db313233df1717cade756/docs/workstreams/research/AF-RES-086/incidents.csv
[files87]: https://github.com/laadkke-arch/agentflow-open/blob/263fe7581cf45eadd1f05139aacaadb27290b86e/docs/workstreams/research/AF-RES-087/files.csv
[run87]: https://github.com/laadkke-arch/agentflow-open/blob/263fe7581cf45eadd1f05139aacaadb27290b86e/docs/workstreams/research/AF-RES-087/runs.jsonl
[gw]: https://github.com/laadkke-arch/agentflow-open/blob/263fe7581cf45eadd1f05139aacaadb27290b86e/docs/workstreams/research/AF-RES-087/evidence/auxiliary/G-WKB.json
[gn]: https://github.com/laadkke-arch/agentflow-open/blob/263fe7581cf45eadd1f05139aacaadb27290b86e/docs/workstreams/research/AF-RES-087/evidence/auxiliary/G-native.json
[f87]: https://github.com/laadkke-arch/agentflow-open/blob/263fe7581cf45eadd1f05139aacaadb27290b86e/docs/workstreams/research/AF-RES-087/evidence/auxiliary/F-no-pandas-meta.json
[pair88]: https://github.com/laadkke-arch/agentflow-open/blob/e173b53f071aabfa749d33ab7da7ce970d5641b5/docs/workstreams/research/AF-RES-088/pairs.csv
[met88]: https://github.com/laadkke-arch/agentflow-open/blob/e173b53f071aabfa749d33ab7da7ce970d5641b5/docs/workstreams/research/AF-RES-088/metrics.json
[frame88]: https://github.com/laadkke-arch/agentflow-open/blob/e173b53f071aabfa749d33ab7da7ce970d5641b5/docs/workstreams/research/AF-RES-088/frame.csv
[cand88]: https://github.com/laadkke-arch/agentflow-open/blob/e173b53f071aabfa749d33ab7da7ce970d5641b5/docs/workstreams/research/AF-RES-088/candidates.csv
[out88]: https://github.com/laadkke-arch/agentflow-open/blob/e173b53f071aabfa749d33ab7da7ce970d5641b5/docs/workstreams/research/AF-RES-088/outcomes.jsonl
[corr88]: https://github.com/laadkke-arch/agentflow-open/blob/e173b53f071aabfa749d33ab7da7ce970d5641b5/docs/workstreams/research/AF-RES-088/evidence_corrections.jsonl
[exec88]: https://github.com/laadkke-arch/agentflow-open/blob/e173b53f071aabfa749d33ab7da7ce970d5641b5/docs/workstreams/research/AF-RES-088/execution/README.md
