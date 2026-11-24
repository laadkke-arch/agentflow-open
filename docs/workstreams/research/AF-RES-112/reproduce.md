# AF-RES-112 재현·검산과 최소 재개

검사 대상 결과 SHA는 마지막 `HANDOFF.md`와 후속 `evidence/final-verification.json`의 `result_commit`을 사용한다. 결과를 포함한 커밋과 그 뒤에 붙인 검사 영수증/HANDOFF 커밋은 다르다. 아래 상대 경로는 저장소 루트 기준이며 사용자 PC 설치를 전제로 하지 않는다. 고정 원장은 재계산할 수 있으나 새 모델 판독은 과거 문맥의 동일 실행 재현이 아니다.

## 1. 고정 결과판의 공통 검사

새로운 깨끗한 checkout에서 지정 SHA를 확인한다. 기존 미저장 작업을 덮어쓰지 않는다. `RESULT_SHA`는 설명용 자리표시자가 아니라 HANDOFF에서 복사한 실제40자리 값으로 설정해야 한다.

```sh
git fetch origin refs/heads/work/research-af-res-112:refs/remotes/origin/work/research-af-res-112
git rev-parse HEAD
python -B -m workbench.session check docs/workstreams/research/AF-RES-112/manifest.json --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

`cloud_check.py`는 doctor, `scripts/check.py --require-git`, reference-audit discovery, original-smoke, session check-all을 실행한다. 마지막 자동 발견은 `docs/tasks` 대상이므로 이 작업의 owned_path manifest를 반드시 별도로 명시 검사한다. 실제 발견 개수는 출력과 `.workbench/cloud-check.json.session_validation`을 읽어 기록한다. 환경 라벨 `codex-cloud`는 호출자가 준 문자열이며 계정 연결 또는 제품/브라우저 통합 증명이 아니다. `.workbench`의 원 receipt와 stdout/stderr는 작업 경로 아래 evidence에 복사한 뒤 커밋한다.

현재 작업에서는 임시 검증 checkout을 owned_path의 무시된 `cache/verify`에 만들어 같은 결과 SHA를 검사한다. 검사기가 쓰는 임시 산출물은 그 checkout 안에 남으며 본 저장소의 중앙 파일을 수정하지 않는다. 검사 뒤 새 문서만 추가했다면 그 문서가 앞선 검사에 포함됐다고 하지 않는다.

## 2. 원장과 필수 표 재계산

네 명령은 라이브 웹 접근이나 새 모델 호출 없이 저장된 자료에서 재계산한다. Python 표준 라이브러리만 필요하다.

```sh
python -B docs/workstreams/research/AF-RES-112/compile_observations.py --check
python -B docs/workstreams/research/AF-RES-112/compile_control.py --check
python -B docs/workstreams/research/AF-RES-112/build_results.py --check
python -B docs/workstreams/research/AF-RES-112/check_study.py
python -B docs/workstreams/research/AF-RES-112/redact_transport_metadata.py --check
node docs/workstreams/research/AF-RES-112/check_reader_runtime.mjs
```

`compile_observations.py`는 `packets.jsonl`의12자리를 순서대로 훑어 각 수신 이벤트의 노출/단계 판단/최종 하나를 대사한다. 36자리 중18 observed·18 not_recruited·0 early_stop인지,1500자/회·4500자 총합, UTF-8 바이트, 판단 후 다음 이동 순서를 확인한다. `compile_control.py`는 C의 예정2자리·최대6단계를 별도 계산하며 주 분모를 바꾸지 않는다. 두 파생 궤적은 실제 choice 이벤트의 선택·이유·시각을 같은 단계 노출에 결합한다. G1 connector의 표시 원문주소와 관측된 HTTP 최종 주소의 차이도 한정한다. 원 봉인 이벤트와 파생 원장의 관계는 `evidence/ledger-derivation.json`을 확인한다.

`build_results.py`는 원장과 독립 평가를 결합해 `pairs.csv`, `metrics.json`, `RESULT.md`를 만든다. 표1은 패킷/gold/사후 설명 메모, 표2는 실제 단계 판단의 counterexample와 노출 좌표, 표3은 사건별 충분한 근거 성공을 사용한다. `analysis.md`는 출처가 붙은 해석 본문이고 `result-notes.json`은 사후 설명 메모다. 의미 판단은 `adjudication/assessments.json`과 `control-assessment.json`의 독립 평가 입력이며, 라벨 문자열 일치만으로 자동 정답을 만들지 않는다. 출력 업데이트가 필요하면 위 세 생성기에 `--check`를 빼고 실행한 뒤 diff를 검토한다.

`check_study.py`는 생성물의 바이트 일치, source97행/고유73/필수21, 원 원장 해시, 근거 참조 행·문자 범위, 문맥/입력/도구 해시, 원18개 노출 불변, 필수 표 순서와 마지막3행을 확인한다. 의미적 진실·역사판 정답·완전한 OS 가림을 증명하는 검사는 아니다. `redact_transport_metadata.py --check`는 만료된 공개 ZIP 리다이렉트의 서명 쿼리가 현재 JSON 산출물에 남지 않았는지 확인한다. 원래 메타데이터 정리 영수증을 덮어쓰지 않는다.

Node의 도구 검사는 합성2세션에서 개봉 제한·Unicode/UTF-8 비용·선행 판단·보이지 않은 링크 거절·기억한 링크 선택·단일 최종답을 검사한다. 합성2를 실제 수신7에 더하지 않는다. 원래 live 수신 runtime과 archive transport의 해시는 `evidence/reader-contexts.json`에 있다.

## 3. 출처 수와 사건 수를 재현하는 방법

`sources.jsonl`은 `audit-sources/sources.normalized.jsonl`의 정확한 복사본이다. 각 정규화 행의 `provenance.original_row`와 네 입력 원장을 비교할 수 있다. 접두사 GREC/LREC/GOLD/SUPP가 원장 출처를 구별한다. 원 작성자의 요청과 첨부 코드 예제를 각각 저작으로 세더라도 같은 사건 관계를 지우지 않는다. 같은 매뉴얼의 절·판·번역과 같은 예제 포트는 새 독립 저작으로 세지 않는다.

필수 배당은 bucket별 `min(확보, 목표)`의 합3+8+6+4=21이다. 총계73 또는 필수층 가능36을24완료로 바꾸지 않는다. 고유1차73+성공중복11+제외재게시1+접근실패12=97이다. 새 출처를 발견하면 사후 보조층으로 추가하고 기존 모집 순번과 처음 결과를 바꾸지 않는다.

기준 시각 일부는 정확한 최초 열람 시각이 아니다. gold24행의 `accessed_at_utc=null`, `reported_session_label`, `gold-work/clarifications.md`를 함께 읽는다. 원 요청 편집 이력도 생성 당시 스냅샷으로 복구하지 못했다. `evidence/root-rereads.jsonl`의 root 재열람과 출처 감사의 재열람은 새 저작 수에0을 더한다.

## 4. 현재 Godot 실행의 재생

기존 영수증은 Godot `4.7.2.stable.official.ed1daf0bf`, 제공 Linux에서 실행됐다. 원 G2는 stdout8·assertion 실패·OS exit0였다. 성공 여부를 exit0 하나로 해석하지 않는다. 원 G3 Godot3 프로젝트는 실행되지 않았고 작성자의 후속 Godot4 포트만 실행했다.

```sh
python -B docs/workstreams/research/AF-RES-112/gold-work/fetch_examples.py
godot --version
python -B docs/workstreams/research/AF-RES-112/gold-work/run_original_current_engine.py
python -B docs/workstreams/research/AF-RES-112/gold-work/run_gold_checks.py
```

다운로더는 고정된 원 ZIP3개만 열며 각 SHA256이 원 영수증과 다르면 중단한다. 텍스트 프로젝트 파일만 추출하고 원 편집기/셰이더 캐시는 실행하지 않는다. 따라서 원 전체 ZIP의 캐시를 그대로 실행한 시험이 아니다. 기존 `run-current-engine.json`, `run-controlled-current-engine.json`은 덮어쓰지 않고 새 기록은 무시된 `gold-work/examples/`에 생긴다. 새 판/새 환경의 결과는 새 관측이며 이전 영수증과 비교해 커밋한다. 원 소스와 구성 변형은 [REPRODUCE-GOLD.md](gold-work/REPRODUCE-GOLD.md)에 설명했다.

## 5. 미실시 역사판 검사 — 필요한 입력과 첫 행동

정확한 Godot3.4.2, 4.0-dev.20220118, 4.0alpha1 실행파일과 해당 빌드의 commit/해시를 확보하지 못했다. 새 바이너리를 설치하거나 유료 자원을 사용하지 않았다. 다음 작업자는 이미 허용된 환경의 정확한 바이너리를 먼저 식별하고 `--version`/`--help`를 기록해야 한다. 이름이 비슷한 최신 버전으로 대신하지 않는다.

입력은 G1 고정 repo `1a5942e87c2510e6f9fb281ba27f6a257258eb35`, G2 원 ZIP SHA256 `e016439485363faaff80376880e71c92b35d7bd390c7da0d5462ca9372f7f9ea`, G3 원 Godot3 ZIP `7dfda91dcf0440abcc8769d86b884f69e86e681c935d0d2b1d899d8574da5734`이다. 위 다운로더는 G2/G3 원 입력을 해시 확인해 제공한다. G1은 고정 원 repo의 Scene.gd/Path2D.gd/Path2D.tscn/LocalPath2D.tscn/project.godot를 읽고 별도 복사본에서 **생성 호출만** load/preload로 바꾼 두 변형을 준비한다. flag·프레임 처리·잔존 참조·점 추가 전후 위치를 고정하는 자동 UI driver는 아직 없다.

예를 들어 실제 존재하는 정확한3.4.2 바이너리를 입력으로 지정한 뒤 다음 명령을 실행한다. `GODOT_342`의 예시 경로는 아직 충족되지 않은 입력이다.

```sh
GODOT_342=/absolute/path/to/exact-godot-3.4.2
"$GODOT_342" --version
"$GODOT_342" --help
timeout --signal=TERM 10s "$GODOT_342" --no-window --path docs/workstreams/research/AF-RES-112/gold-work/examples/G3/test res://main.tscn
```

timeout124는 계속 실행 중이어서 중단한 것이며 통과가 아니다. G3의 원 출력은 변경 후 g2가 반복돼 g3를 충분히 관측하지 못하므로 출력 보완본은 별도 변형으로 해시를 남긴다. G2에서는 같은 타입/배열/값과 원1 두 번 참조를 유지하면서 UID/path/instance_id/value를 항목마다 관측한다. 구체적인 역사판별 다음 명령과 아직 없는 driver/판별 입력은 [HISTORICAL-NEXT.md](gold-work/HISTORICAL-NEXT.md)에 정리한다. 역사값 분모0을 해소하기 전 정확도는 null이다.

## 6. LilyPond 모집 재개와 미실시 조판

가장 먼저 열 자료는 `https://lists.gnu.org/archive/html/lilypond-user/2022-01/date.html`과 같은 월 thread index/원 mbox이다. `recruitment/lilypond/access-receipts.json`에 실패한 경로가 있다. 고정한 제목 정규식의 정정은 `protocol-amendment.json`을 적용하되2022-01부터 시간순 첫40고유 원질의를 다시 구성한다. 전체 index를 확보하기 전에 검색 순위의 유리한 문의를 L1–L3로 채우지 않는다. 새 사건이 확인되면 목적·정상/경계 입력을 원격 봉인한 뒤 새 gold와 새 수신 문맥을 만든다. 기존 r01–r14 이벤트를 덮어쓰지 않는다.

이 환경에서 `lilypond` 실행파일은 발견되지 않았다. 원 회귀 입력4개와 기대 설명은 직접 읽었지만 조판은 미실시다. 정확한 LilyPond2.24.4 실행파일이 제공되면 아래와 같이 **고정 URL·해시 입력만** 다시 받아 조판한다. 원문 내 `version`은 입력 언어 선언이며 실행 엔진판과 다를 수 있다.

```sh
python -B - <<'PY'
from pathlib import Path
import hashlib, json, urllib.request
p = Path('docs/workstreams/research/AF-RES-112')
target = p / 'cache/lilypond-replay'
target.mkdir(parents=True, exist_ok=True)
for row in json.loads((p/'recruitment/lilypond/regression-receipts.json').read_text()):
    with urllib.request.urlopen(row['original_url'], timeout=30) as response:
        data = response.read()
    assert hashlib.sha256(data).hexdigest() == row['sha256'], row['source_filename']
    (target/row['source_filename']).write_bytes(data)
PY
LILYPOND_2244=/absolute/path/to/exact-lilypond-2.24.4
"$LILYPOND_2244" --version
"$LILYPOND_2244" --output=docs/workstreams/research/AF-RES-112/cache/lilypond-replay/tag-filter docs/workstreams/research/AF-RES-112/cache/lilypond-replay/tag-filter.ly
"$LILYPOND_2244" --output=docs/workstreams/research/AF-RES-112/cache/lilypond-replay/tag-group docs/workstreams/research/AF-RES-112/cache/lilypond-replay/tag-group.ly
"$LILYPOND_2244" --output=docs/workstreams/research/AF-RES-112/cache/lilypond-replay/part-combine-relative docs/workstreams/research/AF-RES-112/cache/lilypond-replay/part-combine-relative.ly
"$LILYPOND_2244" --output=docs/workstreams/research/AF-RES-112/cache/lilypond-replay/part-combine-global docs/workstreams/research/AF-RES-112/cache/lilypond-replay/part-combine-global.ly
```

stdout/stderr/종료값뿐 아니라 생성 악보의 파트 선택·상대음·tie 조건을 원 입력의 기대 설명과 대조한다. 이것은 후속의 새 실행이며 현재 결과의 주 수신 성공에 더하지 않는다.

## 7. 단독 작업자의 재개

한 작업자도 봉인된 파일→원문→검산 순서로 이어갈 수 있다. 새 독립 문맥을 얻지 못하면 기존 좌표를 재생하거나 같은 사람이 다시 읽은 것으로 표시한다. 그때에는 독립 수신 성공률을 내지 않는다. 완결이 막히면 원격에 커밋한 결과·막힌 이유·다음 첫 행동을 HANDOFF로 남기고 끝낸다. 이 절차는 자동 크롤러·자율 검색기 구축이나 중앙 진행표 변경을 요구하지 않는다.
