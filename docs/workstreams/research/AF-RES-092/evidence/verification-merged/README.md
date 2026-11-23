# 합류 결과 SHA의 검증 영수증

검사 대상은 **dbf432a7fefc556e9da08a645a017ca37464cf3e**이며, 원격 브랜치에 게시한 뒤 같은 SHA의 clean worktree에서 실행했다. 이 뒤의 영수증 보존·최종 HANDOFF 커밋을 검사 대상이라고 소급하지 않는다. 앞선 b40 검사는 [별도 원 영수증](../verification/README.md)에, 병행707 검사는 e0d7의 역사적 HANDOFF 기록에 남아 있다.

|실시한 검사|UTC 시각·종료값|확인 범위|
|---|---|---|
|`python -B docs/workstreams/research/AF-RES-092/audit.py`|2026-11-23 17:35:07, exit0|6질문/12경로, 봉인4파일 불변, 원장123/산입40/저작사건29/계보33, 재열람 메타데이터 일관성|
|`python -B -m workbench.session check docs/workstreams/research/AF-RES-092/manifest.json --fetch`|17:35:07–17:35:15, exit0|remote_checked; 통합e2a80afec762b10ee7979136c6332473c70905bb; 계약19f08ce… 동일; 변경140파일 모두 허용경로; outside/unmerged/errors 모두 빈 배열|
|`python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean`|17:35:15–17:35:25, exit0|source_start/source_end 모두 정확 결과SHA, clean; doctor/acceptance/research-case/original-smoke/sessions 명령 종료0|
|GitHub 불변 SHA 원격 재열람|[remote-readback.json](remote-readback.json)|11파일 blob 일치; 필수 표6/12/6행,5/7/6열; 원장·결과·outcomes·기존 최초답/댓글/상류 영수증 연결; dot-control 미변경|

공통 내부 `sessions`의 실제 payload는 **not-executed / no_active_sessions / count0**다. 명령 종료0을 활성 세션 검증으로 보고하지 않는다. AF092의 개별 manifest 검사는 위 두 번째 행에서 따로 실제 실행했다. `codex-cloud`는 호출자 환경 라벨이다.

## 환경과 원 로그

전체 Git 이력(shallow=false)을 사용했고, TMPDIR/TEMP/TMP를 환경에서 제거하여 OS 기본 임시 디렉터리를 썼다. 원 소스·검사기·시간 제한을 수정하지 않았다. `run-summary.json`은 세 명령의 전체 인수·대상SHA·시각·시간·종료값을, `cloud.receipt.json`은 공통 검사 시작/끝의 소스·개별 검사를 담는다. stdout/stderr 원문을 이 폴더에 복사했고 `log-index.json`에 원 receipt의 경로와 보존 파일·SHA256을 대응시켰다.

원격 재열람 중 존재하지 않는 집계 파일명 `evidence/upstream/receipts.json`을 요청해404를 받았다. 실제 개별 원자료 영수증 `pandoc-test_command_6836.md.receipt.json`으로 바로잡아 성공했다. 실패를 재열람 영수증에 남겼으며 새 원자료나 A/B 예산으로 세지 않았다.

## 이 검사로 확인하지 않은 범위

검사는 workbench·계약·자료 구조와 커밋된 내용의 일치를 확인한다. 원 질문자의 실제 jq/Pandoc/Quarto 정확판 변환, P1 글리프/PDF/HTML, P2 원 생성tex/PDF, P3 원 전체입력 AST·서지 출력은 실행하지 않았다. 공개 원문은 이미 보존한 최초판·댓글 해시와 같은 blob인지 확인했으며, b40의 외부 원문 재열람은 [primary-readback.json](../verification/primary-readback.json)에 보존돼 있다. 이 문헌·구조 검증은 원 사용자 목적 달성의 실행 인증이 아니다. 연구 상태 **PARTIAL**은 유지한다.
