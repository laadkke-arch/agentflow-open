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

## 저장 방식

셸 git push는 HTTPS 자격증명이 없어 실패했다. 허용된 GitHub 연결로 같은 트리의 원격 커밋을 만들었다. 묶음1 원격 SHA는 1faf648d69d300ffe0dd970cf3b42aea64eb968e이다. 로컬 임시 커밋 bccd928c2ba263181515adf5c08b6cca90d1f709은 원격 결과가 아니다. 두 트리 diff가0인 것을 확인한 후 로컬 HEAD를 원격에 맞췄다. 이후 봉인도 GitHub 연결의 expected-head 조건으로 저장한다.
