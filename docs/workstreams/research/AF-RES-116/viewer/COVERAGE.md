# 고정 구간 도달성 분석

`analyze_coverage.py`는 이미 봉인한 문서 corpus와 이미 생성한 `reachability/raw/*/paths.jsonl`, `views.jsonl`, `summary.json`을 읽는다. **gold를 작성하거나 정답을 추정하지 않는다.** 제공된 필수 구간이 실제 허용 경로의 누적 표시 구간 안에 전부 포함되는지만 계산한다. 수신자의 선택이나 답을 관측한 시험이 아니다.

## 입력

```json
{
  "schema": 1,
  "corpus_sha256": "실제 corpus 입력파일의 SHA-256",
  "cases": [
    {
      "case_id": "fixture",
      "graph": "fixture-graph-directory",
      "start_doc_id": "manual",
      "semantic_gold_complete": true,
      "missing_inputs": [],
      "modes": {
        "target": {
          "semantic_complete": true,
          "alternatives": [[{"doc_id": "manual", "start": 100, "end": 110}]]
        },
        "operation": {
          "semantic_complete": true,
          "alternatives": [
            [{"doc_id": "manual", "start": 100, "end": 150}],
            [{"doc_id": "example", "start": 20, "end": 70}]
          ]
        },
        "full": {
          "semantic_complete": true,
          "alternatives": [
            [
              {"doc_id": "manual", "start": 100, "end": 150, "condition": "operation"},
              {"doc_id": "manual", "start": 300, "end": 360, "condition": "preservation"},
              {"doc_id": "example", "start": 80, "end": 130, "condition": "exception"}
            ]
          ]
        }
      }
    }
  ]
}
```

각 `alternatives` 안의 배열은 **필수 구간 전체의 AND**, 여러 배열 사이는 **OR**다. 예를 들어 같은 주장을 충분히 지지하는 문서와 공식 예제가 각각 있다면 둘을 별도 대안으로 넣는다. 한 경로가 어느 대안 하나의 모든 구간을 읽으면 그 대안은 covered다. `condition` 같은 추가 라벨은 그대로 보존하되 분석기는 의미를 해석하지 않는다.

대안은 `{"id":"named-alternative", "intervals":[...]}` 형식도 지원한다. `modes` 없이 `target_alternatives`, `operation_alternatives`, `full_alternatives`를 case에 직접 둘 수도 있다. mode 이름은 임의 문자열이지만 보고서에서 target/operation/full을 구분하는 구성이 권장된다.

구간은 corpus 평문의 **유니코드 문자 offset `[start,end)`**다. HTML 원본 offset·바이트·화면 헤더 offset이 아니다. 빈 대안이나 빈 구간은 근거가 아니며 성공으로 처리하지 않는다. 입력 구간이 문서 길이를 넘으면 잘라 맞추지 않고 invalid로 표시한다.

`graph`는 raw root 아래 정확한 디렉터리 이름이다. 생략하면 `case_id`와 같은 디렉터리를 사용하고, 그 디렉터리가 없을 때만 유일하게 일치하는 `start_doc_id`/`start_offset`을 찾는다. 여러 후보를 추측해서 고르지 않는다. graph의 corpus SHA, 각 view의 SHA/길이, path의 interval과 view의 실제 offset 및 요약 건수를 확인한다. 입력 불일치는 오류로 중단한다.

## 판정 층

출력은 다음을 별도 열로 둔다.

| 필드 | 뜻 |
| --- | --- |
| `graph_complete` | 고정 뷰어의 허용 행동열을 끝까지 열거했는가 |
| `mode_semantic_complete` | 입력 작성자가 이 mode의 필요 조건·예외를 모두 정의했다고 명시했는가 |
| `missing_inputs` | 기준 판독에 필요한 원자료·판·입력이 아직 없는가 |
| `outside_corpus_intervals` | 알고 있는 필수 구간이 봉인 corpus 밖에 있는가 |
| `interval_reachability` | 현재 제공된 필수 구간의 위치 포함 여부 |
| `semantic_reachability` | 완전하다고 선언한 gold까지 감안한 고정 뷰어 내 판정 |

`semantic_complete`는 mode에서 case의 `semantic_gold_complete`를 상속하고, 명시한 mode 값으로 덮어쓸 수 있다. 따라서 전체 예외 기준이 미완성이어도 조작만의 기준이 완성되었다면 operation에만 true를 쓸 수 있다. 미지정은 false와 마찬가지로 semantic 판정을 unknown으로 유지한다. 도구는 이 선언의 진실성을 검증하지 않으므로 기준 판독자의 근거가 별도로 필요하다.

`missing_inputs`는 case 또는 mode에 둘 수 있다. 항목이 `{"required_for":["full"], ...}`이면 지정 mode에만 적용한다. 단순 문자열은 해당 scope의 모든 mode에 적용한다. missing input이나 불완전 gold가 있으면 현재 제공한 구간을 모두 덮어도 **semantic reachability는 unknown**이다.

구간에 `outside_corpus:true`를 넣거나 corpus에 없는 `doc_id`를 쓰면 corpus 밖 구간으로 표시한다. **정확히 알고 있는 필수 구간이 허용 corpus 밖에 있다는 사실**은 fixed viewer에서의 불가능 사유가 될 수 있다. 이는 아직 읽지 못한 원자료라는 의미의 `missing_inputs`와 다르다. 외부 구간의 위치·필수성조차 미확정이면 missing input과 불완전 gold로 표시해야 한다. 출력은 unrestricted web reachability를 항상 `not_evaluated`로 유지한다.

도달 경로 하나를 실제로 찾으면 graph 열거가 덜 끝났더라도 현재 구간의 양성 증인이 된다. 반대로 no-match를 불가능으로 바꾸려면 graph가 완전하고, 요구 구간이 유효하며, gold가 완전하고, 해당 mode의 missing input이 없어야 한다.

## 실행과 출력

```sh
python -B docs/workstreams/research/AF-RES-116/viewer/analyze_coverage.py \
  --requirements docs/workstreams/research/AF-RES-116/gold-intervals.json \
  --corpus docs/workstreams/research/AF-RES-116/corpus.json.gz \
  --raw-root docs/workstreams/research/AF-RES-116/reachability/raw \
  --out-dir docs/workstreams/research/AF-RES-116/reachability/coverage-v1
```

이미 있는 출력 디렉터리는 덮어쓰지 않는다. 기준을 고쳤으면 새 판의 입력과 새 출력 디렉터리를 사용한다.

- `coverage-summary.json`: mode별 실제 분모, 모든 대안의 정규화 결과, match 수/깊이별 수, 최소 개봉 수, 정확한 증인 action열·누적 구간·표시 지문, 각 한계와 입력 SHA.
- `matching-paths.jsonl.gz`: **일치하는 모든 열거 경로**. 1–3단계 prefix와 후속 재열람도 각각 행으로 남기므로 전체 행 수를 독립 사건·독자로 해석하지 않는다. `earliest_depth`와 깊이별 건수를 함께 본다. gzip `mtime=0`을 사용한다.

같은 문서의 겹치거나 맞닿은 구간은 합친다. `[0,10)`과 `[10,20)`은 `[0,20)`을 덮지만 `[0,10)`과 `[11,20)`은 한 글자의 미노출 공백이 있으므로 덮지 못한다. 다른 문서의 구간으로 그 공백을 채울 수도 없다.

```sh
python -B docs/workstreams/research/AF-RES-116/viewer/test_coverage.py
```

합성 검사만 실행하며, 문서면·원 꾸러미·작성자 메모·자연 사건 정답을 읽지 않는다. 검사 영수증은 `coverage-synthetic-checks.json`이다. 기존 `reader.py`와 corpus는 수정하지 않는다.
