# AF-RES-096 · 최종 인계

## 상태와 바로 읽을 결론

**연구 상태: PARTIAL.** 신규 질문8·경로16의 사전 봉인 비교와 자료 하한46/24는 갖추었다. 지정092 의존 SHA가 현재 원격 끝과 달라 성공한 작업 계약을 만들지 못했고, 실제 manifest 검사는 종료값2였다. 문서 완결을 원 사용자 전체 환경의 실행 성공으로 일반화하지 않는다. P4의 그림 생성 실행은 의존성에서 실패했다.

사전 고정 규칙에서는 **A만0·B만0·양쪽5·어느 쪽도3·비교불가0**이다. 경계6쌍은 양쪽4/어느쪽도2, 같은범위 대조2쌍은1/1이다. B의 인접 자료는 경계6/6쌍에 실제 노출·열람됐고3/6쌍에서 반환됐으나 완결 여부를 바꾼 쌍은0/6이다. 불일치쌍0이므로 그 안의 승률은 **산출 불가(분모0)**다.

P3의 원 질문을 'Pandoc 옵션으로만 답해야 한다'로 좁히는 **사후 민감도**에서는 P3 양쪽이 부분이 되어 전체 양쪽4/어느쪽도4, 경계3/3, 대조1/1이다. 사전5/3을 덮어쓰지 않았고 단독완결0은 같다. P3는 이전 주 질문의 repost라고 자술한다. 따라서8은 서로 다른 선정 질문 ID라는 분석 단위이며 독립 실제 문제사건8이나 독립 사용자8을 입증한 값이 아니다.

핵심 불일치는 J2의 현재 채택·질문자 긍정 후속과 offset 입력 결손, P3의 옵션 선호와 사전 raw 표지 합성, P4의 문서 연결과 실제 TeX 실패다. 밀려난 주 도구12/12자리를 조사했지만 A만 완결 사례는 미관측이었다. J2 원시험 corroboration과 J4 Oniguruma 없는 build의 실패 경고가 B의 반환에서 빠진 설명 손실은 따로 남겼다.

## 시작판·고정 인수·원격 커밋

- 시작 통합 SHA: `f72073277e6be643302a33f204d70baeb2c749a4`.
- 계획 기준: `e2a80afec762b10ee7979136c6332473c70905bb`.
- 고정 AF-RES-092 인계: `e0d7ecda64bab2bd5d5779a9fb2a18d39a83bcdf`; 결과 원장: `707216d8a7f2f09948bb79bfb30e9b2d62cde9ef`.
- 작업 브랜치: `work/research-af-res-096`; 이 작업의 커밋 변경은 `docs/workstreams/research/AF-RES-096/`에만 있다. 중앙 `dot-control.json`과 다른 작업 경로는 수정하지 않았다.

| 묶음 | 원격 SHA | 보존한 내용 |
| --- | --- | --- |
| ① | `abf2bc2ac9303cb96e6109eba107684e5f858a42` | 신규 요청·76행 모집·13조건·판·두 질의·파일 범위·순위/예산 봉인 |
| ② | `d03ca37daf0c43688c68bc39417d84a9b84803e9` | 16경로 노출·64시도·사전 판단·공통 기준 재검토·순위/접근 감사 봉인 |
| ③ | `a8c88b115b8c15291df1bf59ef12582f7d848b4a` | 공개 후속·고정판 보조 실행·상류 반례·Sphinx/GDAL 교정·자료/밀려난파일 감사 |
| **④ 결과** | `1d399f630930d2763459e16509c5224b0cded9a0` | 세 핵심 표·최종169행 원장·카드·자가검산·독립 최종 감사·P3 사후 민감도 |

이 HANDOFF는④ 결과 검사와 원격 재열람을 끝낸 뒤 작성하는 **마지막 단독 파일 커밋**이다. 아래 검사는④ SHA를 대상으로 했고 이후 HANDOFF 커밋까지 검사한 것으로 표현하지 않는다. 각 이전 묶음의 파일 목록·해시와 원격 확인은 `evidence/seal1-*`부터 `seal4-files.json`까지에 남아 있다.

## 핵심 파일과 Q별 완료 범위

| 파일 | 인수할 내용 |
| --- | --- |
| [RESULT.md](RESULT.md) | 표1/2/3의8/16/8행, 분모, 사전·사후 구분, 다른 분야, 정확히3약점 |
| [SELF_CHECK.md](SELF_CHECK.md) | Q1–Q7 답·직접 URL·반례 탐색·한계·다음 최소 확인 |
| [protocol.json](protocol.json), [frame.csv](frame.csv) | 최종① 기준과 원 모집·제외·revision. 초기 selected 제안보다 protocol을 우선 |
| [exposure.jsonl](exposure.jsonl), [pairs.csv](pairs.csv) | 검색32·본문64·같은파일 절이동194, 사전5/3과 절차상 비교가능8/8 |
| [sources.jsonl](sources.jsonl), [metrics.json](metrics.json) | 169원장행 중 고유1차46, 주10·인접10·상류시험4·R08·Sphinx7·GDAL/PROJ7 |
| [outcomes.csv](outcomes.csv), [cards.md](cards.md) | 답8·댓글18, 현재채택4/8·질문자30일후속5/8·정확한 질문자실행확인0/8; 요청당2링크와질문1개 |
| [사후 민감도](evidence/post-evaluation-sensitivity.json) | P3 option-only 4/4와 질문ID/실제문제사건 독립성 구분. 원값·변경시각·이유·영향행 보존 |
| [다른 분야](evidence/crossdomain/report.md) | Sphinx text/cache와 새 dot이미지, GDAL grid없는투영과 OnlyBest/grid/network 대조. 새 모집·승패 기여0 |
| [최종 독립 감사](evidence/audit/final-report-audit.md) | 표·분모·169원기록·46하한·카드·링크·약점·봉인 불변 PASS, 오류0 |
| [manifest.json](manifest.json) | 성공 manifest가 아니라 최초 start 실패 영수증과 요청한 시작판/허용경로/고정 의존/계약 snapshot |

Q1–Q5의 요청·노출·열람·문서 판정 자리에는 공석이 없다. P1–P4의 C2 공석은 독립 명시조건이 하나라서 그대로 둔 것이다. Q6의 공개 후속과 보조 실행, Q7의 원문·상류 기대값 대조는 완료했다. Q7 프로그램 실제 실행과 원 사용자 전체 실행은 미확인이다. 알려진 교정 자료14개를 새 요청 발견14건이나 실행 성공14건으로 세지 않는다.

## 실제 검사와 원격 재열람

환경은 Linux / Python3.12.14이며 `chatgpt-cloud`는 검사 호출자가 붙인 실행환경 이름이다. 별도 Codex Cloud 계정이나 GitHub Actions 실행을 증명하는 표지가 아니다.

| 검사 | 실제 대상·결과 | 해석 |
| --- | --- | --- |
| `python -B -m workbench.session check docs/workstreams/research/AF-RES-096/manifest.json --fetch` | 결과 SHA `1d399f630930d2763459e16509c5224b0cded9a0`, **exit2**, `{"status":"invalid","error":"unsupported task manifest"}` | 성공 계약이 아닌 실패 영수증을 거부했다. 정상 계약·의존 최신성 검사 통과가 아님 |
| `python -B scripts/cloud_check.py --environment chatgpt-cloud --fetch-contract --require-clean` | 같은 SHA, **exit0 / passed**, 시작·끝 clean, SHA 불변 | doctor, acceptance, research-case, original-smoke 종료값0. acceptance의55·7·9시험, export·Git bundle 복원 통과 |
| 공통 검사 내부 session check-all | 명령exit0이나 payload는 `not-executed / no_active_sessions / count0 / freshness:not_checked` | 신규 AF-RES-096 계약 검사를 대신하지 않음 |
| 사전·자료·최종 독립 감사 | ④에 커밋된 안정 파일에서 모두 PASS/오류0; 아래 GitHub readback이 같은 결과 내용임을 재확인 | 사실의 진실성·기억 영향 부재·원환경 성공을 자동 보증하지 않음 |
| GitHub 결과 재열람 | RESULT·pairs·sources·metrics·SELF_CHECK·P3민감도·Q7보고·jq/Pandoc실행 원장9개가 정확한④ SHA에서 내용 일치 | 원격 Git의 EOL 정규화된 텍스트 기준. ① CSV3개·② pairs1개의 원 EOL 차이는 이전 감사대로 보존 |

최종 검사는 `2026-11-23T19:00:54.192424+00:00`부터 `2026-11-23T19:01:21.252551+00:00`까지 수행했다. 전체 임시 stdout을 인계의 유일 근거로 삼지 않도록 실제 명령·종료값·stdout/stderr 해시·공통 하위 검사 결과를 아래에 커밋한다.

```json
{
  "target_sha": "1d399f630930d2763459e16509c5224b0cded9a0",
  "platform": "Linux-6.18.57-x86_64-with-glibc2.41",
  "python": "3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]",
  "started_utc": "2026-11-23T19:00:54.192424+00:00",
  "finished_utc": "2026-11-23T19:01:21.252551+00:00",
  "clean_at_start": true,
  "clean_at_end": true,
  "end_sha": "1d399f630930d2763459e16509c5224b0cded9a0",
  "checks": [
    {
      "name": "session",
      "command": "python -B -m workbench.session check docs/workstreams/research/AF-RES-096/manifest.json --fetch",
      "started_utc": "2026-11-23T19:00:54.194616+00:00",
      "finished_utc": "2026-11-23T19:00:54.263839+00:00",
      "exit_code": 2,
      "stdout_sha256": "10c4294881f1d6a0b8bad5e9ae03c3e518c860b450803f477d99a731e3fad2e7",
      "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "stdout": "{\"status\": \"invalid\", \"error\": \"unsupported task manifest\"}"
    },
    {
      "name": "common",
      "command": "python -B scripts/cloud_check.py --environment chatgpt-cloud --fetch-contract --require-clean",
      "started_utc": "2026-11-23T19:00:54.264484+00:00",
      "finished_utc": "2026-11-23T19:01:21.251462+00:00",
      "exit_code": 0,
      "stdout_sha256": "098e0517902638eaa2b025d9da0f61884d1bd6c9a6784a465d38635bae6c28d4",
      "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    }
  ],
  "common_steps": [
    {
      "name": "doctor",
      "command": "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python -m workbench doctor",
      "exit_code": 0,
      "status": "passed"
    },
    {
      "name": "acceptance",
      "command": "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python scripts/check.py --require-git",
      "exit_code": 0,
      "status": "passed"
    },
    {
      "name": "research-case",
      "command": "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python -m workbench run reference-audit discovery",
      "exit_code": 0,
      "status": "passed"
    },
    {
      "name": "original-smoke",
      "command": "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python workbench/verify.py",
      "exit_code": 0,
      "status": "passed"
    },
    {
      "name": "sessions",
      "command": "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python -m workbench.session check-all --fetch",
      "exit_code": 0,
      "status": "passed"
    }
  ],
  "session_validation": {
    "status": "not-executed",
    "reason": "no_active_sessions",
    "count": 0,
    "freshness": "not_checked",
    "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc"
  }
}
```

원격 재열람의 실제 확인시각과 blob 식별자는 다음과 같다.

```json
{
  "result_sha": "1d399f630930d2763459e16509c5224b0cded9a0",
  "checked_utc": "2026-11-23T19:00:30.555Z",
  "receipts": [
    {
      "path": "docs/workstreams/research/AF-RES-096/RESULT.md",
      "git_blob_sha": "e947e9b50224f39a84785ddaf47f8e16d800bbe7",
      "exact_normalized_text": true,
      "chars": 59334,
      "expected_chars": 59334
    },
    {
      "path": "docs/workstreams/research/AF-RES-096/pairs.csv",
      "git_blob_sha": "de51cb97bcebb8d85a81739c2d6f349c485ced13",
      "exact_normalized_text": true,
      "chars": 2272,
      "expected_chars": 2272
    },
    {
      "path": "docs/workstreams/research/AF-RES-096/sources.jsonl",
      "git_blob_sha": "e4f5506d618b21ab6914bd41517aba0a31634ef8",
      "exact_normalized_text": true,
      "chars": 526332,
      "expected_chars": 526332
    },
    {
      "path": "docs/workstreams/research/AF-RES-096/metrics.json",
      "git_blob_sha": "e1ec7eac5602d8265f41b864fb0f6a9e8f14b8af",
      "exact_normalized_text": true,
      "chars": 4599,
      "expected_chars": 4599
    },
    {
      "path": "docs/workstreams/research/AF-RES-096/SELF_CHECK.md",
      "git_blob_sha": "fb0cbe8efa8cc50434829b93ad6ee87917031442",
      "exact_normalized_text": true,
      "chars": 9184,
      "expected_chars": 9184
    },
    {
      "path": "docs/workstreams/research/AF-RES-096/evidence/post-evaluation-sensitivity.json",
      "git_blob_sha": "ea588c7ab0898d8599d488496d7aa0c7d2d15730",
      "exact_normalized_text": true,
      "chars": 2202,
      "expected_chars": 2202
    },
    {
      "path": "docs/workstreams/research/AF-RES-096/evidence/crossdomain/report.md",
      "git_blob_sha": "7c385623b691c3970ebf18527e3ab0c1fdb16871",
      "exact_normalized_text": true,
      "chars": 10610,
      "expected_chars": 10610
    },
    {
      "path": "docs/workstreams/research/AF-RES-096/evidence/post-jq/runtime-results.json",
      "git_blob_sha": "3620739097c932c3bac0a48d389612827ec4d661",
      "exact_normalized_text": true,
      "chars": 19899,
      "expected_chars": 19899
    },
    {
      "path": "docs/workstreams/research/AF-RES-096/evidence/post-pandoc/execution.json",
      "git_blob_sha": "2a70ac9bdea4b6b243204d36ee836d28fac65aad",
      "exact_normalized_text": true,
      "chars": 11177,
      "expected_chars": 11177
    }
  ]
}
```

## 실행 확인·실패·미실시와 재현 입력

- **jq1.7.1 실제13회:** J4의 봉인 A/B 필터 각각4벡터로8/8 정확 출력, 원잘림 J1 JSON은exit5/닫힘수리본3행일치, J3의 연구자 envelope·배열 변형2회 일치. J4의 범위밖 JSON quoting 반례는exit0인데 잘못 잘라 실패했다. 공식 checksum·입력·필터·stdout·stderr가 [jq 실행 원장](evidence/post-jq/runtime-results.json)과 validation 폴더에 있다.
- **Pandoc3.6 실제5개 probe:** P3 합성 post-knitr 입력의 기본 표내 br38, 봉인 raw 보정0, 사후 옵션0; 모두exit0이고 보정 두 출력은 바이트 동일. P4 원 TeX의 AST는exit0/RawBlock2개 중TikZ1개, 봉인 그림 filter는exit83/내부 pdflatex exit1. [Pandoc 실행 원장](evidence/post-pandoc/execution.json)에 입력/프로그램/출력 hash와 실제 명령이 있다.
- **미실시:** R이 없어 P3 R→knitr 전체, pdflatex.fmt와 TeX 패키지·pdf2svg가 없어 P4 끝단 그림 생성, Sphinx/Graphviz 및 GDAL/PROJ 고정판 상류 원시험 실행. 원문에 적힌 기대값만을 실제 실행으로 보고하지 않는다.

새 결과 SHA의 **별도 checkout**에서 다음 재생 명령을 사용할 수 있다. 이 스크립트들은 관측파일을 다시 쓰므로 새 실행을 기존 관측과 혼동하지 말고 별도 실행 결과로 보존한다. 이미 수행한 관측은 Git의④ SHA에 고정돼 있다.

```sh
python -B docs/workstreams/research/AF-RES-096/evidence/post-jq/prepare_runtime.py
python -B docs/workstreams/research/AF-RES-096/evidence/post-jq/reproduce_runtime.py
python -B docs/workstreams/research/AF-RES-096/evidence/post-pandoc/prepare-probes.py
python -B docs/workstreams/research/AF-RES-096/evidence/post-pandoc/run-probes.py
```

jq 입력은 `evidence/post-jq/validation/`의 커밋된 fixture다. Pandoc 준비 스크립트는 고정 R0 GUID·URL·hash로 입력을 재구성한다. P4는 GUID `5938869D-E61B-410C-97F5-035731293446`의 원 TeX와 `evidence/pandoc/p4-raw-tikz.lua` 봉인 바이트를 쓴다. 실제 명령은 Pandoc3.6에서 `--standalone -N --from=latex+raw_tex --to=html5 --lua-filter=.../p4-raw-tikz.lua --embed-resources .../_cache/p4/example.tex --output=.../_cache/p4/example.html`이다. 작동하는 pdflatex format·standalone/xcolor/tikz·원 automata/positioning/arrows와 pdf2svg가 먼저 필요하다.

P3 전체 실행의 입력은 GUID `1B054996-200D-4090-BAC2-A656EDCBC92D`의 두 code block을 그대로 저장한 `RMtemplate.html`과 `original.Rmd`다. 답변자 화면의 R4.4.2/rmarkdown2.29/Pandoc3.1.11.1을 고정한 환경에서 `Rscript -e 'rmarkdown::render("original.Rmd")'`를 실행하고 실제 knit된 Markdown·--from 값·표 HTML을 보존한다. 이 판 조합은 답변자에게 귀속되며 원 질문자의 판을 복원한 것은 아니다.

Q7의 실행 명령·입력·반대조건은 [상세 report](evidence/crossdomain/report.md)에 고정돼 있다. 최소 명령은 다음과 같으며 각 해당 프로젝트의 지정 SHA checkout 루트에서 실행한다.

```sh
# Sphinx a1510de4777eaa2e569435f95b05f6f3293d7035
dot -V
python -m pytest tests/test_builders/test_build_text.py tests/test_extensions/test_ext_graphviz.py -rA
sphinx-build -b html -D graphviz_dot=/nonexistent/af096-dot tests/roots/test-ext-graphviz output-missing
# GDAL 35a44cc570cdf4dbd55611e4bd61da76e56bc221 + PROJ 9.5.1
python -m pytest autotest/osr/osr_ct.py -k 'test_osr_ct_2 or only_best_enabled' -rA
# PROJ 41f79ccfe107d3951dac6826f289b55d17cc3b81
gie test/gie/gridshift.gie
ctest --test-dir build -N
ctest --test-dir build -R proj_test_cpp --output-on-failure
```

Sphinx 입력은 tests/roots/test-ext-graphviz 원 fixture이며 normal/missing-dot 출력 캐시를 공유하지 않는다. GDAL은 `(50.5,10,0)`, EPSG4746→4326, OnlyBest True/False, de_adv_BETA2007.tif 유무·hash를 고정한다. PROJ-data manifest와 network/영역/축 조건, 실제 실행·skip 수를 함께 기록해야 판정이 바뀐다.

## 막힌 이유와 다음 첫 행동

최초 요청한 start는 `work/research-af-res-092=e0d7ecda64bab2bd5d5779a9fb2a18d39a83bcdf`를 고정했으나 관측한 원격 끝은 `e742bc665efde0d3883ec4d0f5479e03e914fcbf`였다. 도구가 `dependency changed: work/research-af-res-092`로 exit2를 반환했다. 이를 임의 새 의존으로 바꾸거나 브랜치를 되돌리거나 검사기를 약화하지 않았다. 실패 영수증의 스키마를 성공 manifest로 위장하지 않았다.

**다음 첫 행동은 진행 담당이 고정 인계 SHA와 현재092 원격 끝의 차이를 읽고, 고정 연구 입력을 유지하면서 어떤 계약을 새로 발급할지 결정하는 것이다.** 기존 manifest 실패 기록은 보존한다. 계약 문제가 정리되기 전에 공통검사의 no_active_sessions를 계약 통과로 표시하지 않는다. 중앙 진행표·색인은 진행 담당이 갱신한다.

## 약점 3건에 대한 다음 조사

| 틀릴 수 있는 주장 | 다음 조사 대상·입력·방법 | 판정을 바꿀 관측 |
| --- | --- | --- |
| 인접2자리 정책에는 완결 이득·손실이 없다 | 새로운 공개 요청, 절/파일 예산을 별도 사전 등록, A/B 독자를 분리하고 밀려난 필수 절·실패조건을 기록 | 같은 요구·예산의 실제 B만 또는 A만 완결. 이번0불일치는 일반 동등성 근거가 아님 |
| 문서완결5/8은 원 사용자에게 실행 가능한 답이다 | P4 정확 TeX/converter 환경·원 TeX·봉인 Lua부터 재생. P3 옵션만 허용 여부와 전체 R 실행, J2 offset 입력, J4 quoting 문법을 확인 | 같은 명시조건에서 출력/요구수단 불일치 또는 전체원환경 재현 성공. P3 옵션 한정 민감도는 이미4/8이며 원승패와 분리 |
| 생산자/소비자 명명 규칙이 중요한 외부 경계를 포괄한다 | 새 요청에서 실행단계·라이브러리·데이터자원을 구별. Sphinx dot/cache, GDAL OnlyBest/grid의 위 입력을 실행 | 명명된 생산자 없이 자원 가용성만으로 성패가 갈리거나 외부의존을 주 도구 원문만으로 충분히 설명하는 사례 |

## 색인 제안 한 줄

`AF-RES-096 | PARTIAL | 신규 jq/Pandoc 8쌍: 인접 원문 노출·열람6/6, 사전 단독완결0/8(양쪽5/어느쪽도3), 옵션 한정 민감도4/4; 자료46, 계약 의존 drift·원환경 실행 미확인 | docs/workstreams/research/AF-RES-096/RESULT.md | depends AF-RES-092@e0d7ecda64bab2bd5d5779a9fb2a18d39a83bcdf`

