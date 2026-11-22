# AF-RES-044 최종 수치·경로 감사

- 확인 시각: 2026-11-22T21:18:08Z 이후의 아래 해시 스냅샷.
- 감사자: Vega lane 작성 에이전트. 같은 연구 팀의 자체 점검이며, 원문 판정을 숨긴 독립 외부 평정이 아니다.
- 작업 HEAD: `8c22675a2e90134c386f362cdd2aabe7d14d252e`. 이 문서는 묶음 3 직전 작업 파일을 검산한 receipt이며, 최종 결과 커밋의 식별은 루트의 인계서가 담당한다.
- 방법: 생산 계산기를 다시 실행하지 않고, 입력 파일을 읽는 별도 Python 세트·합계 연산으로 그룹, 대표, atom/subcondition 결합, 개별 시행의 증거 허용, 분모 교집합, 최대값과 witness를 재구성했다. 원자료·루트 코드·판정은 수정하지 않았다.
- 결론: 아래 범위의 계산 불일치는 0건이다. 확인 중 발견한 `semantic_read_scope_count` 13행 오류는 루트가 수정했고 재검산했다. 표집·미관측·양성 대조의 수용 문제까지 통과했다는 뜻은 아니다.

## 1. 원풀·그룹·표시 입력

| 확인 단위 | 검산 결과 | 근거와 해석 |
|---|---:|---|
| 원풀 슬롯 | 72 = 자연 48 + 보강 24 | `pool.csv`의 각 요구 ID에 rank 1~6이 한 번씩 있으며, A/B/C에 같은 후보 ID 순서를 입력한다. |
| 비어 있지 않은 슬롯 / URL / 독립 문서 주소 | 41 / 41 / 22 | 문서 주소는 fragment를 제거한 URL이다. 이는 출처 산입 수와 다른 단위다. |
| P1~P4 미관측 | 24슬롯 | `empty_kind=unobserved`; 수집 실패로 미관측인 풀이다. 대안이 0개인 풀로 계산하지 않는다. |
| V1~V4 실제 부족 | 7슬롯 | `empty_kind=exhausted_scope`; 고정 범주 안에서 자연 href를 다 소진한 빈칸이다. P의 미관측과 구별된다. |
| 그룹 / 화면 | 36 / 36 | 모든 화면이 세 자리여서 108자리다. 비어 있지 않은 카드는 A 22, B 11, C 22, 합계 55개다. |
| 전체 그룹 수 | A 41, B 11, C 41 | 첫 등장 그룹의 첫 멤버가 대표이며 첫 세 그룹을 표시한다. 나머지 그룹과 모든 원멤버가 보존된다. |
| C 미확인 개별 표시 | 25개 singleton / 총 41그룹 | `identity_key_complete=false`의 개별 표시를 재구성했다. 나머지 16개는 알려진 키다. |
| 고정 라벨·설명 | 모든 실제 카드 통과 | `원문 보기` 5자, `관련 링크` 5자, 설명 0자. 빈칸은 별도로 빈 라벨·빈 URL이다. |
| gold의 키 사용 | 0건 | 그룹 키는 URL, upstream, component/purpose/version/role 또는 singleton에서만 재구성된다. |

`metadata-audit-corrections.json`의 C1-1 role, C1-2 component, C4-6 role 보수적 정정이 실제 그룹 metadata에 모두 적용됐다. C4-6은 `['singleton','C4-6']`로 표시된다. 보존된 `pre-metadata-audit-groups.jsonl`·`pre-metadata-audit-views.jsonl`과 비교한 36행의 대표·멤버·카드·화면 밖 그룹은 모두 같다. `views.jsonl`의 metadata hash는 원래 freeze를 가리키므로, 재현 시 아래 override 파일도 함께 사용해야 한다. C2-3 `#altair`의 호스트 발행자가 pandas라는 사실을 대상 upstream Altair와 혼동해 B의 pandas 그룹으로 합치지 않았는지도 기존 입력·계산 감사에 기록했다.

Vega 후보 17개에서 `scope-fact-overrides.json`의 strict fact·locator·limitation이 normalized candidate와 활성 출처 행에 정확하게 적용됐다. 원문 전체 내용을 좁은 Overview 도착절의 주장으로 복제하던 문구가 남지 않았다. strict/W atom 집합과 그룹 키는 이 정정으로 바뀌지 않았다.

## 2. 계획·관측·비용·전이

| 확인 단위 | 결과 |
|---|---|
| 고정 HTTP 계획 ID / 관측 ID | 각각 1,924개, 중복 0, 집합 완전 일치 |
| `clicks.csv` 실제 시행 ID | 1,927개, 중복 0 = 고정 HTTP 1,924 + 별도 브라우저 1 + 공유 재검증 2 |
| HTTP 관측의 전체 행동 완료 여부 | `completed=true` 1,751; 실패 또는 도중 중단 173. 1,924건 모두 접속 성공이라는 뜻은 아니다. |
| 계획·관측 steps 일치 | 1,924/1,924. 도착 action/URL은 계획의 동일 순서 prefix이며 관측되지 않은 추가 행동은 없다. |
| 비용·시작 상태 | 모든 계획 행동의 비용 1, 합계 ≤2; 실제 비용 ≤2; 독립 fresh start 유지. 형제 목록과 멤버 열람을 각각 1회로 계산한다. |
| 실제 outgoing href | 계획 1,582건이 표시 대표의 strict 범위에서 보존된 literal href occurrence와 일치한다. 원풀 밖 대상도 포함된다. |
| 허용되지 않은 전이 | 124건. 첫 도착·고정 source hash·현재 base에서의 raw href 해석이 전이를 입증하지 못한 시행은 목적지 영수증이 있어도 그 경로의 후속 증거로 쓰지 않는다. |
| 고정 계획의 서로 다른 경로 서명 | 1,512개. 같은 view/kind/start/steps의 반복 서명 142개에서 literal occurrence 시행 412개가 추가된다. source occurrence 자체의 중복 충돌은 0이다. |
| strict 완전 ID를 하나 이상 확인한 시행 | 563/1,927. 이는 사용자 563명이나 독립 해법 563개를 뜻하지 않는다. |
| 허용된 의미 판독 범위 레코드 수 | 3,051 = 고정 HTTP 3,046 + 브라우저 1 + 공유 재검증 4 |
| 사용자 클릭·채택 반응 | 모든 시행에서 **미확인**. HTTP/DOM 기반 경로 확인과 원문 의미 판독을 사용자 행동 측정으로 바꾸지 않았다. |

생산 코드의 `provisional=false`를 길이만 보고 믿지 않고 계획·관측·추가 시행의 정확한 ID 집합을 확인했다. 형제 목록만 연 시행은 원문 증거를 제공하지 않는다. 원문을 두 개 읽은 경우도 **동일 시행 안에서 동일 alternative ID의 조건끼리만** 결합된다. CPython 근거의 3.11 문맥 정합성, fragment 도착 성공, 고정 응답 해시 일치도 각각 검사했다.

공유 재검증의 실제 관측은 `C2-REVALIDATED-QTPANDAS-20261122`와 `C2-REVALIDATED-IPYVEGA-20261122` 두 건이다. 동일한 C2-1 첫 카드를 A/B/C가 공유하므로 `applicable_views` 세 곳에 적용하지만 관측 행은 두 행뿐이다. 따라서 방식별 witness 수를 합쳐 6회 추가 관측이라고 쓰면 안 된다. `planned_trials`·`observed_trials`는 고정 HTTP 모집단이고, 브라우저/공유 추가 witness는 별도 필드로 제공된다. `successful_document_path_trials`는 해당 view에 적용되는 추가 witness까지 포함하므로 고정 계획 성공률을 구할 때 단독 분자로 쓰면 안 된다.

## 3. 원풀 분모와 36개 보기 재계산

P1~P4의 12개 보기에서 eligible/direct/reachable/max/W는 모두 `null`이며, 이는 보고서의 **미확인**이다. V1~V4의 12개 보기에서는 입증된 원풀 완전 대안이 0개이고 strict/W 완전 대안도 0개다. V의 조건부 회수 비율은 **해당 없음**이며, 프로젝트 전체에 답이 없다는 판정이 아니다. V3의 원요구에 없는 `text` 탐색 토큰 사용 이탈은 그대로 남아 있어 사전 규칙 준수 성공으로 집계하면 안 된다.

다음 표의 ‘직링크’는 첫 세 대표가 제공하는 근거 집합이고, ‘두 클릭 합집합’은 각 ID마다 자족적인 한 시행 witness가 존재한다는 뜻이다. 모든 ID를 한 사용자 시행에서 동시에 봤다는 뜻은 마지막 최대 열로 별도 확인한다.

| 요구·방식 | 원풀 적격 수 | 직링크 완전 수 | 두 클릭 원풀 ID 합집합 | 한 시행 원풀 ID 최대 | W 직링크 / W 두 클릭 | 원풀 밖 별도 확인 |
|---|---:|---:|---:|---:|---:|---|
| C1-A | 2 | 1 | 1 | 1 | 1 / 1 | 없음 |
| C1-B | 2 | 2 | 2 | 1 | 2 / 2 | 없음 |
| C1-C | 2 | 1 | 1 | 1 | 1 / 1 | 없음 |
| C2-A | 11 | 11 | 11 | 11 | 11 / 11 | IPython Vega, Qtpandas |
| C2-B | 11 | 10 | 11 | 11 | 10 / 11 | IPython Vega, Qtpandas |
| C2-C | 11 | 11 | 11 | 11 | 11 / 11 | IPython Vega, Qtpandas |
| C3-A | 1 | 0 | 1 | 1 | 1 / 1 | 없음 |
| C3-B | 1 | 0 | 0 | 0 | 0 / 1 | 없음 |
| C3-C | 1 | 0 | 1 | 1 | 1 / 1 | 없음 |
| C4-A | 0 | 0 | 0 | 0 | 0 / 0 | 없음 |
| C4-B | 0 | 0 | 0 | 0 | 0 / 0 | 없음 |
| C4-C | 0 | 0 | 0 | 0 | 0 / 0 | 없음 |

보강 원풀 적격 수는 C1의 2 + C2의 11 + C3의 1 = 14다. 각 방식의 직링크 합계는 12/14, 두 클릭 합계는 13/14로 같지만 요구별 이득·손실은 다르다. C1에서 B가 Requests를 표시하고, C2에서 B는 Matplotlib의 직링크 근거를 숨기며, C3에서 B는 strict 두 클릭의 CPython 완전 계약을 잃는다. 총합만으로 방식의 우열을 판단할 수 없다. C4는 의도한 양성 대조의 완전 계약이 입증되지 않아 분모 0이고 그 조건은 미충족이다.

## 4. 자족적 시행 witness와 금지한 합산

| 확인 대상 | 실제 시행 / URL·도착 범위 | 검산 결과 |
|---|---|---|
| C1-B의 HTTPX | `C1-B-T0005`: 형제 목록 → `https://www.python-httpx.org/quickstart/#timeouts`, `article#timeouts` | 비용 2, HTTPX 한 대안의 C1.A1/A2. |
| C1-B의 Requests | `BROWSER-C1-B-DIRECT-REQUESTS`: `https://requests.readthedocs.io/en/stable/user/advanced/#prepared-requests`, 346단어 절 | 비용 1, 별도 새 탭. HTTPX 시행과 합쳐 한 시행의 대안 2개로 계산하지 않는다. |
| C2-B의 한 시행 최대 11 | `C2-B-T0043`: pandas 2.0 ecosystem `#visualization` → 실제 `user_guide/visualization.html#visualization` | 비용 2. 695단어 ecosystem 절과 도착 h1 전체 4,949단어 범위의 조건을 같은 시행 안에서 결합한다. Matplotlib에 대한 짧은 다른 witness만 보고 최대값을 낮추지 않는다. |
| C3-A/C strict 완전 계약 | `C3-A-T0031`, `C3-C-T0031`: `https://peps.python.org/pep-0654/` → 실제 `#specification` | 비용 2. 최초 800단어와 Specification 절을 같은 시행에서 읽는다. |
| C3-B strict 실패 / W 회복 | strict의 모든 자족적 시행은 미완전. W에서는 `C3-B-T0005`의 형제 목록 → PEP 문서, 또는 `C3-B-T0011`의 release → PEP 문서가 완전해진다. | strict 범위의 서로 다른 시행에서 A1/A2를 빌려 완전하다고 하지 않았다. W는 도달 문서 판독 범위만 완화한다. |
| C2의 추가 대안 두 개 | 두 `C2-REVALIDATED-*` 시행 각각 C2-1 → 실제 GitHub href. 원본 steps의 응답 SHA, source DOM index 79(Qtpandas)·58(IPython Vega), fresh opener, 빈 cookie jar를 확인했다. | 각 비용 2. 각 시행은 원풀 10개 + 새 대안 1개를 확인한다. 두 목적지를 합쳐 한 시행으로 만들지 않는다. 원풀 분모는 11 그대로이고, 모든 시행에 걸친 C2 도달 ID 합집합 13과 한 시행 전체 최대 11도 구분된다. |

브라우저 원본 `requests.loaded=true`, `fragment_exists=true`, `fresh_start=true`, `navigation_cost=1`, 64자리 DOM SHA 및 C1.A1/A2 supports를 직접 검사했다. CSV의 성공값을 원본 검증 없이 신뢰한 것이 아니다. DOM SHA `de9533a89aff1ad3441a1cc71963aff544b0abd2e0162ef290c1b04f37a8101c`는 렌더링된 DOM의 해시이며 원 HTTP 응답 바이트의 해시가 아니다. 원래 실패했던 HTTP 시행을 성공으로 덮어쓰지 않았다. 늦게 열린 Pandoc 브라우저 DOM도 P24 원풀에 소급 삽입하지 않았다.

C2 새 목적지는 과거 GitHub 응답과 raw SHA가 달라 과거 의미 판독을 새 시행에 빌릴 수 없었다. 추가 두 시행은 각자의 정확한 신규 응답을 즉시 읽은 기록과 source/target supports를 가지고 있다. 각 행의 완전 ID·원풀 교집합·원풀 밖 차집합을 별도로 재계산했으며 기록과 일치한다. 현행 설치·실행 호환성까지 입증하는 판정으로 넓히지 않았다.

## 5. W/U와 파생 열 정정

모든 1,927행에서 strict 완전 ID는 W 완전 ID의 부분집합이며, 36개 보기의 알려진 direct/reachable 집합에서도 단조성이 성립한다. 실제로 뒤집히는 요구는 C3이다. A/C의 직링크 0→1, B의 두 클릭 0→1이며 그룹·전이·비용은 그대로다. missing fragment를 W로 복구하지 않는다.

U는 12개 보기의 카드·멤버·화면 밖 그룹을 C와 비교했다. 알려진 8요구에서는 병합 변화가 없다. P1~P4의 `changes.csv` U행 네 개는 before/after/gained/lost/eligible 모두 **미확인**이고, 빈 fixture가 같다는 사실을 경험적 무변화라고 쓰지 않는다.

확인 중 발견한 `semantic_read_scope_count` 오류는 응답 해시가 같아도 fragment가 존재하지 않아 도착 실패한 범위를 한 개씩 더 세는 문제였다. 수정 전 13행 전체는 `semantic-scope-count-correction.json.prior_rows`에 보존돼 있다.

- V2-A-T0041, V2-A-T0105, V2-B-T0043, V2-C-T0041, V2-C-T0105: 각 2→1.
- V4-A-T0008, V4-B-T0011, V4-C-T0008: 각 2→1.
- C1-B-T0008: 1→0.
- C2-A-T0091, C2-A-T0110, C2-C-T0091, C2-C-T0110: 각 2→1.

현재 열은 실제 성공한 도착, 고정 해시 일치, 의미 범위 레코드 존재, 허용 전이를 모두 만족하는 record 수와 일치한다. 13행의 `confirmed_complete_ids`, `confirmed_original_pool_ids`, atoms, subconditions, W complete IDs는 수정 전과 같았다. 36개 보기의 원풀 분모·직링크·두 클릭 원풀 집합·한 시행 최대·W 집합도 수정 전과 같다. 새 C2 목적지 두 개는 별도의 후속 관측 추가 효과이며 이 파생 열 오류 정정의 효과와 혼동하지 않았다.

## 6. 출처 원장과 남는 수용 범위

활성 `sources.jsonl`은 632행, source_id 중복 0, 필수 필드 누락 0이다. 산입 행은 84개이며 산입 duplicate_group도 84개다. 핵심 53 + 추가 second-hop 원문 31이라는 합계가 유지된다. 두 C2 재검증의 재독 4행과 루트 최종 원문 점검 9행은 산입하지 않았다. 보존용 `sources-V-v1.jsonl`은 활성 원장에 다시 통합하지 않았다.

이 감사는 기록의 계산·연결·범위 일관성을 확인했다. 루트의 마지막 원문 재열람은 `final-source-review.jsonl`의 9행으로 구별한다. 그 재열람을 이 감사자가 새로 수행했다고 주장하지 않는다. P 후보 풀 미관측, V3 탐색 토큰 이탈, C4 완전 양성 근거 부족은 수치가 맞더라도 남는 제한이다. 모든 후보 URL의 기능 실행 및 실제 사용자 반응 역시 **미확인**이다.

## 7. 감사 대상 파일 SHA-256

아래는 이 receipt가 검산한 파일의 바이트 해시다. 이후 원장을 변경하면 해당 부분을 다시 확인하거나 새 revision receipt를 추가해야 한다.

| owned_path 상대 파일 | SHA-256 |
|---|---|
| `pool.csv` | `53ac7e9dbb95a029aae6c834e7222df3c009b1c4ad6e0993aea7b2ce62982b28` |
| `frame.csv` | `5d70e16f93431a8203d70e39142633637ef480f9a938a9b4f31377a0c1ad88c8` |
| `requirements.csv` | `28d41407046a4cad838d7040baba157283d6eee6cf73221e5571ac8ec64d1e49` |
| `evidence/cases.json` | `3af5c7b7c38c00e3dfa02364f552e06df3b9893691424ba3d7ba565cd61ce962` |
| `evidence/display-metadata-freeze.json` | `6bdbde48f81e2ed500edab6223f5ef237adba7badb3578c7906bae62253c12ac` |
| `groups.jsonl` | `17605ae42f40ce39140acb9bb1939c72e8f352287310efa92c08c89540450fa4` |
| `views.jsonl` | `64d0571cf523be33af06c656e77176874c9c82e6dd65e13e2b67cffa0699f943` |
| `evidence/views-U.jsonl` | `c7d851c8c863ab4f6323a8bfdb935b21c3ca42995509527fceda96121205d082` |
| `evidence/candidate-evidence.jsonl` | `b00d7e049f8ed261d9192ceea947334e60aa0572fde9f00b3c45b925ff58d492` |
| `evidence/results-data.json` | `dd845db57eef42512ed2e0c9960459c8d8d30ccc6e049d1537770477fd6d4e27` |
| `clicks.csv` | `0a82ad6b5c629f5aa8fa6cbf8553ec2bd4c5909ae65dd63d811b640c90401d91` |
| `changes.csv` | `1a81509d4d396f579901589060486c1235d83028681769d2f14d5d2b13e695df` |
| `gold-paths.csv` | `424f454e38a660d47b6f542a6067fb36e5e74d934c6c9165172289bcc3e95efb` |
| `evidence/trial-plan.jsonl` | `16fbf84c0ac0b0cdc4162a021fb65519560c1eb2b91bf5e4de14fff493c11b66` |
| `evidence/trial-observations.jsonl` | `5094c7d4fb492d46dce83f81b848f92ba95716e95910da1e588194d592973f23` |
| `evidence/metadata-audit-corrections.json` | `5e4c4b70ff31ccf10bd87d15a1d6ca240742ea43e840dae555bdc5964f0823f1` |
| `evidence/vega/scope-fact-overrides.json` | `ded3b8f32bdd54ac13be4b4cfe91fcb3e289aa4441b5e0e484438d3554d5a541` |
| `evidence/semantic-scope-count-correction.json` | `de5dcb50fbaa936d7d6053887fa09ae8f032d1ce15165deef8df64107caa0ee3` |
| `evidence/browser-observations.json` | `0f5fab1813d311783c37a78863ca398eb1f3c49dabd967e22865dea788679b7f` |
| `evidence/crossfield/control-second-hop-revalidated-trials.json` | `01fe86bfc8553790068ef630f79720642df8186243b9fb8eae11b39e11279344` |
| `evidence/calculate_results.py` | `48125c93d6b6a51ebf95df1f4369a760f9d3a4c5641207a53bd509dc542d5fdd` |
| `sources.jsonl` | `f5c9111006a9c1fdc642ba7ea7e862764a65058bc0ca27d0322bf30796c34f22` |
| `evidence/final-source-review.jsonl` | `8c162b6e0a16f1aa5e954255a8f731e3eb51203a94d5c2431dcba93b800162b2` |

본 receipt는 `evidence/vega/final-audit.md`만 새로 썼다. 연구 결과·수용 기록·원격 커밋과 최종 HANDOFF 검사는 루트가 이어서 수행한다.
