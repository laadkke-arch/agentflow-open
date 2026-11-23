# AF-RES-052 실행·검사와 미실행 재개의 입력

## 실제 수행 범위

최초 시작 명령은 아래와 같으며 실행 결과·종료 코드는 `evidence/start-receipt.json`에 있다. 같은 활성 세션의 manifest를 덮어쓰기 위해 다시 실행하는 명령은 아니다.

```bash
python -B -m workbench.session start af-res-052 --allow docs/workstreams/research/AF-RES-052/ --output docs/workstreams/research/AF-RES-052/manifest.json --dependency work/research-af-res-033=03ff2eb1264b85016266de1f36ddebe45f5fface --dependency work/research-af-res-048=132e0108e652bdd2413edb71dfd6531507ea63e8 --fetch
```

이 작업에서 수행한 것은 공개 원문 직접 열람, 고정 목록/키/대표 계산, 실제로 얻은 도착 창에서의 경로 재구성, 코드·시험 정의의 D2 판독이다. 공급자 패키지 설치·시험 실행(D3), 실제 사용자 UI 시행, 녹음 재생, 폰트 바이너리 검사 결과는 없다. 이 파일의 후속 명령은 실행 결과와 구별한다.

## 제출 원장의 재구성과 검사

저장소 루트에서 다음 명령은 owned_path의 공개 메타데이터/원장만 읽고 같은 경로의 통합 파일을 만든다. 원문 전문 캐시는 필요하지 않다. `prepare_inputs.py`는 사전 입력 정규화, 두 assemble 스크립트는 관측 통합, `make_report.py`는 결과 작성이다. **최종 출판검증 후 make_report.py를 다시 실행하면 AC15가 결과 동결 전의 pending 상태로 돌아가므로, 최종 검증 영수증을 보존한 상태에서 연구 초안을 재생할 때만 사용한다.**

```bash
python -B docs/workstreams/research/AF-RES-052/prepare_inputs.py
python -B docs/workstreams/research/AF-RES-052/assemble_sources.py
python -B docs/workstreams/research/AF-RES-052/assemble_results.py
python -B docs/workstreams/research/AF-RES-052/make_report.py
python -B docs/workstreams/research/AF-RES-052/verify_research.py
```

최종 제출물의 비변경 검사는 마지막 명령만 실행하면 된다. 로컬 검사의 실제 stdout/종료 코드는 `evidence/local-validation.json`에 있다. 이 검사는 구조·출처 연결·순서·null/0 보존에 관한 것으로, 역사판 또는 사람의 효용을 실행 검증하지 않는다.

결과가 커밋되고 원격 브랜치에서 확인된 다음 사용자 지정 검사를 실행한다.

```bash
python -B -m workbench.session check docs/workstreams/research/AF-RES-052/manifest.json --fetch
```

`evidence/final-verification.json`에는 이 명령의 실제 실행 SHA·시각·stdout·stderr·종료 코드와, 같은 고정 결과 SHA의 `RESULT.md`·`evidence/acceptance-evidence.json` 원격 재열람 및 blob 동일성 검사를 보존한다. 유효한 결과 SHA는 마지막 `HANDOFF.md`를 따른다. 원격 재열람은 본문을 읽는 GitHub 연결 도구로 수행하며 로컬 파일을 읽은 것을 원격 확인이라고 쓰지 않는다.

## 미실행 M-N1 현재 조합 — 정확 입력·명령 제공

[evidence/markdown/REPLAY_PLAN.md](evidence/markdown/REPLAY_PLAN.md)에 원941의 두 code 노드, exact value, lang/meta,4가지 옵션, 예상 C1/C2, package.json, 설치·실행 명령, lockfile/입력/출력 해시, 실패 로그 보존 절차를 적었다.

현재 조합의 계획 pin은 remark-stringify11.0.0, mdast-util-to-markdown2.0.0, unified11.0.0이다. 마지막 판은 manifest의 ^11.0.0 범위 안에서 정한 계획값으로 별도 registry 존재를 검증했다고 주장하지 않는다. npm 접근·설치·실제 의존 해석·실행은 미확인이다. 이 계획을 실행해도 원요청의 literal react-stringify10.0.2·unified10.1.1의 역사적 성공을 증명하지 않는다.

**역사 재개의 첫 행동:** [원941 CodeSandbox](https://codesandbox.io/s/beautiful-water-1j3fe?file=/src/App.js:0-1695)의 보존된 package.json/lockfile와 실제 파이프라인을 확보한다. 현재 REST 본문만 새로 받는 것은 생성판 복원이 아니다. 원955는 [별도 첨부](https://codesandbox.io/s/smoosh-grass-db4x2b)의 네 패키지 tuple과 raw HTML 출력이 입력이다. 자동으로 패키지명을 고치거나 현재판으로 대체하지 않는다.

## 정확 도착을 다시 확인해야 할 입력

| 실패/부분 ID | 원래 입력과 실제 관측 | 다음에 확보할 최소 자료 |
| --- | --- | --- |
| PY-A04 / PY-A17 | `https://pypi.org/project/bandersnatch`의 초기7.0.0 창은347단어; 같은 ref의 다음 부분은8.2.0 레이아웃 | 초기 응답의 나머지 동일 snapshot. 없으면 새 snapshot을 먼저 봉인한 별도 시행으로 A/B/C 모두 다시 계산. |
| PY-A07 / PY-FRAG-07 | `https://bandersnatch.readthedocs.io/en/latest/` 본문 두 번째 정보 링크-h; web link17 클릭 뒤 fragment 미노출 | 정확 href와 실제 option 절. 부모 문서 성공을 anchor 성공으로 바꾸지 않음. |
| PY-A10 / PY-F01 | `https://github.com/pypa/bandersnatch/tree/main/src/bandersnatch_docker_compose`에서 restricted URL | 같은 주소의 해당 관측판 HTML·정확 도착. 별도 pinned README는 이미 읽었지만 다른 획득임. |
| PY-INV-build / D-P1-R6 | `https://build.pypa.io/en/stable/objects.inv` HTTP403 | 출판된 inventory의 build:index URI 레코드와 checksum. `index.html`을 추정하지 않음. |

새 주소 응답을 보존할 후속 명령 예시는 아래와 같다. 입력 URL이 현재 달라졌다면 기존 시행을 덮어쓰지 않는다. 실행 폴더가 이미 있으면 새 이름을 사용한다.

```bash
mkdir -p docs/workstreams/research/AF-RES-052/evidence/python/cache/retry-arrivals
curl --fail --location --dump-header docs/workstreams/research/AF-RES-052/evidence/python/cache/retry-arrivals/pypi.headers 'https://pypi.org/project/bandersnatch' --output docs/workstreams/research/AF-RES-052/evidence/python/cache/retry-arrivals/pypi.html
curl --fail --location --dump-header docs/workstreams/research/AF-RES-052/evidence/python/cache/retry-arrivals/bandersnatch.headers 'https://bandersnatch.readthedocs.io/en/latest/' --output docs/workstreams/research/AF-RES-052/evidence/python/cache/retry-arrivals/bandersnatch.html
curl --fail --location 'https://build.pypa.io/en/stable/objects.inv' --output docs/workstreams/research/AF-RES-052/evidence/python/cache/retry-arrivals/build-objects.inv
```

위 명령은 이번 작업에서 실행한 것으로 기록하지 않는다. 실행자는 각 명령 직후 `$?`,UTC, 요청/최종URL·응답해시를 보존해야 한다. 새 초기 창이 정해지기 전에 도착 내용으로 키를 다시 만들지 않는다. HTML 전문은 Git에 재배포하지 않고 공개 주소·hash·절/행·자체 요약과 한계만 커밋한다.

## 다음 첫 행동의 우선순위

가장 먼저 해결해야 할 것은 도구 설치가 아니라 **사용자 목적과 기능 절의 연결**이다. 새 조사 차수에서 목록과 독립적인 적격 목적·두 필수조건·기능명사·매칭 규칙을 먼저 고정하고, 그 명사로 매치되는 발행자의 기능 절을 찾아 실제4–6위 후보와 C의 알려진5필드 충돌을 확인한다. 현재 파일의 빈 자리를 사후 교체하지 않는다.

그 다음 원판/정확 도착 복구와 필요하다면 위 D3 재현을 수행한다. 이 순서가 뒤집히면 실행 성공을 보고 목적과 판정 조건을 새로 붙이는 조사로 바뀌므로 현재 결론의 결손을 해소하지 못한다.
