# AF-RES-046 · 원장 단위와 판정값

## 단위

- `frame.csv`의 한 행은 검색 원장에 열거된 PR 하나다. 두 저장소×두 기간×40=160행이며 160개를 같은 깊이로 읽었다는 뜻이 아니다. `screened_content`, `status`, `reason`을 같이 읽는다.
- `slot_id`는 선택 또는 잠정 선택한12개의 분석 자리다. N-P/N-S는 자연층, L-P/L-S는 링크 우선층이다. 관련 선행 이슈, 참고 PR, 대체 PR, 회귀 PR은 이 슬롯의 근거이며 새 표본 PR로 늘리지 않는다.
- `baselines.csv`의 한 행은 슬롯의 요구·링크 전 선택이다. 가장 이른 살아 있는 git commit, 원 리뷰가 고정한 head, PR 개설 순간 head는 다르다. `base_parent`는 commit의 부모이며 원 PR의 base SHA와 자동으로 같지 않다.
- `events.csv`의 한 행은 분석에 관련된 발행 사건/commit 기록이다. 일반 댓글·inline·review·commit의 단위를 구별한다. 전체 API 레코드 수와 주요 분석 사건 수를 혼동하지 않는다.
- `changes.csv`는 실제 비교한 patch 또는 변경 없음/미확인 관측이다. 하나의 PR에 여러 행이 있을 수 있다. `labor.csv`는 시간/횟수/파일 수/결측 기록이며 역시 PR 수가 아니다.
- `sources.jsonl`은 직접 의미 판독한 자료·재방문·접근 실패 영수증이다. `work_id`가 독립 저작, `edition_id`가 판이다. 같은 PR 본문/일반댓글, 같은 review 안의 여러 inline, 같은 commit의 여러 파일, 같은 지도 객체의 여러 버전은 보수적으로 한 저작이다.

## 수치와 결측

- `true`/`confirmed`는 해당 자료가 요건을 직접 뒷받침한다는 판정이다. 추정·시간 순서만으로 원인이나 읽음을 채우지 않는다.
- `false`/`not_observed`는 명시적으로 정의한 관측 기준을 충족한 근거가 없다는 뜻일 수 있다. 연구 결과에서는 실제 행동 부재와 구분해 적는다.
- `unknown`/`미확인`은 필요한 판·발언·시간·비교가 없거나 접근하지 못했다는 뜻이다. 수치0으로 바꾸지 않는다.
- `해당 없음`은 조건부 분모가 실제0일 때 사용한다. 자연층에서 적격 리뷰 링크0이면 그 링크에 대한 명시 읽음 비율은0/0%가 아니라 해당 없음이다.
- `author_read_explicit`는 작성자가 해당 자료를 읽었다고 명시한 경우다. URL 인용·감사·답변을 별도 수용/반응 증거로 보존하되 같은 값으로 승격하지 않는다. `already_known`도 명시 발언과 선행 본인 구현이라는 추론을 구분한다.
- `same_author_change_after_link`는 첫 적격 URL 뒤에 같은 작성자와 같은 요구를 연결하는 실제 patch 관측이다. 원 PR 밖의 후속 PR도 같은 요구·작성자·관측창이면 포함할 수 있다. 무링크 PR의 일반 수정은 별도 관찰 대조다.
- `strict_chain`은 사전 SCOPE의 모든 고리를 충족한 주 사건이다. 더 선명한 후속 URL로 첫 URL을 바꾸지 않는다. 미확인 고리가 있으면 엄격 관측 분자에 넣지 않는다.

## 시간

Git `author_date`/`committer_date`, 플랫폼 review `submitted_at`, 댓글 `created_at`, PR 생성·최초 종결을 별도 원천으로 둔다. 부모 관계·review의 commit_id는 판의 관계를 고정하지만 git 날짜는 공개 push 시각을 입증하지 않는다. `public_anchor`는 그 시점에는 해당 판이 공개됐다는 관측이며 실제 첫 공개 순간과 같지 않다.

주창은 생성부터 최초 종결 또는90일 중 이른 시각이다.30/60/90일 감도에서도 원래 PR 슬롯을 유지한다. 종결 뒤 병합된 대체 PR, 회귀 보고, 되돌림은 후기다. 링크가 주창 밖이면 링크 없음으로 오해시키지 않고 창 밖 링크로 명시한다.

`direct_work_time`은 시작·중지·행위자·작업범위가 있는 사람 활동 기록, `self_reported_time`은 당사자 소요시간 진술, `elapsed`는 두 시각 차다. 성능 benchmark의 초, CI 실행시간, commit 수, 파일 수, 주말 여부는 사람 노동시간이 아니다. 다른 사람이 대신 구현한 시간도 원 작성자의 수정시간으로 옮기지 않는다.

## 배당과 재현

최소 원문 배당은 PR 원 제안/구현8, 별도 설계 리뷰5, commit/시험6, 선례 원대상3, 타 분야 원장/규칙4이다. 한 저작은 한 배당에만 사용한다. 직접 읽은 관련 여분 저작은 따로 집계한다. 재방문, 같은 저작의 다른 판·미러, 검색요약·접근 실패는 최소수에 추가하지 않는다.

통합 원장은 `stream`/`stream_record`로 분담 원장에 연결한다. 통합 과정에서 줄바꿈·별칭 필드만 정규화하며 의미 판정 수정은 감사/REVISIONS에 근거를 남긴다. frozen선정 원장과 후속 관측으로 갱신한 원장을 Git 이력에서 구분할 수 있다. CSV 출력은 LF로 통일하며 첫 봉인의 실제 Git 바이트 해시는 `evidence/selection-freeze-normalization.json`에 별도로 보존했다.

코드 검산은 원장 조인·분모·시각산술·표행·출처 중복을 확인한다. 당시 제품 실행, 실제 사용자·사람 노동 재현, 외부 인간 독립 판독을 뜻하지 않는다.


## 후속 통합과 날짜 의미

`cases.json`은 고정된12슬롯의 판정을 정규화한다. `same_author_same_purpose_change=null`은 링크 없음 또는 실제 패치 미복구를 뜻하므로 `same_author_change_status`와 함께 읽는다. 자연층의 링크 뒤 변경 조건부 분모는0이며 해당 없음이다. 자연층에서 수정 자체가 없었다는 뜻이 아니다.

`prelink_same_author_redesign_confirmed`는 L-P2만, `prelink_any_author_same_purpose_implementation_confirmed`는 L-P1/L-P2다. L-S1/L-S2의 기존 문제·실패·넓은 작업과 특정 후속 교정의 선행 구현을 구별한다. 타인 포함4/4는 같은 작성자의 채택률이 아니며, L-P1에서는 이미 시작한 다른 구현의 계속 작업을 포함한다.

`changes.csv`, `labor.csv`는 stream별 열을 손실 없이 합집합으로 보존한다. 비어 있는 다른 stream의 열은0으로 해석하지 않는다. 공통키는 `slot_id`, 원행은 `stream_file`/`stream_record`다. pandas `sha/source_id`와 sklearn `post_sha/source_ids`, pandas `elapsed_seconds`와 sklearn `elapsed_observation_seconds`는 같은 역할의 열이다. 패치 수의 anchor는 stream별 명시된 기준을 사용하며 한 번의 사람 작업 세션으로 바꾸지 않는다.

`sources.jsonl`은 sources, supplement, additional, screening-attempts, crossdomain attempts를 모두 합친다. 검색·실패·부분 판독·재방문도 영수증에 들어가지만 최소수에 추가되지 않는다. `source_id`가 없던 시도는 `ATT-<attempt_id>`로 표시한다. 검색 시도에는 원문 URL 대신 query만 있을 수 있다. 최초 조회 UTC를 보존하지 못한 경우 null과 정밀도 설명을 유지하고 기록 UTC를 소급 조회시각으로 바꾸지 않는다.

Git object의 stream `published_at`/`modified_at`는 실제로 git author/committer 날짜일 수 있다. root는 이를 `git_author_date_from_stream`/`git_committer_date_from_stream`으로 분리하고 `published_at`를 null로 둔다. 실제 공개 관측은 events의 리뷰·PR·merge 시각으로 보며, 해당 시각까지 공개돼 있었다는 상한이다. 최초 push 시각이나 노동 시작 시각을 뜻하지 않는다.

`sensitivity.csv`의36행은12슬롯×30/60/90일이다. `evidence/statistics.json`은 사례 분모·동일인/타인·선행착수 제외 집계를 재계산한다. `synthesize.py`→`assemble.py --stage all` 순서로 재생성한다. 원 선정은994e21a 커밋에 남고 current frame의 `frozen_*` 열에 당시 상태를 보존한다.
