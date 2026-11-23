# AF-RES-093 · HANDOFF

## 상태·판정·첫 행동

**연구 상태: PARTIAL.** ①–④ 조사·기록·봉인·사후 검토·원장 재계산은 원격에 저장했고, Q1–Q7의 가능한 독립 질문과 반례 탐색을 마쳤다. 핵심 판별 정답은 신규 여섯 건 중 **1/6**만 확보했다. I3의 후보2 결원, 나머지 사건의 같은 입력·사용판·두 후보 결과 결손 때문에 오류 감소와 필드 필요 빈도는 산출 불가다. 자료 수 충족을 연구 완료로 바꾸지 않는다.

**다음 첫 행동:** P3 #5595의 원 유지관리자 비교를 Pillow **8.3.0의 서로 다른 fresh P images**에서 반복하고, 같은 p의 `getpalette()[:len(p)]`·index1·RGB를 각각 기록한다. 아래 실행 코드는 이 입력을 고정한다. 현재 gold는 게시된 순차 부착 비교이며 모든 판·저장·임의 편집의 대체 가능성이 아니다. 원 코드나 당시 실행 환경을 확보하지 못하면 새 실행 성공을 지어내지 말고 현재 PARTIAL을 유지한다.

작업 브랜치는 `work/research-af-res-093`, 소유 경로는 `docs/workstreams/research/AF-RES-093/`다. 중앙 `dot-control.json`과 다른 작업 경로는 변경하지 않았다. 이 인계는 Q별 SELF_CHECK와 결과 SHA 검사·원격 재열람을 끝낸 뒤 작성하는 마지막 단독 파일 커밋이다.

## 결과·중간 원격 커밋

| 단계 | 원격 SHA | 고정 내용 |
| --- | --- | --- |
| 시작 통합판 | `f72073277e6be643302a33f204d70baeb2c749a4` | 배정 당시 최신 chore/workspace-foundation; manifest 실제 start |
| 계획 기준 | `e2a80afec762b10ee7979136c6332473c70905bb` | 사용자 지정 브리프·계획판 |
| ① | `b9f878064bcf27b627a16977c9fa4580268aed3c` | 범위·모집 규칙·선행 교정·계약 |
| ② | `3c50d0bd1d8f3659d86f8cf45fe233595c3d2592` | 여섯 요청·12자리 A/B·후보 지원·사전 판정; 이후에만 후속 공개 |
| ③ | `0942f2d953a59f0050e3d73e665b0805fbf0dc2e` | 후속 원자료·정답 범위·반례·별도 검토·재계산 |
| ④ 결과·검사 대상 | `4b1233ead75c0a701b497226b446794eedea3ceb` | 필수 세 표·분모·비용·카드·SELF_CHECK·검산 |

고정 의존 인계: AF-RES-089 `dad9574f3ef1831e50071a019e5e80b6e8dc8983`, AF-RES-091 `f74a55d70b38d8585ff3512fe478442917444441`. 사용한 원 결과는 각각 `4f7ace747bfc5313679b8023ce85b4e7cc3217f2`, `952c81311dc7b5917fa04af6e4513dc5fd7020b0`이다. [manifest](manifest.json)에 계약 도구의 시작판·허용 경로·고정 의존이 있다.

CLI push는 셸 credential 부재로 실패했으므로 연결된 GitHub의 tree/commit/ref 기능으로 동일 tree를 게시하고 fetch하여 로컬을 원격 SHA와 맞췄다. ref 갱신에는 이전 head SHA를 조건으로 사용했고 force는 사용하지 않았다. 위 표는 실제 원격 SHA이며, 게시 전 일시적인 로컬 commit SHA가 아니다.

## 핵심 결과와 분모

| 항목 | A | B |
| --- | --- | --- |
| 사전 판정 | 분리2/6·유보4/6·묶음0/6 | 분리2/6·유보3/6·묶음1/6 |
| 같은 목적·판에서 사후 gold 확보 | 1/6 | 1/6 |
| gold가 있고 확정 판정한 자리 | 0/6 | 1/6 |
| 오병합 / gold분리인 확정 판정 | 0/0 · 산출 불가 | 0/0 · 산출 불가 |
| 불필요한 분리 / gold묶음인 확정 판정 | 0/0 · 산출 불가 | 0/1 |
| 전체 오판 / 채점 가능한 확정 판정 | 0/0 · 산출 불가 | 0/1 |
| payload UTF-8 bytes / 요청6건 | 4268/6 | 7449/6 |

B는 +3181 bytes(+74.5%)이며, 추가 구조필드36자리 중 text25·null11이다. 작성 중 새 원 URL open은 B0/6이다. 원문·metadata 저장량과 사람의 시간은 이 바이트 비용에 포함하지 않는다. A/B의 판정은5/6에서 같고 P3만 유보→묶음이다. 이 한 건은 이미 A에 있던 새 RGBRGB 순서 선호를 다시 해석한 효과와 섞였고, B의 다음 조작도 부착 단계에 가까워 엄격한 후속 조작 효과로 세지 않는다.

P3 gold는 [유지관리자의 양호출 출력](https://github.com/python-pillow/Pillow/issues/5595#issuecomment-877558030)과 [작성자의 raw 경로 수용](https://github.com/python-pillow/Pillow/issues/5595#issuecomment-877853085)에 근거한 **8.3.0·주어진 p·P index1·getpalette 목표의 묶음**이다. 두 fresh image의 독립 실행은 아니다. I1/P2의 분리 예측은 메커니즘 설명이 있어도 사후 정답 결손으로 미채점이다. P1 작성자의 질적 해결보고를 split gold로 허용하는 민감도에서도 A/B 모두 유보라 확정 오류 분모는 바뀌지 않는다.

고유 외부 1차 자료49개(요청6·버전 공식10·사후16·Calc/Arrow8·추가 반례9), 공유 저작 계보47개, 직접 원문을 연 이슈 사건9개를 구분했다. 원장155행 중106행은 하한 제외다. event_id26개에는 시험·명세 family가 있어 독립 사용자 사건26건이 아니다. 같은 프로젝트의 후보/시험/수정과 별도 에이전트의 해석을 독립 application 실행으로 세지 않았다. 외부 독립 실행은0건이다.

처음 작성 당시 revision은 여섯 건 모두 완전 복원하지 못했다. I3의 후대 수정 문장 사전 노출과 이동 전 본문 사용을 오염으로 보존했다. 하한에서 제외한31행은 정확한 개별 access UTC가 없어 범위 또는 기록 시각 상한·이유를 남겼다. Inkscape #2413/#2407 중복은 생성시각·제목에 근거한 추정이고 본문 추가 대조는 미실시이며, 앞3건 선정에는 영향이 없다.

## 핵심 파일

| 파일 | 역할 |
| --- | --- |
| [RESULT.md](RESULT.md) | 요청/후보 → A/B/사후 → 반환 링크의 세 필수 표를 맨 앞에 두고 분모·비용, 방법·반례, 마지막 약점3건 |
| [frame.csv](frame.csv) | 모집 원순번·질의·중복·제외·첫30·선택3+3 |
| [records.jsonl](records.jsonl) / [judgments.csv](judgments.csv) | 같은 후보의 A/B payload·바이트·공식 절, 12개 사전 판정과 후속 원근거·채점 범위 |
| [sources.jsonl](sources.jsonl) | 직접 열람 URL·UTC·판·절·짧은 확인·한계·저작/사건 계보·산입 여부 |
| [cards.md](cards.md) / [SELF_CHECK.md](SELF_CHECK.md) | 실제 반환 링크·조건·한 질문, Q1–Q7 근거/반증 탐색/한계/최소 확인 |
| [SCOPE.md](SCOPE.md) / [manifest.json](manifest.json) | 사전 기준·시작 SHA·계약·고정 의존 |
| [evidence/reconciliation.json](evidence/reconciliation.json) / [audit.py](audit.py) | 원 행에서 재계산한 분모·비용·결원·출처와 읽기 전용 재계산 |
| [evidence/adjudication/ADJUDICATION.md](evidence/adjudication/ADJUDICATION.md) | A/B 예측을 보지 않은 별도 해석자와 P3 범위 재검토 기록 |
| [evidence/calibrations.json](evidence/calibrations.json) | 089/091 교정 두 사건의 고정 원장·값·hash; 신규 적중 불산입 |
| [Inkscape 반례](evidence/inkscape/post/COUNTEREXAMPLES.md) / [Pillow 반례](evidence/pillow/post/counterexamples.md) / [타 분야](evidence/cross-domain/cross-domain.md) | 발견·미발견 범위, 생산자/편집 사용자/목록 편집자의 조건 |
| [reproduce.md](reproduce.md) / [evidence/deliverable-check.json](evidence/deliverable-check.json) | 재열람·재현 명령, 작성 단계 실제 검산 영수증 |

`assemble_preseal.py`는 최종 checkout에서 실행하지 않는다. 사후 원장을 사전 미채점 상태로 되돌리므로 필요하면 봉인 SHA의 별도 checkout에서만 사용한다. `audit.py`는 읽기 전용이다. 표와 카드는 `render_result.py`가 원 행을 바탕으로 생성한다.

## 결과 SHA에서 실제 실시한 검사

아래 검사의 대상은 전부 **`4b1233ead75c0a701b497226b446794eedea3ceb`**다. 검사를 위해 연구 파일이나 공통 코드를 바꾸지 않았다. Python은3.12.14이며 시작·종료 working tree가 모두 clean이었다.

| 검사 | 실제 명령 | 종료값·관측 |
| --- | --- | --- |
| 원 행 검산 | `python -B docs/workstreams/research/AF-RES-093/audit.py` | 0; 저장 reconciliation과 일치 |
| 명시적 계약 검사 | `python -B -m workbench.session check docs/workstreams/research/AF-RES-093/manifest.json --fetch` | 0; passed, remote_checked; 허용 밖0·충돌0·오류0 |
| 공통 검사 최초 | `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 1; 얕은 Git 이력의 backup restore 실패 |
| 이력 보완 | `git fetch --unshallow --no-tags origin chore/workspace-foundation` | 0; shallow true→false, 결과 SHA·작업 파일 유지 |
| 공통 검사 재실행 | `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 0; 아래 개별 단계 참조 |
| 공통/doctor | `python -m workbench doctor` | 0; passed |
| 공통/acceptance | `python scripts/check.py --require-git` | 0; passed |
| 공통/research-case | `python -m workbench run reference-audit discovery` | 0; passed |
| 공통/original-smoke | `python workbench/verify.py` | 0; passed |
| 공통/sessions | `python -m workbench.session check-all --fetch` | 0; no_active_sessions, count0, 작업별 검사 미실시 |

명시적 계약 검사 시각은 `2026-11-23T18:26:35.039053+00:00`, integration은 시작판과 같은 `f72073277e6be643302a33f204d70baeb2c749a4`이었다. 변경 경로104개 전부 소유 경로 안이었다. 공통 `check-all`의 종료0은 활성 session0건에 대한 정상 종료이며, 별도 작업 검사를 했다는 뜻이 아니다. 따라서 위의 manifest를 직접 지정한 `check --fetch` 결과를 별도로 보존한다.

공통 최초 실행 `2026-11-23T18:26:50+00:00`–`2026-11-23T18:26:57+00:00`은 backup restore에서 종료1이었다. 원인은 얕은 clone이 `f720732…`의 부모 `b1d90ad…`를 bundle에 완전히 포함하지 못한 것이다. `--unshallow` 이후 같은 SHA 재실행 `2026-11-23T18:27:46+00:00`–`2026-11-23T18:27:54+00:00`은 종료0이었다. acceptance의 unit test 묶음은55·7·9건 통과, 프로젝트 test/demo·export 및 Git bundle 복원도 통과했다. 새 AI 세션·제품 진실성·응용프로그램 동작·브라우저 연동을 이 검사로 증명하지 않는다.

작성 단계의 frame.csv byte 비교가 한 번 실패한 것은 worktree CRLF77개와 Git LF 정규화 차이였다. Git diff는 비었고 LF 정규화 bytes·CSV 원 행이 모두 같았다. 모집 행이나 봉인 예측을 바꾸지 않았으며 그 발견은 deliverable-check.json에 보존했다.

### 검사 영수증 요약 — 실제 출력에서 추출

```json
{
  "result_sha": "4b1233ead75c0a701b497226b446794eedea3ceb",
  "audit": {
    "exit_code": 0,
    "stdout_sha256": "dde66fb31a323d855bed9378d375fcabd022a3da57cedb5b01785d82906dd7c7"
  },
  "explicit_session_check": {
    "exit_code": 0,
    "status": "passed",
    "task_id": "af-res-093",
    "freshness": "remote_checked",
    "checked_at": "2026-11-23T18:26:35.039053+00:00",
    "checked_out_commit": "4b1233ead75c0a701b497226b446794eedea3ceb",
    "integration_commit": "f72073277e6be643302a33f204d70baeb2c749a4",
    "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc",
    "changed_paths_count": 104,
    "outside_paths": [],
    "unmerged_paths": [],
    "errors": []
  },
  "first_cloud_check": {
    "receipt_sha256": "59e1c3844b0b0942999eba90184683854c888b739719595fc9c1b570f8dbbbb2",
    "status": "failed",
    "exit_code": 1,
    "started_at": "2026-11-23T18:26:50+00:00",
    "completed_at": "2026-11-23T18:26:57+00:00",
    "source_start": {
      "commit": "4b1233ead75c0a701b497226b446794eedea3ceb",
      "dirty": false,
      "clean": true
    },
    "source_end": {
      "commit": "4b1233ead75c0a701b497226b446794eedea3ceb",
      "dirty": false,
      "clean": true
    },
    "checks": [
      {
        "name": "doctor",
        "command": [
          "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python",
          "-m",
          "workbench",
          "doctor"
        ],
        "status": "passed",
        "exit_code": 0,
        "started_at": "2026-11-23T18:26:50+00:00",
        "completed_at": "2026-11-23T18:26:50+00:00",
        "stdout_sha256": "1d595c91bc4b19064a72b5027bdea97e6748fd256edebdb0d710f60274116b77",
        "stdout_bytes": 256,
        "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "stderr_bytes": 0
      },
      {
        "name": "acceptance",
        "command": [
          "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python",
          "scripts/check.py",
          "--require-git"
        ],
        "status": "failed",
        "exit_code": 1,
        "started_at": "2026-11-23T18:26:50+00:00",
        "completed_at": "2026-11-23T18:26:57+00:00",
        "stdout_sha256": "12bbb14e946bdaa2da2062cae0597e913e1597336e129ca54e2613b0210fdbd1",
        "stdout_bytes": 10280,
        "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "stderr_bytes": 0
      }
    ],
    "session_validation": {
      "status": "not-executed",
      "reason": "not_reached"
    },
    "is_shallow": "true",
    "current_sha": "4b1233ead75c0a701b497226b446794eedea3ceb",
    "cause": "shallow checkout: bundle restoration could not read parent b1d90ad986a97b88a4caa764fc4830c86fae746e of f72073277e6be643302a33f204d70baeb2c749a4",
    "repair_command": "git fetch --unshallow --no-tags origin chore/workspace-foundation",
    "repair_exit_code": 0
  },
  "final_cloud_check": {
    "receipt_sha256": "a6bdb404e2bf88ae593ba4f444980b52d87bb2df521521ae46f514af5819e649",
    "status": "passed",
    "exit_code": 0,
    "started_at": "2026-11-23T18:27:46+00:00",
    "completed_at": "2026-11-23T18:27:54+00:00",
    "source_start": {
      "commit": "4b1233ead75c0a701b497226b446794eedea3ceb",
      "dirty": false,
      "clean": true
    },
    "source_end": {
      "commit": "4b1233ead75c0a701b497226b446794eedea3ceb",
      "dirty": false,
      "clean": true
    },
    "checks": [
      {
        "name": "doctor",
        "command": [
          "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python",
          "-m",
          "workbench",
          "doctor"
        ],
        "status": "passed",
        "exit_code": 0,
        "started_at": "2026-11-23T18:27:46+00:00",
        "completed_at": "2026-11-23T18:27:46+00:00",
        "stdout_sha256": "1d595c91bc4b19064a72b5027bdea97e6748fd256edebdb0d710f60274116b77",
        "stdout_bytes": 256,
        "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "stderr_bytes": 0
      },
      {
        "name": "acceptance",
        "command": [
          "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python",
          "scripts/check.py",
          "--require-git"
        ],
        "status": "passed",
        "exit_code": 0,
        "started_at": "2026-11-23T18:27:46+00:00",
        "completed_at": "2026-11-23T18:27:54+00:00",
        "stdout_sha256": "a608a69c1cabe4552bfe66362133256c027f8ecb8343cd0b8bf371b2264913c5",
        "stdout_bytes": 11416,
        "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "stderr_bytes": 0,
        "unit_test_counts": [
          55,
          7,
          9
        ],
        "backup": {
          "commit": "4b1233ead75c0a701b497226b446794eedea3ceb",
          "scope": "Git objects and refs only; not issues, secrets, DB, LFS or untracked files",
          "sha256": "1e9218bd07b023512f5a31b7d6c43c7f96663e83dd5bf3bc7c3bc97f5901347e",
          "status": "passed"
        },
        "exports": {
          "reference-audit": {
            "other_project_absent": true,
            "shared_helper_sha256": "5a26bd94f4aef02132d2f1f7840d6820f339d7caa7dd8d8b8d064cb679ac151a",
            "status": "passed"
          },
          "repo-intake": {
            "other_project_absent": true,
            "shared_helper_sha256": "5a26bd94f4aef02132d2f1f7840d6820f339d7caa7dd8d8b8d064cb679ac151a",
            "status": "passed"
          }
        }
      },
      {
        "name": "research-case",
        "command": [
          "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python",
          "-m",
          "workbench",
          "run",
          "reference-audit",
          "discovery"
        ],
        "status": "passed",
        "exit_code": 0,
        "started_at": "2026-11-23T18:27:54+00:00",
        "completed_at": "2026-11-23T18:27:54+00:00",
        "stdout_sha256": "a5604bef63fa50fd979f7c839ab5e79e571d88aeabda6ac6977a8c63fd6ac129",
        "stdout_bytes": 1775,
        "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "stderr_bytes": 0
      },
      {
        "name": "original-smoke",
        "command": [
          "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python",
          "workbench/verify.py"
        ],
        "status": "passed",
        "exit_code": 0,
        "started_at": "2026-11-23T18:27:54+00:00",
        "completed_at": "2026-11-23T18:27:54+00:00",
        "stdout_sha256": "c55b44687ea30f82dae29f4bce1cdc072e4fb96f779ff9fb4d39dc0da581f701",
        "stdout_bytes": 469,
        "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "stderr_bytes": 0
      },
      {
        "name": "sessions",
        "command": [
          "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python",
          "-m",
          "workbench.session",
          "check-all",
          "--fetch"
        ],
        "status": "passed",
        "exit_code": 0,
        "started_at": "2026-11-23T18:27:54+00:00",
        "completed_at": "2026-11-23T18:27:54+00:00",
        "stdout_sha256": "5dbd686bb3343f33497be6af8c6937c799634169e798e01675f30d9ec067d2ef",
        "stdout_bytes": 198,
        "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "stderr_bytes": 0
      }
    ],
    "session_validation": {
      "status": "not-executed",
      "reason": "no_active_sessions",
      "count": 0,
      "freshness": "not_checked",
      "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc"
    },
    "scope": "workbench checks, not product or browser integration",
    "environment": "codex-cloud",
    "python": "3.12.14",
    "is_shallow": "false",
    "current_sha": "4b1233ead75c0a701b497226b446794eedea3ceb",
    "git_status_porcelain": ""
  }
}
```

원 stdout/stderr는 검사기가 만든 로컬 `.workbench` 실행 로그에 있었으며 위에는 실제 종료값·시각·hash·시험수·범위를 보존했다. 로그 hash는 원 로그 동일성 표식이며 미실시 응용프로그램 실험을 대신하지 않는다.

## GitHub 결과 재열람

결과 SHA에서 아래12파일의 **본문을 GitHub에서 다시 받았고**, 응답 blob SHA를 로컬 Git 객체와 대조했다. 모든 항목이 일치했다. 원격 RESULT 첫 세 표 순서, records12행, sources155행·산입49, reconciliation의 A/B 분모도 다시 읽었다. 표본·교정·두 프로젝트 반례와 타 분야 파일까지 포함한다. 이 원격 검토는 새 외부 1차 자료 수에 더하지 않는다.

| 결과판 파일 | GitHub에서 다시 받은 blob SHA | 대조 |
| --- | --- | --- |
| RESULT.md | `e539957b104f8054f36b7fad2b1bb7bdf8075d0f` | 일치 |
| SELF_CHECK.md | `b39ae81b97b409b03c28de276986a4d899519768` | 일치 |
| cards.md | `497b15bb37fc4d3331732e2d808dd423b8fb6849` | 일치 |
| frame.csv | `51993796deb96a014fa7ecd07ec6f25c7c449e6e` | 일치 |
| records.jsonl | `8ae6ba58de6184dc42b07d8ea2d8f2a48a8cb275` | 일치 |
| judgments.csv | `57cc68a61b6072921c225adcef94557da162c160` | 일치 |
| sources.jsonl | `26edb281c09599f86d6eb87381115d2a4980ddc2` | 일치 |
| evidence/reconciliation.json | `39d38c753f2ef1ddd372e45bee1ecfaa993028af` | 일치 |
| evidence/calibrations.json | `28c33c2144ddea75c512573ee0e7d5b3fccc23ed` | 일치 |
| evidence/inkscape/post/COUNTEREXAMPLES.md | `04d7b02f8d2b57cbaa28d4154a1a25c3f59d7372` | 일치 |
| evidence/pillow/post/counterexamples.md | `75937f84c99a39fea00fc7f94ae0cfe960d91ffa` | 일치 |
| evidence/cross-domain/cross-domain.md | `11dc7ce49fc729b00feb01f72687393f71696225` | 일치 |

결과 RESULT의 SHA-256은 `8c0ffeb4a171d3da0b78aaf83da965ed3bd299add76b939107c886e061698b7a`, sources 원장은 `738cbfe0391e15b007e3416089a54b011e4027ff76b7d279134736d5aa91de9a`다. CSV hash 비교는 저장소의 LF 정규화된 Git blob을 기준으로 했다.

## 미실시 검사·재현 명령과 입력

**미실시:** Inkscape/Pillow/Calc/Arrow 원 application 빌드·원 시험 실행, 실제 사용자 카드 사용, 클릭·시간 절약 관측. 직접 읽은 것은 공개 원자료와 원 assertion·게시된 출력이다. 현재 환경 확인은 Pillow13.0.0·Inkscape1.4(`e7c3feb100`), Python3.9/LibreOffice/pyarrow 없음이었다. 이를 역사판 1.0.2·8.2/8.3·24.2.7.2·18.1.0 대신 사용하지 않았다. 원 SVG/GIF/PNG 및 정확한 배포판·완성 파이프라인 결손도 남아 있다. 이 미실시는 저장소 공통 검사 통과와 별개다.

깨끗한 별도 checkout에서 결과 검사를 다시 하려면:

```sh
git checkout --detach 4b1233ead75c0a701b497226b446794eedea3ceb
python -B docs/workstreams/research/AF-RES-093/audit.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-093/manifest.json --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

얕은 checkout이면 먼저 `git fetch --unshallow --no-tags origin chore/workspace-foundation`을 실행한다. 환경 이름은 검사 라벨이며 계정·모델 연결 증거가 아니다.

### 첫 행동 P3 — 원판 환경에서 실행할 정확한 입력

다음은 **미실시 재현 코드**다. Pillow8.3.0이 설치된 별도 실행환경에서 실행하며, 다른 판에서는 assert로 멈춘다. 유지관리자 원 비교의 순차 부착 대신 각 경로에 새 이미지를 만들어 상태 누적 가능성을 확인한다. palette 목표의 예상은 두 경로 모두 p이며, index/RGB는 추가로 기록할 관측이다.

```sh
python -B - <<'PY'
import json
import PIL
from PIL import Image, ImagePalette

assert PIL.__version__ == "8.3.0", PIL.__version__
expected = [0, 0, 0, 255, 0, 0, 0, 255, 0]
rows = []
for route in ("object", "raw"):
    p = list(expected)
    image = Image.new("P", (100, 100), 1)
    if route == "object":
        palette = ImagePalette.ImagePalette(mode="RGB", palette=p, size=len(p))
        image.putpalette(palette)
    else:
        image.putpalette(p, rawmode="RGB")
    rows.append({
        "route": route,
        "palette_prefix": image.getpalette()[:len(p)],
        "index_0_0": image.getpixel((0, 0)),
        "rgb_0_0": image.convert("RGB").getpixel((0, 0)),
    })
print(json.dumps({"pillow": PIL.__version__, "input_palette": expected, "results": rows}))
assert all(row["palette_prefix"] == expected for row in rows)
PY
```

이 실행 결과를 얻어도 연구자 실행은 유지관리자 원 시험·작성자 확인과 별도 귀속으로 기록한다. 임의 저장·dirty reload까지 대체품이라고 확대하려면 그 다음 조작을 양쪽에 동일하게 더해 별도 판정한다.

### 결손 사건·타 분야의 다음 명령과 입력

| 대상 | 실행할 명령·조작 | 고정 입력과 남은 조건 / 판정을 바꿀 관측 |
| --- | --- | --- |
| I1 | 1.0.2+r75+1 환경의 `inkscape ORIGINAL.svg`; 같은 text를 이동 중 Space stamp / Ctrl+D로 각각 복제한 다음 하나만 resize | #2225 원 SVG와 배포판 패치 일치를 먼저 확보. 원본·복제 text의 shape-inside 참조 ID/geometry를 기록. 둘 다 독립 resize면 분리 예측 재채점, 한 경로만 공유 참조면 분리 gold 후보 |
| I2 | 1.0.2에서 `inkscape ORIGINAL_LPE.svg`; 원본 path Ctrl+C 후 기존 Clone Original LPE의 clipboard link / 메뉴의 새 Clone Original path 생성, 이후 원본 shape 변경 | 기존 target ID·효과 보존 필요를 먼저 고정. 두 경로의 참조 href·target ID·후속 shape를 함께 기록. 버튼 실패만으로 새 메뉴 성공을 대신하지 않음 |
| I3 | 원판 eraser Delete, 원본/clone 선택 상태와 touched 객체를 고정 | 후보2를 먼저 찾기 전 paired 실행 명령을 만들 수 없다. Select+Delete나 spray copies로 입력을 바꾸지 않음 |
| P1 | Pillow8.2.0에서 `ImageOps.expand(frame, border=(0,bar_height,0,0), fill='white')` / `ImageOps.expand(frame.convert('RGB'), border=(0,bar_height,0,0), fill='white')` 뒤 동일 원 자막 draw/save 호출 | #5406의 원 in.gif·font·text·bar_height·프레임 처리·save 옵션을 먼저 확보. 완성 양 GIF의 색/투명도·원 프레임 유지와 실행판을 기록. 현재 자료만으로 누락 옵션을 채운 완성 스크립트를 원 실험이라고 만들지 않음 |
| P2 | Pillow8.3.0에서 같은 `indexed_with_transparency.png`를 각각 열어 `img.convert()` / `img.convert('RGBA')` | 원 공개 첨부의 URL/hash, P mode·RGB palette·transparency0를 먼저 고정. mode와 원 index0에 대응하는 alpha, 두 출력의 입력동일성 기록. 8.3.1은 별도 행 |
| Calc | LibreOffice24.2.7.2의 `libreoffice --calc`; A1=`=SUM(A2:A3)`, A2/A3 빈 상태에서 Copy→D1 `.uno:PasteOnlyValue`, E1 `.uno:PasteOnlyFormula`; D2=7·E2=7 입력 뒤 `.uno:CalculateHard` | C03 첫값0/0와 E1수식 `=SUM(E2:E3)`를 먼저 기록. 다음 D1/E1 값과 수식 문자열 기록. 예상0/7은 아직 실행 관측이 아님 |
| Arrow | 18.1.0 원 빌드의 dictionary test 실행파일에서 `--gtest_filter=TestDictionary.TransposeBasic:TestDictionary.TransposeTrivial:TestDictionary.GetValueIndex` | 원 build의 실행파일 위치는 미확인. 명세/원 시험의 아래 입력을 같은 실행에 넣고 decode와 index 선택 둘 다 기록. 원 시험 실행을 건너뛴 배열 계산과 구분 |

Arrow의 정확한 추가 관측 입력은 dictionary `[A,B,C]`, indices `[1,2,0,0]` → dictionary `[Z,A,C,B]`, map `[1,3,2]`, indices `[3,2,1,1]`이다. 논리값 소비자는 양쪽 `[B,C,A,A]`, raw `indices==0` 소비자는 앞의 행2·3과 뒤의 빈 집합을 비교한다. identity 대조는 D만 더하고 map `[0,1,2]`를 사용한다. 논리값/숫자 index가 같아도 index type bytes나 전체 dictionary 소비는 별도 조건이다. 세부 원 URL과 미발견 탐색은 SELF_CHECK Q7과 cross-domain 자료에 있다.

## 약점 3건과 다음 조사

| 틀릴 수 있는 주장 | 다음 조사 대상·입력·방법 | 판정을 바꿀 관측 |
| --- | --- | --- |
| 1. I1/P2 분리 안내와 P3 제한 묶음이 동일판의 독립 실행에서도 유지된다 | 위 원 SVG·PNG 및 P3 fresh image를 고정하고 양후보의 다음 resize/mode·alpha/palette를 나란히 기록. P1은 완성 caption/save pair를 추가 | I1/P2 양쪽이 필수 결과를 모두 만족하면 불필요한 분리, P3 한쪽만 다르면 범위 안 오병합. 현재 미채점5/6을 성공으로 세지 않음 |
| 2. P3 유보→묶음이 세 추가 필드의 효과다 | 앞 판정에 노출되지 않은 작성자에게 같은 요청·후보 절·열람 예산을 제공해 독립 또는 순서 교차 비교. 첫 출력 이후의 실제 소비 조작을 명시 | A 재독만으로 변화하거나 B가 원문 목적을 새로 해석하면 인과 주장 기각. B가 불필요한 분리를 늘리는 행도 같은 기준으로 집계 |
| 3. 소비값 구분을 모든 화면·편집·재계산·역복원에 전이할 수 있다 | Calc exact paste/recalc pair, Arrow decode/index 소비, Inkscape render/Select Original, Pillow RGBA remap의 고정판 대조; 원본/map/Undo 보유도 확인 | 이후 출력·선택 차이, identity 대조의 동등, 원본/map을 통한 복구가 각각 일반화·분리·복구 불가 주장의 적용 범위를 바꿈 |

## 진행 담당에게 넘길 사항

색인 제안 한 줄: **AF-RES-093 · PARTIAL · 새 요청6/A·B12, 후보쌍5, 엄격 gold1; P3만 유보→제한 묶음, 오판감소 산출 불가, B +3181bytes(+74.5%); 결과 4b1233ead75c0a701b497226b446794eedea3ceb.**

중앙 진행표·연구 색인·다른 작업 경로 갱신은 진행 담당이 이 결과 SHA와 최종 인계 커밋을 확인한 뒤 처리한다. 이 작업에서 중앙 파일을 직접 갱신하지 않았다. 다음 신규 작업을 기다리거나 다른 묶음의 결과를 빌려 정답 결손을 채우지 않았다.

