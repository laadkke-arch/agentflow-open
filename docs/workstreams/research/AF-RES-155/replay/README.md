# AF-RES-155 재생

Linux x86_64, Node v24.22.1과 Python 3.12.14에서 실행했다. 아래 명령의 현재 위치는 작업 브랜치 checkout 최상단이다. 실행 파일과 원장은 소유 경로, 툴과 출력은 임시 경로에 둔다.

```sh
af155_base=docs/workstreams/research/AF-RES-155
af155_tools=$(mktemp -d /tmp/af155-toolchain.XXXXXX)
af155_out=$(mktemp /tmp/af155-replay.XXXXXX.jsonl)
bash "$af155_base/replay/bootstrap.sh" "$af155_tools"
python -m workbench.session check "$af155_base/session.json" --fetch
python "$af155_base/replay/run.py" --tools "$af155_tools" --repeat fresh --phase all > "$af155_out"
python "$af155_base/replay/check_evidence.py" --compare-replay "$af155_out"
```

Pandoc 3.1.11 배포 아카이브 SHA를 검사하고 lockfile대로 Prettier 3.1.1, Mustache.js 4.2.0, CommonMark.js 0.30.0을 설치한다. 기본 대조만 재생할 때는 `--phase main`, 보정 실험만 재생할 때는 `--phase escape-contrast`를 쓴다. 각 실험의 argv와 stdout/stderr는 runs.jsonl 또는 임시 파일에서 차이 비교가 가능하다. 조합 명령의 종료 0과 개별 변환 값은 각각 확인한다.

## 고정 외부 시험 재개

별도 임시 경로를 만들고 각 branch/tag에서 Git clone한다. driver가 commit SHA를 검사한다.

```sh
af155_upstream=$(mktemp -d /tmp/af155-upstream.XXXXXX)
git clone --depth=1 --branch 3.1.11 https://github.com/jgm/pandoc.git "$af155_upstream/pandoc"
git clone --depth=1 --branch 3.1.1 https://github.com/prettier/prettier.git "$af155_upstream/prettier"
git clone --depth=1 --branch v1.3.0 https://github.com/mustache/spec.git "$af155_upstream/mustache-spec"
git clone --depth=1 --branch 3.5.2 https://github.com/Python-Markdown/markdown.git "$af155_upstream/python-markdown"
af155_python_deps=$(mktemp -d /tmp/af155-python-deps.XXXXXX)
uv --cache-dir "$af155_tools/uv-cache" pip install --target "$af155_python_deps" 'Markdown==3.5.2'
PYTHONPATH="$af155_python_deps" python "$af155_base/replay/public_fixtures.py" \
  --upstream "$af155_upstream" --tools "$af155_tools"
```

초회 I/O 점검에서 Pandoc HTML fixture에 standalone 플래그가 없었고 Markdown 패키지 entry point가 없는 채 기본 이름으로 extension을 불러 실패했다. 위 고정 upstream driver와 패키지 설치판에서 다시 실행했다. 각 실패와 보정의 출처는 [공급자 시험 원장](../evidence/public-tests.jsonl)과 [자기점검](../SELF_CHECK.md)에 연결했다. 음악 파일의 발행자 SHA, 변환기와 보정된 한 줄, 시각 대조 위치는 [교차 분야 증거](../evidence/cross-domain.md)에 있다.
