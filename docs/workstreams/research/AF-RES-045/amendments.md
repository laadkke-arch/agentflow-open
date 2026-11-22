# AF-RES-045 변경·노출 원장

## 봉인 전 보정 — 2026-11-22 22:16–22:18 UTC

결말 댓글·PR·시험은 아직 열지 않았다. 원문과 별도 문맥의 같은 모델 검토로 아래를 고쳤다. 초안은 evidence/audacity-initial.json, audacity-api-supplement.md, preseal-spatial-review.md, preseal-temporal-review.md에 남아 있다.

| 항목 | 최초 초안 | 봉인 입력의 보정 | 이유·영향 |
| --- | --- | --- | --- |
| AUD01 accessor | generic GetInfo Selection 가능성 | 당시 실제 존재한 Nyquist *SELECTION* START/END 조회 | 2.3.3 GetInfo에는 Selection 타입이 없고 Nyquist 속성은 있음. A/B 수치 동률은 유지. |
| AUD03 Hz 경계 | 2001Hz를 밖으로 가정 | Fs48000/N2048, bin64=1500Hz, first excluded bin86=2015.625Hz | 실제 bin 반올림 조건 때문에 2001Hz는 외부라 확정 못함. floor low=42(984.375Hz), exclusive high=86이며 연속 [1000,2000]과 동일한 집합이 아님. |
| AUD03 feather | outer feather2bins만 명시 | hard gain k42..85=-6dB/밖0; centered5bin log-gain 등가중 평균 B | 수치 예측을 검사 가능하게 함. 정상-6/-6, 경계0/-2.4dB. 연구자 toy이며 실제 NR 결과로 쓰지 않음. |
| AUD02 대비 | 대비0 | 휘도 차이0, 대비비1:1 | 비율과 차이를 구별. 결론 변화 없음. |
| M02 CSS | font·figure 고정이면 clip만 남음 | single page·same orientation도 연구자가 고정할 때의 clip fallback | 원전에는 회전/분할도 있음. 원문이 정확 legend bbox API를 정한다는 주장을 배제. |
| M02 bbox | 보존 기준 불명 | 동일 figure에서 legend artist만 없는 상태로 tight_layout 적용한 좌우 axes bbox | 정상10-entry와 동일하다는 별도 주장을 하지 않음. 정확 기준에 맞는 후속 증거만 지지 가능. |
| M03 수치 | .5/max(arr)를 무조건 출력처럼 표현 | linear/non-inverted axes limits=[0,max(arr)]일 때 (value-ymin)/(ymax-ymin) | 실제 colorbar limits는 후속에 확인. 중심 목적은 이미 원요구에 있어 새로운 선택 발견으로 세지 않음. |
| frame schema | 두 조사자의 열 이름 합집합 | 60행 공통 열로 정규화 | 노출순서·선정6·탈락1·후순위53 유지. 묶음1 원판도 Git에 보존. |
| request ID | SCOPE 서술 A01/A02/A03 | CSV 정규 ID AUD01/AUD02/AUD03 | 각각 #407/#511/#644를 뜻하는 별칭. 표본 변경 없음. |

## 사전 노출 사건

- E01: AUD02 최초 게시 본문에 사후 Subtasks와 checked #2713이 보임. 원보고 영역을 따로 읽었으나 최초판은 미복원. 명시적 결말 노출 제외 감도에서 AUD02를 뺀다.
- E02: AUD03의 요구 이전 2.4.2 API를 읽는 중 AUD01의 요구 뒤인 Nyquist 코드도 봄. 이후 AUD01 요구 이전 2.3.3에서 같은 START/END 속성을 확인했다. 최초 노출 자체는 삭제하지 않으며 확장 감도에서 AUD01도 제외한다.
- E03: root가 Matplotlib 최초5본문을 한꺼번에 출력하여 정원 이후 #13650 본문도 읽음. 선정3은 이미 앞선 #13430/#13522/#13600이며 바꾸지 않음.
- 모든 최초 게시 본문은 현재판이다. updated_at만으로 본문 변경을 단정하지 않으며, exact creation-body가 검증된 사례 분모는 아직0이다.
- 원문에 이미 있는 Adobe Audition 참조(AUD03)는 새로운 타 분야 발견으로 계산하지 않는다.

## 봉인 후 정정 — 첫 후속 열람 뒤

봉인 `0d998cb3503e8a7f0faf2bf2f8e62dd046a662b1`은 2026-11-22T22:19:23Z, 첫 후속 열람은 Audacity 조사자의22:20:00.421Z다. SCOPE/frame/requests/predictions는 그대로 보존한다. 아래는 사후 판독과 해석의 정정이며 원래12행·6자리와 넓은3/2/1분류를 지우지 않는다.

| 항목 | 원본·오류 | 새로 확인한 내용·이유 | 영향과 원집계 |
| --- | --- | --- | --- |
| AUD03 API 활성 여부 | 전역 define와 조건부 경로를 읽고 같은 파일의 local undef를 놓침 | [2.4.2 L75–77](https://github.com/audacity/audacity/blob/16d52f63a4183bba77ef7305d14622958dc0d1d5/src/effects/NoiseReduction.cpp#L75-L77)은 UI에 영향이 표시되지 않는 이유로 비활성화.22:22:25.972Z패치에서 단서,22:22:34.620Z기존판 오류 확인,22:23:44.433Z재열람. root22:30:53.903Z재확인. | AUD03-P1/P2의 실제 적용 가능성 해석 정정. toy산술 유지. 실제출력·엄격지지0이며 실제 양쪽 기각으로도 세지 않음. |
| M01 조작 차이 | different_conditional이지만 P2는 내부 기하에 scaling이 실패한다고 이미 예상 | 다른 preferred_choice가 동일 관측의 반대 성공 예측을 뜻하지 않음. A성공·B실패가 관측돼도 양쪽 규칙의 출력 예상과 양립 가능. | M01 원분류 유지. 넓은다름3과 엄격판별분모0을 분리. |
| M03 첫 본문 | current initial body; 불변 최초판 미확인 | [댓글470135635](https://github.com/matplotlib/matplotlib/issues/13600#issuecomment-470135635)은 제목만 제출한 뒤 요구를 완성했다고 밝힘. | 생성시점본문은완성요구와다름. 완료본문이해결조언보다앞이라는상대순서만확인. 6슬롯유지. |
| AUD02 제목·선정 | 현재 제목selection검색, 생성일오름차순 | [511 timeline](https://api.github.com/repos/audacity/audacity/issues/511/timeline?per_page=100)2022-03-22rename: 최초제목에는selection없음. | 현재 제목으로 과거 생성 이슈를 표집한 frame은 유효하나 당시 제목검색의 복원이 아님. E01제외감도 유지. |
| AUD02 contrast0 잔존 | 사전정정표는1:1로고쳤으나 P1문구에contrast0이남음 | 동일색의 휘도차이0과 대비비1:1을 구분. WCAG essential 예외는 사용자선호만으로 성립하지 않음. | AUD02-P1표현 정정; P2미확인·쌍판별불가 유지. 원예측문 수정없음. |
| AUD-O360 배당 | agent는별도release저작으로산입제안 | canonical은6165변경의release재게시로보수적중복처리. 원agent파일보존. | 주집계30저작=요구6+제공9+후속9+비교6. 별개release로세면31이나채택안함. |
| 관련 시험과 봉인 시험 | PR13603시험과통과보고, Cartopy1355지도시험 | 전자는None crash, 후자는다른map/gridliner입력. 두봉인입력의A/B시험과다름. | T와R,같은입력과관련입력을분리. 후속완전일치0/6. |

### 분모 해석과 반증 조건

사전 규칙은 같은 조작·입력·목적을 요구한다. M01/M02/M03의 원작성자 정성적 조작 수락을 별도 근거로 남기되, 두 봉인 입력을 확인하지 못한 사례를 판별 분모에 넣지 않았다. 넓은 사전분류는 다름3/같음2/판별불가1이며, 엄격 조건부 판별 분모0, 유일지지0, 양쪽기각0, 비율은 **해당 없음**이다. 이는0%성공률이나 실패율이 아니다. 같은 입력을 증명하는 공개 실행·시험자료가 추가되면 해당 행을 새 판으로 다시 채점한다.

## 저장 방식

셸 git push는 HTTPS 자격증명이 없어 실패했다. 허용된 GitHub 연결로 같은 트리의 원격 커밋을 만들었다. 묶음1 원격 SHA는 1faf648d69d300ffe0dd970cf3b42aea64eb968e이다. 로컬 임시 커밋 bccd928c2ba263181515adf5c08b6cca90d1f709은 원격 결과가 아니다. 두 트리 diff가0인 것을 확인한 후 로컬 HEAD를 원격에 맞췄다. 이후 봉인도 GitHub 연결의 expected-head 조건으로 저장한다.
