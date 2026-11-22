# scikit-learn 후속 판독과 반증

선정 원격 봉인은 994e21aaea7c5da0c4322db9d1ce2c4f52fa6a2f이다. 이 파일은 봉인 뒤 읽은 결과이며 frame.csv·selection.json의 당시 판정을 덮어쓰지 않는다. 선정 당시 N-S2의 초기 코드 미확인 표시는 보존한다. 이후 review1233732288의 원래 head d5a1cbaf23a471e0c87ddad123a22f85fd104932를 복구하여 구체적 구현이 있었다는 점을 확인했다. 다만 최초 업로드 SHA를 별도 플랫폼 기록으로 고정하지는 못했다.

## 첫 링크가 곧 설계 변경의 원인이 되는가

자연층 4건에서는 적격 리뷰 선례 링크를 확인하지 못했다. 추가층 2건에서는 링크 뒤 같은 목적의 실제 패치가 발견되지만, 첫 링크를 원 작성자의 명시적 연결 발언과 완결된 시험·반영까지 잇는 엄격 사슬은 0건이다. 이는 링크가 효과가 없었다는 추정이 아니다. 공개 원문이 첫 링크의 독립적인 기여와 작업시간을 분리해 주지 않는다는 판정이다.

| 슬롯 | 링크 직전 선택과 이후 변경 | 첫 링크 연결을 약화시키는 원문 |
|---|---|---|
| N-S1 #25265 | validate_params를 처음부터 사용. 이후 유지보수자가 빈 줄만 삭제. | [초기 a5d94d](https://github.com/scikit-learn/scikit-learn/commit/a5d94d234de3bb73ad262ca707a43b4161b7fe3c), [564cdae](https://github.com/scikit-learn/scikit-learn/commit/564cdae490d1a123144052db0bd75fbddd1adcb5), [선행 이슈24862 Steps](https://github.com/scikit-learn/scikit-learn/issues/24862). 공통 부품은 리뷰 전 선택되어 있었다. |
| N-S2 #25268 | check_is_fitted와 whitelist 10개 제거를 원 리뷰 head에서 복구. 닫히기 전 후속 패치는 미복구. | [review1233732288](https://github.com/scikit-learn/scikit-learn/pull/25268#pullrequestreview-1233732288)는 changelog 요청. 현재 commits=[]는 무작업의 증거가 아니다. |
| N-S3 #25269 | 초기 입력검증 유지. 유지보수자가 공통 시험의 wrapper 매핑만 삭제. | [fa3c1cb](https://github.com/scikit-learn/scikit-learn/commit/fa3c1cb6ba3a1504c87d17cede4ec4a602e924c8). 작성자 교체와 시험 등록 수정을 설계자의 선례 채택으로 합치지 않는다. |
| N-S4 #25274 | 수치 DataFrame 허용·문자열 혼합 거절은 첫 패치에 완성되어 있다. 뒤 수정은 PR 번호/문구. | [초기 1e55ead](https://github.com/scikit-learn/scikit-learn/commit/1e55ead018c0230f6d1c10b471b6d73d47092bf6), [review1234551573](https://github.com/scikit-learn/scikit-learn/pull/25274#pullrequestreview-1234551573). [선행 이슈19905](https://github.com/scikit-learn/scikit-learn/issues/19905)의 문자열 지원 기대와 최종 거절 동작도 구별한다. |
| L-S1 #25535 | a897a34 testing helper는 미지원 입력 예외를 xfail 처리. 첫 링크는 외부 엔진 시험 워크플로. 이후 fcharras가 feaabb7e에서 예외/xfail 제거. | [첫 댓글1422865990](https://github.com/scikit-learn/scikit-learn/pull/25535#issuecomment-1422865990), [feaabb7e](https://github.com/scikit-learn/scikit-learn/commit/feaabb7e6f2ccecced7a6847a267ad54b026f8a3). 수정자는 원 PR 작성자 ogrisel이 아니며, [후속25605](https://github.com/scikit-learn/scikit-learn/pull/25605)는 미병합. 원 작성자 후기 패치는 강제 push 때문에 미확인이다. |
| L-S2 #25540 | const floating을 구체 DOUBLE_t로 변경한 eb6a658b가 같은 작성자에게서 확인되고 최종 병합에도 남는다. | [사전 실패1416766187](https://github.com/scikit-learn/scikit-learn/pull/25540#issuecomment-1416766187), [감사1416936430](https://github.com/scikit-learn/scikit-learn/pull/25540#issuecomment-1416936430), [작성자 caller 분석1418381186](https://github.com/scikit-learn/scikit-learn/pull/25540#issuecomment-1418381186), [eb6a658b](https://github.com/scikit-learn/scikit-learn/commit/eb6a658b0ada3464e0fa79da716f57af053141fe). 감사는 열람·최초 발견·수정 원인 진술과 같지 않다. |

### 같은 PR 안에서 더 강한 사슬과 무링크 수정이 모두 보인다

L-S2의 두 번째 Cython 이슈 [5243](https://github.com/cython/cython/issues/5243)는 [review1285216537](https://github.com/scikit-learn/scikit-learn/pull/25540#pullrequestreview-1285216537)에서 n_classes 생성자에 ndarray를 유지하라는 이유로 제시됐다. 작성자는 [1097398366](https://github.com/scikit-learn/scikit-learn/pull/25540#discussion_r1097398366)에서 동의하고 [a1dbdc](https://github.com/scikit-learn/scikit-learn/commit/a1dbdc1d8aa1060f60bae2ddd8b7423e0288d33f)에서 실제로 되돌렸다. 이 더 명확한 사건을 첫 Cython5230 링크 대신 선택하면 성공 사례를 사후 선별하게 된다. 따라서 첫 사건의 엄격 분자는 늘리지 않는다.

그 뒤 thomasjpfan은 [review1289640474/1100444710](https://github.com/scikit-learn/scikit-learn/pull/25540#discussion_r1100444710)에서 PyArray API가 직접 ndarray를 다루도록 설계됐다고 설명했다. 이 설명에는 새로운 선례 URL이 없다. 작성자는 [e7e806](https://github.com/scikit-learn/scikit-learn/commit/e7e806bfe356d1ca62e26735b9136571efb318c4)에서 두 반환 함수의 ndarray를 복원하고 [1100471666](https://github.com/scikit-learn/scikit-learn/pull/25540#discussion_r1100471666)에서 컴파일 확인을 보고했다. 링크를 제공하는 기능과 정확한 맥락 설명을 제공하는 기능은 이 관측에서 분리되어야 한다.

첫 참고 이슈 [Cython5230](https://github.com/cython/cython/issues/5230)의 재현은 NumPy 사용자 정의 fused type과 const memoryview의 컴파일 실패다. 최초 TreeBuilder 댓글의 dispatch signature 실패와 구체적인 오류 경로가 동일하다고 증명되지 않았다. 함께 링크된 [HackMD 노트](https://hackmd.io/FR4Vp_OgR-WhlVEsVZzsIw/download)는 현재 본문을 읽었지만 2023-02-04 판이 없다. 현재 노트의 표현을 그때 이미 전달된 지식으로 소급하지 않는다.

## 사람 시간과 비용의 경계

| 기록 | 관측 단위 | 허용되는 해석 | 허용되지 않는 해석 |
|---|---|---|---|
| L-S2 첫 링크 2023-02-04 17:13:52 → 첫 관련 git committer date 2023-02-06 07:55:24 | 139,292초의 경과 | 토요일부터 월요일까지의 달력 간격. 원 작성자 리뷰로 공개 패치가 관측되는 상한 07:57:51까지는 139,439초. | 38시간 41분의 노동, 링크가 아낀 시간, CI 대기시간. |
| L-S2 17개 surviving commits 중 첫 링크 뒤 16개 | 커밋 16개: 일반 패치13+merge3; 실제 변경 파일3개 | 반복 수정 산출물이 존재. | 13회 사람 작업 세션 또는 고정 시간 환산. |
| L-S1 작성자 2023-02-03 시험 보고 | 6.31초의 기계 시험 실행, 15 failed/27 passed 등 | 첫 링크 이전에 실패와 수정 필요를 알고 있었다. | 사람의 직접 작업시간 6.31초. [댓글1416034432](https://github.com/scikit-learn/scikit-learn/pull/25535#issuecomment-1416034432). |
| N-S4 선행 소비자 2022-12-30 보고 | 비수치 자기보고 many hours | 실제 사용자가 DataFrame 실패를 디버깅하는 비용을 호소했다. | 원 PR 작성자의 수정시간, 첫 공개 이후 관측창 노동, 정확한 시간 수치. [issue25261 Describe the bug](https://github.com/scikit-learn/scikit-learn/issues/25261). |
| Cython5230 유지보수자의 weekend 계획 | 미래 작업 계획 | 수정 의향. | 실제 소요시간 또는 작업 완료. [1405427210](https://github.com/cython/cython/issues/5230#issuecomment-1405427210). |

직접 시작/중지 로그, 표본 작성자의 수치 소요시간 자기보고, 동일 품질의 무링크 시간 비교는 각각 0/6이다. 실제 사람 시간은 미확인이다. 비교 가능한 쌍을 분모로 하는 절감률은 0/0이므로 해당 없음이다. 절감량을 0으로 대체하지 않는다. 최소 추가 기록은 첫 실패/요구·직전 판, 첫 자료 노출 시각과 기존 인지 여부, 수정 구간별 실제 시작/중지와 중단 사유, 구현자 구분, 같은 회귀 입력/기대 출력의 전후 통과, 동일 난이도·동일 품질의 무링크 과제 시간을 한 묶음으로 남기는 것이다.

## 관측창·작성자·선행 수정 감도

자연 4건과 L-S2는 모두 5일 안에 종결되어 30/60/90일 절단 변경으로 표본 내 결과가 바뀌지 않는다. L-S1은 각각 2023-03-05/04-04/05-04 14:18:47Z에 끝난다. 첫 링크와 다른 작성자의 feaabb7e는 30일 안에 있어 확인된 링크2건, 같은 작성자 변경1건+미확인1건, 타인 포함 변경2건, 엄격 사슬0건은 세 창에서 동일하다. 이는 강제 push로 잃은 코드를 되찾았다는 뜻이 아니다.

N-S4는 PR API merged_at/closed_at가 2023-01-03 15:46:22Z이고 timeline closed가 15:46:23Z다. 1초를 바꿔도 사건 분류는 같다. reopen은 6개 공개 timeline에서 확인되지 않았다.

같은 작성자만 인정하면 추가층 변경은 확인1/2, 미확인1/2다. 다른 작성자까지 포함하면 확인2/2다. L-S1의 패치는 여전히 미병합 브랜치 수정이고 엄격 인과/노동 사슬은 0/2다. 이를 원 작성자가 자료를 읽고 고쳤다는 2/2로 바꾸면 안 된다.

첫 링크 전에 같은 구체적 후속 패치가 이미 올라왔다는 증거는 두 추가층 사건에서 확보하지 못했다. L-S2에는 첫 링크 전 사전 실패, L-S1에는 엔진 시험 관련 사전 수정·green 보고가 있다. 구체 패치 선행을 확인한 사례만 제외하는 좁은 감도에서는 제외0/2, 결과 동일이다. '이미 문제를 알고 넓은 수정 작업이 진행 중인 사건'까지 배제하는 넓은 감도에서는 두 사건이 모두 빠져 분모0, 조건부 비율은 해당 없음이다. 이 두 제외 규칙을 섞지 않는다.

### 첫 종결 이후의 두 후기

N-S2 원 PR은 2023-01-04 22:30:46Z 닫혔다. 같은 작성자는 22:52:31Z에 [PR25294](https://github.com/scikit-learn/scikit-learn/pull/25294)를 만들고 [1371521054](https://github.com/scikit-learn/scikit-learn/pull/25294#issuecomment-1371521054)에서 이전 PR의 실수와 changelog 추가를 설명했다. [35b5ee](https://github.com/scikit-learn/scikit-learn/commit/35b5ee65770ee7fb7bf15d0acb2ee96d7d3bf1ab)는 같은 기능과 시험을 병합했다. 이는 닫힌 PR을 작업 포기로 단정하는 반례다. 원 관측창과 첫 선례 링크 분자는 바꾸지 않는다.

L-S2는 2023-02-09 병합 뒤 [25584](https://github.com/scikit-learn/scikit-learn/issues/25584)의 read-only 역직렬화 문제가 나왔다. [25585](https://github.com/scikit-learn/scikit-learn/pull/25585)의 실제 패치는 cnp.PyArray_DATA로 바뀌고 joblib mmap_mode='r' 회귀시험을 추가했다. 초안 본문의 const 계획과 최종 구현이 다르다. 첫 병합을 같은 품질의 완료 또는 절감의 증거로 삼기 어려운 후기이며, PR25540의 관측창을 임의로 늘려 본분자에 합치지 않는다.

## 세 관점과 적용 조건

링크 제공자는 발견한 제한과 재현 가능한 예제를 전달한다. Vincent의 두 Cython 링크는 서로 다른 실패를 다루며, fcharras의 워크플로는 외부 엔진이 공통 시험을 돌리는 실무 맥락을 제공한다. 수정자는 caller의 실제 타입, 기존 지원 범위, public ndarray 계약을 유지해야 한다. 따라서 예제에 나온 표면 형태를 그대로 적용하는 것이 목적이 아니다. 결과 소비자는 joblib read-only 버퍼, 수치 DataFrame, sparse/dense fit/predict 등 실제 입력 조합이 유지되는지에 영향을 받는다. [betatim1429734094](https://github.com/scikit-learn/scikit-learn/pull/25535#issuecomment-1429734094)는 일부 외부 엔진의 제약과 scikit-learn의 합리적인 기본 사용을 구별한다.

탐색기에게 이 자료가 지지하는 제품 표현은 '같은 목적의 선례와 적용 제약을 원문으로 찾게 돕는다'까지다. 일부 공개 리뷰 뒤 실제 수정이 있었다고 사례별로 말할 수 있지만, 첫 선례 링크가 원 작성자의 변경을 일으켰다거나 노동을 절감했다는 일반 수치는 이 표본에서 추정할 수 없다.

## 판독 오염·복구 제한과 재개 지점

선정 전 L-S1의 URL 필터가 90일 뒤인 9월 reviewer의 branch/force-push 상태를 노출했다. 선택 전 완전한 결과 가림은 충족되지 않는다. 자연 rank9 #25275의 9월 surviving patch와 rank7 #25272의 개설 다음 날 committer 판도 초기판으로 고정할 수 없다. 후자는 시험 seed만 바꾼 패치이지만 최초 공개 diff를 직접 증명하는 제외 근거가 되지는 못한다. 이 행은 screening-attempts.jsonl에서 명시했고 원 슬롯을 교체하지 않았다. 재개 첫 자료는 #25272 개설 당시 GitHub push event/head archive 또는 당시 로컬 git reflog다. 기존 review1234637508의 head be3bdde4만으로 1월2일 최초 head는 복구되지 않았다.

이 stream의 판독은 AI 연구자의 자체 판독이다. root의 L-S2 교차 재열람 역시 같은 실행 계열의 별도 AI 판독이며 외부 독립 인간 판독으로 표현하지 않는다. 별도 음악/지도 사례는 다른 담당 stream에서 결합된다.
