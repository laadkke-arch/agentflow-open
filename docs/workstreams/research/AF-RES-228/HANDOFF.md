# AF-RES-228 HANDOFF

**DONE · 시도 1 · Codex Cloud의 일회용 Linux 컨테이너에서 실행.** FreshRSS 1.29.1 SQLite에 비식별 공개 자료 두 개를 8회 수신했다. 관측 20/20, 지정 통제 3/3, 새 빈 컨테이너에서 양성·음성 2/2다. 별도 평가자에 의한 독립 검토는 미실시다.

- 저장소와 브랜치는 `laadkke-arch/agentflow-open`의 `work/research-af-res-228`. 작업 시작 통합 SHA는 `f3895893e32e2c055cefde446d34f1467fa27b4c`다. 계약 검사 때 최신 통합 SHA는 `914dbfa789ebec97063ed97130ea2a71c2e9f503`였다. 두 판의 차이는 중앙 진행표에서 다른 작업의 후속을 기록한 2개 커밋이며 228과 215 레코드 및 검사 계약은 같았다. [시작점·선정 규칙](SCOPE.md), [설치·작업 계약](session.json).
- 의존 AF-RES-215 SHA는 `58102fdacb7ac32ffcdacc08a55025612fdc7ebc`. 중앙 DONE과 215 인계 자체 PARTIAL의 경계를 유지한다. 215의 S02/S03를 정확 blob으로 사용했고, 216–218은 입력 범위 밖이다. [215 인계](https://github.com/laadkke-arch/agentflow-open/blob/58102fdacb7ac32ffcdacc08a55025612fdc7ebc/docs/workstreams/research/AF-RES-215/HANDOFF.md), [입력 및 핀](inputs.json).
- **검사한 결과판**은 `e0d151c1d0565631c31196e2c3067fa79643947a`다. 결과판에는 47개 변경 파일이 모두 소유 경로 아래에 있다. 이 인계는 그 결과판에 뒤따르는 단독 커밋이다. [고정 결과판](https://github.com/laadkke-arch/agentflow-open/tree/e0d151c1d0565631c31196e2c3067fa79643947a/docs/workstreams/research/AF-RES-228).

| 묶음 | GitHub 커밋 |
| --- | --- |
| 범위·사전 예측·세션 핀 | [91801fdc](https://github.com/laadkke-arch/agentflow-open/commit/91801fdc085811071d754a6baf76d15fc2a57b13) |
| 직접 자료·원바이트·수신 전 수정 예측 | [48ce2028](https://github.com/laadkke-arch/agentflow-open/commit/48ce20281cb2bb983c2dfe2f3af87cc7aa650482) |
| 네 DB·원형 8회·표 1 | [bb22a4f7](https://github.com/laadkke-arch/agentflow-open/commit/bb22a4f751a38f5425b1a7d9e3ec4234ca45266d) |
| 통제 14회·별도 재생 2회·정정 | [419285c2](https://github.com/laadkke-arch/agentflow-open/commit/419285c2d7b9dbed281d4904655b88b349262244) |
| 필수 표·Q1–Q7·자체 점검 | [e0d151c1](https://github.com/laadkke-arch/agentflow-open/commit/e0d151c1d0565631c31196e2c3067fa79643947a) |

## 결과와 대표 파일

- 세 항목의 명시 read는 두 설정 모두 1이다. 두 누락 항목은 reception=false에서 0, true에서 1이다. 가공한 unread 상태 토큰의 값은 0, 가공한 `read:false`는 수신 미지원이라 reception=true에서 1이다. 원형 열 자리의 재수입에서 ID·URL·별표·태그 관계가 유지됐고 lastSeen은 양수에서 0이 됐다. 수신에서 상태를 수정한 뒤 같은 파일을 넣으면 같은 ID의 읽음·별표가 덮이고 삭제한 발신 라벨이 복구됐다. 로컬 태그는 유지됐다. [RESULT.md](RESULT.md), [observed.csv](observed.csv), [controls.csv](controls.csv), [SQLite schema](schema.sql).
- 한 파일의 교차 GUID 통제는 3피드·2행과 글 오연결을 보였다. 같은 데이터를 둘로 나누면 3행이었다. 두 링크가 다르면 alternate가 쓰였고 canonical만 남긴 경우 빈 링크가 저장됐다. 중립 파일명에서도 명시 별표는 적재됐으며 토큰이 없는 무라벨 글의 별표 값은 전체 CLI 경로에 따라 바뀌었다. [통제 영수증](receipts/C1-collision.json), [파일과 판정](controls.csv), [새 컨테이너](receipts/container-replay.json).
- 52개 원장 행 중 직접 산입은 고유 원자료 48건, 계보 9개다. 사용자 원보고 네 건 가운데 실제 가져오기 시도는 세 건이다. 같은 Inoreader→FreshRSS 1.29.1 계정의 옛 실제 사용자 관측은 0건이다. 확인한 실험과 원사용자 이전 여부는 각각 기록했다. [자료 원장](sources.jsonl), [분모와 Q별 자체 점검](SELF_CHECK.md).

## 실행과 검사 범위

- 소스는 FreshRSS `b2c50115baa36c217e939ee3ea8ecfae52f91abd`, Git archive SHA-256 `08cd6247981819cefc6acb641b570c2b3042a021539045cbfbf2d7c541ccc73a`다. 공식 install/create-user/import-for-user를 새 데이터 경로에서 호출했고 PHP 8.4.28과 PDO SQLite 3.46.1을 확인했다. 주실험·통제·재생의 24개 import는 모두 exit 0이다. 앱 로그와 strace는 초회 새 피드의 아이콘 요청 시도와 실제 외부 통신 결과를 구분한다. 외부 HTTP 성공 0, 구독 갱신 미실시다. 첫 bind 권한 실패와 앱 로그 수집을 고치기 전 원형 검산 8회는 별도 영수증에 보존했다. [실행기](run.py), [기준 실행 환경](receipts/runtime-main.json), [주실험](receipts/container-main.json), [준비 실패·검산](receipts/preflight-main/).
- 결과 SHA를 GitHub에서 새로 clone한 뒤 파일 두 개를 upstream 바이트와 다시 대조했다. 20행의 피드·GUID·ID·URL·read·favorite·태그 및 재수입 lastSeen을 영수증과 대조했다. 통제·재생 표의 14개 영수증과 16개 호출, 필수 표의 행 수·열 이름, Q1–Q7, 마지막 약점 3행, 로컬 링크 대상과 소유 경로를 검사했다. 모두 일치했다. 이 점검과 재생은 작성자가 수행했다.
- `python -m workbench.session check docs/workstreams/research/AF-RES-228/session.json --fetch`는 2026-11-24 22:36:49 UTC에 exit 0, `passed`, `remote_checked`였다. 소유 경로 밖 0, 충돌 0, 오류 0이다. manifest 자체를 제외한 변경 46건과 정확한 215 의존 SHA를 검사했다.
- `python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean`는 결과판에서 exit 0이었다. doctor, acceptance 안의 `scripts/check.py --require-git`와 55/7/9 테스트, reference-audit discovery, original-smoke가 통과했다. 공통 `check-all`은 `docs/tasks/`의 활성 manifest가 없어 `no_active_sessions`였다. 228의 소유 경로 manifest는 이전 항목의 개별 검사에서 원격 확인했다. GitHub Actions와 Windows 재실행은 미실시다. 이 검사는 결과 SHA를 대상으로 했으며 이 인계의 문서 커밋과 구별한다.

## 첫 후속 행동과 색인 제안

1. 통합 담당자는 GitHub에서 브랜치 마지막 인계와 결과 SHA `e0d151c1d0565631c31196e2c3067fa79643947a`를 확인하고 215 항목 아래에 별표 파일 재생 근거를 연결한다. 색인 문구 제안은 “고정 1.29.1 SQLite, 원형 8회/20자리, 누락 read는 reception 의존, 재수입 메타데이터와 사용자 상태 변경 있음”이다. 조회 경로는 [결과](RESULT.md), [목적별 안내](advice.md), [실험 경계](SELF_CHECK.md)다.
2. 실계정에서 과거 안읽음 근거까지 확인해야 한다면 첫 조사는 발신 상태를 사전에 아는 공개 비식별 입력 한 건에서 원 JSON의 상태 토큰을 대조하는 것이다. 같은 GUID의 실제 발생이나 `lastSeen`이 정리 조건에 미치는 결과가 필요하면 RESULT 마지막 표의 특정 검사에서 재개한다. 파일·SQLite·FreshRSS 판이 다르면 별도 결과로 표시한다.
3. 재실행은 [고정 표본 재생 명령](advice.md#고정-표본을-다시-실행하는-명령)의 소스 checkout과 Docker build 뒤 `run.py main`, `controls`, `replay` 순서다. 입력은 [S02](fixtures/S02/starred.json), [S03](fixtures/S03/starred-inoreader.json) 그대로다. 첫 기대 결과는 `{"group":"main","cases":4,"failed":[]}`와 20개의 CSV 자리다.
