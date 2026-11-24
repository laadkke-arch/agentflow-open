# AF-RES-127 최종 인계

**DONE.** OpenLayers 10.11.0의 본 16/16과 대조 12/12를 trusted 마우스 기록으로 비교했다. 고유 외부 1차 저작 37개를 직접 읽었고, 보충 10/10 및 파일럿 3/3을 포함해 깨끗한 두 경로의 41/41행이 재현됐다. 명시 세션·저장소 공통 검사는 모두 종료 0이다. #9625 저자의 실제 앱 판·설정·전후 좌표·채택은 미확인으로 남겼다. fredj의 CodeSandbox 예는 HTTP 403이었다. 공개 댓글의 코드·의도와 당시 소스에서 해당 계약을 대조했다. [결과](RESULT.md) · [출처 원장](sources.jsonl) · [검사 영수증](evidence/acceptance/RECEIPT.md)

선택된 같은 parcel-01의 down에서 Translate가 먼저 처리하면 geometry만 움직였고, DragPan이 먼저 수락한 뒤 넘기면 geometry와 center가 함께 움직였다. 미선택 피처와 빈 배경은 center만 12/16이었다. 같은 경계 밖에서 0px는 pan, 6px는 피처 이동이었다. 관측 뒤 기능 절은 화면 A가 6/16행, 차트 질문 B가 4/16행, 지도 원전 C가 0/16행에서 달라졌다. B는 A가 놓친 두 셀을 맞혔고 A의 맞힘 한 셀을 보류했다. C는 8/8 셀을 맞혔다. [행별 실제 값](runs.jsonl) · [기능 절과 적용 조건](returns.csv) · [고정 재집계](evidence/acceptance/recount.json)

## 기반과 저장 구조

계획 `4a92e22c5356dc7ea2b715f671077e8ab63b2835`, 시작 통합 `5c0eca97d41e084a76bddd7cb0e976e5e9f792e8`다. AF-RES-123 등록 인계 `7554304d725082275661cdd011ad4f4472a00438`를 manifest에 고정하고 검산판 `0a4acb5368e2f064e9b3eb21b52d219de262440f`와 분야 대조를 읽었다. 과제 브랜치는 `work/research-af-res-127`, 범위는 `docs/workstreams/research/AF-RES-127/`다. [manifest](manifest.json) · [시작 범위](SCOPE.md) · [선행 인계](https://github.com/laadkke-arch/agentflow-open/blob/7554304d725082275661cdd011ad4f4472a00438/docs/workstreams/research/AF-RES-123/HANDOFF.md) · [선행 검산](https://github.com/laadkke-arch/agentflow-open/blob/0a4acb5368e2f064e9b3eb21b52d219de262440f/docs/workstreams/research/AF-RES-123/RESULT.md)

저장소의 workbench 계약과 AF-RES-123의 고정 npm·브라우저 입력/페이지 관측/집계 구성을 재사용했다. 이번 fixture에는 타일 없는 Canvas 점, 대조 가능한 seed, 현재판 OpenLayers package lock과 bundle 지문을 둔다. `plan.json` 한 곳에서 세 시험의 궤적·순서·상태를 전개하고 같은 driver를 거친다. 관측의 raw 바이트와 PNG는 evidence에 두고 실행·추천 원장은 다시 생성할 수 있다. 두 깨끗한 경로의 합의와 공통 검사는 모두 같은 작업자의 확인이며 독립 판독은 미실행이다. [설치와 실행](reproduce.md) · [질문별 자기검산](SELF_CHECK.md)

## 고정 검사와 묶음

Codex Cloud에서 고정 결과 `cee582b227357f5935fd87eaa5e3a0e415d65cc9`를 각각 새 clone했다. 브라우저 입력·렌더러·버전·물리값·이벤트 순서·표면 불일치 0을 확인했다. 시각과 Canvas readback 경고 횟수의 차이를 비교 보고서에 분리했다. `workbench.session check … --fetch`는 검사 시 통합 `4ad08bf17c4b1ff6ac6219293ed9fe875743cf38`에서 의존과 계약을 확인했다. Git diff의 86개 파일은 모두 소유 범위이며 명시 세션의 경로 합계는 manifest를 뺀 85개다. 공통 검사의 내부 `check-all`은 `no_active_sessions`이고, 명시 검사·공통 검사·독립 호출한 `scripts/check.py --require-git`의 각 범위와 stdout/stderr를 저장했다. [세션 검사](evidence/acceptance/session.json) · [공통 검사](evidence/acceptance/cloud-check.json) · [원 출력·명령](evidence/acceptance/RECEIPT.md)

| 묶음 | GitHub에서 확인한 판과 대표 파일 |
| --- | --- |
| ① 범위와 B 봉인 | [11c78d102bdee10b9de4f3c87475e5cd8136d11a · predictions](https://github.com/laadkke-arch/agentflow-open/blob/11c78d102bdee10b9de4f3c87475e5cd8136d11a/docs/workstreams/research/AF-RES-127/predictions.csv) |
| ② 원전·A/C·fixture·pilot | [ed2d7895451b3653d72fc7665a27281f2e20e1ee · plan](https://github.com/laadkke-arch/agentflow-open/blob/ed2d7895451b3653d72fc7665a27281f2e20e1ee/docs/workstreams/research/AF-RES-127/plan.json) |
| ③ 본 16행 | [92e6fd713ac324be2e2ca7981a46949be371b85f · 본행 영수증](https://github.com/laadkke-arch/agentflow-open/blob/92e6fd713ac324be2e2ca7981a46949be371b85f/docs/workstreams/research/AF-RES-127/evidence/main/RECEIPT.md) |
| ④ 대조 12행·타 분야·추가 반례 | [18b4bf1a5e5683d2845bfd641c7e4fe0e2e87fd9 · 대조 영수증](https://github.com/laadkke-arch/agentflow-open/blob/18b4bf1a5e5683d2845bfd641c7e4fe0e2e87fd9/docs/workstreams/research/AF-RES-127/evidence/controls/RECEIPT.md) |
| ⑤ 본문·원장 고정 및 두 경로 검사 | [cee582b227357f5935fd87eaa5e3a0e415d65cc9 · 결과](https://github.com/laadkke-arch/agentflow-open/blob/cee582b227357f5935fd87eaa5e3a0e415d65cc9/docs/workstreams/research/AF-RES-127/RESULT.md) · [92906faa2f3cd746003782d3862e03db4429940f · 수용 증거](https://github.com/laadkke-arch/agentflow-open/blob/92906faa2f3cd746003782d3862e03db4429940f/docs/workstreams/research/AF-RES-127/evidence/acceptance/RECEIPT.md) |
| ⑥ 최종 인계 | 이 문서만 추가한 별도 커밋 |

## 첫 재개 행동

실제 앱에 적용한다면 #9625 작성자가 말한 첫 press를 기준으로 사용 판과 Translate의 features/filter/layers, 시작 selected ID, down을 받은 순서, geometry와 center의 전후 값을 한 건 확보한다. 저자의 입력이 공개되기 전에는 고정판의 판 차이와 보충의 첫 press 경로를 시작점으로 쓴다. 이전에 403이었던 공개 예제를 새 접근 경로에서 열 경우 아래 입력으로 본문 bytes를 확보하고, fredj의 예제와 저자 앱의 출처를 구분한다. [작성자 후속](https://github.com/openlayers/openlayers/issues/9625#issuecomment-498282656) · [대체 경로](evidence/map-sources.md)

```sh
af127_example=$(mktemp -d /tmp/af127-example.XXXXXX)
curl -fLsS --max-time 30 'https://codesandbox.io/s/translatefeatures-xrwsp' -o "$af127_example/example.html"
sha256sum "$af127_example/example.html"
```

색인 제안 — AF-RES-127 · 동일 지도 hit의 피처 이동·뷰 이동·동시 처리와 반환할 기능 절 · DONE · [결과](RESULT.md) · AF-RES-123 고정 인계 의존.

| 불일치·약점 | 다음 조사 자료·행동 | 판정을 바꿀 관측 |
| --- | --- | --- |
| 저자의 앱 런타임·옵션·실제 좌표가 미확인이고 v6.0.0과 10.11.0의 filter 조합이 갈린다. | [원 작성자 후속](https://github.com/openlayers/openlayers/issues/9625#issuecomment-498282656) 및 [판 대조](evidence/map-sources.md)를 열고, 앱의 features/filter/layers와 down→첫 drag 한 건을 확인한다. | 앱의 판에서 적격 hit 및 world geometry/center 변화가 밝혀지면 앱에 반환하는 선택/필터 절을 재판정한다. |
| 동시 처리 이동량은 단일 Chromium·Canvas·DPR 및 2프레임 대기 조건이다. | [두 처리기의 원 로그](evidence/main/M-in-feature-translate-pan-r1.json)의 포인터를 다른 시간 간격·렌더러·입력 장치에서 비교한다. | 같은 hit와 down 수락에서 frame 좌표 또는 두 상태 중 어느 것이 바뀌는지가 달라지면 수치·범주의 적용 범위를 좁힌다. |
| B의 지도 요약 선노출과 단일 판독이었다. 실제 링크 채택·읽기 시간은 미측정이다. | [봉인표](predictions.csv)와 [기능 절 원장](returns.csv)으로 판과 설정이 다른 사례를 가리고 독립적으로 읽히며 링크 선택·비용을 기록한다. | 차트 질문으로 지도 원전 기준에 없던 맞힘이나 실제 링크 사용에 차이가 생기면 실무 입력 비용과 반환 순위를 다시 평가한다. |
