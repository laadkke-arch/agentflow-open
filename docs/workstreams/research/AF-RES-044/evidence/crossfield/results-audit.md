# AF-RES-044 집계 구현 내부 검토

검토자: 병렬 보조 에이전트 `crossfield`. 검토 시각: 2026-11-22 20:54–20:57 UTC. 사람 또는 블라인드 독립 판독이 아니다. 출발점은 루트가 작성한 집계 코드와 이미 봉인한 원장이다. 이 검토자는 계산 코드·입력·결과를 수정하지 않았으며, 수정 제안은 루트에 전달했다. 루트의 수정 후 같은 반례를 다시 계산했다.

**판정:** 한 시행 안에서 대안별 원자 조건을 합치는 구조와, 완결된 대안 ID의 시행 간 합집합을 따로 계산하는 구조는 유지된다. 발견한 W 근거 소실, 판 정렬 없는 하위조건 합침, 출발 창이 확인되지 않은 전이의 승격, C2 부분 근거 누락은 수정 후 재검산했다. 실행 원장이 진행 중이므로 최종 도달 수치·방법 우열을 확정하는 검토가 아니다. 아래의 P 미확인 표시 및 접속 지표 명칭은 이 검토 시점의 별도 남은 사항이다.

## 1. 읽은 입력과 검토 시점

경로는 모두 `docs/workstreams/research/AF-RES-044/` 기준이다.

| 입력 | 확인 범위 / 검토 시점 SHA256 |
| --- | --- |
| `SCOPE.md` | 39·41행 direct inventory와 실제 두 동작 구별, 45·47행 같은 요구·판·방향 및 분모, 51행 U/W 단일 요소 완화 |
| `evidence/calculate_results.py` | 전체. 수정 후 `0d38a335f6c9f6a3877d563c0d11efa620fe25475b769cea65d89b3dd74f3713` |
| `evidence/build_study.py` | 그룹·표시·후보 판정 생성. 수정 후 `26956db248fbfcd5db75b13c14cd54f6682b4a187446036c990ae005fb462cbb` |
| `evidence/candidate-evidence.jsonl` | 72행 전체 구조와 C1–C4의 조건·하위조건. 수정 후 `04ea57bc53ac8ad8e45287039c28f99d4de396f65222be2a05efa4240ea9d18d` |
| `gold-paths.csv` | 후보 72행, 최소 완전 원풀 경로 20행. 검토 시점 `abbd3831b99193f7b6aa5ca265227af755531cdb8df6371c2cebaa0424ace975` |
| `changes.csv` | 짝 비교·W·U 156행. 진행 중 계산 산출물이며 최종 도달 관측으로 해석하지 않음 |
| `evidence/trial-plan.jsonl` | 1,924개 고유 trial ID, 모든 계획 비용 최대 2. `16fbf84c0ac0b0cdc4162a021fb65519560c1eb2b91bf5e4de14fff493c11b66` |
| `evidence/trial-observations.jsonl` | 계속 추가 중인 원장의 완료된 JSONL 행. 계획 일치, 중복·미등록 ID, 비용, 도착 성공·raw SHA 검사를 확인. 읽은 부분의 크기를 최종 실행 수로 쓰지 않음 |
| `evidence/results-data.json` | `provisional:true` 중간 산출물. 직접 제공 범위, 도달 합집합, 한 시행 최대, witness, 분모 구분을 확인 |
| `evidence/run_click_trials.py` | 새 opener/빈 CookieJar, 계획 전이, DOM fragment, raw href 존재 검사 및 관측 저장 전체 |
| `evidence/vega/second-hop-coding.json`, `evidence/pandoc/control-second-hop-coding.json`, `evidence/crossfield/control-second-hop-coding.json` | 정규화되는 atom·판·하위조건·W 필드 전체 구조와 아래 반례 행 |
| `views.jsonl`, `evidence/views-U.jsonl`, `evidence/browser-observations.json` | C/C-U 카드·멤버·화면 밖 그룹 동일성, Requests 브라우저 관측 1회의 범위 |

이 SHA들은 검토한 버전의 식별자다. 루트가 이후 정정한 파일의 해시와 일치한다고 주장하지 않는다. 정정 경위는 `evidence/arithmetic-corrections.json` 및 `evidence/candidate-coding-corrections.json`에 연결한다.

## 2. 발견과 수정 재확인

### R1. W가 strict 근거를 버리는 비단조 합침 — 수정 확인

**발견:** 이전 `merged()`는 strict 필드를 W 필드로 교체했다. 전체 본문을 판독하지 않았다는 이유로 W 필드가 빈 경우 이미 확인한 좁은 절의 사실도 사라졌다. 후보 `C4-6`의 `wait_all`과 Python second-hop 목적지 10행이 구체 반례였다. 예를 들어 PEP654 채택 공지의 `availability_3_11`은 strict에 있고 W 비판독 필드에는 없었다. 확대 창에서 그 사실을 부정했다는 관측은 없었다.

**수정:** `calculate_results.py` 43–58행은 W에서 strict 필드와 추가 W 필드를 합친다. 판 정렬 gate를 통과한 각 후보와 각 목적지에 대해 `strict atoms ⊆ W atoms`, `strict subconditions ⊆ W subconditions`를 다시 계산했고 소실은 없었다. 모든 봉인 계획의 complete ID에도 W 소실이 없었다. 이전 반례에서도 전체 완전 대안 ID가 감소하는 현재 계획은 찾지 못했으므로, 처음 오류를 완전 대안 수가 실제 뒤집힌 것처럼 쓰지 않는다.

**보존 조건:** W는 같은 도착 문서의 판독 범위만 늘린다. 카드, 원풀, href 전이 그래프, 비용, 판은 그대로다. fragment 부재나 접속 실패를 성공으로 바꾸지 않는다. 추가 미판독 부분은 계속 미확인이다.

### R2. 현재판·제안 단계 하위조건이 3.11 계약으로 승격 — 수정 확인

**발견:** 이전 정규화는 Python 목적지의 `version_alignment`와 `conflicts`를 버렸다. 다음 출발·목적지 조합은 서로 다른 판 맥락의 하위사실을 합쳐 `C3.A1`을 완전으로 만들었다.

| 실제 계획 ID | 출발 및 두 번째 URL | 이전 잘못된 승격 |
| --- | --- | --- |
| `C3-A-T0023`, `C3-C-T0023` | `https://peps.python.org/pep-0654/` → `https://mail.python.org/archives/list/python-dev@python.org/thread/MQ2UCSQ2ZC4FIGT7KSVI6BJA4FCXSOCL/` | PEP 서두의 3.11 availability와 2021-03-20 제안 메일의 constructor 경계를 합침. 목적지 원장은 final 3.11 mapping 미확인으로 명시 |
| `C3-A-T0067`, `C3-C-T0067` | 같은 PEP 서두 → `https://docs.python.org/3/builtins/exceptions.html#lib-exception-groups` | 관측된 Python 3.15.2 constructor 설명을 3.11 계약으로 결합. 목적지 원장은 `version_not_pinned_to_requested_3_11` 명시 |

위 시행은 수정 전에도 `C3.A2`가 부족해 **전체 대안은 비완전**이었다. 따라서 완전 대안 수치의 뒤집힘은 주장하지 않는다. 부분 근거를 완전 atom으로 승격한 오류를 직접 재현한 것이다. 동일한 문제가 있는 `/3/reference/compound_stmts.html#except-star`, `/3/tutorial/errors.html#tut-exception-groups`의 사실도 3.11 증거로 자동 사용할 수 없다.

**수정:** `calculate_results.py` 17–18·31–33·49행은 실제 `/3.11/` 매뉴얼, Final PEP654, 3.11 대상의 PEP654 채택 공지만 이 계산의 판 맥락에 허용한다. 다른 문서에서 읽은 사실은 원장에 남지만 3.11 증명 합침에 들어가지 않는다. 위 네 계획을 재계산하면 `C3.A1`은 더 이상 완전하지 않고 `availability_3_11`만 남는다. Python 판독 담당도 미확인 판의 사실을 최종 3.11 계약으로 합치지 않는 것이 기록의 의도였다고 확인했다.

**적용 한계:** 현재 allowlist는 이 과제의 봉인 입력을 위한 보수적 gate다. 임의 Python 문서에 일반화한 호환성 판정기가 아니다. 다른 판 문서를 추가하려면 URL 이름만 보고 허용하지 말고 관측된 판과 계약 정렬 근거를 다시 기록해야 한다.

### R3. 출발 창 검증 없는 두 번째 목적지 승격 — 수정 확인

**발견:** 실행기의 `follow_actual_href`는 새로 받은 전체 DOM 어디에든 raw href가 있는지를 검사한다(`run_click_trials.py` 62–65행). 이전 집계는 첫 응답의 raw SHA가 달라도 두 번째 응답의 SHA가 맞으면 두 번째 근거를 채택했다. 출발 내용이 바뀌어 href가 strict 창 밖으로 이동하거나 redirect 때문에 상대 href의 base가 달라진 경우, 봉인된 전이와 실제 관측 전이가 같다고 보장할 수 없었다.

이는 코드상 누락이다. 감사 중 읽은 진행 원장에서 이 누락으로 완전 대안이 실제 과대 집계됐다고 확정하지 않는다. 접속 성공, 목적지 의미 확인, strict 경로 승인 여부를 분리해야 한다는 지적이다.

**수정:** `calculate_results.py` 85–100행은 outgoing 경로에 대해 첫 도착 성공, 봉인 출발 raw SHA 일치, `urljoin(actual final source URL, raw href) == planned destination`을 모두 요구한다. 불충족 경로의 목적지 접속 기록은 보존하지만 해당 전이를 통한 증거로 합치지 않는다. 처음 직접 도착해 확인한 근거는 독립적으로 남는다. 고정 출발 바이트가 일치하면 봉인된 strict 창 내부 href의 위치도 재사용할 수 있다. W 역시 같은 gate를 사용한다.

### R4. Altair·Bokeh의 확인된 Python 조건 누락 — 수정 확인

**발견:** `build_study.py`는 C2의 `complete_alternative_ids`에서만 원자 증거를 만들었다. `control-C2.json` slots 4·6은 각 홈페이지 창에서 Python library를 명시적으로 확인했지만, 완전 대안은 아니므로 `candidate-evidence.jsonl`에는 근거가 전혀 없는 것처럼 들어갔다.

**수정:** 현재 `C2-4`는 `C2-altair:[C2.A1]`, `C2-6`은 `C2-bokeh:[C2.A1]`을 보존한다. 해당 도착 창의 tabular 시각화 조건 `C2.A2`는 여전히 미확인이다. 원풀 분모·대표의 완전 ID는 다른 원문에서 이미 같은 대안이 입증돼 있어 변하지 않지만, 후보별 부분 근거 원장이 정확해졌다.

## 3. 검토 시점에 남은 표시·검증 사항

| ID | 근거와 영향 | 최소 수정 또는 최종 확인 |
| --- | --- | --- |
| R5 — P의 U 결과 미확인 | `calculate_results.py` 129–132행은 P1–P4에도 gained/lost `[]`, eligible `None`, “merges no actual groups”를 기록한다. 이 네 풀은 미관측이다. CSV의 빈 denominator와 효과 0처럼 보이는 문장은 `미확인`과 다르다 | P1–P4의 U 결과와 분모를 명시적 `미확인`으로 기록하고 원풀 미확보 이유를 붙인다. 관측한 나머지 8요구의 C/C-U는 카드 대표뿐 아니라 `cards` 전체와 `offscreen_groups`까지 같음을 이번 감사에서 확인했다 |
| R6 — transport 지표 명칭 | `successful_transport_trials`는 `connectivity_success=True`를 모두 합친다. `siblings_only` 55개 계획은 원문 네트워크 도착이 0인데도 실행기에서 True다. 이것을 HTTP 접속 성공 수로 부르면 부정확하다 | 전체 계획 동작 완료 수로 이름을 붙이거나, `requested_url`이 있는 도착의 HTTP/fragment 성공 및 원문 1개 이상 도착한 시행 수를 따로 낸다. 형제 목록만 여는 시행의 원문 증거 0은 그대로 유지한다 |
| R7 — 최종 완료 gate 보강 | `provisional = len(obs) != len(plans)`는 두 ID 집합이 같은지를 직접 확인하지 않는다. dictionary 변환은 중복 관측을 숨길 수 있다. 브라우저 행 역시 저장한 `loaded/fragment_exists` 값을 확인하기보다 성공 True를 직접 기록한다 | 최종 검산에서 plan/observation ID 집합 완전 일치·각 ID 유일·계획 steps 일치·비용≤2·browser 실제 loaded/fragment/fresh_start/cost/hash 존재를 assert한다. 감사 시점의 읽은 완료 행에는 중복·미등록·계획 불일치·예산 초과를 찾지 못했고 브라우저 원본의 성공 값은 실제로 True였다. 현재 관측의 부정확한 성공을 발견했다는 뜻은 아니다 |

U는 알려진 동일 필드 아래에서 unknown 병합만 바꾸는 민감도다. 관측 입력에서는 U가 그룹을 바꾸지 않으므로 strict 전이 그래프도 그대로다. 미관측 P 풀에 대해서는 “영향 없음”을 추정하지 않는다.

## 4. 통과한 산술·분리 규칙

`calculate()`의 출력 함수를 메모리 capture로 교체해 실행했다. 루트 산출물을 덮어쓰지 않았다. 36개 보기와 1,925개 계산행(1,924개 봉인 계획 + 별도 브라우저 시행 1개)에 다음 검산을 적용했고 불일치를 찾지 못했다. 1,925는 성공 시행 수가 아니다.

- `merged()`는 한 시행에 실제 허용된 records만 받아 **같은 alternative ID** 안에서 atom 및 subcondition을 합친다. 다른 구현끼리 부분 조건을 합치지 않는다.
- `reachable_original_pool_ids`는 이미 한 시행에서 완결된 ID들의 합집합이다. 각 ID의 `witnesses`는 해당 시행의 `confirmed_complete_ids`에 실제 존재한다. 여러 시행의 부분 사실을 먼저 합친 뒤 완전 대안을 만드는 경로는 없다.
- `max_complete_original_pool_ids_in_one_trial`은 개별 시행의 원풀 완전 ID 개수의 최대다. 도달 가능한 대안 ID 합집합 크기와 구분된다. 보고서에서 이 둘을 같은 사용자가 한 번에 확인한 수로 합쳐 쓰면 안 된다.
- C2의 원풀 적격 ID는 11개이고 IPyvega·qtpandas는 이 집합에 없다. 추가 경로에서 확인하더라도 `additional_ids_outside_denominator`에만 넣는다. 두 개를 각각 확인하는 별도 시행을 한 사용자 시행으로 합치지 않는다.
- P1–P4의 주요 분모·direct·reachable·한 시행 최대 필드는 `null`이다. V1–V4 및 C4의 관측된 원풀 적격 수 0과 구별된다. 비율을 만들 때 0 분모는 `해당 없음`, 미관측은 `미확인`이다.
- 원풀 적격 수는 후보 판정으로 별도 재계산하면 C1=2, C2=11, C3=1, C4=0이다. 이는 고정 입력의 분모 확인이며, 진행 중인 실제 접근 성공 수를 추정한 값이 아니다.
- `direct_complete_ids`는 첫 세 문서가 제공하는 근거 inventory이며, 세 문서를 실제로 두 번의 클릭에 읽었다는 뜻이 아니다. direct 집합은 원풀 적격 집합 안에 있다.
- 동일 원문 반복 칸은 fragment를 제거한 문서 URL로 센다. 같은 문서의 다른 절이 다른 필수 근거를 제공할 수 있으므로, 이 칸 수를 곧바로 낭비나 손실로 해석하지 않는다.
- 원시 HTTP 실패는 Requests 브라우저 성공 1회로 덮어쓰지 않는다. 브라우저 시행은 `BROWSER-C1-B-DIRECT-REQUESTS`라는 독립 witness다. 실행 성공·문서 진술·사람의 클릭/채택은 서로 다른 범주다.
- 수정 후 각 개별 증거, 모든 계획, 확인된 시행, 보기의 strict 완전 ID는 대응 W 집합의 부분집합이다. W의 추가 범위를 쓰더라도 strict 그래프 및 비용은 불변이다.

## 5. 최종 산출물에서 다시 확인할 최소 항목

실행이 끝난 뒤 루트는 최종 산출물에 대해 ID 집합 완전 일치와 위 불변식을 재계산하고, 각 표의 도달 값에 실제 witness를 붙여야 한다. 이 감사는 진행 중인 `results-data.json`의 빈 도달 집합을 최종 실패로 판정하지 않았다. 미관측 P 요구를 제외한 관측 분모와 전체 요구의 관측 가능성을 구별하고, 모든 natural 요구에 대한 성공 비율로 관측된 일부만 대입하지 않는다. C4의 원풀 적격 0을 양성 대조 성공이라고 바꾸지 않는다.

최소 재실행은 `python -B docs/workstreams/research/AF-RES-044/evidence/calculate_results.py`다. 다만 그 명령은 결과 파일을 갱신하므로 편집·커밋 담당 루트가 관측 완료 후 실행한다. 이 검토자가 실행한 검산은 `writecsv`와 `dump`를 메모리 함수로 교체한 읽기 전용 계산이었다.

이 감사가 보증하는 것은 명시된 코드 버전과 봉인 입력의 집계 관계다. 원문 해석 전체의 정답, 새로운 판의 호환성, 실제 사용자의 채택을 보증하지 않는다.
