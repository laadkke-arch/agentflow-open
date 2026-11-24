# 고정 표본 재실행

관측에 사용한 플랫폼은 Debian 13 amd64, Python 3.12.14, Go 1.23.12, Node 24.22.1, npm 11.9.0이다. 엔진의 원 소스 checkout과 실행에 사용한 모듈 정보, 종료코드 및 도구 출력은 [설치 원장](../receipts/setup/runtime.json)에 있다.

## 준비와 실행

아래는 저장소 루트에서 실행한다. Go, Node, npm과 Git, Python의 경로는 재현 환경에 맞게 지정한다. 이 관측에서 내려받은 [Go 배포판](https://go.dev/dl/go1.23.12.linux-amd64.tar.gz)의 SHA-256은 `d3847fef834e9db11bf64e3fb34db9c04db14e068eeb064f49af747010454f90`이다. 설치 단계는 원격 저장소와 Go/npm 패키지 저장소가 필요하다. 셀 실행은 고정 로컬 파일만 읽는다.

```sh
runner="$PWD/docs/workstreams/research/AF-RES-186/runner"
scratch="$(mktemp -d /tmp/af186-repro.XXXXXXXX)"

checkout_pin() {
  git init -q "$1" &&
  git -C "$1" remote add origin "$2" &&
  git -C "$1" fetch --depth=1 origin "$3" &&
  git -C "$1" checkout --detach FETCH_HEAD
}

checkout_pin "$scratch/suite" https://github.com/w3c/json-ld-api.git 8811ba2a3bcae883ac91efacffb70ef08d84e92f
checkout_pin "$scratch/gold" https://github.com/piprate/json-gold.git 0dbcf4d641a409700208f66945c0d2af7754fba9
checkout_pin "$scratch/js" https://github.com/digitalbazaar/jsonld.js.git 30f9067c40066519c917721b8ca4a374eabf15e7

go_exec=/path/to/go1.23.12/bin/go
node_exec=/path/to/node
npm_exec=/path/to/npm

python -B "$runner/prepare.py" \
  --suite "$scratch/suite" --gold "$scratch/gold" --js "$scratch/js" \
  --go "$go_exec" --node "$node_exec" --npm "$npm_exec" \
  --scratch "$scratch/build" --logs "$scratch/setup"
python -B "$runner/controls.py"
python -B "$runner/run.py" --runtime "$scratch/setup/runtime.json" --out "$scratch/observed"
python -B "$runner/verify.py" "$scratch/observed" --suite "$scratch/suite"
```

준비 명령은 suite와 두 엔진을 각각 점검한다. 한 엔진이 실패하면 준비 명령의 종료코드는 1이고 `runtime.json`에는 그 이유가 남는다. 나머지 엔진의 실행과 결측 영수증을 수집하려면 `run.py`를 실행한다. 런타임·로더·프로세스·출력 프로토콜 결측에는 해당 분류와 원로그를 붙인다. 규격 불합격을 관측해도 전체 실행에 필요한 로그가 확보되면 `run.py`와 `verify.py`는 0을 반환한다.

- Gold는 고정 checkout에서 `-mod=readonly`, `-trimpath`, CGO 비활성으로 어댑터를 빌드한다. Go가 확인한 실제 링크 모듈과 실행 바이너리 지문을 설치 원장에 남긴다.
- JS 원 checkout에는 upstream 잠금 파일이 없다. 원본의 `dependencies`만 [런타임 manifest](js-deps/package.json)에 옮겼고 npm의 [해결 잠금](js-deps/package-lock.json)을 `npm ci --ignore-scripts --omit=dev`로 적용한다. 측정 시 checkout의 `lib/index.js`가 실제 진입점이다. 새 npm 해석과 2020 환경은 별개다.
- 요청은 고정한 원 document IRI와 Base를 쓰고 mode는 `json-ld-1.1`이다. 로더는 해당 셀의 입력 IRI 한 개만 처리하며, `compact` 문맥은 로컬 JSON으로 읽어 인수로 전달한다. 읽은 IRI·상대 파일·바이트 지문을 영수증에 남긴다.
- `ordered`는 표본 manifest의 상태대로 생략한다. 두 핀에는 사용자 제어 `ordered`가 없고 각 구현은 핵심 경로에서 객체 키를 정렬한다. 공통 채점은 일반 배열을 비순서, `@list`의 요소를 순서 비교하며 양성 compaction에는 기대/실제 문서를 같은 base에서 다시 expand한다. 보조 재확장은 기본 40셀과 구별한다.
- 어댑터가 엔진 오류를 기록하고 정상적으로 영수증을 반환하면 프로세스 종료코드는 0이다. 기대 오류가 난 시험은 `error_code`까지 검사한다. 엔진 오류와 프로세스 실패를 각각 원 stdout·stderr에서 확인할 수 있다.

보관된 셀 하나의 명령, stdin 및 환경은 해당 `receipt.json`을 기준으로 한다. 같은 scratch 및 설치 경로를 유지한 경우 예시는 다음과 같다.

```sh
/tmp/af186-runtime/build/json-gold-driver < "$runner/../receipts/gold-T04-r1/request.json"
```

보관본의 양쪽 반복과 원 자료를 다시 검산하려면 `python -B "$runner/verify.py" "$runner/.." --suite "$scratch/suite"`를 사용한다. 실행 PID·시간·nonce는 새 실행마다 새로 생성된다.
