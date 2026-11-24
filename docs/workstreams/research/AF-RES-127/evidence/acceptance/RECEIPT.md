# 고정 결과판 수용 검사

검사한 결과·원장 SHA는 `cee582b227357f5935fd87eaa5e3a0e415d65cc9`다. Codex Cloud에서 같은 작업자가 GitHub로부터 두 새 경로에 각각 clone하고 그 SHA를 checkout했다. 별도 npm cache에서 각자 lock을 설치했다. 두 경로 모두 검사 전후 Git 상태가 깨끗했다. 날짜는 2026-11-24 UTC, 실행환경은 Debian 13 x86_64·Chromium 156.0.8078.79·Node 24.22.1·npm 11.9.0·Python 3.12.14다. [고정 결과판](https://github.com/laadkke-arch/agentflow-open/tree/cee582b227357f5935fd87eaa5e3a0e415d65cc9/docs/workstreams/research/AF-RES-127) · [재현 명령](../../reproduce.md)

| 비교 | 파일럿 / 본행 / 대조 / 보충 | 시각과 환경에 따른 차이 | 명령·원 출력·종료·입력 지문 |
| --- | --- | --- | --- |
| 원장 → 경로 1 | 3/3 · 16/16 · 12/12 · 10/10 | 관측값·순서·PNG·실행 입력 불일치 0. Canvas readback notice의 횟수가 달랐던 행 22. | [명령](route-1/commands.log) · [stdout/stderr와 종료](route-1/steps.json) · [입력 SHA·환경](route-1/input-environment.json) · [행별 비교](route-1/compare.json) |
| 원장 → 경로 2 | 3/3 · 16/16 · 12/12 · 10/10 | 관측값·순서·PNG·실행 입력 불일치 0. 같은 notice 횟수 차이 21행. | [명령](route-2/commands.log) · [stdout/stderr와 종료](route-2/steps.json) · [입력 SHA·환경](route-2/input-environment.json) · [행별 비교](route-2/compare.json) |
| 경로 1 → 경로 2 | 3/3 · 16/16 · 12/12 · 10/10 | 관측값·순서·PNG·실행 입력 불일치 0. 같은 notice 횟수 차이 15행. | [명령·stdout/stderr·종료](cross-command.json) · [행별 직접 대조](cross.json) |

행 대조에서 clockMs·eventTimeMs·timeOriginMs는 시각 필드로 제외했다. Canvas2D의 getImageData 성능 안내는 내용과 횟수를 별도로 기록했다. 외부 요청·페이지 오류·예상 밖 경고 0건이다. 각 행에 raw SHA와 정규화 SHA를 보존했다. 부가 시험의 옵저버 off 두 행은 정착 비교 범위다. 번들 SHA-256은 `285f0b061c10ab7067482208ef49a8e8efe4fcb42a5a48807443b77386734f07`, plan은 `d5786db46c5ad4d078fc8d13197f8d8338df86b360c9127dae91bde4adbd5fc0`, npm lock은 `a5391bf7631df35a628d200e2641956b10f08b6294d2f7d07464af66e013ddb0`이다. [브라우저 비교기](../../replay/compare.py) · [설치판과 소스 지문](../../fixture/fingerprints.json)

고정판에서 두 번 산출한 재집계는 byte 단위로 같았다. SHA-256은 `fb5a08ea39255fed6043a5dee12655bdeb3c8d9628abdf0dbea59c33d294cfbb`다. 출처 37 고유 저작, 필수 표 데이터 3·8·3행, 본 로그 링크 16개, 마지막 약점 3행, 본·대조·보충의 raw/다시 계산한 원장과 PNG를 검산했다. 보충을 포함한 원장 record는 3,818건이다. [고정판 재집계](recount.json) · [검산기](../../replay/audit.py)

| 검사 | 결과·실제 범위 | 로그 |
| --- | --- | --- |
| `python -B -m workbench.session check docs/workstreams/research/AF-RES-127/manifest.json --fetch` | 종료 0, passed, remote_checked. 통합 `4ad08bf17c4b1ff6ac6219293ed9fe875743cf38`, 의존 `7554304d725082275661cdd011ad4f4472a00438`, 계약 version 2. 세션 검사 범위는 manifest 자신을 뺀 85 변경 경로다. Git diff에서 manifest를 포함한 86 파일이 모두 소유 경로에 있다. | [세션 JSON](session.json) · [전체 변경 경로](changed-paths.txt) |
| `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 종료 0. doctor, 공통 acceptance, reference-audit discovery, original smoke를 완료했다. 내부 일괄 세션 검사는 `no_active_sessions`로 미실행이며 위 명시 검사를 따로 실행했다. | [공통 검사 receipt](cloud-check.json) · [경로 1 원 출력](route-1/steps.json) |
| `python -B scripts/check.py --require-git` | 종료 0. 단위 55개·두 lab 단위 7개/9개, demo·독립 export·Git bundle 복원을 검사했다. 새 웹 Pro 인수인계나 제품 검사는 미실행이다. | [경로 1 원 출력](route-1/steps.json) |

이 수용 기록과 후속 HANDOFF는 고정 결과 SHA를 검사한 뒤 저장한 증거다.
