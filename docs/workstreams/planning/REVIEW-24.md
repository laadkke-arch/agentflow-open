# REVIEW-24 · 링크를 따라가면 사용자가 원하는 결과까지 얻는가

Quarto에서는 PDF의 지문이 매번 달라도 같은 선이 사라지고 같은 셀 값이 남았다. 반대로 Pandoc은 그림을 담은 입력을 읽고도 HTML에 그림을 만들기 전에 멈췄다. 소프트웨어의 일부를 재사용하려는 사람에게 링크를 추천할 때는 **무슨 값이 어디까지 보존돼야 하는가**를 먼저 적을 수 있다. 이번 검토에서 그 값을 직접 판독한 범위와, 여전히 자료나 비교 상대가 부족한 범위는 다음과 같다. [Quarto 출력 원장][runs95] · [Pandoc 실행 영수증][p96]

## 검토 범위와 근거

2026-11-23 UTC, `work/planning@eda57bb`의 최신 REVIEW-23을 기준으로 삼았다. 그 검토의 통합 진행표 `e2a80af`와 이번 `fcde6be`를 ID와 행 전체 값으로 대조했다. 등록 **90→94**, DONE **88→92**, BLOCKED **2→2**다. 기존 90행은 모두 동일했다. 새 DONE은 AF-RES-093~096 네 건이다. AF-RES-018(범용 LLM 웹 검색과의 동등 예산 비교)과 035(Go 추출·DLPack 실행)는 계속 BLOCKED다. DONE 92행 모두 중앙 `acceptance_evidence`가 비어 있다. 연구 결과의 판정은 각 인계와 근거 파일에서 확인했다. [직전 검토][prev] · [이전 진행표][old] · [이번 진행표][reg]

| 새 DONE · 담당 | 등록된 마지막 인계 / 검사한 결과판 | 이 검토에서 대조한 자료 | 수용 범위 |
| --- | --- | --- | --- |
| 093 · web-pro | [ca82b93][h93] / [4b1233e][r93] | 12개 사전 판정, 후보·정답 공석, 요청별 바이트와 사후 판정 사유 | **PARTIAL**. 여섯 요청 중 한 건에서 제한된 팔레트 판독값 비교 가능 |
| 094 · codex-cloud | [b09dd21][h94] / [082ba3b][r94] | 24개 경로, 12개 대응쌍의 두 번째 주소, 두 SVG의 변경 이력과 문서 참조 | **PARTIAL**. 해당 환경의 열람과 역사판의 자원 관계를 확인 |
| 095 · codex-cloud | [b7f6db6][h95] / [55eb703][r95] | 12회 실행의 종료값·PDF·표별 셀과 선, 추가 토큰·그룹 대조, 개별 계약 검사 | **연구 COMPLETE, 개별 원격 검사 종료 1**. Quarto 1.4.553 연구판의 출력으로 한정 |
| 096 · web-pro | [fce8d0d][h96] / [1d399f6][r96] | 사전 8쌍, 16경로 노출 원장, 밀려난 파일, 사후 민감도·원 실행 실패, 계약 시작 기록 | **PARTIAL, 개별 원격 검사 종료 2**. 제공한 문서에서의 완결과 일부 보조 실행까지 |

네 작업 모두 확인 시점에 등록 `result_commit`이 해당 작업 브랜치 끝과 같았고 마지막 커밋은 자기 HANDOFF.md 하나를 추가했다. 094는 결과판과 인계 사이에 검사 영수증 커밋 `eef4c89`가 하나 있다. 이번 검토는 고정 원장에서 수치를 다시 세고 인계와 결과의 주장을 대조했다. 응용프로그램 실행, 당시 사용자 행동, 과거 사이트 응답은 각 작업자가 남긴 관측에 귀속한다. [093 판정 원장][j93] · [094 대응 원장][pairs94] · [095 실행 원장][runs95] · [096 대응 원장][pairs96]

## 앞선 판단을 포함한 제품 연구의 흐름

사용자는 만들려는 소프트웨어의 전체 또는 일부 구조와 목적을 주고, 비슷한 제품뿐 아니라 가져다 쓸 기능·부품·다른 분야의 원리를 가리키는 링크를 원한다. 나중의 설계자가 조건에 따라 근거 묶음을 버리거나 합친다. 입력 JSON, 링크 보관 필드, 크롤러, DB, 검색 엔진, 화면과 최종 설계는 미결정이다. [제품 연구 브리프][brief] · [연구 운영 규칙][workflow]

| 설계자의 질문 | 092까지의 핵심 근거 | 이번 자료까지 반영해 권할 수 있는 범위 |
| --- | --- | --- |
| 부분 요청에서 어떤 문맥을 더 받을까 | 020은 주장 72/73을 전달했어도 충돌 해소는 2/16이었다. 070의 자연 요청 24개에는 추가 답변이 정오를 바꾼 독립 분모가 없었다. 074의 구성 대조에서는 조건을 주자 8/8이 한 답으로 좁혀졌다. 082에는 옛 Python 조건이 이미 있었고, 088 JN1은 전체 JSON을 더해도 map 링크가 유지됐다. | 원문이 이미 말한 값, 비어 있는 값, 답에 따라 바뀌는 링크를 적는다. 093 I2에는 기존 path ID를 지켜야 하는지 물을 이유가 있다. P2는 RGBA가 이미 명시됐다. 096 P3는 ‘옵션’이 필수인지만 달리 읽어도 완결 수가 달라졌다. [누적 검토][prev] · [093 반환 카드][c93] · [096 민감도][s96] |
| 다른 분야에서 빌린 원리가 설계를 바꾸나 | 010은 분야 단서로 원리군 7개를 얻었다. 033의 단서 없는 144쌍은 넓은 의미 지지 1, 당시판 지지 0이었다. 069·073은 접수와 적용, 이전과 유지 책임 인수를 갈랐다. 077 보조 3건에서 핵심 구현 선택 변경은 0이었다. 081·085·089는 선택색과 실제 편집 대상을 가를 입력을 찾았다. | 타 분야 원리를 실패를 드러낼 시험과 보존값으로 쓸 수 있다. 089의 다른 표시가 실제로는 같은 두 음에 작용한 결과, 091의 같은 파일에서 원 Point 행을 되찾을 수 없던 결과가 양방향 대조다. 095의 CSS 선택 범위·Calc 인쇄 스타일도 두 번째 표에 미칠 변경을 점검하는 데 썼다. 원 개발자가 이 선례를 보고 결정을 바꿨는지는 미확인이다. [누적 검토][prev] · [095 분야 간 대조][r95] |
| 링크에 얼마나 설명을 붙이고 비용을 어떻게 잴까 | 021에서 같은 두 절을 열 때 공식 근거 회수는 주소만 6/23, 절 목록 9/23, 조건에 맞춘 절 14/23, 잘못 맞춘 절 8/23이었다. 066은 같은 주소가 반대 권고에도 붙었다. 022의 미인지→결정 변경→실행을 모두 확인한 사건은 0/24, 034의 부분 시간은 380→57초이나 전체는 849→847초였다. 078은 각각 되는 두 기능의 조합이 실패할 수 있음을 보였다. | 볼 곳과 다음 조작을 짧게 설명할 근거는 있다. 093의 추가 바이트, 094의 두 번 열람, 096의 완결 점수는 서로 다른 비용·결과다. 현재 자료로 사람의 전체 재작업이나 절약 시간을 산출할 수 없다. [누적 검토][prev] · [093 비용][m93] · [094 열람][num94] |
| 어떤 판·자료·호출을 같은 링크로 묶을까 | 032의 배포 참조 12건은 유지 9·교체 2·보류 1, 055는 과거 답 4/4·다음 판 0/4였다. 071·075는 조건/양성 존재를 각각 22/22·15/15 복구해도 1위 판정 각 16/16을 보류했다. 079·083·087은 GDAL/PyArrow 경로와 WKB/native reader를 구분했고 091은 혼형 native 쓰기 3회 거절과 원 타입 소실을 확인했다. 086의 당시 제공 주 관측창은 0/9 확인, 090은 본문 목적 3/8·후속 엄격 충족 0/8이었다. | 판·입력·호출·소비자가 읽을 값을 고정한다. 같은 배포 트리에 있는 파일을 해당 절의 생성물로 소개하려면 본문 참조와 발행 근거가 필요하다. 팔레트 prefix, PDF의 의미상 일치, 실행 가능성에는 각각 다른 증거를 붙인다. [누적 검토][prev] · [SVG 파일 계보][line94] · [PDF 판독][num95] |
| 목록이나 인접 도구 검색을 넓힐까 | 060·064·068은 한 조건의 원 절을 찾아도 두 조건 공동 근거가 비었다. 076의 자연 6요구×20후보 직접 양성은 0이었다. 080 범위 확장의 비교 가능한 양성 전환은 자연 1/5·교정 3/5, 084의 고른 4건은 확보본에서 양성 3·기본 조합 반박 1이었다. 088의 비교 가능 26쌍은 개정 전후 변화 0이고 채택 주 해법 3건은 좁은 후보 밖이었다. 092의 엄격 5쌍은 양쪽 2·모두 미완결 3이었으나 순위에 노출된 인접 원문은 0이었다. | 인접 자료 허용→실제 노출→열람→반환→요구를 충족하는 근거→실행을 따로 센다. 096에서 실노출을 확보해도 단독 완결은 없었고, 밀려난 파일이 설명하던 빌드 제한이 빠졌다. 파일에 허용한 읽기 범위와 누락되는 근거가 선택을 바꿀 수 있다. [누적 검토][prev] · [096 노출][ex96] · [밀려난 근거][disp96] |

## 새 결과가 결론을 지지하거나 제한하는 지점

### 093 · 추가 필드의 이득을 채점할 정답이 부족하다

Inkscape·Pillow 각각 30사건의 모집틀에서 첫 적격 3개씩을 골랐다. 후보 쌍은 5/6이고 원 입력·판·관측 목적에서 판정을 대조할 정답은 1/6이다. A(기존 기록)는 분리 2·유보 4, B(다음 조작·참조 대상·보존값 추가)는 분리 2·묶음 1·유보 3이다. 바뀐 한 건은 Pillow #5595다. 8.3.0에서 같은 p를 한 이미지에 차례로 붙였을 때 두 호출의 팔레트 앞부분이 p와 같았고, 작성자가 raw 경로를 수용했다. **오병합을 채점할 분리 정답은 A·B 모두 0개**다. 불필요한 분리도 A는 0/0, B는 0/1이다. [12개 판단][j93] · [사후 근거 검토][a93] · [분모 검산][m93]

#5593의 수정 후 hopper 시험과 #2225의 stamp 실패 영상에는 원판의 두 경로를 같은 입력에 쓴 결과가 없다. I3은 두 번째 후보가 비었고 후대 수정 문장이 사전 노출됐다. 여섯 건 모두 최초 작성판을 완전히 복원하지 못했다. #5595는 A에서 이미 읽은 ‘새 순서 선호’를 B에서 재해석하기도 했다. 그러므로 유보 한 건 감소를 필드의 인과 효과로 측정할 수 없다. 추가 필드 36자리 중 25개에 텍스트가 있었고 같은 여섯 payload는 4,268→7,449바이트(+74.5%)였다. 직접 1차 자료 49개와 직접 연 이슈 사건 9개 중 어떤 것도 나머지 다섯 정답을 대신하지 못한다. [093 결과와 모집 한계][r93] · [분모·비용 원장][m93]

### 094 · 추가 주소를 적은 것과 서로 다른 목적지에 간 것이 갈렸다

6목적×2카드×2접근 수단=24경로에서 34번 문서를 요청했다. 본문 판독 8/24, 필요한 후속 payload 판독 4/16, 목적을 엄격히 충족한 경로 4/24, 최종 접근 실패 20/24였다. 충족 네 경로는 모두 bandersnatch 7.0.1 예제와 **현재** PyPI 홈페이지 조합이다. 예제 URI를 읽은 A와 명시 링크를 받은 B 모두 두 번 만에 도착했다. 당시의 PyPI 서비스라는 귀속은 0/4 확인이다. 12쌍 중 B에 주소가 추가된 쌍은 6개지만 실제 두 번째 주소는 양쪽 같음 4, 한쪽만 요청 2, 양쪽 미요청 6, 양쪽 서로 다름 0이었다. ‘다른 두 번째 주소가 주는 이득’의 분모는 0이다. [경로별 영수증][routes94] · [대응쌍][pairs94] · [목적별 분모][num94]

cibuildwheel·asciicast 공개 입구와 R 도움말 접근에서 프록시 CONNECT 403 또는 브라우저 터널 실패가 났다. 발행 서버의 삭제·장애로 귀속할 근거가 없다. 090의 503과 이번 고정 blob의 200에는 관측 시점과 수단 차이가 있다. 별도 파일 대조는 판 귀속을 바꾼다. asciicast 2.3.1 배포 트리에 남은 두 SVG는 2022년 옛 파일과 바이트가 같고 1.0.0.9000 본문의 img src로 연결된다. 2.3.1 해당 절은 이 두 파일을 참조하지 않았다. EPUB 표지는 한 번 내려받은 패키지 안에서 실제 읽혔고, IIIF 그림은 manifest에 보였지만 원 JPEG를 받지 못했다. 43개 1차 자료·17개 계보로 이 관계들을 확인했어도 독자 클릭·시간과 정상 연결 환경에서의 카드 효과는 미확인이다. [옛판·새판 자원 대조][line94] · [payload 감사][payload94] · [094 인계][h94]

### 095 · 두 매크로의 동률은 원 표의 다음 토큰에 달려 있다

Quarto 1.4.553·실제 번들 Pandoc 3.1.11·XeTeX에서 원본/무인수/두 인수 정의×한 표/두 표×두 번을 실행했다. 실제 PDF 12/12, 판독된 표 18/18, 셀값·순서 144/144, 의미상 반복 일치 6/6이었다. 반복 PDF의 바이트 지문 일치는 0/6이었다. 수정 8/8은 목적 표의 위·아래 선을 지웠지만, 두 표 문서에 공통 적용한 4/4는 뒤 표의 바깥선도 지웠다. 뒤 표의 내부선은 남았다. 첫 표만 그룹으로 감싼 별도 두 실행에서는 뒤 표의 세 선이 보존됐다. 따라서 링크의 적합성은 **한 표만 고칠지 문서 전체에 적용할지**에 따라 갈린다. [실행별 선·셀][runs95] · [반복·지문·분모][num95] · [추가 대조][probe95]

원 표에서는 규칙 명령 뒤에 빈 `\noalign{}`이 있어 두 정의의 실측이 4/4 대응쌍에서 같았다. raw tabular에서는 두 인수 정의가 `Stable`을 `able`로 잘랐고, 마지막 명령 다음에 표 종료가 오자 TeX 종료 1과 PDF 미생성이 관측됐다. 092의 P2에서 비었던 생성 TeX와 PDF는 **고정 연구판**에서 채워졌다. 원 질문자의 도구판·답 적용 PDF, 다중 페이지 표·다른 템플릿까지의 성공은 미확인이다. 40개 1차 자료·17개 계보 수와 연구판 반복 수는 질문자 실행률의 분모가 아니다. [프로브 원 출력][probe95] · [095 결과][r95]

### 096 · 인접 원문이 보이고 쓰여도 단독 완결과 설명 손실은 다르다

새 jq·Pandoc 질문 ID 8개에서 네 파일씩 읽은 16경로의 사전 판정은 A만 0, B만 0, 양쪽 5, 모두 미완결 3, 비교불가 0이다. 경계 6쌍에서 B의 인접 원문은 6/6 실제 노출·열람, 3/6 최종 반환, 단독 완결 0/6이다. 092의 ‘순위 노출 0’이라는 결손은 채워졌다. 하지만 32검색·64파일 접근에 같은 파일 내 절 이동이 194회 있었고, 같은 담당자가 양 경로를 읽은 뒤 공통 기준을 조정했다. P3·P4의 일부 ‘부분/반박’이 이 단계에서 ‘완결’로 바뀌었다. 따라서 이 건수는 사전 규칙 아래의 문서 판단이다. 불일치쌍 안의 승률은 0/0으로 산출할 수 없다. [사전 8쌍][pairs96] · [접근·절 이동][ex96] · [평가 변경 기록][r96]

B가 밀어낸 주 도구 12자리 중 J2의 누락 필드 원 시험과 J4의 Oniguruma 없는 빌드가 실패한다는 근거가 반환에서 빠졌다. J2는 질문자가 긍정적으로 응답했지만 원 입력에 없는 offset까지 입증되지는 않았다. 096-P3의 ‘Pandoc 옵션으로만’이라는 해석에서는 양쪽 완결 4/8·모두 미완결 4/8이다. 096-P4는 원 TeX를 읽어 RawBlock 2개·TikZ 1개를 얻었고, 실제 HTML 생성은 `pdflatex.fmt` 부재에서 실패했다. 현재 채택 표지는 4/8, 30일 안의 질문자 후속은 5/8, 입력·판·명령·결과가 모두 연결된 질문자 실행은 0/8이다. 46개 직접 원자료를 열었고, P3는 재게시라고 밝혀 서로 다른 질문 ID 8개를 독립 사용자 8명으로 환산할 수 없다. [밀려난 두 근거][disp96] · [P3 사후 민감도][s96] · [P4 실행][p96] · [공개 후속][out96]

### 095·096의 원격 계약에서 실제로 어긋난 것

직전 REVIEW는 검토 시점의 092 인계 끝을 `e0d7ecd`로 기록했다. 이번에는 두 작업의 개별 검사 결과를 설명하기 위해 092의 **원격 ref와 변경 경로만** 추가 대조했다. 현재 끝 `e742bc6`은 네 커밋 앞이고 RESULT·outcomes·인계·검사 기록 등에 변경이 있다. 두 끝의 차이에 `evidence/next-inputs/` 변경은 없다. 095는 지정된 고정 결과판의 Qmd를 사용했다. 고정 입력으로 결과를 재현하는 것과 현재 브랜치 끝을 요구하는 운영 검사는 서로 다른 질문이다. [092 두 끝의 변경][diff92] · [095 입력·계약 영수증][contract95]

095의 개별 원격 `check --fetch`는 의존 변경으로 종료 1이고 고정 로컬 검사만 종료 0이다. 096은 시작 시 같은 의존 변경으로 계약 발급이 실패해 그 실패 기록을 남겼다. 이 파일의 개별 검사 종료 2 사유는 `unsupported task manifest`다. 양쪽 공통 검사는 종료 0이었으나 자동 세션 검사의 활성 건수는 0이었다. 중앙 DONE과 이 두 개별 검사의 차이는 남아 있다. 운영 담당은 092의 의존 변경 범위와 새 계약에 쓸 원격 SHA를 확인하고, 과거 연구 근거는 고정된 결과 SHA로 재열람할 수 있다. [095 검사][h95] · [096 시작 기록][contract96] · [096 검사][h96]

## 다음 독립 배정

| ID · 담당 | 인수할 완료 작업 | 질문과 완료 시 생기는 판단 |
| --- | --- | --- |
| AF-RES-097 · codex-cloud | [093][h93] | Pillow #5593·#5595에서 세 판·두 호출·두 반복의 24자리를 채운다. 모드·투명도 또는 팔레트 배열을 지키는 목적별로 대표 링크 하나를 줄 수 있는 판을 가른다. |
| AF-RES-098 · web-pro | [094][h94] | 세 프로젝트의 여섯 새 예제에서 이전·다음 판을 대조한다. 트리에 남은 파일, 현재 절이 참조하는 파일, 해당 빌드의 생성물 중 어느 주장에 근거가 있는지 판별한다. |
| AF-RES-099 · codex-cloud | [096][h96]의 고정 P4, [095][h95]의 출력 판독 방법 | 같은 TeX에서 세 경로를 두 번씩 실행한다. 실제 HTML 속의 그림·라벨·간선과 앞뒤 본문을 기준으로 원 입력 경로·봉인 Lua·공개 PDF→SVG 답이 각각 충족하는 목적을 가른다. |
| AF-RES-100 · web-pro | [096][h96]의 모집·예산 원장 | 새 여덟 질문에서 주 도구만/인접 포함과 파일 전체/제한된 발췌를 교차한다. 32자리에서 어떤 필수 근거가 추가되거나 밀려났는지와 어느 쪽만 완결했는지 판별한다. |

099는 알려진 한 사례의 **실행**을, 100은 그 사례를 제외한 새 요청의 **발견**을 다룬다. 097과 098의 입력·판정·쓰기 경로도 독립이다. 두 번째 URL의 독자 편의, Inkscape 원판의 양경로 편집, Quarto 다중 페이지의 표 격리와 실제 재작업 절감은 열린 질문으로 남긴다. 작업별 고정 입력·자료 최소량·표·중간 커밋·인계 조건은 각 brief 하나로 실행할 수 있게 지정했다. [다음 작업 4건](NEXT_TASKS-24.json)

[prev]: https://github.com/laadkke-arch/agentflow-open/blob/eda57bba6fbe7a0af8a794e7a29564ed3a528e3b/docs/workstreams/planning/REVIEW-23.md
[old]: https://github.com/laadkke-arch/agentflow-open/blob/e2a80afec762b10ee7979136c6332473c70905bb/docs/automation/dot-control.json
[reg]: https://github.com/laadkke-arch/agentflow-open/blob/fcde6becc49120c5be91adf43fb5b4aa42e71d48/docs/automation/dot-control.json
[brief]: https://github.com/laadkke-arch/agentflow-open/blob/fcde6becc49120c5be91adf43fb5b4aa42e71d48/docs/product/RESEARCH_BRIEF.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/fcde6becc49120c5be91adf43fb5b4aa42e71d48/docs/RESEARCH_WORKFLOW.md
[h93]: https://github.com/laadkke-arch/agentflow-open/blob/ca82b938e429779d73d9de134ddac93e462ff03d/docs/workstreams/research/AF-RES-093/HANDOFF.md
[r93]: https://github.com/laadkke-arch/agentflow-open/blob/4b1233ead75c0a701b497226b446794eedea3ceb/docs/workstreams/research/AF-RES-093/RESULT.md
[h94]: https://github.com/laadkke-arch/agentflow-open/blob/b09dd21acb2bf9160a5aca5b1075ad6179743e63/docs/workstreams/research/AF-RES-094/HANDOFF.md
[r94]: https://github.com/laadkke-arch/agentflow-open/blob/082ba3b787edd92d804bf617397743e89d75c5f0/docs/workstreams/research/AF-RES-094/RESULT.md
[h95]: https://github.com/laadkke-arch/agentflow-open/blob/b7f6db6f3e0dbbaa27ea3fbfb70cd6a629e23455/docs/workstreams/research/AF-RES-095/HANDOFF.md
[r95]: https://github.com/laadkke-arch/agentflow-open/blob/55eb703075163a84b38fdc7eb577f66207e9980e/docs/workstreams/research/AF-RES-095/RESULT.md
[h96]: https://github.com/laadkke-arch/agentflow-open/blob/fce8d0ded93fe1f13f2c4978ed273c1ceef32934/docs/workstreams/research/AF-RES-096/HANDOFF.md
[r96]: https://github.com/laadkke-arch/agentflow-open/blob/1d399f630930d2763459e16509c5224b0cded9a0/docs/workstreams/research/AF-RES-096/RESULT.md
[j93]: https://github.com/laadkke-arch/agentflow-open/blob/4b1233ead75c0a701b497226b446794eedea3ceb/docs/workstreams/research/AF-RES-093/judgments.csv
[m93]: https://github.com/laadkke-arch/agentflow-open/blob/4b1233ead75c0a701b497226b446794eedea3ceb/docs/workstreams/research/AF-RES-093/evidence/reconciliation.json
[a93]: https://github.com/laadkke-arch/agentflow-open/blob/4b1233ead75c0a701b497226b446794eedea3ceb/docs/workstreams/research/AF-RES-093/evidence/adjudication/ADJUDICATION.md
[c93]: https://github.com/laadkke-arch/agentflow-open/blob/4b1233ead75c0a701b497226b446794eedea3ceb/docs/workstreams/research/AF-RES-093/cards.md
[routes94]: https://github.com/laadkke-arch/agentflow-open/blob/082ba3b787edd92d804bf617397743e89d75c5f0/docs/workstreams/research/AF-RES-094/traversals.jsonl
[pairs94]: https://github.com/laadkke-arch/agentflow-open/blob/082ba3b787edd92d804bf617397743e89d75c5f0/docs/workstreams/research/AF-RES-094/pairs.csv
[num94]: https://github.com/laadkke-arch/agentflow-open/blob/082ba3b787edd92d804bf617397743e89d75c5f0/docs/workstreams/research/AF-RES-094/evidence/counts.json
[line94]: https://github.com/laadkke-arch/agentflow-open/blob/082ba3b787edd92d804bf617397743e89d75c5f0/docs/workstreams/research/AF-RES-094/evidence/r2-asset-lineage.json
[payload94]: https://github.com/laadkke-arch/agentflow-open/blob/082ba3b787edd92d804bf617397743e89d75c5f0/docs/workstreams/research/AF-RES-094/evidence/payload-audit.json
[runs95]: https://github.com/laadkke-arch/agentflow-open/blob/55eb703075163a84b38fdc7eb577f66207e9980e/docs/workstreams/research/AF-RES-095/runs.jsonl
[num95]: https://github.com/laadkke-arch/agentflow-open/blob/55eb703075163a84b38fdc7eb577f66207e9980e/docs/workstreams/research/AF-RES-095/metrics.json
[probe95]: https://github.com/laadkke-arch/agentflow-open/blob/55eb703075163a84b38fdc7eb577f66207e9980e/docs/workstreams/research/AF-RES-095/evidence/probes/probes.jsonl
[contract95]: https://github.com/laadkke-arch/agentflow-open/blob/55eb703075163a84b38fdc7eb577f66207e9980e/docs/workstreams/research/AF-RES-095/evidence/intake/contract.md
[pairs96]: https://github.com/laadkke-arch/agentflow-open/blob/1d399f630930d2763459e16509c5224b0cded9a0/docs/workstreams/research/AF-RES-096/pairs.csv
[ex96]: https://github.com/laadkke-arch/agentflow-open/blob/1d399f630930d2763459e16509c5224b0cded9a0/docs/workstreams/research/AF-RES-096/exposure.jsonl
[disp96]: https://github.com/laadkke-arch/agentflow-open/blob/1d399f630930d2763459e16509c5224b0cded9a0/docs/workstreams/research/AF-RES-096/evidence/audit/displacement-audit.md
[out96]: https://github.com/laadkke-arch/agentflow-open/blob/1d399f630930d2763459e16509c5224b0cded9a0/docs/workstreams/research/AF-RES-096/outcomes.csv
[p96]: https://github.com/laadkke-arch/agentflow-open/blob/1d399f630930d2763459e16509c5224b0cded9a0/docs/workstreams/research/AF-RES-096/evidence/post-pandoc/execution.json
[s96]: https://github.com/laadkke-arch/agentflow-open/blob/1d399f630930d2763459e16509c5224b0cded9a0/docs/workstreams/research/AF-RES-096/evidence/post-evaluation-sensitivity.json
[contract96]: https://github.com/laadkke-arch/agentflow-open/blob/1d399f630930d2763459e16509c5224b0cded9a0/docs/workstreams/research/AF-RES-096/manifest.json
[diff92]: https://github.com/laadkke-arch/agentflow-open/compare/e0d7ecda64bab2bd5d5779a9fb2a18d39a83bcdf...e742bc665efde0d3883ec4d0f5479e03e914fcbf
