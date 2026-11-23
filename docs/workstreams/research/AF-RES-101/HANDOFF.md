# AF-RES-101 HANDOFF

- **상태: DONE — 지정 공개 연구 범위 완료.** 원 사용자판·원 입력의 전체 효용과 신규 인지는 계속 미확인이다. 자료 미확인을 성공으로 바꾸지 않았다.
- **검사한 결과 SHA / result_commit:** `392ff3d651577ab6aacd65f4ed86884586b960d1`
- **브랜치:** `work/research-af-res-101`
- **owned_path:** `docs/workstreams/research/AF-RES-101/`
- **인계 작성 UTC:** `2026-11-23T22:38:47.019237+00:00`
- 사용자의 “결과와 HANDOFF.md를 지금 커밋” 지시로 추가 탐색을 중단하고 확보된 결과를 확정했다. 결과 묶음을 먼저 원격에 반영하고 정확한 결과 SHA의 검사·GitHub 재열람을 마친 뒤 이 HANDOFF만 마지막 단독 커밋한다. HANDOFF 자체를 앞 결과 SHA에서 검사했다고 주장하지 않는다.

## 결과와 후속 설계자가 사용할 판단

[RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/392ff3d651577ab6aacd65f4ed86884586b960d1/docs/workstreams/research/AF-RES-101/RESULT.md)는 요청8행, 후보24행, 작성자 후속/반환8행으로 시작한다. 모집은 ImageMagick60·Typst27, 선정8건, 후보24자리=실재18+빈6이다. A는9개 제외·7개 반환, B는0개 제외·14개 반환한다. 두 방식의 차이7개를 유효 대안7개로 읽으면 안 된다.

연구판에서 원 목적을 지지하며 기존 실제 시도와 다른 조작인 후보는 TY-A1-C2, TY-A2-C1/C2 세 개다. A의 다른 유효 조작 손실은3/3, B는0/3. 두 요청에 속한 세 후보이고, 원 예시의 위첨자− 생략을 엄격히 처리하면 분모2에서 A2/2·B0/2다. B만 반환한 나머지4개에는 wrapper/셸의 반대 근거가 있다. 따라서 B의 종합 우월성이나 질문자의 새로운 지식을 주장하지 않는다.

전체 후보 사전인지의 독립 분모는0이고18개 미확인이다. 재추천 제거율·이미 아는 후보 반환율은 산출 불가다. 명시 신규 인지 양성 관측0 역시 신규 여부18개 미확인이며0%라는 인지율이 아니다. 수정 IM-A1-C1의 실패 실행 보고1에피소드가 revision과댓글 두 기록에 남아 있다. 봉인 원문 그대로의 실행과 입력·판·출력 완전 연결 실행은 미확인이다.

같은 helper의 다른 binding, 같은 프로그램의 다른 대상/처리 단계, 다른 표기의 같은 호출, 이미 알려진 core를 감싼 새 helper를 분리했다. ImageMagick normalize의 동판 문서/구현 불일치, Typst literal pagebreak의 종료0/목적실패, CSS/셸/Ruby API의 반례도 남겼다. IM-U2 병합 민감도는 실재17·A6·B13, wrapper 경계 민감도는 A8·B14다.

## 근거와 재계산

고유1차자료 **35개**, 필수범주 **29개**로 하한24를 충족했다. 요청8 + ImageMagick 문서/구현5 + Typst 문서/구현7 + 상류시험/입출력5 + Git/FFmpeg4 + 보조6이다. sources.jsonl193행 중 같은 사건 후속·앵커·미러·live reference·배포본 동일파일·비선정 모집79건·재현방법2개는 추가 고유자료로 세지 않았다.

- 모집/최초 이력: [frame.csv](frame.csv), [initial.csv](initial.csv), [SCOPE.md](SCOPE.md), [manifest.json](manifest.json).
- 봉인 후보/후속: [candidates.csv](candidates.csv), [followup.csv](followup.csv), [24자리 동작판정](evidence/assessment.json).
- 분모·결측·민감도: [reconciliation.json](evidence/reconciliation.json), [recalculate.py](recalculate.py). 실제 재계산 exit0, 검증1,145개, validation_errors=[]; 반복 시각 외 결과 일치도 확인했다.
- 자료별 URL·판·지문·관측·한계: [sources.jsonl](sources.jsonl), [범주검산](evidence/source-counts.json).
- 동작 실행: [Typst17개](evidence/typst-official/run-receipt.json), [ImageMagick 원시험19/19 및 합성 대조](evidence/imagemagick/stage3/probes/results.json), [Ruby경계/CLI/셸 보충](evidence/root-supplement/probe-receipt.json), [Git/FFmpeg7대조](evidence/cross-domain/receipt.json).
- 자기점검과 별도 실제 검토: [SELF_CHECK](SELF_CHECK.md), [CSV 교차 검토](evidence/independent-review.md), [분모 비판 검토](evidence/denominator-review.md). 사람의 검토·전면 독립 맹검은 아니다.

## 중간 커밋과 원격 검증

| 묶음 | 원격 SHA | 봉인 UTC | 변경 파일 |
| --- | --- | --- | --- |
| 1 | `9d646592613ba2fd9c52bc9bbf3dbc28bac68693` | 2026-11-23T22:00:31.806896+00:00 | 31개; [원장](evidence/seals/commits.jsonl) |
| 2 | `4e7539906eb03abd46e6910643ed5317f97ddb45` | 2026-11-23T22:07:03.624061+00:00 | 21개; [원장](evidence/seals/commits.jsonl) |
| 3 | `c68b40e646dffcc41261ea21974c2bbfeab53348` | 2026-11-23T22:22:41.461916+00:00 | 140개; [원장](evidence/seals/commits.jsonl) |
| 4 결과 | `392ff3d651577ab6aacd65f4ed86884586b960d1` | 2026-11-23T22:35:13.657893+00:00 | 15개; [봉인](evidence/seals/results.json) |

각 묶음은 위 순서로 별도 커밋하고 GitHub ref를 읽어 원격 SHA를 확인했다. 직접 git push는 인증 입력 수단 부재로 실패했고 GitHub 연결을 통한 tree/commit/ref 갱신을 사용했다. GitHub 갱신은 예상 parent SHA를 지정했으며 중앙 진행표나 선행 작업은 수정하지 않았다. 네 묶음 모두 owned_path 안의 변경이다. 4묶음은 2026-11-23T22:35:37Z에 원격 ref를 확인했다.

시작 통합판 ac7abc85e12b3a5b5f87b694d00e9511332fe272와 계획판 ace1a06a13ea435f5cb6a3e340ad24f03f68ecae의 차이는 dot-control.json뿐이었다. 검사 시점 통합 끝 `e01dd119d08dcb6aa744ffbdf3c56c9640cd4efd`까지의 추가 차이도 dot-control.json뿐임을 실제 git diff로 확인했다. 계약의 실제 task/scope base는 ac7abc85…이며 검사에 통과했다. 의존 운영 pin a4b5471c08dc369367645a9e78249b44f8143f05와 연구 결과 pin f475e1a55c5be68cd6d9bcca1a7c7b4f9893e24c를 구분했다. [시작 blob 대조](evidence/start/contract-read.json)

## 정확한 결과 SHA의 필수 검사

두 명령 모두 `392ff3d651577ab6aacd65f4ed86884586b960d1`에서 실행했고 시작·끝의 작업트리는 깨끗했다.

| 명령 | UTC 시작 → 끝 | 종료값 | 범위와 실제 확인 |
| --- | --- | --- | --- |
| `python -B -m workbench.session check docs/workstreams/research/AF-RES-101/manifest.json --fetch` | 2026-11-23T22:36:33.879780+00:00 → 2026-11-23T22:36:44.554414+00:00 | 0 | AF-RES-101 manifest를 명시하여 개별 계약1개 검사; changed_paths200·outside0·errors0 |
| `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 2026-11-23T22:36:44.555072+00:00 → 2026-11-23T22:37:06.264725+00:00 | 0 | 공통 gate 통과. 자동 세션검사는 no_active_sessions로 실제0개·not-executed; 개별 검사를 대체하지 않음 |

공통 검사의 환경·acceptance·research-case·original-smoke 결과와 세션 미실시를 구별한다. 이 검사는 Git 계약/구조 검사이며 연구 주장·원 사용자 효용의 사실 인증이 아니다. 실제 stdout을 읽고 아래에 범위·UTC·종료값·내용 지문 및 핵심 JSON을 옮겼다. 전체 변경 파일은 각 봉인/커밋 원장에서 복원할 수 있다.

```json
{
  "checked_result_sha": "392ff3d651577ab6aacd65f4ed86884586b960d1",
  "clean_before_and_after": true,
  "checks": [
    {
      "command": [
        "python",
        "-B",
        "-m",
        "workbench.session",
        "check",
        "docs/workstreams/research/AF-RES-101/manifest.json",
        "--fetch"
      ],
      "target_sha": "392ff3d651577ab6aacd65f4ed86884586b960d1",
      "started_utc": "2026-11-23T22:36:33.879780+00:00",
      "ended_utc": "2026-11-23T22:36:44.554414+00:00",
      "exit_code": 0,
      "scope": "explicit AF-RES-101 manifest",
      "stdout_sha256": "5c2559b7c9bae1d12f7aab1d490e1aebeb77111147947d78ac092b47b9cf5318",
      "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "stderr": "",
      "result": {
        "status": "passed",
        "task_id": "af-res-101",
        "freshness": "remote_checked",
        "checked_at": "2026-11-23T22:36:44.541967+00:00",
        "checked_out_commit": "392ff3d651577ab6aacd65f4ed86884586b960d1",
        "task_base_commit": "ac7abc85e12b3a5b5f87b694d00e9511332fe272",
        "integration_commit": "e01dd119d08dcb6aa744ffbdf3c56c9640cd4efd",
        "scope_base_commit": "ac7abc85e12b3a5b5f87b694d00e9511332fe272",
        "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc",
        "outside_paths": [],
        "unmerged_paths": [],
        "errors": [],
        "boundary": "Git contract and ownership checks; not a new AI chat or product verification",
        "changed_paths_count": 200,
        "changed_paths_sha256": "7925121444ef3bdf975f97f2e24cccd8d45a02333b1d7c78dc7d62784fde63ba"
      }
    },
    {
      "command": [
        "python",
        "-B",
        "scripts/cloud_check.py",
        "--environment",
        "codex-cloud",
        "--fetch-contract",
        "--require-clean"
      ],
      "target_sha": "392ff3d651577ab6aacd65f4ed86884586b960d1",
      "started_utc": "2026-11-23T22:36:44.555072+00:00",
      "ended_utc": "2026-11-23T22:37:06.264725+00:00",
      "exit_code": 0,
      "scope": "codex-cloud common gate; actual discovered session count read from stdout",
      "stdout_sha256": "303305db5fa61db6a20ece57432dc3d4181d6bf8a32c09b95ed2e4e6c88c43fb",
      "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "stderr": "",
      "result": {
        "status": "passed",
        "exit_code": 0,
        "checked_out_sha": "392ff3d651577ab6aacd65f4ed86884586b960d1",
        "require_clean": true,
        "source_start": {
          "commit": "392ff3d651577ab6aacd65f4ed86884586b960d1",
          "dirty": false,
          "clean": true
        },
        "source_end": {
          "commit": "392ff3d651577ab6aacd65f4ed86884586b960d1",
          "dirty": false,
          "clean": true
        },
        "session_validation": {
          "status": "not-executed",
          "reason": "no_active_sessions",
          "count": 0,
          "freshness": "not_checked",
          "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc"
        }
      },
      "step_status_lines": [
        "[doctor] passed (exit 0)",
        "[acceptance] passed (exit 0)",
        "[research-case] passed (exit 0)",
        "[original-smoke] passed (exit 0)",
        "[sessions] passed (exit 0)"
      ],
      "unit_test_summary": [
        "Ran 55 tests in 6.272s",
        "Ran 7 tests in 0.001s",
        "Ran 9 tests in 0.001s"
      ]
    }
  ]
}
```

## 고정 GitHub 재열람

UTC 2026-11-23 22:36:02 UTC에 다음을 정확한 결과 SHA로 다시 열었다. 필수 표8/24/8과 마지막약점3행, 최초자료의 원문 위치·지문, 실제 합성 입력/출력 및 재현 절차를 확인했다. 대표 PNG를 직접 다시 봤고 아래7개 remote blob은 로컬 Git blob과 모두 일치한다.

| 다시 연 파일 | GitHub blob | 실제 관측 |
| --- | --- | --- |
| [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/392ff3d651577ab6aacd65f4ed86884586b960d1/docs/workstreams/research/AF-RES-101/RESULT.md) | `b4b49d63283bf20fb96bb474432870ad3642bc40` | 첫3표8/24/8·끝약점3행 확인 |
| [initial.csv](https://github.com/laadkke-arch/agentflow-open/blob/392ff3d651577ab6aacd65f4ed86884586b960d1/docs/workstreams/research/AF-RES-101/initial.csv) | `cdad17a74e9277093040f31bfba4b094362a6473` | 고정 결과 SHA에서 열고 로컬 Git blob 일치 확인 |
| [evidence/typst-official/inputs/a1-c2.typ](https://github.com/laadkke-arch/agentflow-open/blob/392ff3d651577ab6aacd65f4ed86884586b960d1/docs/workstreams/research/AF-RES-101/evidence/typst-official/inputs/a1-c2.typ) | `268d9474e04bc588fde30a0e542c072d0131bb63` | 고정 결과 SHA에서 열고 로컬 Git blob 일치 확인 |
| [evidence/typst-official/run-receipt.json](https://github.com/laadkke-arch/agentflow-open/blob/392ff3d651577ab6aacd65f4ed86884586b960d1/docs/workstreams/research/AF-RES-101/evidence/typst-official/run-receipt.json) | `31cfc923d662b060ca49036f740603a24d7e8f08` | 고정 결과 SHA에서 열고 로컬 Git blob 일치 확인 |
| [reproduce.md](https://github.com/laadkke-arch/agentflow-open/blob/392ff3d651577ab6aacd65f4ed86884586b960d1/docs/workstreams/research/AF-RES-101/reproduce.md) | `5ee51a295812006dc7ea25f62ef503f40a6b3fac` | 고정 결과 SHA에서 열고 로컬 Git blob 일치 확인 |
| [evidence/typst-official/outputs/visual-contact.png](https://github.com/laadkke-arch/agentflow-open/blob/392ff3d651577ab6aacd65f4ed86884586b960d1/docs/workstreams/research/AF-RES-101/evidence/typst-official/outputs/visual-contact.png) | `88db7a2f82357eb1d0cb2c1705f223332a9541dc` | 고정 결과 SHA에서 열고 로컬 Git blob 일치 확인; 이미지 직접 다시 봄 |
| [evidence/typst/initial-part.json](https://github.com/laadkke-arch/agentflow-open/blob/392ff3d651577ab6aacd65f4ed86884586b960d1/docs/workstreams/research/AF-RES-101/evidence/typst/initial-part.json) | `990aede2e6afe9e60d1539b23ad78c8dfb953c59` | 고정 결과 SHA에서 열고 로컬 Git blob 일치 확인 |

## 미실시·제한과 정확한 다음 명령

필수 최종 운영 검사는 미실시0·실패0이다. 다만 원 사용자 환경·접근 실패 이미지·Ruby 전체 실행·상류 전체 suite는 아래와 같이 미실시로 남긴다. 합성 연구판 실행을 원 환경 재현으로 쓰지 않는다. 원 이미지403/503이나 현재 옛 링크404를 통과 자료로 산입하지 않았다. 다음 명령은 이 인계에서 실행했다는 뜻이 아니다. 공개 재읽기·전체 재현은 [reproduce.md](reproduce.md)를 따른다.



### 7.1 원 ImageMagick7.0.10-61/Cygwin

현재 실행한 IM은7.1.1-43 Q16이다. 원판 바이너리·Cygwin 환경·원 image/coords/폰트를 확보하지 못했다. 고정 source를 Linux에서 빌드해도 Cygwin 원 환경 실행과는 다르다. 소스 수준 동작을 확인할 다음 명령은 아래와 같다. compiler·라이브러리·빌드 도구가 갖춰진 별도 재생 환경을 전제로 하며 이번에 실행한 명령은 아니다.

```sh
git clone https://github.com/ImageMagick/ImageMagick.git "$AF101_RUN/ImageMagick-7010"
git -C "$AF101_RUN/ImageMagick-7010" checkout --detach eeb41d70c9baf418a3aa75c424fb305362a1b280
cd "$AF101_RUN/ImageMagick-7010"
./configure --prefix="$AF101_RUN/im7010-prefix"
make -j2
make check TESTS=tests/validate-convert.tap
make check
```

고정 `Makefile.am`의 `TESTS`·`check_PROGRAMS`와 `tests/Makefile.am`의 `tests/validate`, `tests/validate-convert.tap` 항목을 직접 확인했다. 첫 `make check`는 convert 그룹, 둘째는 구성된 전체 suite다. source가 제공하는 예상 종료값과 실제 실행 수를 읽고 준비 실패/컴파일 실패/테스트 실패/미실시를 구별한다. 현재 연구에서 전체 C suite를 돌렸다고 쓰지 않는다. [명령 확인용 두 source 행](evidence/reproduction-sources.jsonl)

원 A2 재현에 필요한 입력은 원 이미지 bytes·SHA, `num`, `coords[0]` 제목·`coords[1]`/`coords[2]` crop geometry, Calibri-Bold의 실제 사용 판, Cygwin/Bash판, ImageMagick7.0.10-61 빌드/quantum 정보다.3.2와 root `probe.py` 실행 후 원 answer revision1 블록은 복사본의 `.cache/root-supplement/probes/answer-77797032-rev1.sh`와 `answer-77797051-rev1.sh`에 있다. 실제 입력을 확보한 Cygwin Bash에서 먼저 아래 구문 검사를 수행한다.

```sh
bash --version
convert -version
bash -n docs/workstreams/research/AF-RES-101/.cache/root-supplement/probes/answer-77797032-rev1.sh
bash -n docs/workstreams/research/AF-RES-101/.cache/root-supplement/probes/answer-77797051-rev1.sh
```

그다음 원 입력값을 셸 변수로 설정한 별도 스크립트에 원literal을 그대로 연결해 실행한다. 원literal에는 `val=300`이 있으므로 이를301로 바꿔 다른 분기를 시험하는 것은 별도 연구자 대조다. 잔여`fi`, `dims`의`d`, 고정30×40 patch, 문자열 안 escape를 먼저 고쳐서 원 제안이 통과했다고 쓰지 않는다. 실제 호출·입력 해시·stdout/stderr·출력 이미지·예상 두 patch geometry를 함께 기록한다.

### 7.2 Ruby/QuickMagick/RMagick/Open3

Ruby/gem 실행기가 없어서 wrapper 후보의 런타임 실행은 미실시다. 고정 QuickMagick0.8.0과 RMagick5.3.0 소스 검토는 실행을 대신하지 않는다. Ruby·해당 gem·native ImageMagick 의존성이 있는 격리 환경에서 아래처럼 원 코드 블록을 추출한다. 이 코드는 원snippet을 수정하지 않고 입력 경로/출력 파일 변수와 gem 판 선택만 연구 harness로 앞에 둔다.

```sh
python -B - <<'PY'
from pathlib import Path
import html, json, re
base = Path('docs/workstreams/research/AF-RES-101')
events = json.loads((base / '.cache/imagemagick/stage2/non-op-30day-projection.json').read_text())
event = next(e for e in events if e.get('post_id') == 77774667 and e.get('revision_number') == 2)
blocks = [html.unescape(s) for s in re.findall(r'<pre\b[^>]*><code\b[^>]*>(.*?)</code></pre>', event['body'], re.S)]
assert len(blocks) == 3
out = base / '.cache/ruby-replay'
out.mkdir(parents=True, exist_ok=True)
gems = ["gem 'quick_magick', '0.8.0'\n", "gem 'rmagick', '5.3.0'\n", '']
for i, body in enumerate(blocks, 1):
    (out / f'c{i}-literal.rb').write_text(body)
    prefix = gems[i-1] + 'remote_image = Struct.new(:path).new(ARGV.fetch(0))\noutfile = ARGV.fetch(1)\n'
    (out / f'c{i}-harness.rb').write_text(prefix + body)
print(json.dumps({'revision_guid': event['revision_guid'], 'body_sha256': event['body_sha256'], 'blocks': 3}))
PY
ruby --version
ruby docs/workstreams/research/AF-RES-101/.cache/ruby-replay/c1-harness.rb /absolute/path/to/input.png /absolute/path/to/c1-output.png
ruby docs/workstreams/research/AF-RES-101/.cache/ruby-replay/c2-harness.rb /absolute/path/to/input.png /absolute/path/to/c2-output.png
ruby docs/workstreams/research/AF-RES-101/.cache/ruby-replay/c3-harness.rb /absolute/path/to/input.png /absolute/path/to/c3-output.png
```

`/absolute/path/to/...`는 확보한 원 입력과 cache 안 새 출력 경로로 교체해야 한다. 원 입력이 없으면 root의 합성5픽셀 PPM을 쓸 수 있으나 원 사용자 실행이 아닌 연구자 대조로 표시한다. C3에 `ruby -rshellwords .../c3-harness.rb ...`를 적용한 별도 대조는 누락된 loading 조건을 보완한 **수정형**이다. RMagick 구판을 추가로 쓸 때는 그 판·ImageMagick 연결 정보를 기록하고5.3.0 반례와 섞지 않는다.

### 7.3 Typst·Git·FFmpeg 상류 suite

합성 실행은 수행했지만 아래 고정 상류 suite 자체는 미실시다. 빌드 의존성과 고정 source checkout을 준비한 뒤 다음 명령으로 재개한다. Typst 테스트는 ref를 갱신하는 `--update` 없이 실행한다.

| 고정 upstream checkout | 다음 명령 | 추가 입력 |
| --- | --- | --- |
| Typst `70ca0d257bb4ba927f63260e20443f244e0bb58c` | `cargo test --workspace --test tests -- layout/container.typ` / `cargo test --workspace --test tests -- math/content.typ` / `cargo test --workspace --test tests -- layout/align.typ` | Cargo·해당 판 빌드 의존성·upstream test assets/fonts. 실제 필터가 고른 시험 수 확인. [Typst 재현](evidence/typst-official/reproduce.md) |
| Git `bea9ecd24b0c3bf06cab4a851694fe09e7e51408` | 빌드 후 `make -C t T=t2070-restore.sh` | 그 판 Git 테스트 빌드와 test-lib. 설치된 Git2.56.1 합성 fixture와 구별 |
| FFmpeg `af25a4bfd2503caf3ee485b27b99b620302f5718` | 빌드 후 `make fate-copy-psp fate-copy-trac3074 fate-copy-trac236 SAMPLES=/absolute/path/to/fate-suite` | 공식 sample corpus의 `h264/wwwq_cut.mp4`, `eac3/csi_miami_stereo_128_spx.eac3`, `mov/fcp_export8-236.mov`; configure·sample SHA·ref diff 기록 |

### 7.4 접근 실패한 원 이미지·원 링크

QR 입력 `https://i.sstatic.net/iyzQE.png`, 답변 그림 `HUbgd.png`, `gDvdB.png`, `2dmoc.gif`는 당시403, 두 gyazo 사진은503, `https://imagemagick.org/Usage/distorts/`는404였다. 원주소·UTC는 [image-acquisition.json](evidence/imagemagick/stage3/image-acquisition.json)과 [original-link-acquisition.json](evidence/imagemagick/stage3/original-link-acquisition.json)을 읽는다. 접근이 회복되면 새 bytes와 SHA를 `.cache/`에 저장하고 과거 실패 영수증을 유지한다. QR에는 reader 이름/판·payload·성공 판정이, 사진에는 source corners·목표 크기/aspect·viewport와 자동 검출 단계가 추가로 필요하다. 접근 가능한 다른 그림을 원 입력이라고 대체하지 않는다.


## 색인에 넣을 한 줄

**AF-RES-101 — 8요청·18실후보/6빈칸: 제품명 필터A7반환/조작동일성 필터B14반환, 연구판에서 확인된 다른 유효 조작3개를 A가 모두 숨김(엄격literal2개); 전체 사전인지·신규 인지 비교는 미확인, B의 오류/부분중복도 보존.**

## 재개 첫 행동

새 자료 없이 같은 비율을 다시 산출하지 않는다. 첫 행동은 IM-A1의 실제 gem/engine 판과 원 이미지, IM-A2의 원 Cygwin shell/coords를 확보할 수 있는 공개 기록을 확인하는 것이다. 확보되지 않으면 [reproduce.md §7](reproduce.md)의 합성 재생을 원자료 대체로 주장하지 않고 기존 미확인을 유지한다. 인지 비교를 재개하려면 후보 전체를 제안 전에 알고 있었다는 명시 기록 또는 입력·판·출력이 연결된 실행 보고가 먼저 필요하다.

| 가장 중요한 불일치·약점 | 다음에 열 자료 또는 실행할 입력 | 어떤 관측이면 결론을 바꿀지 |
| --- | --- | --- |
| 원 사용자판·원 입력 부재와 normalize 문서/구현 불일치 | 7.0.10-61/Cygwin 및 실제 Ruby gem 판에서 원 이미지·좌표로 재생; QR은 원 픽셀과 판독기 결과 필요 | 동일 원판/입력에서 다른 출력 또는 목표 실패가 확인되면 연구판 지지 범위를 낮추고, 일치하면 해당 범위만 확장 |
| 신규 인지·완전 후보 사전 지식 미확인; 원문 예시와 적용 조작 차이 | 제안 전 실제 호출 기록/명시 회고·입력/판/출력 연결 실행; TY-A2 #red의 원 수식 포함 호출 | 전체 후보를 이미 알았다는 독립 증거가 나오면 중복 분모를 열고, 원문 그대로 출력 충족이 확인되면 literal 민감도 갱신 |
| 모집 경계와 후보 단위·노출의 민감도 | TY77831146 최초 첨부, IM77772356 최종 목표, IM-U2 첫 proposal의 부호/viewport/좌표 확인 | 적격 목표가 복구되면 모집 대체, 두 제안이 완전 동일하면17/6/13으로 병합; 기존 주 봉인과 차이는 별도 유지 |
