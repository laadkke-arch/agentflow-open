# AF-RES-053#1 세션 인수인계

## 1. 식별

- 작업 ID / 시도 번호: **AF-RES-053 / #1**.
- 작업 종류: 배정은 `web-pro`. 실제 수행은 ChatGPT 클라우드 세션의 셸·GitHub 도구·동일 모델 보조 조사다.
- 실제 모델과 실행 위치: 이 세션 실행 지시의 모델 표기는 GPT-6 Astra Pro. 별도 web-pro UI의 실행판은 검증하지 않았다. 실행 위치·명령 cwd는 아래 영수증에 있다.
- 공개 가능한 작업자 참조: AF-RES-053#1, `/root`와 동일 모델 보조 조사자3명. 비공개 서비스 작업 ID는 등록하지 않았다.
- 역할/이슈: 새 도표·자막 요구의 N/I/D 사전 예측과 후속 출력 비교 연구.
- 저장소/브랜치: `laadkke-arch/agentflow-open` / `work/research-af-res-053`.
- 실제 시작 커밋: `573a8f1a7cafa90b87bcbb4267e73fee12385bda`.
- 계획 통합판: `d7e60daf1b5b2c918502c407982566369b7149e3`.
- 마지막 확인한 고정 결과 SHA / 원격에서 읽히는 결과 저장 SHA: **`87a375d72c269f921589e98b27265e344a70000d`**.
- 마지막 실제 진행 증거: 위 SHA의 RESULT·수용 원장 원격 내용 대조 일치, session check `passed`/exit0; 종료 UTC **2026-11-23T02:34:24.512091+00:00**.
- PR 주소: 생성하지 않음. 인계는 자기 브랜치의 고정 커밋이다.
- 최종 확인 시각(UTC): 2026-11-23T02:34:24.512091+00:00.
- 상태: **BLOCKED — 부분 인계. 저장·검사는 끝났지만6요구 충원과 후속 원전 배당/역사판 검증이 충족되지 않았다.** 이 문서는 검사 뒤 작성하는 마지막 단독 커밋 대상이다.

고정 결과의 [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/87a375d72c269f921589e98b27265e344a70000d/docs/workstreams/research/AF-RES-053/RESULT.md), [수용 원장](https://github.com/laadkke-arch/agentflow-open/blob/87a375d72c269f921589e98b27265e344a70000d/docs/workstreams/research/AF-RES-053/evidence/acceptance-evidence.json), [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/87a375d72c269f921589e98b27265e344a70000d/docs/workstreams/research/AF-RES-053/SELF_CHECK.md)를 먼저 읽는다. RESULT의 **표1은1~20행(데이터3~20행,18행)**, **표2는22~29행(데이터24~29행,6행)**이다. 이 문서 자체의 SHA는 브랜치 마지막 커밋으로 확인한다. 결과판을 자기 후속 HANDOFF 커밋 SHA로 소급 표기하지 않는다.

## 2. 사용자 요구/작업 범위

- 목표: 같은 수신 API N을 공통으로 읽은 상태에서 같은 분야 I와 다른 분야 D가 같은 추가 예산으로 서로 다른 A/B 예측을 더하는지, 결과 전 봉인과 후속 원문으로 판별한다.
- 읽은 기준: 시작판의 AGENTS/STATE/DOT_AUTOMATION/RESEARCH_WORKFLOW, control의 AF-RES-053 계약, 제품 브리프. 의존 인계는 [AF-RES-049@ae40dc268bca0774ee8e5d8326cfb8aa8101b87b](https://github.com/laadkke-arch/agentflow-open/blob/ae40dc268bca0774ee8e5d8326cfb8aa8101b87b/docs/workstreams/research/AF-RES-049/HANDOFF.md), 결과판은 [ab50b40bd12109fb13c29f2f0256e6654ae81c47](https://github.com/laadkke-arch/agentflow-open/blob/ab50b40bd12109fb13c29f2f0256e6654ae81c47/docs/workstreams/research/AF-RES-049/RESULT.md)이다. 해당 RESULT/runs/cards를 읽었다.
- 자기 허용 경로: `docs/workstreams/research/AF-RES-053/`만. 작업 전용 branch의 변경은 모두 이 경로 안이며 dot-control.json 변경은 없다.
- 조사 범위: UTC2021-01-01~2024-12-31 생성 공개 issue, PR 제외, open/closed 함께. 대소문자 무시 substring으로 Vega 첫40건, libass 전체18건의 본문을 읽었다. M02/M03은 기준 배경만 사용했다.
- 타 세션/운영 환경: 같은 차수 다른 산출물을 기다리거나 인계 입력으로 추가하지 않았다. 운영 서비스 변경·배포는 이 작업에 없다.

### 현재 충족·결손

| 항목 | 실제 수 | 상태 |
| --- | ---: | --- |
| 후보 본문 검토 | Vega40 + libass18 =58 | 기간 내 libass 제목 후보 자체가18개. 현재 최초 가용 본문 기준 |
| 예정/충원 요구 | 6 / 5 | L03 미충원. L02 연구자 정상 대조를 빼는 감도는4/6 |
| N/I/D 카드·예측·결과 | 각18행 | 충원15행+미충원3행을 같은 ID로 보존 |
| I/D 추가 예산 | 5/5쌍 일치 | 단어72/68/114/87/87, 그림0/0/0/1/1; 각≤200단어·1그림 |
| source 기록 / 고유 1차 저작 | 188행 / 보수적71개 | 총수22 하한 충족. 큰 총수의 다수는 선정 제외 원문 |
| 필수 배당 | 요청자5/6, 수신문헌5/4, 인쇄·지도4/4, 독립후속0/6, 반례2/2 | 역할 결손을 초과 원전 수로 상쇄하지 않음 |
| 공개 동일판·입력·조작·새출력 | 관측0/20논리셀 완전 일치 | 모든 셀 판정 미확인. 실패율·성능 동률이 아님 |
| 같은 I/D 사전 예측 | 5/5요구 | 서로 다른 사전예측0/5; D 새 정답 조건부 분모0 → 해당 없음 |
| 연구판 보조 재생 | 2요구,6변형→5SVG+1compile 실패 | 범주 선택 동률2/2; 원작성자 역사판·공개후속 배당 제외 |
| 사후 구판 민감도 | V03 두 변형→2SVG |2.7.0은 A/B 모두10검정. 사전 적중으로 산입 안 함 |

## 3. 실제 변경

| 파일 | 변경 사항/이유 | 어떻게 확인했나 |
| --- | --- | --- |
| manifest.json, SCOPE.md | 입력판·허용경로·단계별 노출/정정 기록 | 지정 start exit0; 고정 SHA·계약 hash·봉인 파일 불변 대조 |
| frame.csv, operations.json |58후보와6자리, 최초 선택지·입력·판정 규칙 | 본문 직접 검토·메타데이터 완전성 대조·제외 사유 기록 |
| cards.csv, predictions.csv | 표시창·단어/그림 수·창밖 노출과18사전 예측 | 결과 전 원격봉인 `9b13473…`; 실제 I/D 예산5쌍·hash 검산 |
| outcomes.csv, streams/*/outcomes.json | 같은18ID의 후속 근거와20논리셀 결손 | 실제 그림/진술/수락/패치/시험을 분리, 원입력·조작 차이 확인 |
| sources.jsonl, evidence/source-counts.json | URL·판·위치·확인 내용·한계·계보 원장 |71고유 저작 보수적 계수; pointer-only/실패/metadata/자체 재생 제외 |
| replay/ | 고정 입력·코드·실제SVG7개·compiled/scenegraph·설치/실행/무결성 영수증 |5.1.0 주재생6변형,2.7.0 사후2변형; input/output hash·정확 label identity/색 대조 |
| RESULT.md, SELF_CHECK.md, evidence/acceptance-evidence.json | 필수 표18/6행, Q1~Q7, 적용 중단 조건, 질문별 반증/재개 자료,26요건 상태 | root 자체 검토+같은모델 방법/원장/최종서술 교차 검토. 독립 사람 검토는 미실시 |
| evidence/*readback*, evidence/session-check-result* | 결과 커밋의 원격 내용과 실제 지정 검사 로그 | 고정 SHA에서 재열람·명령 exit0/UTC/원문 stdout 보존 |

### 단계별 원격 커밋

| 묶음 | 고정 원격 SHA |
| --- | --- |
| 초기 계약·읽기 전 범위 | `0a78a46bdbc5fc5d000c211f083eb46b485442e9` |
| ① 노출·모집·조작 규칙 | `a6b1624c899eacf118c0e01350f52cbd53e21dae` |
| ② 원전 카드·사전 예측 | `9b13473a76a381fe27d775524aa65416ec28f591` |
| ③ 후속·반례·재생·민감도 | `59cabc4175980555cc3387f5d8447180b96ff568` |
| ④ 필수 표·수용 원장·자체 검토 | `c906fc608c78025b8e3577e6a559c6b2feb44217` |
| 원격 재열람·지정 검사 영수증 저장 / 최종 결과 묶음 | `87a375d72c269f921589e98b27265e344a70000d` |
| 마지막 HANDOFF | 이 문서 한 파일만 변경하는 후속 단독 커밋. 실제 SHA는 브랜치 HEAD/Git 변경 목록으로 확인 |

①·②의 순서를 결과 뒤에 재구성하지 않았다. ② 서버 commit 시각은2026-11-23T01:55:36Z, 첫 후속 요청은 libass01:56:50.120240Z, Vega01:58:10.743Z다. frame 준비 CRLF와 Git LF의 hash 차이는 내용변경 없이 별도 설명했다. 공개 원문은 URL·위치·해시·자체 요약으로 보존하고 전체 매뉴얼·원첨부 그림 캐시는 재배포하지 않았다. 커밋한 연구 입력·자체 SVG·실행 영수증으로 실제 재생을 확인할 수 있다.

## 4. 실제 검증 결과

### 지정 검사와 원격 재열람

최초 결과 `c906fc6…`의 원격 대조/검사는 [remote-readback-result.json](https://github.com/laadkke-arch/agentflow-open/blob/87a375d72c269f921589e98b27265e344a70000d/docs/workstreams/research/AF-RES-053/evidence/remote-readback-result.json), [session-check-result.json](https://github.com/laadkke-arch/agentflow-open/blob/87a375d72c269f921589e98b27265e344a70000d/docs/workstreams/research/AF-RES-053/evidence/session-check-result.json) 및 stdout/stderr 파일에 있다. 결과 저장 SHA `87a375d72c269f921589e98b27265e344a70000d`도 다시 원격에서 읽었고 같은 명령을 검사했다. 수용 원장의 R21은 최초 결과 검사 증거를 가리키며, R22의 결과시점 대기 상태는 이 최종 HANDOFF 단독 커밋에서 확정한다.

```bash
python -B -m workbench.session check docs/workstreams/research/AF-RES-053/manifest.json --fetch
```

- 검사한 소스 커밋: `87a375d72c269f921589e98b27265e344a70000d`.
- 실제 종료 코드: **0**; status **passed**; freshness **remote_checked**.
- 시작 UTC: 2026-11-23T02:34:16.523055+00:00; 종료 UTC: 2026-11-23T02:34:24.512091+00:00.
- `outside_paths`, `unmerged_paths`, `errors`: 모두 빈 배열.
- 이 검사는 Git 계약·소유 경로의 검사다. 여섯 요구의 연구 완료나 제품 동작을 검증한 명령이 아니다.
- `validate.py --phase final`은46검산 통과, 연구 완전 충족은 false다. 원장18ID·예산5쌍·봉인 불변·source필드/계보·필수표/Q1~Q7·끝약점3건을 검사했다.

최종 고정판 원격 재열람의 실제 기록:

```json
{
  "checked_UTC": "2026-11-23T02:34:15.991798+00:00",
  "result_sha": "87a375d72c269f921589e98b27265e344a70000d",
  "files": [
    {
      "file": "RESULT.md",
      "ref": "87a375d72c269f921589e98b27265e344a70000d",
      "remote_blob_sha": "bc9f4f7b4d8baf2fe660c9ecb5643ce1fc4e5dc9",
      "characters": 31051,
      "lines": 180,
      "exact_content_match": true,
      "utf8_bytes": 49371,
      "sha256": "aa3aac4c4010535a3512b827d797d2e21530821ad2305c7e336bcb4fbfc0a2aa"
    },
    {
      "file": "evidence/acceptance-evidence.json",
      "ref": "87a375d72c269f921589e98b27265e344a70000d",
      "remote_blob_sha": "233bd0d2b90fc731a3779589a1d91ed663a407eb",
      "characters": 18863,
      "lines": 693,
      "exact_content_match": true,
      "utf8_bytes": 21967,
      "sha256": "274b90fad0295d5d195bfec6d7523df194adcd0a213c9beebcdc2daa15874c18"
    }
  ]
}
```

최종 지정 검사의 실제 실행 metadata와 stderr(비어 있음):

```json
{
  "command": [
    "python",
    "-B",
    "-m",
    "workbench.session",
    "check",
    "docs/workstreams/research/AF-RES-053/manifest.json",
    "--fetch"
  ],
  "cwd": "/workspace/scratch/650acb0f03c4/agentflow-open",
  "checked_result_sha": "87a375d72c269f921589e98b27265e344a70000d",
  "started_UTC": "2026-11-23T02:34:16.523055+00:00",
  "finished_UTC": "2026-11-23T02:34:24.512091+00:00",
  "exit_code": 0,
  "stdout_sha256": "ac176d3696858fe9b1bb3cfbf54395b48ec93167374ccca219829c07a4ec954a",
  "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "stderr": ""
}
```

다음은 최종 지정 검사의 **실제 stdout 전체**다. 편집한 성공 요약으로 대체하지 않았다.

```json
{
  "status": "passed",
  "task_id": "af-res-053",
  "freshness": "remote_checked",
  "checked_at": "2026-11-23T02:34:24.503729+00:00",
  "checked_out_commit": "87a375d72c269f921589e98b27265e344a70000d",
  "task_base_commit": "573a8f1a7cafa90b87bcbb4267e73fee12385bda",
  "integration_commit": "921502a4c7729ca39d2a79319901725deecd48e5",
  "scope_base_commit": "573a8f1a7cafa90b87bcbb4267e73fee12385bda",
  "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc",
  "changed_paths": [
    "docs/workstreams/research/AF-RES-053/.gitignore",
    "docs/workstreams/research/AF-RES-053/RESULT.md",
    "docs/workstreams/research/AF-RES-053/SCOPE.md",
    "docs/workstreams/research/AF-RES-053/SELF_CHECK.md",
    "docs/workstreams/research/AF-RES-053/assemble_outcomes.py",
    "docs/workstreams/research/AF-RES-053/assemble_sources.py",
    "docs/workstreams/research/AF-RES-053/cards.csv",
    "docs/workstreams/research/AF-RES-053/evidence/7278-attachment-receipt.json",
    "docs/workstreams/research/AF-RES-053/evidence/acceptance-evidence.json",
    "docs/workstreams/research/AF-RES-053/evidence/commit-ledger.jsonl",
    "docs/workstreams/research/AF-RES-053/evidence/comparison-counts.json",
    "docs/workstreams/research/AF-RES-053/evidence/donor-card-windows.json",
    "docs/workstreams/research/AF-RES-053/evidence/freeze-verification.json",
    "docs/workstreams/research/AF-RES-053/evidence/governance-sources.jsonl",
    "docs/workstreams/research/AF-RES-053/evidence/operation-refinements.json",
    "docs/workstreams/research/AF-RES-053/evidence/outcomes-validation.json",
    "docs/workstreams/research/AF-RES-053/evidence/pre-outcome-freeze.json",
    "docs/workstreams/research/AF-RES-053/evidence/remote-readback-result.json",
    "docs/workstreams/research/AF-RES-053/evidence/replay-plan.md",
    "docs/workstreams/research/AF-RES-053/evidence/root-card-sources.jsonl",
    "docs/workstreams/research/AF-RES-053/evidence/search-and-exposure.json",
    "docs/workstreams/research/AF-RES-053/evidence/session-check-result.json",
    "docs/workstreams/research/AF-RES-053/evidence/session-check-result.stderr.txt",
    "docs/workstreams/research/AF-RES-053/evidence/session-check-result.stdout.txt",
    "docs/workstreams/research/AF-RES-053/evidence/session-start.json",
    "docs/workstreams/research/AF-RES-053/evidence/source-counts.json",
    "docs/workstreams/research/AF-RES-053/evidence/validation.json",
    "docs/workstreams/research/AF-RES-053/frame.csv",
    "docs/workstreams/research/AF-RES-053/operations.json",
    "docs/workstreams/research/AF-RES-053/outcomes.csv",
    "docs/workstreams/research/AF-RES-053/predictions.csv",
    "docs/workstreams/research/AF-RES-053/replay/analysis-amendments.json",
    "docs/workstreams/research/AF-RES-053/replay/analyze.py",
    "docs/workstreams/research/AF-RES-053/replay/analyze_sensitivity.py",
    "docs/workstreams/research/AF-RES-053/replay/artifact-hashes.json",
    "docs/workstreams/research/AF-RES-053/replay/compare_outputs.py",
    "docs/workstreams/research/AF-RES-053/replay/dependency-integrity.json",
    "docs/workstreams/research/AF-RES-053/replay/dependency-pins.json",
    "docs/workstreams/research/AF-RES-053/replay/imported-versions-runtime-v270.json",
    "docs/workstreams/research/AF-RES-053/replay/input-diffs.json",
    "docs/workstreams/research/AF-RES-053/replay/input-extraction.json",
    "docs/workstreams/research/AF-RES-053/replay/inputs/V02-boundary-A.json",
    "docs/workstreams/research/AF-RES-053/replay/inputs/V02-boundary-B.json",
    "docs/workstreams/research/AF-RES-053/replay/inputs/V02-normal-A.json",
    "docs/workstreams/research/AF-RES-053/replay/inputs/V02-normal-B.json",
    "docs/workstreams/research/AF-RES-053/replay/inputs/V02-original-boundary.json",
    "docs/workstreams/research/AF-RES-053/replay/inputs/V02-researcher-normal.json",
    "docs/workstreams/research/AF-RES-053/replay/inputs/V03-fixed-A.json",
    "docs/workstreams/research/AF-RES-053/replay/inputs/V03-fixed-B.json",
    "docs/workstreams/research/AF-RES-053/replay/inputs/V03-original.json",
    "docs/workstreams/research/AF-RES-053/replay/inspect-runtime.cjs",
    "docs/workstreams/research/AF-RES-053/replay/logs/analyze-label-correction.receipt.json",
    "docs/workstreams/research/AF-RES-053/replay/logs/analyze-label-correction.stderr.txt",
    "docs/workstreams/research/AF-RES-053/replay/logs/analyze-label-correction.stdout.txt",
    "docs/workstreams/research/AF-RES-053/replay/logs/analyze-v270.receipt.json",
    "docs/workstreams/research/AF-RES-053/replay/logs/analyze-v270.stderr.txt",
    "docs/workstreams/research/AF-RES-053/replay/logs/analyze-v270.stdout.txt",
    "docs/workstreams/research/AF-RES-053/replay/logs/analyze.receipt.json",
    "docs/workstreams/research/AF-RES-053/replay/logs/analyze.stderr.txt",
    "docs/workstreams/research/AF-RES-053/replay/logs/analyze.stdout.txt",
    "docs/workstreams/research/AF-RES-053/replay/logs/imports-v270.receipt.json",
    "docs/workstreams/research/AF-RES-053/replay/logs/imports-v270.stderr.txt",
    "docs/workstreams/research/AF-RES-053/replay/logs/imports-v270.stdout.txt",
    "docs/workstreams/research/AF-RES-053/replay/logs/install-v270-retry-once.receipt.json",
    "docs/workstreams/research/AF-RES-053/replay/logs/install-v270-retry-once.stderr.txt",
    "docs/workstreams/research/AF-RES-053/replay/logs/install-v270-retry-once.stdout.txt",
    "docs/workstreams/research/AF-RES-053/replay/logs/install-v270.receipt.json",
    "docs/workstreams/research/AF-RES-053/replay/logs/install-v270.stderr.txt",
    "docs/workstreams/research/AF-RES-053/replay/logs/install-v270.stdout.txt",
    "docs/workstreams/research/AF-RES-053/replay/logs/install.receipt.json",
    "docs/workstreams/research/AF-RES-053/replay/logs/install.stderr.txt",
    "docs/workstreams/research/AF-RES-053/replay/logs/install.stdout.txt",
    "docs/workstreams/research/AF-RES-053/replay/logs/output-differences.receipt.json",
    "docs/workstreams/research/AF-RES-053/replay/logs/output-differences.stderr.txt",
    "docs/workstreams/research/AF-RES-053/replay/logs/output-differences.stdout.txt",
    "docs/workstreams/research/AF-RES-053/replay/logs/render-v270.receipt.json",
    "docs/workstreams/research/AF-RES-053/replay/logs/render-v270.stderr.txt",
    "docs/workstreams/research/AF-RES-053/replay/logs/render-v270.stdout.txt",
    "docs/workstreams/research/AF-RES-053/replay/logs/render.receipt.json",
    "docs/workstreams/research/AF-RES-053/replay/logs/render.stderr.txt",
    "docs/workstreams/research/AF-RES-053/replay/logs/render.stdout.txt",
    "docs/workstreams/research/AF-RES-053/replay/logs/versions.receipt.json",
    "docs/workstreams/research/AF-RES-053/replay/logs/versions.stderr.txt",
    "docs/workstreams/research/AF-RES-053/replay/logs/versions.stdout.txt",
    "docs/workstreams/research/AF-RES-053/replay/output-differences.json",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V02-boundary-A.cell-checks.json",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V02-boundary-A.scenegraph-export.json",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V02-boundary-A.scenegraph.json",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V02-boundary-A.svg",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V02-boundary-A.vega.json",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V02-normal-A.cell-checks.json",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V02-normal-A.scenegraph-export.json",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V02-normal-A.scenegraph.json",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V02-normal-A.svg",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V02-normal-A.vega.json",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V02-normal-B.cell-checks.json",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V02-normal-B.scenegraph-export.json",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V02-normal-B.scenegraph.json",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V02-normal-B.svg",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V02-normal-B.vega.json",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V03-fixed-A.axis-checks.json",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V03-fixed-A.scenegraph-export.json",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V03-fixed-A.scenegraph.json",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V03-fixed-A.svg",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V03-fixed-A.vega.json",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V03-fixed-B.axis-checks.json",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V03-fixed-B.scenegraph-export.json",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V03-fixed-B.scenegraph.json",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V03-fixed-B.svg",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V03-fixed-B.vega.json",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V03-v270-A.scenegraph.json",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V03-v270-A.svg",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V03-v270-A.vega.json",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V03-v270-B.scenegraph.json",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V03-v270-B.svg",
    "docs/workstreams/research/AF-RES-053/replay/outputs/V03-v270-B.vega.json",
    "docs/workstreams/research/AF-RES-053/replay/pre-render-review.json",
    "docs/workstreams/research/AF-RES-053/replay/prediction-comparison.csv",
    "docs/workstreams/research/AF-RES-053/replay/preview-observations.json",
    "docs/workstreams/research/AF-RES-053/replay/preview-receipts.json",
    "docs/workstreams/research/AF-RES-053/replay/render-receipts.json",
    "docs/workstreams/research/AF-RES-053/replay/replay-review.md",
    "docs/workstreams/research/AF-RES-053/replay/reproduce.cjs",
    "docs/workstreams/research/AF-RES-053/replay/reproduce.py",
    "docs/workstreams/research/AF-RES-053/replay/results.json",
    "docs/workstreams/research/AF-RES-053/replay/retrieval-receipts.json",
    "docs/workstreams/research/AF-RES-053/replay/sensitivity-dependency-integrity.json",
    "docs/workstreams/research/AF-RES-053/replay/sensitivity-dependency-pins.json",
    "docs/workstreams/research/AF-RES-053/replay/sensitivity-plan.json",
    "docs/workstreams/research/AF-RES-053/replay/sensitivity-render-receipts.json",
    "docs/workstreams/research/AF-RES-053/replay/sensitivity-results.json",
    "docs/workstreams/research/AF-RES-053/replay/sensitivity-versions.json",
    "docs/workstreams/research/AF-RES-053/replay/sensitivity.cjs",
    "docs/workstreams/research/AF-RES-053/replay/sensitivity.py",
    "docs/workstreams/research/AF-RES-053/replay/setup-retrieval-receipts.json",
    "docs/workstreams/research/AF-RES-053/replay/sources-new.jsonl",
    "docs/workstreams/research/AF-RES-053/replay/validation.json",
    "docs/workstreams/research/AF-RES-053/replay/versions.json",
    "docs/workstreams/research/AF-RES-053/sources.jsonl",
    "docs/workstreams/research/AF-RES-053/streams/donors/.gitignore",
    "docs/workstreams/research/AF-RES-053/streams/donors/SOURCE_COUNTS.json",
    "docs/workstreams/research/AF-RES-053/streams/donors/donor-review.md",
    "docs/workstreams/research/AF-RES-053/streams/donors/figure-observations.json",
    "docs/workstreams/research/AF-RES-053/streams/donors/method-review.md",
    "docs/workstreams/research/AF-RES-053/streams/donors/qgis-history-connector.json",
    "docs/workstreams/research/AF-RES-053/streams/donors/qgis-history-receipt.json",
    "docs/workstreams/research/AF-RES-053/streams/donors/qgis-tree-receipt.json",
    "docs/workstreams/research/AF-RES-053/streams/donors/retrieval-receipts.json",
    "docs/workstreams/research/AF-RES-053/streams/donors/sources.jsonl",
    "docs/workstreams/research/AF-RES-053/streams/libass/.gitignore",
    "docs/workstreams/research/AF-RES-053/streams/libass/aegisub-source-receipts.json",
    "docs/workstreams/research/AF-RES-053/streams/libass/all-issue-metadata.json",
    "docs/workstreams/research/AF-RES-053/streams/libass/body-read-receipts.json",
    "docs/workstreams/research/AF-RES-053/streams/libass/census-page1-receipt.json",
    "docs/workstreams/research/AF-RES-053/streams/libass/census-page2-receipt.json",
    "docs/workstreams/research/AF-RES-053/streams/libass/final-report-review.md",
    "docs/workstreams/research/AF-RES-053/streams/libass/followup-open-receipt.json",
    "docs/workstreams/research/AF-RES-053/streams/libass/followup-retrieval-receipts.json",
    "docs/workstreams/research/AF-RES-053/streams/libass/followup-timeline-receipts.json",
    "docs/workstreams/research/AF-RES-053/streams/libass/frame.csv",
    "docs/workstreams/research/AF-RES-053/streams/libass/original-attachment-receipts.json",
    "docs/workstreams/research/AF-RES-053/streams/libass/outcome-code-receipts.json",
    "docs/workstreams/research/AF-RES-053/streams/libass/outcome-review.md",
    "docs/workstreams/research/AF-RES-053/streams/libass/outcome-sources.jsonl",
    "docs/workstreams/research/AF-RES-053/streams/libass/outcome-validation.json",
    "docs/workstreams/research/AF-RES-053/streams/libass/outcomes.json",
    "docs/workstreams/research/AF-RES-053/streams/libass/receiver-candidates.json",
    "docs/workstreams/research/AF-RES-053/streams/libass/receiver-metadata-receipts.json",
    "docs/workstreams/research/AF-RES-053/streams/libass/receiver-review.md",
    "docs/workstreams/research/AF-RES-053/streams/libass/receiver-source-receipts.json",
    "docs/workstreams/research/AF-RES-053/streams/libass/receiver-sources.jsonl",
    "docs/workstreams/research/AF-RES-053/streams/libass/related-attachment-receipts.json",
    "docs/workstreams/research/AF-RES-053/streams/libass/release-metadata.json",
    "docs/workstreams/research/AF-RES-053/streams/libass/retrieval-receipts.json",
    "docs/workstreams/research/AF-RES-053/streams/libass/screening-validation.json",
    "docs/workstreams/research/AF-RES-053/streams/libass/selection.md",
    "docs/workstreams/research/AF-RES-053/streams/libass/sources.jsonl",
    "docs/workstreams/research/AF-RES-053/streams/vega/.gitignore",
    "docs/workstreams/research/AF-RES-053/streams/vega/decode-7278-receipt.json",
    "docs/workstreams/research/AF-RES-053/streams/vega/direct-body-receipts.json",
    "docs/workstreams/research/AF-RES-053/streams/vega/final-ledger-review.md",
    "docs/workstreams/research/AF-RES-053/streams/vega/frame.csv",
    "docs/workstreams/research/AF-RES-053/streams/vega/outcome-retrieval-receipts.json",
    "docs/workstreams/research/AF-RES-053/streams/vega/outcome-review.md",
    "docs/workstreams/research/AF-RES-053/streams/vega/outcome-sources.jsonl",
    "docs/workstreams/research/AF-RES-053/streams/vega/outcomes.json",
    "docs/workstreams/research/AF-RES-053/streams/vega/receiver-candidates.json",
    "docs/workstreams/research/AF-RES-053/streams/vega/receiver-review.md",
    "docs/workstreams/research/AF-RES-053/streams/vega/receiver-sources.jsonl",
    "docs/workstreams/research/AF-RES-053/streams/vega/release-metadata.json",
    "docs/workstreams/research/AF-RES-053/streams/vega/retrieval-receipts.json",
    "docs/workstreams/research/AF-RES-053/streams/vega/selection.md",
    "docs/workstreams/research/AF-RES-053/streams/vega/sources.jsonl",
    "docs/workstreams/research/AF-RES-053/validate.py"
  ],
  "outside_paths": [],
  "unmerged_paths": [],
  "errors": [],
  "boundary": "Git contract and ownership checks; not a new AI chat or product verification"
}
```

### 실제 renderer 검사와 재현 명령

- 5.1.0/Vega5.20.2: setup exit0, render exit1(지정 V02 경계B compile 실패1건), analyze exit0. B를 고쳐 성공 출력으로 대체하지 않았다.
- V03 A는1빨강9검정, B는0빨강10검정. V02 정상A/B는 동일SVG, 경계A는 field/title 대응 유지, B는 SVG를 생성하지 못함.
- 2.7.0/Vega4.4.0: 첫 설치 HTTP503/exit1, 동일 URL·lock 한 번 재시도 exit0, 추가 두 변형 render exit0. A/B compiled JSON은 동일하고 두 조건 모두 사라져 대상 y축10개가 검정이다.
- 현대 Node24.22.3·native canvas 없음. SVG 구조/색 판독 및 보조 시각 확인이며 역사 폰트 픽셀·독자 가독성 실험은 아니다. V03 긴 라벨6개 줄임표/일부 막대 덮임은 목표 색과 별도 한계다.

저장소 루트에서 필요한 재현만 실행한다. `render`의 종료1이 실제 연구 결과이므로 아래 명령들을 `&&`로 묶어 이후 분석을 생략하지 않는다.

```bash
python -B docs/workstreams/research/AF-RES-053/replay/reproduce.py setup
python -B docs/workstreams/research/AF-RES-053/replay/reproduce.py render
python -B docs/workstreams/research/AF-RES-053/replay/reproduce.py analyze
python -B docs/workstreams/research/AF-RES-053/replay/compare_outputs.py
python -B docs/workstreams/research/AF-RES-053/replay/sensitivity.py setup
python -B docs/workstreams/research/AF-RES-053/replay/sensitivity.py render
python -B docs/workstreams/research/AF-RES-053/replay/analyze_sensitivity.py
python -B docs/workstreams/research/AF-RES-053/validate.py --phase final
```

입력은 [replay/inputs](https://github.com/laadkke-arch/agentflow-open/blob/87a375d72c269f921589e98b27265e344a70000d/docs/workstreams/research/AF-RES-053/replay/inputs)의 V02-normal-A/B, V02-boundary-A/B, V03-fixed-A/B JSON이다. A의 callback과 모든 변경 위치는 reproduce.cjs/input-diffs.json에 있다. 원문 입력 해시, 실제 import 판, release lock·tarball integrity, stdout/stderr/UTC/exit는 [replay-review](https://github.com/laadkke-arch/agentflow-open/blob/87a375d72c269f921589e98b27265e344a70000d/docs/workstreams/research/AF-RES-053/replay/replay-review.md)가 정확 파일로 연결한다. 구판은 같은 V03 파일 bytes를 그대로 읽는다. 설치/재생 파일의 쓰기 범위도 해당 replay 아래다.

**미실시/미확인:** L01/L02 renderer 실행, GIF 전체 프레임 분석, 픽셀 오차 실측, 작성자 실제판 복원, 원작성자 성공 수락, 독립 사람 검토. libass는 B 숫자와 완성 입력이 미정이어서 지금 유효한 비교 렌더 명령 자체를 확정할 수 없다. 임의 값을 넣은 명령을 정답 검증 명령으로 제공하지 않는다. 실행 환경보다 먼저 필요한 입력은 아래6절에 적었다. 이미 확인한 구현을 다시 여는 명령과 입력은 다음과 같다(렌더 실행이 아님).

```bash
git clone --branch 0.17.1 --depth 1 https://github.com/libass/libass.git docs/workstreams/research/AF-RES-053/replay/scratch/libass-0.17.1
git -C docs/workstreams/research/AF-RES-053/replay/scratch/libass-0.17.1 show e8ad72accd3a84268275a9385beb701c9284e5b3:libass/ass_parse.c
git -C docs/workstreams/research/AF-RES-053/replay/scratch/libass-0.17.1 show e8ad72accd3a84268275a9385beb701c9284e5b3:libass/ass_render.c
```

위 clone 경로가 이미 있다면 기존 checkout의 tag/SHA를 확인하고 show만 실행한다. 이 소스 재열람 절차의 명령은 재개용이며 이 경로에서 새 clone을 실행했다는 뜻은 아니다. API/소스 내용은 이번 조사에서 다른 격리 캐시를 통해 실제 읽었다.

## 5. 판단·근거

**현재 결론:** 이번5요구에서는 I와 D의 사전 선택·정상/경계 예측이 모두 같았다. 서로 다른 예측을 가르는 조건부 분모가0이므로 D의 새 정답/새 오답 비율은 해당 없음이다. 공개 역사 자료의 성과는5요구 모두 미확인이다. 보조 연구판의2요구에서는 N/I/D가 같은 범주 선택에 도달했다. 따라서 D의 독자적 추가 판별력이 확인됐다고 표시하지 않았다.

V03의 수신 API는 axis datum의 문맥을 직접 알려 주며, 고정 범주의 색 선택에 필요한 방향을 이미 제공했다. QGIS의 지물 속성 규칙을 무조건 원행 resilience 접근으로 옮기는 B는 실제로 목표 색에 실패하지만, 봉인 D가 B를 권한 관측은 없다. 이를 D 새 오답으로 세지 않았다. 구판2.7.0에서 A도 실패하는 사후 반례는 판/API 가용성을 확인하지 않고 링크의 결론을 옮길 수 없음을 보여 준다. V02 N의 fieldTitle 이름만으로 전체 경계를 독립 예측했다고 주장하지도 않는다. 공통 선택지·창밖 구현 지식이 있었다.

V01 후속 그림은 다른10행·count/resolve 변경이 있어서 원135행 A 성공을 증명하지 못한다. L01 원그림은 요구 도식이며 B 실행이 아니다. L02 원그림의 실패는 봉인 전부터 알고 있었고, 후속 t collision 설명은 B margin 성공 출력이 아니다. URL·판·쪽/절/행·확인일·근거 수준은 [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/87a375d72c269f921589e98b27265e344a70000d/docs/workstreams/research/AF-RES-053/sources.jsonl)188행, [각 셀 원장](https://github.com/laadkke-arch/agentflow-open/blob/87a375d72c269f921589e98b27265e344a70000d/docs/workstreams/research/AF-RES-053/outcomes.csv), [RESULT Q1~Q7](https://github.com/laadkke-arch/agentflow-open/blob/87a375d72c269f921589e98b27265e344a70000d/docs/workstreams/research/AF-RES-053/RESULT.md)에 남겼다. 실제 원문 확인일은2026-11-23 UTC이며 저작의 발행일/판과 구분했다.

설계 제안은, 수신 문서가 두 조작을 모두 허용하면서 아직 결정하지 못한 보존 속성/우선순위가 있고 D가 그 차이를 검증 가능한 관측으로 이어 줄 때 타 분야 링크를 후보로 제공하자는 것이다. 이는 사용자 확정 요구나 사람의 창의성/시간/채택에 대한 관측 결론이 아니다. 세 보기의 단어/그림 수는 같아도 정보밀도·노출·판·유형을 완전히 통제하지 못했다.

다른 세션과의 충돌 가능 항목은 없다. 모든 저장 변경은 owned_path에 있고 통제파일·공통 색인은 수정하지 않았다. 공개 자료의 주소·자체 요약·직접 실행 산출물과 실행 환경만 저장했으며 인증정보를 넣지 않았다. 외부 원전 전체나 원본 그림을 재배포한 보고서로 쓰지 않는다.

### 색인 제안(이번에는 공통 색인을 수정하지 않음)

| 제안 항목 | 연결 파일/원전 | 용도·중단 조건 |
| --- | --- | --- |
| AF-RES-053 / 같은 예산의 타 분야 링크 판별력 | RESULT·cards·predictions·outcomes, 상태 부분 인계 |5요구 예측 일치와2요구 연구판 재생.6요구 검증 완료로 표시 중단 |
| 접근 문자열과 표시 문자열의 분리 | V02 CompileOptions·QGIS Text tab·원repeat 보조SVG |field 접근과 셀별 title을 함께 확인할 때. 단일 title 복사 또는 실제판 미확인 시 보장 중단 |
| 표현식 객체 문맥·판 경계 | V03 ConditionalAxisProperties·scale-domain 설명·2.7/5.1 출력 |source-row 속성이 축 객체에 있는지 확인할 때. 고정 category를 미래 데이터 해법으로 확대 중단 |
| 정적 중심/선택적 표기의 수신 한계 | L01 CSS 중앙 규칙, L02 QGIS 지도, libass t 예외 |단위·내용·발화 시간 보존을 명세할 때. 수치 B나 모든 event 보장을 원전 유추로 대신하지 않음 |

## 6. 다음 대화의 첫 행동

1. `work/research-af-res-053`의 최신 SHA를 재조회하고 마지막 커밋이 이 HANDOFF 한 파일만 추가했는지 확인한다. 고정 결과 입력은 `87a375d72c269f921589e98b27265e344a70000d`다.
2. 이 SHA의 RESULT 첫 두 표, 수용 원장, outcomes.csv의 needed_to_resume를 읽고 마지막 실제 검사 SHA와 작업 파일을 비교한다. 예측은 `9b13473…` 봉인 그대로다.
3. **첫 구체 조사:** 기존5이슈의 공개 편집 이력·당시 editor/build 표기에서 생성 시점 본문과 실제 renderer patch를 복원한다. 가장 먼저 V03 #7507의 실제판을 확인한다. 그 결과로5.1 연구판 재생이 작성자의 판과 연결되는지, 아니면2.7처럼 해당 조작이 없는지를 가를 수 있다. 다음 입력/기대 결과는 아래 표와 같다. 새 공식 작업 ID는 아직 배정되지 않았다.

| 요구 | 다음에 직접 열 자료/파일 | 판정을 바꾸는 최소 입력 |
| --- | --- | --- |
| V03 | [#7507](https://github.com/vega/vega-lite/issues/7507) 생성 본문·편집 이력·당시 renderer build 단서, replay/inputs/V03-original.json |실제 compiler/runtime patch와 같은10행 A/B SVG·색 목록. schema2 표기만으로판정하지 않음 |
| V01 | [#7278](https://github.com/vega/vega-lite/issues/7278) asset135행 및 당시 barley snapshot, outcomes의4셀 |동일판에서 resolve/집계 고정 후3alias A 대direct B 전체 출력. 다른 ecommerce 변형을 대신 넣지 않음 |
| V02 | [#7422](https://github.com/vega/vega-lite/issues/7422) 원repeat·작성자 원정상·실제patch |exact fieldTitle callback A와 escape제거 B의 원입력 전체 출력. 연구자 정상 복사본과 분리 |
| L01 | [#588](https://github.com/libass/libass/issues/588) 완성 ASS/video/frame/띠/폰트·build, operation-refinements |중앙 B의 수치·block 측정/분기 규칙을 새 프로토콜에 먼저 동결한 뒤 정상/경계 A/B 출력 |
| L02 | [#685](https://github.com/libass/libass/issues/685) VLC 포함 libass commit, font/PlayRes/frame, 원정상 fixture |흰 event B MarginV 실제값·0~5초의 내용/alpha/timing을 보존한 분리 출력. 새값 선택은 새 봉인 |
| L03 | frame.csv와 streams/libass/selection.md의 기존18후보 최초 본문 |사전기준 안 정상/경계·보존 목표가 있고 답이 초기 본문에 없는 세 번째 요구. 없으면 빈자리를 유지 |

4. 승인 대기는 없다. 자료·프로토콜 결손이 남아 완전 충족을 보류한다. 규칙/표본/수치 선택을 바꾸는 경우 그때까지 본 결과와 전후 규칙을 새 사전 기록으로 분리하고 현재 봉인을 덮어쓰지 않는다. 같은 예측이라는 기록은 새 후속 그림이 생겨도 바뀌지 않으므로, D 고유의 다른 예측을 시험하려면 별도 사전 비교가 필요하다.
5. 의존 입력은 위049 고정판 두 개에 모두 있다. 같은 차수 다른 결과를 기다릴 필요는 없다.

새 세션은 이 파일을 자동으로 읽는다고 가정하지 않는다. 브랜치와 고정 SHA를 직접 열어 이어간다. 아래 세 약점이 해결되지 않으면 완전 충족으로 표시하지 않는다.

### 가장 중요한 불일치·약점 3건

| 불일치·약점 | 영향받는 주장 | 근거 주소·행 | 다음 최소 조사 | 판정이 바뀔 조건 |
| --- | --- | --- | --- | --- |
| 6자리 중1미충원, 최초 본문/실제판 미복원; L02 정상은 연구자 보충 | 여섯 새 요구·당시 동일판을 대표한 비교라는 주장 | [frame.csv](frame.csv) 데이터1~59행; [#685 본문](https://github.com/libass/libass/issues/685); [source-counts](evidence/source-counts.json) requester5/6 | 기존 모집틀의 최초 본문 및 작성자 build·원정상 fixture 확보 | 정해 둔 기준 안 세 번째 libass 요구와 역사판/정상 입력이 복원돼 새 사전 비교를 할 수 있음 |
| 정확 후속20셀은 미확인이고 L01/L02 B값도 사전 미고정; V01 후속은 입력·조작 불일치 | 두 조작의 실제 승패·공개 후속 검증 및 완전 충족 | [outcomes.csv](outcomes.csv)18행; [V01 변형](https://github.com/vega/vega-lite/issues/7278#issuecomment-792800527); [L02 답](https://github.com/libass/libass/issues/685#issuecomment-1454495083) | 원판·입력·수치A/B를 붙인 정상/경계 출력/고정시험 확보; 새 수치 선택은 별도 봉인 | 같은 조건의 실제 관측이 두 조작을 가르고, 자료 배당까지 충족. 자체 재생만으로 역사판 결손이 사라지지 않음 |
| I/D 예측이 모두 같고 동일 작성자·창밖 노출·검색순서 제한이 남음 | D 내용 자체가 I보다 새 판별력을 주거나 사람의 시간/창의성을 높인다는 주장 | [cards.csv](cards.csv)18행 prior_exposure/outside_window; [predictions.csv](predictions.csv)18행; [노출 기록](evidence/search-and-exposure.json) | 다른 예측을 만들 수 있는 조건을 새로 사전 고정하고, 순서/노출을 분리한 관측 설계 | I가 내지 못한 D의 서로 다른 사전 예측과 이를 가르는 직접 출력이 함께 생김. 현재5/5 예측 일치만으로 효과 우열은 결정되지 않음 |
