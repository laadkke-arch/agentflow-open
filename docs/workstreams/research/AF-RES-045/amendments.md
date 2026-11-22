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

## 최종 별도 문맥 검토 반영

- M03목적변경은 y-data 고정 논리에 한정한다.3.0.2는x도환산하므로가로중앙은별도transform이필요하다. RESULT·카드·검산설명만좁혔고봉인예측·12행집계는그대로다. 근거는 final-spatial-review.md의3.0.2 L1001–1003재독.
- sources의MPL-SEARCH/MPL-IMG-FAIL0/1 final_url literal을실제url필드값으로정규화하면서preseal_final_url을보존했다. TF03/04/07/08의실패→성공중복연결은original_duplicate_of와변경이유를남겼다. connector검색의관측하지못한최종URL은null과사유를유지했다. 모든UTC interval은interval그대로다. 산입수30과판정은변하지않았다.
- 최종재판독의신규열람은별도sourceID로추가하며전부minimum_count=false다. 원격봉인의sources원본은0d998cb…에보존되어있다.

## 최종 방법 반론 — 분모 기준의 사후 강화 공개

SCOPE v1의 원문은 “판별 성공 분모: 사전 두 예측이 갈리고 같은 입력의 후속 증거가 있는 요구 수”다. 정상·경계 두 입력과 A/B 모두의 완결 비교를 명시하지 않았다. 후속을 읽은 뒤 양쪽 입력·경쟁 조작을 모두 요구한 운영은 사후 강화다. 처음 RESULT 초안의 “사전 정의의 엄격 분모0” 표현을 철회하고 원문·원예측을 보존했다. 변경 이유는 최종 별도 문맥 방법검토 C12의 반론이며 영향 행은 M01-P1/P2와 M03-P1/P2다.

| 유지할 해석 | 분모 | 유일 지지 | 양쪽 기각 | 판정불가 | 조건 |
| --- | ---: | ---: | ---: | ---: | --- |
| 사후 완결 비교 | 0 | 0 | 0 | 0 | 두봉인입력·경쟁조작출력까지요구;비율해당없음 |
| 원래 문구를 관대하게 해석 | 1 | 0 | 0 | 1 | M01원예제A의정성R포함;A조작조건부지지와원리유일지지는다름 |
| 조작 수락만으로 확대 | 2 | 0 | 0 | 2 | M01+M03;M03factor동일성불명,같은입력검증으로부르지않음 |

봉인의 넓은3/2/1분류와12행은 유지한다. M02는동률이므로수락되어도판별분모에넣지않는다. M01은P2가이미내부기하에대한B실패를예상해A성공만으로유일지지가생기지않는다.0/1과0/2는실패율·효과없음의증거가아니다. outcomes에원문관대해석및조작수락의명시적case_member필드를추가하고, 기존strict_pair_denominator_member=false값은사후완결비교에해당함을명시했다. 같은집계가E01/E02/현행판제외감도에서도유지되고,불변최초본문필터에서는모두0이다.
