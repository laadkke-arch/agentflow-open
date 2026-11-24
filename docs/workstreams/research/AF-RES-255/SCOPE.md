# AF-RES-255 범위와 사전 판정

002·003의 reftest 이미지 관계와 실제 단어별 줄을 Chromium/Blink와 WebKitGTK에서 각각 두 새 세션으로 확인한다. 원형 관측 단위는 입력×엔진×반복으로 8개다. 단어 좌표는 별도 로드에서 수집한다. 003의 두 시험 블록과 입력 내 파란 비교 블록은 각 로드에서 따로 보되 원형 시험 수는 하나다. 사용자의 읽기 쉬움, 자막의 영상·음성 동기, 조판 일반 이론과 AF-RES-238~242 입력은 범위 밖이다.

## 착수와 표집

- 저장소 `laadkke-arch/agentflow-open`, 배정 `work/research-af-res-255`, 소유 경로 `docs/workstreams/research/AF-RES-255/`. 처음 조회한 통합 SHA `80b4df0af9ae814e2f5d70fa24ffdeeb64f9308a`에서 착수 직전 `d1353701530ffd4c68587276c15d988d2cc92972`로 진행했다. 두 판 모두 AF-RES-255 1회차 RUNNING, 의존 AF-RES-232였다. 계획 SHA `7369707441e2eb70e84004ca6cb3bfeefc8b4061`의 진행표에는 AF-RES-255 행이 없고 착수판과의 차이 7개 커밋은 진행표에 한정된다. 세 판의 빈 contents 본문은 반환된 blob `7a0b6490b055704cd2572c9d3a37a6f81b11def6`, `41cefbc22f8d86795d0aff7204c9cbefb69577fa`, `f6587b49dccac907b5e2dd1e67bf3e36c1590ccd`로 풀었다. [착수판 지침과 진행표](https://github.com/laadkke-arch/agentflow-open/tree/d1353701530ffd4c68587276c15d988d2cc92972).
- 232 중앙 DONE, 자체 PARTIAL, 실제 엔진×시험 0/4. 결과 파일과 입력·예측·분할 원표를 지정된 `430a1a5ec049f58878d963cb8ca539c9375f93d0`에서 읽었다. `workbench.session start --fetch`로 이 의존 브랜치와 허용 경로를 고정했다. [232 인계](https://github.com/laadkke-arch/agentflow-open/blob/430a1a5ec049f58878d963cb8ca539c9375f93d0/docs/workstreams/research/AF-RES-232/HANDOFF.md).
- GitHub에서 WPT 커밋 `5ad65d6ea6c649696be2d0cf5188dfdb43f8d801`을 얕게 fetch했다. root tree `c8645fc7b4202c1da3240835693ebe137bf9fa58`, `css/css-text` tree `08b1300e11f6d4eb22f252b13e1ceaaf0e978e51`의 3,183개 경로에서 `text-wrap[-style]`의 `balance` 선언 또는 연결된 규격 앵커를 검색했다. 검색 결과의 문자 순서는 `LC_ALL=C`다. 적격 조건은 줄 균형 렌더링 비교, 별도 `match`/`mismatch` HTML 참조, Ahem 기반이다. 두 지명 앞 세 후보의 입력을 확인했다. `crashtests/text-wrap-balance-nested-blocks-crash.html`은 충돌시험이고, `parsing/white-space-shorthand-text-wrap.html`은 계산 스타일 단언이며, `white-space/text-wrap-balance-001.html`은 높이 비교 harness다. 이 셋은 별도 WPT 이미지 참조가 없다. 232가 지명한 입력은 `white-space/text-wrap-balance-002.html` L3·L6–15와 `white-space/text-wrap-balance-003.html` L4·L6–24다. 별도 참조의 파일명은 입력 link에서 읽었으며 blob 예상값은 인계에서 받았다. [고정 검색 트리](https://github.com/web-platform-tests/wpt/tree/5ad65d6ea6c649696be2d0cf5188dfdb43f8d801/css/css-text).

## 노출 순서와 동결 규칙

1. 232의 고정 인계·원표에서 알려진 참조 관계와 예측을 읽었다. 002의 불일치 참조 관계가 알려져 있고 003의 입력 L24에는 word 4 다음에 `<br>`가 있다. 두 건 모두 사전 정보에 노출되었으며 독립 가림 채점의 적격 분모는 0이다.
2. 지정 WPT 트리와 입력 blob 및 입력 link를 확인했다. 이 커밋에서 별도 참조 본문·픽셀, 공개 run 및 로컬 렌더링을 열기 전 아래 예상과 판단 규칙을 동결한다.
3. 별도 참조와 직접 자료를 연다. 입력은 교체 없이 실행한다. 원 실행은 고정 WPT의 `./wpt run`과 정규 WebDriver 제품으로 각각 한 시험씩 두 번 실행한다. 비교 결과의 PNG와 runner report를 수집하며, 실행 누락·timeout·오류는 별도 상태다.
4. 같은 원문을 별도 세션에 열어 `document.fonts.ready` 이후 텍스트 `Range.getClientRects()`를 기록한다. 단어는 1부터 시작하며 블록별이고, 동일 블록의 y가 0.5 CSS px 이내인 좌표를 같은 줄로 묶는다. 여러 fragment는 원행으로 보존한다. 실제 `Ahem` face 상태, font resource, glyph·space advance와 블록 폭을 먼저 확인한다. CSS px와 스크린샷 픽셀을 DPR로 구별한다.

## 동결한 예상과 판정 단위

| 입력 | 고정 간격 모델의 정적 예상 | 공개 시험이 확인하는 관계 | 반전/해석 기준 |
|---|---|---|---|
| 002, 20ch·20px, `[3,3,3,3,3,3]` | Ahem 1ch/글리프·공백이면 balance `3` → `[11,11]`, auto의 최대 접두사 `5` → `[19,3]` | `mismatch`의 정상 성공은 참조와 이미지가 다름 | 폭·폰트가 맞는데 다른 위치면 exact cut 예상이 틀린다. 다른 위치에서 mismatch도 성공할 수 있다. |
| 003, 35ch·15px, `[3,8,5,3,6,4,3,4,3]` | balance `4` → `[22,24]`, 최대 접두사 `6` → `[34,12]`. plain/inline 양쪽 cut 4를 예상 | `match`의 정상 성공은 두 초록 시험 블록과 파란 비교 블록을 포함한 페이지가 별도 참조와 이미지 일치 | 특정 분기나 입력별 내부 비용은 별도 근거가 필요하다. 파란 비교 블록 좌표는 기대값이다. |
| C1 `aaaa bbb ccc dd ee`, W8ch | auto 최대 접두사 `2;4` `[8,6,2]`; 고정 줄 수 최소 분산 `1;3` `[4,7,5]`. word 2 뒤 break이면 최소 분산 후보 `2;3` `[8,3,5]` | 합성 통제의 단어 폭·간격·줄·픽셀 비교 | 강제 경계는 cut 1 뒤 첫 줄을 선택할 수 없게 한다. 결과가 `2;4`이면 강제 뒤 목적 최적화에 관한 더 강한 예상이 틀린다. |
| W7 `aaaa b c dddd ee`, W7ch | auto 최대 접두사, 최대 줄 길이 최소 `2;4` `[6,6,2]`; 최소 분산 `1;3` `[4,3,7]`. word 2 뒤 break이면 고정 3줄의 최소 분산과 최대 줄 길이 최소 모두 `2;4` | 합성 통제에서 같은 줄 수로 목적 후보의 출력이 갈림 | `[6,6,2]`이면 해당 관측에서 최소 분산 선택은 성립하지 않는다. `[4,3,7]`이면 최대 줄 길이 최소 선택이 성립하지 않는다. 같은 출력은 같은 코드 분기를 보장하지 않는다. |

표의 번호는 줄 끝 단어의 1-based index다. 모델은 ASCII 단어, 줄 안 gap 1ch, 양끝 gap 0, 강제 개행을 독립 그룹 경계로 삼는다. 줄 수는 관측 auto와 먼저 대조하고 고정 k 비교를 한다. CSS의 auto 구현은 UA 정의다. 이분 탐색, 최대 줄 길이 최소, 분산 최소는 구별된다. 기준 실행은 정상 폰트, 반례는 별도 폴더와 상태로 기록한다. 원형 이미지·실제 단어의 y·cue 시간은 각각 추적한다.
