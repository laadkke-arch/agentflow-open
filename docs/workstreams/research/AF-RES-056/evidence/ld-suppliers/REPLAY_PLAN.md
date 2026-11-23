# 로컬 진단 실행 및 재개 기록

**실시 범위:** 연구자 작성 로컬 입력 2개의 PyLD frame 진단. 원 LD-3 credential의 remote context, 공급자 회귀시험, W3C suite 실행은 미실시다. 모두 순위 봉인 뒤의 예산 밖 조사다.

## 실제 실행 결과

고정 소스는 `digitalbazaar/pyld@3ac1987d9be3648c09b7c7e34865ce82d637e742`, package version은 3.3.0이었다. GitHub 직접 clone 및 해당 SHA checkout은 성공했다. 처음 시도한 git gateway URL은 HTTP400/exit128이었으며 [source-checkout.json](execution-attempts/source-checkout.json)에 두 경로를 구별했다.

기본 환경의 첫 실행은 cachetools 누락으로 import 단계에서 exit1이었고 행동 사례 0개를 실행했다. 이후 단 한 번의 `pip --target transient/deps`로 cachetools 8.0.2·frozendict 2.5.1을 작업 소유 경로에만 설치했다. 설치 명령·exit0·UTC·stdout/stderr는 `execution-attempts/pip-*`에 보존했다. pip 전체 보고의 설명 본문은 남기지 않고 실제 버전·archive URL·SHA256·환경을 [dependency-lock.json](execution-attempts/dependency-lock.json)에 보존했다. lxml 6.1.1은 기존 설치를 사용했으며 원 wheel hash는 확보하지 못했다.

01:55:00.791439~01:55:01.207950 UTC에 다음 frame 실행을 했다. checkout 상태는 clean이었고 runner에서 실제 module 경로·version·git SHA를 검사했다.

```bash
PYTHONPATH="$PWD/transient/deps:$PWD/transient/pyld/lib" python -B replay_plan.py
```

입력 [minimal-fixtures.json](minimal-fixtures.json)의 SHA256은 `9ffdece6a5a4481b7b2b32a427a5b301b1d0bf70d5d62c6ecf9f8071fe297a62`다. 외부 문서 요청을 거부하는 documentLoader를 주입했으며 실제 요청 목록은 비었다. `PLAN-LD-POS`는 C1/C2=true였다. `PLAN-LD-NEST`는 예상한 boolean 실패 대신 frame 확장 예외였으므로 **원 runner exit1**을 유지했다. [원 출력](execution-attempts/offline-frame.stdout.json), [명령·exit·시각](execution-attempts/offline-frame-attempt.json), stderr를 함께 보존했다. 기대값을 사후 수정하지 않았다.

동일 음성 입력에 대한 새 `DIAG-LD-NEST-CAUSE`는 다음 명령으로 expand 결과와 예외 cause를 수집했다.

```bash
PYTHONPATH="$PWD/transient/deps:$PWD/transient/pyld/lib" python -B trace_nest.py
```

[추가 출력](execution-attempts/nest-cause.stdout.json)은 a/b/c가 각각 한 노드의 값 배열로 합쳐졌고, frame은 `@requireAll`의 `colliding keywords`로 실패했음을 보여 준다. 새 진단 exit0은 오류 정보 수집 완료이며 최초 예측의 성공이 아니다. 원 LD-3 자체의 완결 판정은 계속 미확인이다.

## 같은 진단의 재현

위 두 명령은 이 파일의 폴더를 현재 디렉터리로 삼는다. 체크아웃·의존성 transient는 증거 기록 뒤 제거했으므로 아래 순서로 다시 준비해야 한다. 이는 재현용 명령이며 재설치를 추가로 실행한 기록은 아니다.

```bash
git clone --no-checkout https://github.com/digitalbazaar/pyld.git transient/pyld
git -C transient/pyld checkout --detach 3ac1987d9be3648c09b7c7e34865ce82d637e742
python -m pip install --only-binary=:all: --target transient/deps --require-hashes -r replay-requirements.txt
```

Python 3.12.14와 기존 lxml 6.1.1 환경을 맞춘 후 위 두 runner를 실행한다. `replay-requirements.txt`는 이번에 설치한 두 wheel만 고정한다. lxml 원 wheel hash는 없으므로 전 환경의 완전한 바이너리 재현이라고 주장하지 않는다. stdout/stderr·UTC·exit code를 새 파일에 보존한다.

## 미실시인 공식 시험과 원 요구

PyLD checkout의 API suite submodule이 `ffdb326121ea89b7b8280e76a5caea923834bcef`이고 시험 의존성도 준비되어 있을 때 아래 명령을 별도 실행할 수 있다. 이번에는 suite submodule을 초기화하지 않았고 두 명령도 실행하지 않았다.

```bash
PYTHONPATH="../deps:lib" python -m pytest tests/test_jsonld.py::TestExpand::test_scoped_context_on_nest_term_expands_nested_properties tests/test_jsonld.py::TestFrame::test_processing_id_in_inner_context
PYTHONPATH="../deps:lib" python -m pytest --tests=specifications/json-ld-api/tests/expand-manifest.jsonld --earl=af-res-056-api-earl.json
```

두 명령은 `transient/pyld/`를 현재 디렉터리로 삼는다. 두 번째는 expansion manifest 전체를 돌리므로 n006/n007/en01의 결과·skip·분모를 EARL과 출력에서 구분해야 한다. 원 credential의 C1/C2 동시 확인에는 원 remote context 판·당시 package/lock·전체 입력·옵션을 먼저 고정해야 한다. 로컬 양성을 원 질문의 실행으로 대체하지 않는다.
