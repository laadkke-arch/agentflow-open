# 재생과 검산

표시 규칙은 [SCOPE](SCOPE.md), 최초 봉인과 수정은 [노출 기록](evidence/replay-correction.md), 자료별 선택 텍스트는 [선정 원장](evidence/selection.json)에 있다. 재생에는 Python 3.12, Git, pinned raw GitHub을 읽는 네트워크가 필요하다. 이 실행 환경의 Python은 3.12.14였고 Markdown-It 3.0.0과 Docutils 0.21.2로 텍스트를 투영했다. GitHub UI에서 메뉴/픽셀/스크롤을 직접 계측한 결과는 미확인이다.

저장소 루트에서 고정 의존을 받는다. 대조하려는 연구 결과판의 detached checkout을 쓰면 현재 작업과 분리해 확인할 수 있다.

```sh
git fetch origin refs/heads/work/research-af-res-060:refs/remotes/origin/work/research-af-res-060
research="$PWD/docs/workstreams/research/AF-RES-064"
scratch=$(mktemp -d)
python -m venv "$scratch/render"
"$scratch/render/bin/pip" install markdown-it-py==3.0.0 mdurl==0.1.2 docutils==0.21.2
python -B "$research/freeze_inputs.py"
python -B "$research/replay.py" --boundary
"$scratch/render/bin/python" -B "$research/select_routes.py" --cache "$scratch/cache" --output "$scratch/selection"
cmp "$research/evidence/selection.json" "$scratch/selection/selection.json"
```

한 쌍의 표시만 별도 위치에 재생한다. 한 쌍은 A/B/P와 해당 첫 행동의 첫 적격 둘째 행동을 포함한다. 창 ID는 시작이 1이므로 전체 원장에서는 경로 ID, 뷰, 액션 번호, 해시로 대조한다.

```sh
"$scratch/render/bin/python" -B "$research/replay.py" \
  --cache "$scratch/cache" --pair JS-6/SC-005 --output "$scratch/one"
```

전체 재생과 경로·출처·표·실행 원장의 집계를 확인한다.

```sh
"$scratch/render/bin/python" -B "$research/replay.py" --cache "$scratch/cache" --output "$scratch/all"
python -B "$research/audit.py" --replayed "$scratch/all"
python -B -m workbench.session check "$research/manifest.json" --fetch
```

처음에는 빈 캐시로 12개 경로 본문을 HTTP에서 취득한다. 같은 고정 URL의 raw SHA-256 확인을 거친 캐시는 같은 raw를 재사용한다. 날짜가 달라질 수 있는 취득 영수증을 제외한 표시 텍스트·오프셋·해시·둘째 행동은 동일해야 한다. 조회와 표시를 분리한다. 499·500은 그대로, 501·611은 500으로 제한된다. 압축 JSON 801개 분절과 24,000 bytes의 한글 한 토큰, 혼합 제목·코드·수식 및 줄 매핑도 경계 로그에 있다. 이번 표에서 초과한 최종 창은 관측 0이고, W03/W04의 수정 전 독해는 실제 엄격 분모에서 빼는 별도 노출이다. [경계 로그](evidence/boundary-check.json) · [실제 노출](evidence/actual-exposure.json)

`anchor_check.py`의 조회는 브라우저 대신 내려받은 GitHub HTML의 ID 검사다. `--selection`에 별도 선택 파일을 줄 수 있다. GitHub가 렌더 레이아웃을 바꾸면 정적 ID 대조를 다시 확인하며, 해당판 raw 및 명시 함수/행의 검산과 구분한다. [DOM 증거](evidence/anchor-verification.json)

## 공급자 실행 재현

관측은 [고정 문서 판정](evidence/doc-seal.json) 이후의 실험이다. 테스트 환경을 새로 만들 때 [배포·소스 대조](evidence/runtime/package-identity.json)의 런타임 및 SHA를 확인한다. 앱 실행 로그는 [runs.jsonl](runs.jsonl)에서 입력군·arm에 연결된다. 원출력의 일시, 로컬 경로, 오류 스택은 실행마다 달라질 수 있다. 조건·출력·오류 종류의 대조는 원입력 정의와 명시 옵션으로 수행한다.

### JS-6

실행 시 Node v24.22.1, npm 11.9.0이었다. 최초 고정 SHA 소스의 `npm run build`는 re2 declarations의 `RegExpIndicesArray` 부재로 실패했다. 같은 gitHead의 8.17.1 배포판과 잠금파일을 쓰면 그 빌드 단계가 필요 없다. [빌드 실패](evidence/runtime/ajv-build.stdout) · [npm 잠금파일](evidence/runtime/ajv-lock.json)

```sh
mkdir -p "$scratch/ajv"
cp "$research/evidence/runtime/ajv-lock.json" "$scratch/ajv/package-lock.json"
printf '%s\n' '{"dependencies":{"ajv":"8.17.1"}}' > "$scratch/ajv/package.json"
npm --prefix "$scratch/ajv" ci --ignore-scripts --no-audit --no-fund --cache "$scratch/npm-cache"
node "$research/fixtures/js6-probe.cjs" "$scratch/ajv/node_modules/ajv/dist/ajv.js"
```

### JS-3

jschon wheel 0.11.1과 rfc3986 2.0.0을 받아 파일 SHA를 검산한다. 원 추출형, 원 선언 전체, 명시 2020-12 재구성은 서로 다른 arm이다. 네 입력군의 G1은 필수 이름을 하나씩 제거한 네 변형이다. 카탈로그 내부 등록으로 재현하며 원 Node/TypeScript/Ajv, 이메일 테스트와 분리된다.

```sh
python -B "$research/fixtures/fetch_runtime.py" "$scratch/releases"
python -m venv "$scratch/jschon"
"$scratch/jschon/bin/pip" install --no-index --find-links "$scratch/releases/wheels" jschon==0.11.1 rfc3986==2.0.0
"$scratch/jschon/bin/python" -B "$research/fixtures/js3_probe.py"
```

### LD-3

Docker 이미지 digest가 Ruby 3.3.14와 bigdecimal 3.1.5를 고정한다. 초기 컨테이너에서는 직접 RubyGems 다운로드가 403이었고, 호스트에서 Registry SHA를 대조한 뒤 네트워크 없이 설치했다. 세 context 파일의 내용은 [기록한 공개 소스](evidence/runtime/ld3-contexts.json)에서 받는다. 보관판은 별도 인자로 재현한다.

```sh
mkdir -p "$scratch/installed-gems"
ruby_image='ruby@sha256:9da1ed461864c9770e3deb4280c89cfaf9e998d0e92eae45ba6fcbad7afe66ea'
docker pull "$ruby_image"
docker run --rm --network=none \
  --mount "type=bind,source=$scratch/releases/gems,target=/downloads,readonly" \
  --mount "type=bind,source=$scratch/installed-gems,target=/gems" "$ruby_image" \
  sh -ec 'gem install --local --no-document --ignore-dependencies --install-dir /gems /downloads/*.gem'
docker run --rm --network=none \
  --mount "type=bind,source=$research/fixtures,target=/fixtures,readonly" \
  --mount "type=bind,source=$scratch/releases/contexts,target=/contexts,readonly" \
  --mount "type=bind,source=$scratch/installed-gems,target=/gems,readonly" \
  --env GEM_HOME=/gems "$ruby_image" ruby /fixtures/ld3_probe.rb /contexts
```

마지막 명령의 `/contexts` 뒤에 `archived_singular`를 추가하면 2020-12-06 경로 변경 전 파일을 별도 실행한다. 원형 loader의 exact URL 결손과 대체 판의 데이터 손실은 [공급자별 원출력](runs.jsonl)에 보존됐다. 원 환경을 재현하려면 원 사용자 jsonld.js 및 context URL의 당시 bytes가 더 필요하다.

## 검증 주체와 범위

GitHub의 시작 계약, 자체 검산 및 원격 파일 재열람은 이 Codex Cloud 작업자가 실행했다. 로컬 원장 검사는 해시·범위·분모·실행 키·링크 존재의 검증이다. 사람의 행동, 초기 환경에서의 원 사용자 성공 및 디지털 스캔 픽셀을 확인하려면 각각의 독립 입력이 필요하다. [자체 검토](SELF_CHECK.md) · [수용 원장](evidence/acceptance-evidence.json)
