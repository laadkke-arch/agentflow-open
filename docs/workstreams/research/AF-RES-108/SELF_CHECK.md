# AF-RES-108 자가검산

| 질문 | 답 | 직접 연 근거 URL·위치 | 판단에 반하는 경우·어디서 찾아 무엇을 확인했나 | 미확인·결론을 바꿀 최소 추가 조사 |
| --- | --- | --- | --- | --- |
| Q1 | 정상·경계 8쌍 전부 모집했다. 한 값 편집 뒤 결과 또는 허용 범위가 달라진 쌍은 7개다. 16입력 중 8개가 원본이고 8개가 하류 편집이다. | [SQLite 릴리스 3.51.1](https://sqlite.org/changes.html#version_3_51_1) · [SQLite 공식 mirror 고정 시험](https://github.com/sqlite/sqlite/tree/a1de06a4c639a5d741b2b424e5dfea45eaa30e70/test) · [WPT cutoff 트리](https://github.com/web-platform-tests/wpt/tree/f1edffe3511493e684402fdfed42433e79374d55/css/css-flexbox) · [모집 원장](frame.csv) | 최초 후보에서만 고르도록 정렬했다. F4는 방향을 바꿔도 높이가 꽉 차 y=0이었다. F2 최초 후보는 한 항목뿐이어서 다음 파일을 썼다. [실행](runs.jsonl) | canonical SQLite Fossil 네 파일 직접 열람 미확인. [고정 SHA3 원장](evidence/upstream-oracles.json)에서 실제 artifact URL과 공식 mirror를 대조한다. |
| Q2 | 시작 페이지·질의 토큰·출력 단위를 먼저 기록했다. SQLite는 멀티셋·동점 순열을 허용했고 Flexbox는 상대 CSS px를 썼다. | [SQLite ORDER BY](https://sqlite.org/lang_select.html#orderby) · [CSSOM View rect](https://www.w3.org/TR/cssom-view/#dom-element-getboundingclientrect) · [선정과 마스킹](inputs/selection.json) | F2 탈락 후보의 data-offset과 F1 본문의 가운데 정렬이 먼저 보였다. 대체 가림 뒤에도 파일명과 문항의 허용 순서는 그대로였다. [노출](evidence/exposure.json) | 3.51.1 당시 문서 네 쪽이 미확인이다. [공식 ZIP](https://sqlite.org/2025/sqlite-doc-3510100.zip)과 당시 docsrc를 받아 원문 동일성 검사를 한다. |
| Q3 | K/E 파일 SHA, 후보 집합, 메타데이터 및 600+600 코드포인트가 16/16 정합한다. UTF-8은 19,376/19,342B이며 각각 32경계와 0이동이다. | [AF-RES-104 W2 원 규칙](https://github.com/laadkke-arch/agentflow-open/blob/f38c0af427c66876bf411bfd0a728cfcd60013eb/docs/workstreams/research/AF-RES-104/protocol.json) · [Flexbox 2025 CRD](https://www.w3.org/TR/2025/CRD-css-flexbox-1-20251014/) · [좌표](packets.jsonl) | 한글·수학 표시가 UTF-8 차이를 만들 수 있다. F1은 실제 구간까지 동일했다. 6개 단위시험에서 문장 끝, 리스트, 코드, 1자와 빈 입력, NFKC 원좌표를 확인했다. [영수증](evidence/selector-unit.txt) | 원시 HTML 매핑과 뷰별 실제 읽기 시간 미확인. 원시 HTML에서 같은 파서를 실행하고 후보 SHA 및 구간 내용 차이를 다시 기록한다. |
| Q4 | 사전 답 32개를 익명 ID 정렬로 썼다. 같은 작업자가 4회 나눠 봤고 봉인 후 원 기대·실행·방법 매핑을 열었다. | [사전 판독 봉인](https://github.com/laadkke-arch/agentflow-open/commit/58a05b8275a34189c4750a2341443a7dbdcaf3d2) · [노출과 좌표](evidence/exposure.json) | 공개 전에도 Ahem, 원문 이름, 세로/가로 조건을 알고 있었다. 같은 구간과 같은 입력을 여러 차례 보았다는 이력을 자리마다 계산했다. [사전 답](predictions.jsonl) | 독립 판독 미실시. 또 다른 실제 판독자에게 각 짝에서 한 방식만 무작위로 배정하면 기억 효과를 줄여 검증할 수 있다. |
| Q5 | SQLite 3.51.1 및 Chromium 156.0.8078.79로 32/32 성공했다. 두 번 모두 기대와 맞았다. WPT 원본 픽셀 2개와 하네스 30개가 원판에서 통과했다. | [SQLite CLI](https://sqlite.org/cli.html) · [WPT check-layout-th](https://github.com/web-platform-tests/wpt/blob/f1edffe3511493e684402fdfed42433e79374d55/resources/check-layout-th.js#L70-L87) · [원 기대](evidence/upstream-oracles.json) · [출력·stdout·stderr](runs.jsonl) | 변이 뒤 옛 assertion은 F2 한 개와 F3 두 개가 실패했다. offsetTop 3과 border-box 차 4는 border 1px로 설명된다. 파일 URL은 차단되어 SVG만 로컬 HTTP 응답으로 공급했다. [실행환경](evidence/engines.json) | Tcl 전체 suite와 다른 고정 CSS 엔진 미실시. 다른 엔진에서 WPT 원본과 1값 변이가 다른 rect를 내면 버전별 표를 만든다. |
| Q6 | 전체 오답/확정 K 0/8, E 0/8, 확정/적격 모두 8/16, 유보 각 8, 미실행 0. F2 정상 U→S, F4 정상 S→U. S3 두 조건에서 S→V다. | [비용·판정](metrics.json) · [SQLite 동점](https://sqlite.org/lang_select.html#orderby) · [Flexbox §5.1](https://www.w3.org/TR/2025/CRD-css-flexbox-1-20251014/#flex-direction-property) | K/E 사전 오답이 0이라 오답 방지 전환은 0이다. 부가 검사에서 covering index만 바꿔 S3 동점 순서를 뒤집었다. F4의 접근성 금지문이 정상 치수 절을 밀었고 S4의 비수치 조건은 양쪽에서 잘렸다. [대응](pairs.csv) · [반례](evidence/calibration.md) | 경계에서 잘못된 확신을 실제로 막는 빈도 미확인. 보조 반례를 사전 등록한 새 입력으로 바꾸고 독립 응답을 얻는다. |
| Q7 | 정답 수요에는 증거를, 유지보수에는 예외와 좌표 규칙을, 편집자에는 두 근거가 짧은 구간에 동시 수록되는지 제공한다. 표 3에 16개 반환 경로가 있다. | [The Open Group fnmatch](https://pubs.opengroup.org/onlinepubs/9699919799/functions/fnmatch.html) · [열람한 POSIX 재게시](https://man7.org/linux/man-pages/man3/fnmatch.3p.html) · [SVG 2 §13.4.2](https://www.w3.org/TR/2018/CR-SVG2-20181004/painting.html#FillRuleProperty) · [원 시험](https://www.w3.org/Graphics/SVG/Test/20110816/harness/htmlObject/painting-fill-03-t.html) | POSIX는 E에서 FNM_PATHNAME 결합 조건을 회복했다. 기본 모드는 양쪽 다 잘렸다. SVG는 evenodd parity와 표 초기값을 양쪽 다 놓쳤고 별 중심의 두 값은 브라우저에서 달랐다. [교정 출력](evidence/calibration.json) | Open Group과 Savannah 직접 판독이 미확인이다. 두 원본과 HTML 원좌표를 확보하고 표·목록 절대 조건을 포함한 대안을 다시 비교한다. |

## 표 대사

| 표 | 실제 행·분모 | 검산 범위 | 남은 미확인 |
| --- | --- | --- | --- |
| 1 시험·예산 | 8쌍 8행, 실험 모집 결원 0 | 4 Tcl 시험 저작, 4 WPT 시험 저작. 하류 편집 8개를 새 상류 사건으로 세지 않았다. 16/16에서 파일·문자·구간·후보·메타·이동 일치. [패킷](packets.jsonl) | 정식 3.51.1 문서 4쪽, 원시 HTML 맵 5쪽 |
| 2 사전 답·실측 | 32행, 사전 답 32. 16입력×2회 상태 0, 타임아웃 0 | 봉인 SHA, 판독 순번, 구간 안 인용 좌표·SHA, 실제 값·typeof·rect, 그림과 비교를 `adjudicate.py`로 대사했다. [예측](predictions.jsonl) · [실측](runs.jsonl) | 독립 판독 0, 전체 SQLite Tcl suite 미실시 |
| 3 대응·반환 | 16입력과 3합계 19행, 적격 16. 양쪽 오답 0/8, 확정 8/16. 확정 0인 행 오류율 산출 불가. | SQLite 확정 5/8씩, 오답 0/5씩, 유보 3씩. Flexbox 확정 3/8씩, 오답 0/3씩, 유보 5씩. 교정은 별도다. [대응 원장](pairs.csv) | 한 엔진씩, SQLite 실험 문서판의 과거 등가성 |

| 고유 1차 자료 층 | 산입 / 하한 | 제외 사유·범위 |
| --- | --- | --- |
| SQLite 시험 | 0/4 | 4개 시험 바이트를 공식 mirror에서 읽고 릴리스 Fossil SHA3로 검증했다. 직접 원본 URL은 실패한 채 남아 있었다. mirror와 후순위 2개는 산입 밖이다. |
| Flexbox 시험 | 4/4 | WPT 본 시험 저작 네 개. 동일 파일 안 assertion 반복은 한 저작이다. 후보 9개와 별개 참조 파일 2개는 전체 열람 수에만 들었다. |
| 설명/구현 원자료 SQLite / Flexbox | 4/4 · 4/4 | SQLite는 현재 원 사이트 원자료 네 개. 3.51.1 시대판은 미확인이다. Flexbox 한 TR의 여러 앵커와 검증 대시보드는 중복이다. |
| 셸·테스트 하네스·좌표 | 5/4 | SQLite CLI 및 typeof, CSSOM View, WPT check-layout-th 및 testharness. 역할이 다르고 별도 원자료다. |
| POSIX 규격·시험 / SVG 규격·시험 | 0/2 · 2/2 | Open Group과 Savannah 원본 실패, POSIX와 Gnulib의 mirror 제외. SVG CR과 W3C 시험은 2개, WPT import는 같은 시험의 중복이다. |
| 전체 열람과 필수 층 충족 | 36개 · 18/24 자리 | [출처 원장](sources.jsonl)에 49행과 산입 여부가 있다. 직접 열람 36개에는 후보·비교·판 확인 문서를 포함한다. 필수 층의 결원은 canonical SQLite 4개와 POSIX 2개다. |

자가검토는 한 사람이 맡았고 별도 판독자 자료는 0건이다. 이번 자료 묶음은 **PARTIAL**이다. 모집과 32회 실행은 종료했다. 별개의 핵심 미실시는 정식 SQLite 문서 복원·재선택과 원시 HTML 매핑, 직접 출처 층 채우기다. 재개 입력은 [재현 절차](reproduce.md)와 [접근 기록](evidence/access-notes.md)에 있다.
