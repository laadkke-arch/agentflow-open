# AF-RES-123 실행 계약

2026-11-24 UTC, 1차, Codex Cloud Linux. 저장소 `laadkke-arch/agentflow-open`, 작업 브랜치 `work/research-af-res-123`, 소유 경로 `docs/workstreams/research/AF-RES-123/`. 계획판 `13be736df17a4c697880f57029d16de38db061dd` 이후 PLAN#30 가져오기와 Codex·웹 배정 세 커밋의 경로 diff는 `docs/automation/dot-control.json` +92줄이다. 실제 시작판은 원격에서 확인한 `3215fdb429e307175b2f277a9a167d2d07361883`다. 이 판의 AGENTS, STATE, RESEARCH_BRIEF, RESEARCH_WORKFLOW, DOT_AUTOMATION과 진행표의 AF-RES-123 및 선행 행을 읽었다. 관리 사본의 로컬 브랜치 `work`와 새 브랜치의 이름이 충돌했다. 시도 중 바뀐 index가 시작판과 정확히 같은 것을 확인한 뒤 원 checkout을 깨끗하게 복원하고 GitHub에서 새로 clone했다. [시작판](https://github.com/laadkke-arch/agentflow-open/commit/3215fdb429e307175b2f277a9a167d2d07361883) · [계획 이후 비교](https://github.com/laadkke-arch/agentflow-open/compare/13be736df17a4c697880f57029d16de38db061dd...3215fdb429e307175b2f277a9a167d2d07361883) · [계약](manifest.json)

선행 인계 `be7d6e3365e090ca674b4f0baaf570a27f8e51cf` 하나를 `workbench.session start --fetch`로 고정했다. 검사판 `038ac865c8d2cada84e32989bdd5eb174f4bb7d8`의 V8628과 지정 fixture·원장·렌더·검산 기록을 인수했다. 그 연구의 단일 January store 주입은 local에서 49개 색 차이, shared에서 translate 신호 2개 제거를 보였다. 이번에는 #8628의 실제 브라우저 입력에 집중한다. 선행 작업의 나머지 자연 이슈와 자동 판독은 이 과제의 분모에 포함하지 않는다. [119 인계](https://github.com/laadkke-arch/agentflow-open/blob/be7d6e3365e090ca674b4f0baaf570a27f8e51cf/docs/workstreams/research/AF-RES-119/HANDOFF.md) · [119 결과](https://github.com/laadkke-arch/agentflow-open/blob/038ac865c8d2cada84e32989bdd5eb174f4bb7d8/docs/workstreams/research/AF-RES-119/RESULT.md) · [출처 원장](sources.jsonl)

## 입력과 판

- 원 작성자는 순서형 x와 색 인코딩이 있는 interval brush에서 mark 위와 빈 영역의 동작이 다르다고 보고했다. opening fence의 CRLF까지 보존했다. Vega Editor fragment에는 v5.2.0 **스키마 URL**만 추가돼 있다. 최초 공개 리비전, 당시 실행 엔진·브라우저·렌더러, 절대 데이터 주소와 원 바이트, 초기 brush, 좌표 및 점프의 수치 기준은 원글과 공개 댓글 목록에서 확인되지 않았다. GIF는 별도 접근 기록을 둔다. [원글](https://github.com/vega/vega-lite/issues/8628) · [opening 대조](evidence/issue-8628.json)
- 대체 환경은 Vega-Lite npm `5.6.0`과 Vega npm `5.22.1`, 시스템 Chromium `156.0.8078.79` headless, Playwright Core `1.56.1`, Linux, `TZ=UTC`, `en-US`, viewport 900×650, DPR 1, 글꼴 DejaVu Sans다. 5.6.0 npm 배포본의 JS 내부 문자열은 `5.5.0`이다. npm package metadata·tarball integrity·파일 해시·내부 문자열을 모두 기록하며, 고정 소스와 배포본이 바이트 단위로 같은 빌드라는 추정을 두지 않는다. 같은 배포본을 두 렌더러에 쓴다. [고정 입력·런타임 파일 지문](fixture/fingerprints.json) · [VL 태그](https://github.com/vega/vega-lite/tree/1ff500a596b51f579d622c2559a4e7ca3f5d8cdd) · [Vega 태그](https://github.com/vega/vega/tree/7eafbbd4d53d0ce9f08e74ff96c90d411b1bb80a)
- opening의 `data/seattle-weather.csv` 요청에 고정 Vega datasets 2.5.3의 1,461행 CSV를 그대로 반환한다. GitHub raw와 119의 복사본을 바이트 비교했다. 로더와 글꼴 고정을 실험 환경 설정으로 남긴다. [CSV](fixture/data/seattle-weather.csv) · [원 배포 CSV](https://raw.githubusercontent.com/vega/vega-datasets/664835b3090a9069d4626ccae36fad75230c8f36/data/seattle-weather.csv)
- 원형과 119의 수정안을 재사용한다. local의 유일한 의미 diff는 `/encoding/color/value` lightgray → steelblue, shared는 `/params/0/select/translate` 생략 → false다. 각 대안에 projection, clear, mark 변경을 섞지 않는다. CSS, 입력 장치, plot layout, 런타임 데이터와 시간대를 공통으로 고정한다. [정확한 변경](fixture/changes.json)

## 실행 전 기대와 반환 메뉴

| 조건 | 조건부 기대 | 반대로 관측될 수 있는 조건 |
| --- | --- | --- |
| 빈 상태에서 막대 또는 빈 plot에 down | 두 좌표에서 새 extent의 시작이 x다. 동일 x에서 y만 다르면 x 투영은 같다. | 렌더러의 item 또는 group 원점이 다르거나 mark 위에서 이벤트를 소비할 때 실측이 달라질 수 있다. |
| 기존 brush 안에서 down이 foreground brush를 맞힘 | 원형·local은 시작 폭을 저장하고 첫 move에서는 전체 폭을 평행이동한다. 두 위치의 이름이 막대/빈 곳이어도 foreground가 같으면 같은 경로다. | 폭이 0이거나 overlay가 hit를 받지 않으면 새 선택 경로가 열릴 수 있다. 경계 clamp는 두 끝 이동을 제한한다. |
| 기존 brush 밖 또는 foreground 이외에 down | 새 extent로 교체한다. down에서 두 끝이 같으므로 기존 tuple이 비워질 수 있다. | 브라우저 hit에 기존 overlay나 다른 mark가 나타나면 계획 위치·실측과 결과를 각각 남긴다. |
| shared가 foreground를 맞히거나 새 selection을 시작 | translate anchor/delta를 기대하지 않는다. 같은 overlay를 맞혀도 새 extent는 가능하다. | 다른 사양의 clear, on, bind가 꺼졌다면 이 결론을 따로 검증한다. |
| fallback 변경 | 빈 store의 기본 predicate는 true. 활성 store의 외부 bar fill만 달라지고, range·증거 수·원자료·축은 유지될 것으로 예상한다. | `empty:false`, 색 scale이나 fillOpacity가 섞인 입력은 정지 효과부터 달라진다. |
| x month band의 화면 경계 | 폭이 0이면 범주 집합 없음. 같은 band의 소이동은 합법적으로 범주 집합을 유지하며, padding 또는 band 시작을 건너면 범주가 바뀔 수 있다. | 같은 좌표의 data domain이나 scale 종류가 바뀌면 눈금과 투영을 다시 검증해야 한다. |

계약의 근거는 원장의 VL-SELECT, VL-DEFAULT, VL-COLOR, VL-EMPTY, VL-INTERVAL, VL-PAN, VL-PROJ, VG-STREAM, VG-VIEW, VG-COORD, VG-SVG, VG-CANVAS, VG-BAND와 각 test·예제다. 문서의 x/y projection 일반 설명과 고정 소스의 band `E` 열거는 판·scale 종류를 명시해서 함께 사용한다. [기본 mouse stream](https://github.com/vega/vega-lite/blob/1ff500a596b51f579d622c2559a4e7ca3f5d8cdd/src/selection.ts#L304-L320) · [interval의 두 brush와 gate](https://github.com/vega/vega-lite/blob/1ff500a596b51f579d622c2559a4e7ca3f5d8cdd/src/compile/selection/interval.ts#L31-L40) · [band 역변환](https://github.com/vega/vega/blob/7eafbbd4d53d0ce9f08e74ff96c90d411b1bb80a/packages/vega-scale/src/scales/scaleBand.js#L119-L160)

사전 반환은 같은 세 공식 후보에 한정한다. 결과를 보기 전 작성한 이 비교는 단일 작업자의 명시적 판독 규칙이다.

| 저장·컴파일·정지 증거까지 | 반환 우선순위와 보류 조건 |
| --- | --- |
| 원형과 정지 화면만 | 아래 세 절을 조건부로 제시한다. 기존 brush 이동인지 신규 생성인지, 누른 target이 무엇인지에서 링크가 갈린다. |
| local diff 또는 fill fallback만 다름 | 모양을 바꿀 목적이면 조건 색 절. 입력 움직임 수정으로 추천하기 전 hit와 궤적을 확인한다. |
| shared diff 및 anchor·delta 제거 | 기존 brush 이동 금지 목적이면 translate 절. 새 범위 생성 및 실제 겉보기 점프는 재생 후 판정한다. |
| x month 필드와 band enum 컴파일 | 데이터 범주 해석에는 projection 절. 셀이 달라지는 첫 이벤트가 없으면 경계 동작은 정하지 않는다. |

[translate](https://github.com/vega/vega-lite/blob/1ff500a596b51f579d622c2559a4e7ca3f5d8cdd/site/docs/parameter/select.md#L177-L192) · [조건 색](https://github.com/vega/vega-lite/blob/1ff500a596b51f579d622c2559a4e7ca3f5d8cdd/site/docs/encoding/condition.md#L55-L92) · [projection](https://github.com/vega/vega-lite/blob/1ff500a596b51f579d622c2559a4e7ca3f5d8cdd/site/docs/parameter/select.md#L55-L73)

## 입력과 판정 봉인 원칙

- pilot에서 원형 scenegraph의 막대 색 조각 하나의 중심부와 같은 x의 막대 없는 plot 위치를 구한다. 막대 조각의 네 경계·datatype, plot/axis 범위, 페이지 위치, 문서의 `elementFromPoint`와 실제 `View.addEventListener` 항목을 남긴다. Canvas hover가 active를 세팅하므로 모든 시도는 off-chart 시작점에서 목표로 먼저 move한다. 두 위치는 축 tick의 label이나 clipping border와 겹치지 않는 여유 픽셀을 고른다. 기준 좌표는 모든 수정안과 두 렌더러에서 공통으로 사용한다. 기존 brush의 초기화는 같은 별도 드래그이며 두 주 위치를 포함하는 x 범위로 고정한다.
- 주 행렬은 3 설정 × 2 렌더러 × 2 초기 상태 × 2 위치 × 2 새 페이지의 48행이다. 버튼은 mouse left, modifier 없음. 첫 move는 +1 CSS px, 그 뒤 같은 y에서 +20, +40으로 진행한 뒤 up. down 전·down·각 move·up의 browser event와 첫 rAF의 픽셀/투영/fill을 남긴다. 뒤 rAF는 sampling이 너무 일렀는지 점검한다. 초기 brush drag의 이벤트와 상태는 별도 phase다. store를 쓰거나 View.signal setter를 부르거나 event handler를 직접 호출하지 않는다.
- down 전에 일치해야 하는 조건은 plot 좌표계·렌더러 크기·상태(시작 픽셀 extent, 실제 투영 tuple), 정상 이벤트, 예상 실제 hit class다. 비교는 관측 hit class와 시작 상태가 맞는 쌍으로 한다. 기존 brush 안의 mark 위치와 빈 위치가 모두 brush foreground면 그 둘은 brush hit의 반복 대조이며, 막대와 배경의 직접 hit 비교는 빈 초기 상태 및 밖 대조에서 한다. 위치·실측 hit가 달라진 행은 남겨서 판정 수에서 따로 센다. 미실행·렌더 오류·초기화 실패·성공 무변화를 별개 상태로 둔다.
- 시각 점프 판정은 조작 모드에 맞춘 픽셀 잔차다. 새 범위면 down 예상 `[x0,x0]`, 첫 move 예상 `[x0,clamp(x1,0,W)]`. 기존 이동이면 down이 초기 extent 보존, 첫 move가 초기 두 끝에 `x1−x0`를 더한 후 전체 폭을 보존하며 plot 안으로 clamp하는 것이다. x0과 x1은 보정한 입력 CSS 좌표, W는 plot 폭이다. 끝별 절대 오차 최대값이 2px를 **초과**할 때 대체 환경의 점프로 표기하고, 0.5·1·2·4px를 각각 별도 집계한다. down의 잔차와 first의 잔차를 따로 남긴다. 창에서 마지막 move 좌표와 up 좌표도 확인한다. 투영 집합은 band 시작·끝과 pixel extent의 겹침으로 독립 확인하며, 0 폭은 null로 기대한다. 범주 증감, zero-width clear, overlay 전환과 픽셀 잔차를 따로 계산한다.
- 대조는 본 행에서 분리한다. 1px 경계의 같은 쪽/넘는 쪽, 이동 없는 클릭, 기존 brush 안·밖의 동일 길이와 뒤 방향, 대표 관측기 해제 입력을 별도 ID로 둔다. 비교 대상은 x/y 축·원 CSV 및 로드된 source, 요약 bar key와 기하, 선택 안/밖의 fill, brush 폭과 enum이다. 사용자의 실제 장치·페이지에서 재현된 조건과 접근성 결과는 그 환경의 증거가 있어야 판단할 수 있다.
