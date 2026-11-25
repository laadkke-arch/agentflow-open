# AF-RES-265 인계

## 완료한 결과와 미확인 범위

**작업자 자체 상태 REVIEW_READY.** 3모델 × 3목적의 지정 9셀과 18/18회 실행을 완료했다. 세 원본 GLB를 고정 GitHub tree blob과 정확한 길이·SHA-256으로 확인했다. 두 파서의 chunk·기하와 실제 Three 배열이 맞았고, 새 오프라인 컨텍스트에서 GLB 하나로 표시한 6/6회에 추가 모델 파일 요청은 0이었다. R/O 프레임 6/6쌍에서 픽셀이 같았다. 통제 30회, 직접 원자료 25개, EPUB 두 로컬 추출 경로와 빈 폴더 재생까지 완료했다. [고정 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/28973f6f7e17b738ca5a9feb7f984498e2330bd1/docs/workstreams/research/AF-RES-265/RESULT.md), [고정 SELF_CHECK](https://github.com/laadkke-arch/agentflow-open/blob/28973f6f7e17b738ca5a9feb7f984498e2330bd1/docs/workstreams/research/AF-RES-265/SELF_CHECK.md)

Lamp GLB 7,833,440 B 안의 PNG 4개가 공식 분리 PNG와 같은 바이트였다. 원본 KTX2는 디코더 미등록이면 전체 오류, 등록하되 WASM만 누락하면 onLoad·draw와 텍스처 저하가 함께 일어났다. 별도 PNG판과 optional 두 source의 capability fallback은 각각 분리해 실측했다. BoxTextured의 PNG 누락도 흰 표면으로 draw가 남았다. [Lamp GLB 실행](https://github.com/laadkke-arch/agentflow-open/blob/28973f6f7e17b738ca5a9feb7f984498e2330bd1/docs/workstreams/research/AF-RES-265/receipts/round-2/Lamp-O.json), [대조 회차](https://github.com/laadkke-arch/agentflow-open/blob/28973f6f7e17b738ca5a9feb7f984498e2330bd1/docs/workstreams/research/AF-RES-265/runs.csv)

Chromium에서 일부 200 뒤의 종료 이벤트가 달라진 원인은 미확인이다. 두 번째 폴더에서 서버 payload, 요청과 응답 상태, geometry·decode·선택·픽셀은 일치했다. 작가의 HDR/ACES 장면, 타 로더·하드웨어, EPUB 원 배포 ZIP 및 실제 reader 코덱 선택은 표본 밖이다. 별도 모델/사람의 독립 검토는 미실시다. [판정 정정](https://github.com/laadkke-arch/agentflow-open/blob/28973f6f7e17b738ca5a9feb7f984498e2330bd1/docs/workstreams/research/AF-RES-265/COUNTEREXAMPLES.md), [빈 폴더 비교](https://github.com/laadkke-arch/agentflow-open/blob/07a4c83cc6c3823ac48472abe2f94b6bf4b46efc/docs/workstreams/research/AF-RES-265/receipts/fixed-replay.json)

## 식별과 보관

| 항목 | 확인값 |
| --- | --- |
| 배정 | AF-RES-265, attempt 1, Codex Cloud 실행·검사 |
| 저장소 / 작업 판 | `laadkke-arch/agentflow-open` / `work/research-af-res-265` |
| 시작 / 의존 | 통합 `c64c54d2aae4045b0e2a28a1fdfca9f9313de765` / AF-RES-247 `72657241644860b35c01c5ab7a68ff2e9b7db6b5` |
| 사전 합격표 / 원 측정 | `ffe11059acf34169890e49fcea5df835f2a2bf7f` / `7c002297b6f2fa7ebeaf74b7e623be757463872c` |
| 고정 결과 SHA | `28973f6f7e17b738ca5a9feb7f984498e2330bd1` |
| 고정 결과 검사·재생 원본 | `07a4c83cc6c3823ac48472abe2f94b6bf4b46efc` |
| 편집 범위 | `docs/workstreams/research/AF-RES-265/` |
| 최종 인계 | 이 파일만 추가한 마지막 커밋. GitHub 작업 브랜치 head에서 조회 |

고정 결과 SHA에 [chunks.csv](https://github.com/laadkke-arch/agentflow-open/blob/28973f6f7e17b738ca5a9feb7f984498e2330bd1/docs/workstreams/research/AF-RES-265/chunks.csv), [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/28973f6f7e17b738ca5a9feb7f984498e2330bd1/docs/workstreams/research/AF-RES-265/sources.jsonl), [replay.md](https://github.com/laadkke-arch/agentflow-open/blob/28973f6f7e17b738ca5a9feb7f984498e2330bd1/docs/workstreams/research/AF-RES-265/replay.md)와 실행 코드·원영수증이 있다. [SCOPE의 판 대조](https://github.com/laadkke-arch/agentflow-open/blob/07a4c83cc6c3823ac48472abe2f94b6bf4b46efc/docs/workstreams/research/AF-RES-265/SCOPE.md), [고정판 전체 파일 SHA-256](https://github.com/laadkke-arch/agentflow-open/blob/07a4c83cc6c3823ac48472abe2f94b6bf4b46efc/docs/workstreams/research/AF-RES-265/receipts/result-sha256.json)

## 실행 확인

- 2026-11-25 01:36 UTC, 고정 결과 `28973f6…`의 깨끗한 checkout에서 `python -m workbench.session check docs/workstreams/research/AF-RES-265/session.json --fetch` 종료 0, `passed`, `remote_checked`. 그때 통합 head는 `617a47d5b396d82e22a1544ae5eb0928dfa06a3b`. 계약·의존 일치, outside_paths 0이었다.
- 같은 SHA에서 `python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` 종료 0. 내부 `scripts/check.py --require-git`의 공통 55, repo-intake 7, reference-audit 9 tests, export·bundle, discovery와 smoke를 실행했다. 일괄 `check-all`의 `no_active_sessions`는 전역 manifest 미등록이며 위 개별 검사를 별도로 시행했다. 같은 SHA에서 결과 감사와 `git diff --check`도 종료 0이었다. [공통·개별 명령과 원출력](https://github.com/laadkke-arch/agentflow-open/blob/07a4c83cc6c3823ac48472abe2f94b6bf4b46efc/docs/workstreams/research/AF-RES-265/receipts/repo-check.json)
- 같은 고정 결과만 `git archive`로 빈 폴더에 펼쳐 대표 11개와 probe를 재생했다. 실행 종료 0, 60개 원본/런타임 파일과 EPUB 지문 및 12 브라우저 case의 주요 판정이 일치했다. 앞선 별도 폴더에서는 48+2 case를 모두 수행했다. 최초 엄격 비교 exit 1과 종료 이벤트 차이는 직접 남겼고, 주요 판정 대조는 exit 0이었다. [고정판 재생](https://github.com/laadkke-arch/agentflow-open/blob/07a4c83cc6c3823ac48472abe2f94b6bf4b46efc/docs/workstreams/research/AF-RES-265/receipts/fixed-replay.json), [전체 재생 원문](https://github.com/laadkke-arch/agentflow-open/blob/28973f6f7e17b738ca5a9feb7f984498e2330bd1/docs/workstreams/research/AF-RES-265/receipts/clean-replay.json)

## 다음 첫 행동과 색인 제안

통합 검토자는 지정 브랜치 head를 읽고 `RESULT.md` 표의 Lamp PNG/KTX2 결과와 실행 영수증을 먼저 대조한다. 같은 환경에서 판정을 재현할 입력과 명령은 아래와 같다. 이전 실행 폴더를 재사용하지 않는다.

```sh
git fetch origin work/research-af-res-265
p=docs/workstreams/research/AF-RES-265
result=28973f6f7e17b738ca5a9feb7f984498e2330bd1
replay=$(mktemp -d)
mkdir "$replay/export"
git archive "$result" "$p" | tar -x -C "$replay/export"
bash "$replay/export/$p/tools/replay.sh" "$replay/input" representative
```

다른 로더에서의 fallback 확인을 시작할 때는 `ktx-wasm-absent`와 `fallback-ktx-absent`의 같은 파일 제공표부터 복제한다. 성공 표면이 돌아온다면 해당 로더의 복구 규칙을 별도 근거로 추가한다. 종료 이벤트 조사에는 `receipts/round-2/Lamp-O.json`과 `receipts/fixed-examples/Lamp-O.json`의 같은 GLB를 첫 입력으로 쓴다.

색인 문구 제안은 “3D 자산의 컨테이너 원바이트, 소비한 기하·재질과 오프라인 표시를 같은 고정판에서 분리 검증한 AF-RES-265. 선행 AF-RES-247의 Lamp·실행 공석 보완. EPUB OPF→spine→media의 실제 포함을 두 추출 경로로 비교.”다.
