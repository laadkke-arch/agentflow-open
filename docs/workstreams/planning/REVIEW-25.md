# REVIEW-25 · 같은 링크를 다시 줄지, 다른 링크를 붙일지 가르는 근거

Pillow에서는 RGB 값이 같은 검정 픽셀 199개가 변환 뒤에 불투명에서 투명으로 바뀌었다. Pandoc에서는 같은 그림을 표시하고도 HTML에서 검색할 수 있는 원래 문장이 두 개에서 0개가 됐다. 두 사례에서 링크를 고를 기준은 사용자가 결과로 **무엇을 읽거나 다음에 무엇을 할 수 있어야 하는가**였다. 반면 문서 파일을 하나 더 주거나 예제 경로를 찾았다는 사실만으로는 실제 사용, 새 빌드에서의 생성, 사용자의 재작업 절감을 판정하기 어려웠다. [Pillow 픽셀 원 출력][prom97] · [Pandoc 요소별 판독][elem99] · [발행판 원장][line98] · [질문자 후속][out100]

## 이번에 검토한 범위

2026-11-23 UTC. 계획 브랜치 `02cee43`의 최신 REVIEW-24를 먼저 읽었다. 이 문서가 사용한 통합 진행표 `fcde6be`와 이번 `ace1a06`의 tasks를 ID별로 대조했다. 등록 **94→98**, DONE **92→96**, BLOCKED **2→2**다. 기존 94행의 필드값이 모두 같고, 새 DONE은 **AF-RES-097~100** 네 건이다. AF-RES-018(범용 LLM 웹 검색과 같은 예산 비교)과 035(Go 추출·DLPack 호출 경계)는 계속 BLOCKED다. DONE 96행 모두 중앙 `acceptance_evidence`가 빈 배열이다. 아래 판단은 네 작업의 인계, 보고서, 해당 브랜치의 원장과 검사 기록에 근거한다. [직전 누적 검토][prev] · [이전 진행표][old] · [이번 진행표][reg]

| 작업 · 담당 | 중앙에 등록된 인계 | 연구 결과와 검사 대상 | 이번 검토가 받아들인 범위 |
| --- | --- | --- | --- |
| 097 · codex-cloud | [a4b5471][h97] | [f475e1a][r97] | 원 PNG·원 배열의 세 연구판에서 대체 가능 여부를 판정할 수 있다. 질문자의 당시 시스템과 두 사건 밖의 판별 성능은 미확인이다. |
| 098 · web-pro | [5022d58][h98] | [846aa7b][r98]에 검사 기록을 합쳤고 실제 검사는 [01fe105][check98]에서 수행했다. | 두 발행판의 파일 포함·본문 참조를 확인할 수 있다. 6개 예측에는 실제 음성이 없고 12자리 모두 당해 빌드의 신규 생성은 미확인이다. |
| 099 · codex-cloud | [8426e35][h99] | [01c7d0a][r99] | 원 TeX 한 건의 세 경로를 각각 두 번 실행했다. 산출물의 그림, 읽을 수 있는 본문, 추가 파일 필요 여부를 구별할 수 있다. |
| 100 · web-pro · 2차 시도 | [80e2d74][h100] | 등록 인계의 검사 대상 [b3f3694][r100], 이후 합류판의 검사 대상 [8b22a47][check100] | 고정 문서에 필수 근거가 있었는지 판정했다. 같은 표시량에서의 발견률과 실제 질문자 실행은 미확인이다. [현재 결과][head100] |

원격 끝이 등록 인계와 일치한 작업은 097~099다. 100의 원격 끝 `ab89ae6`은 등록 인계보다 세 커밋 앞이다. 같은 HANDOFF가 남은 채 RESULT와 출처 원장이 갱신됐으므로 두 판을 함께 읽었다. 검토자가 실행 원장·대응쌍의 행을 다시 세고 판정값을 비교했다. 바이너리 실행·브라우저 그림 판독·과거 사용자 행동은 각각 연구자의 관측이나 공개 후속 기록에 귀속했다. [100 변경 경로][diff100] · [097 실행 원장][run97] · [098 판별 원장][line98] · [099 실행 원장][run99] · [100 대응 원장][pair100]

## 설계자가 이어받을 누적 판단

목표는 사용자가 만들려는 소프트웨어의 전체 또는 일부 구조와 목적을 받아 재사용할 제품·기능·부품·타 분야 원리를 가리키는 링크를 돌려주는 것이다. 근거 묶음을 나중에 채택·폐기·조합할 수 있어야 한다. 입력 JSON, 필수 저장 필드, 크롤러, 검색 엔진, DB와 UI는 열린 설계 결정이다. 아래 과거 수치는 REVIEW-24의 누적 판정을 이어받았고, 오른쪽 열은 이번 원장에서 달라진 판단이다. [제품 연구 브리프][brief] · [연구 운영 규칙][workflow] · [직전 누적 검토][prev]

| 제품이 내려야 할 판단 | 096까지 확인한 것과 남았던 공백 | 097~100을 반영한 적용 조건 |
| --- | --- | --- |
| 부분 요청에 무엇을 더 물을까 | 020은 주장 72/73을 전달하고도 충돌은 2/16만 해소했다. 070의 자연 요청 24건에는 되물은 답이 정오를 바꾼 독립 분모가 없었다. 074의 구성 입력은 조건 하나로 8/8이 좁혀졌다. 093에서는 여섯 건 중 정답 1건만 있었고 P2의 RGBA 요구는 처음부터 명시됐다. | 097의 두 원 입력은 판과 보존값만으로 어느 호출을 줄지 좁혔다. 100-P1은 기존 호출을 바꿔도 되는지만 달리 읽으면 유일한 인접 자료 이득이 사라진다. 원문에 이미 있는 조건, 기존 시도, 답이 달라질 조건을 구분할 근거다. [097 반환표][r97] · [100 민감도][num100] |
| 타 분야 원리는 어떤 도움을 주었나 | 010은 분야 단서로 원리군 7개를 얻었다. 033의 단서 없는 144쌍에서 넓은 지지는 1, 당시판 지지는 0이었다. 069·073은 접수와 적용, 이전과 유지 책임을 갈랐다. 077 보조 3건의 핵심 구현 변경은 0이었다. 089의 다른 표시가 같은 두 음을 바꿨고 091은 위치가 같아도 원 Point 행 선택을 복구하지 못했다. | 097의 같은 RGB·다른 번호와 099의 같은 SVG·다른 호스트 문서 링크 동작은 실질적인 반증 시험을 제공한다. 099의 Graphviz 대조에서 화살촉을 없애도 방향쌍 제목은 남았다. 원 개발자가 이 선례를 보고 설계 선택을 바꿨는지는 별도 근거가 필요하다. [097 대조군][r97] · [099 분야 간 대조][r99] |
| 어느 정도의 설명과 비용을 감수할까 | 021의 똑같은 두 절 열람에서 공식 근거 회수는 주소만 6/23, 절 목록 9/23, 조건에 맞춘 절 14/23, 잘못 맞춘 절 8/23이었다. 066은 같은 링크가 반대 권고에도 달렸다. 022의 미인지→결정 변경→실행 확인은 0/24였고, 034의 한 부분 시간은 380→57초, 전체는 849→847초였다. 093은 필드 추가로 4,268→7,449바이트, 094는 목적을 엄격히 충족한 경로가 4/24였고, 12대응쌍 중 두 번째 주소가 양쪽에서 실제로 달랐던 쌍은 0이었다. | 어디를 읽고 무슨 값을 확인할지 설명할 이유는 있다. 100이 센 실제 표시 문자·절 이동·유효 인용과 099의 PDF 변환 횟수는 서로 다른 비용이다. 이들로 사람의 총시간이나 재작업 절약분을 환산할 수 없다. [100 비용·노출][num100] · [099 실행][run99] |
| 같은 주소·파일·호출을 하나의 결과로 묶을까 | 032의 배포 참조는 유지 9·교체 2·보류 1이었다. 055는 옛 답 4/4를 복원하고도 다음 판 답은 0/4였다. 071·075는 조건이나 양성 존재를 각각 22/22·15/15 복원했지만 양쪽 모두 1위 판정 16/16을 유보했다. 086의 당시 제공 주 관측창은 확인 0/9, 090의 후속 자원 엄격 충족은 0/8이었다. 094는 새 트리에 남은 옛 SVG 두 개가 현재 절에 연결되지 않음을 보였다. | 098은 실제로 쓰인 정적 옛 그림도 찾았다. 파일의 포함, 정확한 절의 참조, 이번 빌드 생성은 별도로 입증해야 한다. 097은 입력과 판이 바뀌면 같은 호출 쌍을 다시 나눠야 하는 양성·음성 사례를 제공한다. [098 예측과 판독][line98] · [097 판별표][num97] |
| 여러 부품을 잇거나 인접 자료를 찾는 편이 나을까 | 078은 두 기능 각각의 성공과 조합 성공이 갈림을 보였다. 076의 자연 요구 6×20후보에서 직접 양성은 0이었다. 080의 범위 확장으로 비교 가능한 양성 전환은 자연 1/5·교정 3/5였다. 088의 비교 가능 26쌍은 수정 전후 변화 0이고, 092는 순위 안 인접 원문 노출 0이었다. 096에서는 경계 6/6에 인접 원문이 노출돼도 단독 완결 0/6이었고, 전체 8쌍은 양쪽 완결 5·양쪽 미완결 3이었다. J2·J4에서 밀려난 파일에는 진단 근거가 있었다. 095의 연구판에서는 PDF 12/12·셀값 144/144를 확인했고 두 표에 같은 매크로를 적용한 4/4에서 뒤 표의 테두리도 사라졌다. | 099는 096-P4가 막혔던 변환을 고정 환경에서 끝까지 밟았다. 100에서는 인접 원문 단독 이득이 한 해석에서 한 쌍 생겼고 짧은 발췌에서는 양쪽 모두 미완결이었다. 발견, 노출, 문서 충분성, 조합 실행, 작성자 채택을 각각 셀 수 있다. [099 출력][elem99] · [100 대응쌍][pair100] · [100 후속][out100] |

## 새 작업별 근거와 불일치

### 097 · 같은 팔레트와 같은 출력은 판과 다음 호출에 달렸다

Pillow #5593의 원 PNG와 #5595의 원 배열을 공식 Linux wheel 8.2.0·8.3.0·8.3.1에서 매번 새로 열거나 생성했다. 2사건×3판×2호출×2반복의 24/24 출력을 얻었고 12/12 반복쌍의 관측값이 같았다. **두 호출이 모두 맞은 사건·판은 3/6, 한 호출만 맞은 곳도 3/6**이다. #5593은 8.2.0에서 두 호출 모두 RGBA와 원 alpha를 보존했다. 8.3.0·8.3.1의 기본 변환은 RGB 검정 키를 남겼다. 그 결과를 다시 RGBA로 바꾸면 투명 픽셀은 7,221→7,420개다. 원래 검정이던 불투명 199개가 추가로 투명해졌다. 원본에서 곧바로 명시 RGBA를 선택할 이유가 여기 있다. [입력 청크·번호][input97] · [실행][run97] · [재승격 출력][prom97]

#5595에서는 같은 index 1을 읽어도 8.2.0 객체 경로가 파랑, raw RGB 경로가 빨강이었다. 8.3.0·8.3.1에서는 새 객체에 붙인 두 경로 모두 원 배열·번호·빨강을 보존했다. 093의 같은 객체에 차례로 붙인 뒤 prefix만 본 근거보다 강하다. 단, #5593은 단일 투명 번호를 쓴 파일이고 #5595는 제시한 p에 관한 결과다. 공개 작성자의 raw 수용, 연구자의 CPython 3.9.23 재현, 질문자의 2021년 설치환경은 서로 다른 관측이다. 40개 직접 자료와 53개 보조 실행으로도 093 전체 여섯 요청에서 추가 필드가 오병합을 줄였는지는 판정할 수 없다. [목적·판별 분모][num97] · [097 인계][h97]

### 098 · 목록 예측의 여섯 성공에는 실패를 잡아낼 분모가 없다

Matplotlib 3.7.0→3.7.1, CPython 3.12.0→3.12.1, ggplot2 3.5.0→3.5.1의 목록 1,335경로에서 이전 판 예제 두 개씩을 골랐다. 다음 판 **목록만** 본 사용 예측 6개는 모두 양성이었고, 본문을 나중에 열자 여섯 절 모두 실제로 해당 그림을 썼다. 두 판 12/12에서 배포 포함과 본문 참조를 확인했으나 **그 빌드가 해당 바이트를 새로 만들었는지는 0/12 확인**이다. MP 두 쌍은 PNG 바이트가 달라도 픽셀이 같았고 GG 두 쌍은 픽셀도 달랐다. PY 두 쌍은 더 오래된 정적 그림과 같은 바이트를 현재 절이 계속 사용했다. [사전 예측][pred98] · [12자리 원장][line98] · [자료·분모][num98]

따라서 오래된 파일도 현재 독자에게 줄 수 있다. 반대 방향은 094 교정에서만 확인됐다. asciicast의 SVG 두 개는 새 파일 트리에 남았지만 옛 절의 참조 2개가 새 절에서 0개가 됐다. 098의 신규 표본에는 실제 사용 음성도, 검증된 ‘새 이름·같은 바이트’도 없다. 신규 음성 탐지율과 경로 변경 시 놓친 비율은 산출 불가다. 배포 실행 번호와 파일별 산출물 지문을 잇는 자료가 없어 생성 여부 역시 미확인이다. 102개 원자료와 마감 때의 HTML·PNG 24/24 재요청 성공은 이 두 공백을 채우지 않는다. [교정 감사][audit98] · [예제·발행 조사와 반례][r98] · [검사 대상과 범위][check98]

### 099 · 그림을 가진 파일과 나중에 쓸 수 있는 HTML의 차이

096-P4는 원 TeX의 raw TikZ를 읽었지만 TeX format이 없어 HTML 생성을 끝내지 못했다. 099는 원 TeX 한 개, Pandoc 3.6, 고정 diagram과 도구판에서 세 경로를 두 번씩 실행했다. A(질문자의 명령에 대응하는 연구판)는 본문 두 문장을 남겼으나 그림은 0/2였다. B(봉인 Lua)는 생성한 두 HTML 각각에서 상태 4/4, 방향과 라벨 8/8, 앞뒤 본문 DOM 문장 2/2가 맞았고 SVG가 내장됐다. C(공개 PDF→SVG 답)는 독립 SVG 둘에 그림과 페이지 글자 모양을 남겼다. 그 뒤 연구자가 만든 C+ 외부·내장 HTML에서는 각각 그림이 보였지만 본문 DOM은 문장 0/2였고, 외부 파일을 뺀 대조에서는 404가 났다. [원 실행][run99] · [그림·문장·링크 판독][elem99]

그림 원본만 재사용할 개발자, 페이지 외관을 보관할 독자, HTML에서 검색할 독자에게 돌아갈 링크가 달라진다. B는 환경을 준비하고 나서 성공했다. 첫 시도는 pdf2svg 부재로 멈췄고, 전역 색 AFControl을 추가한 입력에서는 전체 문서 PDF가 생성됐는데도 B의 그림별 컴파일은 실패했다. A/B의 HTML과 C의 SVG는 반복 바이트 3/3쌍 일치, 중간 PDF는 0/2쌍 일치다. 095의 PDF 바이트 0/6쌍·의미상 일치 6/6과 함께 보면 해시로 판정할 대상부터 정해야 한다. 단일 원본과 39개 직접 자료는 질문자 당시 버전, 모든 preamble, 여러 그림의 성공을 보장하지 않는다. [반복·산출물 지문][proof99] · [전역 정의 반례와 실행 한계][self99]

### 100 · 짧게 보여 준 효과와 어디를 잘라 보여 준 효과가 섞였다

신규 jq·Pandoc 요청 8건에 주 도구 파일 네 개(A) 또는 주 도구와 인접 도구 파일(B)을 배정했다. 경계 6건은 B의 뒤 두 자리를 바꿨고 대조 2건은 파일을 같게 뒀다. F는 파일 안에서 절 이동을 허용하고 S는 첫 일치 근처 최대 1,200자만 보여 줬다. 32자리에서 A/B 16쌍을 만들었다. P3는 질문 이전 안정판의 인접 소스가 비어 F·S 모두 비교불가다. 아래 숫자는 **제공한 자료로 필수조건을 모두 뒷받침했는가**를 센 것이다. [16쌍 원장][pair100] · [분모·민감도][num100]

| 읽기 조건 | 배정 / 비교 가능 A·B쌍 | A만 완결 | B만 완결 | 양쪽 완결 | 양쪽 미완결 | 비교불가 |
| --- | --- | --- | --- | --- | --- | --- |
| 파일 전체 F | 8 / 7 | 0 | 1 | 4 | 2 | 1 |
| 고정 발췌 S | 8 / 7 | 0 | 0 | 0 | 7 | 1 |

F의 완결 9/14 비교 가능 정책 자리가 S에서 모두 미완결이 됐다(다섯 요청). 양 조건 모두 64번의 파일 자리를 과금했지만 F의 실제 표시량은 270,609자·절 이동 102회, S는 74,400자·이동 0회였다. 32자리 중 24자리에서 독자가 다른 질문의 공유 파일을 이미 본 기록이 있다. 발췌 길이, 첫 일치 위치, 이동 비용 또는 사람의 독립 독해 효과 중 하나에 손실 아홉 건을 귀속할 수 없다. J2에서는 교체한 jq 원 시험을 잃어도 매뉴얼에 같은 연산의 근거가 남았다. J3에서는 Terminal 설정을 더해도 Bash에서 빠진 조건이 남았다. [교체 24자리][disp100] · [노출·비용][num100] · [사례별 원문][r100]

유일한 B 단독 완결인 P1은 기존 `knitr::include_graphics` 호출을 helper로 바꾸는 해석을 허용해야 한다. 기존 호출을 그대로 써야 한다면 B 단독은 0건이다. 최초 요청에는 Pandoc 태그가 없었으므로 최초 태그를 모집 기준으로 삼아 P1을 제외해도 0건이다. 더구나 질문자는 이미 helper를 쓰고 있다고 밝혔다. 문서가 답을 지지한 것과 사용자에게 새로운 방법을 알려 준 것이 이 지점에서 갈린다. 현재 채택 3/8, 당시 판·원 입력·필수 출력을 함께 확인한 작성자 실행은 0/8이다. [P1 의미와 모집 민감도][head100] · [공개 후속 원장][out100]

100의 두 작업 흐름을 합친 뒤 `pairs.csv`는 두 판에서 내용이 같고 입력 지문표에서도 `protocol.json`·`packets.jsonl`·`judgments.jsonl`·`pairs.csv`·`outcomes.csv`의 지문이 일치한다. `sources.jsonl` 총행은 **303→337**, 산입한 고유 자료는 **46→46**이다. 다른 집계 32개와 이 46개를 더할 수 없다. 합류 뒤 증거 보강과 새 판의 운영 검사는 같은 32자리의 새 독립 반복이 아니다. 097~100은 각 연구자가 특정 결과 SHA에서 개별 원격 검사 종료 0을 남겼다. 공통 검사의 활성 세션 0과 개별 검사의 실행을 구별해야 한다. 지난 회차 095·096의 개별 종료 1·2는 그대로 그 당시 결과에 귀속된다. [합류 결정][adopt100] · [등록판 지문][num100] · [후속판 지문][headnum100] · [추가 검사][check100] · [직전 검사 기록][prev]

## 다음 네 작업과 인수 관계

| ID · 담당 | 읽을 완료 입력 | 무엇을 비교해서 설계 판단을 바꾸는가 |
| --- | --- | --- |
| AF-RES-101 · web-pro | [097][h97] | 새 공개 요청 여덟 자리에서 이미 시도한 도구를 통째로 제외하는 방식과 실제 호출만 제외하는 방식을 비교한다. 알려진 방법의 재추천, 같은 도구 안의 유효한 변경, 질문자가 새로 알았다고 확인한 경우를 가른다. |
| AF-RES-102 · web-pro | [098][h98] | 예제 경로가 바뀌었거나 남았을 때 옛 링크와 새 링크 중 무엇을 줄지 검토한다. 이름·본문이 바뀐 층과 보통 층을 따로 모집해, 실제 음성과 새 이름으로 이어진 경우까지 수용하거나 결손을 기록한다. |
| AF-RES-103 · codex-cloud | [099][h99] | 원문·전역 색 대조·공개 다이어그램·범위 변형을 포함한 다섯 입력에서 세 변환 경로를 두 번씩 실행한다. 그림 조각만으로 되는 조건과 주변 정의가 필요한 조건을 실제 HTML·SVG·DOM으로 가른다. |
| AF-RES-104 · codex-cloud | [100의 고정 연구판][r100] 및 [원격 합류판][head100] | 후보 파일과 표시 문자 수를 같게 둔 32자리를 실행한다. 첫 일치 발췌와 두 구간 발췌 중 어느 쪽이 필수 근거와 반례를 살리는지 같은 질문에서 비교한다. |

101은 질문자가 이미 시도했다고 **말한** 조작을, 103은 주어진 입력·도구에서 **실제로 보존되는** 결과를 조사한다. 102는 배포된 판 간 자원 관계를 추적하고 104는 100의 이미 고정된 파일 안에서 절 선택만 바꾼다. 네 작업은 완료된 입력만 읽고 자기 경로에 쓸 수 있다. 여러 alpha 값의 Pillow 입력, 특정 과거 빌드의 신규 생성, 인접 자료가 바꾼 사람의 전체 작업시간은 계속 미확인이다. [작업별 질문·자료·판정표·인계 조건][next]

[prev]: https://github.com/laadkke-arch/agentflow-open/blob/02cee43b45f6e9273f11b58b322faa04d8ac1364/docs/workstreams/planning/REVIEW-24.md
[old]: https://github.com/laadkke-arch/agentflow-open/blob/fcde6becc49120c5be91adf43fb5b4aa42e71d48/docs/automation/dot-control.json
[reg]: https://github.com/laadkke-arch/agentflow-open/blob/ace1a06a13ea435f5cb6a3e340ad24f03f68ecae/docs/automation/dot-control.json
[brief]: https://github.com/laadkke-arch/agentflow-open/blob/ace1a06a13ea435f5cb6a3e340ad24f03f68ecae/docs/product/RESEARCH_BRIEF.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/ace1a06a13ea435f5cb6a3e340ad24f03f68ecae/docs/RESEARCH_WORKFLOW.md
[next]: NEXT_TASKS-25.json
[h97]: https://github.com/laadkke-arch/agentflow-open/blob/a4b5471c08dc369367645a9e78249b44f8143f05/docs/workstreams/research/AF-RES-097/HANDOFF.md
[r97]: https://github.com/laadkke-arch/agentflow-open/blob/f475e1a55c5be68cd6d9bcca1a7c7b4f9893e24c/docs/workstreams/research/AF-RES-097/RESULT.md
[h98]: https://github.com/laadkke-arch/agentflow-open/blob/5022d581d8d7a4a359250797d55c79f6b67d219c/docs/workstreams/research/AF-RES-098/HANDOFF.md
[r98]: https://github.com/laadkke-arch/agentflow-open/blob/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/RESULT.md
[h99]: https://github.com/laadkke-arch/agentflow-open/blob/8426e3511114fd36a00fc57bc270cfe3f5d573c8/docs/workstreams/research/AF-RES-099/HANDOFF.md
[r99]: https://github.com/laadkke-arch/agentflow-open/blob/01c7d0a40a20a35f98c11eb12c2ad28423cbdbd7/docs/workstreams/research/AF-RES-099/RESULT.md
[h100]: https://github.com/laadkke-arch/agentflow-open/blob/80e2d746d0aa0ad7c009043e1cea3ae2e3be1311/docs/workstreams/research/AF-RES-100/HANDOFF.md
[r100]: https://github.com/laadkke-arch/agentflow-open/blob/b3f3694b54bb7a85dc7a21e2731841679fc6753c/docs/workstreams/research/AF-RES-100/RESULT.md
[run97]: https://github.com/laadkke-arch/agentflow-open/blob/f475e1a55c5be68cd6d9bcca1a7c7b4f9893e24c/docs/workstreams/research/AF-RES-097/runs.jsonl
[num97]: https://github.com/laadkke-arch/agentflow-open/blob/f475e1a55c5be68cd6d9bcca1a7c7b4f9893e24c/docs/workstreams/research/AF-RES-097/evidence/reconciliation.json
[prom97]: https://github.com/laadkke-arch/agentflow-open/blob/f475e1a55c5be68cd6d9bcca1a7c7b4f9893e24c/docs/workstreams/research/AF-RES-097/evidence/experiment/promotion-5593-8.3.0-default-1.stdout.json
[input97]: https://github.com/laadkke-arch/agentflow-open/blob/f475e1a55c5be68cd6d9bcca1a7c7b4f9893e24c/docs/workstreams/research/AF-RES-097/inputs.json
[line98]: https://github.com/laadkke-arch/agentflow-open/blob/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/lineage.csv
[pred98]: https://github.com/laadkke-arch/agentflow-open/blob/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/predictions.csv
[num98]: https://github.com/laadkke-arch/agentflow-open/blob/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/evidence/counts.json
[audit98]: https://github.com/laadkke-arch/agentflow-open/blob/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/evidence/calibration/audit.json
[check98]: https://github.com/laadkke-arch/agentflow-open/blob/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/evidence/validation.json
[run99]: https://github.com/laadkke-arch/agentflow-open/blob/01c7d0a40a20a35f98c11eb12c2ad28423cbdbd7/docs/workstreams/research/AF-RES-099/runs.jsonl
[elem99]: https://github.com/laadkke-arch/agentflow-open/blob/01c7d0a40a20a35f98c11eb12c2ad28423cbdbd7/docs/workstreams/research/AF-RES-099/evidence/ELEMENTS.md
[proof99]: https://github.com/laadkke-arch/agentflow-open/blob/01c7d0a40a20a35f98c11eb12c2ad28423cbdbd7/docs/workstreams/research/AF-RES-099/evidence/verification.json
[self99]: https://github.com/laadkke-arch/agentflow-open/blob/01c7d0a40a20a35f98c11eb12c2ad28423cbdbd7/docs/workstreams/research/AF-RES-099/SELF_CHECK.md
[pair100]: https://github.com/laadkke-arch/agentflow-open/blob/b3f3694b54bb7a85dc7a21e2731841679fc6753c/docs/workstreams/research/AF-RES-100/pairs.csv
[num100]: https://github.com/laadkke-arch/agentflow-open/blob/b3f3694b54bb7a85dc7a21e2731841679fc6753c/docs/workstreams/research/AF-RES-100/evidence/derived/metrics.json
[out100]: https://github.com/laadkke-arch/agentflow-open/blob/b3f3694b54bb7a85dc7a21e2731841679fc6753c/docs/workstreams/research/AF-RES-100/outcomes.csv
[disp100]: https://github.com/laadkke-arch/agentflow-open/blob/b3f3694b54bb7a85dc7a21e2731841679fc6753c/docs/workstreams/research/AF-RES-100/displacement.csv
[diff100]: https://github.com/laadkke-arch/agentflow-open/compare/80e2d746d0aa0ad7c009043e1cea3ae2e3be1311...ab89ae6704471aaea96d175103839bc6356d389a
[adopt100]: https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/evidence/canonical-adoption.json
[head100]: https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/RESULT.md
[headnum100]: https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/evidence/derived/metrics.json
[check100]: https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/evidence/result-checks.json
