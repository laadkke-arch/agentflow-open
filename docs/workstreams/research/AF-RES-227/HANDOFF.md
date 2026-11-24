# AF-RES-227 HANDOFF

## 1. 식별

- 상태 **REVIEW_READY**. AF-RES-227 시도 1. Codex Cloud Linux x86-64에서 수행했다.
- 작업 브랜치 `work/research-af-res-227`. 소유 경로 `docs/workstreams/research/AF-RES-227/`.
- 계획 통합판 `fc095c323d0177401d34f1daa7b4d1c529e2351f`. 시작 통합판 `f3895893e32e2c055cefde446d34f1467fa27b4c`.
- 직접 의존 AF-RES-210 `097948b68f3be1802c06c15c7beccaeb5478c06c`. 시작 계약과 마지막 원격 검사에서 같은 의존 SHA를 확인했다. [세션 계약](session.json)
- **고정 결과 커밋 `70b89c4f71c7638fe75ed0b17a42e2a9f7c702c1`**. 이 인계를 붙이기 직전의 결과판이며 GitHub에서 별도 checkout으로 다시 읽었다. [고정 결과판](https://github.com/laadkke-arch/agentflow-open/commit/70b89c4f71c7638fe75ed0b17a42e2a9f7c702c1)

## 2. 확인한 결과

- 기본 64/64, 표시 112/112, 추가 통제 22/22, 진단 144/144가 유효했고 독립 경로 재실행과 일치했다. 순정 64자리는 두 반복의 같은 32쌍·방법 셀이다. 공개 suite 5/5 및 LIS 별도 실행 1/1도 재생했다. 직접 연구 원문은 29건, 출전 계보 묶음은 15개다. [RESULT.md](RESULT.md) · [자료 원장](sources.jsonl) · [재생 대조](receipts/replay-summary.json)
- C1의 Git patience classic 후퇴와 histogram의 직접 영역은 같은 stdout을 냈다. Breezy Python은 반복행을 매치하지 않아 전체 교체를 냈다. C2에서 Git은 B(2,1), Breezy는 A(1,2)를 유지했다. hunk 범위와 편집 수는 같았고 내용은 달랐다. R4의 histogram c(5,4)는 compaction 이후 c(5,5)가 되었다. C4는 같은 앵커와 다른 context를 확인했다. [앵커](anchors.csv) · [원영수증 행렬](matrix.csv) · [반례와 정정](COUNTEREXAMPLES.md)

## 3. 고정 결과판 검사

| 실행 | 실제 판정 | 근거 |
| --- | --- | --- |
| `python -B -m workbench.session check docs/workstreams/research/AF-RES-227/session.json --fetch` | exit 0, `passed`, `remote_checked`, 2026-11-24T22:44:23Z | 통합 SHA `de683d7e8319974618062d191a7cc2dace103cae`, 계약 버전 2 및 의존 SHA 유지, 범위 밖·미병합 0. 작업 manifest를 따로 두고 검사기가 변경 55개를 확인했다. 별도 Git diff는 manifest 포함 56개 모두 소유 경로였다. stdout SHA-256 `baa3da9ac862039b6aa2d6d7da4b5a408f912c4525c7fdfdf5df0fa9b1a44e9d`. |
| `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | exit 0, 시작·종료 clean | doctor, acceptance, research-case 통과. 전체 큐는 `no_active_sessions`로 개별 작업 검사는 위 명령에서 실행했다. 검사 receipt SHA-256 `2cd3e0647cb73da977eb50d6f6289968e7fe207b459bba8e7cfee935176b65f8`. |
| `python -B scripts/check.py --require-git` | exit 0 | 공통 테스트 55, repo-intake 7, reference-audit 9, demo·export와 고정 SHA Git bundle 복원을 확인했다. stdout SHA-256 `c050d2cc1b4a9359628b57f1d8a19d3f8ce9a3778bb5ca58048b336775b838cd`. |
| 고정 결과판 원자료 대조 | 완료 | Q1–Q7 근거와 반증 조건, 예측 32행, 표의 순서, 두 경로의 replay 및 matrix·anchors 재생성 일치를 확인했다. [SELF_CHECK.md](SELF_CHECK.md) |

최초 계약 검사에서는 `.git` 접미사가 붙은 원격 주소의 HTTPS 요청이 401이라 exit 2를 받았다. 검증용 checkout에서 같은 공개 저장소의 `https://github.com/laadkke-arch/agentflow-open`으로 다시 가져와 위 원격 검사를 통과했다. 시작 이후 통합판의 변경은 중앙 진행표 한 파일이었다. 작업의 결과판 변경 범위는 소유 경로다.

## 4. 남은 확인과 다음 첫 행동

- 독립 경로 재생과 자체점검을 실시했다. 독립 평가자 검토, 사람의 가독성 효과 측정, 다른 OS에서의 자체 실행은 미실시다. Breezy 공식 suite의 C 관련 12 skip 및 Sage 자체 실행 범위는 [SELF_CHECK.md](SELF_CHECK.md)에 있다. Fredman 본문 열기 실패와 대체 원전은 [sources.jsonl](sources.jsonl)에 있다.
- 다음 검토자는 작업 브랜치와 위 고정 결과 SHA를 확인하고 [REPLAY.md](REPLAY.md)의 저장된 영수증 대조 명령부터 실행한다. 이어 [C2 원계측](receipts/diagnostic-base.jsonl#L21-L24)의 서로 다른 길이 1 증인과 [R4 histogram](receipts/diagnostic-base.jsonl#L14)의 pre/post 마스크를 확인한다. 다른 stdout과 trace가 나오면 같은 입력 SHA·엔진 tag·방향·context·indent부터 대조한다.
- 색인 반영 제안 **AF-RES-227 / REVIEW_READY / 동률·후퇴와 hunk 비교 / RESULT.md·anchors.csv·replay-summary / AF-RES-210 고정 의존**. 검토용 링크는 [정책과 표시 목적별 원문](advice.md)에 있다.
