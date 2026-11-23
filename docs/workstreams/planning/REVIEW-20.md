# REVIEW-20 · 두 링크를 함께 추천해도 되는가, 옛 권고를 어디까지 유지할 수 있는가

**두 부품을 함께 추천하려면 같은 입력이 두 단계를 거쳐 사용자가 요구한 결과로 돌아오는지 확인해야 한다.** 이번에 그 차이를 직접 보여 준 것은 표 데이터와 이미지 묶음의 고정판 실행이다. 또 다른 실행에서는 파일을 정상적으로 열고도 지리 좌표 정보를 잃었다. 반면 다른 분야의 원전을 건네서 개발자의 구현 선택이 바뀌었는지, 넓은 목록이 원 요청 당시 쓸 만한 답을 더 많이 포함했는지는 여전히 판별할 수 없었다. 아래의 수치는 각각 어떤 선택에 쓸 수 있는지를 기준으로 읽는다. [078 실행 비교][r78] · [079 역사판 관측][gn79] · [077 보기][v77] · [080 셀 원장][m80]

## 이번 검토의 범위와 판정

work/planning의 가장 최근 검토는 [REVIEW-19][prev]다. 거기서 사용한 [통합판 0d2b084][old]과 이번 [통합판 e7a777f][reg]의 작업 배열 전부를 ID로 대조했다. 등록 74→78, DONE 72→76, BLOCKED 2→2, 현재 RUNNING 0이다. 기존 74행의 필드는 그대로였고 018과 035가 BLOCKED다. 새 DONE은 077–080 네 건이다. 네 작업 모두 중앙 result_commit과 해당 작업 브랜치 끝이 일치했고 마지막 변경은 HANDOFF.md 한 파일이었다. DONE 76행의 중앙 acceptance_evidence 배열은 모두 비어 있었다. 아래의 연구 판정은 각 고정 인계와 결과 원장을 읽어 확인했다. 이전 연구의 상세 파일은 다시 열지 않았다.

| 새 DONE · 작업자 역할 | 고정 인계 / 결과 | 실제로 검토할 수 있는 단위 | 연구 수용 범위 |
| --- | --- | --- | --- |
| 077 · web-pro | [a6338ff 인계][h77] / [5170e3e 결과][r77] | 모집 30행, 보조 사례 3, 동종·타 분야 보기 6, 고정 입력 9 | PARTIAL. 원전별로 가능한 설명과 기각 사유가 있다. 주 표본 0/3, 목표 실행 0/9다. |
| 078 · codex-cloud | [f83a48c 인계][h78] / [c23f626 결과][r78] | 설정 8개×시나리오 3개, 본실험 48시도, 별도 진단 18행 | REVIEW_READY. 두 합성 작업과 지정 실행판에서 단독·결합·재제출 결과를 검산할 수 있다. |
| 079 · web-pro | [cc527e2 인계][h79] / [1398a21 결과][r79] | 자연 사건 8, 대조 3, 관측 104행, 관계 26행 | PARTIAL. 자연 7/8에서 역사 양판의 동작을 관측했다. 실제 운영 추천 기록에 적용한 사례는 0개다. |
| 080 · codex-cloud | [152f526 인계][h80] / [cece879 결과][r80] | 자연 120이슈·교정 200이슈에서 계획 12자리, 범위×판 48셀 | PARTIAL. 최초 확보본과 참조판에서는 일부 짝을 비교할 수 있다. 최초 게시 당시 본문을 요구한 엄격 기준에서는 48셀 모두 미확인이다. |

이번 검토에서는 077의 보기별 발췌량·모든 후보 예측 수·보조 관측 수를 원행에서 셌다. 078은 비교 612행에서 전체 충족과 요건별 충족을 각각 집계해 보관된 126개 집계행 모두와 대조했다. 079는 관계행이 가리키는 관측 ID와 URL 규칙 11행을 점검했다. 080은 48셀에서 엄격·최초 확보본의 짝을 따로 다시 계산했다. 모집표 321행에는 이슈 없는 Click 교정 공석 1행이 포함된다. 각 작업자가 남긴 과거 실행 영수증을 읽었고, 이번 계획 검토의 검증 범위는 원장 재계산까지다. [077 시험][t77] · [078 비교][cmp78] · [078 집계][sum78] · [079 관계][rel79] · [080 모집][f80]

## 여기까지의 전체 흐름

사용자가 주는 것은 소프트웨어 전체나 일부의 구조, 목적, 보존할 조건이다. 받아 가고 싶은 것은 바로 쓸 완성품·서비스, 가져다 붙일 기능, 다른 분야에서 빌려 설계나 시험을 바꿀 원리와 그 출처다. 최종 설계자가 어떤 묶음을 버리거나 조합할 수 있도록 입력 형식, 저장량, 검색 경로, 확인 시점을 대안으로 남긴다. [제품 연구 브리프][product] · [연구 운영 규칙][workflow]

| 설계할 때 가를 질문 | 076까지 축적된 근거 | 077–080 이후 해석 |
| --- | --- | --- |
| 부분 요청에 어떤 정보를 더 받아야 하나? | 초기 연구에서 금지 조건이 누락됐다. 020은 조립 때 주장 72/73을 전달했지만 충돌을 완전히 푼 것은 2/16이었다. 070은 24건에서 독립 정오 변화를 판별할 분모가 0이었다. 074의 구성 대조 4쌍에서는 한 값을 준 뒤 8/8이 단일 정답이었으나 자연 요청 8건에서는 양쪽 값 정오를 판별하지 못했다. | 실제로 결과를 가른 입력을 물을 후보가 생겼다. 예컨대 기존 ZIP에 갱신하는지, 옛 소비자가 정확히 같은 스키마를 요구하는지다. 실제로 질문을 받은 사람이 응답할지와 얼마나 절약할지는 미측정이다. |
| 관계를 검색하거나 외부 원리를 주면 무엇을 얻나? | 010은 분야 단서가 있는 원전에서 7개 원리군을 찾았다. 033의 단서 없는 144쌍에서 넓은 지지 1쌍·당시판 지지 0이었다. 069는 요청 접수와 말단 적용을 가르는 시험 관점을, 073은 저장소 이전과 유지 책임 인수를 가르는 선례를 찾았다. 073의 세 검색 보기 각 30자리에서 두 조건 공동 입증은 모두 0이었고, 창설 원고 검증도 0/3이었다. | 077은 제공된 원전의 어디까지 옮길지 설명했지만 세 보조 사례의 핵심 구현 선택은 양쪽 보기가 같았다. 발견·설명·구현안 변화·원 개발자의 채택에 서로 다른 관측이 필요하다. |
| 링크와 근거 설명이 선택과 작업량을 바꾸나? | 021의 두 절 열람 예산에서 공식 지지와 근거 회수는 주소 6/23, 절 목록 9/23, 조건–절 연결 14/23, 잘못 연결한 경우 8/23이었다. 066에서는 같은 주소가 반대 권고 양쪽에 붙었다. 022의 결정 우선 24건에서 미인지→변경→시행의 완전 연쇄는 0건, 034의 부분 과제 중앙시간은 380→57초였으나 전체는 849→847초였다. | 078은 조건을 명시하면 조립의 오승인을 줄일 수 있는 구체적 사례를 준다. 합성 입력에서의 기술적 판별로 실제 개발자의 채택률·재작업·시간을 계산할 수는 없다. |
| 과거 답을 복원하고 기능의 후계를 추적하려면? | 032의 배포 참조 12건은 현재 용도 유지 9·교체 2·보류 1이었다. 055는 과거 답 0/4→2/4→4/4를 복원했으나 다음 판 판단은 모두 0/4였다. 071은 원본이 소실된 통제 22쌍에서 실제 조각과 설정을 보관한 경우 22/22를 재계산했다. 075의 유한 등록부에서는 대표 원문으로 양성 존재 15/15를 복원했지만 유일·공동 1위는 각각 16/16 보류였다. 키와 순회 영수증이 함께 틀리면 요약 보관안도 오판했다. | 079는 무엇이 같은 기능인지도 용도와 소비판에 따라 달라짐을 보였다. 옛 기록에 어떤 주장을 했는지와 새 관계의 방향·적용판을 함께 보존할 이유가 있다. 실제 하류 문서 중 어디를 고쳐야 하는지는 따로 남았다. |
| 목록과 반환 설명은 어느 정도면 충분한가? | 060·064·068에서 이름이나 시작 절을 개선해도 두 조건의 공동 근거가 자주 비었다. 072의 자연 직접 적격 분모는 0, 판독 메모는 54자리 중 6개였다. 076은 표시 108자리에 근거를 남겼다. 자연 6요구×20후보는 직접 0, 교정 직접 5쌍은 링크·발행자 한 줄·동작 카드 모두 5/5 회수했다. 자연 부분 근거 회수는 각각 4/10·5/10·4/10, 표시에서 두 조건과 환경을 함께 확인한 자리는 0/108이었다. | 080은 원 자료집에 무엇이 수록됐는지를 별도로 물었다. 현재 참조판의 넓은 목록이 일부 요구에서 도움이 됐지만, 어느 범위와 판을 수집해야 실제 요청에 유리한지는 미확인이다. |

이 수치는 연구별 모집층과 판독 예산에 한정된다. 특히 반환한 후보 수와 조건을 지지하는 절의 수, 채택한 사람 수에는 공통 분모가 없다. [직전 누적 검토와 각 원장 연결][prev]

## 새 결과에서 확인한 것과 남은 공백

### 077 · 원전의 설명이 달라도 선택을 가르는 입력은 없을 수 있다

Shotcut에서는 원본과 편집 상태를 나누는 darktable 자료, MuseScore에서는 증거본의 참여 범위를 다루는 TEI 자료, Sigil에서는 내용과 논리 경로를 나누는 OCFL 규격을 제공했다. 6개 보기의 후보 13개를 비교하니 경쟁 후보 집합은 2/3에서 달랐고, 정규화한 핵심 선택의 변화는 0/3이었다. 예를 들어 두 MuseScore 판독은 파트 안에서만 복제 요소의 선택을 해제하는 안을 골랐다. 당시 유지관리자가 실제로 병합한 것은 모든 요소의 복사 생성자에서 비트를 지우는 변경이었다. 어느 쪽이 다른 파트의 요구까지 더 잘 보존하는지 가를 실행 결과는 없다. [보기별 선택][v77] · [사례집][cb77] · [당시 병합 PR][mspr]

얕았던 지점은 외부 문헌 수보다 **실제 대상과 입력의 대응**이다. 첫 10건씩 30행에서 엄격 적격 사례와 최초 본문 확인은 각각 0/3이었다. 당시판 대상 자료도 요구했던 독립 6계보 중 확인 3이었다. 9입력·후보 예측 39개 중 보조 코드가 확인한 것은 5입력의 좁은 조건이며 완전한 목표 실행은 0/9다. Sigil 원 신고는 참조와 목적지가 함께 이동하는 경우였고 실험의 하위 폴더 이동은 그 판에서 지원되지 않았다. MuseScore 선택색은 mark로도 달라지므로 생성 직후 flag와 목록을 같이 읽어야 한다. 두 보기에 같은 상한을 적용했어도 실제 발췌는 3,593자와 4,912자였다. 시험 입력은 독해 전에 고정했으므로 ‘새 시험 0/9’에서 원전이 새 시험을 만드는 능력은 추정할 수 없다. [모집 원장][f77] · [시험 원장][t77] · [봉인본 정정][err77]

### 078 · 단독 성공과 연결 성공을 가른 것은 중간 표현과 이전 산출물이었다

SQLite의 SQL NULL, 빈 텍스트, 문자 그대로의 NULL을 구분하려면 앞단이 다른 값으로 기록하고 뒤에서도 그 구분을 읽어야 했다. T01은 지정 입력·CPython 3.13.5에서 빈 비인용 필드를 복원했지만 같은 옵션 이름의 3.12.14는 그렇지 않았다. 별도 NUL 문자를 넣자 CLI가 문자열 뒤를 잘라 양쪽 명령이 정상 종료해도 값이 달라졌다. 이미지에서는 같은 이름의 두 파일을 다른 디렉터리에 두었다. 앞단에서 경로를 버리면 하나가 덮이고, 뒤에서 경로를 버리면 ZIP 중복 오류가 났다. 경로를 모두 보존해 새 ZIP을 만드는 I00은 성공했다. 같은 설정을 기존 ZIP에 재제출하면 오래된 세 번째 멤버가 남았다. [단계별 계약][con78] · [본실험][run78] · [별도 진단][diag78]

단독 근거만 본 A는 표 데이터의 전체 충족을 주 비교 1/8과 봉인 비교 1/4에서 잘못 승인했다. 이미지 봉인에서는 A가 전체 4/4를 맞히면서도 개별 요건 9/24를 잘못 승인했다. 연결 계약을 더한 B는 주 비교의 16개 설정·시나리오 짝을 모두 맞혔고, 봉인 입력의 실제 양성은 분야별 1건씩 보류했다. 주 비교에서 실행 결과를 보고 진단한 C와 봉인 입력 공개 전에 예측한 C도 구별해야 한다. 분야별 정상·봉인 입력이 각 하나고 같은 연구자가 설계와 재판독을 맡았다. 자연 사용자 요구, 다른 뷰어, 동시 게시까지 이 수치를 확대할 근거는 없다. [예측 대 실제][cmp78] · [집계 분모][sum78] · [작업자의 재생 영수증][replay78]

### 079 · 주소를 살린 뒤에도 옛 소비자의 용도를 다시 확인해야 한다

GDAL의 G04에서 새 GEOARROW struct 파일을 구 3.8 소비자가 열었을 때 종료값은 0이었지만 geometry 필드는 0개였고 CRS가 없었다. 기존 WKB 읽기는 보존됐다. 판 한정 별칭은 geometry와 CRS를 복구하면서 bbox 속성 네 개를 더했다. 필수 속성만 있으면 되는 독자와 정확히 같은 스키마가 필요한 독자는 같은 수선을 받아들일 수 없다. 반대 결과도 있다. G03의 조사 입력에서는 포맷판을 바꿨는데도 구 소비자가 필수 값과 geometry·CRS를 보존했다. SciPy O01은 정상값을 맞춘 변환 뒤에도 빈 배열의 출력 형상이 달라졌다. GIS는 재구성 환경으로 GDAL 외에 C++ Arrow·PROJ·빌드도 달랐다. [양판 관측][gn79] · [SciPy 실행 대응][oss79] · [연구 결론][r79]

자연 8사건 중 7건, 대조 3사건 중 0건에서 과거 양판을 실행했다. URL만 보는 정책은 자연에서 위치 수선 2·유지 1·보류 5였다. G03과 G04는 같은 주소에 같은 수선을 받았지만 그 결정이 보존하는 행동은 달랐다. 관계 26행 중 ‘분리’ 2행은 실제 혼합 레코드가 있을 때의 제안이다. 실제 서비스에서 사용한 추천 레코드는 한 건도 제공되지 않아 운영 오병합률은 산출할 수 없다(0/0). 현재 HTTP 응답 11개로 당시 리다이렉트 경로도 증명할 수 없었다. [URL 규칙의 실제 조치][u79] · [관계와 역방향 수선][rel79] · [모집과 실행 유무][f79]

### 080 · 목록에 있는 답과 당시 사용자가 확인한 답 사이에 어떤 자료가 빠졌나

Click·attrs에서 자연 첫 확보본 6건, 닫힌 이슈의 교정 첫 확보본 5건을 읽었다. Click 교정 셋째 자리는 공석이다. 참조판에서 좁은 목록의 알려진 비양성이 넓은 목록에서 양성으로 바뀐 경우는 양쪽을 판정한 자연 5자리 중 1, 교정 5자리 중 3이었다. AN02는 ‘좁음 미확인→넓음 양성’이라 이 회복 수에 들어가지 않는다. 네 조합을 모두 관측한 최초 확보본은 자연 2/6, 교정 0/6이었다. 따라서 두 범위의 차이를 일부 볼 수 있지만 범위 효과와 판 효과를 일반적으로 가를 수 없다. [48셀][m80] · [당시 요구와 사후 답][gold80] · [대응쌍 집계][metrics80]

원래 게시한 본문을 확인한 자리는 0/12, 교정 다섯 보고에서 성공 배포판 확인은 0/5다. 보정한 참조판의 양성·경계 관측 8/8은 정확 성공판에서 실행할 계획 8건을 대신하지 못한다. AC01 작성자는 slots=False 경로의 작동을 보고했지만 당시 두 레지스트리 키 출력은 없다. 참조판에서는 두 번째 키 조회가 실패했고 전용 훅은 두 키를 유지했다. 어느 판이나 입력 차이 때문인지는 미확인이다. AC02는 연구자가 원문의 모듈 범위를 함수 안으로 옮겨 첫 실행이 실패했고, 그 실패와 보정 후 관측을 보존했다. 이 두 사례에서 ‘원 작성자가 틀렸다’, ‘현재 예제가 그대로 당시에도 작동했다’는 결론을 낼 수 없다. [보정 전후 실행][run80] · [계측 정정][fix80] · [AC01 작성자 보고][ac01]

## 서로 어긋나 보이는 결론이 바꾸는 결정

| 함께 읽을 결과 | 확인된 불일치 또는 비교 조건의 차이 | 결정을 바꿀 다음 관측 |
| --- | --- | --- |
| 073의 타 분야 선례와 077의 선택 변화 0/3 | 전자는 후보·시험 관점의 발견, 후자는 이미 주어진 원전으로 낸 구현 선택이었다. 같은 MuseScore 요구 안에서는 두 판독의 지역 수정과 실제 병합된 전역 수정이 갈렸다. | 두 경로가 다르게 동작할 수 있는 일반 복사와 파트 복사를 같은 소스·악보에서 실행한다. |
| 078의 연결 계약과 079의 후계 별칭 | 078의 I00은 새 파일에서는 적합하고 재제출에서 실패했다. 079의 동일 별칭도 geometry 보존에는 유용하지만 정확 스키마 요건을 남겼다. 두 결과 모두 ‘어떤 조건에서’라는 칸을 비워 둔 권고가 잘못될 수 있음을 보인다. | 소비자가 실제 남긴 발행 요구와 대상판을 찾아 한 링크·두 링크·조건부 답 중 어디까지 뒷받침되는지 비교한다. |
| 076의 자연 직접 양성 0과 080의 참조판 회복 | 076은 정해진 20후보 안의 직접 적격을, 080은 다른 요청에서 공식 문서·시험까지 목록을 넓힐 때의 공동 판정을 셌다. 080의 AC01에서는 목록에 들어 있는 작성자의 방법과 공동 조건을 지지한 전용 훅마저 다르다. | 같은 최초 본문·소비판·기능 ID를 고정한 짝에서 이름 등재, 공동 충족, 원 작성자의 성공을 따로 재계산한다. |

현재 조립할 수 있는 대안은 링크에 **무엇을 할 때 유용한가**, **어느 판의 어느 절이나 실행이 그 말을 지지하는가**, **어떤 입력이면 다음 확인이 필요한가**를 붙이는 것이다. 여러 부품이 필요하면 중간 데이터와 게시 상태를 한 줄 더 담는 방식을, 옛 지침을 고치면 이전 판정과 적용 기간을 남기는 방식을 비교할 수 있다. 모든 링크를 상세 색인할지, 언제 원문을 열지, 서비스와 부품 중 어느 것을 먼저 제시할지는 후속 판단으로 남는다.

## PLAN#20 · 독립적으로 배정할 네 작업

| 작업 · 담당 | 단 하나의 고정 인계 | 완성할 판단과 독립 범위 |
| --- | --- | --- |
| 081 · codex-cloud | [077][h77] | 같은 MuseScore 소스의 원본·지역 수정·전역 수정에 악보 조작 여섯 자리를 적용한다. 새 파트와 일반 복사에서 어디까지 상태가 보존되는지 판독 가능한 실행표를 남긴다. |
| 082 · web-pro | [078][h78] | Python·R 문서 사이트의 실제 발행 요구를 모집한다. 호스팅 서비스만 안내할 때와 생성기·게시처를 함께 안내할 때 독자가 확인할 수 있는 조건과 배포 근거를 남긴다. |
| 083 · web-pro | [079][h79] | GDAL G04와 SciPy O02를 참조한 하류의 공개 지침에서 실제 변경이 필요한 대상을 판독한다. 한꺼번에 주소를 바꾸는 방법과 목적별 수선안을 실제 후속 배포·복구 근거로 비교한다. |
| 084 · codex-cloud | [080][h80] | Click·attrs의 기존 사례 네 개를 지정해 생성 이벤트와 질문판·성공판을 복원한다. 16개 셀에서 근거가 바뀐 이유를 재계산하고 남은 공석을 표시한다. |

각 작업은 자기 선행판과 공개 원자료만으로 시작할 수 있다. 작업 간 힌트·새 결과나 같은 사례의 후속 판독자를 공유할 필요가 없다. 필수 표의 열, 원자료 최소량, 반례, 파일별 내용, 중간 커밋과 인계 전 검산은 [배정용 JSON][next]의 각 brief에 들어 있다.

[prev]: https://github.com/laadkke-arch/agentflow-open/blob/bc5dc7e1380e357103406048a26a4fb2af9e232e/docs/workstreams/planning/REVIEW-19.md
[old]: https://github.com/laadkke-arch/agentflow-open/blob/0d2b08431067e8d87212a66ecb27657c65722a59/docs/automation/dot-control.json
[reg]: https://github.com/laadkke-arch/agentflow-open/blob/e7a777f2c13b626532b5828591d6388743688b34/docs/automation/dot-control.json
[product]: https://github.com/laadkke-arch/agentflow-open/blob/e7a777f2c13b626532b5828591d6388743688b34/docs/product/RESEARCH_BRIEF.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/e7a777f2c13b626532b5828591d6388743688b34/docs/RESEARCH_WORKFLOW.md
[h77]: https://github.com/laadkke-arch/agentflow-open/blob/a6338ffd6bc04d45f97e211031bd22aa870fbba0/docs/workstreams/research/AF-RES-077/HANDOFF.md
[r77]: https://github.com/laadkke-arch/agentflow-open/blob/5170e3e07d2278800480e1d71cc2f2a2ce9ab01a/docs/workstreams/research/AF-RES-077/RESULT.md
[v77]: https://github.com/laadkke-arch/agentflow-open/blob/5170e3e07d2278800480e1d71cc2f2a2ce9ab01a/docs/workstreams/research/AF-RES-077/VIEWS.csv
[cb77]: https://github.com/laadkke-arch/agentflow-open/blob/5170e3e07d2278800480e1d71cc2f2a2ce9ab01a/docs/workstreams/research/AF-RES-077/CASEBOOK.md
[t77]: https://github.com/laadkke-arch/agentflow-open/blob/5170e3e07d2278800480e1d71cc2f2a2ce9ab01a/docs/workstreams/research/AF-RES-077/TESTS.csv
[f77]: https://github.com/laadkke-arch/agentflow-open/blob/5170e3e07d2278800480e1d71cc2f2a2ce9ab01a/docs/workstreams/research/AF-RES-077/FRAME.csv
[err77]: https://github.com/laadkke-arch/agentflow-open/blob/5170e3e07d2278800480e1d71cc2f2a2ce9ab01a/docs/workstreams/research/AF-RES-077/evidence/ERRATA.md
[h78]: https://github.com/laadkke-arch/agentflow-open/blob/f83a48c1c93f39796be82fee3d74b731b1a42f87/docs/workstreams/research/AF-RES-078/HANDOFF.md
[r78]: https://github.com/laadkke-arch/agentflow-open/blob/c23f6262b733d9a710a77de8b474689e510fb57c/docs/workstreams/research/AF-RES-078/RESULT.md
[con78]: https://github.com/laadkke-arch/agentflow-open/blob/c23f6262b733d9a710a77de8b474689e510fb57c/docs/workstreams/research/AF-RES-078/contracts.csv
[run78]: https://github.com/laadkke-arch/agentflow-open/blob/c23f6262b733d9a710a77de8b474689e510fb57c/docs/workstreams/research/AF-RES-078/runs.jsonl
[diag78]: https://github.com/laadkke-arch/agentflow-open/blob/c23f6262b733d9a710a77de8b474689e510fb57c/docs/workstreams/research/AF-RES-078/evidence/diagnostics.jsonl
[cmp78]: https://github.com/laadkke-arch/agentflow-open/blob/c23f6262b733d9a710a77de8b474689e510fb57c/docs/workstreams/research/AF-RES-078/comparisons.csv
[sum78]: https://github.com/laadkke-arch/agentflow-open/blob/c23f6262b733d9a710a77de8b474689e510fb57c/docs/workstreams/research/AF-RES-078/evidence/counts.csv
[replay78]: https://github.com/laadkke-arch/agentflow-open/blob/c0b757fac1f1e947447022aab1a7ea2e48ac8c74/docs/workstreams/research/AF-RES-078/evidence/replay.json
[h79]: https://github.com/laadkke-arch/agentflow-open/blob/cc527e2c4f827afaaaa63f75c897d863c3adcc80/docs/workstreams/research/AF-RES-079/HANDOFF.md
[r79]: https://github.com/laadkke-arch/agentflow-open/blob/1398a21f724e3b6c7ad81ee2f56b44715a5c00bd/docs/workstreams/research/AF-RES-079/RESULT.md
[gn79]: https://github.com/laadkke-arch/agentflow-open/blob/1398a21f724e3b6c7ad81ee2f56b44715a5c00bd/docs/workstreams/research/AF-RES-079/streams/gis/historical/observations.jsonl
[oss79]: https://github.com/laadkke-arch/agentflow-open/blob/1398a21f724e3b6c7ad81ee2f56b44715a5c00bd/docs/workstreams/research/AF-RES-079/streams/oss/historical/HISTORICAL_RESULTS.md
[u79]: https://github.com/laadkke-arch/agentflow-open/blob/1398a21f724e3b6c7ad81ee2f56b44715a5c00bd/docs/workstreams/research/AF-RES-079/evidence/url-policy-comparison.json
[rel79]: https://github.com/laadkke-arch/agentflow-open/blob/1398a21f724e3b6c7ad81ee2f56b44715a5c00bd/docs/workstreams/research/AF-RES-079/relations.csv
[f79]: https://github.com/laadkke-arch/agentflow-open/blob/1398a21f724e3b6c7ad81ee2f56b44715a5c00bd/docs/workstreams/research/AF-RES-079/frame.csv
[h80]: https://github.com/laadkke-arch/agentflow-open/blob/152f5261ab9a35ab675ab003931ac4dc89966b55/docs/workstreams/research/AF-RES-080/HANDOFF.md
[r80]: https://github.com/laadkke-arch/agentflow-open/blob/cece879e89d670a50dc64b309cb18c2f2745e60c/docs/workstreams/research/AF-RES-080/RESULT.md
[f80]: https://github.com/laadkke-arch/agentflow-open/blob/cece879e89d670a50dc64b309cb18c2f2745e60c/docs/workstreams/research/AF-RES-080/frames.csv
[m80]: https://github.com/laadkke-arch/agentflow-open/blob/cece879e89d670a50dc64b309cb18c2f2745e60c/docs/workstreams/research/AF-RES-080/matches.csv
[gold80]: https://github.com/laadkke-arch/agentflow-open/blob/cece879e89d670a50dc64b309cb18c2f2745e60c/docs/workstreams/research/AF-RES-080/gold.jsonl
[metrics80]: https://github.com/laadkke-arch/agentflow-open/blob/cece879e89d670a50dc64b309cb18c2f2745e60c/docs/workstreams/research/AF-RES-080/evidence/metrics.json
[run80]: https://github.com/laadkke-arch/agentflow-open/blob/cece879e89d670a50dc64b309cb18c2f2745e60c/docs/workstreams/research/AF-RES-080/runs.jsonl
[fix80]: https://github.com/laadkke-arch/agentflow-open/blob/cece879e89d670a50dc64b309cb18c2f2745e60c/docs/workstreams/research/AF-RES-080/evidence/fixture-correction.md
[mspr]: https://github.com/musescore/MuseScore/pull/4590
[ac01]: https://github.com/python-attrs/attrs/issues/971#issuecomment-1159394251
[next]: NEXT_TASKS-20.json
