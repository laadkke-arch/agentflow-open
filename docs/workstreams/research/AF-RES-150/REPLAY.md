# 오프라인 재생 영수증

Linux 클라우드 checkout, Git 2.56.1, Python 3.12.14, SQLite 3.53.1에서 실행했다. 수집은 웹 원문을 열어 별도로 수행했다. 실행기는 표준 라이브러리와 저장된 입력만 사용한다. SQLite 파일은 실행마다 새 디렉터리에서 방식·시나리오마다 분리했다.

## 입력과 출력 지문

| 파일 | SHA-256 |
| --- | --- |
| [cases.jsonl](cases.jsonl) | `4f1ff4a9f534debf754a0ce557ae820bbfd8d9d0262d1fdbe746de819a8e8083` |
| [sources.jsonl](sources.jsonl) | `f58611d6a126313707c65abf52787521fbb087d9dc00ee97e31ec2de495fdc1b` |
| [replay.py](replay.py) | `9c70817d41b1663258078130ba4e34b18dc2d41cc3da0526991f49dd4a1585fa` |
| [answers.csv](answers.csv) | `c933a7268d797d11a42b2d701e9f8e5ef0c1731a291547b481a1769c2de879e8` |
| [costs.csv](costs.csv) | `7134d87fbffb15ce6735588ca2ecced11a8361423c316274bad56f8f3ad29ec6` |

저장소 루트에서 스크립트를 실행했다. 다음은 실행에 쓴 빈 디렉터리 패턴과 비교 명령이다. 성공한 기본 실행 두 번과 역순 조회 실행 모두 종료 0, 16사례 / DB 23개 / 답 5,336행 / 비용 391행이었다. `cmp` 네 건도 종료 0이다. `row_id` 정렬 CSV 전체의 지문을 비교했다. Python·SQLite 버전이 다르면 페이지 할당 크기가 달라질 수 있다.

```sh
set -eu
AF150_PATH=docs/workstreams/research/AF-RES-150
AF150_A=$(mktemp -d /tmp/af150-final-a-XXXXXX)
AF150_B=$(mktemp -d /tmp/af150-final-b-XXXXXX)
AF150_D=$(mktemp -d /tmp/af150-final-order-XXXXXX)
PYTHONDONTWRITEBYTECODE=1 python "$AF150_PATH/replay.py" --out "$AF150_A"
PYTHONDONTWRITEBYTECODE=1 python "$AF150_PATH/replay.py" --out "$AF150_B"
PYTHONDONTWRITEBYTECODE=1 python "$AF150_PATH/replay.py" --reverse-queries --out "$AF150_D"
for other in "$AF150_B" "$AF150_D"; do
  cmp "$AF150_A/answers.csv" "$other/answers.csv"
  cmp "$AF150_A/costs.csv" "$other/costs.csv"
done
cmp "$AF150_PATH/answers.csv" "$AF150_A/answers.csv"
cmp "$AF150_PATH/costs.csv" "$AF150_A/costs.csv"
sha256sum "$AF150_PATH"/{cases.jsonl,sources.jsonl,replay.py,answers.csv,costs.csv}
```

첫 `--suite main` 실행은 보강 조회 이전 660행, 보강 뒤 684행이었다. 첫 전체 실행은 N05 관계 제거 시 선택 필드가 빠진 행을 비교하는 분기에서 `KeyError: 'right'`, 종료 1이었다. 관계 없는 공지의 선택 필드를 검사하도록 수정한 뒤 새 빈 디렉터리에서 다시 실행했다. 이후 안정 대조의 두 번째 주소를 저장하지 않는 대조를 추가해 최종 5,336행을 재생했다.

## 관측 분리와 재계산

| 구분 | 시행 | 확인 기준 |
| --- | --- | --- |
| 자연 재생 | 날짜로 가린 초기 입력과 후속 입력을 방식별 DB에 전달 | `normal/*/*/pre|post/*`의 F/L/T/A 384행. post의 P 48행은 별도 집계. |
| 사후 과거 조회 | 후속 입력을 저장한 DB에 같은 과거 질문 | `lookback` 192행. N01의 배포–발표 사이를 전후로 다시 물은 `pre-announcement`와 `announcement-lookback` 12행씩. |
| 후속 유입 | Atom/Pulsar, React, PREDIMED 새 관측을 별도 인용으로 질의 | `new-citation` 36행. 기존 인용의 actor와 새 인용의 actor를 분리. |
| 조회 요청 순서 | 같은 실행에서 F/L/T/A의 요청만 뒤집음 | 정상 답·비용 CSV에 바이트 차이 0. |
| 중복 전달 | 케이스의 입력을 같은 순서로 한 번 더 수신 | `duplicate`의 답 내용·근거·판정 변화 0. A 행 쓰기 38→76, B/C 52/60 유지. 남은 행 36/52/60. |
| 역순 정정 전달 | 각 사건 후속 묶음에서 문서는 같은 자리에 두고 관계·공지 전달만 역순 | `reverse`에서 A의 N06 L 두 행 변화. 당시 조회 오류 하나가 우연히 없어지고 현재 조회 오류 하나가 생겼다. B/C 변화 0. |
| 실패 및 재실행 | N12 후속 transaction의 첫 쓰기 뒤 예외, rollback, SQLite 연결 닫기/다시 열기, 원 묶음 재실행 | 각 방식 실제 중단 1, abort 쓰기 1. 중단 전후 DB 행 지문 동일. 비교 가능한 최종 답·근거·판정과 남은 행 모두 정상본과 일치. |
| 고의 오류와 취소 | N04 거짓 별칭, N06 거짓 분리, 각 선언 ID만 취소 | `bad-link/C/N04|N06/injected|repaired/L|P` 8행. C의 네 오답이 원래 결과와 일치하도록 복구. 취소 생략에서는 네 오답 유지. |
| 필드 제거 | pin, scope, authority, available을 독립적으로 하나씩 생략 | `without-*/C`을 정상 C와 같은 `case_id, checkpoint, query_id`로 맞춘다. 취소만 정상 C 대신 오류 구성 C와 맞춘다. |
| 개별 관계 제거 | N05.3 이동의 방향만 생략하고 공지·주체 보존. N06.4 전달 관계 생략 | 변경 단위 각각 한 관계. 이동 L과 두 판의 근거, 이관 L과 주소 동일 판단이 각 두 행씩 달라진다. |
| 주소 한 개 | A에 같은 입력을 주고 안정 대조의 두 번째 주소 쓰기만 생략 | F/L/T/A 32/32 일치, post P 근거 소실 4/4. 대조의 행·성공 쓰기 8→4, 논리 바이트 2,098→1,051. |

확장 실험의 `X01`, `X02`는 작업자가 구성한 전달과 취소다. `9999-01-01/02`는 격리한 실험용 순서값이다. 이 행을 자연 사건·원문 분모에서 제외했다. `delivered`는 전달 ID 전체이며, 저장소에서 실제 반환한 근거는 `actual_sources`다. 최초와 발표 전, 실패 직후에는 원장으로 알 수 있었던 사건만 전달했는지 날짜와 ID를 확인했다. N01에서 발표일을 빼면 과거 시점 L/A 두 답에 S01a가 들어온다. 초기에 아직 그 이벤트가 전달되지 않은 DB에서는 두 값이 그대로다.

재계산은 원장 행의 고유 ID와 아래 필터를 다시 센다. 상세 결과는 [SELF_CHECK.md](SELF_CHECK.md)와 CSV 행에서 교차 확인했다.

```sh
PYTHONDONTWRITEBYTECODE=1 python - docs/workstreams/research/AF-RES-150 <<'PY'
from collections import Counter
import csv, json, sys
from pathlib import Path
d = Path(sys.argv[1])
def read(name):
    return [json.loads(line) for line in (d / name).read_text().splitlines()]
def table(name):
    with (d / name).open() as stream:
        return list(csv.DictReader(stream))
sources = read('sources.jsonl')
cases = read('cases.jsonl')
a = table('answers.csv')
c = table('costs.csv')
counted = [row for row in sources if row['count']]
assert len({s['work_id'] for s in counted}) == len(counted)
assert all(s['access'] == 'direct' for s in counted)
print('sources', len(sources), len(counted), Counter(s['counting_role'] for s in counted))
print('publisher families', len({s['publisher_family'] for s in counted}))
print('cases', Counter((x['kind'], x['domain']) for x in cases))
for m in 'ABC':
    for stage in ['pre', 'post']:
        rows = [r for r in a if (r['scenario'], r['model'], r['checkpoint']) == ('normal', m, stage)]
        print(m, stage, Counter(r['verdict'] for r in rows if r['query_id'] != 'P'))
        if stage == 'post':
            print(m, 'pairs', Counter(r['verdict'] for r in rows if r['query_id'] == 'P'))
print('normal costs', [r for r in c if r['scenario'] == 'normal' and r['case_id'] == 'ALL'])
PY
```

## 좁은 기능 대조

Python 3.12.14에서 `type(range(1,0)).__name__`는 `range`, `repr`은 `range(1, 0)`, `list(range(1,0))`는 `[]`였다. `range(1, 0, step=1)`은 `TypeError`였다. 과거 Python의 직접 호출은 S07a/S07d의 고정 예제를 읽었으며 역사 binary는 실행하지 않았다. [2.5.2 예제](https://docs.python.org/release/2.5.2/lib/built-in-funcs.html) · [3.14 Ranges](https://docs.python.org/3.14/builtins/stdtypes.html#range).

```sh
python - <<'PY'
r = range(1, 0)
assert type(r) is range and list(r) == []
print(type(r).__name__, repr(r), list(r))
try:
    range(1, 0, step=1)
except TypeError as error:
    print(type(error).__name__, str(error))
else:
    raise AssertionError('step unexpectedly accepted by keyword')
PY

node <<'JS'
"use strict";
function Legacy() {
  this.count = 0;
  this.total = 0;
}
function visit(items, state) {
  items.forEach(function add(value) {
    this.count++;
    this.total += value;
  }, state);
  return [state.count, state.total];
}
class Modern {
  count = 0;
  total = 0;
}
for (const version of [Legacy, Modern]) {
  const result = visit([2, 5, 9], new version());
  process.stdout.write(version.name + ": " + JSON.stringify(result) + "\n");
  if (result[0] !== 3 || result[1] !== 16) process.exitCode = 1;
}
JS
```

Node v24.22.3의 두 구성 입력은 각각 `[3,16]`, 종료 0이었다. 공통 콜백 메커니즘만 실측했다. 오래된 브라우저에 인라인 polyfill을 삽입하거나 양쪽 문서의 호환 범위를 실행하지 않았다. 해당 실행에는 역사 브라우저와 es 페이지의 Polyfill 절이 필요하다. [MDN es 본문](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach#polyfill) · [MDN en-US 본문](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach).

다른 외부 프로젝트의 서비스 구동은 미실시다. 예를 들어 Compose 이름 확인을 실사용에서 반복하려면 Docker 데몬과 고정 V1 1.29.2, V2 v2.0.0에 `name`/ `container_name` 없는 `services: {web: {image: busybox}}`를 주고 `docker-compose -p demo up -d`와 `docker compose -p demo up -d`를 각각 새 프로젝트에서 수행한 뒤 `docker ps --filter label=com.docker.compose.project=demo --format '{{.Names}}'`로 확인한다. 실제 기동에는 종료되지 않는 서비스 명령을 더 포함해야 한다. 이 연구는 고정 소스의 이름 함수만 판독했다. [V1 소스](https://raw.githubusercontent.com/docker/compose/1.29.2/compose/service.py) · [V2 소스](https://raw.githubusercontent.com/docker/compose/v2.0.0/pkg/compose/convergence.go).

Open Library 원 거래·revision 비교, Ostrom 1970 본문, NEJM notice PDF를 열지 못했다. 그 URL과 대체 근거는 S08c/d, S11c, S12c에 보존했다. 초기 셸의 외부 자료 조회는 HTTPS tunnel 403이었으며 위 자료 원문 열람은 별도 웹 도구의 본문 확인으로 기록했다. 임의의 외부 브라우저의 상태나 서버의 영구 가용성을 추정하지 않았다.
