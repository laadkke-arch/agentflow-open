# 최종 공간 사례 비판 재판독

- 검토자: 같은 모델의 별도 작업 문맥인 `/root/spatial_donors`. 외부 독립 심사자나 독립 실험이 아니다.
- 대상: 2026-11-22T22:45:47Z에 읽은 작업 트리의 `RESULT.md` 표1 M01–M03, 표2 및 관련 해석·집계; 아래 행 번호는 그 판의 번호다.
- 검토 종료 확인 UTC: 2026-11-22 22:50:09 UTC.
- 공유 결과·봉인 CSV·재현 스크립트는 수정하지 않았다. 이 검토 파일만 작성했다.

## 결론

**공간 사례의 엄격 지지0, M01 미확인, M02 판별불가, M03 미확인 판정은 근거 범위와 맞는다.** 원래 사례의 관측 부족을 다른 후속 코드·시험으로 채운 오류는 현재 표에서 발견하지 못했다.

필요한 본문 수정은 아래 **F1 한 건**이다. F2는 정적 코드 추론의 연결 위치를 더 정확히 하는 보강이다. 현재 코드의 실행을 막는 확정적 오류는 정적 판독에서 발견하지 못했다. 다만 과거 환경은 해결·실행하지 않았으므로 런타임 실행 가능성은 계속 미확인이다.

## F1 — 목적 변경 때 B 전체를 추천한다는 문구는 좁혀야 함

**위치:** 검토판 `RESULT.md` L80의 “M03을 중앙 설명이 아니라 실제 값.5의 주석으로 바꾸면 추천은 B로 뒤집힌다”, 그리고 같은 의미를 반복한 카드·해석이 있으면 그 문구.

**근거:** [3.0.2 colorbar.py](https://github.com/matplotlib/matplotlib/blob/8858a0d1bdd149a0897789e8503ac586be14676d/lib/matplotlib/colorbar.py#L984-L1014) L1001–1003은 일반 자동 colorbar locator 경로에서 **y뿐 아니라 x도** `norm.inverse`로 바꾼다. 따라서 “값.5 위치를 표시한다”는 목적이 수직 위치를 뜻하더라도, 봉인 B의 기본 `text(.5,.5)`는 x까지 data 좌표에 고정한다. 이를 그대로 추천하면 colorbar 가로 중앙을 잃을 수 있다.

**최소 수정안:** “목적을 실제 값.5의 주석으로 바꾸면 B의 **y를 data값에 결부시키는 논리**는 적합할 수 있다. 가로 중앙을 함께 요구한다면 x는 별도 axes 좌표 또는 혼합 transform으로 처리해야 하므로 봉인 B 전체의 우위가 확인된 것은 아니다.”

**영향:** 목적 변경 감도의 해석만 좁힌다. 표1 지지 수·엄격 분모·봉인 예측을 바꾸지 않는다. 원래 요구가 실제로 바뀌었다고 주장하지 않는다.

## F2 — 2.2.2 정규화 좌표 추론의 위치 보강

검토판 L91은 “일수 있어”, “정적판독”으로 한정하므로 실제 실행으로 과장하지 않는다. 고정 SHA의 release message도2.2.2라는 판 표기를 지지한다.

다만 [_mesh L843–861](https://github.com/matplotlib/matplotlib/blob/b471ee21cbe0d0fdd9cf5142d0a4be01517f4e68/lib/matplotlib/colorbar.py#L843-L861)만 제시하기보다 다음 두 위치를 함께 연결하면 mesh에서 axes까지의 대응이 명확해진다.

- [_uniform_y L779–785](https://github.com/matplotlib/matplotlib/blob/b471ee21cbe0d0fdd9cf5142d0a4be01517f4e68/lib/matplotlib/colorbar.py#L779-L785): extension 없는 uniform 구간.
- [_config_axes L430–440](https://github.com/matplotlib/matplotlib/blob/b471ee21cbe0d0fdd9cf5142d0a4be01517f4e68/lib/matplotlib/colorbar.py#L430-L440): outline의 dataLim을 axes limits로 옮김.

판 변화로 추천 차이가 사라질 수 있다는 추론은 **원문의 일반 vertical·uniform·unextended 조건을 둔 정적 해석**으로 유지해야 한다. 모든 norm·extension에 대한 실행 보장으로 확대하지 않는다.

## 통과한 핵심 사항

| 점검 | 판정과 이유 |
| --- | --- |
| M01의 예측 대립 | L8·24·63은 다른 조작과 반대 출력 예측을 구별한다. P2 자체의 내부 기하 실패 예상도 보존한다. A 성공으로 P2 기각 또는 유일 지지를 주장하지 않는다. |
| M01 후속 시험 |1355 시험은 관련 지도 입력이라고 표시되며 원래 빈 axes 첫/둘째 저장 시험으로 승격하지 않는다.1370은 제3조작의 철회다. |
| M02 같은 후보 적합 | 두 후보가 조건부 B를 같이 권한다는 사실을 보존한다. 수락 댓글을10/30개 bbox의 각각의 측정으로 바꾸지 않는다. |
| M02 동작 구분 | layout 제외와 drawing 생략이 분리돼 있다. 범례 없는 기준은 별도의 연구자 대조다. |
| M03 후속 시험 | 직접 다시 읽은13603의 `test_collapsed` L313–327은 annotation·경고·폭·rect를 검사한다. colorbar/factor/anchor를 검사하지 않으므로 현재 표의 “별도 crash” 분리는 맞다. |
| M03 수락·최초판 |470159527은 text 조언 수락과 None 오류를 분리한다.470135635는 제목만 먼저 제출했음을 확인한다. 현재 첫 본문을 불변 최초판으로 쓰지 않는 해석은 타당하다. |
| 표1 행 수 | 검토판은12행이며 미확인7·판별불가5다. 공간6행은 미확인4·판별불가2다. 정성 수락을 엄격 지지로 더하지 않았다. |
| 엄격 분모0 | 전체 정상/경계·같은 조작·목적에 맞춘 후속 비교가 없다는 정의 아래 공간 사례가 분모를 늘리지 않는다. 비율은 해당 없음으로 처리한다. |
| 시각·판 | 공간 최초 후속 열람22:20:03Z는 봉인22:19:23Z 뒤다.1370철회2019-12-31,1355merge2020-07-01,3.0.2/2.2.2 SHA표기는 이번 판독과 기존 원장에 양립한다. |
| 비용 비교 |1956의638ms/2.37ms는 해당 큰 pcolormesh의 작성자 보고로 제한하고 M01의 실행 시간으로 쓰지 않는다. |
| 원전 위치 | InDesign PDF300–301 anchored objects/657–658 preflight, CSS§8.2, Maplex/QGIS 절은 앞선 직접 공간 원전 판독과 일치한다. 이번에 원전을 새로 네트워크로 연 것은 아니다. |

## 재현 스크립트 정적 판독

검토 대상은 `probe_common.py`, `m01_first_save.py`, `m02_legend.py`, `m03_colorbar.py`의 현재 로컬 내용이다. 이번 검토에서 스크립트를 실행하거나 plotting library를 import하지 않았다. 앞서 기록한 Python3.6 문법 검사도 실행 호환성의 보증이 아니다.

- M01은 계측으로 `get_position()`을 호출하지 않으며 explicit pre-draw는 A에만 있다. B는 Pillow affine 변환을 실제 수행하도록 작성되어 있다. 첫·둘째 export, 외부 raster 결과, 기하 모형 bbox가 분리되어 있다.
- M02는 동일 seed 데이터로 A/B/no-artist reference를 만들고 B에서만 `set_in_layout(False)`를 호출한다. figure/font 조건을 바꾸는 자동 수선은 없다. layout 예외면 export를 중단한다.
- M03은 실제 colorbar x/y limits와 변환된 anchor를 각각 저장한다.2.2.2와3.0.2를 명시적으로 검사하고 None crash를 고치지 않는다.
- 공통 기록 helper는 Agg와 버전을 확인하고 결과 경로를 소유 경로에 제한한다. 수동 bbox 필드에 값을 대입하지 않는다.
- Pillow6.2.2 affine·Matplotlib 과거 binary·Cartopy 의존성을 실제 import/run하지 않았으므로 “실행 가능 확인”이라는 상태로 올릴 수 없다. 현재 README와 PREPARATION_STATUS는 이 한계를 명시한다. 확정적 실행 불가 오류는 이번 정적 범위에서 찾지 못했다.

## 읽기 구분

**기존 로컬·대화 문맥의 판독:** 봉인 requests/predictions와 공간 원전 자료, `matplotlib12-outcomes.json`/출처 원장, 기존 preseal 검토. 이번에 네트워크에서 다시 열지 않은 원전은 새 열람으로 세지 않는다.

**이번에 새 네트워크로 직접 연 주소:** 아래8행이다. 모두 이미 연구한 저작의 재방문/메타데이터 확인으로 `minimum_count:false`다. 부모가 sources.jsonl에 추가할 수 있도록 행별 URL·SHA·UTC·위치를 포함한다. 최소 고유 원문 배당은 늘어나지 않는다. GitHub ref 응답은 annotated tag를 가리키며 이번에는 tag object를 peel하지 않았다. fixed commit의 release message 확인은 별도 행에 기록했다.

```jsonl
{"phase":"post-seal final same-model review","minimum_count":false,"allocation":null,"questions":["Q5","Q6","Q7"],"publication_date":null,"duplicate_relation":"revisit/context only; no new unique work allocation","source_id":"SPREV-302-CODE","work_id":"MPL-3.0.2-SOURCE","edition_id":"fixed historical source / current API metadata","url":"https://raw.githubusercontent.com/matplotlib/matplotlib/8858a0d1bdd149a0897789e8503ac586be14676d/lib/matplotlib/colorbar.py","final_url":"https://raw.githubusercontent.com/matplotlib/matplotlib/8858a0d1bdd149a0897789e8503ac586be14676d/lib/matplotlib/colorbar.py","publisher":"Matplotlib project / GitHub","kind":"primary-source reread","checked_utc":"2026-11-22T22:46:14.736735Z","locator":"L510–518;604–615;984–1014, especially1001–1003","confirmed":"For auto colorbar locator the fixed implementation inverse-transforms both y and x; _config_axes sets both limits from outline dataLim.","limitations":"Static inspection only. Actual per-input limits and rendering were not executed. Qualifies y-anchoring recommendation; does not prove full default(.5,.5) is the appropriate datum annotation.","cases":["M03"],"fixed_sha":"8858a0d1bdd149a0897789e8503ac586be14676d"}
{"phase":"post-seal final same-model review","minimum_count":false,"allocation":null,"questions":["Q5","Q6","Q7"],"publication_date":null,"duplicate_relation":"revisit/context only; no new unique work allocation","source_id":"SPREV-222-CODE","work_id":"MPL-2.2.2-SOURCE","edition_id":"fixed historical source / current API metadata","url":"https://raw.githubusercontent.com/matplotlib/matplotlib/b471ee21cbe0d0fdd9cf5142d0a4be01517f4e68/lib/matplotlib/colorbar.py","final_url":"https://raw.githubusercontent.com/matplotlib/matplotlib/b471ee21cbe0d0fdd9cf5142d0a4be01517f4e68/lib/matplotlib/colorbar.py","publisher":"Matplotlib project / GitHub","kind":"primary-source reread","checked_utc":"2026-11-22T22:47:37.713097Z","locator":"_config_axes L430–440; _uniform_y L779–785; _mesh L843–861","confirmed":"Fixed version's unextended uniform mesh uses0..1; axes limits follow mesh outline. This supports a qualified version-dependent coordinate inference.","limitations":"First request22:46:20.010563Z; focused reread22:47:37.713097Z. No historical binary run. Conditions include ordinary vertical unextended uniform colorbar, not every norm/extension.","cases":["M03"],"fixed_sha":"b471ee21cbe0d0fdd9cf5142d0a4be01517f4e68","first_read_utc":"2026-11-22T22:46:20.010563Z"}
{"phase":"post-seal final same-model review","minimum_count":false,"allocation":null,"questions":["Q5","Q6","Q7"],"publication_date":null,"duplicate_relation":"revisit/context only; no new unique work allocation","source_id":"SPREV-M03-TEST","work_id":"MPL-PR-13603","edition_id":"fixed historical source / current API metadata","url":"https://raw.githubusercontent.com/matplotlib/matplotlib/f9d8cd7e0c9a4e94962fc925c57fb678ba252f87/lib/matplotlib/tests/test_tightlayout.py","final_url":"https://raw.githubusercontent.com/matplotlib/matplotlib/f9d8cd7e0c9a4e94962fc925c57fb678ba252f87/lib/matplotlib/tests/test_tightlayout.py","publisher":"Matplotlib project / GitHub","kind":"primary-source reread","checked_utc":"2026-11-22T22:46:24.155947Z","locator":"test_collapsed L313–327","confirmed":"Test uses an outlying annotation, warning/unchanged-width assertion, then rect[0,0,.8,.8]; no colorbar/factor/anchor fixture.","limitations":"Static test definition reread, not execution or source of expected M03 anchor outputs.","cases":["M03"],"fixed_sha":"f9d8cd7e0c9a4e94962fc925c57fb678ba252f87"}
{"phase":"post-seal final same-model review","minimum_count":false,"allocation":null,"questions":["Q5","Q6","Q7"],"publication_date":null,"duplicate_relation":"revisit/context only; no new unique work allocation","source_id":"SPREV-M03-COMMENTS","work_id":"MPL-ISSUE-13600","edition_id":"fixed historical source / current API metadata","url":"https://api.github.com/repos/matplotlib/matplotlib/issues/13600/comments?per_page=100","final_url":"https://api.github.com/repos/matplotlib/matplotlib/issues/13600/comments?per_page=100","publisher":"Matplotlib project / GitHub","kind":"primary-source reread","checked_utc":"2026-11-22T22:46:25Z","locator":"comments470135635,470147866,470153183,470159527","confirmed":"Author says initial submission was title-only; maintainer describes units change; axes-transform proposal receives author acceptance while None bug remains separate.","limitations":"Clock checked after comments batch. Qualitative report has no enumerated two-factor anchor measurements. Same issue already allocated as request.","cases":["M03"]}
{"phase":"post-seal final same-model review","minimum_count":false,"allocation":null,"questions":["Q5","Q6","Q7"],"publication_date":null,"duplicate_relation":"revisit/context only; no new unique work allocation","source_id":"SPREV-222-REF","work_id":"MPL-2.2.2-SOURCE","edition_id":"fixed historical source / current API metadata","url":"https://api.github.com/repos/matplotlib/matplotlib/git/ref/tags/v2.2.2","final_url":"https://api.github.com/repos/matplotlib/matplotlib/git/ref/tags/v2.2.2","publisher":"Matplotlib project / GitHub","kind":"primary-source reread","checked_utc":"2026-11-22T22:46:39Z","locator":"ref/object","confirmed":"v2.2.2 ref points to annotated tag40872824c2a5c03960dc67b03c3cce1bc945f50b.","limitations":"Tag object not peeled in this review; version identity additionally checked through fixed commit's release message. No new source count.","cases":["M03"]}
{"phase":"post-seal final same-model review","minimum_count":false,"allocation":null,"questions":["Q5","Q6","Q7"],"publication_date":null,"duplicate_relation":"revisit/context only; no new unique work allocation","source_id":"SPREV-302-REF","work_id":"MPL-3.0.2-SOURCE","edition_id":"fixed historical source / current API metadata","url":"https://api.github.com/repos/matplotlib/matplotlib/git/ref/tags/v3.0.2","final_url":"https://api.github.com/repos/matplotlib/matplotlib/git/ref/tags/v3.0.2","publisher":"Matplotlib project / GitHub","kind":"primary-source reread","checked_utc":"2026-11-22T22:46:39Z","locator":"ref/object","confirmed":"v3.0.2 ref points to annotated tagdb0e78c7a9540f23e12472ff7161d883175f6791.","limitations":"Tag object not peeled in this review; no new source count. Metadata lookup rather than runtime evidence.","cases":["M01","M02","M03"]}
{"phase":"post-seal final same-model review","minimum_count":false,"allocation":null,"questions":["Q5","Q6","Q7"],"publication_date":null,"duplicate_relation":"revisit/context only; no new unique work allocation","source_id":"SPREV-222-COMMIT","work_id":"MPL-2.2.2-SOURCE","edition_id":"fixed historical source / current API metadata","url":"https://api.github.com/repos/matplotlib/matplotlib/commits/b471ee21cbe0d0fdd9cf5142d0a4be01517f4e68","final_url":"https://api.github.com/repos/matplotlib/matplotlib/commits/b471ee21cbe0d0fdd9cf5142d0a4be01517f4e68","publisher":"Matplotlib project / GitHub","kind":"primary-source reread","checked_utc":"2026-11-22T22:46:39Z","locator":"commit.message;commit.committer.date","confirmed":"Fixed commit identifies v2.2.2 LTS; committer timestamp2018-03-17T02:56:24Z.","limitations":"Commit timestamp is not proof of public package availability at that exact second. Used to verify version label only.","cases":["M03"],"changed_date":"2018-03-17T02:56:24Z","fixed_sha":"b471ee21cbe0d0fdd9cf5142d0a4be01517f4e68"}
{"phase":"post-seal final same-model review","minimum_count":false,"allocation":null,"questions":["Q5","Q6","Q7"],"publication_date":null,"duplicate_relation":"revisit/context only; no new unique work allocation","source_id":"SPREV-302-COMMIT","work_id":"MPL-3.0.2-SOURCE","edition_id":"fixed historical source / current API metadata","url":"https://api.github.com/repos/matplotlib/matplotlib/commits/8858a0d1bdd149a0897789e8503ac586be14676d","final_url":"https://api.github.com/repos/matplotlib/matplotlib/commits/8858a0d1bdd149a0897789e8503ac586be14676d","publisher":"Matplotlib project / GitHub","kind":"primary-source reread","checked_utc":"2026-11-22T22:46:39Z","locator":"commit.message;commit.committer.date","confirmed":"Fixed commit identifies v3.0.2; committer timestamp2018-11-10T01:06:33Z.","limitations":"Commit timestamp is not proof of public package availability at that exact second. No runtime evidence.","cases":["M01","M02","M03"],"changed_date":"2018-11-10T01:06:33Z","fixed_sha":"8858a0d1bdd149a0897789e8503ac586be14676d"}
```

