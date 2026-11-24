# AF-RES-116 재현 절차

이 문서는 **선택한 RESULT commit에 저장된 입력·관측 원장·의미 판정에서 파생 결과를 결정론적으로 재생하는 절차**다. 새 AI 수신자의 선택이나 새 사람의 판독을 반복하는 절차가 아니다. `readers/`의 원 답변과 `evaluation/judgments-*.jsonl`의 의미 판단은 재생의 입력으로 보존한다. 스크립트를 다시 실행해도 새로운 독립 독자나 평가자가 생기지 않는다.

재현 대상값은 **사용자가 checkout한 RESULT commit에서 실행한 `git rev-parse HEAD`의 실제 출력**이다. 이 문서 작성 시 아직 정해지지 않은 첫 원격 RESULT SHA를 임의 값이나 commit placeholder로 적지 않는다. 아래 기록의 수신 봉인 SHA `47e8d24ad9c0313f6d1a361882198f42307a0d5d`는 원 관측의 선행 봉인이며 RESULT SHA를 대신하지 않는다.

## 1. 실행 전제와 대상 기록

이미 확보한 저장소의 RESULT commit을 별도 재현용 checkout으로 준비하고, 그 저장소 최상위에서 시작한다. Python 3.12 이상과 Git이 필요하다. 고정 archive 복원·뷰어·그래프·원장·색인 검산 경로는 Python 표준 라이브러리를 사용하며 외부 웹 재수집이 필요하지 않다. 역사판 Pandoc/ImageMagick/TeX 실행은 7절의 별도 미실행 계획이다.

```sh
export AF116_REPO="$(git rev-parse --show-toplevel)"
export AF116_OWN="$AF116_REPO/docs/workstreams/research/AF-RES-116"
export AF116_RESULT_COMMIT="$(git rev-parse HEAD)"
git rev-parse HEAD
git status --short
python --version
date -u '+%Y-%m-%dT%H:%M:%SZ'
```

실행 기록에 `AF116_RESULT_COMMIT`, 시작/종료 UTC, 실제 실행 주체, Python/Git 판, 명령, 종료 코드, stdout/stderr와 생성물의 SHA-256을 남긴다. 수정된 checkout이라면 commit과 작업 트리 차이를 함께 기록한다. 환경이 제공한 UTC는 외부 시각 인증이 아니다.

주체·제공 문맥의 근거는 [역할 기록](evidence/roles.json), [수신자 실행 기록](evidence/reader-launches.jsonl), `readers/*/events.jsonl`, `evaluation/evaluator-*.json`이다. 원 AI 수신과 가림 평가는 당시 제공된 문맥과 도구 기록의 범위에서 해석한다. 모델 seed는 이 재생 절차의 입력이 아니며, 새 모델 출력의 동일성은 보장하지 않는다. 공유 파일시스템의 경로 제한과 금지 파일 미열람 절차를 OS 격리라고 부르지 않는다. 사람 참여·능동 독해시간·시간 단축을 관측한 시험으로 해석하지 않는다.

이 문서의 명령 검토는 `/root/evaluate_imagemagick`가 가림 판정 파일을 완료한 뒤 별도 문서작성 역할로 수행했다. **2026-11-24 UTC, Python 3.12.14**에서 5절의 여섯 기존 `--check` 명령은 모두 종료 코드 0이었다. 이는 아직 만들어지지 않은 RESULT commit 전체의 최종 검사를 뜻하지 않는다. 가림 평가 파일은 이 문서작성 과정에서 수정하지 않았다.

## 2. 고정 archive 복원과 입력 해시

복원기는 다음 archive를 읽어 AF-RES-116 내부에 원래 상대경로로 복원한다.

| archive | 색인 | 내용 |
| --- | --- | --- |
| `evidence/document-cache.tar.gz` | `evidence/document-cache-index.json` | 고정 문서, 변환물, 매핑과 캡처 영수증 |
| `reachability/raw-enumeration.tar.gz` | `reachability/raw-index.json` | 6개 시작점의 고정 `paths.jsonl`, `views.jsonl`, `summary.json` |
| `evidence/reference-cache/*.tar.gz` | `evidence/reference-cache/index.json` | 기준 판독 스냅샷·발췌·첨부 입력 및 보조 기록관 자료 |

```sh
python -B "$AF116_OWN/analysis/restore_caches.py"
```

`restore_caches.py`는 네트워크를 사용하지 않는다. 경로 탈출과 일반 파일이 아닌 archive 항목을 거절하며, 이미 존재하는 파일은 byte가 같을 때만 유지한다. 다른 byte가 있으면 덮어쓰지 않고 실패한다. 따라서 복원 실패를 없애려고 원자료를 임의 편집하지 말고, RESULT commit과 작업 트리 차이를 먼저 확인한다.

복원 후 archive 자체와 각 복원 파일을 세 색인에 대조한다. 아래 코드는 읽기만 한다.

```sh
python -B - <<'PY'
import hashlib, json, os
from pathlib import Path

root = Path(os.environ['AF116_OWN'])
archives = []
files = []
for name in ['evidence/document-cache-index.json',
             'reachability/raw-index.json',
             'evidence/reference-cache/index.json']:
    index = json.loads((root / name).read_text())
    if 'archives' in index:
        archives.extend(index['archives'])
    else:
        archives.append({'path': index['archive'],
                         'sha256': index.get('archive_sha256', index.get('sha256'))})
    files.extend(index['files'])
for item in archives + files:
    raw = (root / item['path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == item['sha256'], item['path']
    if 'bytes' in item:
        assert len(raw) == item['bytes'], item['path']
print(json.dumps({'archives_checked': len(archives),
                  'file_entries_checked': len(files), 'match': True}))
PY
```

수신 원장과 뷰어가 고정한 핵심 해시는 다음과 같다. 이것들은 RESULT commit SHA와 다른 종류의 입력 식별자다.

| 파일 | SHA-256 |
| --- | --- |
| `corpus.json.gz` | `a2507268ef20cc0b9dc55b351b44e7973961e352f17f86dbb3b2b01dc3127b2d` |
| `viewer/reader.py` | `0c4bb759ea0e3738903176d79ff24f0d96a34e6073c14a2b0b63ff1be35a1d81` |
| `packets.jsonl` | `7f234fe1e1a53fe35e53aa0ca6e669dfa6eb47c58eba6e4c46288ad76ccffde3` |
| `trails.jsonl` | `9f924fe529b20d1b726190d7a48e7541dba86feafd93348c1a15360e6663a578` |

## 3. 뷰어·그래프와 교정 경로 재생

### 합성 검사

다음 명령은 실제 존재하는 합성 검사다. 자연 사건·수신자 수에 더하지 않는다. 각각 자기 검사 영수증을 새 UTC로 쓰므로 **재현용 checkout에서** 실행하고, 새 영수증을 원 관측 시각의 기록과 혼동하지 않는다.

```sh
python -B "$AF116_OWN/viewer/test_reader.py"
python -B "$AF116_OWN/viewer/test_coverage.py"
python -B "$AF116_OWN/analysis/test_collect_trials.py"
```

영수증을 다시 쓰지 않고 같은 합성 검사를 수행하려면 다음 `unittest` 진입점을 사용할 수 있다. 최종 공통 `--require-clean` 검사를 같은 checkout에서 할 때 이 경로를 사용하거나 별도의 깨끗한 checkout을 준비한다.

```sh
python -B -m unittest discover -s "$AF116_OWN/viewer" -p 'test_*.py' -v
python -B -m unittest discover -s "$AF116_OWN/analysis" -p 'test_collect_trials.py' -v
```

표시 한도는 개봉당 전체 1,500 Unicode code point, source slice 최대 1,350자이며 첫 면을 포함해 최대 3개봉이다. 실제 링크 토큰이 경계에 걸리면 그 면의 source slice는 더 짧아질 수 있다. `content_*`와 `total_navigation_*`가 겹치지 않는 비용 분해이고, 과거 이름 `body_*`에는 문서 목차도 포함된다. 자세한 계약은 [viewer/README.md](viewer/README.md)와 [analysis/README.md](analysis/README.md)에 있다.

### 여섯 시작점 전수 열거

출력 경로는 뷰어 코드가 AF-RES-116 내부로 제한한다. 매번 새 디렉터리를 만들고 봉인된 `reachability/raw/`에 쓰지 않는다.

```sh
export AF116_REPLAY="$(mktemp -d "$AF116_OWN/replay.XXXXXXXX")"
for AF116_PAIR in P1:p2192 P2:p383 P3:p21403 I1:i7113_processing I2:i7114_processing I3:i7116_processing
do
    AF116_CASE=${AF116_PAIR%%:*}
    AF116_START=${AF116_PAIR#*:}
    python -B "$AF116_OWN/viewer/enumerate_paths.py" \
        --corpus "$AF116_OWN/corpus.json.gz" \
        --start-doc "$AF116_START" \
        --max-nodes 200000 \
        --out "$AF116_REPLAY/raw/$AF116_CASE"
done
```

`paths.jsonl`과 `views.jsonl`은 고정 graph와 byte 단위로 비교한다. summary는 실제 재실행 시각과 실행 소요만 제외하고 비교한다. `enumeration_complete=false`를 도달 불가능으로 바꾸면 안 된다.

```sh
python -B - <<'PY'
import json, os
from pathlib import Path

root = Path(os.environ['AF116_OWN'])
replay = Path(os.environ['AF116_REPLAY'])
for case in ['P1', 'P2', 'P3', 'I1', 'I2', 'I3']:
    old, new = root / 'reachability/raw' / case, replay / 'raw' / case
    for name in ['paths.jsonl', 'views.jsonl']:
        assert (old / name).read_bytes() == (new / name).read_bytes(), (case, name)
    a, b = [json.loads((directory / 'summary.json').read_text())
            for directory in [old, new]]
    for value in [a, b]:
        value.pop('created_utc', None)
        value.pop('command_wall_seconds', None)
    assert a == b, case
    assert b['enumeration_complete'] is True, case
    print(case, b['nodes'], b['distinct_views'], 'match')
PY
```

고정 summary의 `(경로 노드, 고유 표시)`는 P1 `(2826, 163)`, P2 `(2805, 157)`, P3 `(3045, 167)`, I1/I2 각각 `(179, 66)`, I3 `(175, 64)`다. 길이 1–3의 prefix와 재열람 경로를 별도로 센 수치이며 독자 수가 아니다.

### 사전 고정 교정 경로

K1/K2의 기대 구간은 [calibration/preregistered-cases.json](calibration/preregistered-cases.json)에 있다. 아래는 이미 고정한 선택열의 결정론적 재생이다. 새 수신자 선택·소프트웨어 실행으로 기록하지 않는다.

```sh
python -B "$AF116_OWN/viewer/enumerate_paths.py" \
    --corpus "$AF116_OWN/corpus.json.gz" --start-doc p383 \
    --witness '["open","n3l3","n3l5"]' --out "$AF116_REPLAY/K1-witness.json"
python -B "$AF116_OWN/viewer/enumerate_paths.py" \
    --corpus "$AF116_OWN/corpus.json.gz" --start-doc p383 \
    --witness '["open","n3l10"]' --out "$AF116_REPLAY/K2-witness.json"
python -B "$AF116_OWN/viewer/enumerate_paths.py" \
    --corpus "$AF116_OWN/corpus.json.gz" --start-doc p383 \
    --witness '["open","n3l19","next"]' --out "$AF116_REPLAY/K2-near-wrong.json"
```

각 결과에서 `created_utc`만 빼고 같은 이름의 `calibration/` 고정 JSON과 비교한다. K1/K2의 양성 경로 및 K2의 근접하지만 잘못된 경로를 자연 6건의 성공 분모에 추가하지 않는다.

## 4. 공급된 gold 구간의 coverage 검산

봉인된 raw graph에 대해 자연 사건과 교정 사건을 각각 새 경로로 계산한다. 코드가 graph/corpus 해시, view 문자열 지문·길이, path/view offset, 요약 건수를 검증한다.

```sh
python -B "$AF116_OWN/viewer/analyze_coverage.py" \
    --requirements "$AF116_OWN/gold-intervals.json" \
    --corpus "$AF116_OWN/corpus.json.gz" \
    --raw-root "$AF116_OWN/reachability/raw" \
    --out-dir "$AF116_REPLAY/coverage-natural"
python -B "$AF116_OWN/viewer/analyze_coverage.py" \
    --requirements "$AF116_OWN/calibration/coverage-input.json" \
    --corpus "$AF116_OWN/corpus.json.gz" \
    --raw-root "$AF116_OWN/reachability/raw" \
    --out-dir "$AF116_REPLAY/coverage-calibration"
```

새 coverage와 고정 결과는 아래와 같이 비교한다. UTC·wall duration·실제 checkout 경로는 실행마다 달라진다. gzip 컨테이너는 Python/zlib 판에 따라 헤더가 달라질 수 있으므로 match 원장은 압축 해제한 byte를 비교하고, archive 원본의 해시는 2절에서 별도로 확인한다. 구간·판정·증인·분모·입력 해시는 비교에서 제외하지 않는다.

```sh
python -B - <<'PY'
import copy, gzip, json, os
from pathlib import Path

root = Path(os.environ['AF116_OWN'])
replay = Path(os.environ['AF116_REPLAY'])
def stable(value):
    value = copy.deepcopy(value)
    for key in ['started_utc', 'finished_utc', 'wall_seconds', 'matching_paths_sha256']:
        value.pop(key, None)
    value['requirements_input'].pop('path', None)
    for item in value['graph_inputs']:
        item.pop('path', None)
    for item in value['results']:
        item.pop('graph_directory', None)
    return value

for old, new in [(root / 'reachability/coverage-v1', replay / 'coverage-natural'),
                 (root / 'calibration/coverage', replay / 'coverage-calibration')]:
    assert stable(json.loads((old / 'coverage-summary.json').read_text())) == \
           stable(json.loads((new / 'coverage-summary.json').read_text()))
    assert gzip.decompress((old / 'matching-paths.jsonl.gz').read_bytes()) == \
           gzip.decompress((new / 'matching-paths.jsonl.gz').read_bytes())
    print(old.name, 'coverage match')
PY
```

**판정 경계:** [build_gold_index.py](analysis/build_gold_index.py)의 `OUTSIDE_P1` 등의 `[0,1)`은 외부 필수 근거가 봉인 corpus에 없다는 **존재 표지**다. 원 논문·규격·코드의 실제 0–1 문자 위치가 아니다. 실제 line/page/file 위치와 source ID는 `gold.csv`의 `external_evidence`, 각 `gold-work/*/gold.json`, 출처 원장에 보존돼 있다. 이 표지와 입력 작성자의 semantic completeness 선언을 분석기가 독립적으로 의미 검증하지는 않는다.

따라서 `unreachable_in_fixed_viewer`는 공급된 완전 요구조건과 고정 뷰어의 범위에 한정한다. 전체 웹이나 원 소프트웨어에서의 불가능을 뜻하지 않는다. P3의 원 rendering 환경, I3의 원 JP2처럼 필수 입력이 미해결이면 full 의미 판정은 `unknown`을 유지한다. 근접 본문 target·개별 span 도달을 완전한 O/P/필수 E 답변 성공으로 합치지 않는다.

## 5. 18세션 원장 → 출처·gold·가림 입력 검산

아래 여섯 명령의 `--check`는 파생 파일을 다시 계산하여 저장본과 대조한다. 순서대로 실행하면 무엇이 앞 단계의 입력인지 분명해진다.

```sh
python -B "$AF116_OWN/analysis/collect_trials.py" --check
python -B "$AF116_OWN/analysis/build_recipient_sources.py" --check
python -B "$AF116_OWN/analysis/build_sources.py" --check
python -B "$AF116_OWN/analysis/build_gold_index.py" --check
python -B "$AF116_OWN/analysis/export_reachability.py" --check
python -B "$AF116_OWN/analysis/prepare_masked_evaluation.py" --check
```

| 명령 | 주 입력 → 대조할 파생물 | 무엇을 확인하지 않는가 |
| --- | --- | --- |
| `collect_trials.py --check` | packets + 원 `events.jsonl` + 고정 renderer → `trails.jsonl`, `trial-slots.jsonl`, `citation-checks.jsonl`, `trial-summary.json` | 의미 정답, 실제 문맥 독립성, 사람 시간 |
| `build_recipient_sources.py --check` | trails → `evidence/recipient-source-reads.jsonl` | 재열람을 새 저작으로 추가하지 않음 |
| `build_sources.py --check` | 역할별 원장 → `sources.jsonl`, `source-counts.json`, `source-inventory.csv` | 다운로드·같은 저작의 앵커/미러 수를 독립 저작 수로 바꾸지 않음 |
| `build_gold_index.py --check` | 봉인된 양 분야 gold/target → `gold.csv`, `gold-intervals.json` | 새 기준 판독 또는 역사판 실행 |
| `export_reachability.py --check` | 고정 coverage + raw views → `reachability.jsonl` | 실제 독자의 선택·정답 |
| `prepare_masked_evaluation.py --check` | 봉인 trails + reference → 두 masked 입력, masking map, input receipt | `judgments-*.jsonl`의 의미 판정을 자동 생성하지 않음 |

`collect_trials.py --check`는 새 `collected_utc`만 비교에서 제외한다. 그 밖의 해시 체인·순서·허용 선택·실제 표시 재계산·비용·답 연결·계획자리 값은 검산한다. 문서작성 시 확인된 원장은 18꾸러미/54자리 모두 관측·답변·완료, 유효한 표시 54개, 인용 95개 중 정확 노출 일치 94개와 불일치 1개였다. `strict_supported`는 인용문 존재/주소 검사이며 주장의 의미적 충분성은 아니다.

파생 파일을 실제로 다시 쓰려면 재현용 checkout에서 다음을 실행할 수 있다. 원 `readers/`, packets, corpus와 의미 판정은 변경하지 않는다. `collect_trials.py --write`의 새 수집 UTC는 원 노출 UTC와 구별한다.

```sh
python -B "$AF116_OWN/analysis/collect_trials.py" --write
python -B "$AF116_OWN/analysis/build_recipient_sources.py"
python -B "$AF116_OWN/analysis/build_sources.py"
python -B "$AF116_OWN/analysis/build_gold_index.py"
python -B "$AF116_OWN/analysis/export_reachability.py"
python -B "$AF116_OWN/analysis/prepare_masked_evaluation.py"
```

`gold-work/*/build_gold.py`는 기준 판독자가 작성한 내용의 작성 스크립트다. RESULT 재생에서는 봉인된 `gold.json`을 입력으로 사용한다. 작성 스크립트를 실행하는 것만으로 원문을 새로 읽거나 gold의 의미가 독립 재검증되는 것은 아니다. 기존 가림 평가자에게 unmasked 자료를 보여 준 뒤 같은 평가를 새 독립 가림 평가라고 다시 세지 않는다.

### 표 재구성과 연구 전체 검사: 구현 상태

두 스크립트는 최종 결과 작성 중 구현됐으며 CLI를 확인했다. 결과 고정 전 점검에서 `build_results.py --check`와 `check_study.py --skip-reenumeration`이 통과했다. 이는 최종 결과 SHA의 인수 검사를 대신하지 않는다. 고정 결과판의 전수 재생·검사 결과는 `evidence/acceptance-evidence.json`에 따로 기록한다.

| 명령 | 실제 역할 | 관측 경계 |
| --- | --- | --- |
| `python -B "$AF116_OWN/analysis/build_results.py" --check` | `answers.csv`, `pairs.csv`, `metrics.json`, `RESULT.md`, `analysis/report-tables.md` byte 재계산 대조 | 기존 가림 의미 판정을 고정 입력으로 쓴다. |
| `python -B "$AF116_OWN/analysis/check_study.py"` | 봉인 입력33개, 실제18경로·54문서면, 여섯 그래프9,209경로 전수 재생, 기준50mode, 교정, 평가인용125개, 분모·필수표·링크 종합 검사 | 새 독자/평가자나 역사 바이너리 실행이 아니다. 기본값은 전체 경로 재열거이고 `--skip-reenumeration`은 명시적 축소 검사다. |

표 재생은 `evaluation/judgments-pandoc.jsonl`, `evaluation/judgments-imagemagick.jsonl`과 evaluator receipt를 고정 입력으로 사용해야 한다. 가림 입력의 재생성과 의미 판정의 재실시는 서로 다른 작업이다. A/B/C 매핑을 되붙여 집계하더라도 evaluator가 그 매핑을 보면서 판단한 것으로 역사를 바꾸지 않는다.

존재가 확인된 `build_results.py`는 인자 없이 실행하면 위 다섯 파생물을 쓰고, `--check`이면 byte를 비교한다. `analysis/interpretation.md`의 작성된 해석문도 입력이므로 표를 생성했다고 해석문이 새 독립 평가로 검증되는 것은 아니다.

## 6. 원문 파싱·비용·공통 검사 한계

[viewer/corpus-build.json](viewer/corpus-build.json)은 214개 문서의 기계 캡처/DOM 매핑을 기록한다. Pandoc은 역사판 `MANUAL.txt`를 설치된 **3.1.11.1 renderer**로 HTML화했고 기본 TOC depth 3을 사용했다. 역사판의 웹 HTML/CSS나 브라우저 화면을 복원한 것이 아니다. ImageMagick은 각 고정 upstream commit의 직접 `www/*.html` 허용목록을 사용한다. 제외된 외부 링크·API/하위경로와 누락 fragment는 [excluded-links 원장](documents/excluded-links.jsonl)에 남는다.

HTML entity·공백을 정규화하고 링크 ID를 삽입했다. `documents/mappings/`의 source node line/column은 역추적을 돕지만 정규화 후 모든 문자와 원 HTML byte가 일대일 대응하지 않는다. 이미지의 픽셀·도표는 표시하지 않았고 alt text만 들어갈 수 있다. 따라서 문자열 검색 미발견, 허용목록 밖 목적지, 파싱에서 비활성화된 링크를 전체 공식 문서의 의미상 부재로 해석하지 않는다. 비용은 이 변환/뷰어에서 실제 보인 문자의 비용이다.

`viewer/build_corpus.py --build`는 실제 존재하는 재작성 명령이지만 정규 검산 경로에 넣지 않는다. corpus·매핑·build receipt를 다시 쓰므로 새 버전의 변환 실험으로 구분해야 한다. 기본 재현은 이미 고정된 corpus/archive의 해시와 renderer의 재계산을 사용한다. `--capture-im`, `fetch_public.py`, 모집·외부 캡처 스크립트는 외부 자료를 다시 받는 경로이므로 이 오프라인 재현에서 실행하지 않는다.

UTC 노출→답, 답→선택, 선택→노출 차이는 도구 호출·대기·스케줄 지연이 포함된 wall duration이다. 이를 사람의 능동 읽기 시간이나 절약 시간으로 변환하지 않는다. 해시 체인은 변경 탐지를 돕지만 외부 시각 인증·저자 서명·모든 파일 접근의 감사를 제공하지 않는다. 뷰어의 `arrival_url`도 고정 문서에서 복원한 source locator이며 실제 HTTP 도착 관측은 아니다.

저장소 공통 검사는 저장소 최상위에서 다음과 같이 실행할 수 있다. 연구 전용 coverage/평가의 의미를 대신 검증하는 명령은 아니다.

```sh
cd "$AF116_REPO"
python -B -m workbench.session check "$AF116_OWN/manifest.json" --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

세션 검사에서 `--fetch`를 생략한 검사는 로컬 ref 기준이며 원격 최신성 확인으로 보고하지 않는다. `cloud_check.py`의 환경 이름은 호출자가 붙인 표지이고 특정 계정/제품 통합을 증명하지 않는다. 깨끗한 별도 checkout에서 실행해야 하며 내부 acceptance가 `scripts/check.py --require-git`를 포함한다. 원격 계약 검사와 원격 RESULT 재열람은 통합 담당의 별도 봉인/검사 영수증으로 확인한다. 공통 검사는 `artifacts/` 등의 별도 실행 로그를 만들 수 있으므로 이 문서 수정 작업의 읽기 전용 검산과도 구별한다.

## 7. 역사판 소프트웨어 실행: 아직 미실행인 확인 계획

자연 6건의 역사판 실행을 이 연구에서 독립 재현했다고 보고하지 않는다. 기준 판독에는 소스/규격 해석, 현재 회수한 TIFF byte 검사, 원저자 보고가 구분돼 있다. 설치된 ImageMagick 7.1.1-43의 보조 합성 반례는 7.1.1-3/-4/-6의 자연 사례 실행이 아니다. 아래 명령은 gold에 저장된 **미실행 명령**을 재현 가능한 작업 형태로 적은 것이다. 해당 바이너리·delegate·입력의 판과 SHA를 먼저 확보한 뒤 별도 실행 기록을 남겨야 한다.

### 아직 필요한 최소 입력

| 사건 | 최소 추가 입력·기록 | 성공으로 잘못 세면 안 되는 것 |
| --- | --- | --- |
| P1 | Pandoc 2.19.2, 원 conditional Lua filter와 filter 순서, native Div 보존/출력 HTML grouping 중 요구 범위 | 제목 계층을 바꾼 반대 입력의 성공, native AST를 바꾼 후보의 실행 전 기대 |
| P2 | 원 사용 판, 실제 전체 YAML/key 집합, unique/duplicate key·quoting·multiline 정책. 연구 고정판 3.8.3의 실행 가능한 바이너리 | 작은 구성 입력의 exit 0만으로 전체 약어 동등성·주석 보존을 확정 |
| P3 | **실제 원 Quarto/Pandoc 명령과 옵션, Quarto/Pandoc 판, PDF engine 및 판, template·include/filter·resource 경로, TeX 배포판과 longtable 등 package 판**, 원 입력·그림 및 로그 | 임의 현재 pdflatex 실행을 원 pipeline으로 간주, figure가 같은 페이지에 남은 대조를 next-page float 보존 성공으로 간주 |
| I1 | 7.1.1-3 및 libtiff/delegate/quantum/OS, 원입력 SHA, 당시 viewer/app 판 | RGB 값 동일성만으로 모든 profile/뷰어 외관까지 보장 |
| I2 | 같은 SHA의 demo.tif, 7.1.0-28와 7.1.1-4의 바이너리·delegate/quantum/OS, 요청한 plane의 mask 의도 | 흰 PNG를 원 extra plane이 흰색이었다는 증거로 간주, 모든 TIFF에 meta→alpha를 적용 |
| I3 | **원 JP2 또는 동일성이 입증된 배포본과 SHA-256, ihdr/colr/ICC/cmap/cdef·codestream dump, 정확한 2021 tile의 band 정의, 7.1.1-6의 linked OpenJPEG 판, 모든 component의 독립 기준 decode** | 4 components에서 RGBA를 추론, 제품군 RGBI 설명을 exact 파일 검증으로 대체, 원파일 404를 소프트웨어 불가능으로 바꿈 |

P3 원 Markdown/후속 TeX와 그림은 저장돼 있지만 원 실행환경이 부족하다. I3는 원첨부 HTTP/HTTPS와 배포 디렉터리 회수 실패가 기록돼 있으며 archive 복원으로 JP2가 새로 생기지 않는다.

### Pandoc P1/P2 미실행 명령

입력 설명·해시는 [unexecuted-checks.json](gold-work/pandoc/unexecuted-checks.json), 판정 기준은 [unexecuted-checks.md](gold-work/pandoc/unexecuted-checks.md)에 있다. 출력이 원 입력 폴더를 오염시키지 않도록 새 폴더에서 실행한다. 다음 변수에는 **이미 확보하고 판을 확인할 바이너리의 실제 절대경로**를 설정한다.

```sh
mkdir "$AF116_REPLAY/pandoc-runtime"
cp "$AF116_OWN/gold-work/pandoc/reproduction-inputs/"* "$AF116_REPLAY/pandoc-runtime/"
cd "$AF116_REPLAY/pandoc-runtime"
: "${AF116_PANDOC2192:?Pandoc 2.19.2 바이너리 절대경로가 필요합니다}"
"$AF116_PANDOC2192" --version
"$AF116_PANDOC2192" P1-original.md --self-contained --toc --output=P1-original.html
"$AF116_PANDOC2192" P1-hierarchy-counter.md --self-contained --toc --output=P1-hierarchy-counter.html
"$AF116_PANDOC2192" P1-raw-wrapper-candidate.md --self-contained --toc --output=P1-raw-wrapper-candidate.html
: "${AF116_PANDOC383:?Pandoc 3.8.3 바이너리 절대경로가 필요합니다}"
"$AF116_PANDOC383" --version
"$AF116_PANDOC383" --from=markdown+smart --to=native --abbreviations=P2-bare-keys.txt P2-example.md
"$AF116_PANDOC383" --from=markdown+smart --to=native --abbreviations=P2-space-enriched.yaml P2-example.md
"$AF116_PANDOC383" --from=markdown+smart --to=native --abbreviations=P2-tab-enriched.txt P2-example.md
"$AF116_PANDOC383" --from=markdown-smart --to=native --abbreviations=P2-bare-keys.txt P2-example.md
```

P1은 TOC 항목, 본문 제목 계층, 하나의 emitted group, nesting/ID/속성 및 실제 filter 조건을 각각 확인한다. P2는 native 출력의 token과 `Space`/NBSP, 입력 파일 before/after hash를 비교한다. 구성 입력과 실제 원 파일을 구별한다.

### P3: 원 engine·template이 확인된 뒤의 미실행 명령

위 `pandoc-runtime` 폴더에서 다음 명령을 쓸 수 있다. 첫 둘은 후속 TeX에 `\listfiles`만 덧붙인 **component 재현**이며 원 Markdown→PDF pipeline 전체를 대신하지 않는다.

```sh
: "${AF116_TEX_ENGINE:?확인된 원 LaTeX engine 바이너리 절대경로가 필요합니다}"
"$AF116_TEX_ENGINE" --version
"$AF116_TEX_ENGINE" -interaction=nonstopmode -halt-on-error -recorder P3-followup-with-listfiles.tex
"$AF116_TEX_ENGINE" -interaction=nonstopmode -halt-on-error -recorder P3-followup-with-listfiles.tex
: "${AF116_PANDOC21403:?Pandoc 2.14.0.3 바이너리 절대경로가 필요합니다}"
"$AF116_PANDOC21403" --version
"$AF116_PANDOC21403" --from=markdown --to=latex --standalone P3-original-layoutissue.md --output=P3-pandoc-diagnostic.tex
"$AF116_TEX_ENGINE" -interaction=nonstopmode -halt-on-error P3-upstream-158.tex
```

순수 Pandoc 진단이 Quarto의 `format` YAML을 재현한다고 주장하지 않는다. 원 명령을 확보하면 동일 환경에서 원 입력, 앞 문단 제거, 표 제거, 표를 다른 figure로 교체한 네 경우를 비교한다. 실제 다음 페이지 figure 위치, 표 유지, 각 페이지 body text area와 최하단 text/table 좌표, engine/package 판, log 경고를 기록하고 longtable 폭이 안정될 때까지 필요한 pass를 수행한다. 독립 upstream 입력의 `[htbp]` 대조에서는 `h` 배치가 실제 float 자체를 피했는지도 확인한다.

### ImageMagick I1/I2 미실행 명령

gold의 exact 명령과 전제는 [gold-work/imagemagick/gold.json](gold-work/imagemagick/gold.json)의 `correct_answer.commands_unexecuted`에 있다. I1 명령은 원문 끝의 typographic quote를 ASCII 단일 따옴표로 정상화한 의도상 명령이다.

```sh
mkdir "$AF116_REPLAY/imagemagick-runtime"
cp "$AF116_OWN/gold-work/imagemagick/attachments/lena.png" "$AF116_REPLAY/imagemagick-runtime/"
cp "$AF116_OWN/gold-work/imagemagick/attachments/mandril3.jpg" "$AF116_REPLAY/imagemagick-runtime/"
cp "$AF116_OWN/gold-work/imagemagick/attachments/extracted/demo.tif" "$AF116_REPLAY/imagemagick-runtime/"
cd "$AF116_REPLAY/imagemagick-runtime"
: "${AF116_IM7113:?ImageMagick 7.1.1-3 magick 절대경로가 필요합니다}"
"$AF116_IM7113" -version
"$AF116_IM7113" lena.png \( mandril3.jpg -colorspace gray \) -channel-fx '| gray=>meta' meta.tif
"$AF116_IM7113" identify -verbose meta.tif
: "${AF116_IM7114:?ImageMagick 7.1.1-4 magick 절대경로가 필요합니다}"
"$AF116_IM7114" -version
"$AF116_IM7114" identify -verbose demo.tif
"$AF116_IM7114" demo.tif -channel-fx 'meta' extract.png
```

I2의 다른 조건부 경로는 다음과 같다. 동일 `extract.png`를 덮어쓰지 않도록 별도 새 출력 디렉터리에서 같은 `demo.tif`를 읽고 실행한다.

```sh
mkdir "$AF116_REPLAY/imagemagick-mask-runtime"
cp "$AF116_OWN/gold-work/imagemagick/attachments/extracted/demo.tif" "$AF116_REPLAY/imagemagick-mask-runtime/"
cd "$AF116_REPLAY/imagemagick-mask-runtime"
"$AF116_IM7114" demo.tif -channel-fx 'meta=>alpha' -alpha extract extract.png
```

두 번째 경로는 unspecified extra plane이 사용자가 의도한 opacity mask라는 전제에서만 해석한다. I1은 raw TIFF 태그, RGB 전샘플, 추가 plane 값, profile/색 해석과 viewer 표시를 따로 확인한다. I2는 raw fourth plane과 추출 PNG의 8-bit 값·크기·방향을 비교하고 원저자가 말한 이전 판과 동일 조건으로 대조한다. `identify` 출력이나 성공 종료 코드만으로 그 비교를 대신하지 않는다.

### I3: 원 JP2 회복 후의 미실행 명령

원 JP2를 회복해 동일성을 입증한 새 작업 폴더에서 gold의 다음 명령을 실행한다. 파일명만 같은 새 tile은 원 입력으로 인정하지 않는다.

```sh
: "${AF116_IM7116:?ImageMagick 7.1.1-6 magick 절대경로가 필요합니다}"
"$AF116_IM7116" -version
"$AF116_IM7116" identify -verbose dop10rgbi_32_280_5652_1_nw_2021.jp2
exiftool -G1 -a -s dop10rgbi_32_280_5652_1_nw_2021.jp2
opj_dump -i dop10rgbi_32_280_5652_1_nw_2021.jp2
```

ExifTool/OpenJPEG 도구 판도 실행 기록에 남긴다. `identify`는 ImageMagick의 해석 결과이며 원 band 의미의 독립 증거가 아니다. ExifTool이 cdef/cmap을 생략하면 원시 JP2 box dump가 추가로 필요하다. `opj_dump`의 component 수·정밀도·geometry만으로 near-IR/opacity 의미를 확정하지 않는다. 모든 component의 독립 decode와 exact tile의 band 정의가 있어야 실제 값·뜻의 보존과 색 손실 여부를 판단할 수 있다.
