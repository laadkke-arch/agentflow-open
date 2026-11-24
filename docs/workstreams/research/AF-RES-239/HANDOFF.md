# AF-RES-239 인계

## 1. 식별

- 작업 AF-RES-239, 시도 1. 상태 **DONE**. Codex Cloud 실행·자체 검산 완료, 별도 독립 검토 미실시.
- 저장소 `laadkke-arch/agentflow-open`, 브랜치 `work/research-af-res-239`, 허용 경로 `docs/workstreams/research/AF-RES-239/`.
- 착수 통합 SHA `64e139f16309e41e30f9ec634eabe17fef908bbd`, 결과 고정 SHA `64b2d5a90e3b73c7ff0c197ddfb75bbcc0b4aa93`. 결과판을 GitHub에서 새 checkout하여 2026-11-24 23:25–23:26 UTC에 확인하고 이 파일만 마지막 커밋에 저장했다. [고정 결과 디렉터리](https://github.com/laadkke-arch/agentflow-open/tree/64b2d5a90e3b73c7ff0c197ddfb75bbcc0b4aa93/docs/workstreams/research/AF-RES-239)
- 시작 시 47차 지정 계획 SHA `914dbfa…`에는 239 항목이 없었고 5개 커밋 뒤 배정이 생겼다. 최종 검사에서 통합 head `7369707441e2eb70e84004ca6cb3bfeefc8b4061`를 보았으며 시작 이후 차이는 다른 작업의 진행표 갱신이었다. 239·221의 입력/의존과 공통 계약은 같았다. [범위와 시작판](https://github.com/laadkke-arch/agentflow-open/blob/a9f2e1250ed1182f5a7c2f9d5d02d6c266988880/docs/workstreams/research/AF-RES-239/SCOPE.md)

## 2. 입력과 결과

직접 의존은 221 `78a561e00cb9130430bdee7b5c053f740122e973`이다. 중앙 상태는 DONE, 221 작성자의 인계는 PARTIAL로 기록되어 있다. 221의 정적 M/P/I/E와 미달을 그대로 두고 실행으로 빈 좌표를 채웠다. C1–C5와 R1/R2 전체 배열을 고정하고 각 선택 quad의 두 제품 실제 연결을 판정했다. [221 고정 인계](https://github.com/laadkke-arch/agentflow-open/blob/78a561e00cb9130430bdee7b5c053f740122e973/docs/workstreams/research/AF-RES-221/HANDOFF.md)

- C3 `[[8,-4],[-3,1]]`, L=0에서 scikit-image 0.25.2는 두 번 모두 A=N–W+E–S였고 ContourPy 1.3.3 serial은 B=N–E+S–W였다. C3 평균 +0.5와 안장 −0.25가 반대다. 두 제품의 보간 끝점은 일치 범위였으며 실제 연결이 갈렸다. C2가 scikit-image의 A를 일반 쌍선형 규칙으로 해석하는 반례다.
- C4 두 제품은 정확 동률에서 두 개의 A 선, 쌍선형은 중앙을 공유하는 X다. NW ±2⁻²⁰ 입력에서 ContourPy A/B, scikit-image A/A. C3/C4는 별도 경계법으로 8/8 원반환을 읽었다.
- R1 고정 기대 25개 정점은 high orientation을 역순으로 비교했고 E–S였다. R2는 `(0,0)` N–W가 같아도 전체 `(1,1)`에서는 B/A였다. 같은 엔진의 다른 형식 비교는 R2의 공개 고정 좌표 정답을 제공하지 않는다.
- 기본 호출 28/28, 별도 통제 23/23, 원형 3/3, 4/8 라벨 2/2, 저장된 깨끗한 재생 8/8, 결측 0. 14 입력–엔진 조건의 M/P/I는 14/14 일치했다. 이 중 사전 10, 동시 노출 후 재구성 4다. E 고정 1/1과 독립 블라인드 분모 0을 분리했다. 원장 44행 중 고유 산입 29개·11계보, 본문 미확인 8행.

## 3. 고정 파일과 커밋

| 대표 파일 | 확인 항목 |
|---|---|
| [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/64b2d5a90e3b73c7ff0c197ddfb75bbcc0b4aa93/docs/workstreams/research/AF-RES-239/RESULT.md) | 필수 표 2개, 기본 28행, Q1–Q7, 마지막 약점 3건 |
| [inputs.json](inputs.json), [environment.json](environment.json), [session.json](session.json) | 전체 격자·수준·좌표·해시, 실제 wheel/import, 소유 경로 및 221 고정 |
| [observed.csv](observed.csv), [controls.csv](controls.csv), [receipts](receipts/) | 전체 원반환과 선택 칸, 23통제, 원시험·재생 stdout/stderr |
| [sources.jsonl](sources.jsonl), [COUNTEREXAMPLES.md](COUNTEREXAMPLES.md), [SELF_CHECK.md](SELF_CHECK.md) | 원출처, 실패 경로, 독립 경계식 검산 및 범위 |
| [run.py](run.py), [analyze.py](analyze.py), [verify.py](verify.py), [requirements.lock](requirements.lock) | 정상 API, 클립, 별도 검산, Linux cp312 잠금 |

① `a9f2e1250ed1182f5a7c2f9d5d02d6c266988880` 범위·예측, ② `b14749fda1c6d63770b8cbca0cb8af67219637b7` 원장·영수증, ③ `ab437611d8916101ab941f16f9835874622210d5` 필수 표·주관측, ④ `55944e8d99341a22749742d7a8ad717bfb1ee018` 반례·재생, ⑤ `64b2d5a90e3b73c7ff0c197ddfb75bbcc0b4aa93` RESULT/SELF_CHECK. 고정 트리의 새 경로 100개가 모두 허용 경로에 있었다. `dot-control.json`의 작업 브랜치 diff는 비어 있었다.

## 4. 실제 검사

아래 검사는 고정 결과 SHA를 checkout한 상태에서 실행했다. 모든 종료 코드는 실제 값이다.

| 검사 | 종료 · 범위 |
|---|---|
| `python -m workbench.session check docs/workstreams/research/AF-RES-239/session.json --fetch` | 0, `passed / remote_checked`, 검사 2026-11-24T23:25:39.361704Z. 통합 `7369707…`, 계약 SHA-256 `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`, 의존 221 그대로. 작업 manifest를 제외한 99개 변경, 범위 밖/충돌/오류 각각 0 |
| `python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 0, 시작·종료 checkout clean. doctor/acceptance/reference-audit discovery/original-smoke 0. 내부 `python scripts/check.py --require-git`에서 공통 55, 두 lab 7/9, demo, 독립 export, Git bundle 복원 통과. 공통 `check-all` stdout은 `not-executed / no_active_sessions`, 그 조회의 exit는 0. AF-RES-239 소유 경로의 manifest는 위 개별 검사로 검증 |
| 태그 공개 시험 | scikit-image `pytest test_find_contours.py -k 'binary or mask'` exit 0, 7 통과/10 제외. ContourPy의 `test_convert_lines`, `test_dechunk_lines`, `test_z_interp_log_saddle` exit 0, 162 통과. [실행 원영수증](receipts/published-tests/) |
| 새 checkout·별도 가상환경의 대표 8개 재생 | `run.py replay`와 `verify.py --replay-dir` 둘 다 exit 0. C3/C4/R1/R2×2의 dtype/shape/순서/좌표·유효 옵션·입력 바이트 해시 동일. 환경 SHA-256 `3a74bbd270c5539d7c622a24280c4a6222b4f38e5cd588ef5226ed0897660d97`. 이전 clean 재생의 [전체 원스트림](receipts/replay/)과 고정 결과판에서 별도 재실행 |
| GitHub 결과판 재열람·산출물 대조 | 핵심 파일/도구 14개와 폴더 영수증, RESULT 상대 링크 56개, 두 필수 표, Q1–Q7별 근거·반증·미확인, 마지막 3행 검증. C3 A/B 및 C4 A/A, 기본 28·통제 23행. `git diff --check` exit 0 |

고정 결과판 검사 시 session/cloud/replay/verify 바깥 stderr는 모두 0바이트였다. 비교 식별용 stdout SHA-256은 session `7efb61ccfb7367eb54ab4e016625e8720605d52a3231274e43ee65f63c146753`, cloud `7cb4730f93a68f5a80ff0eb027709b7443cef194ad0fe5630ec829059ea8882b`, 최종 clean replay `99355737d7676459668f6e2cff27f4fe9ae3fbb2562e9f9445549e09e7970d3d`다. 공통 검사는 작업환경/계약 구조와 저장소의 예제 범위를 검사한다. 등고선 기하의 증거는 이 작업의 공개 API 영수증과 검산이다.

## 5. 남은 판단과 다음 첫 행동

1. 다음 검토자는 브랜치 GitHub head와 고정 결과 SHA를 확인하고 `RESULT.md` 표 1의 핵심 비교를 C2/C3/C4 원영수증 및 `COUNTEREXAMPLES.md`에서 먼저 교차 판독한다. 검토 전에 R2 (1,1)의 새 고정 참조 및 블라인드 입력을 따로 정하면 동일 엔진 상대 비교의 한계를 점검할 수 있다.
2. 1991 논문 `2에서 점근선 교점 기준을 직접 읽었다. 정확한 p.85 분자 글리프는 스캔에서 재확인하지 못했다. 후속 대소식과 자체 편미분 결과는 C3의 −0.25를 지지한다. 첫 추가 원문 대조는 IEEE VIS DOI `10.1109/VISUAL.1991.175782` p.85 Fig.7과 저자 고해상도 판 또는 정오표로 한다. 동일 좌표 정의에서 인쇄 기호나 변수 정의가 확인될 때 수식 인용을 갱신한다.
3. 실측 DEM 정확도, 2D 엔진 내부 분기 trace, 다른 OS/ABI, R2 렌더러 이미지 재생은 범위에 해당하는 관측이 없다. 원전의 역사적 영향·독자 선호도 221에서 이어 추정하지 않았다. 실제 요구가 쌍선형 지형인지 4/8 픽셀 연결인지 먼저 확정하여 해석한다.

색인에는 221의 정적 C3 예측에서 이 고정 결과판의 실제 좌표로 연결한다. 항목 문구는 “고정판 두 등고선 엔진의 대각 연결 검산, C3 평균/안장 분기, C4 동률, R2 선택/전체 차이”로 제안한다. Linux 범위, 28회, 29개 고유 근거 및 독립 검토 미실시를 함께 표시한다.
