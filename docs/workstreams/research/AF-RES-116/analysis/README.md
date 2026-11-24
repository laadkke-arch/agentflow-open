# 수신 원장 기계 수집

`collect_trials.py`는 고정 `packets.jsonl`의 packet ID·사건·A/B/C를 그대로 `readers/<packet_id>/events.jsonl`에 연결한다. 로그를 요약·검사하지만 **정답·완전 근거·부분 복원·위험한 확정 등 의미 등급은 만들지 않는다.** 실제로 하지 않은 수신을 성공/실패로 채우지 않는다.

## 실행

```sh
# 실제 파일을 쓰지 않고 현재 관측·미관측 수와 검사 결과만 확인
python -B docs/workstreams/research/AF-RES-116/analysis/collect_trials.py

# 수신 원장이 확보된 뒤 root가 파생 파일을 생성
python -B docs/workstreams/research/AF-RES-116/analysis/collect_trials.py --write

# 이후 같은 고정 입력에서 파생 원장이 재생성되는지 검사
python -B docs/workstreams/research/AF-RES-116/analysis/collect_trials.py --check
```

입력 변경이 필요하면 `--packets`, `--readers`, `--corpus`, `--engine`을 지정한다. 기본 계획은 18꾸러미와 각 3단계이며, 연구 자연 표본에서는 그 값을 유지한다. `--expected-packets`는 합성 검사 등 명시적 별도 입력용이다.

`--write`는 파생 결과만 갱신한다. 원 packets, corpus, reader.py, events.jsonl에는 쓰지 않는다. `--check`는 수집 UTC만 비교에서 제외하고 다른 파생 값은 같은지 확인한다. 로그 수신이 진행 중이면 미완료 경고와 미관측 자리를 남긴다. 미관측 상태 자체는 오류가 아니므로 readers 디렉터리가 아직 없어도 정상 종료한다.

## 출력

| 경로 | 내용 |
| --- | --- |
| `trails.jsonl` | 실제 exposure마다 packet/조건, 직전 선택 원문과 이유, 실제 표시·지문·URL/fragment/offset, 단계 답 원문, UTC와 기간, 모든 표시 비용 |
| `analysis/trial-slots.jsonl` | 예정 54자리 각각의 observed / early_stop / unstarted 및 답 기록 여부 |
| `analysis/citation-checks.jsonl` | 각 단계의 인용문이 그 단계까지 실제 보인 구간에 존재하는지, 문서·offset 일치 여부 |
| `analysis/trial-summary.json` | 예정 18꾸러미/54자리 대사, 세션 상태, 오류·경고, input SHA, 조건별 실제 비용, 사건↔조건↔세션 매핑 |

`packet_status_counts`의 observed는 조기종료 없이 하나 이상 exposure가 있는 꾸러미, early_stop은 명시적 조기종료 꾸러미, unstarted는 아직 exposure가 없는 꾸러미다. 초기화만 된 세션도 unstarted다. 각 단계 자리에서 이미 읽은 것은 observed, 명시적 조기종료로 남은 것은 early_stop, 아직 열지 않은 나머지는 unstarted다. `finished_packets`, `answered_stages`, `fully_observed_and_answered_packets`를 별도로 보므로 observed를 완료로 오해하지 않는다.

## 프로토콜 검사

- 해시 체인, 순번, 세션 ID와 실제 UTC 순서.
- init의 엔진·corpus SHA, 시작 문서, 3개봉/1,500자 핀.
- choice → exposure → answer 연결과 다음 선택 전에 이전 답이 있었는지.
- 원 corpus와 고정 렌더러로 실제 view 전체를 다시 계산하여 비교.
- 완전히 표시된 링크만 선택했는지, 이전 표시 링크의 누적, 실제 허용 행동.
- 전체 표시 1,500자 상한, Unicode 문자와 UTF-8 바이트, 본문/내비게이션의 분리 합계와 누적 비용.
- 최대 3개봉, 단계 답 중복, 종료와 조기종료의 남은 자리.
- 사건마다 정확히 A/B/C 꾸러미가 존재하는지 및 packet 문구 비용과 corpus 핀.

해시 체인이 깨진 로그라도 읽을 수 있는 원 관측은 버리지 않는다. `session_audit_valid=false`, 오류, 검증되지 않은 exposure 수로 보존한다. 이 원장에서 `observed`는 로그에 exposure가 있다는 뜻이다. 별도 `validated_logged_exposures`와 `unverified_logged_exposures`를 확인해야 한다. 프로토콜 오류가 있으면 CLI는 종료값 2를 반환하며 `--write`에서는 오류를 포함한 파생 자료도 남긴다.

## 인용 검사

인용은 해당 단계까지 누적된 **같은 문서의 연속 표시 구간 합집합**에서만 찾는다. 인접 구간은 이어 읽은 것으로 합치지만, 미노출 틈·다른 문서·본문과 뷰어 헤더를 이어 붙이지 않는다. `doc_id`가 주어지면 그 문서 안에서 일치해야 한다. 다른 문서에서만 일치하면 별도 상태로 남긴다. `start/end`를 주장했다면 그 위치와 인용문도 맞는지 확인한다.

- `exact_visible_source`: 원문 평문의 실제 노출 구간에 정확히 존재.
- `exact_visible_source_wrong_claimed_offset`: 인용문은 보였지만 주장한 offset은 틀림.
- `viewer_display_only_not_source_proof`: 헤더/내비게이션 등 표시에는 있으나 문서 근거로 분류하지 않음.
- `quote_visible_only_in_different_document`: 다른 문서에만 존재.
- `whitespace_normalization_only`: 공백 정규화 후에만 맞음. 정확한 인용 성공으로 승격하지 않음.
- `not_in_cumulative_visible_intervals`: 실제 누적 노출로 찾지 못함.

`strict_supported`는 **인용문 존재·주소의 기계적 일치**만 뜻한다. 주장의 옳음이나 필수조건 충족을 뜻하지 않는다. `verified_quote_presence`는 이에 더해 세션 프로토콜 검사도 유효할 때만 true다. 인용 불일치는 연구에서 관측해야 할 값이므로 그것만으로 exporter를 오류 종료시키지 않는다. 의미 판독자는 실제 인용과 gold를 별도로 대조한다.

## 기간과 가림 한계

노출→답, 답→다음 선택, 선택→노출의 UTC 차이를 그대로 계산한다. 도구와 스케줄 지연을 포함하는 wall duration이며 사람의 능동 독해시간이나 절약 시간으로 환산하지 않는다. 원 engine이 기록한 시간도 함께 보존한다.

이 도구는 새 AI 문맥이 실제로 독립이었는지, 다른 파일을 읽지 않았는지, 사람의 판단이었는지를 증명하지 않는다. 그런 사실은 실행 주체의 별도 문맥·접근 기록으로 확인해야 한다.

## 필요한 오류 검사만

```sh
python -B docs/workstreams/research/AF-RES-116/analysis/test_collect_trials.py
```

원 reader로 실제 합성 로그를 만든 뒤 선택 문구를 사후 변조하는 사례, 보이지 않은 틈과 다른 문서를 이어 인용하는 사례, 완료/조기종료/미시작 계획자리 대사 세 가지를 검사한다. 합성 파일은 analysis 하위 임시 폴더에 생성 후 삭제하며 `exporter-synthetic-checks.json`만 남긴다. 자연 관측에는 추가하지 않는다.
